# Compounding Overlay v0.4 — Frozen Historical Proxy Test

Status: EXPERIMENTAL / Historical Proxy / not official 3.2 authority
Data: 2005-01-03 ~ 2025-12-30
Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)

Raw Strong R5 days (20y): 260
Confirmed 2-of-3 Strong R5 days (20y): 201

## Primary 20-year — 5bp/side

| Model | CAGR | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades | Turnover |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hold | 6.31% | — | -52.92% | — | 100.00% | — | — |
| v0.2 audited | 6.13% | -0.17%p | -49.53% | 6.41% | 96.60% | 460 | 28.40 |
| v0.3 | 6.00% | -0.30%p | -48.26% | 8.79% | 96.04% | 551 | 37.60 |
| v0.4 | 6.05% | -0.25%p | -48.59% | 8.19% | 96.11% | 549 | 38.20 |

## Recent 10-year — 5bp/side

| Model | CAGR | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades |
|---|---:|---:|---:|---:|---:|---:|
| Hold | 9.95% | — | -41.19% | — | 100.00% | — |
| v0.2 audited | 9.86% | -0.10%p | -37.91% | 7.95% | 96.50% | 215 |
| v0.3 | 9.75% | -0.20%p | -37.08% | 9.96% | 95.85% | 285 |
| v0.4 | 9.75% | -0.21%p | -37.21% | 9.66% | 95.96% | 273 |

## v0.4 rolling robustness — 5bp/side
- Rolling 5y Hold-beat ratio: 50.00%
- Rolling 10y Hold-beat ratio: 0.00%
- Rolling 5y PASS-A ratio: 50.00%
- Rolling 10y PASS-A ratio: 63.64%

## Frozen criteria — v0.4
- PASS A compounding preservation: True
- PASS B >=15% relative MDD improvement: False
- Hard Fail: False
- Verdict: **MIXED**

The 15% MDD target is retained for comparability even though the separate defense-ceiling diagnostic showed it is close to the theoretical maximum of an 80%-floor model. No v0.4 parameter is altered after this test.