import json
from dataclasses import dataclass, asdict
from pathlib import Path

EPS = 1e-9


@dataclass(frozen=True)
class Sleeves:
    core: float
    tactical: float
    leverage: float

    @property
    def total(self) -> float:
        return self.core + self.tactical + self.leverage


@dataclass
class MapResult:
    before: Sleeves
    after: Sleeves
    target: float
    status: str
    actions: list[str]
    data_quality: str

    def to_dict(self):
        return {
            "before": asdict(self.before),
            "after": asdict(self.after),
            "before_total": self.before.total,
            "after_total": self.after.total,
            "target": self.target,
            "status": self.status,
            "actions": self.actions,
            "data_quality": self.data_quality,
        }


def _take(value: float, amount: float) -> tuple[float, float]:
    used = min(value, max(0.0, amount))
    return value - used, used


def map_risk_budget(
    current: Sleeves,
    baseline: Sleeves,
    target: float,
    *,
    full_evidence_authorized: bool,
    core_reduction_authorized: bool = False,
    leverage_restore_authorized: bool = False,
    risk_coefficients_complete: bool = True,
) -> MapResult:
    """Deterministic sleeve-level mapper for frozen Risk Budget Execution v0.1.

    This test implementation intentionally operates on normalized sleeve risk units.
    It does not invent beta/volatility coefficients for instruments.
    """
    actions: list[str] = []
    quality = "FULL" if risk_coefficients_complete else "PARTIAL"

    # Reduction requires Full Evidence permission. Regime context by itself is never enough.
    if target < current.total - EPS:
        if not full_evidence_authorized:
            return MapResult(
                current,
                current,
                target,
                "HOLD / CONFLICT",
                ["No reduction: Full Evidence execution permission absent"],
                quality,
            )

        core = current.core
        tactical = current.tactical
        leverage = current.leverage
        need = current.total - target

        leverage, used = _take(leverage, need)
        if used > EPS:
            actions.append(f"Reduce Leverage {used:.2f}")
            need -= used

        tactical, used = _take(tactical, need)
        if used > EPS:
            actions.append(f"Reduce Tactical {used:.2f}")
            need -= used

        if need > EPS and core_reduction_authorized:
            core, used = _take(core, need)
            if used > EPS:
                actions.append(f"Reduce Core {used:.2f}")
                need -= used

        after = Sleeves(round(core, 10), round(tactical, 10), round(leverage, 10))

        if need > EPS:
            status = "PARTIAL EXECUTION / CORE PROTECTED"
            actions.append(f"Unfilled reduction {need:.2f}: Core authority absent or insufficient")
        else:
            status = "EXECUTABLE"

        if not risk_coefficients_complete:
            status = "DATA PARTIAL"
            actions.append("Exact risk-unit translation unavailable; nominal sleeve mapping only")

        return MapResult(current, after, target, status, actions, quality)

    # Restoration does not create authorization to re-add leverage.
    if target > current.total + EPS:
        core = current.core
        tactical = current.tactical
        leverage = current.leverage
        need = target - current.total

        core_room = max(0.0, baseline.core - core)
        used = min(core_room, need)
        if used > EPS:
            core += used
            need -= used
            actions.append(f"Restore Core {used:.2f}")

        tactical_room = max(0.0, baseline.tactical - tactical)
        used = min(tactical_room, need)
        if used > EPS:
            tactical += used
            need -= used
            actions.append(f"Restore Tactical {used:.2f}")

        if need > EPS and leverage_restore_authorized:
            leverage_room = max(0.0, baseline.leverage - leverage)
            used = min(leverage_room, need)
            if used > EPS:
                leverage += used
                need -= used
                actions.append(f"Restore Leverage {used:.2f}")

        after = Sleeves(round(core, 10), round(tactical, 10), round(leverage, 10))

        if need > EPS and not leverage_restore_authorized and baseline.leverage > leverage:
            status = "LEVERAGE RESTORE BLOCKED"
            actions.append(f"Unfilled restoration {need:.2f}: leverage authorization absent")
        elif need > EPS:
            status = "PARTIAL EXECUTION / CORE PROTECTED"
            actions.append(f"Unfilled restoration {need:.2f}: baseline capacity insufficient")
        else:
            status = "EXECUTABLE"

        if not risk_coefficients_complete:
            status = "DATA PARTIAL"
            actions.append("Exact risk-unit translation unavailable; nominal sleeve mapping only")

        return MapResult(current, after, target, status, actions, quality)

    status = "DATA PARTIAL" if not risk_coefficients_complete else "EXECUTABLE"
    actions.append("No risk-budget change required")
    return MapResult(current, current, target, status, actions, quality)


def assert_sleeves(actual: Sleeves, expected: Sleeves):
    assert abs(actual.core - expected.core) < EPS, (actual, expected)
    assert abs(actual.tactical - expected.tactical) < EPS, (actual, expected)
    assert abs(actual.leverage - expected.leverage) < EPS, (actual, expected)


def run_tests():
    results = []

    # 1) 100 -> 95 with sufficient leverage: Core unchanged.
    b = Sleeves(80, 10, 10)
    r = map_risk_budget(b, b, 95, full_evidence_authorized=True)
    assert_sleeves(r.after, Sleeves(80, 10, 5))
    assert r.status == "EXECUTABLE"
    results.append(("T1 100->95 sufficient leverage", "PASS", r))

    # 2) 100 -> 90 with sufficient non-core: Core unchanged.
    r = map_risk_budget(b, b, 90, full_evidence_authorized=True)
    assert_sleeves(r.after, Sleeves(80, 10, 0))
    assert r.status == "EXECUTABLE"
    results.append(("T2 100->90 sufficient non-core", "PASS", r))

    # 3) 100 -> 80 with sufficient Leverage + Tactical: Core unchanged.
    r = map_risk_budget(b, b, 80, full_evidence_authorized=True)
    assert_sleeves(r.after, Sleeves(80, 0, 0))
    assert r.status == "EXECUTABLE"
    results.append(("T3 100->80 sufficient non-core", "PASS", r))

    # 4) Non-core insufficient and Core reduction not authorized.
    b4 = Sleeves(90, 5, 5)
    r = map_risk_budget(b4, b4, 80, full_evidence_authorized=True, core_reduction_authorized=False)
    assert_sleeves(r.after, Sleeves(90, 0, 0))
    assert abs(r.after.total - 90) < EPS
    assert r.status == "PARTIAL EXECUTION / CORE PROTECTED"
    results.append(("T4 Core Preservation Gate", "PASS", r))

    # 5) 80 -> 100 recovery: Core first, Tactical second, Leverage last.
    baseline5 = Sleeves(90, 5, 5)
    current5 = Sleeves(80, 0, 0)
    r = map_risk_budget(
        current5,
        baseline5,
        100,
        full_evidence_authorized=True,
        leverage_restore_authorized=True,
    )
    assert_sleeves(r.after, baseline5)
    assert r.actions[:3] == ["Restore Core 10.00", "Restore Tactical 5.00", "Restore Leverage 5.00"]
    assert r.status == "EXECUTABLE"
    results.append(("T5 80->100 recovery order", "PASS", r))

    # 6) Missing exact risk coefficients: nominal mapping allowed, numeric translation flagged PARTIAL.
    r = map_risk_budget(b, b, 95, full_evidence_authorized=True, risk_coefficients_complete=False)
    assert_sleeves(r.after, Sleeves(80, 10, 5))
    assert r.status == "DATA PARTIAL"
    assert r.data_quality == "PARTIAL"
    results.append(("T6 Missing risk multipliers", "PASS", r))

    # 7) Same market target, different portfolio composition -> different sleeve mapping.
    pa = Sleeves(80, 10, 10)
    pb = Sleeves(70, 30, 0)
    ra = map_risk_budget(pa, pa, 90, full_evidence_authorized=True)
    rb = map_risk_budget(pb, pb, 90, full_evidence_authorized=True)
    assert abs(ra.after.total - 90) < EPS and abs(rb.after.total - 90) < EPS
    assert ra.after != rb.after
    assert_sleeves(ra.after, Sleeves(80, 10, 0))
    assert_sleeves(rb.after, Sleeves(70, 20, 0))
    results.append(("T7 Portfolio composition independence", "PASS", ra))
    results.append(("T7B Alternate portfolio mapping", "PASS", rb))

    # 8) R6/Panic context without Full Evidence execution permission -> no automatic reduction/core sale.
    b8 = Sleeves(90, 5, 5)
    r = map_risk_budget(
        b8,
        b8,
        80,
        full_evidence_authorized=False,
        core_reduction_authorized=False,
    )
    assert_sleeves(r.after, b8)
    assert r.status == "HOLD / CONFLICT"
    results.append(("T8 Panic without Full Evidence permission", "PASS", r))

    # Additional guard: recovery target 100 but leverage authorization absent.
    r = map_risk_budget(
        current5,
        baseline5,
        100,
        full_evidence_authorized=True,
        leverage_restore_authorized=False,
    )
    assert_sleeves(r.after, Sleeves(90, 5, 0))
    assert r.status == "LEVERAGE RESTORE BLOCKED"
    results.append(("Guard leverage restore authorization", "PASS", r))

    return results


def main():
    results = run_tests()
    outdir = Path(__file__).parent / "results"
    outdir.mkdir(exist_ok=True)

    payload = {
        "version": "Risk Budget Execution v0.1",
        "status": "DETERMINISTIC TEST",
        "official_3_2_authority": False,
        "tests_passed": sum(1 for _, s, _ in results if s == "PASS"),
        "tests_total": len(results),
        "results": [
            {"name": name, "result": status, **mapped.to_dict()}
            for name, status, mapped in results
        ],
    }

    with open(outdir / "risk_budget_execution_v0_1_test_results.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    lines = [
        "# AI Market Master 3.2 — Risk Budget Execution v0.1 Deterministic Test",
        "",
        "Status: EXPERIMENTAL EXECUTION-LAYER VALIDATION / NOT OFFICIAL 3.2 AUTHORITY",
        "",
        f"Result: **{payload['tests_passed']}/{payload['tests_total']} PASS**",
        "",
        "| Test | Result | Before (C/T/L) | Target | After (C/T/L) | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for name, status, mapped in results:
        b = mapped.before
        a = mapped.after
        lines.append(
            f"| {name} | {status} | {b.core:.0f}/{b.tactical:.0f}/{b.leverage:.0f} | "
            f"{mapped.target:.0f} | {a.core:.0f}/{a.tactical:.0f}/{a.leverage:.0f} | {mapped.status} |"
        )

    lines += [
        "",
        "## Validation meaning",
        "- Reduction consumes Leverage before Tactical and Core.",
        "- Core is not sold merely to force the numeric target when Core authority is absent.",
        "- Recovery restores Core, then Tactical, then separately-authorized Leverage.",
        "- Missing exact risk multipliers produces DATA PARTIAL rather than fabricated coefficients.",
        "- The same market target maps differently when portfolio sleeve composition changes.",
        "- R6/Panic context without Full Evidence execution permission does not trigger automatic selling.",
        "",
        "This test validates deterministic execution semantics only. It does not validate market timing, future returns, or official 3.2 integration.",
    ]

    with open(outdir / "risk_budget_execution_v0_1_test_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
