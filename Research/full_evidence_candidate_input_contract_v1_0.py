"""AI Market Master 3.2 — Full Evidence Candidate v1.0 input contract.

Step 2 only. This module freezes and validates the normalized input supplied to the
Candidate evaluator. It does not choose a target risk budget, action direction,
portfolio trade, or Runtime Log output.

The Candidate must never infer improvement/deterioration, polarity, strength, or
structural flags from raw C1-C8 values unless a later version explicitly defines
that transformation. Those labels are explicit upstream evidence inputs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Mapping, Optional, Tuple

from full_evidence_candidate_evaluator_v1_0 import (
    CATEGORIES,
    CandidateFlags,
    CandidateState,
    CategoryEvidence,
    normalize_regime,
)

ALLOWED_RISK_BUDGETS = frozenset({60, 70, 80, 90, 95, 100})
ALLOWED_PREVIOUS_ACTIONS = frozenset({"NONE", "HOLD", "REDUCE", "RESTORE", "BLOCKED"})
ALLOWED_COST_GATE = frozenset({"PASS", "FAIL", "UNAVAILABLE", "EMERGENCY_BYPASS"})


@dataclass(frozen=True)
class PreviousOverlayState:
    """State carried from the immediately preceding Candidate evaluation.

    current_target_risk_budget is explicit. The contract does not silently assume
    a previous target. For the first prospective evaluation the caller should pass
    100, matching Candidate v1.0's strategic baseline.
    """

    current_target_risk_budget: int
    previous_action_direction: str = "NONE"
    previous_validated_regime: Optional[str] = None
    previous_market_date: Optional[str] = None
    trading_sessions_since_last_reduction: Optional[int] = None
    trading_sessions_since_last_restoration: Optional[int] = None

    def validate(self) -> None:
        if self.current_target_risk_budget not in ALLOWED_RISK_BUDGETS:
            raise ValueError(
                "current_target_risk_budget must be one of "
                f"{sorted(ALLOWED_RISK_BUDGETS)}"
            )

        action = str(self.previous_action_direction).upper()
        if action not in ALLOWED_PREVIOUS_ACTIONS:
            raise ValueError(
                f"previous_action_direction must be one of {sorted(ALLOWED_PREVIOUS_ACTIONS)}"
            )

        if self.previous_validated_regime is not None:
            regime = normalize_regime(self.previous_validated_regime)
            if regime not in {f"R{i}" for i in range(1, 9)}:
                raise ValueError("previous_validated_regime must resolve to R1..R8")

        if self.previous_market_date is not None:
            date.fromisoformat(str(self.previous_market_date))

        for name in (
            "trading_sessions_since_last_reduction",
            "trading_sessions_since_last_restoration",
        ):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, int) or value < 0):
                raise ValueError(f"{name} must be a non-negative integer or null")


@dataclass(frozen=True)
class CostGateContext:
    """Explicit Cost Gate evidence for Step 3.

    PASS/FAIL may be supplied only when expected edge and estimated total cost are
    both known. The frozen Candidate rule is Expected Edge > 2x total cost.
    UNAVAILABLE preserves missing cost/edge information. EMERGENCY_BYPASS is an
    explicit upstream authorization and must include a reason; this contract does
    not invent emergency authority.
    """

    status: str = "UNAVAILABLE"
    expected_edge_bps: Optional[float] = None
    estimated_total_cost_bps: Optional[float] = None
    emergency_reason: Optional[str] = None

    def validate(self) -> None:
        status = str(self.status).upper()
        if status not in ALLOWED_COST_GATE:
            raise ValueError(f"cost_gate.status must be one of {sorted(ALLOWED_COST_GATE)}")

        edge = self.expected_edge_bps
        cost = self.estimated_total_cost_bps
        if edge is not None and not isinstance(edge, (int, float)):
            raise ValueError("expected_edge_bps must be numeric or null")
        if cost is not None and not isinstance(cost, (int, float)):
            raise ValueError("estimated_total_cost_bps must be numeric or null")
        if cost is not None and cost < 0:
            raise ValueError("estimated_total_cost_bps must be >= 0")

        if status in {"PASS", "FAIL"}:
            if edge is None or cost is None:
                raise ValueError("PASS/FAIL Cost Gate requires both edge and total cost")
            passed = float(edge) > 2.0 * float(cost)
            if status == "PASS" and not passed:
                raise ValueError("Cost Gate PASS conflicts with Expected Edge > 2x cost rule")
            if status == "FAIL" and passed:
                raise ValueError("Cost Gate FAIL conflicts with Expected Edge > 2x cost rule")

        if status == "EMERGENCY_BYPASS" and not str(self.emergency_reason or "").strip():
            raise ValueError("EMERGENCY_BYPASS requires emergency_reason")


@dataclass(frozen=True)
class CandidateInput:
    """Normalized, frozen Step-2 input for Candidate v1.0 evaluation."""

    market_date: str
    timestamp: str
    session_checkpoint: str
    data_mode: str
    validation_status: str
    quality: str
    preliminary_regime: str
    validated_regime: str
    transition_state: str
    categories: Mapping[str, CategoryEvidence]
    flags: CandidateFlags
    previous: PreviousOverlayState
    cost_gate: CostGateContext = field(default_factory=CostGateContext)
    candidate_conflict_reasons: Tuple[str, ...] = ()
    source_reason_codes: Tuple[str, ...] = ()

    def validate(self) -> None:
        date.fromisoformat(str(self.market_date))
        if not str(self.timestamp).strip():
            raise ValueError("timestamp is required")
        if not str(self.session_checkpoint).strip():
            raise ValueError("session_checkpoint is required")
        if not str(self.data_mode).strip():
            raise ValueError("data_mode is required")
        if not str(self.validation_status).strip():
            raise ValueError("validation_status is required")

        quality = str(self.quality).upper()
        if quality not in {"FULL", "PARTIAL", "BLOCKED"}:
            raise ValueError("quality must be FULL/PARTIAL/BLOCKED")

        prelim = normalize_regime(self.preliminary_regime)
        validated = normalize_regime(self.validated_regime)
        allowed_regimes = {f"R{i}" for i in range(1, 9)}
        if prelim not in allowed_regimes:
            raise ValueError("preliminary_regime must resolve to R1..R8")
        if validated not in allowed_regimes:
            raise ValueError("validated_regime must resolve to R1..R8")

        if set(self.categories) != set(CATEGORIES):
            missing = sorted(set(CATEGORIES) - set(self.categories))
            extra = sorted(set(self.categories) - set(CATEGORIES))
            raise ValueError(f"categories must be exactly C1-C8; missing={missing}, extra={extra}")

        for name in CATEGORIES:
            obj = self.categories[name]
            if not isinstance(obj, CategoryEvidence):
                raise ValueError(f"{name}: must be CategoryEvidence")
            obj.validate(name)

        if quality == "FULL" and any(self.categories[c].value is None for c in CATEGORIES):
            raise ValueError("FULL Candidate input cannot contain missing C1-C8 values")

        if bool(self.candidate_conflict_reasons) != bool(self.flags.material_conflict):
            raise ValueError(
                "candidate_conflict_reasons and flags.material_conflict must agree; "
                "only unresolved Candidate-level material conflicts belong here"
            )

        self.previous.validate()
        self.cost_gate.validate()
        self._validate_flag_regime_consistency(validated)

    def _validate_flag_regime_consistency(self, regime: str) -> None:
        f = self.flags
        if (f.r8_entry or f.r7_to_r8_transition or f.r8_persistence or f.strong_r8) and regime != "R8":
            raise ValueError("R8 entry/transition/persistence/strong_r8 flags require validated R8")
        if f.r4_r5_persistence and regime not in {"R4", "R5"}:
            raise ValueError("r4_r5_persistence requires validated R4 or R5")

    def to_candidate_state(self) -> CandidateState:
        self.validate()
        return CandidateState(
            validated_regime=self.validated_regime,
            categories=self.categories,
            flags=self.flags,
        )

    def to_dict(self) -> dict:
        self.validate()
        return {
            "market_date": self.market_date,
            "timestamp": self.timestamp,
            "session_checkpoint": self.session_checkpoint,
            "data_mode": self.data_mode,
            "validation_status": self.validation_status,
            "quality": self.quality,
            "preliminary_regime": self.preliminary_regime,
            "validated_regime": self.validated_regime,
            "transition_state": self.transition_state,
            "categories": {c: asdict(self.categories[c]) for c in CATEGORIES},
            "flags": asdict(self.flags),
            "previous": asdict(self.previous),
            "cost_gate": asdict(self.cost_gate),
            "candidate_conflict_reasons": list(self.candidate_conflict_reasons),
            "source_reason_codes": list(self.source_reason_codes),
        }


def _require_mapping(obj: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(obj, Mapping):
        raise ValueError(f"{name} must be an object")
    return obj


def candidate_input_from_dict(payload: Mapping[str, Any]) -> CandidateInput:
    """Parse a JSON-compatible mapping into the frozen Candidate v1.0 contract."""

    payload = _require_mapping(payload, "payload")
    required = {
        "market_date", "timestamp", "session_checkpoint", "data_mode",
        "validation_status", "quality", "preliminary_regime", "validated_regime",
        "transition_state", "categories", "flags", "previous",
    }
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"missing Candidate input fields: {missing}")

    raw_categories = _require_mapping(payload["categories"], "categories")
    categories = {}
    for c in CATEGORIES:
        if c not in raw_categories:
            raise ValueError(f"categories missing {c}")
        raw = _require_mapping(raw_categories[c], c)
        categories[c] = CategoryEvidence(
            status=raw.get("status", ""),
            value=raw.get("value"),
            trend=raw.get("trend", "UNKNOWN"),
            polarity=raw.get("polarity", "UNKNOWN"),
            strength=raw.get("strength", "UNKNOWN"),
        )

    raw_flags = _require_mapping(payload["flags"], "flags")
    flags = CandidateFlags(**{k: bool(raw_flags.get(k, False)) for k in CandidateFlags.__dataclass_fields__})

    raw_prev = _require_mapping(payload["previous"], "previous")
    if "current_target_risk_budget" not in raw_prev:
        raise ValueError("previous.current_target_risk_budget is required")
    previous = PreviousOverlayState(
        current_target_risk_budget=int(raw_prev["current_target_risk_budget"]),
        previous_action_direction=raw_prev.get("previous_action_direction", "NONE"),
        previous_validated_regime=raw_prev.get("previous_validated_regime"),
        previous_market_date=raw_prev.get("previous_market_date"),
        trading_sessions_since_last_reduction=raw_prev.get("trading_sessions_since_last_reduction"),
        trading_sessions_since_last_restoration=raw_prev.get("trading_sessions_since_last_restoration"),
    )

    raw_cost = _require_mapping(payload.get("cost_gate", {}), "cost_gate")
    cost_gate = CostGateContext(
        status=raw_cost.get("status", "UNAVAILABLE"),
        expected_edge_bps=raw_cost.get("expected_edge_bps"),
        estimated_total_cost_bps=raw_cost.get("estimated_total_cost_bps"),
        emergency_reason=raw_cost.get("emergency_reason"),
    )

    obj = CandidateInput(
        market_date=str(payload["market_date"]),
        timestamp=str(payload["timestamp"]),
        session_checkpoint=str(payload["session_checkpoint"]),
        data_mode=str(payload["data_mode"]),
        validation_status=str(payload["validation_status"]),
        quality=str(payload["quality"]),
        preliminary_regime=str(payload["preliminary_regime"]),
        validated_regime=str(payload["validated_regime"]),
        transition_state=str(payload["transition_state"]),
        categories=categories,
        flags=flags,
        previous=previous,
        cost_gate=cost_gate,
        candidate_conflict_reasons=tuple(payload.get("candidate_conflict_reasons", [])),
        source_reason_codes=tuple(payload.get("source_reason_codes", [])),
    )
    obj.validate()
    return obj
