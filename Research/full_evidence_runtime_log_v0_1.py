import csv
import json
from copy import deepcopy
from pathlib import Path

CATEGORIES = [f"C{i}" for i in range(1, 9)]
HORIZONS = {"1d", "5d", "20d"}

SIGNAL_REQUIRED = [
    "sample_id", "market_date", "timestamp", "session_checkpoint",
    "data_mode", "validation_status", "quality",
    *CATEGORIES,
    "preliminary_regime", "validated_regime", "transition_state",
    "material_conflicts", "evidence_gate_result", "gate_reached",
    "target_risk_budget", "action_direction", "allowed_step_size",
    "reason_codes", "core_before", "tactical_before", "leverage_before",
    "exact_risk_multipliers", "leverage_restore_authority",
    "core_reduction_authority", "core_after", "tactical_after",
    "leverage_after", "mapper_status", "action_hierarchy",
    "unresolved_constraints",
]

PROJECTION_FIELDS = SIGNAL_REQUIRED + [
    "ret_1d", "ret_5d", "ret_20d",
    "mae_5d", "mfe_5d", "mae_20d", "mfe_20d",
    "outcome_status_1d", "outcome_status_5d", "outcome_status_20d",
    "last_revision", "correction_count",
]


def _read_events(path):
    path = Path(path)
    if not path.exists():
        return []
    events = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def _append_event(path, event):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def _validate_category(name, obj):
    if not isinstance(obj, dict):
        raise ValueError(f"{name} must be an object with status/value")
    if "status" not in obj or "value" not in obj:
        raise ValueError(f"{name} requires status and value")
    status = str(obj["status"]).strip().upper()
    if obj["value"] is None and status in {"OK", "VERIFIED", "VALID"}:
        raise ValueError(f"{name}: missing value cannot be marked valid")
    if obj["value"] is None and status in {"NEUTRAL", "ZERO"}:
        raise ValueError(f"{name}: missing != neutral")


def validate_signal(sample):
    missing = [k for k in SIGNAL_REQUIRED if k not in sample]
    if missing:
        raise ValueError(f"missing signal fields: {missing}")
    for c in CATEGORIES:
        _validate_category(c, sample[c])
    if sample["quality"] not in {"FULL", "PARTIAL", "BLOCKED"}:
        raise ValueError("quality must be FULL/PARTIAL/BLOCKED")
    if sample["mapper_status"] not in {
        "EXECUTABLE", "PARTIAL EXECUTION / CORE PROTECTED",
        "LEVERAGE RESTORE BLOCKED", "HOLD / CONFLICT", "DATA PARTIAL",
        "NOT MAPPED"
    }:
        raise ValueError("invalid mapper_status")
    if sample["action_direction"] not in {"HOLD", "REDUCE", "RESTORE", "BLOCKED"}:
        raise ValueError("invalid action_direction")
    return True


def append_signal(log_path, sample):
    validate_signal(sample)
    events = _read_events(log_path)
    if any(e.get("record_type") == "SIGNAL" and e.get("sample_id") == sample["sample_id"] for e in events):
        raise ValueError("duplicate sample_id")
    event = {
        "record_type": "SIGNAL",
        "sample_id": sample["sample_id"],
        "revision": 0,
        "payload": deepcopy(sample),
    }
    _append_event(log_path, event)
    return event


def append_outcome(log_path, sample_id, horizon, metrics):
    if horizon not in HORIZONS:
        raise ValueError("horizon must be 1d/5d/20d")
    events = _read_events(log_path)
    if not any(e.get("record_type") == "SIGNAL" and e.get("sample_id") == sample_id for e in events):
        raise ValueError("unknown sample_id")
    if any(e.get("record_type") == "OUTCOME" and e.get("sample_id") == sample_id and e.get("horizon") == horizon for e in events):
        raise ValueError("outcome already recorded; use a documented correction")

    allowed = {
        "1d": {"ret_1d"},
        "5d": {"ret_5d", "mae_5d", "mfe_5d"},
        "20d": {"ret_20d", "mae_20d", "mfe_20d"},
    }[horizon]
    extra = set(metrics) - allowed
    if extra:
        raise ValueError(f"invalid outcome fields for {horizon}: {sorted(extra)}")

    event = {
        "record_type": "OUTCOME",
        "sample_id": sample_id,
        "horizon": horizon,
        "payload": deepcopy(metrics),
    }
    _append_event(log_path, event)
    return event


def append_correction(log_path, sample_id, corrected_fields, reason):
    if not reason or not str(reason).strip():
        raise ValueError("correction reason required")
    events = _read_events(log_path)
    signal = next((e for e in events if e.get("record_type") == "SIGNAL" and e.get("sample_id") == sample_id), None)
    if signal is None:
        raise ValueError("unknown sample_id")
    invalid = set(corrected_fields) - set(SIGNAL_REQUIRED)
    if invalid:
        raise ValueError(f"correction can only alter signal-time fields: {sorted(invalid)}")
    revision = 1 + sum(1 for e in events if e.get("record_type") == "CORRECTION" and e.get("sample_id") == sample_id)
    event = {
        "record_type": "CORRECTION",
        "sample_id": sample_id,
        "revision": revision,
        "reason": str(reason),
        "payload": deepcopy(corrected_fields),
    }
    _append_event(log_path, event)
    return event


def build_projection(log_path):
    events = _read_events(log_path)
    rows = {}
    for e in events:
        sid = e.get("sample_id")
        typ = e.get("record_type")
        if typ == "SIGNAL":
            row = deepcopy(e["payload"])
            row.update({
                "ret_1d": None, "ret_5d": None, "ret_20d": None,
                "mae_5d": None, "mfe_5d": None, "mae_20d": None, "mfe_20d": None,
                "outcome_status_1d": "PENDING", "outcome_status_5d": "PENDING", "outcome_status_20d": "PENDING",
                "last_revision": 0, "correction_count": 0,
            })
            rows[sid] = row
        elif typ == "CORRECTION":
            if sid not in rows:
                raise ValueError("correction before signal")
            for k, v in e["payload"].items():
                rows[sid][k] = deepcopy(v)
            rows[sid]["last_revision"] = e["revision"]
            rows[sid]["correction_count"] += 1
        elif typ == "OUTCOME":
            if sid not in rows:
                raise ValueError("outcome before signal")
            for k, v in e["payload"].items():
                rows[sid][k] = v
            rows[sid][f"outcome_status_{e['horizon']}"] = "MATURE"
    return [rows[k] for k in sorted(rows)]


def write_projection_csv(log_path, csv_path):
    rows = build_projection(log_path)
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PROJECTION_FIELDS, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            out = {}
            for k in PROJECTION_FIELDS:
                v = row.get(k)
                if isinstance(v, (dict, list)):
                    out[k] = json.dumps(v, ensure_ascii=False, sort_keys=True)
                elif v is None:
                    out[k] = "PENDING" if k.startswith(("ret_", "mae_", "mfe_")) else ""
                else:
                    out[k] = v
            w.writerow(out)
    return csv_path


def initialize_store(jsonl_path, csv_path):
    jsonl_path = Path(jsonl_path)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    if not jsonl_path.exists():
        jsonl_path.write_text("", encoding="utf-8")
    write_projection_csv(jsonl_path, csv_path)
