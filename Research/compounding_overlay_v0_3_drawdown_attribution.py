import json
from pathlib import Path

import numpy as np
import pandas as pd

import compounding_overlay_v0_1_backtest as v1
import compounding_overlay_v0_3_audited_backtest as v3

START = v1.PRIMARY_START
END = v1.PRIMARY_END
COST_BP = 5


def load_state():
    ks11 = v1.load_symbol("ks11")
    kq11 = v1.load_symbol("kq11")
    ks200 = v1.load_symbol("ks200")
    base = v3.assign_regimes_audited(v1.build_features(ks11, kq11, ks200))
    d = v3.mark_strong_r5(base)
    v1.next_exposure = v3.next_exposure_v03
    sim = v1.simulate(d, START, END, COST_BP)
    state = d.loc[sim.curve.index].copy()
    state = state.join(sim.curve[["Hold", "Overlay", "Exposure"]])
    return state


def trading_pos(index, dt):
    try:
        return int(index.get_loc(dt))
    except Exception:
        return None


def first_date(mask, idx):
    hit = idx[mask]
    return None if len(hit) == 0 else hit[0]


def pct(x):
    if x is None or not np.isfinite(x):
        return None
    return float(x)


def drawdown_episodes(state, min_depth=-0.10):
    px = state["K2_Close"].astype(float)
    episodes = []
    peak_date = px.index[0]
    peak_price = float(px.iloc[0])
    in_dd = False
    trough_date = peak_date
    trough_price = peak_price
    trough_dd = 0.0

    for dt, price in px.items():
        price = float(price)
        if not in_dd:
            if price >= peak_price:
                peak_date, peak_price = dt, price
                continue
            in_dd = True
            trough_date, trough_price = dt, price
            trough_dd = price / peak_price - 1
        else:
            dd = price / peak_price - 1
            if dd < trough_dd:
                trough_dd = dd
                trough_date, trough_price = dt, price
            if price >= peak_price:
                if trough_dd <= min_depth:
                    episodes.append((peak_date, peak_price, trough_date, trough_price, trough_dd, dt))
                peak_date, peak_price = dt, price
                in_dd = False
                trough_date, trough_price, trough_dd = dt, price, 0.0

    if in_dd and trough_dd <= min_depth:
        episodes.append((peak_date, peak_price, trough_date, trough_price, trough_dd, None))

    episodes.sort(key=lambda x: x[4])
    return episodes


def episode_detail(state, ep):
    peak_date, peak_price, trough_date, trough_price, hold_dd, recovery_date = ep
    end_date = recovery_date if recovery_date is not None else state.index[-1]
    w = state.loc[peak_date:end_date].copy()
    pre_trough = w.loc[:trough_date]

    def event_for_regime(reg):
        return first_date(pre_trough["Regime"].eq(reg).to_numpy(), pre_trough.index)

    def event_for_exposure(level):
        return first_date((pre_trough["Exposure"] <= level + 1e-9).to_numpy(), pre_trough.index)

    r5 = event_for_regime("R5")
    sr5 = event_for_regime("R5S")
    r6 = event_for_regime("R6")
    e95 = event_for_exposure(0.95)
    e90 = event_for_exposure(0.90)
    e80 = event_for_exposure(0.80)

    post_trough = w.loc[trough_date:]
    r8_after = first_date(post_trough["Regime"].eq("R8").to_numpy(), post_trough.index)
    full_after = first_date((post_trough["Exposure"] >= 0.999).to_numpy(), post_trough.index)

    def event_stats(dt):
        if dt is None:
            return {"date": None, "market_drawdown_from_peak": None, "fraction_of_final_drawdown_realized": None, "trading_days_from_peak": None}
        px = float(state.loc[dt, "K2_Close"])
        dd = px / peak_price - 1
        frac = abs(dd) / abs(hold_dd) if hold_dd < 0 else None
        p0 = trading_pos(state.index, peak_date)
        p1 = trading_pos(state.index, dt)
        delay = None if p0 is None or p1 is None else p1 - p0
        return {
            "date": str(dt.date()),
            "market_drawdown_from_peak": pct(dd),
            "fraction_of_final_drawdown_realized": pct(frac),
            "trading_days_from_peak": delay,
        }

    hold_curve = w["Hold"]
    overlay_curve = w["Overlay"]
    hold_local_dd = float((hold_curve / hold_curve.cummax() - 1).min())
    overlay_local_dd = float((overlay_curve / overlay_curve.cummax() - 1).min())

    return {
        "peak_date": str(peak_date.date()),
        "peak_price": float(peak_price),
        "trough_date": str(trough_date.date()),
        "trough_price": float(trough_price),
        "hold_price_drawdown": float(hold_dd),
        "recovery_date": None if recovery_date is None else str(recovery_date.date()),
        "hold_equity_mdd_in_episode": hold_local_dd,
        "overlay_equity_mdd_in_episode": overlay_local_dd,
        "overlay_mdd_relative_improvement": (abs(hold_local_dd) - abs(overlay_local_dd)) / abs(hold_local_dd) if hold_local_dd else None,
        "first_R5": event_stats(r5),
        "first_StrongR5": event_stats(sr5),
        "first_R6": event_stats(r6),
        "first_exposure_95": event_stats(e95),
        "first_exposure_90": event_stats(e90),
        "first_exposure_80": event_stats(e80),
        "first_R8_after_trough": event_stats(r8_after),
        "first_full_exposure_after_trough": event_stats(full_after),
        "min_exposure_before_trough": float(pre_trough["Exposure"].min()),
    }


def strong_r5_episode_stats(state):
    sig = state["StrongR5"].fillna(False).astype(bool)
    positions = np.flatnonzero(sig.to_numpy())
    if len(positions) == 0:
        return {"episodes": [], "summary": {}}

    groups = []
    start = prev = positions[0]
    for p in positions[1:]:
        # same episode if gap <= 5 trading days
        if p - prev <= 5:
            prev = p
        else:
            groups.append((start, prev))
            start = prev = p
    groups.append((start, prev))

    eps = []
    px = state["K2_Close"].astype(float).to_numpy()
    idx = state.index
    for s, e in groups:
        p0 = px[s]
        end20 = min(len(px) - 1, s + 20)
        end60 = min(len(px) - 1, s + 60)
        f20 = px[s + 1:end20 + 1] / p0 - 1 if end20 > s else np.array([])
        f60 = px[s + 1:end60 + 1] / p0 - 1 if end60 > s else np.array([])
        min20 = float(np.min(f20)) if len(f20) else np.nan
        min60 = float(np.min(f60)) if len(f60) else np.nan
        meaningful = bool((np.isfinite(min20) and min20 <= -0.05) or (np.isfinite(min60) and min60 <= -0.08))
        eps.append({
            "start": str(idx[s].date()),
            "end": str(idx[e].date()),
            "signal_days": int(sig.iloc[s:e + 1].sum()),
            "min_forward_20d": pct(min20),
            "min_forward_60d": pct(min60),
            "meaningful_follow_through": meaningful,
        })

    n = len(eps)
    meaningful_n = sum(x["meaningful_follow_through"] for x in eps)
    return {
        "episodes": eps,
        "summary": {
            "episode_count": n,
            "meaningful_follow_through_count": meaningful_n,
            "meaningful_follow_through_ratio": meaningful_n / n if n else None,
            "diagnostic_definition": "meaningful if next-20d minimum <= -5% OR next-60d minimum <= -8%; diagnostic only, not a trading rule",
        },
    }


def fmt_pct(x):
    if x is None or not np.isfinite(x):
        return "—"
    return f"{x * 100:.1f}%"


def fmt_event(e):
    if e["date"] is None:
        return "—"
    return f"{e['date']} ({fmt_pct(e['market_drawdown_from_peak'])}, final DD {fmt_pct(e['fraction_of_final_drawdown_realized'])} realized)"


def main():
    state = load_state()
    eps = drawdown_episodes(state, -0.10)[:6]
    details = [episode_detail(state, e) for e in eps]
    sr5 = strong_r5_episode_stats(state)

    result = {
        "status": "Historical Proxy diagnostic only; no strategy thresholds changed",
        "period": [str(state.index[0].date()), str(state.index[-1].date())],
        "cost_bp_side": COST_BP,
        "top_drawdowns": details,
        "strong_r5_diagnostics": sr5,
    }

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)
    with open(outdir / "compounding_overlay_v0_3_drawdown_attribution.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    lines = [
        "# Compounding Overlay v0.3 — Top Drawdown Attribution",
        "",
        "Status: Historical Proxy diagnostic only. No thresholds or strategy rules are changed by this analysis.",
        f"Period: {result['period'][0]} ~ {result['period'][1]} / cost {COST_BP}bp per side",
        "",
        "## Top drawdown episodes",
        "",
        "| Peak → Trough | Hold price DD | v0.3 episode MDD improvement | First R5 | First Strong R5 | First 80% exposure | Min exposure | R8 after trough |",
        "|---|---:|---:|---|---|---|---:|---|",
    ]
    for d in details:
        lines.append(
            f"| {d['peak_date']} → {d['trough_date']} | {fmt_pct(d['hold_price_drawdown'])} | "
            f"{fmt_pct(d['overlay_mdd_relative_improvement'])} | {fmt_event(d['first_R5'])} | "
            f"{fmt_event(d['first_StrongR5'])} | {fmt_event(d['first_exposure_80'])} | "
            f"{fmt_pct(d['min_exposure_before_trough'])} | {fmt_event(d['first_R8_after_trough'])} |"
        )

    lines += [
        "",
        "## Strong R5 follow-through diagnostic",
        "",
        f"- Strong R5 clustered episodes: {sr5['summary'].get('episode_count', 0)}",
        f"- Meaningful downside follow-through episodes: {sr5['summary'].get('meaningful_follow_through_count', 0)}",
        f"- Follow-through ratio: {fmt_pct(sr5['summary'].get('meaningful_follow_through_ratio'))}",
        "- Diagnostic definition only: next-20d minimum <= -5% OR next-60d minimum <= -8%.",
        "",
        "## Interpretation guide",
        "- If first 80% exposure occurs after most of the final drawdown is already realized, the main defect is late defense rather than insufficient floor depth.",
        "- If Strong R5 fires frequently without subsequent downside, the main defect is false-positive frequency / over-defense.",
        "- If 80% is reached early but MDD improvement remains small, the 80% Historical Proxy floor itself limits maximum defense.",
        "- This report diagnoses the frozen v0.3; it must not be used to silently retune v0.3 parameters.",
    ]

    with open(outdir / "compounding_overlay_v0_3_drawdown_attribution.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
