# Compounding Overlay v0.1 — Historical Proxy Backtest Results

Data: 2005-01-03 ~ 2025-12-30
Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)
Execution: t-close signal → t+1 open; KOSPI200 is the return asset; KOSPI/KOSDAQ/KOSPI200 feed proxy axes.

## Primary 20-year test

| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | MDD improvement | Avg exposure | Trades |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2bp | 6.31% | 6.09% | -0.22%p | -52.92% | -47.49% | 10.27% | 92.54% | 628 |
| 5bp | 6.31% | 6.02% | -0.29%p | -52.92% | -47.51% | 10.22% | 92.54% | 628 |
| 10bp | 6.30% | 5.90% | -0.40%p | -52.92% | -47.55% | 10.15% | 92.54% | 628 |

## Recent 10-year test

| Cost/side | Hold CAGR | Overlay CAGR | CAGR diff | Hold MDD | Overlay MDD | Avg exposure | Trades |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2bp | 9.96% | 9.77% | -0.19%p | -41.19% | -36.47% | 92.18% | 311 |
| 5bp | 9.95% | 9.69% | -0.26%p | -41.19% | -36.58% | 92.18% | 311 |
| 10bp | 9.94% | 9.56% | -0.38%p | -41.19% | -36.76% | 92.18% | 311 |

## Frozen-rule verdict at 5bp

- PASS A (CAGR no worse than Hold by >0.3%p): True
- PASS B (MDD relative improvement >=15%): False
- Hard Fail condition: False
- Verdict: **MIXED**

## Regime counts
- U: 1532
- R2: 872
- R5: 809
- R3: 475
- R1: 455
- R7: 315
- R4: 236
- R8: 196
- R6: 43

This is Historical Proxy validation, not Full C1–C8 validation. v0.1 thresholds were frozen before results and are not altered here.