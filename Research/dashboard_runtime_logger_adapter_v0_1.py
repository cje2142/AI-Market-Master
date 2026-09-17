import argparse
import hashlib
import json
import re
from pathlib import Path

import full_evidence_runtime_log_v0_1 as runtime
from risk_budget_execution_v0_1 import Sleeves, map_risk_budget

CATEGORIES = [f"C{i}" for i in range(1, 9)]
QUALITY = {"FULL", "PARTIAL", "BLOCKED"}
ACTIONS = {"HOLD", "REDUCE", "RESTORE", "BLOCKED"}

SNAPSHOT_REQUIRED = [
    "market_date", "timestamp", "session_checkpoint", "data_mode",
    "validation_status", "quality", *CATEGORIES,
    "preliminary_regime", "validated_regime", "transition_state",
    "material_conflicts", "evidence_gate_result", "gate_reached",
    "target_risk_budget", "action_direction", "allowed_step_size",
    "reason_codes",
]


def _bool(v, name):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        x = v.strip().upper()
        if x in {"YES", "Y", "TRUE", "1"}:
            return True
        if x in {"NO", "N", "FALSE", "0"}:
            return False
    raise ValueError(f"{name} must be boolean or YES/NO")


def _canonical(obj):
    if isinstance(obj, dict):
        return {k: _canonical(obj[k]) for k in sorted(obj)}
    if isinstance(obj, list):
        normalized = [_canonical(x) for x in obj]
        return sorted(normalized, key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True))
    return obj


def validate_snapshot(snapshot):
    missing = [k for k in SNAPSHOT_REQUIRED if k not in snapshot]
    if missing:
        raise ValueError(f"missing dashboard snapshot fields: {missing}")

    if snapshot["quality"] not in QUALITY:
        raise ValueError("quality must be FULL/PARTIAL/BLOCKED")
    if snapshot["action_direction"] not in ACTIONS:
        raise ValueError("action_direction must be HOLD/REDUCE/RESTORE/BLOCKED")

    any_missing = False
    for c in CATEGORIES:
        obj = snapshot[c]
        runtime._validate_category(c, obj)
        if obj.get("value") is None:
            any_missing = True

    if snapshot["quality"] == "FULL" and any_missing:
        raise ValueError("FULL snapshot cannot contain missing C1-C8 values")
    if snapshot["action_direction"] == "BLOCKED" and snapshot["quality"] != "BLOCKED":
        raise ValueError("BLOCKED action requires quality=BLOCKED")

    target = snapshot["target_risk_budget"]
    if target is not None and not isinstance(target, (int, float)):
        raise ValueError("target_risk_budget must be numeric or null")
    if target is not None and not (0 <= float(target) <= 100):
        raise ValueError("target_risk_budget must be within 0..100")
    return True


def signal_fingerprint(snapshot):
    validate_snapshot(snapshot)
    payload = {k: snapshot[k] for k in SNAPSHOT_REQUIRED}
    canonical = json.dumps(_canonical(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def sample_id_for(snapshot):
    digest = signal_fingerprint(snapshot)[:12]
    checkpoint = re.sub(r"[^A-Za-z0-9_-]+", "-", str(snapshot["session_checkpoint"])).strip("-") or "session"
    date = re.sub(r"[^0-9]", "", str(snapshot["market_date"]))
    return f"AMM32-{date}-{checkpoint}-{digest}"


def _sleeves(obj, name):
    if not isinstance(obj, dict):
        raise ValueError(f"{name} must be object")
    missing = [k for k in ("core", "tactical", "leverage") if k not in obj]
    if missing:
        raise ValueError(f"{name} missing {missing}")
    vals = [float(obj[k]) for k in ("core", "tactical", "leverage")]
    if any(v < 0 for v in vals):
        raise ValueError(f"{name} sleeve values must be >=0")
    return Sleeves(*vals)


def _map_portfolio(snapshot):
    portfolio = snapshot.get("portfolio")
    target = snapshot.get("target_risk_budget")
    base_unresolved = list(snapshot.get("unresolved_constraints", []))

    if portfolio is None or target is None:
        reason = "portfolio input unavailable" if portfolio is None else "target risk budget unavailable"
        return {
            "core_before": None, "tactical_before": None, "leverage_before": None,
            "exact_risk_multipliers": False if portfolio is None else portfolio.get("exact_risk_multipliers"),
            "leverage_restore_authority": False if portfolio is None else portfolio.get("leverage_restore_authority"),
            "core_reduction_authority": False if portfolio is None else portfolio.get("core_reduction_authority"),
            "core_after": None, "tactical_after": None, "leverage_after": None,
            "mapper_status": "NOT MAPPED",
            "action_hierarchy": [],
            "unresolved_constraints": base_unresolved + [reason],
        }

    for k in (
        "baseline", "current", "exact_risk_multipliers",
        "leverage_restore_authority", "core_reduction_authority",
        "full_evidence_authorized",
    ):
        if k not in portfolio:
            raise ValueError(f"portfolio missing {k}")

    baseline = _sleeves(portfolio["baseline"], "portfolio.baseline")
    current = _sleeves(portfolio["current"], "portfolio.current")
    if abs(baseline.total - 100.0) > 1e-6:
        raise ValueError("portfolio.baseline normalized risk units must total 100")

    exact = _bool(portfolio["exact_risk_multipliers"], "exact_risk_multipliers")
    leverage_auth = _bool(portfolio["leverage_restore_authority"], "leverage_restore_authority")
    core_auth = _bool(portfolio["core_reduction_authority"], "core_reduction_authority")
    full_auth = _bool(portfolio["full_evidence_authorized"], "full_evidence_authorized")

    mapped = map_risk_budget(
        current,
        baseline,
        float(target),
        full_evidence_authorized=full_auth,
        core_reduction_authorized=core_auth,
        leverage_restore_authorized=leverage_auth,
        risk_coefficients_complete=exact,
    )

    blockers = base_unresolved[:]
    if mapped.status != "EXECUTABLE":
        blockers.extend([
            a for a in mapped.actions
            if a.startswith("Unfilled") or a.startswith("No reduction") or a.startswith("Exact risk-unit")
        ])

    return {
        "core_before": current.core,
        "tactical_before": current.tactical,
        "leverage_before": current.leverage,
        "exact_risk_multipliers": exact,
        "leverage_restore_authority": leverage_auth,
        "core_reduction_authority": core_auth,
        "core_after": mapped.after.core,
        "tactical_after": mapped.after.tactical,
        "leverage_after": mapped.after.leverage,
        "mapper_status": mapped.status,
        "action_hierarchy": mapped.actions,
        "unresolved_constraints": blockers,
    }


def build_runtime_sample(snapshot):
    validate_snapshot(snapshot)
    sid = sample_id_for(snapshot)
    mapped = _map_portfolio(snapshot)

    sample = {
        "sample_id": sid,
        "market_date": snapshot["market_date"],
        "timestamp": snapshot["timestamp"],
        "session_checkpoint": snapshot["session_checkpoint"],
        "data_mode": snapshot["data_mode"],
        "validation_status": snapshot["validation_status"],
        "quality": snapshot["quality"],
        **{c: snapshot[c] for c in CATEGORIES},
        "preliminary_regime": snapshot["preliminary_regime"],
        "validated_regime": snapshot["validated_regime"],
        "transition_state": snapshot["transition_state"],
        "material_conflicts": snapshot["material_conflicts"],
        "evidence_gate_result": snapshot["evidence_gate_result"],
        "gate_reached": snapshot["gate_reached"],
        "target_risk_budget": snapshot["target_risk_budget"],
        "action_direction": snapshot["action_direction"],
        "allowed_step_size": snapshot["allowed_step_size"],
        "reason_codes": snapshot["reason_codes"],
        **mapped,
    }
    runtime.validate_signal(sample)
    return sample


def append_dashboard_snapshot(snapshot, log_path, csv_path):
    sample = build_runtime_sample(snapshot)
    event = runtime.append_signal(log_path, sample)
    runtime.write_projection_csv(log_path, csv_path)
    return event, sample


def main():
    parser = argparse.ArgumentParser(description="Append normalized Dashboard snapshot to Full Evidence Runtime Log v0.1")
    parser.add_argument("snapshot_json")
    parser.add_argument("--log", default="Research/runtime/full_evidence_runtime_log_v0_1.jsonl")
    parser.add_argument("--csv", default="Research/runtime/full_evidence_runtime_log_v0_1.csv")
    args = parser.parse_args()

    with open(args.snapshot_json, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    event, sample = append_dashboard_snapshot(snapshot, args.log, args.csv)
    print(json.dumps({"sample_id": sample["sample_id"], "record_type": event["record_type"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
