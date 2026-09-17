import json
import tempfile
from datetime import date, timedelta
from pathlib import Path

import full_evidence_runtime_log_v0_1 as runtime
from full_evidence_outcome_updater_v0_1 import normalize_sessions, update_runtime_outcomes


def base_signal(sample_id, market_date):
    cats = {f"C{i}": {"status": "VERIFIED", "value": 0.01 * i} for i in range(1, 9)}
    return {
        "sample_id": sample_id,
        "market_date": market_date,
        "timestamp": f"{market_date}T15:30:00+09:00",
        "session_checkpoint": "CLOSE",
        "data_mode": "TEST",
        "validation_status": "VERIFIED",
        "quality": "FULL",
        **cats,
        "preliminary_regime": "R7",
        "validated_regime": "R7",
        "transition_state": "R8 WATCH",
        "material_conflicts": [],
        "evidence_gate_result": "HOLD",
        "gate_reached": "NONE",
        "target_risk_budget": None,
        "action_direction": "HOLD",
        "allowed_step_size": 0,
        "reason_codes": ["SAI_BALANCED_HOLD_-0.08"],
        "core_before": None,
        "tactical_before": None,
        "leverage_before": None,
        "exact_risk_multipliers": False,
        "leverage_restore_authority": False,
        "core_reduction_authority": False,
        "core_after": None,
        "tactical_after": None,
        "leverage_after": None,
        "mapper_status": "NOT MAPPED",
        "action_hierarchy": [],
        "unresolved_constraints": ["TEST"],
    }


def sessions_from_closes(start, closes):
    d = date.fromisoformat(start)
    out = []
    i = 0
    while i < len(closes):
        if d.weekday() < 5:
            out.append({"date": d, "close": closes[i]})
            i += 1
        d += timedelta(days=1)
    return out


def projection(log):
    return {r["sample_id"]: r for r in runtime.build_projection(log)}


def expect_error(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def run_tests():
    results = []

    # T1: +1d matures, later horizons remain pending.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S1", "2026-01-02"))
        summary = update_runtime_outcomes(log, csvp, sessions_from_closes("2026-01-02", [100, 102]))
        p = projection(log)["S1"]
        assert summary["appended_count"] == 1
        assert abs(p["ret_1d"] - 0.02) < 1e-12
        assert p["outcome_status_1d"] == "MATURE" and p["outcome_status_5d"] == "PENDING"
        results.append(("T1 +1d isolated maturation", "PASS"))

    # T2: +5d return and close-based MAE/MFE are exact.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S2", "2026-01-02"))
        update_runtime_outcomes(log, csvp, sessions_from_closes("2026-01-02", [100, 95, 97, 105, 90, 110]))
        p = projection(log)["S2"]
        assert abs(p["ret_5d"] - 0.10) < 1e-12
        assert abs(p["mae_5d"] - (-0.10)) < 1e-12
        assert abs(p["mfe_5d"] - 0.10) < 1e-12
        results.append(("T2 +5d return MAE MFE", "PASS"))

    # T3: +20d uses exactly 20 observed future sessions.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S3", "2026-01-02"))
        closes = [100] + list(range(101, 121))
        update_runtime_outcomes(log, csvp, sessions_from_closes("2026-01-02", closes))
        p = projection(log)["S3"]
        assert abs(p["ret_20d"] - 0.20) < 1e-12
        assert abs(p["mae_20d"] - 0.01) < 1e-12
        assert abs(p["mfe_20d"] - 0.20) < 1e-12
        results.append(("T3 +20d observed-session horizon", "PASS"))

    # T4: insufficient observed future sessions never get imputed.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S4", "2026-01-02"))
        update_runtime_outcomes(log, csvp, sessions_from_closes("2026-01-02", [100, 99, 98, 97, 96]))
        p = projection(log)["S4"]
        assert p["outcome_status_5d"] == "PENDING" and p["ret_5d"] is None
        assert p["outcome_status_20d"] == "PENDING"
        results.append(("T4 unavailable future stays PENDING", "PASS"))

    # T5: rerun is idempotent; mature horizons are not duplicated.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S5", "2026-01-02"))
        sess = sessions_from_closes("2026-01-02", [100, 101, 102, 103, 104, 105])
        first = update_runtime_outcomes(log, csvp, sess)
        lines_before = len(log.read_text(encoding="utf-8").strip().splitlines())
        second = update_runtime_outcomes(log, csvp, sess)
        lines_after = len(log.read_text(encoding="utf-8").strip().splitlines())
        assert first["appended_count"] == 2 and second["appended_count"] == 0
        assert lines_before == lines_after
        results.append(("T5 idempotent rerun no duplicate outcome", "PASS"))

    # T6: documented signal correction survives outcome maturation unchanged.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S6", "2026-01-02"))
        runtime.append_correction(log, "S6", {"reason_codes": ["SAI_BALANCED_HOLD_-0.08", "CORRECTED"]}, "test correction")
        update_runtime_outcomes(log, csvp, sessions_from_closes("2026-01-02", [100, 101]))
        p = projection(log)["S6"]
        assert p["reason_codes"] == ["SAI_BALANCED_HOLD_-0.08", "CORRECTED"]
        assert p["correction_count"] == 1 and p["outcome_status_1d"] == "MATURE"
        results.append(("T6 signal correction remains immutable to outcome", "PASS"))

    # T7: multiple samples mature independently from their own signal dates.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S7A", "2026-01-02"))
        runtime.append_signal(log, base_signal("S7B", "2026-01-06"))
        sess = sessions_from_closes("2026-01-02", [100, 101, 102, 103, 104, 105])
        update_runtime_outcomes(log, csvp, sess)
        p = projection(log)
        assert p["S7A"]["outcome_status_5d"] == "MATURE"
        assert p["S7B"]["outcome_status_1d"] == "MATURE" and p["S7B"]["outcome_status_5d"] == "PENDING"
        results.append(("T7 independent multi-sample maturation", "PASS"))

    # T8: absent signal date is explicit unavailable, never nearest-date substituted.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S8", "2026-01-03"))
        summary = update_runtime_outcomes(log, csvp, sessions_from_closes("2026-01-02", [100, 101, 102]))
        p = projection(log)["S8"]
        assert len(summary["unavailable"]) == 1 and summary["appended_count"] == 0
        assert p["outcome_status_1d"] == "PENDING"
        results.append(("T8 no nearest-date substitution", "PASS"))

    # T9: corrupt observed data is rejected rather than silently repaired.
    dup = [{"date": "2026-01-02", "close": 100}, {"date": "2026-01-02", "close": 101}]
    expect_error(lambda: normalize_sessions(dup))
    expect_error(lambda: normalize_sessions([{"date": "2026-01-02", "close": 0}]))
    results.append(("T9 duplicate or invalid observed data rejected", "PASS"))

    # T10: year-boundary maturation uses observed sequence, not calendar-day arithmetic.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); log = td / "r.jsonl"; csvp = td / "r.csv"
        runtime.initialize_store(log, csvp)
        runtime.append_signal(log, base_signal("S10", "2026-12-31"))
        sess = [
            {"date": "2026-12-31", "close": 100},
            {"date": "2027-01-04", "close": 103},
        ]
        update_runtime_outcomes(log, csvp, sess)
        p = projection(log)["S10"]
        assert abs(p["ret_1d"] - 0.03) < 1e-12
        results.append(("T10 year-boundary observed-session maturation", "PASS"))

    return results


def main():
    results = run_tests()
    passed = sum(status == "PASS" for _, status in results)
    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    md = [
        "# Full Evidence Outcome Updater v0.1 — Deterministic Test",
        "",
        "Status: EXPERIMENTAL VALIDATION LAYER / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{passed}/{len(results)} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    md += [f"| {name} | {status} |" for name, status in results]
    md += [
        "",
        "Validated boundaries:",
        "- outcomes append only after observed KOSPI trading sessions exist",
        "- +1d/+5d/+20d mature independently",
        "- MAE/MFE use intervening closes only",
        "- unavailable future sessions stay PENDING and are never imputed",
        "- reruns are idempotent and do not duplicate OUTCOME events",
        "- signal-time fields and documented CORRECTION history remain untouched",
        "- missing signal dates are not silently replaced with nearest dates",
        "- malformed observed price data fails closed",
        "- year boundaries use observed-session order rather than calendar-day arithmetic",
        "",
        "This validates updater semantics only. It does not validate market timing or official 3.2 integration.",
    ]
    (outdir / "full_evidence_outcome_updater_v0_1_test_results.md").write_text("\n".join(md), encoding="utf-8")
    (outdir / "full_evidence_outcome_updater_v0_1_test_results.json").write_text(
        json.dumps({"passed": passed, "total": len(results), "tests": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\n".join(md))


if __name__ == "__main__":
    main()
