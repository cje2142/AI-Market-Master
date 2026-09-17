import json
import tempfile
from pathlib import Path

from full_evidence_runtime_log_v0_1 import (
    append_correction,
    append_outcome,
    append_signal,
    build_projection,
    initialize_store,
    write_projection_csv,
)


def base_signal(sample_id="S1", quality="FULL"):
    cats = {f"C{i}": {"status": "VERIFIED", "value": 0.1 * i} for i in range(1, 9)}
    return {
        "sample_id": sample_id,
        "market_date": "2026-09-17",
        "timestamp": "2026-09-17T15:30:00+09:00",
        "session_checkpoint": "CLOSE",
        "data_mode": "LIVE",
        "validation_status": "VERIFIED",
        "quality": quality,
        **cats,
        "preliminary_regime": "R4",
        "validated_regime": "R4",
        "transition_state": "R4->R5 WATCH",
        "material_conflicts": [],
        "evidence_gate_result": "HOLD / WATCH",
        "gate_reached": "NONE",
        "target_risk_budget": 100,
        "action_direction": "HOLD",
        "allowed_step_size": 0,
        "reason_codes": ["TECHNICAL_CONFLICT"],
        "core_before": 80,
        "tactical_before": 10,
        "leverage_before": 10,
        "exact_risk_multipliers": False,
        "leverage_restore_authority": False,
        "core_reduction_authority": False,
        "core_after": 80,
        "tactical_after": 10,
        "leverage_after": 10,
        "mapper_status": "DATA PARTIAL",
        "action_hierarchy": [],
        "unresolved_constraints": ["RISK_MULTIPLIERS_MISSING"],
    }


def expect_error(fn):
    try:
        fn()
    except ValueError:
        return True
    raise AssertionError("expected ValueError")


def run_tests():
    results = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        log = td / "runtime.jsonl"
        csvp = td / "runtime.csv"
        initialize_store(log, csvp)

        # T1 valid signal append
        append_signal(log, base_signal("S1"))
        assert len(build_projection(log)) == 1
        results.append(("T1 valid signal append", "PASS"))

        # T2 duplicate rejection
        expect_error(lambda: append_signal(log, base_signal("S1")))
        results.append(("T2 duplicate sample rejection", "PASS"))

        # T3 missing != neutral and PARTIAL explicit missing accepted
        s2 = base_signal("S2", "PARTIAL")
        s2["C6"] = {"status": "DATA UNAVAILABLE", "value": None}
        append_signal(log, s2)
        bad = base_signal("S3", "PARTIAL")
        bad["C6"] = {"status": "NEUTRAL", "value": None}
        expect_error(lambda: append_signal(log, bad))
        results.append(("T3 missing-state handling", "PASS"))

        # T4 outcome starts PENDING
        p = {r["sample_id"]: r for r in build_projection(log)}
        assert p["S1"]["outcome_status_1d"] == "PENDING"
        assert p["S1"]["outcome_status_20d"] == "PENDING"
        results.append(("T4 future outcomes remain PENDING", "PASS"))

        # T5 mature only authorized horizon fields
        append_outcome(log, "S1", "1d", {"ret_1d": -0.01})
        p = {r["sample_id"]: r for r in build_projection(log)}
        assert p["S1"]["ret_1d"] == -0.01 and p["S1"]["ret_5d"] is None
        assert p["S1"]["outcome_status_1d"] == "MATURE" and p["S1"]["outcome_status_5d"] == "PENDING"
        results.append(("T5 horizon maturation isolation", "PASS"))

        # T6 outcome cannot mutate signal fields
        expect_error(lambda: append_outcome(log, "S2", "5d", {"validated_regime": "R1"}))
        results.append(("T6 outcome cannot rewrite signal", "PASS"))

        # T7 documented correction preserves audit history
        before_lines = log.read_text(encoding="utf-8").strip().splitlines()
        append_correction(log, "S1", {"validated_regime": "R5"}, "documented input correction")
        after_lines = log.read_text(encoding="utf-8").strip().splitlines()
        p = {r["sample_id"]: r for r in build_projection(log)}
        assert len(after_lines) == len(before_lines) + 1
        assert p["S1"]["validated_regime"] == "R5" and p["S1"]["correction_count"] == 1
        results.append(("T7 append-only correction audit", "PASS"))

        # T8 correction cannot alter outcome fields
        expect_error(lambda: append_correction(log, "S1", {"ret_20d": 0.5}, "bad correction"))
        results.append(("T8 correction boundary", "PASS"))

        # T9 BLOCKED sample retained
        s4 = base_signal("S4", "BLOCKED")
        s4["action_direction"] = "BLOCKED"
        s4["mapper_status"] = "HOLD / CONFLICT"
        append_signal(log, s4)
        p = {r["sample_id"]: r for r in build_projection(log)}
        assert "S4" in p and p["S4"]["quality"] == "BLOCKED"
        results.append(("T9 blocked observations retained", "PASS"))

        # T10 deterministic CSV projection
        write_projection_csv(log, csvp)
        a = csvp.read_text(encoding="utf-8-sig")
        write_projection_csv(log, csvp)
        b = csvp.read_text(encoding="utf-8-sig")
        assert a == b and "sample_id" in a and "S1" in a and "S4" in a
        results.append(("T10 deterministic CSV projection", "PASS"))

    return results


def main():
    results = run_tests()
    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    md = [
        "# Full Evidence Runtime Log v0.1 — Deterministic Test",
        "",
        "Status: EXPERIMENTAL LOGGING-LAYER VALIDATION / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{sum(r == 'PASS' for _, r in results)}/{len(results)} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    md += [f"| {name} | {status} |" for name, status in results]
    md += [
        "",
        "Validated semantics:",
        "- signal-time evidence is frozen before outcomes mature",
        "- duplicate samples are rejected",
        "- missing evidence remains explicit and is never silently neutralized",
        "- +1d/+5d/+20d outcomes mature independently",
        "- outcomes cannot rewrite signal-time fields",
        "- documented corrections are append-only and auditable",
        "- BLOCKED/PARTIAL samples remain in the dataset",
        "- CSV is a deterministic projection of the canonical JSONL journal",
        "",
        "This validates logging semantics only. It does not validate market timing or official 3.2 integration.",
    ]
    (outdir / "full_evidence_runtime_log_v0_1_test_results.md").write_text("\n".join(md), encoding="utf-8")
    (outdir / "full_evidence_runtime_log_v0_1_test_results.json").write_text(
        json.dumps({"passed": len(results), "total": len(results), "tests": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\n".join(md))


if __name__ == "__main__":
    main()
