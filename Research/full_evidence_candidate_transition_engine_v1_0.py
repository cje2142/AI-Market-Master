"""AI Market Master 3.2 — Full Evidence Candidate Transition Engine v1.0.

Step 3 implementation.

Consumes the frozen Step-2 CandidateInput and Step-1 GateResult, then selects a
Candidate action and normalized target risk budget. It does not map portfolio
sleeves and does not append the Runtime Log; those remain later steps.

Design boundary:
- official C1-C8 / Regime / SAI rules are untouched;
- no raw C1-C8 threshold is invented here;
- only frozen Candidate gates, prior target state, Cost Gate, cooldown and the
  already-frozen discrete transition path are used.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional, Tuple

from full_evidence_candidate_evaluator_v1_0 import GateResult, evaluate_gates, normalize_regime
from full_evidence_candidate_input_contract_v1_0 import CandidateInput


@dataclass(frozen=True)
class TransitionDecision:
    action_direction: str
    previous_target_risk_budget: int
    target_risk_budget: int
    allowed_step_size: int
    evidence_gate_result: str
    gate_reached: str
    cost_gate_status: str
    cooldown_status: str
    fast_recovery: bool
    reason_codes: Tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def _trend(inp: CandidateInput, category: str) -> str:
    return str(inp.categories[category].trend).upper()


def _is_fast_v_rebound(inp: CandidateInput, gates: GateResult) -> bool:
    """Frozen V-rebound priority: R7->R8 plus C1/C2/C3/C5 improvement.

    This is the only Step-3 path that may use the frozen +20pp fast-restoration
    allowance. It is intentionally narrower than a generic positive market state.
    """
    return bool(
        gates.restoration_10
        and inp.flags.r7_to_r8_transition
        and all(_trend(inp, c) == "IMPROVING" for c in ("C1", "C2", "C3", "C5"))
        and inp.flags.c5_structure_recovery
    )


def _reduction_candidate(current: int, gates: GateResult) -> Optional[tuple[int, str]]:
    """Map frozen reduction gates onto the frozen discrete downward path.

    A stronger gate may satisfy a shallower step when the current state cannot take
    the full nominal gate size without violating the allowed-state path. This avoids
    deadlock during abrupt deterioration while never exceeding the frozen per-step
    reduction limit.
    """
    if current == 100:
        if gates.reduction_5 or gates.reduction_additional_5 or gates.reduction_strong_10:
            return 95, "REDUCTION_TO_95"
        return None

    if current == 95:
        if gates.reduction_additional_5 or gates.reduction_strong_10:
            return 90, "REDUCTION_TO_90"
        return None

    if current == 90:
        if gates.reduction_strong_10:
            return 80, "STRONG_REDUCTION_TO_80"
        return None

    if current == 80:
        if gates.reduction_strong_10:
            return 70, "STRONG_REDUCTION_TO_70"
        return None

    if current == 70:
        if gates.reduction_deepest_70_to_60:
            return 60, "DEEPEST_REDUCTION_TO_60"
        return None

    return None


def _restoration_candidate(
    inp: CandidateInput,
    current: int,
    gates: GateResult,
    fast_v_rebound: bool,
) -> Optional[tuple[int, str]]:
    """Map recovery gates onto the frozen upward path.

    The transition table intentionally preserves the older frozen state path:
    - 60 may use the base Recovery Gate; fast V-rebound may restore to 80.
    - 70/80 require the stronger persistence/additional gate for the next normal
      restoration; a fast R7->R8 rebound may take 70 directly to 90.
    - 90 requires the Return-100 gate.
    - 95 may use the standard base Recovery Gate to return to 100.
    """
    if current == 60:
        if fast_v_rebound:
            return 80, "FAST_V_REBOUND_60_TO_80"
        if gates.restoration_10:
            return 70, "RESTORATION_60_TO_70"
        return None

    if current == 70:
        if fast_v_rebound:
            return 90, "FAST_V_REBOUND_70_TO_90"
        if gates.restoration_additional_10:
            return 80, "RESTORATION_70_TO_80"
        return None

    if current == 80:
        if gates.restoration_additional_10:
            return 90, "RESTORATION_80_TO_90"
        return None

    if current == 90:
        if gates.restoration_return_100:
            return 100, "RESTORATION_90_TO_100"
        return None

    if current == 95:
        if gates.restoration_10 or gates.restoration_return_100:
            return 100, "RESTORATION_95_TO_100"
        return None

    return None


def _reduction_cooldown_allows(inp: CandidateInput, gates: GateResult) -> tuple[bool, str]:
    sessions = inp.previous.trading_sessions_since_last_reduction
    if sessions is None or sessions >= 1:
        return True, "COOLDOWN_CLEAR"

    # Frozen exception: materially worsening R5 -> R6 with new independent
    # confirmation. Strong/deepest Full Evidence gates provide that confirmation.
    prev_regime = (
        normalize_regime(inp.previous.previous_validated_regime)
        if inp.previous.previous_validated_regime is not None
        else None
    )
    current_regime = normalize_regime(inp.validated_regime)
    worsening_exception = bool(
        prev_regime == "R5"
        and current_regime == "R6"
        and (gates.reduction_strong_10 or gates.reduction_deepest_70_to_60)
    )
    if worsening_exception:
        return True, "COOLDOWN_BYPASS_R5_TO_R6"
    return False, "COOLDOWN_BLOCKED"


def _cost_gate_allows(inp: CandidateInput, direction: str, gates: GateResult) -> tuple[bool, str]:
    status = str(inp.cost_gate.status).upper()

    if status == "PASS":
        return True, "COST_GATE_PASS"
    if status == "FAIL":
        return False, "COST_GATE_FAIL"
    if status == "UNAVAILABLE":
        # Candidate v1.0 says the 2x rule applies when the Cost Gate can be
        # estimated. Missing cost/edge therefore remains explicit but is not
        # silently converted into FAIL or PASS.
        return True, "COST_GATE_UNAVAILABLE"

    # EMERGENCY_BYPASS was frozen only for confirmed R6 structural-risk control.
    if status == "EMERGENCY_BYPASS":
        valid_bypass = bool(
            direction == "REDUCE"
            and normalize_regime(inp.validated_regime) == "R6"
            and (gates.reduction_strong_10 or gates.reduction_deepest_70_to_60)
        )
        return valid_bypass, (
            "COST_GATE_EMERGENCY_BYPASS" if valid_bypass else "COST_GATE_BYPASS_NOT_APPLICABLE"
        )

    raise ValueError(f"unexpected Cost Gate status: {status}")


def evaluate_transition(inp: CandidateInput) -> TransitionDecision:
    """Return deterministic HOLD/REDUCE/RESTORE/BLOCKED + target risk budget."""
    inp.validate()
    current = inp.previous.current_target_risk_budget
    gates = evaluate_gates(inp.to_candidate_state())

    reasons = list(inp.source_reason_codes)
    reasons.extend(gates.reasons)

    if str(inp.quality).upper() == "BLOCKED":
        reasons.append("INPUT_QUALITY_BLOCKED")
        return TransitionDecision(
            action_direction="BLOCKED",
            previous_target_risk_budget=current,
            target_risk_budget=current,
            allowed_step_size=0,
            evidence_gate_result="BLOCKED",
            gate_reached="NONE",
            cost_gate_status=str(inp.cost_gate.status).upper(),
            cooldown_status="NOT_APPLICABLE",
            fast_recovery=False,
            reason_codes=tuple(dict.fromkeys(reasons)),
        )

    if gates.conflict_hold:
        reasons.append("MATERIAL_CONFLICT_HOLD")
        reasons.extend(inp.candidate_conflict_reasons)
        return TransitionDecision(
            action_direction="HOLD",
            previous_target_risk_budget=current,
            target_risk_budget=current,
            allowed_step_size=0,
            evidence_gate_result="HOLD / CONFLICT",
            gate_reached="CONFLICT",
            cost_gate_status=str(inp.cost_gate.status).upper(),
            cooldown_status="NOT_APPLICABLE",
            fast_recovery=False,
            reason_codes=tuple(dict.fromkeys(reasons)),
        )

    reduction = _reduction_candidate(current, gates)
    fast_v_rebound = _is_fast_v_rebound(inp, gates)
    restoration = _restoration_candidate(inp, current, gates, fast_v_rebound)

    if reduction is not None and restoration is not None:
        reasons.append("OPPOSING_GATE_DIRECTIONS_HOLD")
        return TransitionDecision(
            action_direction="HOLD",
            previous_target_risk_budget=current,
            target_risk_budget=current,
            allowed_step_size=0,
            evidence_gate_result="HOLD / GATE DIRECTION CONFLICT",
            gate_reached="DIRECTION_CONFLICT",
            cost_gate_status=str(inp.cost_gate.status).upper(),
            cooldown_status="NOT_APPLICABLE",
            fast_recovery=fast_v_rebound,
            reason_codes=tuple(dict.fromkeys(reasons)),
        )

    if reduction is not None:
        target, gate_name = reduction
        cooldown_ok, cooldown_status = _reduction_cooldown_allows(inp, gates)
        if not cooldown_ok:
            reasons.append(cooldown_status)
            return TransitionDecision(
                action_direction="HOLD",
                previous_target_risk_budget=current,
                target_risk_budget=current,
                allowed_step_size=0,
                evidence_gate_result="REDUCTION GATE / COOLDOWN BLOCKED",
                gate_reached=gate_name,
                cost_gate_status=str(inp.cost_gate.status).upper(),
                cooldown_status=cooldown_status,
                fast_recovery=False,
                reason_codes=tuple(dict.fromkeys(reasons)),
            )

        cost_ok, cost_status = _cost_gate_allows(inp, "REDUCE", gates)
        if not cost_ok:
            reasons.append(cost_status)
            return TransitionDecision(
                action_direction="HOLD",
                previous_target_risk_budget=current,
                target_risk_budget=current,
                allowed_step_size=0,
                evidence_gate_result="REDUCTION GATE / COST BLOCKED",
                gate_reached=gate_name,
                cost_gate_status=cost_status,
                cooldown_status=cooldown_status,
                fast_recovery=False,
                reason_codes=tuple(dict.fromkeys(reasons)),
            )

        step = current - target
        if step < 5 or step > 10:
            raise AssertionError("reduction step violates frozen 5..10pp boundary")
        reasons.extend([gate_name, cost_status, cooldown_status])
        return TransitionDecision(
            action_direction="REDUCE",
            previous_target_risk_budget=current,
            target_risk_budget=target,
            allowed_step_size=step,
            evidence_gate_result="REDUCTION AUTHORIZED",
            gate_reached=gate_name,
            cost_gate_status=cost_status,
            cooldown_status=cooldown_status,
            fast_recovery=False,
            reason_codes=tuple(dict.fromkeys(reasons)),
        )

    if restoration is not None:
        target, gate_name = restoration
        cost_ok, cost_status = _cost_gate_allows(inp, "RESTORE", gates)
        if not cost_ok:
            reasons.append(cost_status)
            return TransitionDecision(
                action_direction="HOLD",
                previous_target_risk_budget=current,
                target_risk_budget=current,
                allowed_step_size=0,
                evidence_gate_result="RESTORATION GATE / COST BLOCKED",
                gate_reached=gate_name,
                cost_gate_status=cost_status,
                cooldown_status="RECOVERY_GATE_HYSTERESIS",
                fast_recovery=fast_v_rebound,
                reason_codes=tuple(dict.fromkeys(reasons)),
            )

        step = target - current
        if step < 5 or step > 20:
            raise AssertionError("restoration step violates frozen 5..20pp boundary")
        reasons.extend([gate_name, cost_status, "RECOVERY_GATE_HYSTERESIS"])
        return TransitionDecision(
            action_direction="RESTORE",
            previous_target_risk_budget=current,
            target_risk_budget=target,
            allowed_step_size=step,
            evidence_gate_result="RESTORATION AUTHORIZED",
            gate_reached=gate_name,
            cost_gate_status=cost_status,
            cooldown_status="FAST_RECOVERY_OVERRIDE" if fast_v_rebound else "RECOVERY_GATE_HYSTERESIS",
            fast_recovery=fast_v_rebound,
            reason_codes=tuple(dict.fromkeys(reasons)),
        )

    reasons.append("NO_STATE_ELIGIBLE_TRANSITION")
    return TransitionDecision(
        action_direction="HOLD",
        previous_target_risk_budget=current,
        target_risk_budget=current,
        allowed_step_size=0,
        evidence_gate_result="HOLD",
        gate_reached="NONE",
        cost_gate_status=str(inp.cost_gate.status).upper(),
        cooldown_status="NOT_APPLICABLE",
        fast_recovery=fast_v_rebound,
        reason_codes=tuple(dict.fromkeys(reasons)),
    )
