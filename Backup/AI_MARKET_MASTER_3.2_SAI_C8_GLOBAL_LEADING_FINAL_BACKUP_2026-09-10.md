# AI Market Master 3.2 — SAI-C8 Global Leading Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression verification for the SAI-C8 Global Leading integration.

## 1. Integration Result
`SAI-C8 Global Leading` has been formally integrated into `SCORING_RULE` as the eighth numeric sub-component for a future Strategy Action Index.

Official global numeric state remains:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

C1-C8 now cover E1-E8 at component level only. Global aggregation, C1-C8 global Base Weights, global missing/partial handling, any Conditional Numeric Weight logic, final output range/Action Bands and regression validation are still required before global Strategy Action Index activation.

## 2. Six Official Authority Snapshot
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `fa51e24dd54bacc2c3aacc613f30ef6451a9e426`
   - C1-C8 numeric component authority
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`

Supporting files before final-backup registration:
- `VERSION_STATUS.md`: `8ce98f180d1a506ffe14663d78651eb528c7a322`
- `CHANGELOG.md`: `eec431b18f4ed42c3fb8503e0c197973a1171214`

## 3. C8 Numeric Structure
Five numeric axes:
- Global Equity Risk `GR`: 30%
- Korea Leading `KR`: 25%
- Semiconductor Risk `SEMI`: 20%
- Global Rate/Liquidity `GLIQ`: 15%
- Crypto Risk `CRYPTO`: 10%

Full formula:
`SAI-C8 = 0.30*GR + 0.25*KR + 0.20*SEMI + 0.15*GLIQ + 0.10*CRYPTO`
Range: `[-1.00,+1.00]`.

## 4. Canonical Symbol / Composite Rules
- GR = SPYUSDT + QQQUSDT composite
- KR = EWYUSDT
- SEMI = SOXLUSDT
- GLIQ = TMFUSDT
- CRYPTO = BTCUSDT
- SAMSUNGUSDT / SKHYNIXUSDT = G2/G3 confirmation only, not extra numeric axes

The fixed 8-symbol Binance Engine remains unchanged and still queries:
`EWYUSDT / SAMSUNGUSDT / SKHYNIXUSDT / SOXLUSDT / QQQUSDT / SPYUSDT / TMFUSDT / BTCUSDT`.

## 5. Normalization
Aligned return window required. For Binance numeric inputs, use same-query rolling 24h return or equivalently computed aligned 24h return.

`N_SPY = clip(r_SPY/0.015,-1,+1)`
`N_QQQ = clip(r_QQQ/0.020,-1,+1)`
`GR = 0.50*N_SPY + 0.50*N_QQQ`

`KR = clip(r_EWY/0.025,-1,+1)`
`SEMI = clip(r_SOXL/0.050,-1,+1)`
`GLIQ = clip(r_TMF/0.030,-1,+1)`
`CRYPTO = clip(r_BTC/0.040,-1,+1)`

These thresholds and 30/25/20/15/10 weights are v1 design calibrations, not claims of empirical backtest optimization.

## 6. Missing / Partial Gate
Full VERIFIED eligibility requires:
- all five axes valid
- GR uses both SPY and QQQ
- source/window/freshness validation passes

Predefined partial formula:
`C8_partial = sum(w_i*X_i for valid axes) / sum(w_i for valid axes)`

PARTIAL requires all:
1. GR available;
2. at least 3 of 5 axes valid;
3. original fixed-weight coverage >=60%;
4. no STALE input used numerically.

Additional rules:
- one-of-two SPY/QQQ GR is allowed only as PARTIAL
- any valid Binance FALLBACK input caps C8 at PARTIAL and preserves the required Confidence downgrade
- GR missing, fewer than 3 axes, coverage <60%, or STALE-only completion -> DATA UNAVAILABLE
- missing values are never zero/Neutral.

## 7. Freshness Boundary
BINANCE_RULE remains authority:
- LIVE -> normal numeric eligibility
- FALLBACK -> only inside official TTL/eligibility; C8 capped PARTIAL
- STALE -> numeric C8 prohibited, historical context only

No C8 rule overrides Binance query/requery, field-depth, fallback or stale restrictions.

## 8. Positioning / Confirmation Boundary
Not direct numeric C8 terms:
- SAMSUNGUSDT / SKHYNIXUSDT returns
- OI / OI change
- Funding
- Global/Top-Trader Long/Short ratios
- Premium / Mark-Index spread
- ADL risk
- Order book / recent trades

These remain G2/G3/G6 confirmation, crowding and positioning context.

## 9. Conflict / Shock
`C8 Conflict: ACTIVE` includes:
- GR vs KR opposite and both |value|>=0.50
- GR vs SEMI opposite and both |value|>=0.50

`C8 Korea Confirmation Conflict: ACTIVE` when EWY materially conflicts with both available Samsung/SK hynix confirmation signals.

`C8 Semiconductor Confirmation Conflict: ACTIVE` when SOXL materially conflicts with both available Samsung/SK hynix confirmation signals.

`C8 Shock: ACTIVE` when:
- GR, KR and SEMI all <=-0.80, or
- GR, KR and SEMI all >=+0.80, or
- comparable extreme aligned global-leading movement is independently confirmed by G6 positioning/crowding evidence.

Flags feed Change Detection / Transition / Regime re-validation only. No automatic Regime, global SAI, portfolio action or permanent Base Weight change.

## 10. Anti-Double-Counting / Anti-Circularity
- SPY and QQQ -> one GR composite
- EWY scored once as KR
- SOXL scored once as SEMI
- TMF scored once as GLIQ
- BTC scored once as CRYPTO and limited to 10% internal C8 weight
- Samsung/SK hynix remain confirmation only
- G6 positioning remains context only
- C6 Korea Treasury 3Y remains domestic and is not re-added
- C7 domestic volatility/derivatives are not re-added
- C4 domestic sector breadth and AI Cycle fundamentals are not re-added
- five C8 axes remain one E8 Evidence Group for adaptive consensus counting
- C8 cannot select a Regime, use that Regime to alter itself, then use altered C8 as sole reconfirmation
- VH/H/M/L remains qualitative only.

## 11. Regression / Validation Cases
A. all five axes +1 -> +1.00 PASS
B. all five axes -1 -> -1.00 PASS
C. GR positive / KR+SEMI negative -> aggregate retained + conflict PASS
D. GR+KR+SEMI only -> 75% coverage -> PARTIAL PASS
E. KR+SEMI+GLIQ+CRYPTO without GR -> DATA UNAVAILABLE PASS
F. GR+KR only -> DATA UNAVAILABLE PASS
G. one SPY/QQQ missing -> GR single-index fallback + overall PARTIAL PASS
H. valid FALLBACK -> numeric permitted, C8 PARTIAL + Confidence downgrade PASS
I. STALE -> numeric prohibited PASS
J. Samsung/SKH disagreement -> confirmation conflict only PASS

C1-C7 regression boundary review: PASS. Existing formulas/missing rules/flags remain defined and no C8 input is silently inserted into C1-C7.

## 12. Cross-Authority Verification
- MASTER_RULE: PASS — six-authority architecture, HTS/KRX final confirmation, Binance supporting role and 24 engines preserved.
- DASHBOARD_RULE: PASS — exactly 8 dashboard categories preserved; Global Leading remains mapped inside existing categories.
- TECHNICAL_RULE: PASS — technical authority unchanged; Global Leading remains confirmation input only.
- BINANCE_RULE: PASS — fixed 8 symbols, G1-G6, LIVE/FALLBACK/STALE, freshness and positioning ownership preserved.
- ADAPTIVE_VALIDATION_RULE: PASS — E8 remains qualitative/adaptive owner; VH/H/M/L remains non-numeric; C8 is one E8 family.
- SCORING_RULE: PASS — sole numeric authority; C1-C8 component formulas defined; global scores remain DATA UNAVAILABLE.

## 13. Final State
- C1-C8 component formulas: VERIFIED BY RULE DESIGN
- Global AI Master Score: DATA UNAVAILABLE
- Global Strategy Action Index: DATA UNAVAILABLE
- 24 Engines: unchanged
- 8 Dashboard categories: unchanged
- 6 official authority files: unchanged in count
- unresolved authority conflict: NONE

Final seal principle:
`E1-E8 component coverage complete != global Strategy Action Index activated`.

Reliability > Speed.