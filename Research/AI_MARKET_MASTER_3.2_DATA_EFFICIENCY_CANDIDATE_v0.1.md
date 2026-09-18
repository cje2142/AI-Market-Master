# AI Market Master 3.2 — Data Efficiency Candidate v0.1

Version: v0.1
Status: FROZEN RESEARCH CANDIDATE / PROSPECTIVE VALIDATION ONLY
Date Frozen: 2026-09-18

## 1. Authority Boundary
This file is NOT an official 3.2 scoring authority.

Official authority remains:
- Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md
- Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md
- Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md

No official C1-C8 formula, regime authority, portfolio action authority, or runtime authority is modified by this candidate.

Purpose:
- reduce recurring data-collection burden,
- improve data availability,
- reduce redundant or low-uniqueness inputs,
- preserve the decision-relevant information content of official 3.2,
- prospectively compare this candidate against official 3.2 before any authority change.

## 2. Design Principles
1. Same timestamp / same raw-data snapshot for Official and Candidate whenever possible.
2. No hidden numeric weights.
3. Missing values are never treated as zero or Neutral.
4. Same underlying datum must not be double-counted across components.
5. DIRECT authoritative data is preferred.
6. VALIDATED SUBSTITUTE may be numeric only after equivalence validation.
7. PROXY remains Context/Confirmation only.
8. Official 3.2 remains the production reference until prospective validation passes.
9. Candidate simplification must be evaluated by decision contribution × reliability × substitutability × uniqueness.

## 3. Candidate Top-Level Weights
Official C8 numeric weight is removed from this candidate and the original C1-C7 relative weights are renormalized by 1/0.93.

- C1 Smart Money: 19.35%
- C2 Program Flow: 12.90%
- C3 Breadth/Internal: 16.13%
- C4 Market Leadership/Rotation: 10.75%
- C5 Technical Structure: 21.51%
- C6 Liquidity/Macro: 10.75%
- C7 Volatility/Derivatives Risk: 8.60%
- C8 Global Leading: 0% numeric / Context only

Candidate global formula:

`SAI_DE_v0.1 =
0.1935*C1 +
0.1290*C2 +
0.1613*C3 +
0.1075*C4 +
0.2151*C5 +
0.1075*C6 +
0.0860*C7`

Rounding note:
The displayed weights are rounded. Runtime implementation should use exact renormalized weights derived from official C1-C7 base weights divided by 0.93 when feasible.

## 4. C1 Smart Money
Structure unchanged from official 3.2.

Cash:
`G_C=|P_C|+|F_C|+|I_C|`
`D_FC=F_C/G_C`
`A_C=clip((G_C/KTV)/0.05,0,+1)`
`FC=A_C*D_FC`

Futures:
`G_F=|P_F|+|F_F|+|I_F|`
`FF=F_F/G_F`

`C1=0.55*FC+0.45*FF`

Data plan:
- P_C/F_C/I_C: Kiwoom REST ka10051
- KTV: Kiwoom REST ka20003, KOSPI 001 traded value
- P_F/F_F/I_F: Kiwoom futures investor-flow source after HTS/API equivalence confirmation

Required unresolved acceptance tests:
- ka10051 amount-unit normalization vs HTS
- ka20003 KTV amount-unit normalization vs HTS
- futures investor-flow API/TR equivalence vs HTS [0780]

Until matched, affected axis remains PARTIAL or DATA UNAVAILABLE under candidate runtime rules.

## 5. C2 Program Flow
Structure unchanged from official 3.2.

`ARB_R=ARB/KTV`
`NONARB_R=NONARB/KTV`
`N_ARB=clip(ARB_R/0.030,-1,+1)`
`N_NONARB=clip(NONARB_R/0.100,-1,+1)`
`C2=0.25*N_ARB+0.75*N_NONARB`

Primary source:
- Kiwoom REST ka90005

Non-arbitrage remains structural core.
Total Program remains reconciliation/context only.

## 6. C3 Breadth / Internal
Structure unchanged from official 3.2.

`B_K=(ADV_K-DEC_K)/(ADV_K+DEC_K)`
`N_K=clip(B_K/0.40,-1,+1)`
`B_Q=(ADV_Q-DEC_Q)/(ADV_Q+DEC_Q)`
`N_Q=clip(B_Q/0.40,-1,+1)`
`C3=0.70*N_K+0.30*N_Q`

Primary source:
- Kiwoom REST ka20003
- KOSPI 001
- KOSDAQ 101

## 7. C4 Market Leadership / Rotation — Simplified
Official candidate sets are reduced to a fixed, API-efficient structure.

Comparator:
`r_K = KOSPI return`

Large-cap candidate axis:
- KOSPI200
- KRX100

`LC_RAW=average(r_KOSPI200,r_KRX100)-r_K`
`N_LC=clip(LC_RAW/0.005,-1,+1)`

Growth axis:
- KOSDAQ

`GR_RAW=r_KOSDAQ-r_K`
`N_GR=clip(GR_RAW/0.015,-1,+1)`

`C4=0.40*N_LC+0.60*N_GR`

Context / validation only:
- KOSPI100
- KTOP30
- KOSDAQ150

Completeness:
- VERIFIED: valid KOSPI, KOSPI200, KRX100, KOSDAQ
- PARTIAL: valid KOSPI + at least one large-cap candidate + KOSDAQ
- otherwise DATA UNAVAILABLE

Candidate comparison fields:
- C4_OFFICIAL
- C4_DE
- Delta_C4
- C4_DIRECTION_FLIP

Initial research thresholds:
- |Delta_C4| < 0.10: Equivalent
- 0.10 <= |Delta_C4| <= 0.20: Minor Difference
- |Delta_C4| > 0.20: Material Difference
- any sign flip across non-trivial values: Direction Flip flag

These thresholds are research diagnostics, not production action thresholds.

## 8. C5 Technical Structure
Structure unchanged from official 3.2.

`C5=0.55*TP+0.25*MOM+0.20*SES`

Source:
- KOSPI daily OHLCV / derived indicators
- MA20/50/60/200
- VWAP20/50/60/200
- RSI9
- MACD
- CLV
- daily KOSPI return

Official C5 missing-data and technical rules remain authoritative for this candidate unless explicitly revised in a later candidate version.

## 9. C6 Liquidity / Macro — Simplified
Candidate numeric axes:
- USD/KRW
- KTB3Y

`FX=-clip(r_USDKRW/0.008,-1,+1)`
`KTB=-clip(dKTB_bp/10,-1,+1)`

`C6=0.50*FX+0.50*KTB`

Context only:
- CD91
- customer deposits
- margin credit
- receivables
- futures deposits

Completeness:
- VERIFIED: FX + KTB3Y valid
- PARTIAL: exactly one valid axis; C6 equals the valid axis
- neither valid: DATA UNAVAILABLE

Candidate comparison fields:
- C6_OFFICIAL
- C6_DE
- Delta_C6

Special review cases:
- official CASH/CD91 materially changes official C6 direction,
- Candidate and Official C6 signs differ,
- omitted liquidity evidence precedes a material risk event.

## 10. C7 Volatility / Derivatives Risk
Structure unchanged from official 3.2.

`VOL=-clip(r_VKOSPI/0.10,-1,+1)`

`FLEAD_RAW=r_KOSPI200_Futures-r_KOSPI200_Spot`
`FLEAD=clip(FLEAD_RAW/0.005,-1,+1)`

`C7=0.70*VOL+0.30*FLEAD`

Primary data plan:
- VKOSPI: Kiwoom ka20003 KOSPI response row 603, subject to one-time HTS value acceptance test
- KOSPI200 futures: Kiwoom OpenAPI+
- KOSPI200 spot/index: Kiwoom market/index source

Context only:
- raw basis
- OI / Delta OI
- isolated PCR/strike data
- rollover/expiry positioning

## 11. C8 Global Leading — Shadow Context
C8 has zero numeric weight in this candidate.

Retain as Shadow Validation / Context:
- US Futures
- Prior US Close
- SOX
- Nikkei
- Shanghai / Shenzhen / Hang Seng
- Binance global / TradFi proxies where valid under BINANCE_RULE

Required shadow fields:
- C8_OFFICIAL
- C8_context_direction
- C8_conflict_flag
- C8_effect_on_official_vs_candidate

C8 must not be silently re-added numerically.

If C8 repeatedly provides useful independent risk warnings or recovery confirmation missed by the candidate, numeric removal must be reconsidered.

## 12. Candidate Missing-Data Rule
Usable = numeric VERIFIED or predefined PARTIAL component.

Candidate Global VERIFIED:
- C1-C7 all VERIFIED.

Candidate Global PARTIAL requires all:
1. C5 usable
2. C1 or C2 usable
3. C3 or C4 usable
4. C6 or C7 usable
5. at least 5 of 7 components usable
6. at least 70% of original Candidate weight coverage

When PARTIAL:
`SAI_DE_partial=sum(w_i*C_i for usable)/sum(w_i for usable)`

Log:
- missing_components
- original_candidate_weight_coverage
- effective_weight_after_missing
- missing_data_effect_vs_official

Missing-data renormalization is itself a validation target; it must not be assumed harmless.

## 13. Regime / Evidence Boundary
The official Adaptive Validation Rule remains unchanged.

Candidate scoring does NOT create a new Regime Engine.

Regime evaluation must preserve:
- independent Price/Structure axis,
- Money Flow/Internal axis,
- Risk/Environment axis,
- anti-double-counting,
- conflict resolution,
- transition detection,
- regime re-validation.

C8 remains E8 Context for adaptive qualitative interpretation even though its numeric Candidate weight is zero.

## 14. Official-vs-Candidate Comparison Protocol
Every prospective sample should use the same observation timestamp and raw snapshot when possible.

Required fields:
- Official C1-C8 and SAI
- Candidate C1-C7 and SAI_DE
- SAI_delta
- direction_agreement
- regime_agreement
- C4_delta
- C6_delta
- C8_effect
- missing_data_effect
- official_data_coverage
- candidate_data_coverage

Initial Material SAI Divergence diagnostic:
`|SAI_OFFICIAL-SAI_DE| >= 0.15`

The 0.15 threshold is provisional research-only and must not become a production action threshold without validation.

For each material divergence, attribute cause to:
- C4 simplification
- C6 simplification
- C8 numeric removal
- missing-data renormalization
- source/timestamp mismatch
- other / unknown

## 15. Outcome Horizons
Prospective outcomes:
- T+1 trading day
- T+5 trading days
- T+20 trading days

Track:
- KOSPI forward return
- forward drawdown where available
- risk-warning usefulness
- false warning
- recovery delay
- direction consistency
- data availability

This candidate is not a point-forecast model. Evaluation must emphasize risk timing, false-positive reduction, recovery delay, and robust availability.

## 16. Validation Gates
Stage 1:
- 20 prospective samples
- structural / implementation / missing-data validation
- no adoption decision

Stage 2:
- >=30 samples
- >=2 months
- early provisional comparison
- availability, SAI agreement, regime agreement, divergence attribution, warning quality

Stage 3:
- >=3 months
- target ~40 samples with meaningful regime diversity
- result must be one of:
  - PROVISIONAL ADOPT
  - CONTINUE VALIDATION
  - REJECT / REDESIGN

Stage 4:
- >=60 samples
- >=6 months
- only then may formal official scoring-authority integration be reviewed.

## 17. Freeze Rule
v0.1 is frozen as one prospective model.

During the validation window:
- do not tune weights sample-by-sample,
- do not add/remove inputs after seeing outcomes,
- do not change thresholds to improve observed results,
- do not backfill revised logic into earlier prospective samples.

Any substantive formula/input/weight change creates a new version and restarts or separately branches prospective validation.

## 18. Current Unresolved Acceptance Tests
Before treating runtime collection as fully automated:
1. ka10051 amount unit vs HTS
2. ka20003 KTV unit vs HTS
3. futures investor-flow API/TR vs HTS [0780]
4. ka20003 row 603 vs HTS VKOSPI
5. USD/KRW authoritative recurring source
6. KTB3Y authoritative recurring source

Failure of one acceptance test does not authorize an undocumented proxy. Use PARTIAL / DATA UNAVAILABLE / Context as defined.

## 19. Final State
Candidate name:
`AI Market Master 3.2 — Data Efficiency Candidate v0.1`

State:
`FROZEN / PROSPECTIVE VALIDATION READY`

Official 3.2 remains unchanged.
