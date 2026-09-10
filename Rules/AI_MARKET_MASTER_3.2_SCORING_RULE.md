# AI Market Master 3.2 Scoring Rule

Version: 3.2 Unified Stable
Status: Scoring Authority

## 1. Scope
This file is the only authority for numeric `AI Master Score` and `Strategy Action Index` definitions, inputs, weights, formulas, missing-data handling and validation.

It may also define validated numeric sub-components used by a future complete Strategy Action Index. A sub-component does not activate the global Strategy Action Index unless the full Numeric Score Activation Gate is satisfied.

## 2. Current Official Status
No complete reproducible global formula for either score has yet been adopted.

Therefore the official current numeric state remains:
- `AI Master Score: DATA UNAVAILABLE`
- `Strategy Action Index: DATA UNAVAILABLE`

Defined component specifications:
- `SAI-C1 Smart Money`
- `SAI-C2 Program Flow`
- `SAI-C3 Breadth / Market Internal`
- `SAI-C4 Sector / Leadership`
- `SAI-C5 Technical Structure`
- `SAI-C6 Liquidity / Macro`

None may be presented alone or in combination as the final Strategy Action Index until the global activation gate is complete.

## 3. Numeric Score Activation Gate
A global numeric score may be activated only after all of the following are explicitly defined and verified in this file:
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

## 4. No Reverse Engineering by Guess
Do not infer a formula from legacy score labels, traffic-light colors, qualitative judgments, portfolio actions, analyst intuition, previous displayed numbers without documented calculation rules, Market Regime labels, Transition labels, VH/H/M/L Evidence Priority or qualitative Strategy postures.

A signal label, Regime or qualitative priority does not create a score band.

## 5. Category Score / Indicator Distinction
Dashboard categories may show verified Score / Indicator values even when the two official global numeric scores are unavailable.
Valid indicators can include Foreign Spot/Futures flow, Program flow, Breadth, RSI, MACD, ADX, Funding, OI/OI change, Customer Deposits/Margin Credit, Support/Resistance, AI-cycle indicators and qualitative Evidence Priority when sourced from its owning rule.

Indicators are not automatically global score components unless this SCORING_RULE explicitly defines them.

## 6. Qualitative Signals
Canonical qualitative signals remain:
🟢 Strong Bull / Positive
🔵 Bull
🟡 Neutral
🟠 Warning / Caution
🔴 Bear / Negative
⚫ Extreme Risk
⚪ DATA UNAVAILABLE

Qualitative signals must never be mathematically converted into unofficial numeric scores.

## 7. Adaptive Evidence Firewall
`ADAPTIVE_VALIDATION_RULE` owns Market Regime, Transition, E1-E8 Evidence Groups, VH/H/M/L Evidence Priority and qualitative Strategy posture.

Prohibited unless explicitly defined and validated here:
- VH/H/M/L → numbers or percentages
- Regime labels → fixed score bands
- Strategy posture → Strategy Action Index number
- signal count → numeric score
- hidden analyst weighting of adaptive Evidence Groups
- silent normalization/reweighting based on missing adaptive inputs

Adaptive Evidence Priority is not numeric weight.

## 8. Confidence Is Not Score
High / Medium / Low Confidence reflects evidence strength, completeness, freshness and agreement. Confidence and Regime Confidence are not probabilities or scores.

## 9. Missing Data
Missing mandatory data follows each component's explicit rule. If no rule exists, output `DATA UNAVAILABLE`. Missing data is never silently converted to zero/Neutral.

## 10. Partial Score Rule
A partial numeric component is allowed only when the component explicitly defines which inputs may be missing, the predefined partial formula, output label and minimum completeness. Otherwise use `DATA UNAVAILABLE`.

## 11. Binance Integration
Binance does not create a separate AI Market Master numeric score. Binance G1-G6/E8 data may feed future scoring only if a formula explicitly defines its role. Binance status itself is not a market score.

## 12. Strategy Action Index Principle
When eventually activated, Strategy Action Index must represent execution intensity through a reproducible official formula. Qualitative Strategy postures are not SAI numbers. Until the global formula is complete, output `DATA UNAVAILABLE` while allowing qualitative strategy under the owning rules.

## 13. AI Master Score Principle
AI Master Score must represent integrated market evidence through a reproducible official formula and cannot be inferred from Final Signal, Market Regime, Evidence Priority or Portfolio Action. Until formally defined, output `DATA UNAVAILABLE`.

## 14. Regression Protection
Always invalid:
- incomplete mandatory inputs + invented score
- signal color converted to number without formula
- qualitative consensus converted to percentage
- score copied from earlier session without recomputation
- hidden/manual analyst weighting
- silent weight renormalization except predefined partial formulas
- VH/H/M/L converted to numeric values
- Market Regime converted to score by intuition
- one sub-component or incomplete component set presented as global SAI

## 15. Cross-Component Ownership Map
- C1 / E1: Smart Money
- C2 / E2: Program Flow
- C3 / E3: Breadth / Internal
- C4 / E4: Sector / Leadership
- C5 / E5: Technical Structure
- C6 / E6: Liquidity / Macro
- E7: Volatility / Derivatives Risk — no numeric SAI component yet
- E8: Global Leading / Binance — no numeric SAI component yet

The same underlying datum must not be counted as independent confirmation in multiple components.

# SAI-C1 Smart Money

## 16. Purpose and Boundary
Measures whether major directional capital in the Korean equity market is increasing or reducing risk exposure.
Numeric rules are owned here; E1 interpretation/Regime/Transition/VH-H-M-L remain owned by ADAPTIVE_VALIDATION_RULE.

## 17. Inputs
Required:
- Foreign KOSPI cash net flow, KRW amount aligned to KOSPI traded-value unit
- Foreign KOSPI200 futures net contracts, denominator = total KOSPI200 futures OI contracts

Optional:
- Institutional KOSPI cash net flow, KRW amount aligned to KOSPI traded-value unit

Excluded from independent C1 scoring: Program/Arbitrage/Non-Arbitrage, Breadth/ADL, Options, Financial Investment when already inside Institution total, cumulative futures position when current flow is scored, OI change as separate directional score.

## 18. Normalization
`FC = Foreign KOSPI Cash Net Flow / KOSPI Total Traded Value`
`N_FC = clip(FC / 0.015,-1,+1)`

`FF = Foreign KOSPI200 Futures Net Contracts / KOSPI200 Futures Total OI`
`N_FF = clip(FF / 0.10,-1,+1)`

`IC = Institutional KOSPI Cash Net Flow / KOSPI Total Traded Value`
`N_IC = clip(IC / 0.010,-1,+1)`

All normalized values are clipped to [-1,+1].

## 19. Formula
Full:
`SAI-C1 = 0.40*N_FC + 0.40*N_FF + 0.20*N_IC`
Range [-1,+1].

## 20. Missing / Partial
- all three valid → VERIFIED
- institution missing only → `C1 = 0.50*N_FC + 0.50*N_FF` / PARTIAL
- Foreign Cash or Foreign Futures missing/invalid denominator → DATA UNAVAILABLE

## 21. Conflict / Shock
`C1 Conflict: ACTIVE` when Foreign Cash and Foreign Futures are materially opposed; disclose conflict without ad hoc reweighting.

`C1 Shock: ACTIVE` candidate when:
- |Foreign Cash / KOSPI Traded Value| >= 2.25%
- |Foreign Futures / Total OI| >= 15%
- |Institution Cash / KOSPI Traded Value| >= 1.50%

Shock feeds Change Detection only; no automatic Regime/global SAI/portfolio/permanent-weight change.

## 22. Anti-Double-Counting / Anti-Circularity
Each current flow is scored once. Program remains C2, Breadth C3, Options/OI risk E7. C1 cannot select a Regime, alter itself from that Regime, then reconfirm the same Regime.

## 23. Validation Cases
- `N_FC=.75,N_FF=.60,N_IC=.30` → C1=.60
- `N_FC=-.70,N_FF=-.80,N_IC=-.20` → C1=-.64
- `.70,-.90,.20` → C1=-.04 + Conflict
- institution missing with `.60,.80` → C1=.70 / PARTIAL
- mandatory input missing → DATA UNAVAILABLE

# SAI-C2 Program Flow

## 24. Purpose and Boundary
Measures whether KOSPI program trading supplies or withdraws liquidity while separating structural Non-Arbitrage flow from more mechanical Arbitrage flow. E2 remains the adaptive interpretation owner.

## 25. Inputs
- Arbitrage Program net flow, KRW — optional/supplementary/mechanical-sensitive
- Non-Arbitrage Program net flow, KRW — required structural core
- Total Program net flow — reconciliation/context only, not an extra score

## 26. Normalization
`ARB = Arbitrage Program Net Flow / KOSPI Total Traded Value`
`N_ARB = clip(ARB / 0.0075,-1,+1)`

`NONARB = Non-Arbitrage Program Net Flow / KOSPI Total Traded Value`
`N_NONARB = clip(NONARB / 0.015,-1,+1)`

## 27. Formula
`SAI-C2 = 0.30*N_ARB + 0.70*N_NONARB`
Range [-1,+1].

## 28. Missing / Partial
- both valid → VERIFIED
- Arbitrage missing, Non-Arbitrage valid → `C2=N_NONARB` / PARTIAL
- Non-Arbitrage missing/invalid → DATA UNAVAILABLE

## 29. Conflict / Shock / Mechanical Event
`C2 Conflict: ACTIVE` when signs oppose and both |N|>=0.30. Formula unchanged; Non-Arbitrage retains structural priority.

`C2 Shock: ACTIVE` when:
- |Arbitrage/KOSPI traded value| >=1.125%
- |Non-Arbitrage/KOSPI traded value| >=2.25%

Known expiry/index/sector/ETF rebalance or comparable mechanical event → `C2 Mechanical Event: ACTIVE`. Calculate C2, but Arbitrage alone cannot create structural Regime conclusion. No automatic numeric weight change.

## 30. Anti-Double-Counting / Anti-Circularity
Total Program is not scored after components. Foreign/Institution flow remains C1, Breadth C3, Technical C5, Options/OI/Volatility E7. C2 cannot circularly select/reweight/reconfirm Regime.

## 31. Validation Cases
- `N_ARB=.50,N_NONARB=.70` → C2=.64
- `-.40,-.80` → -.68
- `+1,-.60` → -.12 + Conflict
- Arbitrage missing, Non-Arb=.65 → .65 / PARTIAL
- Non-Arb missing → DATA UNAVAILABLE

# SAI-C3 Breadth / Market Internal

## 32. Purpose and Boundary
Measures whether domestic market participation is broadening or deteriorating beneath the headline index. E3 remains the adaptive interpretation owner.

## 33. Inputs
Required KOSPI active breadth:
- ADV_K
- DEC_K
UNCH_K is context/validation.

Optional KOSDAQ confirmation:
- ADV_Q
- DEC_Q
UNCH_Q is context/validation.

Isolated raw ADL absolute level is contextual only in v1 because comparable accumulation history is required for numeric use.

## 34. Normalization
If ADV_K+DEC_K>0:
`B_K=(ADV_K-DEC_K)/(ADV_K+DEC_K)`
`N_K=clip(B_K/0.50,-1,+1)`

If ADV_Q+DEC_Q>0:
`B_Q=(ADV_Q-DEC_Q)/(ADV_Q+DEC_Q)`
`N_Q=clip(B_Q/0.50,-1,+1)`

Unchanged issues do not create directional points.

## 35. Formula
`SAI-C3 = 0.70*N_K + 0.30*N_Q`
Range [-1,+1].

## 36. Missing / Partial
- KOSPI + KOSDAQ valid → VERIFIED
- KOSDAQ missing only → `C3=N_K` / PARTIAL
- KOSPI breadth missing/invalid or ADV_K+DEC_K<=0 → DATA UNAVAILABLE

## 37. Conflict / Divergence / Shock
`C3 Conflict: ACTIVE` when N_K and N_Q oppose and both |N|>=0.30.

KOSPI return is comparator only. `C3 Divergence: ACTIVE` when:
- KOSPI return>0 and N_K<=-0.30
- KOSPI return<0 and N_K>=+0.30

`C3 Shock: ACTIVE` when:
- |B_K|>=0.75, or
- KOSPI/KOSDAQ breadth same direction and both |B|>=0.65

Flags feed Change Detection/Transition only.

## 38. Anti-Double-Counting / Anti-Circularity
KOSPI/KOSDAQ breadth scored once. Raw ADL contextual. Index returns comparator only. Program C2, Smart Money C1, Technical C5, derivatives risk E7. C3 cannot circularly select/reweight/reconfirm Regime.

## 39. Validation Cases
- KOSPI 600/300 => N_K=.6667; KOSDAQ 1000/600 => N_Q=.50; C3≈.6167
- KOSPI 250/650 => -.8889; KOSDAQ 500/1100 => -.75; C3≈-.8472
- N_K=.60,N_Q=-.50 → C3=.27 + Conflict
- KOSDAQ missing,N_K=-.55 → -.55 / PARTIAL
- KOSPI missing → DATA UNAVAILABLE

# SAI-C4 Sector / Leadership

## 40. Purpose and Boundary
Measures sector participation and KOSPI-relative leadership while preventing theme/index overlap from becoming independent evidence. E4 remains qualitative/adaptive owner.

## 41. Fixed Sector Universe v1
Exactly eight canonical benchmark identities:
1. Semiconductor — KRX Semiconductor Index
2. Automobile — KRX Automobile Index
3. Secondary Battery — KRX Secondary Battery TOP 10 Index
4. Financials — KOSPI 200 Financial Index
5. Shipbuilding — iSelect Shipbuilding TOP10 Index (PR)
6. Defense — iSelect Defense TOP10 Index (Price Return)
7. AI Power Infrastructure — KRX-Akros AI Power Infrastructure Index
8. Bio — KRX Bio TOP 10 Index

Canonical identity = provider + exact benchmark name. ETF ticker/code is not benchmark index code. Verified HTS short code may be alias only. Ambiguous mapping = unavailable. Universe changes require formal SCORING_RULE revision.

## 42. Data Standard
Source priority follows MASTER_RULE. Required: KOSPI daily return plus same-session daily returns for available fixed-universe benchmarks. Mixed-session/asynchronous data is not silently combined. ETF return is contextual verification only, not silent numeric replacement.

## 43. Sector Direction Breadth
For each valid sector return r_i:
- r_i > +0.20% → D_i=+1
- r_i < -0.20% → D_i=-1
- otherwise D_i=0

`SD=(UP-DOWN)/N_valid`
Range [-1,+1].

## 44. Relative Leadership Breadth
`RS_i = SectorReturn_i - KOSPIReturn`
- RS_i > +0.20%p → L_i=+1
- RS_i < -0.20%p → L_i=-1
- otherwise 0

`RL=(OUT-UNDER)/N_valid`
Range [-1,+1]. KOSPI is comparator only.

## 45. Formula / Completeness
`SAI-C4=0.60*SD+0.40*RL`
Range [-1,+1].

- 8/8 + valid KOSPI comparator → eligible VERIFIED
- 6-7/8 + valid comparator → PARTIAL using valid fixed-universe sectors
- <6/8 → DATA UNAVAILABLE
- invalid/missing/asynchronous KOSPI comparator → DATA UNAVAILABLE

Missing sectors are excluded, never neutralized.

## 46. Leadership Concentration / Conflict / Shock
Leadership Concentration is qualitative/contextual under E4, not a direct numeric C4 term. States may include BROAD/NORMAL/CONCENTRATED/EXTREME; no unvalidated concentration ratio changes C4.

`C4 Conflict: ACTIVE` when SD and RL have opposite signs and both |value|>=0.50.

`C4 Shock: ACTIVE` when:
- |SD|>=0.75, or
- SD/RL same sign and both |value|>=0.60

No automatic Regime/global SAI/portfolio/permanent-weight change.

## 47. Anti-Double-Counting / Anti-Circularity
SD and RL are transforms of the same fixed sector-return set, not independent Evidence Groups. Smart Money C1, Program C2, Breadth C3, Technical C5, AI fundamentals separate, derivatives E7, Binance/global E8. C4 cannot circularly select/reweight/reconfirm Regime.

## 48. Validation Cases
- SD=-1,RL=+1 → C4=-.20 + Conflict
- six valid sectors + KOSPI → PARTIAL
- five or fewer sectors → DATA UNAVAILABLE
- missing KOSPI comparator → DATA UNAVAILABLE
- |SD|>=.75 → Shock flag while formula remains bounded

# SAI-C5 Technical Structure

## 49. Purpose and Boundary
Measures whether KOSPI technical price structure confirms strength or deterioration using closing-confirmed Price Structure, validated Support/Resistance position and MA/VWAP Trend Position while minimizing repeated scoring of price-derived indicators.

TECHNICAL_RULE remains calculation/interpretation authority; E5 remains adaptive qualitative owner.

## 50. Timeframe and Data Standard
Official C5 v1 uses KOSPI Daily / Closing-confirmed structure. Intraday data may produce only `C5 Intraday Preview` and cannot overwrite the latest closing-confirmed C5 by itself.

Validated TECHNICAL_RULE outputs:
- recent confirmed daily swing structure for PS
- nearest validated major Support Cluster S and Resistance Cluster R for SR when available
- MA20, MA60, VWAP20, VWAP60 for TP when available
- aligned daily close

Volume, RSI, MACD, ADX, Ichimoku and Elliott/Fibonacci are confirmation/context, not direct C5 numeric terms.

## 51. Price Structure Score PS
Mandatory directional core:
- HH+HL → PS=+1.00
- LH+LL → PS=-1.00
- HH+LL or LH+HL / non-directional → 0
- one-sided validated improvement → +0.50
- one-sided validated deterioration → -0.50

Closing-confirmed breakout above relevant validated swing-high/resistance may set +1; confirmed breakdown below swing-low/support may set -1. Intraday touch alone cannot. Insufficient swing identity => PS unavailable.

## 52. Support / Resistance Score SR
With validated S<R and close C inside intact corridor:
`X=clip(2*(C-S)/(R-S)-1,-1,+1)`
`SR=0.50*X`
Thus intact corridor contributes [-.50,+.50].

Confirmed closing breakout above R → SR=+1.00.
Confirmed closing breakdown below S → SR=-1.00.
Touch alone does not create ±1. Fibonacci/Elliott/MA/VWAP/previous highs-lows may validate clusters but are not re-added numerically.

## 53. MA / VWAP Trend Position TP
Fixed anchors: MA20, MA60, VWAP20, VWAP60.
For each valid A_j:
- Close > A_j*1.002 → T_j=+1
- Close < A_j*0.998 → T_j=-1
- otherwise 0

`TP=average(T_j)`.
- 4/4 anchors → full TP
- 2-3 anchors → usable but overall C5 PARTIAL
- <2 → TP unavailable

## 54. Formula / Missing / Partial
Full:
`SAI-C5=0.50*PS+0.30*SR+0.20*TP`
Range [-1,+1].

SR missing only:
`C5=0.70*PS+0.30*TP` / PARTIAL

TP missing only:
`C5=0.625*PS+0.375*SR` / PARTIAL

PS unavailable/invalid, or PS valid but both SR and TP unavailable → DATA UNAVAILABLE.

## 55. Confirmation / Conflict / Divergence / Shock
Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci remain contextual validation. ADX is strength, not direction.

`C5 Divergence: ACTIVE` when price-vs-RSI/MACD divergence is validated and material.

`C5 Conflict: ACTIVE` when:
- PS and SR oppose and both |value|>=0.50, or
- PS and TP oppose and both |value|>=0.50

`C5 Shock: ACTIVE` for confirmed major Support breakdown, confirmed major Resistance breakout, or current TECHNICAL_RULE Recovery Structure Failure trigger including closing break below Correction Low 5,593.

Flags do not alter formula ad hoc and do not automatically change Regime/global SAI/portfolio/permanent weight.

## 56. Anti-Double-Counting / Anti-Circularity
PS, SR and TP form one E5/C5 technical family, not three independent Evidence Groups. Volume/Momentum/Elliott/Fibonacci are not extra numeric terms. Breadth C3, sector C4, Smart Money C1, Program C2, Liquidity C6, derivatives E7, global E8 remain separate. C5 cannot circularly select/reweight/reconfirm Regime.

## 57. Validation Cases
- PS=1,SR=.4,TP=1 → C5=.82
- PS=-1,SR=-1,TP=-1 → -1
- PS=1,SR=-.4,TP=.5 → .48
- PS=1,SR=.2,TP=-.75 → .41 + Conflict
- SR missing: PS=1,TP=.5 → .85 / PARTIAL
- TP missing: PS=-1,SR=-.5 → -.8125 / PARTIAL
- PS missing → DATA UNAVAILABLE
- volume spike alone → no directional C5 contribution
- intraday breakout without close → preview only
- close below 5,593 → C5 Shock + Recovery Structure Failure review

# SAI-C6 Liquidity / Macro

## 58. Purpose and Boundary
`SAI-C6 Liquidity / Macro` is the sixth formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether domestic financial conditions are becoming more supportive or restrictive for Korean equities using FX pressure, domestic rate pressure and investable cash liquidity, while separating leverage-risk and lower-frequency macro context from the direct daily numeric score.

Authority boundary:
- Numeric C6 formula, normalization, internal weights, freshness/completeness rules and C6 conflict/shock conditions are owned by this SCORING_RULE.
- `E6 Liquidity / Macro` remains the qualitative/adaptive owner for USD/KRW, rates, deposits, margin/credit, broader liquidity conditions, Market Regime, Transition and VH/H/M/L Evidence Priority.
- MASTER_RULE Engine 06 remains the Global Liquidity analysis engine; C6 is a numeric sub-component, not a new engine.
- C6 cannot select or reconfirm a Market Regime by itself.

## 59. Timeframe / Source / Point-in-Time Standard
Official C6 v1 uses the latest completed Korean-market daily observation set available at execution time.

Source priority follows MASTER_RULE:
1. user-provided HTS/KRX or official domestic market data
2. verified official domestic data providers
3. other verified supplementary sources

FX and Korea Treasury 3Y inputs use completed daily observations. Intraday current values may be shown only as `C6 Intraday Preview` and do not overwrite the latest official completed-daily C6 by themselves.

Customer Deposits use the latest officially published observation available at execution time. Its observation date must be disclosed when it differs from the FX/rate reference date. Its 5-observation change is measured from that series' own observation dates; unavailable future/revised information must not be backfilled into an earlier point-in-time calculation.

Unknown source date, invalid unit, or an observation that cannot be aligned to a valid 5-observation comparison makes that input unavailable.

## 60. C6-A FX Pressure
Input: USD/KRW daily close or validated equivalent.

`FX_raw = USDKRW_t / USDKRW_t-5 - 1`
`FX = -clip(FX_raw / 0.020,-1,+1)`

Interpretation:
- USD/KRW +2.0% over 5 completed observations or more → FX=-1.00
- no change → 0
- USD/KRW -2.0% or more → FX=+1.00

The negative sign reflects tighter Korean risk-asset financial conditions from material KRW weakness. The absolute USD/KRW level is context only in C6 v1 and is not an additional numeric term.

## 61. C6-B Domestic Rate Pressure
Input: Korea Treasury 3Y yield, daily closing yield or validated official equivalent.

Let `dY5_bp` = current 3Y yield minus the 5-observation-prior yield, expressed in basis points.

`RATE = -clip(dY5_bp / 20,-1,+1)`

Interpretation:
- +20bp or more over 5 completed observations → RATE=-1.00
- unchanged → 0
- -20bp or less → RATE=+1.00

A rate decline caused by stress/recession does not automatically create a bullish Market Regime. Such meaning is resolved through E6/E7/E8 and cross-engine validation rather than changing this numeric transform ad hoc.

## 62. C6-C Cash Liquidity
Input: official Customer Deposits / investor cash-deposit series used as stock-market waiting cash.

`DEP5 = Deposit_t / Deposit_t-5 - 1`
`CASH = clip(DEP5 / 0.05,-1,+1)`

Interpretation:
- +5.0% over 5 valid observations or more → CASH=+1.00
- unchanged → 0
- -5.0% or less → CASH=-1.00

Absolute deposit level is context only in v1. Observation date must be preserved; the latest published value must not be mislabeled as same-session if publication timing differs.

## 63. SAI-C6 Formula
When FX, RATE and CASH are all valid:
`SAI-C6 = 0.35*FX + 0.35*RATE + 0.30*CASH`

Component range:
`-1.00 <= SAI-C6 <= +1.00`

Internal weights:
- FX Pressure 35%
- Domestic Rate Pressure 35%
- Cash Liquidity 30%

Rationale:
FX and domestic rates directly reflect daily financial-condition pressure and receive equal structural weight. Customer Deposits add domestic deployable-liquidity confirmation without being allowed to dominate market-price financing conditions.

These C6 internal weights do not define the future global weight of C6 inside the complete Strategy Action Index.

## 64. C6 Missing / Partial Rule
Full C6:
- FX + RATE + CASH valid → VERIFIED when source/date/unit validation passes.

FX missing only:
`C6 = 0.5385*RATE + 0.4615*CASH`
Status: PARTIAL.

RATE missing only:
`C6 = 0.5385*FX + 0.4615*CASH`
Status: PARTIAL.

CASH missing only:
`C6 = 0.50*FX + 0.50*RATE`
Status: PARTIAL.

Minimum gate:
- at least two distinct C6 axes must be valid, and
- at least one of FX or RATE must be present.

One axis alone, CASH alone, or invalid 5-observation comparison → `SAI-C6 = DATA UNAVAILABLE`.
Missing values are never converted to zero/Neutral.
The partial formulas are predefined and are not silent reweighting.

## 65. Margin Credit / Structural Macro Boundary
Margin Credit is not a direct numeric C6 term in v1 because rising credit can simultaneously indicate buying liquidity and leverage fragility.

Permitted qualitative E6/E7 context includes:
- deposits weakening while margin credit rises → credit-stress / leverage-quality warning
- deposits strengthening while margin credit rises rapidly → liquidity expansion with overheat watch
- deposits strengthening while margin credit is stable → healthier liquidity-quality context
- deposits and margin credit both contracting → deleveraging/liquidity-contraction context

No fixed numeric margin-credit bonus/penalty is adopted in C6 v1. Any future numeric use requires a separately validated formula and explicit anti-double-counting with E7.

Policy Rate, M2 and other lower-frequency liquidity/macro series remain Structural Macro Context in v1. They may inform E6 interpretation or Change Detection when a verified structural shift occurs, but they are not silently inserted into the daily C6 number and do not alter C6 weights ad hoc.

## 66. C6 Conflict Rule
Raise `C6 Conflict: ACTIVE` when any two available numeric C6 axes:
- have opposite signs, and
- both satisfy `|value| >= 0.50`.

Examples:
- KRW strengthens while domestic rates tighten sharply
- FX/RATE conditions improve while deployable cash liquidity materially contracts

When active:
- keep the formula unchanged
- disclose component conflict
- do not interpret a near-zero aggregate as absence of information
- pass conflict to ADAPTIVE_VALIDATION_RULE / Change Detection
- do not change weights ad hoc.

## 67. C6 Shock / Weight Shift Candidate
C6 remains clipped to [-1,+1]. Raise `C6 Shock: ACTIVE` when any validated raw input reaches:
- |USD/KRW 5-observation change| >= 2.5%
- |Korea Treasury 3Y 5-observation change| >= 30bp
- |Customer Deposits 5-observation change| >= 7.5%

C6 Shock is a Change Detection / Transition / Weight Shift candidate only. It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 68. C6 Anti-Double-Counting
For C6 numeric scoring:
- USD/KRW financial-condition change is scored once in FX
- Korea Treasury 3Y change is scored once in RATE
- Customer Deposit change is scored once in CASH
- Margin Credit is contextual only in v1
- Policy Rate/M2 are structural context only in v1
- Foreign/Institution flow remains C1/E1
- Program flow remains C2/E2
- Breadth/ADL remains C3/E3
- Sector Leadership remains C4/E4
- Price/MA/VWAP/technical structure remains C5/E5
- Options/OI/volatility remains E7
- Binance/TMF/SPY/QQQ/BTC/EWY/SOXL and other global-leading proxies remain E8

Korea Treasury 3Y in C6 represents domestic financial conditions. TMF is an E8 global-leading proxy and must not be added to C6 numerically as a second rate signal.

## 69. C6 Anti-Circularity
Required separation:
`Validated Domestic Macro/Liquidity Data → C6 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C6 must not:
1. choose a Market Regime,
2. use that Regime to alter its own numeric weights,
3. use the altered C6 as the sole reason to reconfirm the same Regime.

VH/H/M/L Evidence Priority must never be converted into numeric C6 weights.

## 70. C6 Validation Cases
### Case A — Broad Easing
USD/KRW 5d=-2%, 3Y 5d=-20bp, Deposits 5d=+5%.
FX=+1, RATE=+1, CASH=+1 → C6=+1.00.

### Case B — Broad Tightening
USD/KRW 5d=+2%, 3Y 5d=+20bp, Deposits 5d=-5%.
FX=-1, RATE=-1, CASH=-1 → C6=-1.00.

### Case C — Offset Conflict
FX=+1, RATE=-1, CASH=0 → C6=0.00 + `C6 Conflict: ACTIVE`.

### Case D — CASH Missing
FX=+0.60,RATE=+0.40 → C6=+0.50 / PARTIAL.

### Case E — FX Missing
RATE=-0.80,CASH=-0.50 → C6≈-0.6615 / PARTIAL.

### Case F — RATE Missing
FX=+0.80,CASH=-0.40 → C6≈+0.2462 / PARTIAL. Conflict is raised only if both opposing absolute values meet the >=0.50 threshold.

### Case G — Only CASH Available
Expected: DATA UNAVAILABLE.

### Case H — Margin Credit Surge Alone
No direct numeric C6 contribution; qualitative leverage/overheat context only.

### Case I — FX Shock
USD/KRW 5-observation change +3% → FX remains clipped at -1.00 + `C6 Shock: ACTIVE`.

### Case J — Lower-Frequency Policy/M2 Update
Use as structural E6 context; no silent numeric insertion into C6.

Result: PASS by rule design.

## 71. Current Component / Global SAI Status After C6
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C4 Sector / Leadership`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C5 Technical Structure`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C6 Liquidity / Macro`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

C1-C6 remain component-level formulas only. Global SAI remains unavailable until remaining required components, global aggregation, global missing/partial handling, final range/Action Bands and regression validation are complete.

## 72. Future Formula Adoption Procedure
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

## 73. Final Principle
No complete official global formula = no official global number.
A validated sub-component does not equal Strategy Action Index.
Adaptive priority ≠ numeric weight.
Reliability > Speed.
DATA UNAVAILABLE is preferable to fabricated precision.
