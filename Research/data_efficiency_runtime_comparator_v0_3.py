"""AI Market Master 3.2 — Runtime Comparator v0.3.

Purpose:
- compare Official 3.2 and Data Efficiency Candidate v0.1 on the SAME observation;
- preserve an append-only JSONL research journal;
- never modify Official 3.2 authority or Candidate v0.1 freeze;
- keep outcomes PENDING until matured.

This module compares already-computed component/SAI outputs. It does not reimplement
official scoring formulas and therefore cannot silently drift from the authority files.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

OFFICIAL_COMPONENTS = tuple(f"C{i}" for i in range(1, 9))
CANDIDATE_COMPONENTS = tuple(f"C{i}" for i in range(1, 8))
HORIZONS = ("1d", "5d", "20d")
VALID_STATUS = {"VERIFIED", "PARTIAL", "DATA UNAVAILABLE", "UNAVAILABLE", "BLOCKED"}
MATERIAL_SAI_DELTA = 0.15


def _read_events(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    out: list[dict] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _append_event(path: str | Path, event: Mapping[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def _is_num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _component(obj: Any, name: str) -> dict:
    if not isinstance(obj, Mapping):
        raise ValueError(f"{name} must be an object")
    if "status" not in obj or "value" not in obj:
        raise ValueError(f"{name} requires status and value")
    status = str(obj["status"]).strip().upper()
    value = obj["value"]
    if value is not None and not _is_num(value):
        raise ValueError(f"{name}.value must be numeric or null")
    if value is not None and not -1.0000001 <= float(value) <= 1.0000001:
        raise ValueError(f"{name}.value outside [-1,+1]")
    if value is None and status in {"VERIFIED", "VALID", "OK"}:
        raise ValueError(f"{name}: missing value cannot be VERIFIED")
    return {"status": status, "value": None if value is None else float(value)}


def _direction(value: Any) -> str:
    if value is None:
        return "UNAVAILABLE"
    value = float(value)
    if value > 0:
        return "POSITIVE"
    if value < 0:
        return "NEGATIVE"
    return "NEUTRAL"


def _same_sign(a: Any, b: Any) -> bool | None:
    da, db = _direction(a), _direction(b)
    if "UNAVAILABLE" in {da, db}:
        return None
    return da == db


def _action_band(value: Any) -> str:
    """Official 3.2 Action Bands from SCORING_RULE section 28."""
    if value is None:
        return "DATA UNAVAILABLE"
    value = float(value)
    if value >= 0.60:
        return "STRONG POSITIVE"
    if value >= 0.30:
        return "POSITIVE"
    if value > -0.30:
        return "BALANCED"
    if value > -0.60:
        return "NEGATIVE"
    return "STRONG NEGATIVE"


def _coverage(components: Mapping[str, dict], weights: Mapping[str, float]) -> float:
    covered = 0.0
    for name, weight in weights.items():
        if components[name]["value"] is not None:
            covered += weight
    return covered


OFFICIAL_WEIGHTS = {
    "C1": 0.18, "C2": 0.12, "C3": 0.15, "C4": 0.10,
    "C5": 0.20, "C6": 0.10, "C7": 0.08, "C8": 0.07,
}
_candidate_den = sum(OFFICIAL_WEIGHTS[f"C{i}"] for i in range(1, 8))
CANDIDATE_WEIGHTS = {
    f"C{i}": OFFICIAL_WEIGHTS[f"C{i}"] / _candidate_den for i in range(1, 8)
}


def validate_snapshot(snapshot: Mapping[str, Any]) -> dict:
    if not isinstance(snapshot, Mapping):
        raise ValueError("snapshot must be an object")

    required = {
        "sample_id", "market_date", "timestamp", "session_checkpoint",
        "official", "candidate", "official_regime", "candidate_regime",
    }
    missing = sorted(required - set(snapshot))
    if missing:
        raise ValueError(f"missing comparator fields: {missing}")

    official = snapshot["official"]
    candidate = snapshot["candidate"]
    if not isinstance(official, Mapping) or not isinstance(candidate, Mapping):
        raise ValueError("official/candidate must be objects")

    off_components: dict[str, dict] = {}
    de_components: dict[str, dict] = {}

    for name in OFFICIAL_COMPONENTS:
        if name not in official:
            raise ValueError(f"official missing {name}")
        off_components[name] = _component(official[name], f"official.{name}")
    for name in CANDIDATE_COMPONENTS:
        if name not in candidate:
            raise ValueError(f"candidate missing {name}")
        de_components[name] = _component(candidate[name], f"candidate.{name}")

    for model_name, model in (("official", official), ("candidate", candidate)):
        key = "SAI" if model_name == "official" else "SAI_DE"
        if key not in model:
            raise ValueError(f"{model_name} missing {key}")
        if model[key] is not None and not _is_num(model[key]):
            raise ValueError(f"{model_name}.{key} must be numeric or null")

    return {
        "official_components": off_components,
        "candidate_components": de_components,
        "official_sai": None if official["SAI"] is None else float(official["SAI"]),
        "candidate_sai": None if candidate["SAI_DE"] is None else float(candidate["SAI_DE"]),
    }


def build_comparison(snapshot: Mapping[str, Any]) -> dict:
    parsed = validate_snapshot(snapshot)
    off = parsed["official_components"]
    de = parsed["candidate_components"]
    off_sai = parsed["official_sai"]
    de_sai = parsed["candidate_sai"]

    sai_delta = None if off_sai is None or de_sai is None else de_sai - off_sai
    c4_delta = None if off["C4"]["value"] is None or de["C4"]["value"] is None else (
        de["C4"]["value"] - off["C4"]["value"]
    )
    c6_delta = None if off["C6"]["value"] is None or de["C6"]["value"] is None else (
        de["C6"]["value"] - off["C6"]["value"]
    )

    c8_value = off["C8"]["value"]
    c8_nominal_weighted = None if c8_value is None else OFFICIAL_WEIGHTS["C8"] * c8_value

    official_coverage = _coverage(off, OFFICIAL_WEIGHTS)
    candidate_coverage = _coverage(de, CANDIDATE_WEIGHTS)

    explicit_missing_effect = snapshot.get("missing_data_effect")
    if explicit_missing_effect is not None and not _is_num(explicit_missing_effect):
        raise ValueError("missing_data_effect must be numeric or null")

    result = {
        "sample_id": str(snapshot["sample_id"]),
        "market_date": str(snapshot["market_date"]),
        "timestamp": str(snapshot["timestamp"]),
        "session_checkpoint": str(snapshot["session_checkpoint"]),
        "official": {
            **{k: deepcopy(off[k]) for k in OFFICIAL_COMPONENTS},
            "SAI": off_sai,
        },
        "candidate_de_v01": {
            **{k: deepcopy(de[k]) for k in CANDIDATE_COMPONENTS},
            "SAI_DE": de_sai,
        },
        "comparison": {
            "SAI_delta_candidate_minus_official": sai_delta,
            "direction_agreement": _same_sign(off_sai, de_sai),
            "official_direction": _direction(off_sai),
            "candidate_direction": _direction(de_sai),
            "official_action_band": _action_band(off_sai),
            "candidate_action_band": _action_band(de_sai),
            "action_band_agreement": _action_band(off_sai) == _action_band(de_sai),
            "material_sai_divergence": (
                None if sai_delta is None else abs(sai_delta) >= MATERIAL_SAI_DELTA
            ),
            "C4_delta_candidate_minus_official": c4_delta,
            "C4_direction_flip": _same_sign(off["C4"]["value"], de["C4"]["value"]) is False,
            "C6_delta_candidate_minus_official": c6_delta,
            "C6_direction_flip": _same_sign(off["C6"]["value"], de["C6"]["value"]) is False,
            "C8_official_value": c8_value,
            "C8_nominal_weighted_contribution": c8_nominal_weighted,
            "C8_effect": snapshot.get("C8_effect"),
            "missing_data_effect": explicit_missing_effect,
            "official_data_coverage": official_coverage,
            "candidate_data_coverage": candidate_coverage,
            "regime_agreement": str(snapshot["official_regime"]) == str(snapshot["candidate_regime"]),
            "official_regime": str(snapshot["official_regime"]),
            "candidate_regime": str(snapshot["candidate_regime"]),
        },
        "outcome": {
            "1d": "PENDING",
            "5d": "PENDING",
            "20d": "PENDING",
        },
        "notes": deepcopy(snapshot.get("notes", [])),
    }
    return result


def append_comparison(log_path: str | Path, snapshot: Mapping[str, Any]) -> dict:
    payload = build_comparison(snapshot)
    events = _read_events(log_path)
    sid = payload["sample_id"]
    if any(e.get("record_type") == "COMPARISON" and e.get("sample_id") == sid for e in events):
        raise ValueError("duplicate comparator sample_id")

    event = {
        "record_type": "COMPARISON",
        "sample_id": sid,
        "revision": 0,
        "payload": payload,
    }
    _append_event(log_path, event)
    return event


def append_correction(
    log_path: str | Path,
    sample_id: str,
    corrected_payload_fields: Mapping[str, Any],
    reason: str,
) -> dict:
    """Append a documented correction without rewriting the original comparison."""
    if not reason or not str(reason).strip():
        raise ValueError("correction reason required")
    events = _read_events(log_path)
    if not any(e.get("record_type") == "COMPARISON" and e.get("sample_id") == sample_id for e in events):
        raise ValueError("unknown comparator sample_id")
    revision = 1 + sum(
        1 for e in events
        if e.get("record_type") == "CORRECTION" and e.get("sample_id") == sample_id
    )
    event = {
        "record_type": "CORRECTION",
        "sample_id": sample_id,
        "revision": revision,
        "reason": str(reason),
        "payload": deepcopy(dict(corrected_payload_fields)),
    }
    _append_event(log_path, event)
    return event


def append_outcome(
    log_path: str | Path,
    sample_id: str,
    horizon: str,
    metrics: Mapping[str, Any],
) -> dict:
    if horizon not in HORIZONS:
        raise ValueError("horizon must be 1d/5d/20d")
    events = _read_events(log_path)
    if not any(e.get("record_type") == "COMPARISON" and e.get("sample_id") == sample_id for e in events):
        raise ValueError("unknown comparator sample_id")
    if any(
        e.get("record_type") == "OUTCOME"
        and e.get("sample_id") == sample_id
        and e.get("horizon") == horizon
        for e in events
    ):
        raise ValueError("outcome already recorded")

    allowed = {
        "1d": {"ret_1d", "risk_warning_useful_1d", "false_warning_1d"},
        "5d": {"ret_5d", "mae_5d", "mfe_5d", "risk_warning_useful_5d", "false_warning_5d"},
        "20d": {
            "ret_20d", "mae_20d", "mfe_20d",
            "risk_warning_useful_20d", "false_warning_20d", "recovery_delay_20d",
        },
    }[horizon]
    extra = set(metrics) - allowed
    if extra:
        raise ValueError(f"invalid outcome fields for {horizon}: {sorted(extra)}")

    event = {
        "record_type": "OUTCOME",
        "sample_id": sample_id,
        "horizon": horizon,
        "payload": deepcopy(dict(metrics)),
    }
    _append_event(log_path, event)
    return event


def build_projection(log_path: str | Path) -> list[dict]:
    events = _read_events(log_path)
    rows: dict[str, dict] = {}
    for event in events:
        sid = event.get("sample_id")
        typ = event.get("record_type")
        if typ == "COMPARISON":
            if sid in rows:
                raise ValueError("duplicate COMPARISON event in journal")
            rows[sid] = deepcopy(event["payload"])
        elif typ == "CORRECTION":
            if sid not in rows:
                raise ValueError("correction before comparison")
            for key, value in event["payload"].items():
                rows[sid][key] = deepcopy(value)
            rows[sid]["last_revision"] = event.get("revision")
            rows[sid]["last_correction_reason"] = event.get("reason")
        elif typ == "OUTCOME":
            if sid not in rows:
                raise ValueError("outcome before comparison")
            horizon = event["horizon"]
            rows[sid]["outcome"][horizon] = {
                "status": "MATURE",
                **deepcopy(event["payload"]),
            }
    return [rows[k] for k in sorted(rows)]


def initialize_store(log_path: str | Path) -> Path:
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("", encoding="utf-8")
    return p
