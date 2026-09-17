import json
import numpy as np

import compounding_overlay_v0_1_backtest as v1


def next_exposure_v02(current, signal_regime, last_reduce_i, i):
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

    # Reduction: unchanged v0.1 cooldown and max single -10%p.
    if target < current:
        if last_reduce_i is not None and i - last_reduce_i < 2:
            return current, last_reduce_i
        if current >= 1.00:
            new = max(target, 0.95)
        else:
            new = max(target, current - 0.10)
        allowed = np.array([0.80, 0.90, 0.95, 1.00])
        new = float(allowed[np.argmin(np.abs(allowed - new))])
        return new, i if new < current else last_reduce_i

    # R8: direct restoration to 100%.
    if signal_regime == "R8" and current < 1.00:
        return 1.00, last_reduce_i

    # R1/R2/R3: normal fast restoration toward 100%.
    if target > current:
        step = 0.10
        new = min(target, current + step)
        allowed = np.array([0.80, 0.90, 0.95, 1.00])
        new = float(allowed[np.argmin(np.abs(allowed - new))])
        return new, last_reduce_i

    return current, last_reduce_i


def main():
    v1.next_exposure = next_exposure_v02

    print("Downloading KRX-derived cache data for v0.2...")
    ks11 = v1.load_symbol("ks11")
    kq11 = v1.load_symbol("kq11")
    ks200 = v1.load_symbol("ks200")
    d = v1.assign_regimes(v1.build_features(ks11, kq11, ks200))

    results = {
        "data_start": str(d.index.min().date()),
        "data_end": str(d.index.max().date()),
        "formula_version": "Compounding Overlay v0.2 Design Freeze 1",
        "changes_vs_v0_1": [
            "R3 target 100% instead of 95%",
            "R4 95%, R5 90%, R6 80%, R7 90% — defense concentrated in R5/R6",
            "R8 immediate restoration to 100%",
        ],
        "primary": {},
        "recent10": {},
        "rolling5": {},
        "rolling10": {},
        "stress": {},
        "regime_counts": d.loc[v1.PRIMARY_START:v1.PRIMARY_END, "Regime"].value_counts().to_dict(),
    }

    for bp in v1.COSTS_BP:
        p, _ = v1.eval_window(d, v1.PRIMARY_START, v1.PRIMARY_END, bp)
        r10, _ = v1.eval_window(d, v1.RECENT_START, v1.PRIMARY_END, bp)
        results["primary"][str(bp)] = p
        results["recent10"][str(bp)] = r10
        results["rolling5"][str(bp)] = v1.rolling_year_windows(d, 5, bp)
        results["rolling10"][str(bp)] = v1.rolling_year_windows(d, 10, bp)

    results["stress"] = v1.stress_windows(d, 5)

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

    with open("compounding_overlay_v0_2_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    lines = [
        "# Compounding Overlay v0.2 — Historical Proxy Backtest Results",
        "",
        f"Data: {results['data_start']} ~ {results['data_end']}",
        "Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)",
        "Execution: same frozen v0.1 P/I/V and Regime formulas; only the three pre-frozen v0.2 exposure changes differ.",
        "",
        "## Primary 20-year test",
        "",
        "| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | MDD improvement | Avg exposure | Trades |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for bp in v1.COSTS_BP:
        m = results["primary"][str(bp)]
        lines.append(f"| {bp}bp | {v1.pct(m['Hold']['CAGR'])} | {v1.pct(m['Overlay']['CAGR'])} | {m['CAGR_Diff_pp']:+.2f}%p | {v1.pct(m['Hold']['MDD'])} | {v1.pct(m['Overlay']['MDD'])} | {v1.pct(m['MDD_Relative_Improvement'])} | {v1.pct(m['Overlay']['AvgExposure'])} | {m['Trades']} |")

    lines += [
        "",
        "## Recent 10-year test",
        "",
        "| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | Avg exposure | Trades |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for bp in v1.COSTS_BP:
        m = results["recent10"][str(bp)]
        lines.append(f"| {bp}bp | {v1.pct(m['Hold']['CAGR'])} | {v1.pct(m['Overlay']['CAGR'])} | {m['CAGR_Diff_pp']:+.2f}%p | {v1.pct(m['Hold']['MDD'])} | {v1.pct(m['Overlay']['MDD'])} | {v1.pct(m['Overlay']['AvgExposure'])} | {m['Trades']} |")

    lines += [
        "",
        "## Frozen-rule verdict at 5bp",
        "",
        f"- PASS A (CAGR no worse than Hold by >0.3%p): {pass_a}",
        f"- PASS B (MDD relative improvement >=15%): {pass_b}",
        f"- Hard Fail condition: {fail_hard}",
        f"- Verdict: **{verdict}**",
        "",
        "This is Historical Proxy validation, not Full C1–C8 validation. No v0.2 parameter is altered after seeing these results.",
    ]

    with open("compounding_overlay_v0_2_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
