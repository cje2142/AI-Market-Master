"""AI Market Master 3.2 — Dashboard -> Candidate -> Runtime adapter v1.0.

Step 6 integration layer.

Pipeline:
Dashboard snapshot -> Candidate Input Contract v1.0 -> Transition Engine v1.0
-> optional Risk Budget Connector v1.0 -> Full Evidence Runtime Log v0.1.

Safety boundaries:
- no C1-C8 trend/polarity/strength is inferred from numeric values;
- all Candidate structural flags are explicit in the Dashboard snapshot;
- prior Overlay state remains explicit, per the frozen Step-2 contract;
- portfolio context is optional and cannot alter the Candidate market decision;
- HOLD/BLOCKED never becomes a portfolio trade;
- Runtime Log schema/append-only semantics are unchanged.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

import full_evidence_runtime_log_v0_1 as runtime
from full_evidence_candidate_evaluator_v1_0 import CATEGORIES, CandidateFlags
from full_evidence_candidate_input_contract_v1_0 import candidate_input_from_dict
from full_evidence_candidate_risk_budget_connector_v1_0 import (
    PortfolioExecutionContext,
    connect_candidate_to_risk_budget,
)
from full_evidence_candidate_transition_engine_v1_0 import evaluate_transition
from risk_budget_execution_v0_1 import Sleeves

QUALITY = {"FULL", "PARTIAL", "BLOCKED"}

DASHBOARD_REQUIRED = [
    "market_date", "timestamp", "session_checkpoint", "data_mode",
    "validation_status", "quality", *CATEGORIES,
    "preliminary_regime", "validated_regime", "transition_state",
    "material_conflicts", "reason_codes", "candidate",
]

EVIDENCE_LABEL_FIELDS = ("trend", "polarity", "strength")
PORTFOLIO_BOOL_FIELDS = (
    "core_reduction_authorized",
    "leverage_restore_authorized",
    "risk_coefficients_complete",
)


def _strict_bool(value: Any, name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        token = value.strip().upper()
        if token in {"TRUE", "YES", "Y", "1"}:
            return True
        if token in {"FALSE", "NO", "N", "0"}:
            return False
    raise ValueError(f"{name} must be boolean or explicit YES/NO")


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be an object")
    return value


def _sleeves(value: Any, name: str) -> Sleeves:
    obj = _mapping(value, name)
    missing = [k for k in ("core", "tactical", "leverage") if k not in obj]
    if missing:
        raise ValueError(f"{name} missing {missing}")
    vals = []
    for k in ("core", "tactical", "leverage"):
        v = obj[k]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"{name}.{k} must be numeric")
        if float(v) < 0:
            raise ValueError(f"{name}.{k} must be >= 0")
        vals.append(float(v))
    return Sleeves(*vals)


def validate_dashboard_candidate_snapshot(snapshot: Mapping[str, Any]) -> None:
    snapshot = _mapping(snapshot, "snapshot")
    missing = [k for k in DASHBOARD_REQUIRED if k not in snapshot]
    if missing:
        raise ValueError(f"missing Dashboard Candidate fields: {missing}")

    quality = str(snapshot["quality"]).upper()
    if quality not in QUALITY:
        raise ValueError("quality must be FULL/PARTIAL/BLOCKED")

    for c in CATEGORIES:
        runtime._validate_category(c, snapshot[c])

    if quality == "FULL" and any(snapshot[c].get("value") is None for c in CATEGORIES):
        raise ValueError("FULL Dashboard Candidate snapshot cannot contain missing C1-C8 values")

    if not isinstance(snapshot["material_conflicts"], list):
        raise ValueError("material_conflicts must be a list")
    if not isinstance(snapshot["reason_codes"], list):
        raise ValueError("reason_codes must be a list")

    candidate = _mapping(snapshot["candidate"], "candidate")
    required_candidate = {
        "evidence", "flags", "previous", "cost_gate", "candidate_conflict_reasons"
    }
    missing_candidate = sorted(required_candidate - set(candidate))
    if missing_candidate:
        raise ValueError(f"candidate missing fields: {missing_candidate}")

    evidence = _mapping(candidate["evidence"], "candidate.evidence")
    if set(evidence) != set(CATEGORIES):
        missing_c = sorted(set(CATEGORIES) - set(evidence))
        extra_c = sorted(set(evidence) - set(CATEGORIES))
        raise ValueError(
            f"candidate.evidence must be exactly C1-C8; missing={missing_c}, extra={extra_c}"
        )
    for c in CATEGORIES:
        obj = _mapping(evidence[c], f"candidate.evidence.{c}")
        missing_labels = [k for k in EVIDENCE_LABEL_FIELDS if k not in obj]
        if missing_labels:
            raise ValueError(f"candidate.evidence.{c} missing {missing_labels}")

    flags = _mapping(candidate["flags"], "candidate.flags")
    expected_flags = set(CandidateFlags.__dataclass_fields__)
    if set(flags) != expected_flags:
        missing_flags = sorted(expected_flags - set(flags))
        extra_flags = sorted(set(flags) - expected_flags)
        raise ValueError(
            f"candidate.flags must be explicit and complete; missing={missing_flags}, extra={extra_flags}"
        )
    for name in expected_flags:
        _strict_bool(flags[name], f"candidate.flags.{name}")

    _mapping(candidate["previous"], "candidate.previous")
    cost = _mapping(candidate["cost_gate"], "candidate.cost_gate")
    if "status" not in cost:
        raise ValueError("candidate.cost_gate.status is required")
    if not isinstance(candidate["candidate_conflict_reasons"], list):
        raise ValueError("candidate.candidate_conflict_reasons must be a list")

    portfolio = snapshot.get("portfolio")
    if portfolio is not None:
        portfolio = _mapping(portfolio, "portfolio")
        required_portfolio = {
            "baseline", "current", *PORTFOLIO_BOOL_FIELDS,
        }
        missing_p = sorted(required_portfolio - set(portfolio))
        if missing_p:
            raise ValueError(f"portfolio missing fields: {missing_p}")
        _sleeves(portfolio["baseline"], "portfolio.baseline")
        _sleeves(portfolio["current"], "portfolio.current")
        for name in PORTFOLIO_BOOL_FIELDS:
            _strict_bool(portfolio[name], f"portfolio.{name}")


def build_candidate_input(snapshot: Mapping[str, Any]):
    """Merge official Dashboard C1-C8 values with explicit Candidate labels.

    Numeric status/value comes only from top-level Dashboard output. Candidate evidence
    supplies labels only; duplicate numeric values are not accepted or reconciled.
    """
    validate_dashboard_candidate_snapshot(snapshot)
    candidate = snapshot["candidate"]

    categories = {}
    for c in CATEGORIES:
        labels = candidate["evidence"][c]
        categories[c] = {
            "status": snapshot[c]["status"],
            "value": snapshot[c]["value"],
            "trend": labels["trend"],
            "polarity": labels["polarity"],
            "strength": labels["strength"],
        }

    payload = {
        "market_date": snapshot["market_date"],
        "timestamp": snapshot["timestamp"],
        "session_checkpoint": snapshot["session_checkpoint"],
        "data_mode": snapshot["data_mode"],
        "validation_status": snapshot["validation_status"],
        "quality": snapshot["quality"],
        "preliminary_regime": snapshot["preliminary_regime"],
        "validated_regime": snapshot["validated_regime"],
        "transition_state": snapshot["transition_state"],
        "categories": categories,
        "flags": candidate["flags"],
        "previous": candidate["previous"],
        "cost_gate": candidate["cost_gate"],
        "candidate_conflict_reasons": candidate["candidate_conflict_reasons"],
        "source_reason_codes": snapshot["reason_codes"],
    }
    return candidate_input_from_dict(payload)


def _portfolio_context(snapshot: Mapping[str, Any]):
    raw = snapshot.get("portfolio")
    if raw is None:
        return None
    return PortfolioExecutionContext(
        baseline=_sleeves(raw["baseline"], "portfolio.baseline"),
        current=_sleeves(raw["current"], "portfolio.current"),
        core_reduction_authorized=_strict_bool(
            raw["core_reduction_authorized"], "portfolio.core_reduction_authorized"
        ),
        leverage_restore_authorized=_strict_bool(
            raw["leverage_restore_authorized"], "portfolio.leverage_restore_authorized"
        ),
        risk_coefficients_complete=_strict_bool(
            raw["risk_coefficients_complete"], "portfolio.risk_coefficients_complete"
        ),
    )


def _identity_fingerprint(snapshot: Mapping[str, Any]) -> str:
    """Stable signal identity; excludes portfolio and derived Candidate decision.

    Reprocessing the same Dashboard checkpoint after a Candidate/portfolio correction
    keeps the same sample id so the append-only Runtime Log rejects silent rewrite.
    """
    payload = {
        "market_date": snapshot["market_date"],
        "timestamp": snapshot["timestamp"],
        "session_checkpoint": snapshot["session_checkpoint"],
        "data_mode": snapshot["data_mode"],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def sample_id_for(snapshot: Mapping[str, Any]) -> str:
    validate_dashboard_candidate_snapshot(snapshot)
    digest = _identity_fingerprint(snapshot)[:12]
    checkpoint = re.sub(
        r"[^A-Za-z0-9_-]+", "-", str(snapshot["session_checkpoint"])
    ).strip("-") or "session"
    day = re.sub(r"[^0-9]", "", str(snapshot["market_date"]))
    return f"AMM32C-{day}-{checkpoint}-{digest}"


def build_runtime_sample(snapshot: Mapping[str, Any]) -> dict:
    validate_dashboard_candidate_snapshot(snapshot)
    candidate_input = build_candidate_input(snapshot)
    decision = evaluate_transition(candidate_input)
    portfolio = _portfolio_context(snapshot)
    unresolved = list(snapshot.get("unresolved_constraints", []))

    if portfolio is None:
        core_before = tactical_before = leverage_before = None
        core_after = tactical_after = leverage_after = None
        exact = False
        leverage_auth = False
        core_auth = False
        mapper_status = "NOT MAPPED"
        action_hierarchy = []
        unresolved.append("portfolio input unavailable; Candidate market decision logged without sleeve mapping")
    else:
        result = connect_candidate_to_risk_budget(candidate_input, portfolio)
        core_before = result.before.core
        tactical_before = result.before.tactical
        leverage_before = result.before.leverage
        core_after = result.after.core
        tactical_after = result.after.tactical
        leverage_after = result.after.leverage
        exact = portfolio.risk_coefficients_complete
        leverage_auth = portfolio.leverage_restore_authorized
        core_auth = portfolio.core_reduction_authorized
        action_hierarchy = list(result.mapper_actions)
        unresolved.extend(result.unresolved_constraints)

        if decision.action_direction in {"HOLD", "BLOCKED"}:
            # Runtime v0.1 has no NOT EXECUTED enum. Preserve no-execution explicitly
            # as NOT MAPPED rather than pretending EXECUTABLE.
            mapper_status = "NOT MAPPED"
        else:
            mapper_status = result.mapper_status

    reasons = list(decision.reason_codes)
    if "CANDIDATE_V1_0" not in reasons:
        reasons.append("CANDIDATE_V1_0")

    sample = {
        "sample_id": sample_id_for(snapshot),
        "market_date": snapshot["market_date"],
        "timestamp": snapshot["timestamp"],
        "session_checkpoint": snapshot["session_checkpoint"],
        "data_mode": snapshot["data_mode"],
        "validation_status": snapshot["validation_status"],
        "quality": snapshot["quality"],
        **{c: {"status": snapshot[c]["status"], "value": snapshot[c]["value"]} for c in CATEGORIES},
        "preliminary_regime": snapshot["preliminary_regime"],
        "validated_regime": snapshot["validated_regime"],
        "transition_state": snapshot["transition_state"],
        "material_conflicts": list(snapshot["material_conflicts"]),
        "evidence_gate_result": decision.evidence_gate_result,
        "gate_reached": decision.gate_reached,
        "target_risk_budget": decision.target_risk_budget,
        "action_direction": decision.action_direction,
        "allowed_step_size": decision.allowed_step_size,
        "reason_codes": reasons,
        "core_before": core_before,
        "tactical_before": tactical_before,
        "leverage_before": leverage_before,
        "exact_risk_multipliers": exact,
        "leverage_restore_authority": leverage_auth,
        "core_reduction_authority": core_auth,
        "core_after": core_after,
        "tactical_after": tactical_after,
        "leverage_after": leverage_after,
        "mapper_status": mapper_status,
        "action_hierarchy": action_hierarchy,
        "unresolved_constraints": unresolved,
    }
    runtime.validate_signal(sample)
    return sample


def append_dashboard_candidate_snapshot(snapshot, log_path, csv_path):
    sample = build_runtime_sample(snapshot)
    event = runtime.append_signal(log_path, sample)
    runtime.write_projection_csv(log_path, csv_path)
    return event, sample


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate Dashboard Candidate v1.0 snapshot and append Runtime Log v0.1"
    )
    parser.add_argument("snapshot_json")
    parser.add_argument("--log", default="Research/runtime/full_evidence_runtime_log_v0_1.jsonl")
    parser.add_argument("--csv", default="Research/runtime/full_evidence_runtime_log_v0_1.csv")
    args = parser.parse_args()

    with Path(args.snapshot_json).open("r", encoding="utf-8") as f:
        snapshot = json.load(f)
    event, sample = append_dashboard_candidate_snapshot(snapshot, args.log, args.csv)
    print(json.dumps({
        "sample_id": sample["sample_id"],
        "record_type": event["record_type"],
        "action_direction": sample["action_direction"],
        "target_risk_budget": sample["target_risk_budget"],
        "mapper_status": sample["mapper_status"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
