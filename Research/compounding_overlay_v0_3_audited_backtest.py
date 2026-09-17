import json
import numpy as np

import compounding_overlay_v0_1_backtest as v1


def assign_regimes_audited(d):
    """Frozen v0.1 proxy regimes with the R8 OR-condition implemented literally."""
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
            regimes.append("R6")
            continue

        prior = regimes[max(0, i - 20):i]
        recovery_recent = any(x in {"R5", "R6", "R7"} for x in prior)
        i_improved = False
        if i >= 10 and np.isfinite(d["I"].iloc[i - 10]):
            i_improved = (r["I"] - d["I"].iloc[i - 10]) >= 0.15
        i_recovery_ok = bool(i_improved or (r["I"] > 0))

        r8 = (
            recovery_recent
            and r["K_Close"] > r["ma20"]
            and r["r20"] > 0
            and i_recovery_ok
            and np.isfinite(r["vperc_max10_prev"])
            and r["vperc"] <= r["vperc_max10_prev"] - 0.10
        )
        if r8:
            regimes.append("R8")
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
            regimes.append("R7")
            continue

        if r["P"] <= -0.40 and (r["I"] <= -0.20 or r["vperc"] >= 0.70):
            regimes.append("R5")
            continue

        r4 = (
            (r["P"] > 0 or r["dd252"] > -0.07)
            and r["I"] <= -0.20
            and (r["K_Close"] < r["ma20"] or r["r5"] < 0)
            and np.isfinite(r["vperc_med20_prev"])
            and r["vperc"] > r["vperc_med20_prev"]
        )
        if r4:
            regimes.append("R4")
            continue

        if r["P"] >= 0.40 and r["k2_rel_raw"] > 0 and r["I"] < 0.20 and r["vperc"] < 0.80:
            regimes.append("R2")
            continue

        if r["P"] >= 0.40 and r["I"] >= 0.20 and r["vperc"] < 0.70:
            regimes.append("R1")
            continue

        if -0.40 < r["P"] < 0.40 and r["vperc"] < 0.80 and bool(r["rotation_cross"]):
            reg = "R3"

        regimes.append(reg)

    out = d.copy()
    out["Regime"] = regimes
    return out


def staged_reduce(current, target, last_reduce_i, i):
    # Frozen max single reduction <= 10%p with discrete states 100/95/90/80.
    if last_reduce_i is not None and i - last_reduce_i < 2:
        return current, last_reduce_i
    if current >= 0.999:
        new = 0.95
    elif current >= 0.949:
        new = 0.90
    elif current >= 0.899:
        new = 0.80 if target <= 0.80 else 0.90
    else:
        new = current
    if new < target:
        new = target
    return new, i if new < current else last_reduce_i


def next_exposure_v02_audited(current, signal_regime, last_reduce_i, i):
    target = {
        "R1": 1.00,
        "R2": 1.00,
        "R3": 1.00,
        "R4": 0.95,
        "R5": 0.90,
        "R6": 0.80,
        "R7": 0.90,
        "R8": 1.00,
        "U": current,
    }[signal_regime]

    if target < current:
        return staged_reduce(current, target, last_reduce_i, i)

    if signal_regime == "R8" and current < 1.00:
        return 1.00, last_reduce_i

    if target > current:
        new = min(target, current + 0.10)
        if current <= 0.801 and target >= 0.90:
            new = 0.90
        elif current <= 0.901 and target >= 1.00:
            new = 1.00
        elif current <= 0.951 and target >= 1.00:
            new = 1.00
        return round(new, 2), last_reduce_i

    return current, last_reduce_i


def next_exposure_v03(current, signal_regime, last_reduce_i, i):
    target = {
        "R1": 1.00,
        "R2": 1.00,
        "R3": 1.00,
        "R4": 0.95,
        "R5": 0.90,
        "R5S": 0.80,
        "R6": 0.80,
        "R7": 0.90,
        "R8": 1.00,
        "U": current,
    }[signal_regime]

    if target < current:
        return staged_reduce(current, target, last_reduce_i, i)

    if signal_regime == "R8" and current < 1.00:
        return 1.00, last_reduce_i

    if target > current:
        new = min(target, current + 0.10)
        if current <= 0.801 and target >= 0.90:
            new = 0.90
        elif current <= 0.901 and target >= 1.00:
            new = 1.00
        elif current <= 0.951 and target >= 1.00:
            new = 1.00
        return round(new, 2), last_reduce_i

    return current, last_reduce_i


def mark_strong_r5(d):
    out = d.copy()
    strong = (
        (out["Regime"] == "R5")
        & (out["P"] <= -0.80)
        & ((out["I"] <= -0.50) | (out["vperc"] >= 0.85))
    )
    out["StrongR5"] = strong
    out.loc[strong, "Regime"] = "R5S"
    return out


def rolling_summary(items):
    if not items:
        return {"n": 0, "beat_hold_ratio": None, "passA_ratio": None, "median_cagr_diff_pp": None, "median_mdd_improvement": None}
    diffs = np.array([x["CAGR_Diff_pp"] for x in items], dtype=float)
    mdds = np.array([x["MDD_Relative_Improvement"] for x in items], dtype=float)
    return {
        "n": len(items),
        "beat_hold_ratio": float(np.mean(diffs > 0)),
        "passA_ratio": float(np.mean(diffs >= -0.30)),
        "median_cagr_diff_pp": float(np.median(diffs)),
        "median_mdd_improvement": float(np.median(mdds)),
    }


def run_model(d, transition, version):
    v1.next_exposure = transition
    res = {
        "version": version,
        "primary": {},
        "recent10": {},
        "rolling5": {},
        "rolling10": {},
        "rolling5_summary": {},
        "rolling10_summary": {},
        "stress": {},
    }
    for bp in v1.COSTS_BP:
        p, _ = v1.eval_window(d, v1.PRIMARY_START, v1.PRIMARY_END, bp)
        r10, _ = v1.eval_window(d, v1.RECENT_START, v1.PRIMARY_END, bp)
        r5 = v1.rolling_year_windows(d, 5, bp)
        r10w = v1.rolling_year_windows(d, 10, bp)
        res["primary"][str(bp)] = p
        res["recent10"][str(bp)] = r10
        res["rolling5"][str(bp)] = r5
        res["rolling10"][str(bp)] = r10w
        res["rolling5_summary"][str(bp)] = rolling_summary(r5)
        res["rolling10_summary"][str(bp)] = rolling_summary(r10w)
    res["stress"] = v1.stress_windows(d, 5)
    p5 = res["primary"]["5"]
    res["verdict_5bp"] = {
        "PASS_A_Compounding": p5["CAGR_Diff_pp"] >= -0.30,
        "PASS_B_Risk": p5["MDD_Relative_Improvement"] >= 0.15,
        "HardFail": p5["CAGR_Diff_pp"] <= -1.0 or p5["Overlay"]["AvgExposure"] <= 0.85,
    }
    if res["verdict_5bp"]["PASS_A_Compounding"] and res["verdict_5bp"]["PASS_B_Risk"]:
        res["verdict_5bp"]["Verdict"] = "PASS"
    elif res["verdict_5bp"]["HardFail"]:
        res["verdict_5bp"]["Verdict"] = "FAIL"
    else:
        res["verdict_5bp"]["Verdict"] = "MIXED"
    return res


def money(mult):
    return mult * 100_000_000


def pct(x):
    return f"{x*100:.2f}%"


def main():
    print("Loading KRX-derived data and running audited v0.2 + frozen v0.3...")
    ks11 = v1.load_symbol("ks11")
    kq11 = v1.load_symbol("kq11")
    ks200 = v1.load_symbol("ks200")
    base = assign_regimes_audited(v1.build_features(ks11, kq11, ks200))
    v03data = mark_strong_r5(base)

    v02 = run_model(base, next_exposure_v02_audited, "v0.2-audited")
    v03 = run_model(v03data, next_exposure_v03, "v0.3-frozen")

    strong_count = int(v03data.loc[v1.PRIMARY_START:v1.PRIMARY_END, "StrongR5"].sum())
    strong_recent = int(v03data.loc[v1.RECENT_START:v1.PRIMARY_END, "StrongR5"].sum())
    base_counts = base.loc[v1.PRIMARY_START:v1.PRIMARY_END, "Regime"].value_counts().to_dict()

    out = {
        "data_start": str(base.index.min().date()),
        "data_end": str(base.index.max().date()),
        "implementation_audit": {
            "R8_or_condition_corrected": True,
            "staged_reduction_max_10pp_corrected": True,
            "threshold_changes": False,
        },
        "strong_r5_rule": "Base R5 AND P<=-0.80 AND (I<=-0.50 OR Vpercentile>=0.85)",
        "strong_r5_count_20y": strong_count,
        "strong_r5_count_recent10": strong_recent,
        "base_regime_counts_20y": base_counts,
        "v0_2_audited": v02,
        "v0_3": v03,
    }

    with open("compounding_overlay_v0_3_audited_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    p2 = v02["primary"]["5"]
    p3 = v03["primary"]["5"]
    t2 = v02["recent10"]["5"]
    t3 = v03["recent10"]["5"]

    lines = [
        "# Compounding Overlay v0.3 — Audited Historical Proxy Test",
        "",
        "Status: Historical Proxy / corrected implementation / frozen thresholds",
        f"Data: {out['data_start']} ~ {out['data_end']}",
        "Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)",
        "",
        "## Implementation audit applied before result generation",
        "- Frozen R8 rule implemented literally as: 10-day I improvement >=0.15 OR current I>0.",
        "- Frozen staged reduction implemented deterministically: 100->95->90->80, never >10%p in one reduction.",
        "- No P/I/V, R1-R8, Strong R5, cost, or execution threshold was changed after results.",
        "",
        f"Strong R5 observations: {strong_count} days in primary 20-year window; {strong_recent} days in recent 10-year window.",
        "",
        "## Primary 20-year — 5bp/side",
        "",
        "| Model | CAGR | Final wealth (100m start) | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| Hold | {pct(p2['Hold']['CAGR'])} | {money(p2['Hold']['TerminalMultiple']):,.0f} KRW | — | {pct(p2['Hold']['MDD'])} | — | 100.00% | — |",
        f"| v0.2 audited | {pct(p2['Overlay']['CAGR'])} | {money(p2['Overlay']['TerminalMultiple']):,.0f} KRW | {p2['CAGR_Diff_pp']:+.2f}%p | {pct(p2['Overlay']['MDD'])} | {pct(p2['MDD_Relative_Improvement'])} | {pct(p2['Overlay']['AvgExposure'])} | {p2['Trades']} |",
        f"| v0.3 | {pct(p3['Overlay']['CAGR'])} | {money(p3['Overlay']['TerminalMultiple']):,.0f} KRW | {p3['CAGR_Diff_pp']:+.2f}%p | {pct(p3['Overlay']['MDD'])} | {pct(p3['MDD_Relative_Improvement'])} | {pct(p3['Overlay']['AvgExposure'])} | {p3['Trades']} |",
        "",
        "## Recent 10-year — 5bp/side",
        "",
        "| Model | CAGR | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades |",
        "|---|---:|---:|---:|---:|---:|---:|",
        f"| Hold | {pct(t2['Hold']['CAGR'])} | — | {pct(t2['Hold']['MDD'])} | — | 100.00% | — |",
        f"| v0.2 audited | {pct(t2['Overlay']['CAGR'])} | {t2['CAGR_Diff_pp']:+.2f}%p | {pct(t2['Overlay']['MDD'])} | {pct(t2['MDD_Relative_Improvement'])} | {pct(t2['Overlay']['AvgExposure'])} | {t2['Trades']} |",
        f"| v0.3 | {pct(t3['Overlay']['CAGR'])} | {t3['CAGR_Diff_pp']:+.2f}%p | {pct(t3['Overlay']['MDD'])} | {pct(t3['MDD_Relative_Improvement'])} | {pct(t3['Overlay']['AvgExposure'])} | {t3['Trades']} |",
        "",
        "## Rolling robustness — 5bp/side",
        f"- v0.2 audited rolling 5y Hold-beat ratio: {pct(v02['rolling5_summary']['5']['beat_hold_ratio'])}",
        f"- v0.3 rolling 5y Hold-beat ratio: {pct(v03['rolling5_summary']['5']['beat_hold_ratio'])}",
        f"- v0.2 audited rolling 10y Hold-beat ratio: {pct(v02['rolling10_summary']['5']['beat_hold_ratio'])}",
        f"- v0.3 rolling 10y Hold-beat ratio: {pct(v03['rolling10_summary']['5']['beat_hold_ratio'])}",
        "",
        "## Frozen pass/fail — v0.3 at 5bp",
        f"- PASS A compounding preservation: {v03['verdict_5bp']['PASS_A_Compounding']}",
        f"- PASS B >=15% relative MDD improvement: {v03['verdict_5bp']['PASS_B_Risk']}",
        f"- Hard Fail: {v03['verdict_5bp']['HardFail']}",
        f"- Verdict: **{v03['verdict_5bp']['Verdict']}**",
        "",
        "This remains Historical Proxy validation, not Full C1-C8 validation.",
    ]

    with open("compounding_overlay_v0_3_audited_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
