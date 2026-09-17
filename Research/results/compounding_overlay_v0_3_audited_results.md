# Compounding Overlay v0.3 — Audited Historical Proxy Test

Status: Historical Proxy / corrected implementation / frozen thresholds
Data: 2005-01-03 ~ 2025-12-30
Source: FinanceData/fdr_krx_data_cache (KRX-derived public cache)

## Implementation audit applied before result generation
- Frozen R8 rule implemented literally as: 10-day I improvement >=0.15 OR current I>0.
- Frozen staged reduction implemented deterministically: 100->95->90->80, never >10%p in one reduction.
- No P/I/V, R1-R8, Strong R5, cost, or execution threshold was changed after results.

Strong R5 observations: 260 days in primary 20-year window; 152 days in recent 10-year window.

## Primary 20-year — 5bp/side

| Model | CAGR | Final wealth (100m start) | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hold | 6.31% | 339,544,658 KRW | — | -52.92% | — | 100.00% | — |
| v0.2 audited | 6.13% | 328,650,336 KRW | -0.17%p | -49.53% | 6.41% | 96.60% | 460 |
| v0.3 | 6.00% | 320,628,319 KRW | -0.30%p | -48.26% | 8.79% | 96.04% | 551 |

## Recent 10-year — 5bp/side

| Model | CAGR | CAGR diff vs Hold | MDD | MDD improvement | Avg exposure | Trades |
|---|---:|---:|---:|---:|---:|---:|
| Hold | 9.95% | — | -41.19% | — | 100.00% | — |
| v0.2 audited | 9.86% | -0.10%p | -37.91% | 7.95% | 96.50% | 215 |
| v0.3 | 9.75% | -0.20%p | -37.08% | 9.96% | 95.85% | 285 |

## Rolling robustness — 5bp/side
- v0.2 audited rolling 5y Hold-beat ratio: 43.75%
- v0.3 rolling 5y Hold-beat ratio: 43.75%
- v0.2 audited rolling 10y Hold-beat ratio: 0.00%
- v0.3 rolling 10y Hold-beat ratio: 0.00%

## Frozen pass/fail — v0.3 at 5bp
- PASS A compounding preservation: False
- PASS B >=15% relative MDD improvement: False
- Hard Fail: False
- Verdict: **MIXED**

This remains Historical Proxy validation, not Full C1-C8 validation.