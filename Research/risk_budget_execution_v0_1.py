from dataclasses import dataclass, asdict

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
    """Reusable implementation of frozen Risk Budget Execution v0.1 semantics."""
    actions: list[str] = []
    quality = "FULL" if risk_coefficients_complete else "PARTIAL"

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
