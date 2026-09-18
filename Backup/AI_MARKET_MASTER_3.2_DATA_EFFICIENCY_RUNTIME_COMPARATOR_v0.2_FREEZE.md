# AI Market Master 3.2 — Data Efficiency Runtime Comparator v0.2 Freeze

Date: 2026-09-18
Status: FROZEN RESEARCH IMPLEMENTATION / PROSPECTIVE COMPARISON ONLY

## Reason for v0.2
The first real E2E sample exposed an important diagnostic gap in v0.1:
sign-direction agreement can be TRUE even when the two SAI values fall into different official Action Bands.

Example from 2026-09-18 09:03:
- Official SAI = +0.2952 -> BALANCED
- DE Candidate SAI = +0.4438356 -> POSITIVE
- sign direction agreement = TRUE
- Action Band agreement = FALSE

Therefore v0.2 adds official Action Band diagnostics while preserving all v0.1 append-only and authority boundaries.

## Added fields
- official_action_band
- candidate_action_band
- action_band_agreement

Official band definitions are read from Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md section 28:
- +0.60 to +1.00: Strong Positive
- +0.30 to <+0.60: Positive
- >-0.30 to <+0.30: Balanced
- >-0.60 to <=-0.30: Negative
- -1.00 to <=-0.60: Strong Negative

## Files
- Research/data_efficiency_runtime_comparator_v0_2.py
- Research/test_data_efficiency_runtime_comparator_v0_2.py
- Research/runtime/data_efficiency_runtime_comparator_v0_2.jsonl

## First E2E sample
Sample ID:
AMM32-DE-20260918-0903

Observed:
- Official SAI exact arithmetic: +0.2952 / PARTIAL / BALANCED
- Candidate SAI_DE partial: +0.4438356164 / PARTIAL / POSITIVE
- Delta: +0.1486356164
- Material divergence threshold 0.15: NOT triggered
- Action Band disagreement: triggered
- Official data-weight coverage: 100%
- Candidate data-weight coverage: 78.49%
- Regime agreement: TRUE
- Outcomes: T+1/T+5/T+20 PENDING

Candidate C4 was unavailable because KOSPI200 and KRX100 returns were not supplied.
Candidate C6 was unavailable because KTB3Y bp change was not supplied.

The Candidate PARTIAL gate nevertheless passes:
- 5/7 components usable
- C5 usable
- C1/C2 usable
- C3/C4 axis satisfied via C3
- C6/C7 axis satisfied via C7
- candidate weight coverage 78.49% >= 70%

## Important interpretation
The higher Candidate SAI is NOT evidence that the Candidate is superior.
The first sample specifically demonstrates why missing-data renormalization must be monitored:
two negative official components, C4 and C6, are unavailable in the Candidate and the remaining usable axes are renormalized upward.

This is a prospective validation observation, not an authority change or trading recommendation.

Official 3.2 remains unchanged.
Data Efficiency Candidate v0.1 remains unchanged.
