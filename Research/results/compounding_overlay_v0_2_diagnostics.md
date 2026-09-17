# Compounding Overlay v0.2 — Diagnostics

## 1. v0.1 → v0.2 structural change

| Metric | v0.1 | v0.2 | Change |
|---|---:|---:|---:|
| 20y Overlay CAGR | 6.02% | 6.19% | +0.17%p |
| 20y CAGR diff vs Hold | -0.29%p | -0.12%p | +0.17%p |
| 20y MDD | -47.51% | -49.41% | -1.90%p |
| 20y MDD relative improvement | 10.22% | 6.63% | -3.59%p |
| Avg exposure | 92.54% | 96.45% | +3.91%p |
| Trades | 628 | 451 | -177 |
| Turnover | 43.60x | 28.20x | -15.40x |

Interpretation: v0.2 restored compounding primarily by staying invested more often, but it surrendered part of the defensive benefit.

## 2. Recent 10y consistency

- CAGR diff vs Hold: v0.1 -0.26%p → v0.2 -0.12%p
- MDD relative improvement: v0.1 11.18% → v0.2 7.80%
- Avg exposure: v0.1 92.18% → v0.2 96.35%
- Trades: v0.1 311 → v0.2 208

## 3. rolling5 at 5bp

- windows: 16
- Overlay beats Hold: 8/16 (50.0%)
- PASS A windows (CAGR diff >= -0.30%p): 9/16 (56.2%)
- PASS B windows (MDD relative improvement >=15%): 0/16 (0.0%)

Worst CAGR-diff windows:
- 2009-2013: CAGR diff -0.76%p, MDD improve 6.68%, avg exp 97.27%, trades 137
- 2012-2016: CAGR diff -0.64%p, MDD improve -3.50%, avg exp 97.33%, trades 97
- 2010-2014: CAGR diff -0.57%p, MDD improve 6.68%, avg exp 97.36%, trades 114
- 2011-2015: CAGR diff -0.56%p, MDD improve 6.04%, avg exp 96.80%, trades 111
- 2013-2017: CAGR diff -0.51%p, MDD improve 1.23%, avg exp 97.58%, trades 97

Best CAGR-diff windows:
- 2018-2022: CAGR diff +0.37%p, MDD improve 8.38%, avg exp 95.33%, trades 108
- 2008-2012: CAGR diff +0.34%p, MDD improve 8.46%, avg exp 96.03%, trades 158
- 2006-2010: CAGR diff +0.33%p, MDD improve 6.63%, avg exp 96.29%, trades 133
- 2020-2024: CAGR diff +0.20%p, MDD improve 2.55%, avg exp 95.92%, trades 104
- 2007-2011: CAGR diff +0.19%p, MDD improve 6.63%, avg exp 95.74%, trades 150

## 3. rolling10 at 5bp

- windows: 11
- Overlay beats Hold: 0/11 (0.0%)
- PASS A windows (CAGR diff >= -0.30%p): 9/11 (81.8%)
- PASS B windows (MDD relative improvement >=15%): 0/11 (0.0%)

Worst CAGR-diff windows:
- 2009-2018: CAGR diff -0.54%p, MDD improve 6.04%, avg exp 97.00%, trades 236
- 2010-2019: CAGR diff -0.48%p, MDD improve 6.04%, avg exp 96.91%, trades 217
- 2012-2021: CAGR diff -0.29%p, MDD improve 7.80%, avg exp 96.93%, trades 193
- 2011-2020: CAGR diff -0.27%p, MDD improve 7.80%, avg exp 96.67%, trades 209
- 2007-2016: CAGR diff -0.26%p, MDD improve 6.63%, avg exp 96.52%, trades 245

Best CAGR-diff windows:
- 2013-2022: CAGR diff -0.07%p, MDD improve 7.80%, avg exp 96.43%, trades 206
- 2008-2017: CAGR diff -0.08%p, MDD improve 8.46%, avg exp 96.80%, trades 255
- 2015-2024: CAGR diff -0.10%p, MDD improve 7.80%, avg exp 96.20%, trades 209
- 2016-2025: CAGR diff -0.12%p, MDD improve 7.80%, avg exp 96.35%, trades 208
- 2014-2023: CAGR diff -0.12%p, MDD improve 7.80%, avg exp 96.40%, trades 204

## 4. Stress windows at 5bp

- 2008_crash: Hold CAGR -38.05%, Overlay CAGR -34.82%, diff +3.23%p, Hold MDD -49.38%, Overlay MDD -45.21%, MDD improve 8.46%, avg exp 91.69%, trades 35
- 2017_bull: Hold CAGR 25.00%, Overlay CAGR 24.78%, diff -0.23%p, Hold MDD -5.99%, Overlay MDD -5.90%, MDD improve 1.48%, avg exp 99.22%, trades 23
- 2020_crash: Hold CAGR -92.42%, Overlay CAGR -89.00%, diff +3.42%p, Hold MDD -34.23%, Overlay MDD -30.73%, MDD improve 10.23%, avg exp 92.50%, trades 3
- 2020_v_rebound: Hold CAGR 109.28%, Overlay CAGR 106.25%, diff -3.03%p, Hold MDD -8.20%, Overlay MDD -8.02%, MDD improve 2.20%, avg exp 97.42%, trades 9
- 2022_bear: Hold CAGR -26.80%, Overlay CAGR -25.99%, diff +0.81%p, Hold MDD -28.86%, Overlay MDD -27.36%, MDD improve 5.20%, avg exp 92.97%, trades 36

## 5. Diagnostic conclusion

- Problem A: v0.2 still pays an underexposure drag in benign/sideways-to-rising windows, although much less than v0.1.
- Problem B: the 80% floor is reached only after the existing R5/R6 sequence, so abrupt crashes can inflict much of the drawdown before maximum defense is active.
- Problem C: a blanket deeper defense would likely recreate v0.1 compounding drag. The next version should deepen defense only when an already-bearish R5/R6 state is accompanied by independent severity confirmation.
- Problem D: R8 immediate restoration appears directionally correct and should remain unchanged for v0.3 unless a specific stress test disproves it.

Recommended v0.3 scope: keep v0.2 normal exposure map unchanged; add a Strong-Risk Gate only inside R5/R6. Do not alter P/I/V or Regime formulas.