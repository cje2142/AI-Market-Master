import json
from pathlib import Path

from full_evidence_candidate_evaluator_v1_0 import CategoryEvidence, CandidateFlags
from full_evidence_candidate_input_contract_v1_0 import (
    CandidateInput,
    CostGateContext,
    PreviousOverlayState,
)
from full_evidence_candidate_risk_budget_connector_v1_0 import (
    PortfolioExecutionContext,
    connect_candidate_to_risk_budget,
)
from risk_budget_execution_v0_1 import Sleeves


def _categories(*, trends=None, polarities=None, strengths=None):
    trends = trends or {}
    polarities = polarities or {}
    strengths = strengths or {}
    return {
        f"C{i}": CategoryEvidence(
            status="VERIFIED",
            value=0.0,
            trend=trends.get(f"C{i}", "STABLE"),
            polarity=polarities.get(f"C{i}", "NEUTRAL"),
            strength=strengths.get(f"C{i}", "NORMAL"),
        )
        for i in range(1, 9)
    }


def _input(
    *,
    current_target=100,
    regime="R3",
    flags=None,
    trends=None,
    polarities=None,
    strengths=None,
    quality="FULL",
    sessions_since_reduction=None,
):
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
        categories=_categories(trends=trends, polarities=polarities, strengths=strengths),
        flags=flags or CandidateFlags(),
        previous=PreviousOverlayState(
            current_target_risk_budget=current_target,
            previous_action_direction="NONE",
            trading_sessions_since_last_reduction=sessions_since_reduction,
        ),
        cost_gate=CostGateContext(
            status="PASS",
            expected_edge_bps=30.0,
            estimated_total_cost_bps=10.0,
        ),
        source_reason_codes=("TEST_SOURCE",),
    )


def _base_reduction(current_target=100):
    trends = {"C1": "DETERIORATING", "C3": "DETERIORATING", "C6": "DETERIORATING"}
    return _input(current_target=current_target, regime="R4", trends=trends)


def _strong_reduction(current_target=90):
    trends = {c: "DETERIORATING" for c in ("C1", "C2", "C3", "C5", "C7")}
    strengths = {"C1": "STRONG"}
    flags = CandidateFlags(c5_structural_breakdown=True, c7_volatility_expansion=True)
    return _input(
        current_target=current_target,
        regime="R5",
        flags=flags,
        trends=trends,
        strengths=strengths,
        sessions_since_reduction=1,
    )


def _base_restore(current_target=60):
    trends = {"C1": "IMPROVING", "C3": "IMPROVING", "C5": "IMPROVING"}
    flags = CandidateFlags(r8_entry=True, c5_structure_recovery=True)
    return _input(current_target=current_target, regime="R8", flags=flags, trends=trends)


def _fast_restore(current_target=60):
    trends = {c: "IMPROVING" for c in ("C1", "C2", "C3", "C5")}
    flags = CandidateFlags(r7_to_r8_transition=True, c5_structure_recovery=True)
    return _input(current_target=current_target, regime="R8", flags=flags, trends=trends)


def _portfolio(
    current,
    baseline=None,
    *,
    core_auth=False,
    leverage_auth=False,
    exact=True,
):
    baseline = baseline or Sleeves(80, 10, 10)
    return PortfolioExecutionContext(
        baseline=baseline,
        current=current,
        core_reduction_authorized=core_auth,
        leverage_restore_authorized=leverage_auth,
        risk_coefficients_complete=exact,
    )


def run_tests():
    out = []

    # T1 HOLD must never invoke a portfolio transition.
    r = connect_candidate_to_risk_budget(_input(), _portfolio(Sleeves(80, 10, 10)))
    assert r.decision.action_direction == "HOLD"
    assert r.after == r.before and r.mapper_status == "NOT EXECUTED"
    out.append(("T1 HOLD produces no portfolio action", "PASS"))

    # T2 100->95 reduction consumes Leverage first.
    r = connect_candidate_to_risk_budget(_base_reduction(), _portfolio(Sleeves(80, 10, 10)))
    assert r.decision.action_direction == "REDUCE" and r.candidate_target_risk_budget == 95
    assert r.after == Sleeves(80, 10, 5)
    assert r.mapper_actions[0] == "Reduce Leverage 5.00"
    out.append(("T2 Candidate reduction maps to Leverage first", "PASS"))

    # T3 same market target, no leverage -> Tactical is reduced; market decision unchanged.
    r = connect_candidate_to_risk_budget(
        _base_reduction(),
        _portfolio(Sleeves(80, 20, 0), baseline=Sleeves(80, 20, 0)),
    )
    assert r.candidate_target_risk_budget == 95 and r.after == Sleeves(80, 15, 0)
    assert r.mapper_actions[0] == "Reduce Tactical 5.00"
    out.append(("T3 portfolio composition changes mapping, not market target", "PASS"))

    # T4 Core Preservation Gate stops an unauthorized Core sale.
    r = connect_candidate_to_risk_budget(
        _strong_reduction(current_target=90),
        _portfolio(Sleeves(90, 0, 0), baseline=Sleeves(90, 5, 5), core_auth=False),
    )
    assert r.decision.target_risk_budget == 80
    assert r.after == Sleeves(90, 0, 0)
    assert r.mapper_status == "PARTIAL EXECUTION / CORE PROTECTED"
    out.append(("T4 Core Preservation Gate retained", "PASS"))

    # T5 explicit Core authority permits residual reduction.
    r = connect_candidate_to_risk_budget(
        _strong_reduction(current_target=90),
        _portfolio(Sleeves(90, 0, 0), baseline=Sleeves(90, 5, 5), core_auth=True),
    )
    assert r.after == Sleeves(80, 0, 0) and r.mapper_status == "EXECUTABLE"
    out.append(("T5 explicit Core authority reaches target", "PASS"))

    # T6 restoration fills Core before Tactical and Leverage.
    baseline = Sleeves(90, 5, 5)
    r = connect_candidate_to_risk_budget(
        _base_restore(current_target=60),
        _portfolio(Sleeves(60, 0, 0), baseline=baseline, leverage_auth=True),
    )
    assert r.decision.target_risk_budget == 70
    assert r.after == Sleeves(70, 0, 0)
    assert r.mapper_actions[0] == "Restore Core 10.00"
    out.append(("T6 restoration starts with Core", "PASS"))

    # T7 leverage restoration remains separately authorized.
    polarities = {c: "POSITIVE" for c in ("C1", "C2", "C3", "C5")}
    inp = _input(current_target=90, regime="R1", polarities=polarities)
    r = connect_candidate_to_risk_budget(
        inp,
        _portfolio(Sleeves(90, 5, 0), baseline=baseline, leverage_auth=False),
    )
    assert r.decision.target_risk_budget == 100
    assert r.after == Sleeves(90, 5, 0)
    assert r.mapper_status == "LEVERAGE RESTORE BLOCKED"
    out.append(("T7 leverage restore authority remains separate", "PASS"))

    # T8 incomplete risk coefficients remain DATA PARTIAL, never fabricated.
    r = connect_candidate_to_risk_budget(
        _base_reduction(),
        _portfolio(Sleeves(80, 10, 10), exact=False),
    )
    assert r.after == Sleeves(80, 10, 5)
    assert r.mapper_status == "DATA PARTIAL"
    out.append(("T8 missing exact risk multipliers remain DATA PARTIAL", "PASS"))

    # T9 REDUCE cannot accidentally restore if actual risk is already below target.
    r = connect_candidate_to_risk_budget(
        _base_reduction(),
        _portfolio(Sleeves(80, 10, 4)),
    )
    assert r.decision.action_direction == "REDUCE" and r.decision.target_risk_budget == 95
    assert r.after == r.before and r.mapper_status == "NOT EXECUTED"
    assert r.integration_status == "TARGET SATISFIED / NO DIRECTION INVERSION"
    out.append(("T9 REDUCE never inverts into restoration", "PASS"))

    # T10 RESTORE cannot accidentally reduce if actual risk is already above target.
    r = connect_candidate_to_risk_budget(
        _base_restore(current_target=60),
        _portfolio(Sleeves(80, 0, 0), baseline=baseline),
    )
    assert r.decision.action_direction == "RESTORE" and r.decision.target_risk_budget == 70
    assert r.after == r.before and r.mapper_status == "NOT EXECUTED"
    out.append(("T10 RESTORE never inverts into reduction", "PASS"))

    # T11 lagged actual portfolio may catch up only by the Candidate allowed step.
    r = connect_candidate_to_risk_budget(
        _strong_reduction(current_target=90),
        _portfolio(Sleeves(90, 5, 5), baseline=Sleeves(90, 5, 5), core_auth=True),
    )
    assert r.decision.target_risk_budget == 80 and r.decision.allowed_step_size == 10
    assert r.execution_target_risk_budget == 90
    assert abs(r.before.total - r.after.total - 10) < 1e-9
    assert r.integration_status == "PARTIAL / CANDIDATE TARGET NOT YET REACHED"
    out.append(("T11 lagged portfolio execution respects Candidate step cap", "PASS"))

    # T12 Fast V-rebound actual restoration is capped at the frozen +20pp.
    r = connect_candidate_to_risk_budget(
        _fast_restore(current_target=60),
        _portfolio(Sleeves(50, 0, 0), baseline=baseline, leverage_auth=True),
    )
    assert r.decision.target_risk_budget == 80 and r.decision.allowed_step_size == 20
    assert r.execution_target_risk_budget == 70
    assert abs(r.after.total - r.before.total - 20) < 1e-9
    out.append(("T12 Fast V-rebound portfolio move capped at +20pp", "PASS"))

    # T13 BLOCKED Candidate input never reaches mapper execution.
    r = connect_candidate_to_risk_budget(
        _input(current_target=90, regime="R7", quality="BLOCKED"),
        _portfolio(Sleeves(80, 10, 0)),
    )
    assert r.decision.action_direction == "BLOCKED"
    assert r.after == r.before and r.mapper_status == "NOT EXECUTED"
    out.append(("T13 BLOCKED Candidate never executes portfolio action", "PASS"))

    return out


def main():
    results = run_tests()
    passed = sum(status == "PASS" for _, status in results)
    total = len(results)

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)

    md = [
        "# Full Evidence Candidate -> Risk Budget Connector v1.0 — Deterministic Test",
        "",
        "Status: EXPERIMENTAL STEP-5 INTEGRATION TEST / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{passed}/{total} PASS**",
        "",
        "| Test | Result |",
        "|---|---|",
    ]
    md += [f"| {name} | {status} |" for name, status in results]
    md += [
        "",
        "Boundary: these tests validate Candidate-to-portfolio execution integration only. They do not establish profitability, market-timing performance, provisional adoption, or official 3.2 integration.",
    ]

    (outdir / "full_evidence_candidate_risk_budget_connector_v1_0_test_results.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )
    (outdir / "full_evidence_candidate_risk_budget_connector_v1_0_test_results.json").write_text(
        json.dumps({"passed": passed, "total": total, "tests": results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\n".join(md))


if __name__ == "__main__":
    main()
