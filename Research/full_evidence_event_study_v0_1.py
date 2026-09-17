import io
import json
import urllib.request
from pathlib import Path

import pandas as pd

BASE = "https://raw.githubusercontent.com/FinanceData/fdr_krx_data_cache/master/data/index"
EVENTS = [
    ("2026-07-15", "Strong Bull / Recovery", "HOLD / avoid chasing / partial profit management", "REGIME+HTS"),
    ("2026-07-16", "Panic / Capitulation", "NO CHASE-SELL / leverage reduction on rebound", "REGIME+HTS"),
    ("2026-07-21", "Selective strength / weak internals", "HOLD / SELECTIVE BUY", "REGIME+HTS"),
    ("2026-07-24", "Risk-Off Correction", "NO AGGRESSIVE BUY", "REGIME+HTS"),
    ("2026-07-30", "Risk / Oversold conflict", "MANAGE LEVERAGE / WAIT RECOVERY", "REGIME+HTS"),
    ("2026-08-04", "Bullish Rebound + high volatility", "CONFIRMATION BUY", "REGIME+HTS"),
    ("2026-09-08", "Leadership Bull -> Distribution confirmation", "CORE HOLD / NO NEW LEVERAGE", "REGIME"),
    ("2026-09-10", "R2 maintained / R4 watch", "HOLD", "C1-C8 PARTIAL"),
    ("2026-09-11", "R4 Distribution / R5 watch", "RISK REDUCTION WATCH / TECHNICAL CONFLICT", "C1-C8 FULL"),
]
HORIZONS = [1, 5, 20]


def read_year(symbol: str, year: int = 2026) -> pd.DataFrame:
    url = f"{BASE}/year_{symbol}/{year}.csv"
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read()
    df = pd.read_csv(io.BytesIO(raw), encoding="utf-8-sig")
    df["Date"] = pd.to_datetime(df["Date"])
    return df[["Date", "Open", "High", "Low", "Close"]].drop_duplicates("Date").sort_values("Date").set_index("Date")


def pct(x):
    return None if x is None or pd.isna(x) else float(x)


def event_metrics(df: pd.DataFrame, date: str):
    dt = pd.Timestamp(date)
    if dt not in df.index:
        return {"status": "DATE_NOT_AVAILABLE"}
    loc = df.index.get_loc(dt)
    if not isinstance(loc, int):
        loc = int(loc.start)
    base = float(df.iloc[loc]["Close"])
    out = {"status": "OK", "signal_close": base, "available_future_sessions": int(len(df) - loc - 1)}
    for h in HORIZONS:
        key = f"h{h}"
        if loc + h >= len(df):
            out[key] = {"status": "PENDING"}
            continue
        future = df.iloc[loc + 1: loc + h + 1]
        end_close = float(df.iloc[loc + h]["Close"])
        returns = future["Close"].astype(float) / base - 1.0
        out[key] = {
            "status": "COMPLETE",
            "end_date": str(df.index[loc + h].date()),
            "forward_return": float(end_close / base - 1.0),
            "mae_close": float(returns.min()),
            "mfe_close": float(returns.max()),
        }
    return out


def fmt(v):
    return "PENDING" if v is None else f"{v*100:+.2f}%"


def main():
    print("Loading 2026 KRX-derived index data...")
    data = {
        "KOSPI": read_year("ks11"),
        "KOSPI200": read_year("ks200"),
        "KOSDAQ": read_year("kq11"),
    }
    out = {
        "status": "DIAGNOSTIC_ONLY",
        "study": "Full Evidence Validation Set v0.1 event study",
        "data_sources": "FinanceData/fdr_krx_data_cache KRX-derived public cache",
        "events": [],
    }
    for date, state, posture, quality in EVENTS:
        row = {
            "date": date,
            "dashboard_state": state,
            "historical_posture": posture,
            "evidence_quality": quality,
            "markets": {name: event_metrics(df, date) for name, df in data.items()},
        }
        out["events"].append(row)

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)
    with open(outdir / "full_evidence_event_study_v0_1.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = [
        "# AI Market Master 3.2 — Full Evidence Validation Event Study v0.1",
        "",
        "Status: DIAGNOSTIC ONLY / no rule retuning / no success threshold selected after outcomes",
        "Primary path: KOSPI. KOSPI200 and KOSDAQ are secondary confirmation.",
        "Forward returns are signal-close to future close. MAE/MFE use intervening closes, not intraday extremes.",
        "",
        "| Date | Historical state | Historical posture | Quality | KOSPI +1d | +5d | 5d MAE | 5d MFE | +20d | 20d MAE | 20d MFE |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for e in out["events"]:
        m = e["markets"]["KOSPI"]
        vals = {}
        for h in HORIZONS:
            obj = m.get(f"h{h}", {})
            if obj.get("status") == "COMPLETE":
                vals[h] = obj
            else:
                vals[h] = None
        lines.append(
            f"| {e['date']} | {e['dashboard_state']} | {e['historical_posture']} | {e['evidence_quality']} | "
            f"{fmt(vals[1]['forward_return'] if vals[1] else None)} | "
            f"{fmt(vals[5]['forward_return'] if vals[5] else None)} | "
            f"{fmt(vals[5]['mae_close'] if vals[5] else None)} | "
            f"{fmt(vals[5]['mfe_close'] if vals[5] else None)} | "
            f"{fmt(vals[20]['forward_return'] if vals[20] else None)} | "
            f"{fmt(vals[20]['mae_close'] if vals[20] else None)} | "
            f"{fmt(vals[20]['mfe_close'] if vals[20] else None)} |"
        )

    lines += [
        "",
        "## Interpretation boundary",
        "- This table does not declare a decision correct merely because the next return moved in the same direction.",
        "- Panic/Recovery decisions are evaluated for path quality and re-entry risk, not only endpoint return.",
        "- Missing future horizons remain PENDING and are never imputed.",
        "- 2026-09-10 is PARTIAL Full Evidence because C6 was unavailable; missing != neutral.",
        "- 2026-09-11 contains technical conflict (positive C5), so WATCH and EXECUTE must remain distinct.",
    ]
    with open(outdir / "full_evidence_event_study_v0_1.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
