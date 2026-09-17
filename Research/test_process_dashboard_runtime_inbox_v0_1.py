import json
import tempfile
from copy import deepcopy
from pathlib import Path

import process_dashboard_runtime_inbox_v0_1 as processor


def cat(value=0.1, status="VERIFIED"):
    return {"status": status, "value": value}


def snapshot(ts="2026-09-17T15:30:00+09:00"):
    return {
        "market_date": "2026-09-17",
        "timestamp": ts,
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


def run_tests():
    results = []

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        inbox = root / "inbox"
        inbox.mkdir()
        log = root / "runtime.jsonl"
        csvp = root / "runtime.csv"

        # T1 valid inbox snapshot is appended.
        (inbox / "a.json").write_text(json.dumps(snapshot(), ensure_ascii=False), encoding="utf-8")
        r1 = processor.process_inbox(inbox, log, csvp)
        assert len(r1) == 1 and r1[0]["status"] == "APPENDED"
        assert len([x for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]) == 1
        results.append(("T1 valid inbox snapshot appended", "PASS"))

        # T2 rerun scans retained inbox but skips duplicate rather than duplicating journal.
        r2 = processor.process_inbox(inbox, log, csvp)
        assert len(r2) == 1 and r2[0]["status"] == "SKIP DUPLICATE"
        assert len([x for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]) == 1
        results.append(("T2 retained inbox duplicate safely skipped", "PASS"))

        # T3 materially new signal timestamp creates a second sample.
        (inbox / "b.json").write_text(json.dumps(snapshot("2026-09-17T15:35:00+09:00"), ensure_ascii=False), encoding="utf-8")
        r3 = processor.process_inbox(inbox, log, csvp)
        assert any(x["file"].endswith("b.json") and x["status"] == "APPENDED" for x in r3)
        assert len([x for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]) == 2
        results.append(("T3 new signal timestamp appended as new sample", "PASS"))

    # T4 invalid snapshot fails instead of being silently repaired.
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        inbox = root / "inbox"
        inbox.mkdir()
        log = root / "runtime.jsonl"
        csvp = root / "runtime.csv"
        bad = snapshot()
        bad["C6"] = {"status": "DATA UNAVAILABLE", "value": None}
        # quality intentionally left FULL -> invalid
        (inbox / "bad.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        failed = False
        try:
            processor.process_inbox(inbox, log, csvp)
        except ValueError as e:
            failed = "FULL snapshot" in str(e)
        assert failed
        results.append(("T4 invalid snapshot fails closed", "PASS"))

    return results


def main():
    results = run_tests()
    outdir = Path(__file__).parent / "results"
    outdir.mkdir(exist_ok=True)
    payload = {
        "version": "Dashboard Runtime Ingestion v0.1",
        "tests_passed": sum(1 for _, s in results if s == "PASS"),
        "tests_total": len(results),
        "production_runtime_sample_created": False,
        "results": [{"name": n, "result": s} for n, s in results],
    }
    (outdir / "dashboard_runtime_ingestion_v0_1_test_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Dashboard Runtime Ingestion v0.1 — Deterministic Test",
        "",
        f"Result: **{payload['tests_passed']}/{payload['tests_total']} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
        *[f"| {n} | {s} |" for n, s in results],
        "",
        "All tests use temporary stores. No production prospective sample is created.",
    ]
    (outdir / "dashboard_runtime_ingestion_v0_1_test_results.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
