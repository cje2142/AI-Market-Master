import json
from pathlib import Path

V1 = Path('Research/results/compounding_overlay_v0_1_results.json')
V2 = Path('Research/results/compounding_overlay_v0_2_results.json')
OUT = Path('Research/results/compounding_overlay_v0_2_diagnostics.md')


def load(p):
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


def pct(x):
    return f"{x*100:.2f}%"


def pp(x):
    return f"{x:+.2f}%p"


def summarize_roll(arr):
    n = len(arr)
    beat = sum(1 for x in arr if x['CAGR_Diff_pp'] > 0)
    pass_a = sum(1 for x in arr if x['CAGR_Diff_pp'] >= -0.30)
    pass_b = sum(1 for x in arr if x['MDD_Relative_Improvement'] >= 0.15)
    worst = sorted(arr, key=lambda x: x['CAGR_Diff_pp'])[:5]
    best = sorted(arr, key=lambda x: x['CAGR_Diff_pp'], reverse=True)[:5]
    return n, beat, pass_a, pass_b, worst, best


def main():
    a = load(V1)
    b = load(V2)
    lines = ['# Compounding Overlay v0.2 — Diagnostics', '']

    p1 = a['primary']['5']; p2 = b['primary']['5']
    r1 = a['recent10']['5']; r2 = b['recent10']['5']
    lines += [
        '## 1. v0.1 → v0.2 structural change', '',
        '| Metric | v0.1 | v0.2 | Change |',
        '|---|---:|---:|---:|',
        f"| 20y Overlay CAGR | {pct(p1['Overlay']['CAGR'])} | {pct(p2['Overlay']['CAGR'])} | {(p2['Overlay']['CAGR']-p1['Overlay']['CAGR'])*100:+.2f}%p |",
        f"| 20y CAGR diff vs Hold | {pp(p1['CAGR_Diff_pp'])} | {pp(p2['CAGR_Diff_pp'])} | {(p2['CAGR_Diff_pp']-p1['CAGR_Diff_pp']):+.2f}%p |",
        f"| 20y MDD | {pct(p1['Overlay']['MDD'])} | {pct(p2['Overlay']['MDD'])} | {(p2['Overlay']['MDD']-p1['Overlay']['MDD'])*100:+.2f}%p |",
        f"| 20y MDD relative improvement | {pct(p1['MDD_Relative_Improvement'])} | {pct(p2['MDD_Relative_Improvement'])} | {(p2['MDD_Relative_Improvement']-p1['MDD_Relative_Improvement'])*100:+.2f}%p |",
        f"| Avg exposure | {pct(p1['Overlay']['AvgExposure'])} | {pct(p2['Overlay']['AvgExposure'])} | {(p2['Overlay']['AvgExposure']-p1['Overlay']['AvgExposure'])*100:+.2f}%p |",
        f"| Trades | {p1['Trades']} | {p2['Trades']} | {p2['Trades']-p1['Trades']:+d} |",
        f"| Turnover | {p1['Turnover']:.2f}x | {p2['Turnover']:.2f}x | {p2['Turnover']-p1['Turnover']:+.2f}x |",
        '',
        'Interpretation: v0.2 restored compounding primarily by staying invested more often, but it surrendered part of the defensive benefit.',
        '',
        '## 2. Recent 10y consistency', '',
        f"- CAGR diff vs Hold: v0.1 {pp(r1['CAGR_Diff_pp'])} → v0.2 {pp(r2['CAGR_Diff_pp'])}",
        f"- MDD relative improvement: v0.1 {pct(r1['MDD_Relative_Improvement'])} → v0.2 {pct(r2['MDD_Relative_Improvement'])}",
        f"- Avg exposure: v0.1 {pct(r1['Overlay']['AvgExposure'])} → v0.2 {pct(r2['Overlay']['AvgExposure'])}",
        f"- Trades: v0.1 {r1['Trades']} → v0.2 {r2['Trades']}",
        ''
    ]

    for horizon in ['rolling5','rolling10']:
        arr = b[horizon]['5']
        n, beat, pass_a, pass_b, worst, best = summarize_roll(arr)
        lines += [
            f"## 3. {horizon} at 5bp", '',
            f"- windows: {n}",
            f"- Overlay beats Hold: {beat}/{n} ({beat/n*100:.1f}%)",
            f"- PASS A windows (CAGR diff >= -0.30%p): {pass_a}/{n} ({pass_a/n*100:.1f}%)",
            f"- PASS B windows (MDD relative improvement >=15%): {pass_b}/{n} ({pass_b/n*100:.1f}%)",
            '',
            'Worst CAGR-diff windows:',
        ]
        for x in worst:
            lines.append(f"- {x['label']}: CAGR diff {pp(x['CAGR_Diff_pp'])}, MDD improve {pct(x['MDD_Relative_Improvement'])}, avg exp {pct(x['Overlay']['AvgExposure'])}, trades {x['Trades']}")
        lines.append('')
        lines.append('Best CAGR-diff windows:')
        for x in best:
            lines.append(f"- {x['label']}: CAGR diff {pp(x['CAGR_Diff_pp'])}, MDD improve {pct(x['MDD_Relative_Improvement'])}, avg exp {pct(x['Overlay']['AvgExposure'])}, trades {x['Trades']}")
        lines.append('')

    lines += ['## 4. Stress windows at 5bp', '']
    for name, x in b['stress'].items():
        lines.append(
            f"- {name}: Hold CAGR {pct(x['Hold']['CAGR'])}, Overlay CAGR {pct(x['Overlay']['CAGR'])}, "
            f"diff {pp(x['CAGR_Diff_pp'])}, Hold MDD {pct(x['Hold']['MDD'])}, Overlay MDD {pct(x['Overlay']['MDD'])}, "
            f"MDD improve {pct(x['MDD_Relative_Improvement'])}, avg exp {pct(x['Overlay']['AvgExposure'])}, trades {x['Trades']}"
        )

    lines += [
        '', '## 5. Diagnostic conclusion', '',
        '- Problem A: v0.2 still pays an underexposure drag in benign/sideways-to-rising windows, although much less than v0.1.',
        '- Problem B: the 80% floor is reached only after the existing R5/R6 sequence, so abrupt crashes can inflict much of the drawdown before maximum defense is active.',
        '- Problem C: a blanket deeper defense would likely recreate v0.1 compounding drag. The next version should deepen defense only when an already-bearish R5/R6 state is accompanied by independent severity confirmation.',
        '- Problem D: R8 immediate restoration appears directionally correct and should remain unchanged for v0.3 unless a specific stress test disproves it.',
        '',
        'Recommended v0.3 scope: keep v0.2 normal exposure map unchanged; add a Strong-Risk Gate only inside R5/R6. Do not alter P/I/V or Regime formulas.',
    ]

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(OUT.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
