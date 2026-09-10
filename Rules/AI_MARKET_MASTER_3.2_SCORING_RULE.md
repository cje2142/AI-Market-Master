# AI Market Master 3.2 Scoring Rule

Version: 3.2 Unified Stable
Status: Scoring Authority

## 1. Scope
This file is the only authority for numeric `AI Master Score` and `Strategy Action Index` definitions, inputs, weights, formulas, missing-data handling and validation.

Validated numeric sub-components do not activate a global score unless the applicable Numeric Score Activation Gate is satisfied in this file.

## 2. Current Official Status
Official current global numeric state:
- `AI Master Score: DATA UNAVAILABLE`
- `Strategy Action Index: FORMULA ACTIVATED / RUNTIME DATA-DEPENDENT`

Defined component specifications:
- `SAI-C1 Smart Money`
- `SAI-C2 Program Flow`
- `SAI-C3 Breadth / Market Internal`
- `SAI-C4 Sector / Leadership`
- `SAI-C5 Technical Structure`
- `SAI-C6 Liquidity / Macro`
- `SAI-C7 Volatility / Derivatives Risk`
- `SAI-C8 Global Leading`

C1-C8 are component specifications and inputs to the activated global Strategy Action Index v1. A runtime numeric Strategy Action Index may be shown only when the Global SAI data/completeness gate below passes. Otherwise output `Strategy Action Index: DATA UNAVAILABLE`.

AI Master Score remains unavailable because no complete reproducible AI Master Score formula has been adopted.

## 3. Numeric Score Activation Gate
A global numeric score may be activated only after all are explicitly defined and verified here:
1. Formula
2. Mandatory inputs
3. Input units / normalization
4. Weight or aggregation rule
5. Missing-data rule
6. Partial-data rule
7. Range / bounds
8. Interpretation bands if applicable
9. Actual calculation procedure
10. Validation / regression tests

The Strategy Action Index v1 satisfies this rule-design gate in Sections 48-57. AI Master Score does not.

## 4. Global Scoring Firewalls
Never infer a global score from qualitative signal colors, Market Regime, Transition, VH/H/M/L Evidence Priority, qualitative Strategy posture, analyst intuition, prior displayed numbers, indicator counts or hidden weights.

Missing mandatory data is never silently converted to zero/Neutral. Partial formulas are allowed only when explicitly predefined here.

Confidence and Regime Confidence are non-numeric evidence-quality labels, not market scores or probabilities.

Binance does not create a separate market score. Binance data can enter C8 only through the explicit C8 rules below and remains subject to BINANCE_RULE freshness, fallback and anti-hallucination controls.

Strategy Action Index is an execution-bias index, not an automatic trade command. Final portfolio action remains governed by MASTER_RULE + ADAPTIVE_VALIDATION_RULE with technical location, Regime/Transition, conflict and portfolio exposure.

## 5. Cross-Component Ownership Map
- C1 / E1: Smart Money
- C2 / E2: Program Flow
- C3 / E3: Breadth / Internal
- C4 / E4: Sector / Leadership
- C5 / E5: Technical Structure
- C6 / E6: Liquidity / Macro
- C7 / E7: Volatility / Derivatives Risk
- C8 / E8: Global Leading / Binance

The same underlying datum must not be counted as independent confirmation across multiple components.

# SAI-C1 Smart Money

## 6. Purpose / Inputs
Measures whether major directional capital in the Korean equity market is increasing or reducing risk exposure. E1 remains adaptive interpretation owner.

Required:
- Foreign KOSPI cash net flow
- Foreign KOSPI200 futures net contracts / total KOSPI200 futures OI

Optional:
- Institutional KOSPI cash net flow

Excluded from independent C1 scoring: Program, Breadth, Options, duplicated Financial Investment inside Institution total, cumulative futures position when current futures flow is already scored, OI change as independent direction.

## 7. Normalization / Formula
`FC = ForeignCash / KOSPITradedValue`
`N_FC = clip(FC/0.015,-1,+1)`

`FF = ForeignKOSPI200FuturesNet / TotalFuturesOI`
`N_FF = clip(FF/0.10,-1,+1)`

`IC = InstitutionCash / KOSPITradedValue`
`N_IC = clip(IC/0.010,-1,+1)`

Full:
`SAI-C1 = 0.40*N_FC + 0.40*N_FF + 0.20*N_IC`
Range `[-1,+1]`.

## 8. Missing / Flags / Validation
- all three valid -> VERIFIED
- Institution missing -> `0.50*N_FC + 0.50*N_FF` / PARTIAL
- Foreign Cash or Foreign Futures missing/invalid denominator -> DATA UNAVAILABLE

`C1 Conflict: ACTIVE` when Foreign Cash and Foreign Futures are materially opposed.

`C1 Shock: ACTIVE` when any validated raw ratio reaches:
- |ForeignCash/KOSPITradedValue| >=2.25%
- |ForeignFutures/TotalOI| >=15%
- |InstitutionCash/KOSPITradedValue| >=1.50%

Shock feeds Change Detection only. No automatic Regime/global SAI/portfolio/permanent-weight change.

Validation examples retained: `.75,.60,.30 -> .60`; `-.70,-.80,-.20 -> -.64`; `.70,-.90,.20 -> -.04 + Conflict`; mandatory missing -> DATA UNAVAILABLE.

# SAI-C2 Program Flow

## 9. Purpose / Inputs
Measures whether KOSPI program trading supplies or withdraws liquidity while separating structural Non-Arbitrage from more mechanical Arbitrage flow. E2 remains adaptive interpretation owner.

- Arbitrage Program net flow — optional/supplementary
- Non-Arbitrage Program net flow — required structural core
- Total Program — reconciliation/context only

## 10. Normalization / Formula
`ARB = ArbitrageNet / KOSPITradedValue`
`N_ARB = clip(ARB/0.0075,-1,+1)`

`NONARB = NonArbitrageNet / KOSPITradedValue`
`N_NONARB = clip(NONARB/0.015,-1,+1)`

`SAI-C2 = 0.30*N_ARB + 0.70*N_NONARB`
Range `[-1,+1]`.

## 11. Missing / Flags / Validation
- both valid -> VERIFIED
- Arbitrage missing, Non-Arbitrage valid -> `C2=N_NONARB` / PARTIAL
- Non-Arbitrage missing/invalid -> DATA UNAVAILABLE

`C2 Conflict: ACTIVE` when signs oppose and both |N|>=0.30.

`C2 Shock: ACTIVE` when:
- |Arbitrage/KOSPI traded value| >=1.125%
- |Non-Arbitrage/KOSPI traded value| >=2.25%

Known expiry/index/sector/ETF rebalance or comparable mechanical event -> `C2 Mechanical Event: ACTIVE`. Calculate C2, but Arbitrage alone cannot create a structural Regime conclusion.

Validation examples retained: `.50,.70 -> .64`; `-.40,-.80 -> -.68`; `+1,-.60 -> -.12 + Conflict`.

# SAI-C3 Breadth / Market Internal

## 12. Purpose / Inputs
Measures whether domestic participation is broadening or deteriorating beneath the headline index. E3 remains adaptive interpretation owner.

Required KOSPI breadth: `ADV_K`, `DEC_K`; `UNCH_K` context only.
Optional KOSDAQ confirmation: `ADV_Q`, `DEC_Q`; `UNCH_Q` context only.
Raw ADL absolute level is contextual only in v1.

## 13. Normalization / Formula
`B_K=(ADV_K-DEC_K)/(ADV_K+DEC_K)`
`N_K=clip(B_K/0.50,-1,+1)`

`B_Q=(ADV_Q-DEC_Q)/(ADV_Q+DEC_Q)`
`N_Q=clip(B_Q/0.50,-1,+1)`

`SAI-C3=0.70*N_K+0.30*N_Q`
Range `[-1,+1]`.

## 14. Missing / Flags / Validation
- KOSPI + KOSDAQ valid -> VERIFIED
- KOSDAQ missing -> `C3=N_K` / PARTIAL
- KOSPI invalid/missing or ADV_K+DEC_K<=0 -> DATA UNAVAILABLE

`C3 Conflict: ACTIVE` when N_K and N_Q oppose and both |N|>=0.30.

KOSPI return is comparator only. `C3 Divergence: ACTIVE` when KOSPI return>0 with N_K<=-0.30, or return<0 with N_K>=+0.30.

`C3 Shock: ACTIVE` when |B_K|>=0.75, or KOSPI/KOSDAQ breadth have same direction and both |B|>=0.65.

Validation examples retained: 600/300 with 1000/600 -> C3≈.6167; 250/650 with 500/1100 -> C3≈-.8472; N_K=.60,N_Q=-.50 -> .27 + Conflict.

# SAI-C4 Sector / Leadership

## 15. Purpose / Fixed Universe
Measures sector participation and KOSPI-relative leadership. E4 remains adaptive interpretation owner.

Fixed C4 v1 universe:
1. KRX Semiconductor Index
2. KRX Automobile Index
3. KRX Secondary Battery TOP 10 Index
4. KOSPI 200 Financial Index
5. iSelect Shipbuilding TOP10 Index (PR)
6. iSelect Defense TOP10 Index (Price Return)
7. KRX-Akros AI Power Infrastructure Index
8. KRX Bio TOP 10 Index

Canonical identity = provider + exact benchmark name. ETF ticker/code is not benchmark index code. Ambiguous mapping = unavailable.

## 16. Data / Formula
Required recurring data: same-session KOSPI daily return plus same-session sector benchmark daily returns.

For each sector return `r_i`:
- >+0.20% -> D_i=+1
- <-0.20% -> D_i=-1
- else 0

`SD=(UP-DOWN)/N_valid`

`RS_i=SectorReturn_i-KOSPIReturn`
- >+0.20%p -> L_i=+1
- <-0.20%p -> L_i=-1
- else 0

`RL=(OUT-UNDER)/N_valid`

`SAI-C4=0.60*SD+0.40*RL`
Range `[-1,+1]`.

## 17. Completeness / Flags
- 8/8 + valid KOSPI comparator -> eligible VERIFIED
- 6-7/8 + valid comparator -> PARTIAL
- <6/8 or invalid/asynchronous KOSPI comparator -> DATA UNAVAILABLE

Leadership Concentration remains qualitative/contextual under E4, not a direct C4 numeric term.

`C4 Conflict: ACTIVE` when SD and RL oppose and both |value|>=0.50.

`C4 Shock: ACTIVE` when |SD|>=0.75, or SD/RL same sign and both |value|>=0.60.

ETF return cannot silently substitute a missing benchmark return.

# SAI-C5 Technical Structure

## 18. Purpose / Timeframe
Measures whether KOSPI technical price structure confirms strength or deterioration. TECHNICAL_RULE remains calculation authority and E5 remains adaptive interpretation owner.

Official C5 v1 = KOSPI Daily / Closing-confirmed. Intraday data produces only `C5 Intraday Preview`.

Numeric terms:
- `PS` Price Structure — mandatory, 50%
- `SR` Support/Resistance Position — 30%
- `TP` MA/VWAP Trend Position — 20%

## 19. PS / SR / TP
PS:
- HH+HL -> +1
- LH+LL -> -1
- mixed -> 0
- one-sided validated improvement/deterioration -> +/-0.50
- confirmed closing breakout/breakdown may set +/-1

SR with validated `S<R` and close `C` inside corridor:
`X=clip(2*(C-S)/(R-S)-1,-1,+1)`
`SR=0.50*X`
Confirmed closing breakout above R -> +1; breakdown below S -> -1.

TP fixed anchors: MA20, MA60, VWAP20, VWAP60.
For each anchor A_j:
- Close > A_j*1.002 -> +1
- Close < A_j*0.998 -> -1
- else 0
`TP=average(T_j)`.
4/4 anchors = full; 2-3 = usable but C5 PARTIAL; <2 = unavailable.

## 20. Formula / Missing / Flags
Full:
`SAI-C5=0.50*PS+0.30*SR+0.20*TP`
Range `[-1,+1]`.

SR missing only: `0.70*PS+0.30*TP` / PARTIAL.
TP missing only: `0.625*PS+0.375*SR` / PARTIAL.
PS missing, or PS only with both SR/TP missing -> DATA UNAVAILABLE.

Volume, RSI, MACD, ADX, Ichimoku, Elliott and Fibonacci are validation/context only in C5 v1.

`C5 Divergence: ACTIVE` for validated material price-vs-RSI/MACD divergence.
`C5 Conflict: ACTIVE` when PS/SR or PS/TP oppose and both |value|>=0.50.
`C5 Shock: ACTIVE` for confirmed major Support breakdown, Resistance breakout or Recovery Structure Failure trigger including closing break below 5,593.

# SAI-C6 Liquidity / Macro

## 21. Purpose / Time Standard
Measures whether domestic financial conditions are becoming more supportive or restrictive using FX pressure, domestic rate pressure and investable cash liquidity. E6 remains adaptive interpretation owner.

Official C6 uses latest completed daily observations. Customer Deposits use latest officially published observation available at execution time; observation date must be disclosed when different from FX/rate date. Intraday values are preview only.

## 22. Normalization / Formula
FX:
`FX_raw = USDKRW_t/USDKRW_t-5 - 1`
`FX = -clip(FX_raw/0.020,-1,+1)`

RATE:
`dY5_bp = KoreaTreasury3Y_t - KoreaTreasury3Y_t-5`
`RATE = -clip(dY5_bp/20,-1,+1)`

CASH:
`DEP5 = Deposit_t/Deposit_t-5 - 1`
`CASH = clip(DEP5/0.05,-1,+1)`

Full:
`SAI-C6=0.35*FX+0.35*RATE+0.30*CASH`
Range `[-1,+1]`.

## 23. Missing / Context / Flags
- all three valid -> VERIFIED
- FX missing -> `0.5385*RATE+0.4615*CASH` / PARTIAL
- RATE missing -> `0.5385*FX+0.4615*CASH` / PARTIAL
- CASH missing -> `0.50*FX+0.50*RATE` / PARTIAL
- fewer than two axes, or no FX/RATE axis -> DATA UNAVAILABLE

Margin Credit is context/flag only because rising credit can indicate both liquidity expansion and leverage fragility. Policy Rate, M2 and lower-frequency macro remain Structural Macro Context.

`C6 Conflict: ACTIVE` when any two available numeric axes oppose and both |value|>=0.50.

`C6 Shock: ACTIVE` when:
- |USD/KRW 5-observation change| >=2.5%
- |Korea Treasury 3Y 5-observation change| >=30bp
- |Customer Deposits 5-observation change| >=7.5%

Korea Treasury 3Y is domestic financial-condition input; TMF remains C8/E8 global-leading data and is not re-scored in C6.

# SAI-C7 Volatility / Derivatives Risk

## 24. Purpose and Boundary
Measures whether domestic volatility and derivatives-price structure indicate risk expansion or normalization while avoiding false direction from OI, isolated option strikes, expiry mechanics or duplicated global-leading derivatives data. E7 remains adaptive interpretation owner.

## 25. Timeframe / Source Standard
Official C7 v1 uses completed Korean-market observations when available.
VOL requires VKOSPI spot or a validated official equivalent plus enough history to calculate a 20-observation moving average. VKOSPI futures do not silently replace VKOSPI spot.

BASIS requires same-session Actual KOSPI200 futures basis, Theoretical/Fair basis and KOSPI200 spot/index denominator. Raw basis sign alone must not be scored.

## 26. C7-A Volatility Stress
`VOL_REL = VKOSPI_t / VKOSPI_MA20 - 1`
`VOL = -clip(VOL_REL / 0.30,-1,+1)`

VKOSPI absolute level is context only in v1.

## 27. C7-B Basis Stress
`BasisGap = ActualBasis - FairBasis`
`BG = BasisGap / KOSPI200Spot`
`BASIS = clip(BG / 0.003,-1,+1)`

BASIS is optional because Fair/Theoretical Basis may require a separate HTS lookup.

## 28. Formula / Missing / Partial
Full:
`SAI-C7 = 0.60*VOL + 0.40*BASIS`
Range `[-1,+1]`.

- VOL + BASIS valid -> eligible VERIFIED
- VOL valid, BASIS unavailable -> `C7=VOL` / PARTIAL
- VOL unavailable -> DATA UNAVAILABLE even if BASIS is available

Missing data is never zero/Neutral.

## 29. OI / Options / Volatility-Futures Boundary
Context/flags only, not direct C7 numeric terms:
- KOSPI200 futures OI/OI change
- isolated Call/Put OI/volume
- full-market Put/Call Ratio
- volatility futures/term structure
- rollover/expiry positioning

OI is directionless without price/position context. One strike cannot represent the full options market. PCR may reflect fear/hedging or contrarian extremes. Volatility futures contain expiry/term-structure effects.

## 30. Conflict / Shock / Mechanical Event
`C7 Conflict: ACTIVE` when VOL and BASIS oppose and both |value|>=0.50.

`C7 Shock: ACTIVE` when:
- |VKOSPI/VKOSPI_MA20 - 1| >=45%, or
- |BasisGap/KOSPI200Spot| >=0.45%, or
- VOL and BASIS both <=-0.80 with independent derivatives-risk confirmation.

`C7 Mechanical Event: ACTIVE` for derivatives expiry, rollover, major index/sector rebalance or comparable distortion.

Flags feed Change Detection / Transition / Regime re-validation only. No automatic Regime/global SAI/portfolio/permanent-weight change.

## 31. C7 Anti-Double-Counting / Anti-Circularity
VKOSPI relative stress is scored once; VKOSPI absolute level and volatility futures are contextual only. Fair-value-adjusted KOSPI200 basis is scored once. OI/PCR/isolated options remain context.

Smart Money C1, Program C2, Breadth C3, Sector C4, Technical C5, Liquidity C6 and Global Leading C8 remain separate. Binance OI/Funding/Long-Short data remain E8/G6 and are not re-scored in C7.

C7 cannot choose a Regime, use that Regime to alter its own weights, then use altered C7 to reconfirm the same Regime. VH/H/M/L remains qualitative only.

## 32. C7 Validation Cases
- VOL=-1,BASIS=-1 -> C7=-1
- VOL=+1,BASIS=+.5 -> C7=+.8
- VOL=-.8,BASIS=+.7 -> C7=-.2 + Conflict
- VOL=-.6,BASIS unavailable -> -.6 / PARTIAL
- VOL unavailable -> DATA UNAVAILABLE
- OI surge alone -> no direct numeric direction
- one ATM option strike -> no official PCR
- volatility futures without VKOSPI -> context only

# SAI-C8 Global Leading

## 33. Purpose and Boundary
`SAI-C8 Global Leading` is the eighth formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether major global risk, Korea-leading, semiconductor, rates/liquidity and high-beta risk proxies are providing supportive or restrictive leading conditions for the Korean market, while preventing duplicate counting of correlated symbols and positioning fields.

Authority boundary:
- Numeric C8 formula, normalization, fixed internal weights, missing/partial handling and C8 conflict/shock conditions are owned by this SCORING_RULE.
- `E8 Global Leading` interpretation, Market Regime, Transition and VH/H/M/L Evidence Priority remain owned by ADAPTIVE_VALIDATION_RULE.
- BINANCE_RULE remains the authority for the fixed 8-symbol watchlist, G1-G6, LIVE/FALLBACK/STALE, freshness, fallback eligibility, field depth and positioning interpretation.
- C8 is a numeric sub-component, not a new engine or Evidence Group.
- C8 cannot select or reconfirm a Market Regime by itself.

## 34. C8 Fixed Numeric Axis Map
Five numeric axes:
1. `GR` Global Equity Risk — 30%
2. `KR` Korea Leading — 25%
3. `SEMI` Semiconductor Risk — 20%
4. `GLIQ` Global Rate/Liquidity — 15%
5. `CRYPTO` Crypto Risk — 10%

Canonical symbol mapping:
- GR = SPYUSDT + QQQUSDT composite
- KR = EWYUSDT
- SEMI = SOXLUSDT
- GLIQ = TMFUSDT
- CRYPTO = BTCUSDT

SAMSUNGUSDT and SKHYNIXUSDT remain Korea/Semiconductor confirmation signals under G2/G3 and are not additional numeric C8 axes.

The Binance Engine still queries all 8 fixed symbols under BINANCE_RULE. C8 does not reduce or redefine that watchlist.

## 35. Observation Window / Source / Freshness Standard
C8 numeric inputs should use the same validated observation window and materially aligned query time whenever possible.

For Binance numeric inputs, use same-query rolling 24h return or an equivalently computed aligned 24h return. Do not silently mix different return windows inside one C8 calculation.

Source/freshness rules:
- LIVE: eligible for normal numeric use.
- FALLBACK: eligible only when BINANCE_RULE fallback conditions and TTL are satisfied; any C8 using FALLBACK is capped at `PARTIAL` and the Binance Confidence downgrade must be preserved.
- STALE: prohibited from numeric C8 use; historical context only.

If official non-Binance evidence is used for an axis, its instrument identity, source, observation window and timestamp must be disclosed and aligned with the C8 calculation. HTS/KRX remains final Korean-market confirmation under MASTER_RULE.

## 36. C8-A Global Equity Risk
Normalize the aligned return `r` for each valid equity proxy:

`N_SPY = clip(r_SPY / 0.015,-1,+1)`
`N_QQQ = clip(r_QQQ / 0.020,-1,+1)`

When both are valid:
`GR = 0.50*N_SPY + 0.50*N_QQQ`

If only one is valid, `GR` may equal the single available normalized equity proxy, but the overall C8 status is `PARTIAL` even if all other axes are present.

If neither is valid, GR is unavailable and C8 cannot pass the minimum gate.

SPY and QQQ form one Global Equity Risk composite and are not independent Evidence Groups.

## 37. C8-B Korea Leading
`KR = clip(r_EWY / 0.025,-1,+1)`

EWY is the primary numeric Korea-leading proxy. SAMSUNGUSDT and SKHYNIXUSDT are confirmation/context only and must not be re-added numerically after EWY.

## 38. C8-C Semiconductor Risk
`SEMI = clip(r_SOXL / 0.050,-1,+1)`

SOXL is the primary numeric global semiconductor risk-appetite proxy. Samsung/SK hynix Binance returns remain G2/G3 confirmation only.

C4 domestic sector breadth and AI Cycle fundamentals are separate evidence families and are not numerically re-added to C8.

## 39. C8-D Global Rate / Liquidity
`GLIQ = clip(r_TMF / 0.030,-1,+1)`

TMF is a global long-duration rates/liquidity proxy. A TMF rise caused by recession/panic does not automatically create a bullish Regime; meaning is cross-validated with C6/E6, C7/E7 and broader E8 evidence.

C6 Korea Treasury 3Y remains domestic financial-condition input and is not re-scored here.

## 40. C8-E Crypto Risk
`CRYPTO = clip(r_BTC / 0.040,-1,+1)`

BTC is a high-beta auxiliary risk/liquidity proxy and receives the smallest fixed C8 weight. BTC alone cannot determine broad equity risk or Korean-market action.

## 41. SAI-C8 Formula
When all five axes are valid and freshness/source/window checks pass:

`SAI-C8 = 0.30*GR + 0.25*KR + 0.20*SEMI + 0.15*GLIQ + 0.10*CRYPTO`

Range:
`-1.00 <= SAI-C8 <= +1.00`

Internal weights:
- GR 30%
- KR 25%
- SEMI 20%
- GLIQ 15%
- CRYPTO 10%

These are C8 v1 calibration weights. They do not define C8's global weight inside Strategy Action Index except where Section 49 explicitly assigns the global C8 Base Weight.

The normalization saturation boundaries and internal weights are design calibrations, not claims of empirical backtest optimization.

## 42. C8 Missing / Partial Rule
Full C8:
- all five axes valid
- GR uses both SPY and QQQ
- all numeric inputs satisfy source/window/freshness validation
-> eligible `VERIFIED`.

Predefined partial formula:
`C8_partial = sum(w_i*X_i for valid axes) / sum(w_i for valid axes)`

PARTIAL is allowed only if all are true:
1. GR is available;
2. at least 3 of the 5 axes are valid;
3. original fixed-weight coverage of valid axes is at least 60%;
4. no STALE input is used numerically.

Additional rule:
- if GR uses only SPY or only QQQ, overall C8 status is PARTIAL.
- any valid FALLBACK input caps overall C8 status at PARTIAL.

If GR is unavailable, fewer than 3 axes are valid, fixed-weight coverage is below 60%, or STALE data would be required to pass the gate -> `SAI-C8 = DATA UNAVAILABLE`.

Missing values are never converted to zero/Neutral. The partial formula is predefined and therefore is not silent reweighting.

## 43. Positioning / Confirmation Boundary
The following remain context/flags only in C8 v1 and are not additional numeric terms:
- SAMSUNGUSDT / SKHYNIXUSDT returns
- OI / OI change
- Funding Rate
- Global/Top-Trader Long/Short ratios
- Premium / Mark-Index spread
- ADL risk
- Order book / recent trades

These are interpreted under BINANCE_RULE G2/G3/G6.

Examples:
- Price down + OI up -> possible new short/hedge expansion
- Price up + OI up -> new position inflow possible; direction needs corroboration
- extreme Funding -> crowding warning

No positioning flag changes C8 numeric weights ad hoc.

## 44. C8 Conflict / Confirmation Conflict
Raise `C8 Conflict: ACTIVE` when a material cross-axis conflict is validated, including:
- GR and KR opposite with both |value|>=0.50, or
- GR and SEMI opposite with both |value|>=0.50.

Other major axis conflicts may be disclosed contextually but do not trigger hidden reweighting.

Raise `C8 Korea Confirmation Conflict: ACTIVE` when KR/EWY materially conflicts with both available SAMSUNGUSDT and SKHYNIXUSDT confirmation signals.

Raise `C8 Semiconductor Confirmation Conflict: ACTIVE` when SEMI/SOXL materially conflicts with both available Samsung/SK hynix confirmation signals.

Conflict flags do not directly alter the formula. A near-zero aggregate caused by opposing global-leading evidence is not treated as absence of information.

## 45. C8 Shock / Change Detection
Raise `C8 Shock: ACTIVE` when validated conditions include:
- GR, KR and SEMI all <=-0.80, or
- GR, KR and SEMI all >=+0.80, or
- another extreme aligned global-leading move is independently confirmed by G6 positioning/crowding evidence.

C8 Shock is a Change Detection / Transition / Regime re-validation input only.
It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 46. C8 Anti-Double-Counting / Anti-Circularity
For C8 numeric scoring:
- SPY + QQQ are compressed into one GR composite.
- EWY is scored once as KR.
- SOXL is scored once as SEMI.
- TMF is scored once as GLIQ.
- BTC is scored once as CRYPTO and limited to 10% internal C8 weight.
- Samsung/SK hynix Binance returns remain confirmation only.
- G6 positioning fields remain context only.
- C6 domestic rates/liquidity are not re-added.
- C7 domestic volatility/derivatives are not re-added.
- C4 domestic sector breadth and AI Cycle fundamentals are not re-added.

C8 is one E8 evidence family; its five axes are not five independent Evidence Groups for adaptive consensus counting.

Required separation:
`Validated Global Leading Data -> C8 Calculation`

and independently:
`Raw HTS + other Evidence -> Preliminary Regime -> Adaptive Priority -> Transition/Conflict -> Regime Re-validation`

C8 must not choose a Regime, use that Regime to alter its own numeric weights, then use altered C8 as the sole reason to reconfirm the same Regime. VH/H/M/L remains qualitative only.

## 47. C8 Validation Cases
A. All five axes +1 -> C8=+1.00.
B. All five axes -1 -> C8=-1.00.
C. `GR=+0.8, KR=-0.8, SEMI=-0.6, GLIQ=+0.2, CRYPTO=0` -> calculate normally + `C8 Conflict: ACTIVE`.
D. GR+KR+SEMI only -> 75% original weight coverage; predefined renormalized `PARTIAL` allowed.
E. KR+SEMI+GLIQ+CRYPTO without GR -> DATA UNAVAILABLE despite 70% coverage.
F. GR+KR only -> DATA UNAVAILABLE because fewer than 3 axes.
G. one of SPY/QQQ missing while the other is valid -> GR single-index fallback, overall C8 PARTIAL.
H. valid FALLBACK input inside TTL -> numeric use permitted but overall C8 PARTIAL and Confidence downgraded.
I. STALE Binance input -> numeric use prohibited.
J. Samsung/SKH conflict with EWY/SOXL -> confirmation conflict only; no direct numeric weight change.

Result: PASS by rule design.

# Global Strategy Action Index v1

## 48. Purpose / Activation Boundary
Global `Strategy Action Index` (SAI) converts the eight independently specified C1-C8 component values into a reproducible execution-bias index.

SAI is not an automatic buy/sell command and does not replace Market Regime, Transition, qualitative Evidence Priority, Technical location, portfolio exposure or MASTER portfolio-risk rules.

Runtime numeric SAI is allowed only when Section 50's global data gate passes. Otherwise output `Strategy Action Index: DATA UNAVAILABLE`.

`AI Master Score` remains `DATA UNAVAILABLE` and is not inferred from SAI.

## 49. Global Base Weights / Base Formula
Fixed v1 Base Weights:
- C1 Smart Money = 18%
- C2 Program Flow = 12%
- C3 Breadth / Internal = 15%
- C4 Sector / Leadership = 10%
- C5 Technical Structure = 20%
- C6 Liquidity / Macro = 10%
- C7 Volatility / Derivatives Risk = 8%
- C8 Global Leading = 7%

Sum = 100%.

`SAI_Base = 0.18*C1 + 0.12*C2 + 0.15*C3 + 0.10*C4 + 0.20*C5 + 0.10*C6 + 0.08*C7 + 0.07*C8`

Range: `-1.00 <= SAI <= +1.00`.

Family-level Base distribution:
- Flow = C1+C2 = 30%
- Internal = C3+C4 = 25%
- Structure = C5 = 20%
- Environment = C6+C7+C8 = 25%

The 18/12/15/10/20/10/8/7 weights are v1 rule-design calibrations, not claims of empirical backtest optimization. They may not be changed automatically or permanently from observed outcomes without an explicit future SCORING_RULE revision.

## 50. Global Missing / Partial Gate
A component is `usable` only when that component's own rule produces a valid numeric value with status VERIFIED or predefined PARTIAL.

### Global VERIFIED
Global SAI status is VERIFIED only when:
- C1-C8 are all usable;
- every C1-C8 status is VERIFIED;
- applicable source/date/session/freshness checks pass.

### Global PARTIAL
If one or more usable components are PARTIAL or one/two components are unavailable, calculate only with the predefined global partial formula:

`SAI_Partial = sum(w_i*C_i for usable components) / sum(w_i for usable components)`

PARTIAL is allowed only when all are true:
1. C5 Technical Structure is usable;
2. at least one of C1/C2 is usable;
3. at least one of C3/C4 is usable;
4. at least one of C6/C7/C8 is usable;
5. at least 6 of 8 components are usable;
6. original fixed Base Weight coverage of usable components is at least 70%.

Any predefined component PARTIAL may be used inside this formula, but global status remains PARTIAL.

If any gate fails -> `Strategy Action Index: DATA UNAVAILABLE`.
Missing values are never set to zero/Neutral.
Conditional Adaptive Weight is prohibited whenever global status is PARTIAL.

## 51. Family Scores / Global Conflict
For conflict and adaptive-event logic only when all C1-C8 are VERIFIED, define:

`F_FLOW = 0.60*C1 + 0.40*C2`
`F_INTERNAL = 0.60*C3 + 0.40*C4`
`F_STRUCTURE = C5`
`F_ENV = 0.40*C6 + 0.32*C7 + 0.28*C8`

These are within-SCORING aggregation helpers, not new Evidence Groups. The four family scores correspond to the fixed 30/25/20/25 Base family distribution and do not replace E1-E8.

Raise `Global SAI Conflict: ACTIVE` when any two independent family scores:
- have opposite signs, and
- both satisfy `|F| >= 0.50`.

When active:
- keep the mathematically calculated Base SAI;
- do not interpret a near-zero aggregate as absence of information;
- block Conditional Adaptive Weight;
- disclose the material conflict;
- resolve action through ADAPTIVE_VALIDATION_RULE + MASTER_RULE rather than score counting.

## 52. Conditional Adaptive Weight v1
Conditional numeric reweighting is an exception layer over the fixed Base Weights. It is not Regime-to-number conversion.

Eligibility requires all:
- C1-C8 status VERIFIED;
- `Global SAI Conflict` not ACTIVE;
- qualifying Shock and confirmation data validated;
- no qualifying trigger depends solely on mechanical-event distortion.

### Qualifying Family Events
`Flow Adaptive Event`:
- C1 and C2 same direction;
- at least one has its own Shock ACTIVE;
- the other satisfies `|C| >= 0.50`.

`Internal Adaptive Event`:
- C3 and C4 same direction;
- at least one has its own Shock ACTIVE;
- the other satisfies `|C| >= 0.50`.

`Structure Adaptive Event`:
- C5 Shock ACTIVE;
- at least one independent family among F_FLOW/F_INTERNAL/F_ENV has the same direction and `|F| >= 0.50`.

`Environment Adaptive Event`:
- at least two of C6/C7/C8 have the same direction;
- both qualifying values satisfy `|C| >= 0.50`;
- at least one has its own Shock ACTIVE.

Mechanical-event guard:
A C2 or C7 Shock accompanied by its Mechanical Event flag cannot be the sole qualifying Shock for numeric reweighting unless the owning rule's event review confirms that the directional stress is structural rather than mechanical.

### Weight Adjustment
No qualifying event:
- Base Weights unchanged.

Exactly one qualifying family event:
- active family weight `+5 percentage points`;
- the other three family weights are reduced proportionally to their Base family weights;
- component ratios inside each family remain fixed.

Exactly two qualifying family events with the same direction:
- each active family weight `+3 percentage points`;
- the other two family weights are reduced proportionally to their Base family weights;
- component ratios inside each family remain fixed.

Exactly two qualifying family events with opposite directions:
- `Conditional Adaptive Weight: BLOCKED`;
- retain Base Weights;
- disclose Conflict / Transition review.

Three or more qualifying family events:
- retain Base Weights;
- raise `Broad Market Shock: ACTIVE`;
- do not increase any family because broad alignment does not justify preferring one already-confirming family over another.

Maximum total family-weight reallocation = 6 percentage points.
All adjusted component weights must remain non-negative and sum to 1.00.

`SAI_Final = sum(w_i_adjusted * C_i)` when adaptive weighting is valid; otherwise `SAI_Final = SAI_Base` for VERIFIED status or `SAI_Partial` for PARTIAL status.

VH/H/M/L is never converted into numeric weights. Market Regime labels never directly select a numeric weight table.

Required anti-circularity order:
`C1-C8 -> Base SAI -> Preliminary Regime -> Adaptive Validation / Transition / Conflict -> Regime Re-validation -> Conditional Adaptive Event -> Final SAI -> Strategy / Portfolio Response`.

Prohibited:
`Regime -> numeric reweight -> Final SAI -> same Regime reconfirmed solely from Final SAI`.

## 53. Strategy Action Index Action Bands
Use the final valid SAI value in `[-1,+1]`.

- `+0.60 <= SAI <= +1.00` -> `Strong Positive Execution Bias`
- `+0.30 <= SAI < +0.60` -> `Positive Execution Bias`
- `-0.30 < SAI < +0.30` -> `Balanced / Hold Bias`
- `-0.60 < SAI <= -0.30` -> `Negative Execution Bias`
- `-1.00 <= SAI <= -0.60` -> `Strong Negative Execution Bias`

These bands are numeric SAI interpretation labels, not ADAPTIVE_VALIDATION qualitative Strategy Postures and not automatic portfolio orders.

After independent confirmation, MASTER action vocabulary may be considered:
- Strong Positive -> 적극매수 / 비중확대 검토
- Positive -> 분할매수 / 보유강화 검토
- Balanced -> 보유 / 현금대기 / 다음 확인
- Negative -> 비중축소 / 분할매도 검토
- Strong Negative -> 적극 비중축소 / 현금확보 검토; leverage-reduction priority applies before core spot when reduction is actually required.

The +/-0.30 and +/-0.60 thresholds are v1 design calibrations, not empirically optimized market-performance cutoffs.

## 54. Execution Safety Overrides
The numeric SAI and its Action Band never override:
- verified Market Regime / Transition evidence;
- material unresolved Conflict;
- C5 technical location / support-resistance confirmation;
- MASTER portfolio leverage/exposure/concentration assessment;
- HTS/KRX final Korean-market confirmation;
- Extreme Risk controls;
- Binance freshness restrictions.

If Global SAI status is PARTIAL, show the numeric value and Action Band only as a partial execution bias. PARTIAL SAI alone cannot authorize the strongest aggressive action.

If `Global SAI Conflict: ACTIVE`, adaptive weighting is blocked and score-only execution is prohibited.

If C2/C7 Mechanical Event is ACTIVE and materially affects the direction, require structural re-validation before event-sensitive evidence supports strong execution.

A Strong Positive SAI does not automatically permit leverage expansion. A Strong Negative SAI does not automatically require core-spot liquidation. Final portfolio action remains cross-engine and portfolio-specific.

## 55. Actual Calculation Procedure
For every runtime SAI calculation:
1. Calculate C1-C8 only from their owning formulas and current validated inputs.
2. Record each component value, status and material Conflict/Shock/Mechanical flags.
3. Apply Section 50 Global VERIFIED/PARTIAL/DATA UNAVAILABLE gate.
4. If PARTIAL, calculate only `SAI_Partial`; adaptive weighting is prohibited.
5. If VERIFIED, calculate `SAI_Base` and four family scores.
6. Evaluate `Global SAI Conflict`.
7. Complete Preliminary Regime -> Adaptive Validation -> Transition/Conflict -> Regime re-validation under ADAPTIVE_VALIDATION_RULE.
8. Only after re-validation, test Section 52 Conditional Adaptive Events.
9. Apply Base or adjusted weights according to Section 52.
10. Calculate `SAI_Final` and constrain numerical round-off to [-1,+1].
11. Assign the Section 53 Action Band.
12. Display SAI numeric value, Validation Status, Base/Adaptive mode, material Conflict/Shock state and Action Band; use two decimals for normal presentation while retaining full precision internally.
13. Derive final portfolio action only through MASTER_RULE + ADAPTIVE_VALIDATION_RULE, not from the SAI number alone.

## 56. Regression / Stress Validation
Rule-design validation completed before activation:

### Weight invariants
- Base component weights sum exactly to 1.00.
- Base family weights sum exactly to 1.00.
- Every defined one-family +5pp pattern preserves total weight 1.00 and positive component weights.
- Every defined two-family +3pp/+3pp pattern preserves total weight 1.00 and positive component weights.

### Range regression
Exhaustive mathematical corner testing over all 256 combinations of `C1-C8 in {-1,+1}` was evaluated across Base and every allowed one-family/two-family adjusted-weight pattern.
Result: every score remained inside `[-1,+1]`.

Boundary cases:
- all C1-C8 = +1 -> SAI = +1.00
- all C1-C8 = -1 -> SAI = -1.00

Theoretical maximum score displacement caused solely by adaptive reallocation for component values in [-1,+1]:
- one-family 5pp shift: <=0.10 versus Base
- two-family total 6pp shift: <=0.12 versus Base

### Missing / Partial regression
- C5 missing -> DATA UNAVAILABLE even if seven other components are available.
- fewer than six usable components -> DATA UNAVAILABLE.
- missing Flow family, Internal family or Environment family -> DATA UNAVAILABLE.
- valid six-plus-component state with C5, all required families and >=70% Base Weight coverage -> PARTIAL.
- any component PARTIAL -> global status cannot be VERIFIED.
- PARTIAL -> Conditional Adaptive Weight blocked.

### Conflict / interpretation regression
Example stress set:
`C1=.9,C2=.7,C3=.8,C4=.6,C5=-.9,C6=-.4,C7=-.8,C8=-.6`
produces a near-neutral Base SAI around `+0.10`, while Flow/Internal are strongly positive and Structure/Environment strongly negative. `Global SAI Conflict: ACTIVE` therefore prevents false 'no information' interpretation and blocks adaptive reweighting.

Action Bands are monotonic and sign-symmetric around the Balanced interval.

Result: `PASS BY FORMULA / RULE-DESIGN REGRESSION`.
This is not empirical market-performance backtesting and does not establish that v1 weights or thresholds are statistically optimal.

## 57. Current Status After Global SAI v1 Activation
- C1 Smart Money: FORMULA DEFINED / COMPONENT INPUT
- C2 Program Flow: FORMULA DEFINED / COMPONENT INPUT
- C3 Breadth / Market Internal: FORMULA DEFINED / COMPONENT INPUT
- C4 Sector / Leadership: FORMULA DEFINED / COMPONENT INPUT
- C5 Technical Structure: FORMULA DEFINED / COMPONENT INPUT
- C6 Liquidity / Macro: FORMULA DEFINED / COMPONENT INPUT
- C7 Volatility / Derivatives Risk: FORMULA DEFINED / COMPONENT INPUT
- C8 Global Leading: FORMULA DEFINED / COMPONENT INPUT
- `Strategy Action Index`: FORMULA ACTIVATED; runtime numeric output permitted only when Section 50 gate passes
- `AI Master Score`: DATA UNAVAILABLE

Activation-gate result for Strategy Action Index v1:
1. Formula -> DEFINED
2. Mandatory inputs -> DEFINED
3. Component normalization -> DEFINED in C1-C8
4. Global weights / aggregation -> DEFINED
5. Missing-data rule -> DEFINED
6. Partial-data rule -> DEFINED
7. Range -> DEFINED [-1,+1]
8. Action Bands -> DEFINED
9. Calculation procedure -> DEFINED
10. Formula/regression tests -> PASS BY RULE DESIGN

Empirical optimization / out-of-sample market backtest remains NOT ESTABLISHED and must not be claimed.

## 58. Final Principle
A valid Strategy Action Index requires official C1-C8 formulas + global data gate + reproducible aggregation + validation.
No valid runtime inputs = `Strategy Action Index: DATA UNAVAILABLE`.

Strategy Action Index = execution bias, not automatic trade.
AI Master Score remains separate and DATA UNAVAILABLE.
Adaptive priority != numeric weight.
Conflict is information, not noise to average away.
Reliability > Speed.
DATA UNAVAILABLE is preferable to fabricated precision.