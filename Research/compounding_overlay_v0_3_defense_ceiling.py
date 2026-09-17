import json
from pathlib import Path

import numpy as np

import compounding_overlay_v0_3_drawdown_attribution as da


def constant_exposure_mdd(prices, exposure):
    r = prices.pct_change().fillna(0.0).to_numpy()
    eq = np.cumprod(1.0 + exposure * r)
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1.0
    return float(dd.min())


def required_exposure_for_target(prices, hold_mdd, relative_improvement=0.15):
    target_abs = abs(hold_mdd) * (1.0 - relative_improvement)
    lo, hi = 0.0, 1.0
    # Find highest constant exposure whose MDD magnitude remains <= target_abs.
    for _ in range(70):
        mid = (lo + hi) / 2.0
        mdd = abs(constant_exposure_mdd(prices, mid))
        if mdd <= target_abs:
            lo = mid
        else:
            hi = mid
    return lo


def fmt_pct(x):
    return "—" if x is None or not np.isfinite(x) else f"{x*100:.1f}%"


def main():
    state = da.load_state()
    episodes = da.drawdown_episodes(state, -0.10)[:6]
    actual = [da.episode_detail(state, ep) for ep in episodes]

    rows = []
    for ep, act in zip(episodes, actual):
        peak_date, _, trough_date, _, _, _ = ep
        prices = state.loc[peak_date:trough_date, "K2_Close"].astype(float)
        hold_mdd = constant_exposure_mdd(prices, 1.0)
        ideal90 = constant_exposure_mdd(prices, 0.90)
        ideal80 = constant_exposure_mdd(prices, 0.80)
        imp90 = (abs(hold_mdd) - abs(ideal90)) / abs(hold_mdd)
        imp80 = (abs(hold_mdd) - abs(ideal80)) / abs(hold_mdd)
        req15 = required_exposure_for_target(prices, hold_mdd, 0.15)
        rows.append({
            "peak_date": act["peak_date"],
            "trough_date": act["trough_date"],
            "hold_mdd_close_to_close": hold_mdd,
            "actual_v03_episode_improvement": act["overlay_mdd_relative_improvement"],
            "perfect_90_from_peak_improvement": imp90,
            "perfect_80_from_peak_improvement": imp80,
            "constant_exposure_required_for_15pct_improvement": req15,
            "actual_first_80_fraction_final_dd_realized": act["first_exposure_80"]["fraction_of_final_drawdown_realized"],
        })

    out = {
        "status": "Structural feasibility diagnostic only; perfect-foresight ceilings are not tradable strategies",
        "target_relative_mdd_improvement": 0.15,
        "historical_proxy_floor": 0.80,
        "episodes": rows,
    }

    outdir = Path("results")
    outdir.mkdir(exist_ok=True)
    with open(outdir / "compounding_overlay_v0_3_defense_ceiling.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = [
        "# Compounding Overlay v0.3 — 80% Floor Defense Ceiling",
        "",
        "Status: Structural feasibility diagnostic only. Perfect 80%/90% exposure from each peak is hindsight and is NOT a tradable strategy.",
        "Purpose: test whether the frozen >=15% relative MDD-improvement target is realistically compatible with the Historical Proxy 80% exposure floor.",
        "",
        "| Peak → Trough | Actual v0.3 MDD improvement | Perfect 90% from peak | Perfect 80% from peak | Constant exposure needed for 15% MDD improvement | DD already realized when v0.3 first reached 80% |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['peak_date']} → {r['trough_date']} | {fmt_pct(r['actual_v03_episode_improvement'])} | "
            f"{fmt_pct(r['perfect_90_from_peak_improvement'])} | {fmt_pct(r['perfect_80_from_peak_improvement'])} | "
            f"{fmt_pct(r['constant_exposure_required_for_15pct_improvement'])} | "
            f"{fmt_pct(r['actual_first_80_fraction_final_dd_realized'])} |"
        )

    lines += [
        "",
        "## Reading the ceiling",
        "- Perfect 80% from peak is an unattainable hindsight upper-bound for an 80%-floor model during each decline.",
        "- If the exposure required for 15% improvement is close to 80%, the 15% target demands near-perfect early defense and leaves almost no timing error budget.",
        "- If perfect 80% itself fails to reach 15% improvement, the target and floor are structurally incompatible for that episode.",
        "- No v0.4 threshold should be selected from this table alone; it is a feasibility check, not optimization.",
    ]

    with open(outdir / "compounding_overlay_v0_3_defense_ceiling.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
