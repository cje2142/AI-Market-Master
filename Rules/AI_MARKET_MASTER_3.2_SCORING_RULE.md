# AI Market Master 3.2 Scoring Rule

Version: 3.2 Unified Stable
Status: Scoring Authority / HTS-Operational v2

## 1. Scope / Official State
This file is the sole authority for numeric `Strategy Action Index` and any future `AI Master Score` formulas, inputs, normalization, weights, missing-data handling, conflict/shock logic and regression requirements.

Official state:
- `Strategy Action Index: FORMULA ACTIVATED / RUNTIME DATA-DEPENDENT`
- `AI Master Score: DATA UNAVAILABLE`

HTS/KRX remains final Korean-market confirmation. Missing values are never zero/Neutral. VH/H/M/L, Regime labels, qualitative Strategy posture and signal counts never become hidden numeric weights.

## 2. v2 Operational Design
C1-C8 v2 uses data the user can repeatedly export from HTS. Ownership remains E1-E8; numeric C1-C8 do not create new Evidence Groups.

- C1/E1 Smart Money
- C2/E2 Program Flow
- C3/E3 Breadth/Internal
- C4/E4 Market Leadership/Rotation numeric proxy; full sector interpretation remains qualitative E4 context
- C5/E5 Technical Structure
- C6/E6 Liquidity/Macro
- C7/E7 Volatility/Derivatives Risk
- C8/E8 Global Leading

Same underlying data must not be counted as independent confirmation across components.

# SAI-C1 Smart Money v2

## 3. Inputs / Formula
Cash rows: Individual `P_C`, Foreign `F_C`, Institution-total `I_C`, plus KOSPI traded value `KTV` in a matched currency unit.
Futures rows: Individual `P_F`, Foreign `F_F`, Institution-total `I_F`.

`G_C=|P_C|+|F_C|+|I_C|`
`D_FC=F_C/G_C`
`A_C=clip((G_C/KTV)/0.05,0,+1)`
`FC=A_C*D_FC`

The activity multiplier prevents tiny absolute cash flows from producing a large Smart Money score merely because Foreign dominates a very small participant-flow denominator.

`G_F=|P_F|+|F_F|+|I_F|`
`FF=F_F/G_F`

Require positive denominators and matched units where applicable.

`SAI-C1=0.55*FC+0.45*FF`
Range `[-1,+1]`.

Financial Investment/Trust/Pension and other institution sub-rows remain context because they are already inside Institution-total. Futures OI is not mixed with futures net-flow units.

## 4. Missing / Conflict / Shock
- cash axis FC + futures axis FF valid -> VERIFIED
- only one valid -> C1 equals valid axis / PARTIAL
- neither valid -> DATA UNAVAILABLE

`C1 Low Activity: ACTIVE` when `G_C/KTV<2%`; this is disclosed and prevents cash flow from acting as a sole Shock trigger.

`C1 Conflict: ACTIVE` when FC and FF oppose and both `|value|>=0.35`.
`C1 Shock: ACTIVE` when FC/FF share direction, one `|value|>=0.65`, other `|value|>=0.45`.
A single `|value|>=0.75` without same-direction confirmation is `C1 Shock Watch` only.

# SAI-C2 Program Flow v2

## 5. Formula
Convert Arbitrage `ARB`, Non-Arbitrage `NONARB`, KOSPI traded value `KTV` to the same unit.

`ARB_R=ARB/KTV`
`NONARB_R=NONARB/KTV`
`N_ARB=clip(ARB_R/0.030,-1,+1)`
`N_NONARB=clip(NONARB_R/0.100,-1,+1)`
`SAI-C2=0.25*N_ARB+0.75*N_NONARB`

Non-Arbitrage is structural core; Total Program is reconciliation/context only.

## 6. Missing / Conflict / Shock / Mechanical
- ARB+NONARB valid -> VERIFIED
- ARB missing -> `C2=N_NONARB` / PARTIAL
- NONARB missing or KTV invalid -> DATA UNAVAILABLE

Conflict: opposite N_ARB/N_NONARB and both `|N|>=0.30`.
Shock: `|NONARB_R|>=10%`, or same direction and both `|N|>=0.75`.
Expiry/index/sector/ETF rebalance or comparable distortion -> `C2 Mechanical Event: ACTIVE`. Event-sensitive Shock cannot alone reweight numerically without structural confirmation.

# SAI-C3 Breadth / Internal v2

## 7. Formula
`B_K=(ADV_K-DEC_K)/(ADV_K+DEC_K)`
`N_K=clip(B_K/0.40,-1,+1)`
`B_Q=(ADV_Q-DEC_Q)/(ADV_Q+DEC_Q)`
`N_Q=clip(B_Q/0.40,-1,+1)`
`SAI-C3=0.70*N_K+0.30*N_Q`

KOSPI breadth is mandatory; KOSDAQ is confirmation. Unchanged counts and absolute ADL are context only.

## 8. Missing / Flags
- KOSPI+KOSDAQ valid -> VERIFIED
- KOSPI only -> `C3=N_K` / PARTIAL
- KOSPI invalid -> DATA UNAVAILABLE

Conflict: N_K/N_Q opposite and both `|N|>=0.30`.
Divergence: KOSPI return >0 with `N_K<=-0.30`, or <0 with `N_K>=+0.30`.
Shock: `|B_K|>=0.60`, or same-direction KOSPI/KOSDAQ breadth both `|B|>=0.50`.

# SAI-C4 Market Leadership / Rotation v2

## 9. Inputs / Formula
KOSPI return `r_K` is comparator.
Large-cap candidates: KOSPI100, KOSPI200, KTOP30, KRX100.
Growth candidates: KOSDAQ, KOSDAQ150.

`LC_RAW=average(valid large-cap returns)-r_K`
`N_LC=clip(LC_RAW/0.005,-1,+1)`
`GR_RAW=average(valid growth returns)-r_K`
`N_GR=clip(GR_RAW/0.015,-1,+1)`
`SAI-C4=0.40*N_LC+0.60*N_GR`

Positive C4 means relative leadership/rotation support, not broad-market bullishness by itself. Full sector leadership remains qualitative E4 context.

## 10. Completeness / Flags
VERIFIED: valid KOSPI + >=3/4 large-cap candidates + both growth candidates.
PARTIAL: valid KOSPI + >=2/4 large-cap candidates + >=1 growth candidate.
If either LC or GR cannot be formed -> DATA UNAVAILABLE.

Conflict: N_LC/N_GR opposite and both `|N|>=0.40`.
Shock: same direction and both `|N|>=0.75`.

# SAI-C5 Technical Structure v2

## 11. Axes
Official timeframe: KOSPI Daily / closing-confirmed. Intraday data is preview only.

- Trend Position `TP` 55%
- Momentum `MOM` 25%
- Session Structure `SES` 20%

ADX, volume, Elliott/Fibonacci, support/resistance and Ichimoku remain validation/context unless used by explicit structural Shock logic under TECHNICAL_RULE.

## 12. Trend Position
Anchors: MA20/50/60/200 and VWAP20/50/60/200.
For each A: Close > A*1.002 => +1; Close < A*0.998 => -1; otherwise 0.
`TP=average(valid anchor scores)`.
6-8 anchors = full TP; 4-5 = usable PARTIAL; <4 = unavailable.

## 13. Momentum
`RSI_N=clip((RSI9-50)/20,-1,+1)`.
MACD direction: +1 when MACD>Signal and Oscillator>0; -1 when MACD<Signal and Oscillator<0; else 0.
`MOM=0.50*RSI_N+0.50*MACD_D`.
Both families required for full MOM; one available may be used but C5 becomes PARTIAL.

## 14. Session Structure
Require High>Low and valid daily KOSPI return `r_K`.
`CLV=clip(2*(Close-Low)/(High-Low)-1,-1,+1)`
`DAY=clip(r_K/0.015,-1,+1)`
`SES=0.60*CLV+0.40*DAY`

## 15. Formula / Missing / Flags
`SAI-C5=0.55*TP+0.25*MOM+0.20*SES`
Range `[-1,+1]`.

VERIFIED requires full TP + full MOM + SES.
PARTIAL:
- MOM missing -> `(0.55*TP+0.20*SES)/0.75`
- SES missing -> `(0.55*TP+0.25*MOM)/0.80`
- TP only 4-5 anchors, or MOM single-family fallback -> same available formula / PARTIAL
TP unavailable, or MOM+SES both unavailable -> DATA UNAVAILABLE.

Conflict: TP opposes MOM or SES and both `|value|>=0.50`.
Shock: TECHNICAL_RULE confirms major closing support breakdown/resistance breakout including close below 5,593, or `|r_K|>=2.5%` with same-direction `|CLV|>=0.50`.

# SAI-C6 Liquidity / Macro v2

## 16. Formula
`FX=-clip(r_USDKRW/0.008,-1,+1)`.

Use HTS absolute rate `대비` in percentage points:
`dKTB_bp=100*Delta_KTB3Y_percentage_points`
`dCD_bp=100*Delta_CD91_percentage_points`
`KTB=-clip(dKTB_bp/10,-1,+1)`
`CD=-clip(dCD_bp/5,-1,+1)`
Full `RATE=0.70*KTB+0.30*CD`.
One rate axis may stand in for RATE but forces PARTIAL.

`DEP5=Deposit_t/Deposit_t-5obs-1`
`CASH=clip(DEP5/0.05,-1,+1)`

`SAI-C6=0.35*FX+0.35*RATE+0.30*CASH`

## 17. Missing / Flags
VERIFIED requires FX + full RATE + CASH.
PARTIAL requires >=2 of FX/RATE/CASH and at least one of FX/RATE; renormalize original 0.35/0.35/0.30 weights across valid top-level axes. Single-rate RATE forces PARTIAL.
Otherwise DATA UNAVAILABLE.

Margin Credit, receivables, futures deposits are context/risk flags only.
Conflict: any two top-level axes oppose and both `|value|>=0.50`.
Shock: `|r_USDKRW|>=1.2%`, `|dKTB_bp|>=15bp`, `|dCD_bp|>=8bp`, or `|DEP5|>=7.5%`.

# SAI-C7 Volatility / Derivatives Risk v2

## 18. Formula
`VOL=-clip(r_VKOSPI/0.10,-1,+1)`
`FLEAD_RAW=r_KOSPI200_Futures-r_KOSPI200_Spot`
`FLEAD=clip(FLEAD_RAW/0.005,-1,+1)`
`SAI-C7=0.70*VOL+0.30*FLEAD`

FLEAD is same-session futures-vs-spot directional lead, not fair-value basis.

## 19. Missing / Context / Flags
VOL+FLEAD -> VERIFIED; VOL only -> `C7=VOL` / PARTIAL; VOL missing -> DATA UNAVAILABLE.

Context only: raw basis without fair basis, OI snapshot without change, isolated Call/Put strike, PCR without full-market data, volatility futures/term structure, rollover/expiry positioning.

Conflict: VOL/FLEAD oppose and both `|value|>=0.50`.
Shock: `|r_VKOSPI|>=15%`, or same-direction VOL/FLEAD both `|value|>=0.80`.
Expiry/rollover/rebalance distortion -> `C7 Mechanical Event: ACTIVE`; event-sensitive Shock cannot alone trigger adaptive numeric reweighting.

# SAI-C8 Global Leading v2

## 20. Source Boundary
Primary numeric source is the recurring HTS global-market panel. Binance remains supporting/confirmation under BINANCE_RULE and is not required or silently re-added to numeric C8 v2.

Top-level axes:
- US Futures `USF` 40%
- Prior US Close `USC` 25%
- SOX Semiconductor `SEMI` 20%
- Asia `ASIA` 15%

WTI, Gold, DAX/CAC and Binance positioning are context unless a future explicit scoring revision adopts them.

## 21. US Futures / Prior Close
`SPF=clip(r_MiniSP500/0.0075,-1,+1)`
`NQF=clip(r_MiniNASDAQ/0.010,-1,+1)`
Both -> `USF=0.45*SPF+0.55*NQF`; one -> axis usable but C8 PARTIAL.

`SPX=clip(r_SP500/0.015,-1,+1)`
`NAS=clip(r_NASDAQ/0.020,-1,+1)`
Both -> `USC=0.50*SPX+0.50*NAS`; one -> axis usable but C8 PARTIAL.

Current futures and prior close retain separate timestamps/time layers.

## 22. Semiconductor / Asia
`SEMI=clip(r_SOX/0.025,-1,+1)`.

`N_NIK=clip(r_Nikkei225/0.015,-1,+1)`
`N_SHA=clip(r_Shanghai/0.015,-1,+1)`
`N_SZX=clip(r_Shenzhen/0.020,-1,+1)`
`N_HSI=clip(r_HangSeng/0.020,-1,+1)`

CHINA/HK base weights: Shanghai 25%, Shenzhen 25%, Hang Seng 50%; renormalize only across valid members.
Nikkei + CHINA -> `ASIA=0.40*N_NIK+0.60*CHINA`.
One side only may be used but forces C8 PARTIAL.

## 23. Formula / Completeness / Flags
`SAI-C8=0.40*USF+0.25*USC+0.20*SEMI+0.15*ASIA`
Range `[-1,+1]`.

VERIFIED requires both US futures, both prior US closes, SOX, and Nikkei + >=2 of Shanghai/Shenzhen/Hang Seng, with valid timestamps/session labels.

PARTIAL requires USF + >=3/4 top-level axes + >=65% original C8 weight coverage + known timestamps. Use `C8_partial=sum(w_i*X_i)/sum(w_i)` across valid axes. Any one-member composite fallback forces PARTIAL. Otherwise DATA UNAVAILABLE.

Conflict: USF/USC opposite and both `|value|>=0.40`, or USF/SEMI opposite and both `|value|>=0.50`.
Shock: USF/USC/SEMI same direction all `|value|>=0.75`, or USF/SEMI/ASIA same direction all `|value|>=0.80`.

C8 is one E8 family. SOX is scored once here. C4/C6/C7 are not re-added. Binance EWY/SOXL/SPY/QQQ/TMF/BTC and G6 fields remain confirmation/context only.

# Global Strategy Action Index v2

## 24. Base Weights / Formula
Base Weights remain:
C1 18%, C2 12%, C3 15%, C4 10%, C5 20%, C6 10%, C7 8%, C8 7%.

`SAI_Base=0.18*C1+0.12*C2+0.15*C3+0.10*C4+0.20*C5+0.10*C6+0.08*C7+0.07*C8`
Range `[-1,+1]`.

Families: Flow C1+C2=30%; Internal C3+C4=25%; Structure C5=20%; Environment C6+C7+C8=25%.
Weights are rule-design calibrations, not empirically optimized estimates.

## 25. Global VERIFIED / PARTIAL Gate
Usable = component returns valid numeric VERIFIED or predefined PARTIAL.
Global VERIFIED requires C1-C8 all VERIFIED.

Global PARTIAL:
`SAI_Partial=sum(w_i*C_i for usable)/sum(w_i for usable)`
requires all:
1. C5 usable
2. C1 or C2 usable
3. C3 or C4 usable
4. C6 or C7 or C8 usable
5. >=6/8 components usable
6. >=70% original Base Weight coverage

Any component PARTIAL forces global PARTIAL. Failed gate -> `Strategy Action Index: DATA UNAVAILABLE`. Adaptive numeric reweighting is prohibited in PARTIAL mode.

## 26. Family Scores / Global Conflict
Only with all C1-C8 VERIFIED:
`F_FLOW=0.60*C1+0.40*C2`
`F_INTERNAL=0.60*C3+0.40*C4`
`F_STRUCTURE=C5`
`F_ENV=0.40*C6+0.32*C7+0.28*C8`

These are helper aggregates, not new Evidence Groups.
`Global SAI Conflict: ACTIVE` when any two family scores oppose and both `|F|>=0.50`.
Conflict keeps Base SAI, blocks adaptive weighting, must be disclosed, and prevents near-zero from being interpreted as absence of information.

## 27. Conditional Adaptive Weight
Eligibility: all C1-C8 VERIFIED, no Global SAI Conflict, validated Shock + independent confirmation, no sole mechanical-event distortion.

Flow Event: C1/C2 same direction, one Shock, other `|C|>=0.50`.
Internal Event: C3/C4 same direction, one Shock, other `|C|>=0.50`.
Structure Event: C5 Shock + FLOW/INTERNAL/ENV same direction with `|F|>=0.50`.
Environment Event: >=2 of C6/C7/C8 same direction and both `|C|>=0.50`, one Shock.

Adjustment:
- none -> Base
- exactly one family -> +5pp to active family; other three reduced proportionally
- exactly two same direction -> +3pp each; other two reduced proportionally
- exactly two opposite -> Adaptive BLOCKED / Base retained
- 3+ families -> Base retained + `Broad Market Shock: ACTIVE`
- max total reallocation 6pp; component ratios inside family fixed; all weights non-negative and total 1.00

`SAI_Final=sum(adjusted_weight_i*C_i)` when valid; otherwise Base/Partial applies.

Anti-circularity order:
`C1-C8 -> Base SAI -> Preliminary Regime -> Adaptive Validation / Transition / Conflict -> Regime Re-validation -> Conditional Adaptive Event -> Final SAI -> Strategy / Portfolio Response`.
Final SAI cannot solely reconfirm the Regime that caused its context.

## 28. Action Bands / Safety
- +0.60 to +1.00 -> Strong Positive Execution Bias
- +0.30 to <+0.60 -> Positive Execution Bias
- >-0.30 to <+0.30 -> Balanced / Hold Bias
- >-0.60 to <=-0.30 -> Negative Execution Bias
- -1.00 to <=-0.60 -> Strong Negative Execution Bias

These are execution-bias labels, not automatic orders. They never override Regime/Transition, material Conflict, C5 technical location, HTS/KRX confirmation, portfolio exposure/concentration, Extreme Risk controls or Binance freshness restrictions. PARTIAL SAI alone cannot authorize strongest aggressive action.

## 29. Runtime Procedure
1. Parse/unit-validate recurring HTS input.
2. Calculate C1-C8 from v2 owning formulas.
3. Record status and Conflict/Shock/Mechanical/Low-Activity flags.
4. Apply global gate.
5. PARTIAL -> calculate only SAI_Partial; no adaptive numeric weighting.
6. VERIFIED -> calculate SAI_Base + family scores + Global Conflict.
7. Run Preliminary Regime -> Adaptive Validation -> Transition/Conflict -> Regime re-validation.
8. Test Conditional Adaptive Events only after re-validation.
9. Calculate SAI_Final, constrain round-off to [-1,+1], assign Action Band.
10. Display value, status, Base/Adaptive mode and material flags.
11. Final portfolio action remains MASTER_RULE + ADAPTIVE_VALIDATION_RULE, not score-only execution.

## 30. Regression / Sample Validation
Mathematical invariants:
- component formulas bounded [-1,+1]
- Base weights and family weights sum 1.00
- all allowed one/two-family reallocations remain non-negative and sum 1.00
- all 256 C1-C8 {-1,+1} corner combinations remain inside [-1,+1]
- Missing never equals Neutral
- PARTIAL cannot use adaptive weights

Provided 2026-09-10 HTS sample produces approximately:
C1 -0.61, C2 -0.68, C3 -0.03, C4 +0.51, C5 +0.52, C6 -0.23, C7 +0.33, C8 -0.12, Base SAI about -0.05.

Interpretation: Balanced/Hold arithmetic with material internal tension—negative Smart Money/Non-Arbitrage versus positive technical recovery/rotation/volatility normalization. Conflict/Transition review remains mandatory. This is formula sanity validation, not a performance backtest.

## 31. Calibration Boundary
C1-C8 v2 and Global SAI are `VERIFIED BY RULE DESIGN` when data gates pass.
Not empirically optimized: normalization thresholds, Shock thresholds, internal weights, Global Base Weights, Action Bands and the C1 5% cash-activity saturation threshold.

## 32. Final Principle
Use repeatable, validated HTS-native inputs. Do not demand unavailable theoretical inputs when a reproducible formulation exists; do not substitute convenience for validation.

Strategy Action Index = execution bias, not automatic trade.
AI Master Score remains DATA UNAVAILABLE.
Adaptive priority != numeric weight.
Conflict is information, not noise.
Reliability > Speed.