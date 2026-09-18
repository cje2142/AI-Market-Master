"""AI Market Master 3.2 — Data Efficiency Dashboard Auto-Log Bridge v0.1.

Non-authoritative research sidecar.

The canonical input schema is defined by DASHBOARD_RULE section 20A.
A defensive legacy-normalization layer is retained so historical sidecars do not
break runtime ingestion. New Dashboard executions must emit canonical schema.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import data_efficiency_dashboard_input_adapter_v0_1 as de_adapter
import data_efficiency_runtime_comparator_v0_3 as comparator


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be an object")
    return value


def _sample_id(snapshot: Mapping[str, Any]) -> str:
    explicit = snapshot.get("sample_id")
    if explicit:
        return str(explicit)

    identity = {
        "market_date": snapshot.get("market_date"),
        "timestamp": snapshot.get("timestamp"),
        "session_checkpoint": snapshot.get("session_checkpoint"),
    }
    canonical = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
    day = re.sub(r"[^0-9]", "", str(snapshot.get("market_date", ""))) or "unknown"
    checkpoint = re.sub(
        r"[^A-Za-z0-9_-]+",
        "-",
        str(snapshot.get("session_checkpoint", "session")),
    ).strip("-") or "session"
    return f"AMM32-DE-{day}-{checkpoint}-{digest}"


def _legacy_pct(raw: Mapping[str, Any], key: str) -> float | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"legacy raw {key} must be numeric or null")
    return float(value) / 100.0


def _legacy_regime(regime: Any) -> str:
    if isinstance(regime, str):
        return regime
    if isinstance(regime, Mapping):
        primary = regime.get("primary")
        transition = regime.get("transition")
        parts = [str(x) for x in (primary, transition) if x not in (None, "")]
        if parts:
            return "; ".join(parts)
    raise ValueError("legacy regime cannot be normalized")


def normalize_autolog_snapshot(snapshot: Mapping[str, Any]) -> dict:
    """Return canonical 20A schema while preserving Official values.

    Canonical schema is passed through. Historical aliases are converted only for
    ingestion compatibility. Correction payloads are not prospective samples.
    """
    snapshot = _mapping(snapshot, "snapshot")
    if "correction_of" in snapshot:
        raise ValueError("non-sample correction payload")

    official_src = _mapping(snapshot.get("official"), "official")
    canonical_ready = (
        "SAI" in official_src
        and "official_regime" in snapshot
        and "de_raw" in snapshot
    )
    if canonical_ready:
        out = deepcopy(dict(snapshot))
        out.setdefault("sample_id", _sample_id(out))
        return out

    official = deepcopy(dict(official_src))
    legacy_sai = official.pop("strategy_action_index", None)
    if "SAI" not in official:
        if isinstance(legacy_sai, Mapping):
            official["SAI"] = legacy_sai.get("value")
        elif legacy_sai is not None:
            official["SAI"] = legacy_sai

    regime = snapshot.get("official_regime")
    if regime is None:
        regime = official.pop("regime", None)
    official_regime = _legacy_regime(regime)

    raw_src = snapshot.get("de_raw")
    if raw_src is None:
        raw_src = _mapping(snapshot.get("candidate_raw_inputs", {}), "candidate_raw_inputs")
        de_raw = {
            "r_kospi": _legacy_pct(raw_src, "KOSPI_return_pct"),
            "r_kosdaq": _legacy_pct(raw_src, "KOSDAQ_return_pct"),
            "r_kospi200": _legacy_pct(raw_src, "KOSPI200_return_pct"),
            "r_krx100": _legacy_pct(raw_src, "KRX100_return_pct"),
            "r_usdkrw": _legacy_pct(raw_src, "USDKRW_return_pct"),
            "d_ktb3y_bp": raw_src.get("KTB3Y_change_bp"),
        }
    else:
        de_raw = deepcopy(dict(_mapping(raw_src, "de_raw")))

    out = {
        "sample_id": snapshot.get("sample_id"),
        "market_date": snapshot.get("market_date"),
        "timestamp": snapshot.get("timestamp"),
        "session_checkpoint": snapshot.get("session_checkpoint"),
        "official": official,
        "official_regime": official_regime,
        "de_raw": de_raw,
        "C8_effect": snapshot.get("C8_effect"),
        "missing_data_effect": snapshot.get("missing_data_effect"),
        "notes": list(snapshot.get("notes", [])) + [
            "LEGACY_SCHEMA_NORMALIZED_BY_DE_BRIDGE"
        ],
    }
    out["sample_id"] = out.get("sample_id") or _sample_id(out)
    return out


def validate_autolog_snapshot(snapshot: Mapping[str, Any]) -> dict:
    snapshot = normalize_autolog_snapshot(snapshot)
    required = {
        "sample_id",
        "market_date",
        "timestamp",
        "session_checkpoint",
        "official",
        "official_regime",
        "de_raw",
    }
    missing = sorted(k for k in required if snapshot.get(k) in (None, ""))
    if missing:
        raise ValueError(f"missing auto-log fields: {missing}")

    official = _mapping(snapshot["official"], "official")
    for name in [f"C{i}" for i in range(1, 9)]:
        if name not in official:
            raise ValueError(f"official missing {name}")
    if "SAI" not in official:
        raise ValueError("official missing SAI")

    raw = _mapping(snapshot["de_raw"], "de_raw")
    allowed_raw = {
        "r_kospi", "r_kosdaq", "r_kospi200", "r_krx100",
        "r_usdkrw", "d_ktb3y_bp",
    }
    unknown = sorted(set(raw) - allowed_raw)
    if unknown:
        raise ValueError(f"unknown de_raw fields: {unknown}")
    return snapshot


def build_comparator_snapshot(snapshot: Mapping[str, Any]) -> dict:
    snapshot = validate_autolog_snapshot(snapshot)
    official = snapshot["official"]

    base_dashboard = {
        "C1": official["C1"],
        "C2": official["C2"],
        "C3": official["C3"],
        "C5": official["C5"],
        "C7": official["C7"],
    }
    de = de_adapter.build_candidate_snapshot(base_dashboard, snapshot["de_raw"])

    candidate_regime = snapshot.get("candidate_regime")
    if candidate_regime is None:
        candidate_regime = snapshot["official_regime"]

    return {
        "sample_id": _sample_id(snapshot),
        "market_date": snapshot["market_date"],
        "timestamp": snapshot["timestamp"],
        "session_checkpoint": snapshot["session_checkpoint"],
        "official": official,
        "candidate": de["candidate"],
        "official_regime": snapshot["official_regime"],
        "candidate_regime": candidate_regime,
        "C8_effect": snapshot.get("C8_effect"),
        "missing_data_effect": snapshot.get("missing_data_effect"),
        "notes": list(snapshot.get("notes", [])) + [
            f"DE auto-log candidate status: {de['candidate_status']}",
            f"DE auto-log candidate coverage: {de['candidate_coverage']:.6f}",
            "Data Efficiency Candidate v0.1 is research-only; Official 3.2 remains authority.",
        ],
    }


def append_autolog_snapshot(snapshot: Mapping[str, Any], log_path: str | Path):
    comparator_snapshot = build_comparator_snapshot(snapshot)
    event = comparator.append_comparison(log_path, comparator_snapshot)
    return event, comparator_snapshot


def process_json_file(input_path: str | Path, log_path: str | Path):
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as f:
        snapshot = json.load(f)
    return append_autolog_snapshot(snapshot, log_path)
