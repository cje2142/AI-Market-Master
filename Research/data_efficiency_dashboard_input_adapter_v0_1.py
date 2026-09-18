"""AI Market Master 3.2 — Data Efficiency Dashboard Input Adapter v0.1.

Research-only adapter for Data Efficiency Candidate v0.1.

Purpose:
- add the minimal Candidate-specific raw inputs that the normal Dashboard may omit;
- compute Candidate C4 and C6 deterministically;
- combine Candidate C1/C2/C3/C4/C5/C6/C7 into SAI_DE;
- preserve Official 3.2 output unchanged.

This module does not modify official Dashboard or scoring authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

OFFICIAL_BASE_WEIGHTS = {
    "C1": 0.18,
    "C2": 0.12,
    "C3": 0.15,
    "C4": 0.10,
    "C5": 0.20,
    "C6": 0.10,
    "C7": 0.08,
}
_DEN = sum(OFFICIAL_BASE_WEIGHTS.values())  # 0.93
DE_WEIGHTS = {k: v / _DEN for k, v in OFFICIAL_BASE_WEIGHTS.items()}

REQUIRED_BASE = ("C1", "C2", "C3", "C5", "C7")
REQUIRED_RAW = (
    "r_kospi",
    "r_kosdaq",
    "r_kospi200",
    "r_krx100",
    "r_usdkrw",
    "d_ktb3y_bp",
)


def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _clip(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(v)))


def _component(obj: Any, name: str) -> dict:
    if not isinstance(obj, Mapping):
        raise ValueError(f"{name} must be object")
    if "status" not in obj or "value" not in obj:
        raise ValueError(f"{name} requires status and value")
    status = str(obj["status"]).strip().upper()
    value = obj["value"]
    if value is not None and not _is_num(value):
        raise ValueError(f"{name}.value must be numeric or null")
    if value is None and status in {"VERIFIED", "VALID", "OK"}:
        raise ValueError(f"{name}: missing value cannot be VERIFIED")
    if value is not None and not -1.0000001 <= float(value) <= 1.0000001:
        raise ValueError(f"{name}.value outside [-1,+1]")
    return {"status": status, "value": None if value is None else float(value)}


def _raw_number(raw: Mapping[str, Any], key: str) -> float | None:
    value = raw.get(key)
    if value is None:
        return None
    if not _is_num(value):
        raise ValueError(f"raw.{key} must be numeric or null")
    return float(value)


def compute_c4(raw: Mapping[str, Any]) -> dict:
    """Candidate C4.

    VERIFIED:
      KOSPI + KOSDAQ + KOSPI200 + KRX100.
    PARTIAL:
      KOSPI + KOSDAQ + exactly one large-cap candidate.
    Otherwise unavailable.
    Returns are decimal returns, e.g. +2.36% -> 0.0236.
    """
    r_k = _raw_number(raw, "r_kospi")
    r_q = _raw_number(raw, "r_kosdaq")
    r_200 = _raw_number(raw, "r_kospi200")
    r_100 = _raw_number(raw, "r_krx100")

    if r_k is None or r_q is None:
        return {
            "status": "DATA UNAVAILABLE",
            "value": None,
            "details": {"reason": "KOSPI_AND_KOSDAQ_REQUIRED"},
        }

    large = [x for x in (r_200, r_100) if x is not None]
    if not large:
        return {
            "status": "DATA UNAVAILABLE",
            "value": None,
            "details": {"reason": "LARGE_CAP_AXIS_UNAVAILABLE"},
        }

    lc_raw = sum(large) / len(large) - r_k
    gr_raw = r_q - r_k
    n_lc = _clip(lc_raw / 0.005)
    n_gr = _clip(gr_raw / 0.015)
    value = 0.40 * n_lc + 0.60 * n_gr

    return {
        "status": "VERIFIED" if len(large) == 2 else "PARTIAL",
        "value": value,
        "details": {
            "LC_RAW": lc_raw,
            "GR_RAW": gr_raw,
            "N_LC": n_lc,
            "N_GR": n_gr,
            "large_cap_members": len(large),
        },
    }


def compute_c6(raw: Mapping[str, Any]) -> dict:
    """Candidate C6.

    VERIFIED: USD/KRW return + KTB3Y bp change.
    PARTIAL: exactly one axis.
    Returns use decimal return for FX; KTB change is basis points.
    """
    r_fx = _raw_number(raw, "r_usdkrw")
    d_ktb = _raw_number(raw, "d_ktb3y_bp")

    fx = None if r_fx is None else -_clip(r_fx / 0.008)
    ktb = None if d_ktb is None else -_clip(d_ktb / 10.0)

    valid = [x for x in (fx, ktb) if x is not None]
    if not valid:
        return {
            "status": "DATA UNAVAILABLE",
            "value": None,
            "details": {"FX": fx, "KTB": ktb},
        }
    if len(valid) == 1:
        return {
            "status": "PARTIAL",
            "value": valid[0],
            "details": {"FX": fx, "KTB": ktb},
        }
    return {
        "status": "VERIFIED",
        "value": 0.50 * fx + 0.50 * ktb,
        "details": {"FX": fx, "KTB": ktb},
    }


def _usable(obj: Mapping[str, Any]) -> bool:
    return obj.get("value") is not None and str(obj.get("status", "")).upper() in {
        "VERIFIED", "PARTIAL", "VALID", "OK"
    }


def candidate_global(components: Mapping[str, Mapping[str, Any]]) -> dict:
    parsed = {f"C{i}": _component(components[f"C{i}"], f"C{i}") for i in range(1, 8)}
    usable = {k: v for k, v in parsed.items() if _usable(v)}
    coverage = sum(DE_WEIGHTS[k] for k in usable)

    all_verified = all(parsed[f"C{i}"]["status"] == "VERIFIED" for i in range(1, 8))
    if all_verified:
        sai = sum(DE_WEIGHTS[k] * parsed[k]["value"] for k in DE_WEIGHTS)
        return {
            "status": "VERIFIED",
            "value": sai,
            "coverage": 1.0,
            "usable_components": sorted(usable),
        }

    gate = (
        _usable(parsed["C5"])
        and (_usable(parsed["C1"]) or _usable(parsed["C2"]))
        and (_usable(parsed["C3"]) or _usable(parsed["C4"]))
        and (_usable(parsed["C6"]) or _usable(parsed["C7"]))
        and len(usable) >= 5
        and coverage >= 0.70
    )
    if not gate:
        return {
            "status": "DATA UNAVAILABLE",
            "value": None,
            "coverage": coverage,
            "usable_components": sorted(usable),
        }

    numerator = sum(DE_WEIGHTS[k] * usable[k]["value"] for k in usable)
    sai = numerator / coverage
    return {
        "status": "PARTIAL",
        "value": sai,
        "coverage": coverage,
        "usable_components": sorted(usable),
    }


def build_candidate_snapshot(base_dashboard: Mapping[str, Any], de_raw: Mapping[str, Any]) -> dict:
    """Build DE Candidate numeric snapshot from Official Dashboard components + DE raw fields.

    Required Official-derived base components:
      C1, C2, C3, C5, C7

    Candidate-specific raw fields:
      r_kospi, r_kosdaq, r_kospi200, r_krx100, r_usdkrw, d_ktb3y_bp

    The three newly required collection fields for a FULL Candidate C4/C6 are:
      r_kospi200, r_krx100, d_ktb3y_bp

    r_kospi, r_kosdaq and r_usdkrw are normally already present in the Dashboard data.
    """
    if not isinstance(base_dashboard, Mapping):
        raise ValueError("base_dashboard must be object")
    if not isinstance(de_raw, Mapping):
        raise ValueError("de_raw must be object")

    missing = [k for k in REQUIRED_BASE if k not in base_dashboard]
    if missing:
        raise ValueError(f"base_dashboard missing {missing}")

    components = {
        "C1": _component(base_dashboard["C1"], "base_dashboard.C1"),
        "C2": _component(base_dashboard["C2"], "base_dashboard.C2"),
        "C3": _component(base_dashboard["C3"], "base_dashboard.C3"),
        "C4": compute_c4(de_raw),
        "C5": _component(base_dashboard["C5"], "base_dashboard.C5"),
        "C6": compute_c6(de_raw),
        "C7": _component(base_dashboard["C7"], "base_dashboard.C7"),
    }
    global_result = candidate_global(components)

    return {
        "candidate": {**deepcopy(components), "SAI_DE": global_result["value"]},
        "candidate_status": global_result["status"],
        "candidate_coverage": global_result["coverage"],
        "usable_components": global_result["usable_components"],
        "raw_input_status": {
            key: ("AVAILABLE" if de_raw.get(key) is not None else "MISSING")
            for key in REQUIRED_RAW
        },
    }
