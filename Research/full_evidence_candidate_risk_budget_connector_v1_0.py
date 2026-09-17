"""AI Market Master 3.2 — Candidate v1.0 -> Risk Budget Execution connector.

Step 5 integration layer.

This module connects the validated Candidate Transition Engine v1.0 market target to
the already-frozen Risk Budget Execution v0.1 mapper without changing either side.

Boundaries:
- Candidate decides market action/target.
- Portfolio context decides sleeve composition and separate Core/Leverage authority.
- The connector never invents C1-C8 evidence, Regime, target, Core authority, leverage
  authority, or risk coefficients.
- HOLD/BLOCKED can never become a portfolio trade.
- A REDUCE decision can never cause restoration, and a RESTORE decision can never
  cause reduction, even when actual portfolio risk differs from the logical Candidate
  target because of prior partial execution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional, Tuple

from full_evidence_candidate_input_contract_v1_0 import CandidateInput
from full_evidence_candidate_transition_engine_v1_0 import (
    TransitionDecision,
    evaluate_transition,
)
from risk_budget_execution_v0_1 import MapResult, Sleeves, map_risk_budget

EPS = 1e-9


@dataclass(frozen=True)
class PortfolioExecutionContext:
    """Portfolio-only inputs. Market authority is deliberately absent.

    `core_reduction_authorized` and `leverage_restore_authorized` are independent
    execution authorities already required by Risk Budget Execution v0.1.
    The Candidate decision does not fabricate either one.
    """

    baseline: Sleeves
    current: Sleeves
    core_reduction_authorized: bool = False
    leverage_restore_authorized: bool = False
    risk_coefficients_complete: bool = True

    def validate(self) -> None:
        for name, sleeves in (("baseline", self.baseline), ("current", self.current)):
            if not isinstance(sleeves, Sleeves):
                raise ValueError(f"{name} must be Sleeves")
            if min(sleeves.core, sleeves.tactical, sleeves.leverage) < -EPS:
                raise ValueError(f"{name} sleeve values must be non-negative")

        if abs(self.baseline.total - 100.0) > 1e-6:
            raise ValueError("baseline normalized risk units must total 100")

        for name in (
            "core_reduction_authorized",
            "leverage_restore_authorized",
            "risk_coefficients_complete",
        ):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be boolean")


@dataclass(frozen=True)
class CandidateExecutionResult:
    decision: TransitionDecision
    candidate_target_risk_budget: int
    execution_target_risk_budget: Optional[float]
    before: Sleeves
    after: Sleeves
    integration_status: str
    mapper_status: str
    mapper_actions: Tuple[str, ...]
    unresolved_constraints: Tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "decision": self.decision.to_dict(),
            "candidate_target_risk_budget": self.candidate_target_risk_budget,
            "execution_target_risk_budget": self.execution_target_risk_budget,
            "before": asdict(self.before),
            "after": asdict(self.after),
            "before_total": self.before.total,
            "after_total": self.after.total,
            "integration_status": self.integration_status,
            "mapper_status": self.mapper_status,
            "mapper_actions": list(self.mapper_actions),
            "unresolved_constraints": list(self.unresolved_constraints),
        }


def _unchanged(
    decision: TransitionDecision,
    portfolio: PortfolioExecutionContext,
    *,
    integration_status: str,
    mapper_status: str,
    reason: str,
) -> CandidateExecutionResult:
    return CandidateExecutionResult(
        decision=decision,
        candidate_target_risk_budget=decision.target_risk_budget,
        execution_target_risk_budget=None,
        before=portfolio.current,
        after=portfolio.current,
        integration_status=integration_status,
        mapper_status=mapper_status,
        mapper_actions=(),
        unresolved_constraints=(reason,),
    )


def _bounded_execution_target(
    decision: TransitionDecision,
    current_total: float,
) -> tuple[Optional[float], Optional[str]]:
    """Prevent direction inversion and cap actual movement to Candidate step size.

    Candidate target state and actual portfolio risk can diverge after a prior
    PARTIAL EXECUTION / CORE PROTECTED result. The market target remains unchanged,
    but one connector invocation may not move actual portfolio risk farther than the
    current Candidate decision's frozen allowed_step_size.
    """

    target = float(decision.target_risk_budget)
    step = float(decision.allowed_step_size)

    if decision.action_direction == "REDUCE":
        if current_total <= target + EPS:
            return None, "ALREADY_AT_OR_BELOW_CANDIDATE_TARGET"
        return max(target, current_total - step), None

    if decision.action_direction == "RESTORE":
        if current_total >= target - EPS:
            return None, "ALREADY_AT_OR_ABOVE_CANDIDATE_TARGET"
        return min(target, current_total + step), None

    return None, "NO_EXECUTABLE_CANDIDATE_DIRECTION"


def connect_candidate_to_risk_budget(
    candidate_input: CandidateInput,
    portfolio: PortfolioExecutionContext,
) -> CandidateExecutionResult:
    """Evaluate Candidate v1.0 and map an authorized action into portfolio sleeves."""

    candidate_input.validate()
    portfolio.validate()
    decision = evaluate_transition(candidate_input)

    if decision.action_direction == "BLOCKED":
        return _unchanged(
            decision,
            portfolio,
            integration_status="BLOCKED / NO PORTFOLIO ACTION",
            mapper_status="NOT EXECUTED",
            reason="Candidate input/transition is BLOCKED",
        )

    if decision.action_direction == "HOLD":
        return _unchanged(
            decision,
            portfolio,
            integration_status="HOLD / NO PORTFOLIO ACTION",
            mapper_status="NOT EXECUTED",
            reason="Candidate action is HOLD",
        )

    execution_target, no_action_reason = _bounded_execution_target(
        decision, portfolio.current.total
    )
    if execution_target is None:
        return _unchanged(
            decision,
            portfolio,
            integration_status="TARGET SATISFIED / NO DIRECTION INVERSION",
            mapper_status="NOT EXECUTED",
            reason=str(no_action_reason),
        )

    # Candidate REDUCE is the Full Evidence reduction authorization. The connector
    # removes the older duplicated manual full_evidence_authorized input at this
    # integration boundary. Core/Leverage authorities remain separate.
    mapped: MapResult = map_risk_budget(
        portfolio.current,
        portfolio.baseline,
        execution_target,
        full_evidence_authorized=(decision.action_direction == "REDUCE"),
        core_reduction_authorized=portfolio.core_reduction_authorized,
        leverage_restore_authorized=portfolio.leverage_restore_authorized,
        risk_coefficients_complete=portfolio.risk_coefficients_complete,
    )

    # Fail closed if a future mapper change ever reverses Candidate direction.
    if decision.action_direction == "REDUCE" and mapped.after.total > portfolio.current.total + EPS:
        raise AssertionError("REDUCE Candidate decision caused portfolio restoration")
    if decision.action_direction == "RESTORE" and mapped.after.total < portfolio.current.total - EPS:
        raise AssertionError("RESTORE Candidate decision caused portfolio reduction")

    actual_move = abs(mapped.after.total - portfolio.current.total)
    if actual_move > decision.allowed_step_size + 1e-6:
        raise AssertionError("portfolio move exceeds Candidate allowed_step_size")

    unresolved = []
    if execution_target != float(decision.target_risk_budget):
        unresolved.append(
            "Actual portfolio risk lagged Candidate state; execution was capped to current allowed step"
        )
    if mapped.status != "EXECUTABLE":
        unresolved.extend(
            action
            for action in mapped.actions
            if action.startswith("Unfilled")
            or action.startswith("Exact risk-unit")
            or action.startswith("No reduction")
        )

    integration_status = (
        "EXECUTED TO CANDIDATE TARGET"
        if abs(mapped.after.total - float(decision.target_risk_budget)) <= 1e-6
        else "PARTIAL / CANDIDATE TARGET NOT YET REACHED"
    )

    return CandidateExecutionResult(
        decision=decision,
        candidate_target_risk_budget=decision.target_risk_budget,
        execution_target_risk_budget=execution_target,
        before=portfolio.current,
        after=mapped.after,
        integration_status=integration_status,
        mapper_status=mapped.status,
        mapper_actions=tuple(mapped.actions),
        unresolved_constraints=tuple(unresolved),
    )
