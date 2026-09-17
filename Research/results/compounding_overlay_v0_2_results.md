# Compounding Overlay v0.2 — Historical Proxy Backtest Results

Data: 2005-01-03 ~ 2025-12-30
Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)
Execution: same frozen v0.1 P/I/V and Regime formulas; only the three pre-frozen v0.2 exposure changes differ.

## Primary 20-year test

| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | MDD improvement | Avg exposure | Trades |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2bp | 6.31% | 6.23% | -0.08%p | -52.92% | -49.37% | 6.70% | 96.45% | 451 |
| 5bp | 6.31% | 6.19% | -0.12%p | -52.92% | -49.41% | 6.63% | 96.45% | 451 |
| 10bp | 6.30% | 6.11% | -0.19%p | -52.92% | -49.47% | 6.51% | 96.45% | 451 |

## Recent 10-year test

| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | Avg exposure | Trades |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2bp | 9.96% | 9.88% | -0.08%p | -41.19% | -37.92% | 96.35% | 208 |
| 5bp | 9.95% | 9.84% | -0.12%p | -41.19% | -37.97% | 96.35% | 208 |
| 10bp | 9.94% | 9.76% | -0.19%p | -41.19% | -38.06% | 96.35% | 208 |

## Frozen-rule verdict at 5bp

- PASS A (CAGR no worse than Hold by >0.3%p): True
- PASS B (MDD relative improvement >=15%): False
- Hard Fail condition: False
- Verdict: **MIXED**

This is Historical Proxy validation, not Full C1–C8 validation. No v0.2 parameter is altered after seeing these results.