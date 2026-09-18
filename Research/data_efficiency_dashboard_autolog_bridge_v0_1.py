"""AI Market Master 3.2 — Data Efficiency Dashboard Auto-Log Bridge v0.1.

Non-authoritative research sidecar.

Input:
- one normalized Official Dashboard snapshot
- optional Candidate-specific raw fields

Output:
- append-only Data Efficiency comparison journal entry

This bridge never changes Official 3.2 calculations, Regime, Dashboard layout, or portfolio action.
"""

from __future__ import annotations

import hashlib
import json
import re
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


def validate_autolog_snapshot(snapshot: Mapping[str, Any]) -> None:
    snapshot = _mapping(snapshot, "snapshot")
    required = {
        "market_date",
        "timestamp",
        "session_checkpoint",
        "official",
        "official_regime",
        "de_raw",
    }
    missing = sorted(required - set(snapshot))
    if missing:
        raise ValueError(f"missing auto-log fields: {missing}")

    official = _mapping(snapshot["official"], "official")
    for name in [f"C{i}" for i in range(1, 9)]:
        if name not in official:
            raise ValueError(f"official missing {name}")
    if "SAI" not in official:
        raise ValueError("official missing SAI")

    _mapping(snapshot["de_raw"], "de_raw")


def build_comparator_snapshot(snapshot: Mapping[str, Any]) -> dict:
    validate_autolog_snapshot(snapshot)
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
        # Candidate does not own a separate Regime Engine.
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
