import json
import tempfile
from datetime import date, timedelta
from pathlib import Path

import full_evidence_runtime_log_v0_1 as runtime
from full_evidence_runtime_validation_monitor_v0_1 import analyze, render_markdown


def signal(sample_id, market_date, regime="R7", quality="FULL", action="HOLD", mapper="NOT MAPPED"):
    cats = {f"C{i}": {"status": "VERIFIED", "value": 0.01 * i} for i in range(1, 9)}
    return {
        "sample_id": sample_id,
        "market_date": market_date,
        "timestamp": f"{market_date}T15:30:00+09:00",
        "session_checkpoint": "CLOSE",
        "data_mode": "TEST",
        "validation_status": "VERIFIED",
        "quality": quality,
        **cats,
        "preliminary_regime": regime,
        "validated_regime": regime,
        "transition_state": "NONE",
        "material_conflicts": [],
        "evidence_gate_result": "HOLD",
        "gate_reached": "NONE",
        "target_risk_budget": None,
        "action_direction": action,
        "allowed_step_size": 0,
        "reason_codes": ["TEST"],
        "core_before": None,
        "tactical_before": None,
        "leverage_before": None,
        "exact_risk_multipliers": False,
        "leverage_restore_authority": False,
        "core_reduction_authority": False,
        "core_after": None,
        "tactical_after": None,
        "leverage_after": None,
        "mapper_status": mapper,
        "action_hierarchy": [],
        "unresolved_constraints": [],
    }


def add_samples(log, n, start="2026-01-02", regimes=("R1", "R7"), actions=None):
    d0 = date.fromisoformat(start)
    for i in range(n):
        d = d0 + timedelta(days=i)
        action = actions[i] if actions and i < len(actions) else "HOLD"
        runtime.append_signal(log, signal(f"S{i:03d}", d.isoformat(), regimes[i % len(regimes)], action=action))


def run_tests():
    out = []

    # T1 empty log reports zero and no stage.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        log.write_text("", encoding="utf-8")
        m = analyze(log, "2026-01-02")
        assert m["total_samples"] == 0 and m["stage1"]["status"] == "NOT MET"
        out.append(("T1 empty dataset safe", "PASS"))

    # T2 20 samples across two R families satisfy Stage 1 explicit gate.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        add_samples(log, 20, regimes=("R1 Bull", "R7 Support"))
        m = analyze(log, "2026-02-01")
        assert m["stage1"]["status"] == "MET"
        assert m["distinct_classified_regime_families"] == 2
        out.append(("T2 Stage1 explicit gate", "PASS"))

    # T3 30 samples before 2 months cannot enter provisional manual review.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        add_samples(log, 30, regimes=("R1", "R4", "R7"))
        m = analyze(log, "2026-02-15")
        assert m["stage2a_provisional"]["status"] == "NOT YET ELIGIBLE"
        out.append(("T3 Stage2A time gate enforced", "PASS"))

    # T4 30 samples + 2 months + 3 regimes reaches manual review only, never auto-adopt.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        add_samples(log, 30, regimes=("R1", "R4", "R7"))
        m = analyze(log, "2026-03-02")
        assert m["stage2a_provisional"]["status"] == "MANUAL REVIEW REQUIRED"
        assert "at least 8 deterioration/risk-control observations" in m["stage2a_provisional"]["manual_checks_required"]
        out.append(("T4 provisional review never auto-adopts", "PASS"))

    # T5 three-month checkpoint becomes due by calendar-month arithmetic.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        add_samples(log, 1, start="2026-01-31", regimes=("R7",))
        m0 = analyze(log, "2026-04-29")
        m1 = analyze(log, "2026-04-30")
        assert not m0["stage2b_three_month_checkpoint"]["due"]
        assert m1["stage2b_three_month_checkpoint"]["due"]
        out.append(("T5 three-month checkpoint calendar logic", "PASS"))

    # T6 REDUCE/RESTORE counts remain explicitly tracking proxies only.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        actions = ["REDUCE"] * 10 + ["RESTORE"] * 10
        add_samples(log, 20, actions=actions)
        m = analyze(log, "2026-05-01")
        p = m["tracking_proxies_not_protocol_equivalents"]
        assert p["reduce_actions"] == 10 and p["restore_actions"] == 10
        assert "not automatically equivalent" in p["note"]
        out.append(("T6 no hidden observation classifier", "PASS"))

    # T7 correction count and matured outcomes come from canonical projection.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        runtime.append_signal(log, signal("S", "2026-01-02", "R7"))
        runtime.append_correction(log, "S", {"reason_codes": ["CORRECTED"]}, "test")
        runtime.append_outcome(log, "S", "1d", {"ret_1d": 0.01})
        m = analyze(log, "2026-01-05")
        assert m["correction_count"] == 1
        assert m["outcome_maturity"]["1d"]["count"] == 1
        assert m["outcome_maturity"]["5d"]["count"] == 0
        out.append(("T7 canonical correction and maturity counts", "PASS"))

    # T8 markdown reports current progress without inventing score/adoption.
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "r.jsonl"
        add_samples(log, 1, regimes=("R7",))
        m = analyze(log, "2026-01-02")
        md = render_markdown(m)
        assert "Samples: **1**" in md
        assert "does not create a score or decide adoption automatically" in md
        out.append(("T8 report boundary", "PASS"))

    return out


def main():
    results = run_tests()
    passed = sum(s == "PASS" for _, s in results)
    outdir = Path("results")
    outdir.mkdir(exist_ok=True)
    md = [
        "# Full Evidence Runtime Validation Monitor v0.1 — Deterministic Test",
        "",
        "Status: MONITORING LAYER / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{passed}/{len(results)} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    md += [f"| {name} | {status} |" for name, status in results]
    md += [
        "",
        "Boundary: the monitor reports Protocol v0.2 progress and explicit gates only. It does not create a hidden score, invent qualitative thresholds, or automatically adopt/reject the Candidate model.",
    ]
    (outdir / "full_evidence_runtime_validation_monitor_v0_1_test_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (outdir / "full_evidence_runtime_validation_monitor_v0_1_test_results.json").write_text(
        json.dumps({"passed": passed, "total": len(results), "tests": results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\n".join(md))


if __name__ == "__main__":
    main()
