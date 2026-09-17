import json
from pathlib import Path

import numpy as np

import compounding_overlay_v0_1_backtest as v1
import compounding_overlay_v0_3_audited_backtest as v3


def mark_v04_state(base):
    out = base.copy()
    raw = (
        (out["Regime"] == "R5")
        & (out["P"] <= -0.80)
        & ((out["I"] <= -0.50) | (out["vperc"] >= 0.85))
    )
    confirmed = raw & (raw.astype(int).rolling(3, min_periods=1).sum() >= 2)
    out["StrongR5Raw"] = raw
    out["StrongR5Confirmed"] = confirmed
    out.loc[raw & ~confirmed, "Regime"] = "R5S"
    out.loc[confirmed, "Regime"] = "R5C"
    return out


def next_exposure_v04(current, signal_regime, last_reduce_i, i):
    target = {
        "R1": 1.00,
        "R2": 1.00,
        "R3": 1.00,
        "R4": 0.95,
        "R5": 0.90,
        "R5S": 0.90,
        "R5C": 0.80,
        "R6": 0.80,
        "R7": 0.90,
        "R8": 1.00,
        "U": current,
    }[signal_regime]

    if target < current:
        # Strong-risk accelerator: use full -10%p step for confirmed Strong R5 or R6.
        if signal_regime in {"R5C", "R6"}:
            if last_reduce_i is not None and i - last_reduce_i < 2:
                return current, last_reduce_i
            if current >= 0.999:
                new = 0.90
            elif current >= 0.899:
                new = 0.80
            else:
                new = current
            if new < target:
                new = target
            return new, i if new < current else last_reduce_i

        # Ordinary deterioration keeps the audited gradual path.
        return v3.staged_reduce(current, target, last_reduce_i, i)

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


def fmt_pct(x):
    return "—" if x is None or not np.isfinite(x) else f"{x*100:.2f}%"


def main():
    print("Loading KRX-derived data for frozen v0.4 test...")
    ks11 = v1.load_symbol("ks11")
    kq11 = v1.load_symbol("kq11")
    ks200 = v1.load_symbol("ks200")

    base = v3.assign_regimes_audited(v1.build_features(ks11, kq11, ks200))
    v03data = v3.mark_strong_r5(base)
    v04data = mark_v04_state(base)

    v02 = v3.run_model(base, v3.next_exposure_v02_audited, "v0.2-audited")
    v03 = v3.run_model(v03data, v3.next_exposure_v03, "v0.3-frozen")
    v04 = v3.run_model(v04data, next_exposure_v04, "v0.4-frozen")

    out = {
        "data_start": str(base.index.min().date()),
        "data_end": str(base.index.max().date()),
        "v0_4_design": {
            "raw_strong_r5_rule": "Base R5 AND P<=-0.80 AND (I<=-0.50 OR Vpercentile>=0.85)",
            "confirmation": "raw Strong R5 true today AND true on >=2 of last 3 trading days including today",
            "accelerator": "Confirmed Strong R5 or R6 may reduce 100->90 in one -10pp step, then subject to frozen cooldown 90->80",
            "floor": 0.80,
            "threshold_changes_after_results": False,
        },
        "counts_20y": {
            "raw_strong_r5_days": int(v04data.loc[v1.PRIMARY_START:v1.PRIMARY_END, "StrongR5Raw"].sum()),
            "confirmed_strong_r5_days": int(v04data.loc[v1.PRIMARY_START:v1.PRIMARY_END, "StrongR5Confirmed"].sum()),
        },
        "counts_recent10": {
            "raw_strong_r5_days": int(v04data.loc[v1.RECENT_START:v1.PRIMARY_END, "StrongR5Raw"].sum()),
            "confirmed_strong_r5_days": int(v04data.loc[v1.RECENT_START:v1.PRIMARY_END, "StrongR5Confirmed"].sum()),
        },
        "v0_2_audited": v02,
        "v0_3": v03,
        "v0_4": v04,
    }

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)
    with open(outdir / "compounding_overlay_v0_4_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    models = [("v0.2 audited", v02), ("v0.3", v03), ("v0.4", v04)]
    lines = [
        "# Compounding Overlay v0.4 — Frozen Historical Proxy Test",
        "",
        "Status: EXPERIMENTAL / Historical Proxy / not official 3.2 authority",
        f"Data: {out['data_start']} ~ {out['data_end']}",
        "Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)",
        "",
        f"Raw Strong R5 days (20y): {out['counts_20y']['raw_strong_r5_days']}",
        f"Confirmed 2-of-3 Strong R5 days (20y): {out['counts_20y']['confirmed_strong_r5_days']}",
        "",
        "## Primary 20-year — 5bp/side",
        "",
        "| Model | CAGR | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades | Turnover |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    hold = v02["primary"]["5"]["Hold"]
    lines.append(f"| Hold | {fmt_pct(hold['CAGR'])} | — | {fmt_pct(hold['MDD'])} | — | 100.00% | — | — |")
    for name, res in models:
        m = res["primary"]["5"]
        lines.append(
            f"| {name} | {fmt_pct(m['Overlay']['CAGR'])} | {m['CAGR_Diff_pp']:+.2f}%p | {fmt_pct(m['Overlay']['MDD'])} | "
            f"{fmt_pct(m['MDD_Relative_Improvement'])} | {fmt_pct(m['Overlay']['AvgExposure'])} | {m['Trades']} | {m['Turnover']:.2f} |"
        )

    lines += [
        "",
        "## Recent 10-year — 5bp/side",
        "",
        "| Model | CAGR | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    hold10 = v02["recent10"]["5"]["Hold"]
    lines.append(f"| Hold | {fmt_pct(hold10['CAGR'])} | — | {fmt_pct(hold10['MDD'])} | — | 100.00% | — |")
    for name, res in models:
        m = res["recent10"]["5"]
        lines.append(
            f"| {name} | {fmt_pct(m['Overlay']['CAGR'])} | {m['CAGR_Diff_pp']:+.2f}%p | {fmt_pct(m['Overlay']['MDD'])} | "
            f"{fmt_pct(m['MDD_Relative_Improvement'])} | {fmt_pct(m['Overlay']['AvgExposure'])} | {m['Trades']} |"
        )

    r5 = v04["rolling5_summary"]["5"]
    r10 = v04["rolling10_summary"]["5"]
    verdict = v04["verdict_5bp"]
    lines += [
        "",
        "## v0.4 rolling robustness — 5bp/side",
        f"- Rolling 5y Hold-beat ratio: {fmt_pct(r5['beat_hold_ratio'])}",
        f"- Rolling 10y Hold-beat ratio: {fmt_pct(r10['beat_hold_ratio'])}",
        f"- Rolling 5y PASS-A ratio: {fmt_pct(r5['passA_ratio'])}",
        f"- Rolling 10y PASS-A ratio: {fmt_pct(r10['passA_ratio'])}",
        "",
        "## Frozen criteria — v0.4",
        f"- PASS A compounding preservation: {verdict['PASS_A_Compounding']}",
        f"- PASS B >=15% relative MDD improvement: {verdict['PASS_B_Risk']}",
        f"- Hard Fail: {verdict['HardFail']}",
        f"- Verdict: **{verdict['Verdict']}**",
        "",
        "The 15% MDD target is retained for comparability even though the separate defense-ceiling diagnostic showed it is close to the theoretical maximum of an 80%-floor model. No v0.4 parameter is altered after this test.",
    ]

    with open(outdir / "compounding_overlay_v0_4_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
