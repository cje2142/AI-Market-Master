import argparse
import csv
import io
import json
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import full_evidence_runtime_log_v0_1 as runtime

BASE = "https://raw.githubusercontent.com/FinanceData/fdr_krx_data_cache/master/data/index"
HORIZONS = (1, 5, 20)


def _to_float(value):
    if value is None:
        raise ValueError("missing Close")
    return float(str(value).replace(",", "").strip())


def normalize_sessions(rows):
    """Return sorted unique observed KOSPI sessions as [{'date': date, 'close': float}, ...].

    The updater never invents missing sessions. The supplied rows are treated only as
    observed exchange sessions; unavailable future rows remain PENDING.
    """
    out = []
    seen = set()
    for row in rows:
        d = row["date"]
        if isinstance(d, str):
            d = date.fromisoformat(d[:10])
        if not isinstance(d, date):
            raise ValueError("session date must be date or ISO date string")
        if d in seen:
            raise ValueError(f"duplicate observed session: {d}")
        close = _to_float(row["close"])
        if close <= 0:
            raise ValueError(f"invalid Close for {d}: {close}")
        seen.add(d)
        out.append({"date": d, "close": close})
    out.sort(key=lambda x: x["date"])
    return out


def fetch_ks11_year(year):
    url = f"{BASE}/year_ks11/{int(year)}.csv"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            raw = r.read().decode("utf-8-sig")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise

    rows = []
    for row in csv.DictReader(io.StringIO(raw)):
        if not row.get("Date") or not row.get("Close"):
            continue
        rows.append({"date": row["Date"], "close": row["Close"]})
    return rows


def load_public_kospi_sessions(start_year, end_year):
    rows = []
    for year in range(int(start_year), int(end_year) + 1):
        rows.extend(fetch_ks11_year(year))
    return normalize_sessions(rows)


def horizon_metrics(sessions, signal_index, horizon):
    if signal_index + horizon >= len(sessions):
        return None
    base = sessions[signal_index]["close"]
    future = sessions[signal_index + 1: signal_index + horizon + 1]
    returns = [x["close"] / base - 1.0 for x in future]
    result = {f"ret_{horizon}d": returns[-1]}
    if horizon in (5, 20):
        result[f"mae_{horizon}d"] = min(returns)
        result[f"mfe_{horizon}d"] = max(returns)
    return result


def update_runtime_outcomes(log_path, csv_path, sessions):
    sessions = normalize_sessions(sessions)
    index = {x["date"]: i for i, x in enumerate(sessions)}
    rows = runtime.build_projection(log_path)

    appended = []
    pending = []
    unavailable = []

    for row in rows:
        sid = row["sample_id"]
        signal_date = date.fromisoformat(str(row["market_date"])[:10])
        loc = index.get(signal_date)
        if loc is None:
            unavailable.append({"sample_id": sid, "reason": "SIGNAL_DATE_NOT_IN_OBSERVED_KOSPI_DATA"})
            continue

        for h in HORIZONS:
            horizon = f"{h}d"
            if row.get(f"outcome_status_{horizon}") == "MATURE":
                continue
            metrics = horizon_metrics(sessions, loc, h)
            if metrics is None:
                pending.append({"sample_id": sid, "horizon": horizon})
                continue
            runtime.append_outcome(log_path, sid, horizon, metrics)
            appended.append({"sample_id": sid, "horizon": horizon, **metrics})

    # CSV is always regenerated from the canonical append-only JSONL journal.
    runtime.write_projection_csv(log_path, csv_path)
    return {
        "appended_count": len(appended),
        "appended": appended,
        "pending": pending,
        "unavailable": unavailable,
        "observed_sessions": len(sessions),
        "latest_observed_date": str(sessions[-1]["date"]) if sessions else None,
    }


def year_span_for_runtime(log_path):
    rows = runtime.build_projection(log_path)
    if not rows:
        now_year = datetime.now(ZoneInfo("Asia/Seoul")).year
        return now_year, now_year
    years = [date.fromisoformat(str(r["market_date"])[:10]).year for r in rows]
    now_year = datetime.now(ZoneInfo("Asia/Seoul")).year
    # Load one following year so late-December signals can mature across year-end.
    return min(years), max(max(years), now_year) + 1


def main():
    parser = argparse.ArgumentParser(description="Mature +1d/+5d/+20d Full Evidence outcomes from observed KOSPI closes")
    parser.add_argument("--log", default="Research/runtime/full_evidence_runtime_log_v0_1.jsonl")
    parser.add_argument("--csv", default="Research/runtime/full_evidence_runtime_log_v0_1.csv")
    args = parser.parse_args()

    log_path = Path(args.log)
    csv_path = Path(args.csv)
    start_year, end_year = year_span_for_runtime(log_path)
    sessions = load_public_kospi_sessions(start_year, end_year)
    summary = update_runtime_outcomes(log_path, csv_path, sessions)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
