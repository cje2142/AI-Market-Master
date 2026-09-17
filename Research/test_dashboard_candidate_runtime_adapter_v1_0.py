import copy
import json
import tempfile
from pathlib import Path

import full_evidence_runtime_log_v0_1 as runtime
from dashboard_candidate_runtime_adapter_v1_0 import (
    build_runtime_sample,
    sample_id_for,
    validate_dashboard_candidate_snapshot,
)
from process_dashboard_candidate_runtime_inbox_v1_0 import process_inbox


FLAG_NAMES = (
    "material_conflict",
    "c5_reduction_conflict",
    "r4_r5_persistence",
    "r8_entry",
    "r7_to_r8_transition",
    "r8_persistence",
    "strong_r8",
    "c5_structural_breakdown",
    "c5_structure_recovery",
    "c6_liquidity_deterioration",
    "c7_volatility_expansion",
    "c7_stabilization",
)


def _flags(**overrides):
    out = {name: False for name in FLAG_NAMES}
    out.update(overrides)
    return out


def _evidence(*, trends=None, polarities=None, strengths=None):
    trends = trends or {}
    polarities = polarities or {}
    strengths = strengths or {}
    return {
        f"C{i}": {
            "trend": trends.get(f"C{i}", "STABLE"),
            "polarity": polarities.get(f"C{i}", "NEUTRAL"),
            "strength": strengths.get(f"C{i}", "NORMAL"),
        }
        for i in range(1, 9)
    }


def _snapshot(
    *,
    regime="R3",
    current_target=100,
    evidence=None,
    flags=None,
    conflict_reasons=None,
    cost_status="PASS",
    portfolio=None,
    quality="FULL",
):
    cats = {f"C{i}": {"status": "VERIFIED", "value": 0.01 * i} for i in range(1, 9)}
    if cost_status == "PASS":
        cost = {"status": "PASS", "expected_edge_bps": 30.0, "estimated_total_cost_bps": 10.0}
    elif cost_status == "FAIL":
        cost = {"status": "FAIL", "expected_edge_bps": 10.0, "estimated_total_cost_bps": 10.0}
    elif cost_status == "UNAVAILABLE":
        cost = {"status": "UNAVAILABLE"}
    else:
        raise ValueError(cost_status)

    s = {
        "market_date": "2026-09-18",
        "timestamp": "2026-09-18T15:30:00+09:00",
        "session_checkpoint": "CLOSE",
        "data_mode": "TEST",
        "validation_status": "VERIFIED",
        "quality": quality,
        **cats,
        "preliminary_regime": regime,
        "validated_regime": regime,
        "transition_state": "TEST",
        "material_conflicts": [],
        "reason_codes": ["TEST_SOURCE"],
        "candidate": {
            "evidence": evidence or _evidence(),
            "flags": flags or _flags(),
            "previous": {
                "current_target_risk_budget": current_target,
                "previous_action_direction": "NONE",
                "previous_validated_regime": None,
                "previous_market_date": None,
                "trading_sessions_since_last_reduction": None,
                "trading_sessions_since_last_restoration": None,
            },
            "cost_gate": cost,
            "candidate_conflict_reasons": list(conflict_reasons or []),
        },
        "unresolved_constraints": [],
    }
    if portfolio is not None:
        s["portfolio"] = portfolio
    return s


def _portfolio(baseline=(80, 10, 10), current=None, core_auth=False, lev_auth=False, exact=True):
    current = current or baseline
    return {
        "baseline": {"core": baseline[0], "tactical": baseline[1], "leverage": baseline[2]},
        "current": {"core": current[0], "tactical": current[1], "leverage": current[2]},
        "core_reduction_authorized": core_auth,
        "leverage_restore_authorized": lev_auth,
        "risk_coefficients_complete": exact,
    }


def run_tests():
    out = []

    # T1: no gate, no portfolio => Candidate HOLD is logged automatically.
    s = _snapshot()
    row = build_runtime_sample(s)
    assert row["action_direction"] == "HOLD"
    assert row["target_risk_budget"] == 100
    assert row["mapper_status"] == "NOT MAPPED"
    assert "CANDIDATE_V1_0" in row["reason_codes"]
    out.append(("T1 Dashboard to Candidate HOLD runtime sample", "PASS"))

    # T2: base R4 reduction automatically flows through mapper and removes Leverage first.
    trends = {"C1": "DETERIORATING", "C3": "DETERIORATING", "C6": "DETERIORATING"}
    s = _snapshot(regime="R4", evidence=_evidence(trends=trends), portfolio=_portfolio())
    row = build_runtime_sample(s)
    assert (row["action_direction"], row["target_risk_budget"]) == ("REDUCE", 95)
    assert (row["core_after"], row["tactical_after"], row["leverage_after"]) == (80.0, 10.0, 5.0)
    assert row["mapper_status"] == "EXECUTABLE"
    out.append(("T2 reduction auto maps Leverage first", "PASS"))

    # T3: Candidate-level conflict forces HOLD and mapper does not execute.
    trends = {"C1": "DETERIORATING", "C3": "DETERIORATING", "C6": "DETERIORATING"}
    s = _snapshot(
        regime="R4",
        evidence=_evidence(trends=trends),
        flags=_flags(material_conflict=True),
        conflict_reasons=["TEST_CONFLICT"],
        portfolio=_portfolio(),
    )
    s["material_conflicts"] = ["TEST_CONFLICT"]
    row = build_runtime_sample(s)
    assert row["action_direction"] == "HOLD"
    assert row["mapper_status"] == "NOT MAPPED"
    assert row["core_after"] == row["core_before"]
    out.append(("T3 conflict HOLD cannot become portfolio trade", "PASS"))

    # T4: BLOCKED quality remains BLOCKED and no portfolio action is created.
    s = _snapshot(quality="BLOCKED", portfolio=_portfolio())
    row = build_runtime_sample(s)
    assert row["action_direction"] == "BLOCKED"
    assert row["mapper_status"] == "NOT MAPPED"
    out.append(("T4 BLOCKED remains no-execution", "PASS"))

    # T5: explicit Candidate evidence labels are mandatory; no numeric-value inference fallback.
    s = _snapshot()
    del s["candidate"]["evidence"]["C5"]["trend"]
    try:
        validate_dashboard_candidate_snapshot(s)
        raise AssertionError("missing explicit trend was accepted")
    except ValueError as exc:
        assert "missing" in str(exc)
    out.append(("T5 explicit evidence labels required", "PASS"))

    # T6: all structural flags are explicit; omitted flag cannot silently become False.
    s = _snapshot()
    del s["candidate"]["flags"]["c7_stabilization"]
    try:
        validate_dashboard_candidate_snapshot(s)
        raise AssertionError("incomplete flags were accepted")
    except ValueError as exc:
        assert "explicit and complete" in str(exc)
    out.append(("T6 explicit complete structural flags required", "PASS"))

    # T7: stable signal identity excludes portfolio changes / derived execution.
    a = _snapshot(portfolio=_portfolio())
    b = copy.deepcopy(a)
    b["portfolio"] = _portfolio(baseline=(90, 5, 5), current=(90, 5, 5))
    assert sample_id_for(a) == sample_id_for(b)
    out.append(("T7 sample identity independent of portfolio", "PASS"))

    # T8: recovery maps into Core first.
    trends = {"C1": "IMPROVING", "C3": "IMPROVING", "C5": "IMPROVING"}
    s = _snapshot(
        regime="R8",
        current_target=60,
        evidence=_evidence(trends=trends),
        flags=_flags(r8_entry=True, c5_structure_recovery=True),
        portfolio=_portfolio(baseline=(90, 5, 5), current=(60, 0, 0)),
    )
    row = build_runtime_sample(s)
    assert (row["action_direction"], row["target_risk_budget"]) == ("RESTORE", 70)
    assert (row["core_after"], row["tactical_after"], row["leverage_after"]) == (70.0, 0.0, 0.0)
    out.append(("T8 restoration auto maps Core first", "PASS"))

    # T9: leverage restoration authority remains separate from Candidate recovery.
    polarities = {"C1": "POSITIVE", "C2": "POSITIVE", "C3": "POSITIVE", "C5": "POSITIVE"}
    s = _snapshot(
        regime="R1",
        current_target=90,
        evidence=_evidence(polarities=polarities),
        portfolio=_portfolio(baseline=(90, 5, 5), current=(90, 5, 0), lev_auth=False),
    )
    row = build_runtime_sample(s)
    assert row["action_direction"] == "RESTORE" and row["target_risk_budget"] == 100
    assert row["mapper_status"] == "LEVERAGE RESTORE BLOCKED"
    assert row["leverage_after"] == 0.0
    out.append(("T9 leverage restore authority remains separate", "PASS"))

    # T10: missing exact risk coefficients are retained as DATA PARTIAL.
    s = _snapshot(regime="R4", evidence=_evidence(trends={"C1": "DETERIORATING", "C3": "DETERIORATING", "C6": "DETERIORATING"}), portfolio=_portfolio(exact=False))
    row = build_runtime_sample(s)
    assert row["mapper_status"] == "DATA PARTIAL"
    assert row["exact_risk_multipliers"] is False
    out.append(("T10 missing risk coefficients remain DATA PARTIAL", "PASS"))

    # T11: end-to-end append writes canonical JSONL + CSV projection.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        inbox = td / "inbox"
        inbox.mkdir()
        s = _snapshot()
        (inbox / "one.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
        log = td / "runtime.jsonl"
        csv = td / "runtime.csv"
        result = process_inbox(inbox, log, csv)
        assert result[0]["status"] == "APPENDED"
        rows = runtime.build_projection(log)
        assert len(rows) == 1 and rows[0]["action_direction"] == "HOLD"
        assert csv.exists()
    out.append(("T11 end-to-end inbox to Runtime Log projection", "PASS"))

    # T12: duplicate same checkpoint is skipped rather than silently rewritten.
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        inbox = td / "inbox"
        inbox.mkdir()
        a = _snapshot(portfolio=_portfolio())
        b = copy.deepcopy(a)
        b["portfolio"] = _portfolio(baseline=(90, 5, 5), current=(90, 5, 5))
        (inbox / "a.json").write_text(json.dumps(a, ensure_ascii=False), encoding="utf-8")
        (inbox / "b.json").write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
        log = td / "runtime.jsonl"
        csv = td / "runtime.csv"
        result = process_inbox(inbox, log, csv)
        assert [x["status"] for x in result] == ["APPENDED", "SKIP DUPLICATE"]
        assert len(runtime.build_projection(log)) == 1
    out.append(("T12 duplicate checkpoint cannot silently rewrite signal", "PASS"))

    return out


def main():
    results = run_tests()
    passed = sum(status == "PASS" for _, status in results)
    total = len(results)
    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    md = [
        "# Dashboard -> Candidate -> Runtime v1.0 — Step 6 Deterministic Test",
        "",
        "Status: EXPERIMENTAL STEP-6 INTEGRATION / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{passed}/{total} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    md += [f"| {name} | {status} |" for name, status in results]
    md += [
        "",
        "Boundary: validates automatic plumbing and fail-closed semantics only; does not establish investment performance, provisional adoption, or official 3.2 integration.",
    ]

    (outdir / "dashboard_candidate_runtime_adapter_v1_0_test_results.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )
    (outdir / "dashboard_candidate_runtime_adapter_v1_0_test_results.json").write_text(
        json.dumps({"passed": passed, "total": total, "tests": results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\n".join(md))


if __name__ == "__main__":
    main()
