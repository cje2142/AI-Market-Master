"""AI Market Master 3.2 — Full Evidence Candidate Evaluator v1.0.

Step 1 implementation only: deterministic evaluation of the frozen Candidate v1.0
Evidence Gates. This module deliberately does NOT yet choose a target risk budget,
action direction, portfolio mapping, or Runtime Log output. Those are wired in later
steps so no hidden transition rule is introduced here.

Important boundary:
- Raw C1-C8 numeric values are preserved as evidence, but this evaluator does not
  invent thresholds to decide whether a category is improving/deteriorating.
- Direction/strength/structural flags must be supplied explicitly by the normalized
  Candidate input layer that will be frozen in Step 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional, Tuple

CATEGORIES = tuple(f"C{i}" for i in range(1, 9))
A_CLASS = frozenset({"C1", "C2", "C5"})
B_CLASS = frozenset({"C3", "C4"})
C_CLASS = frozenset({"C6", "C7", "C8"})

VALID_TRENDS = frozenset({"DETERIORATING", "IMPROVING", "STABLE", "UNKNOWN"})
VALID_POLARITIES = frozenset({"POSITIVE", "NEGATIVE", "NEUTRAL", "CONFLICT", "MISSING", "UNKNOWN"})
VALID_STRENGTHS = frozenset({"NORMAL", "STRONG", "SHOCK", "UNKNOWN"})

REDUCTION_REGIMES = frozenset({"R4", "R5", "R6"})
STRONG_REDUCTION_REGIMES = frozenset({"R5", "R6"})
BULL_REGIMES = frozenset({"R1", "R2"})


@dataclass(frozen=True)
class CategoryEvidence:
    """Normalized per-category evidence used by Candidate v1.0 gates.

    value/status retain the official C1-C8 output. trend/polarity/strength are
    explicit normalized labels; this module never derives them from raw values.
    """

    status: str
    value: Optional[float]
    trend: str = "UNKNOWN"
    polarity: str = "UNKNOWN"
    strength: str = "UNKNOWN"

    def validate(self, name: str) -> None:
        trend = str(self.trend).upper()
        polarity = str(self.polarity).upper()
        strength = str(self.strength).upper()
        status = str(self.status).strip().upper()

        if trend not in VALID_TRENDS:
            raise ValueError(f"{name}: invalid trend {self.trend!r}")
        if polarity not in VALID_POLARITIES:
            raise ValueError(f"{name}: invalid polarity {self.polarity!r}")
        if strength not in VALID_STRENGTHS:
            raise ValueError(f"{name}: invalid strength {self.strength!r}")

        if self.value is None and status in {"VERIFIED", "VALID", "OK"}:
            raise ValueError(f"{name}: missing value cannot be marked valid")
        if self.value is None and polarity in {"POSITIVE", "NEGATIVE", "NEUTRAL"}:
            raise ValueError(f"{name}: missing value cannot be assigned numeric polarity")


@dataclass(frozen=True)
class CandidateFlags:
    """Explicit structural/context flags required by the frozen Candidate rules."""

    material_conflict: bool = False
    c5_reduction_conflict: bool = False
    r4_r5_persistence: bool = False
    r8_entry: bool = False
    r7_to_r8_transition: bool = False
    r8_persistence: bool = False
    strong_r8: bool = False
    c5_structural_breakdown: bool = False
    c5_structure_recovery: bool = False
    c6_liquidity_deterioration: bool = False
    c7_volatility_expansion: bool = False
    c7_stabilization: bool = False


@dataclass(frozen=True)
class CandidateState:
    validated_regime: str
    categories: Mapping[str, CategoryEvidence]
    flags: CandidateFlags = field(default_factory=CandidateFlags)

    def validate(self) -> None:
        regime = normalize_regime(self.validated_regime)
        if regime not in {f"R{i}" for i in range(1, 9)}:
            raise ValueError(f"invalid validated_regime: {self.validated_regime!r}")

        missing = [c for c in CATEGORIES if c not in self.categories]
        extra = [c for c in self.categories if c not in CATEGORIES]
        if missing:
            raise ValueError(f"missing categories: {missing}")
        if extra:
            raise ValueError(f"unexpected categories: {extra}")

        for name in CATEGORIES:
            obj = self.categories[name]
            if not isinstance(obj, CategoryEvidence):
                raise ValueError(f"{name}: must be CategoryEvidence")
            obj.validate(name)


@dataclass(frozen=True)
class GateResult:
    conflict_hold: bool
    reduction_5: bool
    reduction_additional_5: bool
    reduction_strong_10: bool
    reduction_deepest_70_to_60: bool
    restoration_10: bool
    restoration_additional_10: bool
    restoration_return_100: bool
    deterioration_categories: Tuple[str, ...]
    improving_categories: Tuple[str, ...]
    positive_categories: Tuple[str, ...]
    reasons: Tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "conflict_hold": self.conflict_hold,
            "reduction_5": self.reduction_5,
            "reduction_additional_5": self.reduction_additional_5,
            "reduction_strong_10": self.reduction_strong_10,
            "reduction_deepest_70_to_60": self.reduction_deepest_70_to_60,
            "restoration_10": self.restoration_10,
            "restoration_additional_10": self.restoration_additional_10,
            "restoration_return_100": self.restoration_return_100,
            "deterioration_categories": list(self.deterioration_categories),
            "improving_categories": list(self.improving_categories),
            "positive_categories": list(self.positive_categories),
            "reasons": list(self.reasons),
        }


def normalize_regime(value: str) -> str:
    """Extract canonical R1..R8 prefix from a descriptive Regime label."""
    text = str(value).strip().upper()
    for i in range(1, 9):
        token = f"R{i}"
        if text == token or text.startswith(token + " ") or text.startswith(token + "-"):
            return token
    return text


def _names_with(state: CandidateState, attr: str, expected: str) -> Tuple[str, ...]:
    expected = expected.upper()
    return tuple(
        c for c in CATEGORIES
        if str(getattr(state.categories[c], attr)).upper() == expected
    )


def _class_count(names: Iterable[str], evidence_class: frozenset[str]) -> int:
    return sum(1 for name in names if name in evidence_class)


def _represented_classes(names: Iterable[str]) -> int:
    name_set = set(names)
    return sum(bool(name_set & cls) for cls in (A_CLASS, B_CLASS, C_CLASS))


def _strong_deterioration(state: CandidateState, category: str) -> bool:
    obj = state.categories[category]
    return (
        str(obj.trend).upper() == "DETERIORATING"
        and str(obj.strength).upper() in {"STRONG", "SHOCK"}
    )


def evaluate_gates(state: CandidateState) -> GateResult:
    """Evaluate only the frozen Candidate v1.0 Evidence Gates.

    This function intentionally stops before selecting a risk-budget target or
    action. Step 3 will translate gate results plus previous target/cooldown/cost
    state into HOLD/REDUCE/RESTORE and 100/95/90/80/70/60.
    """

    state.validate()
    regime = normalize_regime(state.validated_regime)
    f = state.flags

    deteriorating = _names_with(state, "trend", "DETERIORATING")
    improving = _names_with(state, "trend", "IMPROVING")
    positive = _names_with(state, "polarity", "POSITIVE")

    a_deteriorating = _class_count(deteriorating, A_CLASS)
    a_improving = _class_count(improving, A_CLASS)
    a_positive = _class_count(positive, A_CLASS)

    c1_or_c2_strong_deterioration = (
        _strong_deterioration(state, "C1") or _strong_deterioration(state, "C2")
    )

    conflict_hold = bool(f.material_conflict)

    reduction_5 = (
        not conflict_hold
        and regime in REDUCTION_REGIMES
        and a_deteriorating >= 1
        and len(deteriorating) >= 3
        and not f.c5_reduction_conflict
    )

    reduction_additional_5 = (
        not conflict_hold
        and regime in {"R4", "R5"}
        and f.r4_r5_persistence
        and a_deteriorating >= 2
        and len(deteriorating) >= 4
        and _represented_classes(deteriorating) >= 2
    )

    reduction_strong_10 = (
        not conflict_hold
        and regime in STRONG_REDUCTION_REGIMES
        and c1_or_c2_strong_deterioration
        and f.c5_structural_breakdown
        and len(deteriorating) >= 5
        and (f.c6_liquidity_deterioration or f.c7_volatility_expansion)
    )

    reduction_deepest_70_to_60 = (
        not conflict_hold
        and regime == "R6"
        and len(deteriorating) >= 5
        and c1_or_c2_strong_deterioration
        and f.c5_structural_breakdown
    )

    restoration_10 = (
        not conflict_hold
        and (f.r8_entry or f.r7_to_r8_transition)
        and ("C1" in improving or "C2" in improving)
        and "C3" in improving
        and f.c5_structure_recovery
        and len(improving) >= 3
    )

    restoration_additional_10 = (
        not conflict_hold
        and regime == "R8"
        and f.r8_persistence
        and a_improving >= 2
        and len(improving) >= 4
        and (f.c7_stabilization or "C8" in improving)
    )

    restoration_return_100 = (
        not conflict_hold
        and (regime in BULL_REGIMES or f.strong_r8)
        and a_positive >= 2
        and len(positive) >= 4
    )

    reasons = []
    if conflict_hold:
        reasons.append("MATERIAL_CONFLICT_HOLD")
    if reduction_5:
        reasons.append("REDUCTION_GATE_5")
    if reduction_additional_5:
        reasons.append("REDUCTION_GATE_ADDITIONAL_5")
    if reduction_strong_10:
        reasons.append("REDUCTION_GATE_STRONG_10")
    if reduction_deepest_70_to_60:
        reasons.append("REDUCTION_GATE_DEEPEST_70_TO_60")
    if restoration_10:
        reasons.append("RESTORATION_GATE_10")
    if restoration_additional_10:
        reasons.append("RESTORATION_GATE_ADDITIONAL_10")
    if restoration_return_100:
        reasons.append("RESTORATION_GATE_RETURN_100")
    if not reasons:
        reasons.append("NO_CANDIDATE_GATE")

    return GateResult(
        conflict_hold=conflict_hold,
        reduction_5=reduction_5,
        reduction_additional_5=reduction_additional_5,
        reduction_strong_10=reduction_strong_10,
        reduction_deepest_70_to_60=reduction_deepest_70_to_60,
        restoration_10=restoration_10,
        restoration_additional_10=restoration_additional_10,
        restoration_return_100=restoration_return_100,
        deterioration_categories=tuple(deteriorating),
        improving_categories=tuple(improving),
        positive_categories=tuple(positive),
        reasons=tuple(reasons),
    )
