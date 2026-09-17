import csv
import json
import tempfile
from copy import deepcopy
from pathlib import Path

import dashboard_runtime_logger_adapter_v0_1 as adapter


def cat(value=0.1, status="VERIFIED"):
    return {"status": status, "value": value}


def base_snapshot():
    s = {
        "market_date": "2026-09-17",
        "timestamp": "2026-09-17T15:30:00+09:00",
        "session_checkpoint": "CLOSE",
        "data_mode": "LIVE",
        "validation_status": "VERIFIED",
        "quality": "FULL",
        "C1": cat(-0.4), "C2": cat(-0.3), "C3": cat(-0.2), "C4": cat(0.1),
        "C5": cat(-0.2), "C6": cat(0.1), "C7": cat(-0.1), "C8": cat(-0.2),
        "preliminary_regime": "R4",
        "validated_regime": "R4",
        "transition_state": "R4 WATCH",
        "material_conflicts": [],
        "evidence_gate_result": "REDUCTION AUTHORIZED",
        "gate_reached": "FIRST -5%p",
        "target_risk_budget": 95,
        "action_direction": "REDUCE",
        "allowed_step_size": -5,
        "reason_codes": ["R4", "A_CLASS_DETERIORATION", "3_GROUP_CONFIRM"],
        "portfolio": {
            "baseline": {"core": 80, "tactical": 10, "leverage": 10},
            "current": {"core": 80, "tactical": 10, "leverage": 10},
            "exact_risk_multipliers": True,
            "leverage_restore_authority": False,
            "core_reduction_authority": False,
            "full_evidence_authorized": True,
        },
    }
    return s


def run_tests():
    results = []

    # T1 FULL Dashboard snapshot -> valid Runtime sample.
    s = base_snapshot()
    sample = adapter.build_runtime_sample(s)
    assert sample["quality"] == "FULL"
    assert sample["mapper_status"] == "EXECUTABLE"
    results.append(("T1 FULL snapshot builds valid Runtime sample", "PASS"))

    # T2 same snapshot rerun -> same sample_id / duplicate rejected.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "log.jsonl"
        csvp = Path(td) / "log.csv"
        _, first = adapter.append_dashboard_snapshot(s, log, csvp)
        second_id = adapter.sample_id_for(deepcopy(s))
        assert first["sample_id"] == second_id
        duplicate_rejected = False
        try:
            adapter.append_dashboard_snapshot(deepcopy(s), log, csvp)
        except ValueError as e:
            duplicate_rejected = "duplicate sample_id" in str(e)
        assert duplicate_rejected
    results.append(("T2 duplicate snapshot stable-id rejection", "PASS"))

    # T3 new signal timestamp -> new sample_id.
    s2 = deepcopy(s)
    s2["timestamp"] = "2026-09-17T15:35:00+09:00"
    assert adapter.sample_id_for(s) != adapter.sample_id_for(s2)
    results.append(("T3 new signal timestamp creates new sample_id", "PASS"))

    # T4 PARTIAL with explicit missing category accepted and preserved.
    p = deepcopy(s)
    p["quality"] = "PARTIAL"
    p["validation_status"] = "PARTIAL DATA"
    p["C6"] = {"status": "DATA UNAVAILABLE", "value": None}
    ps = adapter.build_runtime_sample(p)
    assert ps["C6"]["value"] is None and ps["quality"] == "PARTIAL"
    results.append(("T4 PARTIAL explicit missing preserved", "PASS"))

    # T5 FULL with missing category rejected.
    bad = deepcopy(s)
    bad["C6"] = {"status": "DATA UNAVAILABLE", "value": None}
    rejected = False
    try:
        adapter.build_runtime_sample(bad)
    except ValueError as e:
        rejected = "FULL snapshot" in str(e)
    assert rejected
    results.append(("T5 FULL snapshot cannot hide missing category", "PASS"))

    # T6 REDUCE + portfolio -> Leverage first.
    rs = adapter.build_runtime_sample(s)
    assert (rs["core_after"], rs["tactical_after"], rs["leverage_after"]) == (80.0, 10.0, 5.0)
    assert rs["action_hierarchy"][0] == "Reduce Leverage 5.00"
    results.append(("T6 reduction maps Leverage first", "PASS"))

    # T7 R6 REDUCE without Full Evidence authority -> no automatic sale.
    panic = deepcopy(s)
    panic["preliminary_regime"] = "R6"
    panic["validated_regime"] = "R6"
    panic["transition_state"] = "PANIC"
    panic["target_risk_budget"] = 80
    panic["gate_reached"] = "BLOCKED BY EVIDENCE GATE"
    panic["evidence_gate_result"] = "NOT AUTHORIZED"
    panic["portfolio"]["full_evidence_authorized"] = False
    pr = adapter.build_runtime_sample(panic)
    assert (pr["core_after"], pr["tactical_after"], pr["leverage_after"]) == (80.0, 10.0, 10.0)
    assert pr["mapper_status"] == "HOLD / CONFLICT"
    results.append(("T7 Panic without Full Evidence authority cannot sell", "PASS"))

    # T8 HOLD without portfolio -> market observation still loggable as NOT MAPPED.
    hold = deepcopy(s)
    hold.pop("portfolio")
    hold["target_risk_budget"] = 100
    hold["action_direction"] = "HOLD"
    hold["allowed_step_size"] = 0
    hold["evidence_gate_result"] = "HOLD"
    hold["gate_reached"] = "NONE"
    hs = adapter.build_runtime_sample(hold)
    assert hs["mapper_status"] == "NOT MAPPED"
    assert hs["core_before"] is None and hs["core_after"] is None
    results.append(("T8 HOLD without portfolio remains loggable", "PASS"))

    # T9 portfolio composition is excluded from market sample identity.
    alt = deepcopy(s)
    alt["portfolio"]["baseline"] = {"core": 70, "tactical": 30, "leverage": 0}
    alt["portfolio"]["current"] = {"core": 70, "tactical": 30, "leverage": 0}
    a = adapter.build_runtime_sample(s)
    b = adapter.build_runtime_sample(alt)
    assert a["sample_id"] == b["sample_id"]
    assert (a["core_after"], a["tactical_after"], a["leverage_after"]) != (b["core_after"], b["tactical_after"], b["leverage_after"])
    results.append(("T9 portfolio changes mapping but not market sample_id", "PASS"))

    # T10 CSV projection matches appended canonical JSONL sample.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "log.jsonl"
        csvp = Path(td) / "log.csv"
        _, appended = adapter.append_dashboard_snapshot(s, log, csvp)
        with csvp.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        assert rows[0]["sample_id"] == appended["sample_id"]
        assert rows[0]["mapper_status"] == appended["mapper_status"]
        assert rows[0]["outcome_status_1d"] == "PENDING"
    results.append(("T10 CSV projection matches canonical append", "PASS"))

    return results


def main():
    results = run_tests()
    outdir = Path(__file__).parent / "results"
    outdir.mkdir(exist_ok=True)
    payload = {
        "version": "Dashboard Runtime Logger Adapter v0.1",
        "status": "DETERMINISTIC TEST",
        "official_3_2_authority": False,
        "tests_passed": sum(1 for _, status in results if status == "PASS"),
        "tests_total": len(results),
        "results": [{"name": name, "result": status} for name, status in results],
        "production_runtime_sample_created": False,
    }
    (outdir / "dashboard_runtime_logger_adapter_v0_1_test_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Dashboard Runtime Logger Adapter v0.1 — Deterministic Test",
        "",
        "Status: EXPERIMENTAL ADAPTER VALIDATION / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{payload['tests_passed']}/{payload['tests_total']} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    lines += [f"| {name} | {status} |" for name, status in results]
    lines += [
        "",
        "Production Runtime Log was NOT used by these tests; no prospective market sample was created.",
        "Passing this test validates transfer/logging semantics only, not market timing or official 3.2 integration.",
    ]
    (outdir / "dashboard_runtime_logger_adapter_v0_1_test_results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
