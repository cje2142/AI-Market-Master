import json
from pathlib import Path

from full_evidence_candidate_evaluator_v1_0 import CategoryEvidence, CandidateFlags
from full_evidence_candidate_input_contract_v1_0 import (
    CandidateInput,
    CostGateContext,
    PreviousOverlayState,
)
from full_evidence_candidate_transition_engine_v1_0 import evaluate_transition


def _categories(*, trends=None, polarities=None, strengths=None, missing=None):
    trends = trends or {}
    polarities = polarities or {}
    strengths = strengths or {}
    missing = set(missing or [])
    out = {}
    for i in range(1, 9):
        c = f"C{i}"
        if c in missing:
            out[c] = CategoryEvidence(
                status="DATA UNAVAILABLE",
                value=None,
                trend=trends.get(c, "UNKNOWN"),
                polarity=polarities.get(c, "MISSING"),
                strength=strengths.get(c, "UNKNOWN"),
            )
        else:
            out[c] = CategoryEvidence(
                status="VERIFIED",
                value=0.0,
                trend=trends.get(c, "STABLE"),
                polarity=polarities.get(c, "NEUTRAL"),
                strength=strengths.get(c, "NORMAL"),
            )
    return out


def _cost(status="PASS"):
    if status == "PASS":
        return CostGateContext(status="PASS", expected_edge_bps=30.0, estimated_total_cost_bps=10.0)
    if status == "FAIL":
        return CostGateContext(status="FAIL", expected_edge_bps=10.0, estimated_total_cost_bps=10.0)
    if status == "UNAVAILABLE":
        return CostGateContext(status="UNAVAILABLE")
    if status == "EMERGENCY_BYPASS":
        return CostGateContext(status="EMERGENCY_BYPASS", emergency_reason="confirmed R6 structural-risk control")
    raise ValueError(status)


def _input(
    *,
    current=100,
    regime="R3",
    quality="FULL",
    flags=None,
    trends=None,
    polarities=None,
    strengths=None,
    missing=None,
    cost="PASS",
    previous_regime=None,
    sessions_since_reduction=None,
    conflict_reasons=(),
):
    flags = flags or CandidateFlags()
    return CandidateInput(
        market_date="2026-09-17",
        timestamp="2026-09-17T15:30:00+09:00",
        session_checkpoint="CLOSE",
        data_mode="TEST",
        validation_status="VERIFIED",
        quality=quality,
        preliminary_regime=regime,
        validated_regime=regime,
        transition_state="TEST",
        categories=_categories(
            trends=trends,
            polarities=polarities,
            strengths=strengths,
            missing=missing,
        ),
        flags=flags,
        previous=PreviousOverlayState(
            current_target_risk_budget=current,
            previous_action_direction="NONE",
            previous_validated_regime=previous_regime,
            previous_market_date="2026-09-16" if previous_regime else None,
            trading_sessions_since_last_reduction=sessions_since_reduction,
            trading_sessions_since_last_restoration=None,
        ),
        cost_gate=_cost(cost),
        candidate_conflict_reasons=tuple(conflict_reasons),
        source_reason_codes=("TEST_SOURCE",),
    )


def _strong_reduction_input(*, current, regime="R5", cost="PASS", previous_regime=None, sessions=1):
    trends = {c: "DETERIORATING" for c in ("C1", "C2", "C3", "C5", "C7")}
    strengths = {"C1": "STRONG"}
    flags = CandidateFlags(c5_structural_breakdown=True, c7_volatility_expansion=True)
    return _input(
        current=current,
        regime=regime,
        flags=flags,
        trends=trends,
        strengths=strengths,
        cost=cost,
        previous_regime=previous_regime,
        sessions_since_reduction=sessions,
    )


def run_tests():
    out = []

    # T1 — no qualifying gate => HOLD.
    d = evaluate_transition(_input())
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("HOLD", 100, 0)
    out.append(("T1 no gate remains HOLD", "PASS"))

    # T2 — base reduction gate maps 100 -> 95.
    trends = {"C1": "DETERIORATING", "C3": "DETERIORATING", "C6": "DETERIORATING"}
    d = evaluate_transition(_input(current=100, regime="R4", trends=trends))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("REDUCE", 95, 5)
    out.append(("T2 base reduction 100 to 95", "PASS"))

    # T3 — persisted additional gate maps 95 -> 90.
    trends = {c: "DETERIORATING" for c in ("C1", "C2", "C3", "C5")}
    flags = CandidateFlags(r4_r5_persistence=True)
    d = evaluate_transition(_input(current=95, regime="R4", flags=flags, trends=trends, sessions_since_reduction=1))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("REDUCE", 90, 5)
    out.append(("T3 additional reduction 95 to 90", "PASS"))

    # T4 — strong gate maps 90 -> 80.
    d = evaluate_transition(_strong_reduction_input(current=90))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("REDUCE", 80, 10)
    out.append(("T4 strong reduction 90 to 80", "PASS"))

    # T5 — strong gate maps 80 -> 70.
    d = evaluate_transition(_strong_reduction_input(current=80))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("REDUCE", 70, 10)
    out.append(("T5 strong reduction 80 to 70", "PASS"))

    # T6 — deepest R6 gate maps 70 -> 60.
    d = evaluate_transition(_strong_reduction_input(current=70, regime="R6"))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("REDUCE", 60, 10)
    assert d.gate_reached == "DEEPEST_REDUCTION_TO_60"
    out.append(("T6 deepest reduction 70 to 60", "PASS"))

    # T7 — stronger gate may satisfy shallower state path (R6 at 95 -> 90).
    d = evaluate_transition(_strong_reduction_input(current=95, regime="R6"))
    assert (d.action_direction, d.target_risk_budget) == ("REDUCE", 90)
    out.append(("T7 strong-gate fallback preserves discrete path", "PASS"))

    # T8 — same-direction reduction cooldown blocks when zero sessions elapsed.
    trends = {c: "DETERIORATING" for c in ("C1", "C2", "C3", "C5")}
    flags = CandidateFlags(r4_r5_persistence=True)
    d = evaluate_transition(
        _input(
            current=95,
            regime="R4",
            flags=flags,
            trends=trends,
            previous_regime="R4",
            sessions_since_reduction=0,
        )
    )
    assert d.action_direction == "HOLD" and d.target_risk_budget == 95
    assert d.cooldown_status == "COOLDOWN_BLOCKED"
    out.append(("T8 reduction cooldown blocks repeat action", "PASS"))

    # T9 — R5 -> R6 structural worsening bypasses zero-session cooldown.
    d = evaluate_transition(
        _strong_reduction_input(current=90, regime="R6", previous_regime="R5", sessions=0)
    )
    assert d.action_direction == "REDUCE" and d.target_risk_budget == 80
    assert d.cooldown_status == "COOLDOWN_BYPASS_R5_TO_R6"
    out.append(("T9 R5 to R6 cooldown bypass", "PASS"))

    # T10 — Cost Gate FAIL blocks an otherwise valid reduction.
    d = evaluate_transition(_strong_reduction_input(current=90, cost="FAIL"))
    assert d.action_direction == "HOLD" and d.target_risk_budget == 90
    assert d.cost_gate_status == "COST_GATE_FAIL"
    out.append(("T10 Cost Gate FAIL blocks reduction", "PASS"))

    # T11 — Cost Gate UNAVAILABLE remains explicit and does not become invented FAIL.
    d = evaluate_transition(_strong_reduction_input(current=90, cost="UNAVAILABLE"))
    assert d.action_direction == "REDUCE" and d.target_risk_budget == 80
    assert d.cost_gate_status == "COST_GATE_UNAVAILABLE"
    out.append(("T11 unavailable Cost Gate remains explicit", "PASS"))

    # T12 — emergency bypass is accepted only for qualifying R6 structural reduction.
    d = evaluate_transition(_strong_reduction_input(current=90, regime="R6", cost="EMERGENCY_BYPASS"))
    assert d.action_direction == "REDUCE" and d.target_risk_budget == 80
    assert d.cost_gate_status == "COST_GATE_EMERGENCY_BYPASS"
    out.append(("T12 R6 emergency Cost Gate bypass", "PASS"))

    # T13 — Candidate-level material conflict has precedence over a reduction gate.
    trends = {c: "DETERIORATING" for c in ("C1", "C3", "C6")}
    flags = CandidateFlags(material_conflict=True)
    d = evaluate_transition(
        _input(
            current=100,
            regime="R4",
            flags=flags,
            trends=trends,
            conflict_reasons=("TEST_MATERIAL_CONFLICT",),
        )
    )
    assert d.action_direction == "HOLD" and d.target_risk_budget == 100
    assert d.gate_reached == "CONFLICT"
    out.append(("T13 material conflict forces HOLD", "PASS"))

    # T14 — BLOCKED input remains blocked with unchanged target.
    d = evaluate_transition(_input(current=90, regime="R7", quality="BLOCKED"))
    assert d.action_direction == "BLOCKED" and d.target_risk_budget == 90
    out.append(("T14 blocked quality remains blocked", "PASS"))

    # T15 — missing PARTIAL evidence is preserved and cannot fabricate a reduction.
    d = evaluate_transition(_input(current=100, regime="R4", quality="PARTIAL", missing={"C1"}))
    assert d.action_direction == "HOLD" and d.target_risk_budget == 100
    out.append(("T15 missing evidence does not become neutral signal", "PASS"))

    # T16 — base Recovery Gate maps 60 -> 70.
    trends = {"C1": "IMPROVING", "C3": "IMPROVING", "C5": "IMPROVING"}
    flags = CandidateFlags(r8_entry=True, c5_structure_recovery=True)
    d = evaluate_transition(_input(current=60, regime="R8", flags=flags, trends=trends))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("RESTORE", 70, 10)
    out.append(("T16 base restoration 60 to 70", "PASS"))

    # T17 — additional Recovery Gate maps 80 -> 90.
    trends = {c: "IMPROVING" for c in ("C1", "C2", "C3", "C5")}
    flags = CandidateFlags(r8_persistence=True, c7_stabilization=True)
    d = evaluate_transition(_input(current=80, regime="R8", flags=flags, trends=trends))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("RESTORE", 90, 10)
    out.append(("T17 additional restoration 80 to 90", "PASS"))

    # T18 — Return-100 Gate maps 90 -> 100.
    polarities = {c: "POSITIVE" for c in ("C1", "C2", "C3", "C5")}
    d = evaluate_transition(_input(current=90, regime="R1", polarities=polarities))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("RESTORE", 100, 10)
    out.append(("T18 return-to-100 restoration", "PASS"))

    # T19 — frozen fast V-rebound may restore 60 -> 80, exactly +20pp.
    trends = {c: "IMPROVING" for c in ("C1", "C2", "C3", "C5")}
    flags = CandidateFlags(r7_to_r8_transition=True, c5_structure_recovery=True)
    d = evaluate_transition(_input(current=60, regime="R8", flags=flags, trends=trends))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("RESTORE", 80, 20)
    assert d.fast_recovery and d.cooldown_status == "FAST_RECOVERY_OVERRIDE"
    out.append(("T19 fast V-rebound 60 to 80", "PASS"))

    # T20 — Cost Gate FAIL also blocks an otherwise valid restoration.
    trends = {"C1": "IMPROVING", "C3": "IMPROVING", "C5": "IMPROVING"}
    flags = CandidateFlags(r8_entry=True, c5_structure_recovery=True)
    d = evaluate_transition(_input(current=60, regime="R8", flags=flags, trends=trends, cost="FAIL"))
    assert d.action_direction == "HOLD" and d.target_risk_budget == 60
    assert d.cost_gate_status == "COST_GATE_FAIL"
    out.append(("T20 Cost Gate FAIL blocks restoration", "PASS"))

    # T21 — emergency bypass cannot be used for restoration.
    d = evaluate_transition(
        _input(current=60, regime="R8", flags=flags, trends=trends, cost="EMERGENCY_BYPASS")
    )
    assert d.action_direction == "HOLD" and d.target_risk_budget == 60
    assert d.cost_gate_status == "COST_GATE_BYPASS_NOT_APPLICABLE"
    out.append(("T21 emergency bypass rejected for restoration", "PASS"))

    # T22 — standard Recovery Gate restores 95 -> 100 without an ad-hoc state.
    d = evaluate_transition(_input(current=95, regime="R8", flags=flags, trends=trends))
    assert (d.action_direction, d.target_risk_budget, d.allowed_step_size) == ("RESTORE", 100, 5)
    out.append(("T22 standard restoration 95 to 100", "PASS"))

    return out


def main():
    results = run_tests()
    passed = sum(status == "PASS" for _, status in results)
    total = len(results)

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    md = [
        "# Full Evidence Candidate Transition Engine v1.0 — Deterministic Test",
        "",
        "Status: EXPERIMENTAL CANDIDATE TEST / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{passed}/{total} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    md += [f"| {name} | {status} |" for name, status in results]
    md += [
        "",
        "Boundary: these tests validate frozen Candidate v1.0 transition semantics only. They do not establish profitability, market-timing performance, provisional adoption, or official 3.2 integration.",
    ]

    (outdir / "full_evidence_candidate_transition_engine_v1_0_test_results.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )
    (outdir / "full_evidence_candidate_transition_engine_v1_0_test_results.json").write_text(
        json.dumps({"passed": passed, "total": total, "tests": results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\n".join(md))


if __name__ == "__main__":
    main()
