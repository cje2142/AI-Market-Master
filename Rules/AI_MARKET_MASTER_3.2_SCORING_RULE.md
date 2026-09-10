# AI Market Master 3.2 Scoring Rule

Version: 3.2 Unified Stable
Status: Scoring Authority / HTS-Operational v2

## 1. Scope
This file is the sole authority for numeric `Strategy Action Index` and any future `AI Master Score` formulas, inputs, normalization, weights, missing-data handling, conflict/shock logic and regression requirements.

Official state:
- `Strategy Action Index: FORMULA ACTIVATED / RUNTIME DATA-DEPENDENT`
- `AI Master Score: DATA UNAVAILABLE`

HTS/KRX remains the final Korean-market confirmation source under MASTER_RULE. Missing values are never converted to zero/Neutral. VH/H/M/L, Regime labels, qualitative Strategy posture and raw signal counts are never converted into hidden numeric weights.

## 2. v2 Operational Design Principle
C1-C8 v2 uses data that the user can repeatedly export from HTS. The goal is operational reproducibility without weakening validation.

Component ownership:
- C1 / E1: Smart Money
- C2 / E2: Program Flow
- C3 / E3: Breadth / Internal
- C4 / E4: Market Leadership / Rotation numeric proxy; full sector interpretation remains qualitative E4 context
- C5 / E5: Technical Structure
- C6 / E6: Liquidity / Macro
- C7 / E7: Volatility / Derivatives Risk
- C8 / E8: Global Leading

The same underlying datum must not be counted as independent confirmation across multiple components.

# SAI-C1 Smart Money v2

## 3. Inputs / Formula
Use the HTS investor-flow panel for KOSPI cash and KOSPI futures.

Required cash rows:
- Individual KOSPI net flow `P_C`
- Foreign KOSPI net flow `F_C`
- Institution-total KOSPI net flow `I_C`

Required futures rows:
- Individual futures net flow `P_F`
- Foreign futures net flow `F_F`
- Institution-total futures net flow `I_F`

`G_C = |P_C| + |F_C| + |I_C|`
`D_FC = F_C / G_C`

`G_F = |P_F| + |F_F| + |I_F|`
`D_FF = F_F / G_F`

Require positive denominators.

`SAI-C1 = 0.55*D_FC + 0.45*D_FF`
Range `[-1,+1]`.

This avoids mixing futures net-flow units with futures OI contract units. Financial Investment, Trust, Pension and other institution sub-rows are context only because they are already included inside Institution-total.

## 4. Missing / Conflict / Shock
- Cash + futures axes valid -> VERIFIED.
- only one axis valid -> C1 equals that valid axis / PARTIAL.
- neither valid or denominator invalid -> DATA UNAVAILABLE.

`C1 Conflict: ACTIVE` when D_FC and D_FF have opposite signs and both `|D|>=0.35`.

`C1 Shock: ACTIVE` when cash and futures are same direction, one has `|D|>=0.65` and the other `|D|>=0.45`.
A single `|D|>=0.75` without same-direction confirmation is a `C1 Shock Watch`, not an adaptive reweight trigger.

# SAI-C2 Program Flow v2

## 5. Inputs / Formula
Inputs must be converted to the same currency unit:
- Arbitrage net `ARB`
- Non-Arbitrage net `NONARB`
- KOSPI traded value `KTV`

`ARB_R = ARB / KTV`
`NONARB_R = NONARB / KTV`

`N_ARB = clip(ARB_R/0.030,-1,+1)`
`N_NONARB = clip(NONARB_R/0.100,-1,+1)`

`SAI-C2 = 0.25*N_ARB + 0.75*N_NONARB`
Range `[-1,+1]`.

Non-Arbitrage remains structural core. Total Program is reconciliation/context only.

## 6. Missing / Conflict / Shock / Mechanical Event
- ARB + NONARB valid -> VERIFIED.
- ARB missing, NONARB valid -> `C2=N_NONARB` / PARTIAL.
- NONARB missing or KTV invalid -> DATA UNAVAILABLE.

`C2 Conflict: ACTIVE` when N_ARB and N_NONARB oppose and both `|N|>=0.30`.

`C2 Shock: ACTIVE` when `|NONARB_R|>=10%`, or N_ARB/N_NONARB have the same direction and both `|N|>=0.75`.

Expiry, major index/sector rebalance, ETF rebalance or comparable mechanical distortion -> `C2 Mechanical Event: ACTIVE`.
Mechanical Event does not erase C2, but event-sensitive C2 Shock cannot by itself trigger adaptive numeric reweighting without structural confirmation.

# SAI-C3 Breadth / Market Internal v2

## 7. Formula
Required KOSPI breadth: `ADV_K`, `DEC_K`.
Optional KOSDAQ confirmation: `ADV_Q`, `DEC_Q`.
Unchanged counts are context only.

`B_K=(ADV_K-DEC_K)/(ADV_K+DEC_K)`
`N_K=clip(B_K/0.40,-1,+1)`

`B_Q=(ADV_Q-DEC_Q)/(ADV_Q+DEC_Q)`
`N_Q=clip(B_Q/0.40,-1,+1)`

`SAI-C3=0.70*N_K+0.30*N_Q`
Range `[-1,+1]`.

ADL absolute level is context only because advance/decline participation is already scored here.

## 8. Missing / Conflict / Divergence / Shock
- KOSPI + KOSDAQ valid -> VERIFIED.
- KOSPI valid, KOSDAQ missing -> `C3=N_K` / PARTIAL.
- KOSPI missing or `ADV_K+DEC_K<=0` -> DATA UNAVAILABLE.

`C3 Conflict: ACTIVE` when N_K/N_Q oppose and both `|N|>=0.30`.
`C3 Divergence: ACTIVE` when KOSPI return is positive with `N_K<=-0.30`, or negative with `N_K>=+0.30`.
`C3 Shock: ACTIVE` when `|B_K|>=0.60`, or KOSPI/KOSDAQ breadth share the same direction and both `|B|>=0.50`.

# SAI-C4 Market Leadership / Rotation v2

## 9. Purpose / Inputs
C4 numeric v2 measures recurring market-segment leadership and rotation using HTS index returns rather than requiring eight sector benchmark returns that are not repeatably supplied.

KOSPI return `r_K` is the comparator.
Large-cap candidates:
- KOSPI100
- KOSPI200
- KTOP30
- KRX100

Growth/rotation candidates:
- KOSDAQ
- KOSDAQ150

Full sector-level leadership remains qualitative/contextual under E4 and may supplement judgment but is not required for numeric C4.

## 10. Formula
`LC_RAW = average(valid large-cap returns) - r_K`
`N_LC = clip(LC_RAW/0.005,-1,+1)`

`GR_RAW = average(valid growth returns) - r_K`
`N_GR = clip(GR_RAW/0.015,-1,+1)`

`SAI-C4 = 0.40*N_LC + 0.60*N_GR`
Range `[-1,+1]`.

Positive C4 means relative leadership/rotation support; it is not by itself a broad-market bullish signal.

## 11. Completeness / Conflict / Shock
VERIFIED requires:
- valid KOSPI comparator;
- at least 3 of 4 large-cap candidates;
- both KOSDAQ and KOSDAQ150.

PARTIAL requires:
- valid KOSPI comparator;
- at least 2 of 4 large-cap candidates;
- at least one growth candidate.

If either LC or GR axis cannot be formed -> DATA UNAVAILABLE.

`C4 Conflict: ACTIVE` when N_LC and N_GR oppose and both `|N|>=0.40`.
`C4 Shock: ACTIVE` when N_LC/N_GR share direction and both `|N|>=0.75`.

# SAI-C5 Technical Structure v2

## 12. Timeframe / Inputs
Official C5 v2 = KOSPI Daily / closing-confirmed.
Intraday data is preview only.

Numeric axes:
- Trend Position `TP` 55%
- Momentum `MOM` 25%
- Session Structure `SES` 20%

ADX, volume, Elliott/Fibonacci, support/resistance and Ichimoku remain validation/context under TECHNICAL_RULE unless explicitly used by a defined Shock flag.

## 13. Trend Position
Fixed recurring anchors:
- MA20, MA50, MA60, MA200
- VWAP20, VWAP50, VWAP60, VWAP200

For each valid anchor A:
- `Close > A*1.002` -> +1
- `Close < A*0.998` -> -1
- otherwise 0

`TP = average(valid anchor scores)`.

6-8 anchors -> full TP.
4-5 anchors -> usable TP but C5 cannot be VERIFIED.
<4 anchors -> TP unavailable.

## 14. Momentum
`RSI_N = clip((RSI9-50)/20,-1,+1)`.

MACD direction:
- MACD > Signal and Oscillator >0 -> `MACD_D=+1`
- MACD < Signal and Oscillator <0 -> `MACD_D=-1`
- otherwise `MACD_D=0`

`MOM = 0.50*RSI_N + 0.50*MACD_D`.

Both RSI9 and MACD/Signal/Oscillator are required for full MOM.
If only one momentum family is available, that available normalized family may be used but C5 becomes PARTIAL.

## 15. Session Structure
Require High > Low and valid KOSPI daily return `r_K`.

`CLV = clip(2*(Close-Low)/(High-Low)-1,-1,+1)`
`DAY = clip(r_K/0.015,-1,+1)`
`SES = 0.60*CLV + 0.40*DAY`

This prevents a strong late-session rebound from being interpreted as fully bullish when the session still closes down materially.

## 16. C5 Formula / Missing / Flags
Full:
`SAI-C5 = 0.55*TP + 0.25*MOM + 0.20*SES`
Range `[-1,+1]`.

VERIFIED requires full TP + full MOM + SES.

Predefined PARTIAL formulas:
- MOM unavailable, TP+SES valid -> `(0.55*TP+0.20*SES)/0.75`
- SES unavailable, TP+MOM valid -> `(0.55*TP+0.25*MOM)/0.80`
- TP based on only 4-5 anchors with MOM+SES valid -> same full formula but status PARTIAL
- MOM itself uses a single available momentum family -> status PARTIAL

TP unavailable, or both MOM and SES unavailable -> DATA UNAVAILABLE.

`C5 Conflict: ACTIVE` when TP opposes MOM or SES and both opposing values satisfy `|value|>=0.50`.
`C5 Shock: ACTIVE` when TECHNICAL_RULE confirms a major closing support breakdown/resistance breakout, including Recovery Structure Failure below 5,593, or when `|r_K|>=2.5%` and CLV confirms the same direction with `|CLV|>=0.50`.

# SAI-C6 Liquidity / Macro v2

## 17. Inputs / Formula
Use recurring HTS daily financial-condition data plus Customer Deposits history.

FX:
`FX = -clip(r_USDKRW/0.008,-1,+1)`

Rates use the HTS absolute rate change (`대비`) in percentage points, converted to basis points:
`dKTB_bp = 100 * Delta_KTB3Y_percentage_points`
`dCD_bp = 100 * Delta_CD91_percentage_points`

`KTB = -clip(dKTB_bp/10,-1,+1)`
`CD = -clip(dCD_bp/5,-1,+1)`

When both are valid:
`RATE = 0.70*KTB + 0.30*CD`

When only one is valid, RATE may equal the available rate axis but C6 status is PARTIAL.

Customer Deposits:
`DEP5 = Deposit_t/Deposit_t-5obs - 1`
`CASH = clip(DEP5/0.05,-1,+1)`

Full:
`SAI-C6 = 0.35*FX + 0.35*RATE + 0.30*CASH`
Range `[-1,+1]`.

## 18. Missing / Conflict / Shock
VERIFIED requires FX + full RATE(KTB+CD) + CASH.

PARTIAL requires at least two of FX/RATE/CASH and at least one of FX/RATE. Use predefined renormalization across available top-level axes:
`C6_partial = sum(w_i*X_i)/sum(w_i)` with original weights 0.35/0.35/0.30.
Any single-rate RATE axis also forces PARTIAL.

Otherwise DATA UNAVAILABLE.

Margin Credit, receivables and futures deposits are context/risk flags only in v2; rising credit is not automatically bullish.

`C6 Conflict: ACTIVE` when any two top-level axes oppose and both `|value|>=0.50`.
`C6 Shock: ACTIVE` when any validated raw change reaches:
- `|r_USDKRW|>=1.2%`
- `|dKTB_bp|>=15bp`
- `|dCD_bp|>=8bp`
- `|DEP5|>=7.5%`

# SAI-C7 Volatility / Derivatives Risk v2

## 19. Inputs / Formula
C7 v2 uses recurring HTS fields and removes mandatory VKOSPI-MA20/fair-basis requirements.

Volatility change:
`VOL = -clip(r_VKOSPI/0.10,-1,+1)`

KOSPI200 futures lead:
`FLEAD_RAW = r_KOSPI200_Futures - r_KOSPI200_Spot`
`FLEAD = clip(FLEAD_RAW/0.005,-1,+1)`

`SAI-C7 = 0.70*VOL + 0.30*FLEAD`
Range `[-1,+1]`.

A falling VKOSPI is risk-normalizing/positive; rising VKOSPI is risk-expanding/negative. FLEAD measures same-session futures-vs-spot directional lead, not fair-value basis.

## 20. Missing / Context / Conflict / Shock
- VOL + FLEAD valid -> VERIFIED.
- VOL valid, FLEAD unavailable -> `C7=VOL` / PARTIAL.
- VOL unavailable -> DATA UNAVAILABLE.

Context only, not direct numeric terms:
- raw futures basis level without fair/theoretical basis
- current OI snapshot without OI change/time series
- isolated Call/Put strike OI or volume
- full-market PCR unless explicitly supplied
- volatility futures/term structure, especially when liquidity is thin
- rollover/expiry positioning

`C7 Conflict: ACTIVE` when VOL/FLEAD oppose and both `|value|>=0.50`.
`C7 Shock: ACTIVE` when `|r_VKOSPI|>=15%`, or VOL/FLEAD share direction and both `|value|>=0.80`.

Expiry, rollover, major rebalance or comparable distortion -> `C7 Mechanical Event: ACTIVE`. Event-sensitive Shock cannot alone trigger adaptive numeric reweighting without structural confirmation.

# SAI-C8 Global Leading v2

## 21. Source Boundary
Primary numeric source is the recurring HTS global-market panel. Binance remains a global leading/supporting layer under BINANCE_RULE and may confirm or contradict C8, but is not required for numeric C8 v2 and is not silently re-added.

Numeric axes:
- current US Futures `USF` 40%
- prior US Close `USC` 25%
- Philadelphia Semiconductor `SEMI` 20%
- Asia `ASIA` 15%

WTI, Gold, DAX/CAC and Binance positioning remain macro/context unless a future explicit scoring revision adopts them.

## 22. US Futures / Prior US Close
Current futures:
`SPF = clip(r_MiniSP500/0.0075,-1,+1)`
`NQF = clip(r_MiniNASDAQ/0.010,-1,+1)`

Both valid:
`USF = 0.45*SPF + 0.55*NQF`
One valid only -> USF equals that axis, but C8 status cannot be VERIFIED.

Prior US close:
`SPX = clip(r_SP500/0.015,-1,+1)`
`NAS = clip(r_NASDAQ/0.020,-1,+1)`

Both valid:
`USC = 0.50*SPX + 0.50*NAS`
One valid only -> USC equals that axis, but C8 status cannot be VERIFIED.

Current futures and prior close are deliberately separate time layers and must retain their source timestamps; they are not treated as simultaneous observations.

## 23. Semiconductor / Asia
`SEMI = clip(r_SOX/0.025,-1,+1)`

Asia normalization:
`N_NIK = clip(r_Nikkei225/0.015,-1,+1)`
`N_SHA = clip(r_Shanghai/0.015,-1,+1)`
`N_SZX = clip(r_Shenzhen/0.020,-1,+1)`
`N_HSI = clip(r_HangSeng/0.020,-1,+1)`

China/HK composite with base weights Shanghai 25%, Shenzhen 25%, Hang Seng 50%; renormalize only across valid members:
`CHINA = weighted_average(valid N_SHA,N_SZX,N_HSI)`.

When Nikkei + CHINA valid:
`ASIA = 0.40*N_NIK + 0.60*CHINA`.
If only one side is available, ASIA may equal that side but C8 status cannot be VERIFIED.

## 24. C8 Formula / Completeness
`SAI-C8 = 0.40*USF + 0.25*USC + 0.20*SEMI + 0.15*ASIA`
Range `[-1,+1]`.

VERIFIED requires:
- both Mini S&P500 and Mini Nasdaq for USF;
- both prior S&P500 and Nasdaq for USC;
- SOX;
- Nikkei plus at least two of Shanghai/Shenzhen/Hang Seng for ASIA;
- valid timestamps/session labels.

PARTIAL requires all:
1. USF available;
2. at least 3 of 4 top-level axes available;
3. original C8 weight coverage >=65%;
4. no axis uses unknown timestamp/source.

`C8_partial = sum(w_i*X_i for valid axes)/sum(w_i for valid axes)`.
Any one-member composite fallback inside USF/USC/ASIA forces PARTIAL.
Otherwise DATA UNAVAILABLE.

Binance LIVE/FALLBACK/STALE is disclosed separately under BINANCE_RULE. STALE Binance cannot upgrade or numerically alter C8.

## 25. C8 Conflict / Shock / Anti-Double-Counting
`C8 Conflict: ACTIVE` when:
- USF and USC oppose and both `|value|>=0.40`, or
- USF and SEMI oppose and both `|value|>=0.50`.

`C8 Shock: ACTIVE` when USF, USC and SEMI share direction and all `|value|>=0.75`, or when USF, SEMI and ASIA share direction and all `|value|>=0.80`.

C8 is one E8 evidence family. Its sub-axes are not independent E1-E8 groups. SOX is scored once here; Korea sector breadth, C4 market rotation, C6 domestic liquidity and C7 domestic volatility are not re-added. Binance EWY/SOXL/SPY/QQQ/TMF/BTC and G6 positioning are confirmation/context only in v2.

# Global Strategy Action Index v2 Operational Layer

## 26. Base Weights / Formula
Global Base Weights remain unchanged after v2 regression:
- C1 Smart Money 18%
- C2 Program Flow 12%
- C3 Breadth/Internal 15%
- C4 Market Leadership/Rotation 10%
- C5 Technical Structure 20%
- C6 Liquidity/Macro 10%
- C7 Volatility/Derivatives 8%
- C8 Global Leading 7%

`SAI_Base = 0.18*C1 + 0.12*C2 + 0.15*C3 + 0.10*C4 + 0.20*C5 + 0.10*C6 + 0.08*C7 + 0.07*C8`
Range `[-1,+1]`.

Family Base distribution:
- Flow C1+C2 = 30%
- Internal C3+C4 = 25%
- Structure C5 = 20%
- Environment C6+C7+C8 = 25%

Weights remain v1/v2 rule-design calibrations, not empirically optimized estimates.

## 27. Global VERIFIED / PARTIAL Gate
A component is usable when its own rule returns a valid numeric VERIFIED or predefined PARTIAL value.

Global VERIFIED requires all C1-C8 VERIFIED.

Global PARTIAL uses:
`SAI_Partial = sum(w_i*C_i for usable components)/sum(w_i for usable components)`

PARTIAL requires all:
1. C5 usable;
2. at least one of C1/C2 usable;
3. at least one of C3/C4 usable;
4. at least one of C6/C7/C8 usable;
5. at least 6/8 components usable;
6. original Base Weight coverage >=70%.

Any component PARTIAL forces global PARTIAL. If any gate fails -> `Strategy Action Index: DATA UNAVAILABLE`.
Conditional Adaptive Weight is prohibited in global PARTIAL mode.

## 28. Family Scores / Global Conflict
Only when all C1-C8 are VERIFIED:
`F_FLOW = 0.60*C1 + 0.40*C2`
`F_INTERNAL = 0.60*C3 + 0.40*C4`
`F_STRUCTURE = C5`
`F_ENV = 0.40*C6 + 0.32*C7 + 0.28*C8`

These are helper aggregates, not new Evidence Groups.

`Global SAI Conflict: ACTIVE` when any two family scores oppose and both `|F|>=0.50`.
When active, retain Base SAI, block Conditional Adaptive Weight, disclose conflict and do not interpret a near-zero SAI as absence of information.

## 29. Conditional Adaptive Weight
Eligibility requires all C1-C8 VERIFIED, no Global SAI Conflict, validated Shock + independent confirmation, and no sole mechanical-event distortion.

Flow Event:
- C1/C2 same direction;
- one Shock ACTIVE;
- other `|C|>=0.50`.

Internal Event:
- C3/C4 same direction;
- one Shock ACTIVE;
- other `|C|>=0.50`.

Structure Event:
- C5 Shock ACTIVE;
- at least one independent family among FLOW/INTERNAL/ENV same direction and `|F|>=0.50`.

Environment Event:
- at least two of C6/C7/C8 same direction and both `|C|>=0.50`;
- one Shock ACTIVE.

Adjustment:
- no event -> Base unchanged;
- exactly one family event -> active family +5 percentage points, other three reduced proportionally to Base family weights;
- exactly two same-direction family events -> each +3pp, other two reduced proportionally;
- exactly two opposite-direction family events -> Adaptive BLOCKED / Base retained;
- three or more family events -> Base retained + `Broad Market Shock: ACTIVE`;
- maximum total family reallocation = 6pp;
- component ratios inside each family remain fixed;
- all adjusted weights remain non-negative and sum to 1.00.

`SAI_Final = sum(adjusted_weight_i*C_i)` when adaptive weighting is valid; otherwise Base or Partial SAI applies.

Required anti-circularity:
`C1-C8 -> Base SAI -> Preliminary Regime -> Adaptive Validation / Transition / Conflict -> Regime Re-validation -> Conditional Adaptive Event -> Final SAI -> Strategy / Portfolio Response`.

Prohibited:
`Regime -> numeric reweight -> Final SAI -> same Regime reconfirmed solely from Final SAI`.

## 30. Action Bands / Safety
- `+0.60 <= SAI <= +1.00` -> Strong Positive Execution Bias
- `+0.30 <= SAI < +0.60` -> Positive Execution Bias
- `-0.30 < SAI < +0.30` -> Balanced / Hold Bias
- `-0.60 < SAI <= -0.30` -> Negative Execution Bias
- `-1.00 <= SAI <= -0.60` -> Strong Negative Execution Bias

Action Bands are execution-bias labels, not automatic orders.
They never override Market Regime/Transition, material Conflict, C5 technical location, HTS/KRX confirmation, portfolio leverage/exposure/concentration, Extreme Risk controls or BINANCE_RULE freshness restrictions.
PARTIAL SAI alone cannot authorize the strongest aggressive action.

## 31. Actual Calculation Procedure
1. Parse and unit-validate the recurring HTS dataset.
2. Calculate C1-C8 from the owning v2 formulas only.
3. Record each component value, status and Conflict/Shock/Mechanical flags.
4. Apply Global VERIFIED/PARTIAL/DATA UNAVAILABLE gate.
5. If PARTIAL, calculate only SAI_Partial and stop adaptive numeric reweighting.
6. If VERIFIED, calculate SAI_Base and family scores.
7. Evaluate Global SAI Conflict.
8. Run Preliminary Regime -> Adaptive Validation -> Transition/Conflict -> Regime Re-validation.
9. Only then test Conditional Adaptive Events.
10. Calculate SAI_Final in [-1,+1] and assign Action Band.
11. Display numeric value, validation status, Base/Adaptive mode, material conflicts/shocks and Action Band.
12. Final portfolio action remains MASTER_RULE + ADAPTIVE_VALIDATION_RULE output, not score-only execution.

## 32. v2 Regression / Sample Validation
Mathematical invariants:
- Base weights sum 1.00.
- Family weights sum 1.00.
- allowed one-family/two-family adaptive reallocations preserve total 1.00 and non-negative component weights.
- all C1-C8 corner combinations remain inside [-1,+1].
- Missing is never zero.
- Global PARTIAL cannot use adaptive weights.

Provided 2026-09-10 HTS sample, using v2 formulas and stated units, produces approximately:
- C1 -0.61
- C2 -0.68
- C3 -0.03
- C4 +0.51
- C5 +0.52
- C6 -0.23
- C7 +0.33
- C8 -0.12
- Base SAI about -0.05

Interpretation: arithmetic SAI is Balanced/Hold, but the evidence is not information-free: Smart Money/Non-Arbitrage are materially negative while technical/session recovery, rotation and volatility normalization offset part of that pressure. Conflict/Transition review remains mandatory.

This sample is a formula sanity check, not a performance backtest.

## 33. Validation Status / Calibration Boundary
C1-C8 v2 and Global SAI are `VERIFIED BY RULE DESIGN` when their data gates pass.
The following remain `NOT EMPIRICALLY OPTIMIZED` until out-of-sample testing exists:
- normalization saturation thresholds
- Shock thresholds
- C1-C8 internal weights
- Global Base Weights
- +/-0.30 and +/-0.60 Action Bands

## 34. Final Principle
Use what can actually be validated from repeatable HTS inputs.
Do not demand unavailable theoretical inputs when a reproducible HTS-native formulation exists.
Do not substitute convenience for validation.

Strategy Action Index = execution bias, not automatic trade.
AI Master Score remains DATA UNAVAILABLE.
Adaptive priority != numeric weight.
Conflict is information, not noise.
Reliability > Speed.