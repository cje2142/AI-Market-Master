import io
import json
import math
import urllib.request
from dataclasses import dataclass

import numpy as np
import pandas as pd

BASE = "https://raw.githubusercontent.com/FinanceData/fdr_krx_data_cache/master/data/index"
START_WARMUP = 2005
END_YEAR = 2025
PRIMARY_START = "2006-01-02"
PRIMARY_END = "2025-12-31"
RECENT_START = "2016-01-01"
COSTS_BP = [2, 5, 10]


def read_year(symbol: str, year: int) -> pd.DataFrame:
    url = f"{BASE}/year_{symbol}/{year}.csv"
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read()
    df = pd.read_csv(io.BytesIO(raw), encoding="utf-8-sig")
    df["Date"] = pd.to_datetime(df["Date"])
    return df[["Date", "Open", "High", "Low", "Close"]].copy()


def load_symbol(symbol: str) -> pd.DataFrame:
    frames = []
    for y in range(START_WARMUP, END_YEAR + 1):
        try:
            frames.append(read_year(symbol, y))
        except Exception as e:
            print(f"WARN {symbol} {y}: {e}")
    if not frames:
        raise RuntimeError(f"No data for {symbol}")
    df = pd.concat(frames, ignore_index=True).drop_duplicates("Date").sort_values("Date")
    return df.set_index("Date")


def pct_rank_last(x):
    s = pd.Series(x)
    if s.isna().all():
        return np.nan
    v = s.iloc[-1]
    if pd.isna(v):
        return np.nan
    valid = s.dropna()
    return float((valid <= v).mean())


def ternary_ma(close, ma):
    return np.where(close > ma * 1.005, 1, np.where(close < ma * 0.995, -1, 0))


def ternary_ret(r, pos, neg):
    return np.where(r > pos, 1, np.where(r < neg, -1, 0))


def build_features(ks11, kq11, ks200):
    idx = ks11.index.intersection(kq11.index).intersection(ks200.index)
    d = pd.DataFrame(index=idx)
    for pfx, src in [("K", ks11), ("Q", kq11), ("K2", ks200)]:
        for c in ["Open", "High", "Low", "Close"]:
            d[f"{pfx}_{c}"] = src.loc[idx, c].astype(float)

    c = d["K_Close"]
    d["ret1"] = c.pct_change()
    d["r5"] = c.pct_change(5)
    d["r20"] = c.pct_change(20)
    d["r60"] = c.pct_change(60)
    d["ma20"] = c.rolling(20).mean()
    d["ma60"] = c.rolling(60).mean()
    d["ma200"] = c.rolling(200).mean()
    d["high252"] = c.rolling(252).max()
    d["dd252"] = c / d["high252"] - 1

    parts = np.column_stack([
        ternary_ma(c, d["ma20"]),
        ternary_ma(c, d["ma60"]),
        ternary_ma(c, d["ma200"]),
        ternary_ret(d["r20"], 0.03, -0.03),
        ternary_ret(d["r60"], 0.06, -0.06),
    ])
    d["P"] = np.nanmean(parts, axis=1)

    q20 = d["Q_Close"].pct_change(20)
    k220 = d["K2_Close"].pct_change(20)
    k20 = d["K_Close"].pct_change(20)
    d["q_rel_raw"] = q20 - k20
    d["k2_rel_raw"] = k220 - k20
    qn = (d["q_rel_raw"] / 0.05).clip(-1, 1)
    k2n = (d["k2_rel_raw"] / 0.025).clip(-1, 1)
    d["I"] = 0.60 * qn + 0.40 * k2n

    d["rv20"] = d["ret1"].rolling(20).std() * math.sqrt(252)
    d["vperc"] = d["rv20"].rolling(252).apply(pct_rank_last, raw=False)
    d["vperc_med20_prev"] = d["vperc"].shift(1).rolling(20).median()
    d["vperc_max10_prev"] = d["vperc"].shift(1).rolling(10).max()
    d["rv20_max5_prev"] = d["rv20"].shift(1).rolling(5).max()
    d["low10_prev"] = d["K_Close"].shift(1).rolling(10).min()

    def crossed_recent(series, n=10):
        out = []
        arr = series.to_numpy()
        for i in range(len(arr)):
            if i < n:
                out.append(False)
                continue
            w = arr[i-n:i+1]
            w = w[np.isfinite(w)]
            out.append(bool(len(w) and np.nanmin(w) < 0 and np.nanmax(w) > 0))
        return out

    d["rotation_cross"] = np.array(crossed_recent(d["q_rel_raw"], 10)) | np.array(crossed_recent(d["k2_rel_raw"], 10))
    return d


def assign_regimes(d):
    regimes = []
    for i, (dt, r) in enumerate(d.iterrows()):
        reg = "U"
        if not np.isfinite(r.get("P", np.nan)) or not np.isfinite(r.get("I", np.nan)) or not np.isfinite(r.get("vperc", np.nan)):
            regimes.append(reg)
            continue

        panic_flags = sum([
            bool(r["ret1"] <= -0.04) if np.isfinite(r["ret1"]) else False,
            bool(r["r5"] <= -0.08) if np.isfinite(r["r5"]) else False,
            bool(r["dd252"] <= -0.15) if np.isfinite(r["dd252"]) else False,
        ])
        if r["vperc"] >= 0.80 and panic_flags >= 2:
            reg = "R6"
            regimes.append(reg)
            continue

        prior = regimes[max(0, i-20):i]
        recovery_recent = any(x in {"R5", "R6", "R7"} for x in prior)
        r8 = (
            recovery_recent
            and r["K_Close"] > r["ma20"]
            and r["r20"] > 0
            and ((r["I"] - d["I"].iloc[i-10] >= 0.15) if i >= 10 and np.isfinite(d["I"].iloc[i-10]) else False or r["I"] > 0)
            and np.isfinite(r["vperc_max10_prev"])
            and r["vperc"] <= r["vperc_max10_prev"] - 0.10
        )
        if r8:
            reg = "R8"
            regimes.append(reg)
            continue

        r7 = (
            r["dd252"] <= -0.15
            and r["r5"] > -0.03
            and np.isfinite(r["low10_prev"])
            and r["K_Close"] >= r["low10_prev"] * 1.02
            and np.isfinite(r["rv20_max5_prev"])
            and r["rv20"] < r["rv20_max5_prev"]
        )
        if r7:
            reg = "R7"
            regimes.append(reg)
            continue

        if r["P"] <= -0.40 and (r["I"] <= -0.20 or r["vperc"] >= 0.70):
            reg = "R5"
            regimes.append(reg)
            continue

        r4 = (
            (r["P"] > 0 or r["dd252"] > -0.07)
            and r["I"] <= -0.20
            and (r["K_Close"] < r["ma20"] or r["r5"] < 0)
            and np.isfinite(r["vperc_med20_prev"])
            and r["vperc"] > r["vperc_med20_prev"]
        )
        if r4:
            reg = "R4"
            regimes.append(reg)
            continue

        if r["P"] >= 0.40 and r["k2_rel_raw"] > 0 and r["I"] < 0.20 and r["vperc"] < 0.80:
            reg = "R2"
            regimes.append(reg)
            continue

        if r["P"] >= 0.40 and r["I"] >= 0.20 and r["vperc"] < 0.70:
            reg = "R1"
            regimes.append(reg)
            continue

        if -0.40 < r["P"] < 0.40 and r["vperc"] < 0.80 and bool(r["rotation_cross"]):
            reg = "R3"

        regimes.append(reg)
    out = d.copy()
    out["Regime"] = regimes
    return out


def next_exposure(current, signal_regime, last_reduce_i, i):
    # Historical Proxy mode floor = 80%.
    target = {
        "R1": 1.00,
        "R2": 1.00,
        "R3": 0.95,
        "R4": 0.90,
        "R5": 0.80,
        "R6": 0.80,
        "R7": 0.80,
        "R8": 1.00,
        "U": current,
    }[signal_regime]

    if target < current:
        if last_reduce_i is not None and i - last_reduce_i < 2:
            return current, last_reduce_i
        if current >= 1.00:
            new = max(target, 0.95)
        elif current >= 0.95:
            new = max(target, 0.90)
        else:
            new = max(target, current - 0.10)
        new = max(0.80, round(new, 2))
        return new, i if new < current else last_reduce_i

    if target > current:
        # Slow Exit / Fast Re-entry. R8 may restore up to +20%p.
        step = 0.20 if signal_regime == "R8" else 0.10
        new = min(target, current + step)
        allowed = np.array([0.80, 0.90, 0.95, 1.00])
        new = float(allowed[np.argmin(np.abs(allowed - new))])
        return new, last_reduce_i

    return current, last_reduce_i


@dataclass
class RunResult:
    curve: pd.DataFrame
    trades: int
    turnover: float


def simulate(d, start, end, cost_bp):
    x = d.loc[pd.Timestamp(start):pd.Timestamp(end)].copy()
    if len(x) < 2:
        raise ValueError("insufficient window")
    cost = cost_bp / 10000.0

    hold_eq = 1.0 * (1 - cost)  # initial buy
    strat_eq = 1.0 * (1 - cost)
    exposure = 1.0
    last_reduce_i = None
    trades = 0
    turnover = 0.0
    recs = []

    prev_close = x["K2_Close"].iloc[0]
    # First row: establish initial state only.
    recs.append((x.index[0], hold_eq, strat_eq, exposure, x["Regime"].iloc[0]))

    for j in range(1, len(x)):
        dt = x.index[j]
        row = x.iloc[j]
        prev_signal = x["Regime"].iloc[j-1]

        opn = row["K2_Open"]
        cls = row["K2_Close"]
        if not (np.isfinite(opn) and np.isfinite(cls) and np.isfinite(prev_close) and prev_close > 0 and opn > 0):
            prev_close = cls
            recs.append((dt, hold_eq, strat_eq, exposure, row["Regime"]))
            continue

        gap = opn / prev_close - 1
        intraday = cls / opn - 1

        hold_eq *= (1 + gap) * (1 + intraday)

        # Old exposure receives overnight gap.
        strat_eq *= (1 + exposure * gap)

        new_exp, new_last_reduce = next_exposure(exposure, prev_signal, last_reduce_i, j)
        if abs(new_exp - exposure) >= 0.049999:
            change = abs(new_exp - exposure)
            strat_eq *= (1 - cost * change)
            turnover += change
            trades += 1
        exposure = new_exp
        last_reduce_i = new_last_reduce

        strat_eq *= (1 + exposure * intraday)
        prev_close = cls
        recs.append((dt, hold_eq, strat_eq, exposure, row["Regime"]))

    # final liquidation for both
    hold_eq *= (1 - cost)
    strat_eq *= (1 - cost * exposure)
    recs[-1] = (recs[-1][0], hold_eq, strat_eq, exposure, recs[-1][4])

    curve = pd.DataFrame(recs, columns=["Date", "Hold", "Overlay", "Exposure", "Regime"]).set_index("Date")
    return RunResult(curve, trades, turnover)


def metrics(series, exposure=None):
    s = series.dropna()
    years = (s.index[-1] - s.index[0]).days / 365.25
    cagr = s.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan
    peak = s.cummax()
    dd = s / peak - 1
    mdd = float(dd.min())
    rets = s.pct_change().dropna()
    sharpe = float(rets.mean() / rets.std() * math.sqrt(252)) if rets.std() > 0 else np.nan
    neg = rets[rets < 0]
    sortino = float(rets.mean() / neg.std() * math.sqrt(252)) if len(neg) > 1 and neg.std() > 0 else np.nan
    avg_exp = float(exposure.loc[s.index].mean()) if exposure is not None else 1.0
    return {
        "CAGR": float(cagr),
        "TerminalMultiple": float(s.iloc[-1]),
        "MDD": mdd,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "AvgExposure": avg_exp,
    }


def eval_window(d, start, end, cost_bp):
    r = simulate(d, start, end, cost_bp)
    h = metrics(r.curve["Hold"])
    o = metrics(r.curve["Overlay"], r.curve["Exposure"])
    mdd_improve = (abs(h["MDD"]) - abs(o["MDD"])) / abs(h["MDD"]) if h["MDD"] else np.nan
    return {
        "start": str(r.curve.index[0].date()),
        "end": str(r.curve.index[-1].date()),
        "cost_bp": cost_bp,
        "Hold": h,
        "Overlay": o,
        "CAGR_Diff_pp": (o["CAGR"] - h["CAGR"]) * 100,
        "MDD_Relative_Improvement": mdd_improve,
        "Trades": r.trades,
        "Turnover": r.turnover,
    }, r


def rolling_year_windows(d, years, cost_bp):
    out = []
    start_year = 2006
    last_year = 2025
    for y0 in range(start_year, last_year - years + 2):
        y1 = y0 + years - 1
        start = f"{y0}-01-01"
        end = f"{y1}-12-31"
        try:
            m, _ = eval_window(d, start, end, cost_bp)
            m["label"] = f"{y0}-{y1}"
            out.append(m)
        except Exception:
            pass
    return out


def stress_windows(d, cost_bp=5):
    windows = {
        "2008_crash": ("2008-01-01", "2008-12-31"),
        "2017_bull": ("2017-01-01", "2017-12-31"),
        "2020_crash": ("2020-02-01", "2020-03-23"),
        "2020_v_rebound": ("2020-03-24", "2020-12-30"),
        "2022_bear": ("2022-01-01", "2022-12-31"),
    }
    out = {}
    for k, (a, b) in windows.items():
        m, _ = eval_window(d, a, b, cost_bp)
        out[k] = m
    return out


def pct(x):
    return "n/a" if x is None or not np.isfinite(x) else f"{x*100:.2f}%"


def main():
    print("Downloading KRX-derived cache data...")
    ks11 = load_symbol("ks11")
    kq11 = load_symbol("kq11")
    ks200 = load_symbol("ks200")
    d = assign_regimes(build_features(ks11, kq11, ks200))

    results = {
        "data_start": str(d.index.min().date()),
        "data_end": str(d.index.max().date()),
        "formula_version": "Compounding Overlay v0.1 Simulation Formula Freeze",
        "primary": {},
        "recent10": {},
        "rolling5": {},
        "rolling10": {},
        "stress": {},
        "regime_counts": d.loc[PRIMARY_START:PRIMARY_END, "Regime"].value_counts().to_dict(),
    }

    for bp in COSTS_BP:
        p, _ = eval_window(d, PRIMARY_START, PRIMARY_END, bp)
        r10, _ = eval_window(d, RECENT_START, PRIMARY_END, bp)
        results["primary"][str(bp)] = p
        results["recent10"][str(bp)] = r10
        results["rolling5"][str(bp)] = rolling_year_windows(d, 5, bp)
        results["rolling10"][str(bp)] = rolling_year_windows(d, 10, bp)

    results["stress"] = stress_windows(d, 5)

    # Primary pass/fail at 5bp
    p5 = results["primary"]["5"]
    diff_pp = p5["CAGR_Diff_pp"]
    mdd_imp = p5["MDD_Relative_Improvement"]
    avg_exp = p5["Overlay"]["AvgExposure"]
    pass_a = diff_pp >= -0.30
    pass_b = mdd_imp >= 0.15
    fail_hard = diff_pp <= -1.0 or avg_exp <= 0.85
    if pass_a and pass_b:
        verdict = "PASS"
    elif fail_hard:
        verdict = "FAIL"
    else:
        verdict = "MIXED"
    results["verdict_5bp"] = {
        "PASS_A_Compounding": pass_a,
        "PASS_B_Risk": pass_b,
        "HardFail": fail_hard,
        "Verdict": verdict,
    }

    with open("compounding_overlay_v0_1_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("# Compounding Overlay v0.1 — Historical Proxy Backtest Results")
    lines.append("")
    lines.append(f"Data: {results['data_start']} ~ {results['data_end']}")
    lines.append("Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)")
    lines.append("Execution: t-close signal → t+1 open; KOSPI200 is the return asset; KOSPI/KOSDAQ/KOSPI200 feed proxy axes.")
    lines.append("")
    lines.append("## Primary 20-year test")
    lines.append("")
    lines.append("| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | MDD improvement | Avg exposure | Trades |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for bp in COSTS_BP:
        m = results["primary"][str(bp)]
        lines.append(f"| {bp}bp | {pct(m['Hold']['CAGR'])} | {pct(m['Overlay']['CAGR'])} | {m['CAGR_Diff_pp']:+.2f}%p | {pct(m['Hold']['MDD'])} | {pct(m['Overlay']['MDD'])} | {pct(m['MDD_Relative_Improvement'])} | {pct(m['Overlay']['AvgExposure'])} | {m['Trades']} |")
    lines.append("")
    lines.append("## Recent 10-year test")
    lines.append("")
    lines.append("| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | Avg exposure | Trades |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for bp in COSTS_BP:
        m = results["recent10"][str(bp)]
        lines.append(f"| {bp}bp | {pct(m['Hold']['CAGR'])} | {pct(m['Overlay']['CAGR'])} | {m['CAGR_Diff_pp']:+.2f}%p | {pct(m['Hold']['MDD'])} | {pct(m['Overlay']['MDD'])} | {pct(m['Overlay']['AvgExposure'])} | {m['Trades']} |")
    lines.append("")
    lines.append("## Frozen-rule verdict at 5bp")
    lines.append("")
    lines.append(f"- PASS A (CAGR no worse than Hold by >0.3%p): {pass_a}")
    lines.append(f"- PASS B (MDD relative improvement >=15%): {pass_b}")
    lines.append(f"- Hard Fail condition: {fail_hard}")
    lines.append(f"- Verdict: **{verdict}**")
    lines.append("")
    lines.append("## Regime counts")
    for k, v in results["regime_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("This is Historical Proxy validation, not Full C1–C8 validation. v0.1 thresholds were frozen before results and are not altered here.")

    with open("compounding_overlay_v0_1_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
