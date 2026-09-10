# AI Market Master 3.2 Scoring Rule

Version: 3.2 Unified Stable
Status: Scoring Authority

## 1. Scope
This file is the only authority for numeric `AI Master Score` and `Strategy Action Index` definitions, inputs, weights, formulas, missing-data handling and validation.

Validated numeric sub-components do not activate the global Strategy Action Index unless the full Numeric Score Activation Gate is satisfied.

## 2. Current Official Status
Official current global numeric state:
- `AI Master Score: DATA UNAVAILABLE`
- `Strategy Action Index: DATA UNAVAILABLE`

Defined component specifications:
- `SAI-C1 Smart Money`
- `SAI-C2 Program Flow`
- `SAI-C3 Breadth / Market Internal`
- `SAI-C4 Sector / Leadership`
- `SAI-C5 Technical Structure`
- `SAI-C6 Liquidity / Macro`
- `SAI-C7 Volatility / Derivatives Risk`

None may be presented alone or in combination as the final Strategy Action Index until the global activation gate is complete.

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

Until then, global numeric output is prohibited.

## 4. Global Scoring Firewalls
Never infer a global score from qualitative signal colors, Market Regime, Transition, VH/H/M/L Evidence Priority, qualitative Strategy posture, analyst intuition, prior displayed numbers, indicator counts or hidden weights.

Missing mandatory data is never silently converted to zero/Neutral. Partial formulas are allowed only when explicitly predefined here.

Confidence and Regime Confidence are non-numeric evidence-quality labels, not market scores or probabilities.

Binance does not create a separate market score. Binance G1-G6/E8 data may enter future numeric scoring only after an explicit formula revision.

## 5. Cross-Component Ownership Map
- C1 / E1: Smart Money
- C2 / E2: Program Flow
- C3 / E3: Breadth / Internal
- C4 / E4: Sector / Leadership
- C5 / E5: Technical Structure
- C6 / E6: Liquidity / Macro
- C7 / E7: Volatility / Derivatives Risk
- E8: Global Leading / Binance — no numeric SAI component yet

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
- all three valid → VERIFIED
- Institution missing → `0.50*N_FC + 0.50*N_FF` / PARTIAL
- Foreign Cash or Foreign Futures missing/invalid denominator → DATA UNAVAILABLE

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
- both valid → VERIFIED
- Arbitrage missing, Non-Arbitrage valid → `C2=N_NONARB` / PARTIAL
- Non-Arbitrage missing/invalid → DATA UNAVAILABLE

`C2 Conflict: ACTIVE` when signs oppose and both |N|>=0.30.

`C2 Shock: ACTIVE` when:
- |Arbitrage/KOSPI traded value| >=1.125%
- |Non-Arbitrage/KOSPI traded value| >=2.25%

Known expiry/index/sector/ETF rebalance or comparable mechanical event → `C2 Mechanical Event: ACTIVE`. Calculate C2, but Arbitrage alone cannot create a structural Regime conclusion.

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
- KOSPI + KOSDAQ valid → VERIFIED
- KOSDAQ missing → `C3=N_K` / PARTIAL
- KOSPI invalid/missing or ADV_K+DEC_K<=0 → DATA UNAVAILABLE

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
- 8/8 + valid KOSPI comparator → eligible VERIFIED
- 6-7/8 + valid comparator → PARTIAL
- <6/8 or invalid/asynchronous KOSPI comparator → DATA UNAVAILABLE

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
- all three valid → VERIFIED
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

Korea Treasury 3Y is domestic financial-condition input; TMF remains E8 and is not re-scored in C6.

# SAI-C7 Volatility / Derivatives Risk

## 24. Purpose and Boundary
`SAI-C7 Volatility / Derivatives Risk` is the seventh formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether domestic volatility and derivatives-price structure indicate risk expansion or normalization while avoiding false direction from OI, isolated option strikes, expiry mechanics or duplicated global-leading derivatives data.

Authority boundary:
- Numeric C7 formula, normalization, missing/partial handling and C7 Conflict/Shock conditions are owned by this SCORING_RULE.
- `E7 Volatility / Derivatives Risk` remains the qualitative/adaptive owner for volatility, options, OI and derivatives-risk structure, Market Regime, Transition and VH/H/M/L Evidence Priority.
- C7 is a numeric sub-component, not a new engine or Evidence Group.
- C7 cannot select or reconfirm a Market Regime by itself.

## 25. Timeframe / Source Standard
Official C7 v1 uses completed Korean-market observations when available.
Source priority follows MASTER_RULE: HTS/KRX/official domestic data first, then verified official supplementary data.

Intraday values may be shown as `C7 Intraday Preview`; they do not overwrite the latest completed/validated C7 by themselves.

VOL requires VKOSPI spot or a validated official equivalent plus enough history to calculate a 20-observation moving average.
VKOSPI futures do not silently replace VKOSPI spot because futures contain expiry/term-structure effects.

BASIS requires same-session:
- Actual KOSPI200 futures basis
- Theoretical/Fair basis
- KOSPI200 spot/index denominator

Raw basis sign alone must not be scored because normal basis depends on rates, dividends and time to expiry.

## 26. C7-A Volatility Stress
`VOL_REL = VKOSPI_t / VKOSPI_MA20 - 1`
`VOL = -clip(VOL_REL / 0.30,-1,+1)`

Interpretation:
- VKOSPI 30% or more above its MA20 -> VOL=-1.00
- at MA20 -> 0
- 30% or more below MA20 -> VOL=+1.00

VKOSPI absolute level is context only in v1 and is not separately added as another numeric term.

## 27. C7-B Basis Stress
`BasisGap = ActualBasis - FairBasis`
`BG = BasisGap / KOSPI200Spot`
`BASIS = clip(BG / 0.003,-1,+1)`

Interpretation:
- fair-value-adjusted +0.30% premium or more -> BASIS=+1.00
- fair basis alignment -> 0
- fair-value-adjusted -0.30% discount or less -> BASIS=-1.00

BASIS is optional because fair/theoretical basis may require a separate HTS lookup.

## 28. SAI-C7 Formula / Missing / Partial
When VOL and BASIS are both valid:
`SAI-C7 = 0.60*VOL + 0.40*BASIS`
Status: eligible for VERIFIED when source/session/unit validation passes.

Range:
`-1.00 <= SAI-C7 <= +1.00`

Internal weights:
- Volatility Stress 60%
- Basis Stress 40%

If VOL is valid and BASIS unavailable:
`SAI-C7 = VOL`
Status: PARTIAL.

If VOL is unavailable/invalid:
`SAI-C7 = DATA UNAVAILABLE`, even if BASIS is available.

Missing data is never converted to zero/Neutral. The VOL-only partial formula is predefined and is not silent reweighting.

## 29. OI / Options / Volatility-Futures Boundary
The following are contextual validation inputs or flags only in C7 v1, not direct numeric terms:
- KOSPI200 futures OI and OI change
- Call/Put OI and volume at isolated strikes
- full-market Put/Call Ratio when available
- volatility futures and volatility term structure
- rollover/expiry positioning

Reason:
- OI increase is directionless without price/position context
- one strike cannot represent the full options market
- PCR can reflect fear/hedging or contrarian extremes depending on context
- volatility futures contain term-structure/expiry effects

Examples of permitted context:
- Price down + OI up -> possible new short/hedge expansion
- Price up + OI up -> possible new long expansion
- Price down + OI down -> possible long liquidation

These labels do not alter C7 numeric weights ad hoc.

## 30. C7 Conflict Rule
Raise `C7 Conflict: ACTIVE` when:
- VOL and BASIS have opposite signs, and
- both satisfy `|value| >= 0.50`.

When active:
- keep the 60/40 formula unchanged
- disclose the conflict
- do not interpret a near-zero aggregate as absence of information
- pass the conflict to ADAPTIVE_VALIDATION_RULE / Change Detection
- reduce Confidence when materially decision-relevant under owning rules

## 31. C7 Shock / Mechanical Event
Raise `C7 Shock: ACTIVE` when any validated condition includes:
- `|VKOSPI/VKOSPI_MA20 - 1| >= 45%`, or
- `|BasisGap/KOSPI200Spot| >= 0.45%`, or
- VOL and BASIS are both <=-0.80 with independent derivatives-risk confirmation.

The third condition is a same-direction downside stress confirmation, not a new numeric contribution.

Raise `C7 Mechanical Event: ACTIVE` for derivatives expiry, rollover, major index/sector rebalance or comparable market-structure event that can distort OI, option prices or basis.

C7 Shock/Mechanical Event feed Change Detection / Transition / Regime re-validation only. They do not automatically change Market Regime, global SAI, portfolio action or permanent Base Weight.

## 32. C7 Anti-Double-Counting / Anti-Circularity
For C7 numeric scoring:
- VKOSPI spot relative-to-MA20 stress is scored once in VOL
- VKOSPI absolute level and volatility futures are contextual only
- fair-value-adjusted KOSPI200 basis is scored once in BASIS
- OI/PCR/isolated option-strike data remain context/flags only
- Smart Money stays C1/E1
- Program stays C2/E2
- Breadth stays C3/E3
- Sector Leadership stays C4/E4
- Technical price structure stays C5/E5
- Liquidity/Macro stays C6/E6
- Binance OI/Funding/Long-Short and TMF/SPY/QQQ/BTC/EWY/SOXL stay E8 and are not re-scored in C7

Required separation:
`Validated Domestic Volatility/Derivatives Data -> C7 Calculation`

and independently:
`Raw HTS + other Evidence -> Preliminary Regime -> Adaptive Priority -> Transition/Conflict -> Regime Re-validation`

C7 must not choose a Regime, use that Regime to alter its own weights, and then use altered C7 as the sole reason to reconfirm the same Regime. VH/H/M/L remains qualitative only.

## 33. C7 Validation Cases
A. `VOL=-1.00, BASIS=-1.00 -> C7=-1.00`.
B. `VOL=+1.00, BASIS=+0.50 -> C7=+0.80`.
C. `VOL=-0.80, BASIS=+0.70 -> C7=-0.20 + C7 Conflict: ACTIVE`.
D. `VOL=-0.60, BASIS unavailable -> C7=-0.60 / PARTIAL`.
E. VOL unavailable, BASIS=-1.00 -> DATA UNAVAILABLE.
F. OI surge alone -> no direct C7 direction.
G. one ATM Call/Put strike only -> no official PCR.
H. volatility futures move without VKOSPI spot -> context only; cannot create VERIFIED C7.
I. expiry/rollover distortion -> Mechanical Event; no structural Regime conclusion by itself.
J. |VKOSPI/MA20-1|>=45% -> Shock while VOL remains clipped at +/-1.

Result: PASS by rule design.

## 34. Current Component / Global SAI Status After C7
- C1 Smart Money: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- C2 Program Flow: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- C3 Breadth / Market Internal: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- C4 Sector / Leadership: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- C5 Technical Structure: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- C6 Liquidity / Macro: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- C7 Volatility / Derivatives Risk: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- Strategy Action Index: DATA UNAVAILABLE
- AI Master Score: DATA UNAVAILABLE

Global SAI remains unavailable until remaining required components, global aggregation, global missing/partial handling, final range/Action Bands and regression validation are complete.

## 35. Future Formula Adoption Procedure
Before activating global Strategy Action Index:
1. identify source/version
2. define every required component and global formula
3. document mandatory inputs and units
4. define normalization and aggregation
5. define global missing/partial handling
6. verify no conflict with MASTER/DASHBOARD/TECHNICAL/BINANCE/ADAPTIVE_VALIDATION
7. test known and stress cases
8. define output range and Action Bands
9. update VERSION_STATUS and CHANGELOG
10. only then change official global status from DATA UNAVAILABLE

## 36. Final Principle
No complete official global formula = no official global number.
A validated sub-component does not equal Strategy Action Index.
Adaptive priority != numeric weight.
Reliability > Speed.
DATA UNAVAILABLE is preferable to fabricated precision.
