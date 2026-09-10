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

`SAI-C1 Smart Money`, `SAI-C2 Program Flow`, `SAI-C3 Breadth / Market Internal`, `SAI-C4 Sector / Leadership` and `SAI-C5 Technical Structure` are defined below as component specifications only. None may be presented as the final Strategy Action Index.

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
Do not infer a formula from:
- legacy score labels
- traffic-light colors
- qualitative judgments
- portfolio actions
- analyst intuition
- previous displayed numbers without documented calculation rules
- Market Regime labels
- Transition labels
- VH/H/M/L Evidence Priority
- qualitative Strategy postures

A signal label, Regime or qualitative priority does not create a score band.

## 5. Category Score / Indicator Distinction
Dashboard categories may show verified `Score / Indicator` values even when the two official global numeric scores are unavailable.

Examples of valid indicators:
- Foreign Spot / Futures flow
- Program flow
- Breadth
- RSI
- MACD
- ADX
- Funding
- OI / OI change
- Customer deposits / margin credit
- Support / resistance
- AI-cycle supply/demand indicators
- qualitative Evidence Priority such as VH/H/M/L when sourced from ADAPTIVE_VALIDATION_RULE

These are not automatically AI Master Score components unless this SCORING_RULE explicitly defines them as such.

## 6. Qualitative Signals
Canonical signals may be produced from validated evidence and engine consensus according to the owning analysis rules:
🟢 Strong Bull / Positive
🔵 Bull
🟡 Neutral
🟠 Warning / Caution
🔴 Bear / Negative
⚫ Extreme Risk
⚪ DATA UNAVAILABLE

Qualitative signals must never be mathematically converted into unofficial numeric scores.

## 7. Adaptive Evidence Firewall
`ADAPTIVE_VALIDATION_RULE` may use:
- Market Regime
- Transition Regime / Risk
- E1-E8 Evidence Groups
- VH / H / M / L Evidence Priority
- qualitative Strategy posture

These are analytical classification and priority tools only.

The following conversions are prohibited unless this SCORING_RULE explicitly defines and validates a separate numeric scoring formula:
- VH/H/M/L → 4/3/2/1
- VH/H/M/L → percentages
- Regime labels → fixed score bands
- Strategy posture → Strategy Action Index number
- signal count → numeric score
- hidden analyst weighting of adaptive Evidence Groups
- silent normalization or reweighting based on missing adaptive inputs

Adaptive Evidence Priority is not numeric weight.

## 8. Confidence Is Not Score
`High / Medium / Low` Confidence measures evidence strength, completeness, freshness and agreement. It is not a probability, score or Strategy Action Index.

Regime Confidence is also non-numeric and cannot be converted into a score without an official future formula.

## 9. Missing Data
If an official scoring formula or component is defined, missing mandatory data must follow that formula's explicitly documented missing-data rule. If no such rule exists, output DATA UNAVAILABLE rather than silently reweighting.

## 10. Partial Score Rule
A partial numeric component or score is prohibited unless the formula explicitly defines:
- which inputs may be missing
- how weights are adjusted or not adjusted
- how the output is labeled
- the minimum completeness threshold

Otherwise use DATA UNAVAILABLE.

## 11. Binance Integration
Binance does not create a separate AI Market Master numeric score. Binance G1-G6 signals may feed future official scoring only if the formula explicitly defines their role. Symbol availability or Binance VERIFIED status is not itself a market score.

Binance use inside E8 Global Leading does not grant it numeric scoring authority.

## 12. Strategy Action Index Principle
Strategy Action Index, when eventually activated, must represent execution intensity according to a reproducible official formula. It must not be a disguised analyst opinion.

Qualitative Strategy postures from ADAPTIVE_VALIDATION_RULE — Defensive Observation, Hold, Constructive Hold, Accumulation, Risk Reduction Watch, Staged Reduction, Strong Risk Reduction and Extreme Risk Control — are not Strategy Action Index values.

Until the complete global formula is verified, output DATA UNAVAILABLE while still allowing qualitative strategy under MASTER_RULE and ADAPTIVE_VALIDATION_RULE.

## 13. AI Master Score Principle
AI Master Score, when eventually defined, must represent integrated market evidence according to a reproducible official formula and cannot be inferred from the final Signal, Market Regime, Evidence Priority Matrix or final Portfolio Action alone.

Until such formula is verified, output DATA UNAVAILABLE.

## 14. Legacy Engine Score Boundary
Legacy backups contain historical concepts such as Flow Score, Momentum Score, Risk Score, AI Score Delta and Engine Reliability Scoring, but no currently verified complete reproducible formula has been adopted here.

Therefore those historical labels/concepts do not authorize current global numeric scoring or numeric adaptive weights.

## 15. Regression Protection
The following are always invalid:
- incomplete mandatory inputs + invented numeric score
- signal color converted to a number without formula
- qualitative consensus converted to a percentage
- score copied from an earlier session without recomputation
- hidden/manual analyst weighting
- silent weight renormalization
- VH/H/M/L converted to numeric values without formal adoption
- Market Regime converted into a score by intuition
- qualitative Strategy posture presented as Strategy Action Index
- one numeric sub-component presented as the global Strategy Action Index

## 16. SAI-C1 Smart Money — Purpose and Boundary
`SAI-C1 Smart Money` is the first formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether major directional capital in the Korean equity market is increasing or reducing risk exposure.

Authority boundary:
- Numeric C1 formula, normalization, bounds, component weights and missing-data handling are owned by this SCORING_RULE.
- `E1 Smart Money` interpretation, Market Regime, Transition, VH/H/M/L Evidence Priority and adaptive conflict resolution remain owned by ADAPTIVE_VALIDATION_RULE.
- C1 does not replace E1 and cannot select or reconfirm a Regime by itself.
- C1 must not convert E1 VH/H/M/L priority into numeric weight.

## 17. SAI-C1 Inputs and Units
Core inputs:

### C1-A Foreign KOSPI Cash
- Input: foreign investor KOSPI cash-market net buy/sell amount
- Unit: KRW amount, using the same unit as KOSPI total traded value before ratio conversion
- Required: YES

### C1-B Foreign KOSPI200 Futures
- Input: foreign investor KOSPI200 futures net buy/sell contracts
- Unit: contracts
- Denominator: KOSPI200 futures total Open Interest in contracts
- Required: YES

### C1-C Institutional KOSPI Cash
- Input: total institutional KOSPI cash-market net buy/sell amount
- Unit: KRW amount, using the same unit as KOSPI total traded value before ratio conversion
- Required: NO; supplementary component

The following are not independent C1 numeric inputs:
- Program / arbitrage / non-arbitrage flow
- Breadth / ADL
- Options flow
- Financial Investment when already contained inside total Institution flow
- foreign cumulative futures position when current foreign futures flow is already scored
- OI change as an independent directional C1 score

## 18. SAI-C1 Normalization
All normalized values are clipped to `[-1.00, +1.00]`.

### C1-A Foreign Cash Normalization
Let:
`FC = Foreign KOSPI Cash Net Flow / KOSPI Total Traded Value`

Then:
`N_FC = clip(FC / 0.015, -1, +1)`

Interpretation:
- +1.5% or greater of KOSPI traded value → +1.00
- 0 → 0
- -1.5% or lower → -1.00
- values between are linearly normalized

### C1-B Foreign Futures Normalization
Let:
`FF = Foreign KOSPI200 Futures Net Contracts / KOSPI200 Futures Total OI`

Then:
`N_FF = clip(FF / 0.10, -1, +1)`

Interpretation:
- +10% or greater of total OI → +1.00
- 0 → 0
- -10% or lower → -1.00
- values between are linearly normalized

### C1-C Institution Cash Normalization
Let:
`IC = Institutional KOSPI Cash Net Flow / KOSPI Total Traded Value`

Then:
`N_IC = clip(IC / 0.010, -1, +1)`

Interpretation:
- +1.0% or greater of KOSPI traded value → +1.00
- 0 → 0
- -1.0% or lower → -1.00
- values between are linearly normalized

These are SAI-C1 v1 calibration boundaries. They are component-specific numeric rules, not conversions from qualitative Evidence Priority.

## 19. SAI-C1 Formula
When all three inputs are available:

`SAI-C1 = 0.40*N_FC + 0.40*N_FF + 0.20*N_IC`

Component range:
`-1.00 <= SAI-C1 <= +1.00`

Internal weights:
- Foreign KOSPI Cash: 40%
- Foreign KOSPI200 Futures: 40%
- Institutional KOSPI Cash: 20%

Rationale:
- Foreign Cash provides stronger structural confirmation value.
- Foreign Futures provides higher short-term transition sensitivity.
- Institution Cash is a domestic confirmation component and has lower weight than the two foreign-flow components.

These C1 internal weights do not define the future weight of C1 inside the complete global Strategy Action Index.

## 20. SAI-C1 Missing / Partial Rule
### Full C1
If C1-A, C1-B and C1-C are all available:
`SAI-C1 = 0.40*N_FC + 0.40*N_FF + 0.20*N_IC`
Status: `VERIFIED` if source/unit validation also passes.

### Institution Missing Only
If C1-A and C1-B are available but C1-C is unavailable:
`SAI-C1 = 0.50*N_FC + 0.50*N_FF`
Status: `PARTIAL`

This 50/50 rule is an explicit predefined partial formula and is therefore not silent reweighting.

### Mandatory Input Missing
If either C1-A Foreign Cash or C1-B Foreign Futures is unavailable or its denominator cannot be validated:
`SAI-C1 = DATA UNAVAILABLE`

Missing data is never converted to zero / Neutral.

## 21. SAI-C1 Conflict and Shock Flags
The aggregate C1 number must not hide important internal conflict.

### Foreign Cash / Futures Conflict
When Foreign Cash and Foreign Futures are materially opposed in direction, disclose:
`C1 Conflict: ACTIVE`

The conflict must be passed to ADAPTIVE_VALIDATION_RULE for contextual interpretation. The C1 weights are not changed ad hoc to force a directional result.

### C1 Shock Flag
C1 remains clipped to ±1.00. Extreme flow does not extend the numeric range.

A `C1 Shock` / Weight Shift candidate may be raised when any validated input reaches at least 1.5 times its normal saturation boundary:
- |Foreign Cash / KOSPI Traded Value| >= 2.25%
- |Foreign Futures / Total OI| >= 15%
- |Institution Cash / KOSPI Traded Value| >= 1.50%

A C1 Shock is a change-detection input, not an automatic Regime change, Strategy Action Index override or permanent weight update.

## 22. SAI-C1 Anti-Double-Counting
For C1 numeric scoring:
- current Foreign Cash flow is scored once
- current Foreign Futures flow is scored once
- total Institution flow is scored once
- cumulative futures position may be contextual confirmation only
- Financial Investment may explain Institution composition only
- Program/Arbitrage/Non-Arbitrage remain E2 and are not added to C1
- Breadth/ADL remain E3 and are not added to C1
- options/OI-risk structure remain E7 and are not added to C1

No derivative of an already-scored datum may be added as a new independent C1 contribution unless this rule is formally revised.

## 23. SAI-C1 Validation Cases
### Case A — Normal Bullish Alignment
`N_FC=+0.75, N_FF=+0.60, N_IC=+0.30`

`C1 = 0.40*0.75 + 0.40*0.60 + 0.20*0.30 = +0.60`
Expected: positive Smart Money numeric component, no conflict.

### Case B — Normal Bearish Alignment
`N_FC=-0.70, N_FF=-0.80, N_IC=-0.20`

`C1 = -0.64`
Expected: negative Smart Money numeric component, no conflict.

### Case C — Foreign Cash / Futures Reversal Conflict
`N_FC=+0.70, N_FF=-0.90, N_IC=+0.20`

`C1 = -0.04`
Expected: near-neutral aggregate plus `C1 Conflict: ACTIVE`; do not interpret the near-zero score as absence of information.

### Case D — Institution Missing
`N_FC=+0.60, N_FF=+0.80, N_IC=DATA UNAVAILABLE`

`C1 = 0.50*0.60 + 0.50*0.80 = +0.70`
Status: `PARTIAL`.

### Case E — Mandatory Input Missing
Foreign Cash available, Foreign Futures unavailable, Institution available.

Expected: `SAI-C1 = DATA UNAVAILABLE`.

### Case F — Extreme Flow
If normalized foreign futures raw ratio exceeds ±15% of total OI:
- numeric contribution remains clipped to ±1.00
- `C1 Shock: ACTIVE`
- pass shock to change/transition analysis
- do not change global Base Weight or Market Regime automatically.

## 24. SAI-C1 Adaptive / Anti-Circularity Boundary
Required separation:

`Raw HTS Flow Data → C1 Calculation`

and independently:

`Raw HTS + other Evidence → Preliminary Regime → Transition / Conflict → Regime Re-validation`

C1 may inform later strategy once the global SAI formula exists, but C1 must not:
1. choose a Regime,
2. use that Regime to alter itself,
3. then use the altered C1 as the sole reason to reconfirm the same Regime.

Any future Conditional Numeric Weight must be separately defined in this SCORING_RULE and must not be inferred from VH/H/M/L.

## 25. Current C1 / Global SAI Status
`SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY.

`Strategy Action Index`: DATA UNAVAILABLE.

The global SAI remains unavailable because the remaining components, global aggregation, global missing/partial rule, final range mapping, Action Bands and regression validation are not yet complete.

## 26. Future Formula Adoption Procedure
Before activating the global Strategy Action Index:
1. identify source/version
2. define every component and global formula
3. document all mandatory inputs and units
4. define normalization and aggregation
5. define missing/partial handling
6. verify no conflict with MASTER/DASHBOARD/TECHNICAL/BINANCE/ADAPTIVE_VALIDATION rules
7. test known cases
8. define output range and Action Bands
9. update VERSION_STATUS and CHANGELOG
10. only then change Current Official Status from DATA UNAVAILABLE

## 27. General Final Principle
No complete official global formula = no official global number.
A validated sub-component does not equal Strategy Action Index.
Adaptive priority ≠ numeric weight.
Reliability > Speed.
DATA UNAVAILABLE is preferable to fabricated precision.

## 28. SAI-C2 Program Flow — Purpose and Boundary
`SAI-C2 Program Flow` is the second formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether KOSPI program trading is supplying or withdrawing market liquidity, while separating structurally informative Non-Arbitrage flow from more mechanical/event-sensitive Arbitrage flow.

Authority boundary:
- Numeric C2 formula, normalization, bounds, internal weights, missing-data handling and numeric shock thresholds are owned by this SCORING_RULE.
- `E2 Program Flow` interpretation, Market Regime, Transition, VH/H/M/L Evidence Priority, conflict resolution and re-validation remain owned by ADAPTIVE_VALIDATION_RULE.
- C2 does not replace E2 and cannot select or reconfirm a Regime by itself.
- C2 must not convert E2 VH/H/M/L priority into numeric weight.

## 29. SAI-C2 Inputs and Units
### C2-A Arbitrage Program Flow
- Input: KOSPI arbitrage program net buy/sell amount
- Unit: KRW amount, unit-aligned with KOSPI total traded value before ratio conversion
- Required: NO; supplementary/mechanical-sensitive component

### C2-B Non-Arbitrage Program Flow
- Input: KOSPI non-arbitrage program net buy/sell amount
- Unit: KRW amount, unit-aligned with KOSPI total traded value before ratio conversion
- Required: YES; structural core component

### Validation-only Total Program Flow
- Input: total KOSPI program net buy/sell amount when available
- Use: source/unit reconciliation against Arbitrage + Non-Arbitrage
- It is not a third independent numeric contribution.

If total program is provided and materially fails to reconcile with unit-aligned Arbitrage + Non-Arbitrage, disclose a data-integrity conflict and do not silently score inconsistent inputs.

## 30. SAI-C2 Normalization
All normalized values are clipped to `[-1.00,+1.00]`.

### C2-A Arbitrage Normalization
Let:
`ARB = Arbitrage Program Net Flow / KOSPI Total Traded Value`

Then:
`N_ARB = clip(ARB / 0.0075, -1, +1)`

Interpretation:
- +0.75% or greater of KOSPI traded value → +1.00
- 0 → 0
- -0.75% or lower → -1.00
- intermediate values are linearly normalized

### C2-B Non-Arbitrage Normalization
Let:
`NONARB = Non-Arbitrage Program Net Flow / KOSPI Total Traded Value`

Then:
`N_NONARB = clip(NONARB / 0.015, -1, +1)`

Interpretation:
- +1.50% or greater of KOSPI traded value → +1.00
- 0 → 0
- -1.50% or lower → -1.00
- intermediate values are linearly normalized

These are SAI-C2 v1 calibration boundaries. They are component-specific numeric rules, not conversions from qualitative Evidence Priority.

## 31. SAI-C2 Formula
When Arbitrage and Non-Arbitrage inputs are both valid:

`SAI-C2 = 0.30*N_ARB + 0.70*N_NONARB`

Component range:
`-1.00 <= SAI-C2 <= +1.00`

Internal weights:
- Arbitrage Program: 30%
- Non-Arbitrage Program: 70%

Rationale:
- Non-Arbitrage flow has greater structural significance under the existing 3.2 Program Conflict rule.
- Arbitrage flow is retained because it contains useful liquidity/hedging information but is more sensitive to basis, expiry and index-rebalancing mechanics.
- Strong Arbitrage buying must not numerically dominate persistent Non-Arbitrage selling.

These internal weights do not define the future weight of C2 inside the complete global Strategy Action Index.

## 32. SAI-C2 Missing / Partial Rule
### Full C2
If Arbitrage and Non-Arbitrage are both available and source/unit validation passes:
`SAI-C2 = 0.30*N_ARB + 0.70*N_NONARB`
Status: `VERIFIED`.

### Arbitrage Missing Only
If Non-Arbitrage is available but Arbitrage is unavailable:
`SAI-C2 = N_NONARB`
Status: `PARTIAL`.

This is an explicit predefined partial formula and is not silent reweighting.

### Non-Arbitrage Missing
If Non-Arbitrage is unavailable or its unit/denominator cannot be validated:
`SAI-C2 = DATA UNAVAILABLE`.

Arbitrage alone may not create a C2 numeric score.
Missing data is never converted to zero / Neutral.

## 33. SAI-C2 Conflict Rule
The aggregate number must not hide Arbitrage/Non-Arbitrage divergence.

`C2 Conflict: ACTIVE` when:
- `N_ARB` and `N_NONARB` have opposite signs, and
- both absolute normalized magnitudes are at least `0.30`.

When C2 Conflict is ACTIVE:
- keep the formula unchanged
- disclose the conflict
- preserve Non-Arbitrage structural priority in qualitative interpretation
- pass the conflict to ADAPTIVE_VALIDATION_RULE
- do not alter C2 weights ad hoc to force a directional result.

A near-zero aggregate caused by opposing flows is not interpreted as absence of information.

## 34. SAI-C2 Shock / Weight Shift Candidate
C2 remains clipped to ±1.00. Extreme flow does not extend the numeric range.

Raise `C2 Shock: ACTIVE` when either validated raw ratio reaches 1.5 times its normal saturation boundary:
- |Arbitrage / KOSPI Traded Value| >= 1.125%
- |Non-Arbitrage / KOSPI Traded Value| >= 2.25%

C2 Shock is passed to Change Detection / Transition analysis as a Weight Shift candidate.
It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 35. Mechanical Event Flag
When a known derivatives expiry, index/sector rebalance, ETF mechanical rebalance or comparable market-structure event can materially distort program flow, disclose:
`C2 Mechanical Event: ACTIVE`.

Rules:
- C2 is still calculated from validated raw data.
- Arbitrage flow must not independently create a structural Regime conclusion on a Mechanical Event day.
- Non-Arbitrage remains the stronger structural interpretation input, but its significance must still be cross-validated with E1 Smart Money, E3 Breadth, E5 Technical and E7 Risk when relevant.
- Mechanical Event does not automatically change numeric C2 weights; any future numeric event adjustment requires a separately validated SCORING_RULE revision.

## 36. SAI-C2 Anti-Double-Counting
For C2 numeric scoring:
- Arbitrage is scored once
- Non-Arbitrage is scored once
- Total Program is reconciliation/context only and is not added after its components
- Foreign/institution investor flows remain C1/E1 and are not re-added to C2
- Breadth/ADL remain E3
- Technical price/volume remain E5
- options/OI/volatility remain E7

No derivative or sum of already-scored Program inputs may be added as an additional independent C2 contribution.

## 37. SAI-C2 Validation Cases
### Case A — Bullish Alignment
`N_ARB=+0.50, N_NONARB=+0.70`
`C2 = 0.30*0.50 + 0.70*0.70 = +0.64`
Expected: positive C2, no conflict.

### Case B — Bearish Alignment
`N_ARB=-0.40, N_NONARB=-0.80`
`C2 = 0.30*(-0.40) + 0.70*(-0.80) = -0.68`
Expected: negative C2, no conflict.

### Case C — Arbitrage Buy / Non-Arbitrage Sell
`N_ARB=+1.00, N_NONARB=-0.60`
`C2 = +0.30 - 0.42 = -0.12`
Expected: `C2 Conflict: ACTIVE`; structural interpretation remains cautionary because Non-Arbitrage is negative.

### Case D — Arbitrage Missing
`N_ARB=DATA UNAVAILABLE, N_NONARB=+0.65`
`C2 = +0.65`
Status: `PARTIAL`.

### Case E — Non-Arbitrage Missing
`N_ARB=+0.80, N_NONARB=DATA UNAVAILABLE`
Expected: `SAI-C2 = DATA UNAVAILABLE`.

### Case F — Extreme Non-Arbitrage Flow
If |Non-Arbitrage / KOSPI Traded Value| >= 2.25%:
- normalized contribution remains clipped to ±1.00
- `C2 Shock: ACTIVE`
- pass to Change Detection / Transition analysis
- no automatic global SAI or Regime change.

### Case G — Mechanical Rebalance Day
Large Arbitrage flow with a known expiry/rebalance event:
- calculate C2 normally
- disclose `C2 Mechanical Event: ACTIVE`
- do not treat Arbitrage alone as structural confirmation.

## 38. SAI-C2 Adaptive / Anti-Circularity Boundary
Required separation:

`Raw HTS Program Data → C2 Calculation`

and independently:

`Raw HTS + other Evidence → Preliminary Regime → Transition / Conflict → Regime Re-validation`

C2 may inform later strategy once the global SAI formula exists, but C2 must not:
1. choose a Regime,
2. use that Regime to alter itself,
3. use the altered C2 as the sole reason to reconfirm the same Regime.

Any future Conditional Numeric Weight must be separately defined in this SCORING_RULE and must not be inferred from E2 VH/H/M/L priority.

## 39. Current Component / Global SAI Status
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C4 Sector / Leadership`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

The global SAI remains unavailable until remaining components, global aggregation, global missing/partial handling, output range/Action Bands and required validation are complete.

## 40. C2 Final Principle
Program Total = validation/context, not an extra score.
Non-Arbitrage > Arbitrage for structural interpretation.
Mechanical flow ≠ structural market change by itself.
Conflict and Shock are information, not reasons to distort the formula.
No complete global formula = no global Strategy Action Index.

## 41. SAI-C3 Breadth / Market Internal — Purpose and Boundary
`SAI-C3 Breadth / Market Internal` is the third formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether domestic market participation is broadening or deteriorating beneath headline index performance, while preserving the distinction between KOSPI core participation and broader KOSDAQ confirmation.

Authority boundary:
- Numeric C3 formula, normalization, bounds, internal weights, missing-data handling and numeric divergence/shock thresholds are owned by this SCORING_RULE.
- `E3 Breadth / Internal` interpretation, Market Regime, Transition, VH/H/M/L Evidence Priority, conflict resolution and re-validation remain owned by ADAPTIVE_VALIDATION_RULE.
- C3 does not replace E3 and cannot select or reconfirm a Regime by itself.
- C3 must not convert E3 VH/H/M/L priority into numeric weight.

## 42. SAI-C3 Inputs and Units
### C3-A KOSPI Active Breadth
Required inputs:
- KOSPI advancing issue count `ADV_K`
- KOSPI declining issue count `DEC_K`

Validation/context input:
- unchanged issue count `UNCH_K` when available

Directional breadth denominator:
`ADV_K + DEC_K`

Required: YES.

### C3-B KOSDAQ Active Breadth
Inputs:
- KOSDAQ advancing issue count `ADV_Q`
- KOSDAQ declining issue count `DEC_Q`

Validation/context input:
- unchanged issue count `UNCH_Q` when available

Required: NO; supplementary cross-market participation confirmation.

### ADL Boundary
An isolated raw ADL level is not a C3 numeric input in v1.
Reason: its absolute level depends on accumulation history and is not comparable across sessions without a validated reference series.
ADL may be used contextually under E3. A future C3 revision may add ADL change/trend only after an explicit comparable-history formula is defined.

## 43. SAI-C3 Breadth Calculation and Normalization
### C3-A KOSPI
If `ADV_K + DEC_K > 0`:
`B_K = (ADV_K - DEC_K) / (ADV_K + DEC_K)`

Then:
`N_K = clip(B_K / 0.50, -1, +1)`

Interpretation:
- active breadth +50% or greater → +1.00
- 0 → 0
- active breadth -50% or lower → -1.00
- intermediate values are linearly normalized

### C3-B KOSDAQ
If `ADV_Q + DEC_Q > 0`:
`B_Q = (ADV_Q - DEC_Q) / (ADV_Q + DEC_Q)`

Then:
`N_Q = clip(B_Q / 0.50, -1, +1)`

Interpretation uses the same symmetric saturation boundary.

Unchanged issues do not enter the directional numerator and do not create Bull/Bear points. They remain validation/context for participation quality.

These are SAI-C3 v1 calibration boundaries. They are component-specific numeric rules, not conversions from qualitative Evidence Priority or signal counts.

## 44. SAI-C3 Formula
When KOSPI and KOSDAQ breadth are both valid:

`SAI-C3 = 0.70*N_K + 0.30*N_Q`

Component range:
`-1.00 <= SAI-C3 <= +1.00`

Internal weights:
- KOSPI active breadth: 70%
- KOSDAQ active breadth: 30%

Rationale:
- KOSPI is the structural core for Korean-market portfolio action.
- KOSDAQ adds broader domestic participation/risk-appetite confirmation without overriding the KOSPI internal structure.

These internal weights do not define the future weight of C3 inside the complete global Strategy Action Index.

## 45. SAI-C3 Missing / Partial Rule
### Full C3
If both KOSPI and KOSDAQ active breadth are valid:
`SAI-C3 = 0.70*N_K + 0.30*N_Q`
Status: `VERIFIED` when source/count validation passes.

### KOSDAQ Missing Only
If KOSPI active breadth is valid but KOSDAQ breadth is unavailable:
`SAI-C3 = N_K`
Status: `PARTIAL`.

This is an explicit predefined partial formula and is not silent reweighting.

### KOSPI Missing / Invalid
If KOSPI advancing/declining counts are unavailable, inconsistent, or `ADV_K + DEC_K <= 0`:
`SAI-C3 = DATA UNAVAILABLE`.

Missing data is never converted to zero / Neutral.

## 46. SAI-C3 Cross-Market Conflict Rule
Raise `C3 Conflict: ACTIVE` when:
- `N_K` and `N_Q` have opposite signs, and
- both absolute normalized magnitudes are at least `0.30`.

When active:
- keep the formula unchanged
- disclose KOSPI/KOSDAQ participation divergence
- do not reinterpret a near-zero aggregate as absence of information
- pass the conflict to ADAPTIVE_VALIDATION_RULE
- do not alter C3 weights ad hoc.

## 47. SAI-C3 Index / Breadth Divergence Rule
KOSPI daily return may be used only as a comparator, not as an additional C3 numeric contribution.

Raise `C3 Divergence: ACTIVE` when either condition is verified:
- KOSPI daily return > 0 and `N_K <= -0.30`
- KOSPI daily return < 0 and `N_K >= +0.30`

Interpretation:
- price up + weak breadth = concentration/distribution warning candidate
- price down + improving breadth = internal stabilization/recovery-watch candidate

The divergence flag is passed to Change Detection / Transition analysis and does not by itself change Market Regime or C3 weights.

## 48. SAI-C3 Shock / Weight Shift Candidate
C3 remains clipped to ±1.00. Extreme breadth does not extend the numeric range.

Raise `C3 Shock: ACTIVE` when either condition is verified:
1. `|B_K| >= 0.75`, or
2. KOSPI and KOSDAQ breadth are in the same direction and both satisfy `|B_K| >= 0.65` and `|B_Q| >= 0.65`.

A C3 Shock is a broad-participation Change Detection / Weight Shift candidate only.
It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 49. SAI-C3 Anti-Double-Counting
For C3 numeric scoring:
- KOSPI advance/decline breadth is scored once
- KOSDAQ advance/decline breadth is scored once as supplementary confirmation
- unchanged counts are validation/context only
- raw ADL level is contextual only in v1 and not an extra numeric contribution
- KOSPI/KOSDAQ index returns are divergence comparators only
- Program flow remains C2/E2
- foreign/institution flow remains C1/E1
- MA/VWAP/momentum/price structure remain E5 and are not re-added to C3
- volatility/options/OI remain E7

E5 Technical may reference Breadth/ADL contextually under existing rules but must not count it again as independent numeric confirmation.

## 50. SAI-C3 Validation Cases
### Case A — Broad Bullish Participation
KOSPI: `ADV=600, DEC=300`
`B_K=+0.3333`, `N_K=+0.6667`
KOSDAQ: `ADV=1000, DEC=600`
`B_Q=+0.25`, `N_Q=+0.50`

`C3 = 0.70*0.6667 + 0.30*0.50 ≈ +0.6167`
Expected: positive C3, no conflict.

### Case B — Broad Bearish Participation
KOSPI: `ADV=250, DEC=650`
`B_K=-0.4444`, `N_K=-0.8889`
KOSDAQ: `ADV=500, DEC=1100`
`B_Q=-0.375`, `N_Q=-0.75`

`C3 ≈ -0.8472`
Expected: strong negative C3, no conflict.

### Case C — KOSPI / KOSDAQ Conflict
`N_K=+0.60`, `N_Q=-0.50`

`C3=+0.27`
Expected: `C3 Conflict: ACTIVE`; do not interpret +0.27 as clean broad participation.

### Case D — KOSDAQ Missing
`N_K=-0.55`, KOSDAQ unavailable.

`C3=-0.55`
Status: `PARTIAL`.

### Case E — KOSPI Missing
KOSPI breadth unavailable, KOSDAQ valid.
Expected: `SAI-C3 = DATA UNAVAILABLE`.

### Case F — Index Up / Breadth Weak
KOSPI daily return positive and `N_K=-0.45`.
Expected: calculate C3 normally + `C3 Divergence: ACTIVE`.

### Case G — Extreme Breadth Collapse
`B_K <= -0.75`.
Expected:
- `N_K=-1.00`
- `C3 Shock: ACTIVE`
- pass to Change Detection / Transition analysis
- no automatic global SAI or Regime change.

### Case H — Many Unchanged Issues
If unchanged issues are numerous but `ADV_K + DEC_K > 0`, active breadth is still calculated from advancing/declining issues and unchanged count is disclosed/contextualized when material.
Expected: no artificial directional point from unchanged issues.

## 51. SAI-C3 Adaptive / Anti-Circularity Boundary
Required separation:

`Raw HTS Breadth Data → C3 Calculation`

and independently:

`Raw HTS + other Evidence → Preliminary Regime → Transition / Conflict → Regime Re-validation`

C3 may inform later strategy once the global SAI formula exists, but C3 must not:
1. choose a Regime,
2. use that Regime to alter itself,
3. use the altered C3 as the sole reason to reconfirm the same Regime.

Any future Conditional Numeric Weight must be separately defined in this SCORING_RULE and must not be inferred from E3 VH/H/M/L priority.

## 52. Current Component / Global SAI Status After C3
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

The global SAI remains unavailable until remaining components, global aggregation, global missing/partial handling, output range/Action Bands and required validation are complete.

## 53. C3 Final Principle
Breadth measures participation, not headline index direction.
KOSPI breadth is the structural core; KOSDAQ breadth is supplementary confirmation.
Raw ADL without comparable history is context, not a numeric score.
Index/Breadth divergence is information, not a reason to distort the formula.
No complete global formula = no global Strategy Action Index.

## 54. SAI-C4 Sector / Leadership — Purpose and Boundary
`SAI-C4 Sector / Leadership` is the fourth formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether Korean-market sector participation and relative leadership are broadening or deteriorating, while separating broad sector direction from KOSPI-relative leadership and preventing theme/index overlap from being counted as independent evidence.

Authority boundary:
- Numeric C4 formula, fixed-universe input rules, thresholds, bounds, internal weights, completeness handling and numeric conflict/shock conditions are owned by this SCORING_RULE.
- `E4 Sector / Leadership` remains the qualitative/adaptive owner for sector rotation, leadership concentration/expansion, Market Regime, Transition, Evidence Priority and re-validation.
- C4 does not replace E4 and cannot select or reconfirm a Market Regime by itself.
- C4 must not convert E4 VH/H/M/L priority into numeric weight.

## 55. SAI-C4 Fixed Sector Universe v1
The C4 v1 universe contains exactly eight verified benchmark identities:
1. Semiconductor — KRX Semiconductor Index
2. Automobile — KRX Automobile Index
3. Secondary Battery — KRX Secondary Battery TOP 10 Index
4. Financials — KOSPI 200 Financial Index
5. Shipbuilding — iSelect Shipbuilding TOP10 Index (PR)
6. Defense — iSelect Defense TOP10 Index (Price Return)
7. AI Power Infrastructure — KRX-Akros AI Power Infrastructure Index
8. Bio — KRX Bio TOP 10 Index

Identification rule:
- canonical identity = `index provider + exact benchmark index name`
- ETF ticker/code is never treated as the benchmark index code
- an HTS short code may be stored only as a verified alias
- if the displayed index name cannot be mapped unambiguously to one of these eight identities, that sector is unavailable for C4 numeric calculation.

The universe is fixed for C4 v1. Adding, removing or substituting sectors requires a future SCORING_RULE revision rather than an ad hoc session-level change.

## 56. SAI-C4 Data Collection and Freshness Standard
Source priority follows MASTER_RULE:
1. user-provided HTS/KRX data
2. verified official KRX/index-provider data
3. other verified supplementary data

Required recurring data:
- KOSPI daily return
- same-session daily return for each available fixed-universe sector benchmark

Preferred validation fields:
`Index Name | Current Level | Change | Daily Return | Source | Timestamp`

Numeric C4 uses daily return only. Current level/change/source/timestamp are validation/context unless separately defined later.

All C4 sector returns and the KOSPI comparator must refer to the same trading session and materially aligned observation time. Mixed-date or materially asynchronous data is not silently combined.

ETF return may be used as contextual verification only; it is not a silent numeric replacement for a missing benchmark-index return.

## 57. SAI-C4-A Sector Direction Breadth
For each valid fixed-universe sector `i`, let `r_i` be its daily percentage return.

Classification:
- `r_i > +0.20%` → `D_i = +1`
- `r_i < -0.20%` → `D_i = -1`
- `-0.20% <= r_i <= +0.20%` → `D_i = 0`

Let:
- `UP` = count of sectors with `D_i=+1`
- `DOWN` = count of sectors with `D_i=-1`
- `N_valid` = number of valid fixed-universe sector returns

Then:
`SD = (UP - DOWN) / N_valid`

Range:
`-1.00 <= SD <= +1.00`

The ±0.20% neutral band is a C4 v1 noise-control calibration rule. It is not a qualitative signal-color conversion.

Sector Direction Breadth measures sector-level participation. Issue advance/decline Breadth remains C3/E3 and is not re-added here.

## 58. SAI-C4-B Relative Leadership Breadth
Let `r_K` be the same-session KOSPI daily return.

For each valid sector `i`:
`RS_i = r_i - r_K`

Classification:
- `RS_i > +0.20%p` → `L_i = +1`
- `RS_i < -0.20%p` → `L_i = -1`
- `-0.20%p <= RS_i <= +0.20%p` → `L_i = 0`

Let:
- `OUT` = count of sectors with `L_i=+1`
- `UNDER` = count of sectors with `L_i=-1`

Then:
`RL = (OUT - UNDER) / N_valid`

Range:
`-1.00 <= RL <= +1.00`

KOSPI return is a comparator only and is not separately added as a third C4 numeric contribution.

## 59. SAI-C4 Formula and Completeness Gate
When completeness and same-session validation pass:

`SAI-C4 = 0.60*SD + 0.40*RL`

Component range:
`-1.00 <= SAI-C4 <= +1.00`

Internal weights:
- Sector Direction Breadth: 60%
- Relative Leadership Breadth: 40%

Rationale:
- broad absolute sector direction receives greater weight so widespread losses do not become strongly bullish merely because sectors decline less than the headline index.
- relative leadership remains material for detecting concentration, rotation and resilience.

Completeness:
- `N_valid = 8` + valid KOSPI return + source/session validation → eligible for `VERIFIED`
- `N_valid = 6 or 7` + valid KOSPI return → predefined `PARTIAL`; calculate SD/RL using only the valid fixed-universe sectors
- `N_valid < 6` → `SAI-C4 = DATA UNAVAILABLE`
- KOSPI daily return unavailable/invalid/asynchronous → `SAI-C4 = DATA UNAVAILABLE`

Coverage threshold = 75% of the fixed universe, minimum 6 of 8.
Missing sectors are excluded from `N_valid`; they are never converted to zero/Neutral.

These C4 internal weights do not define the future global weight of C4 inside the complete Strategy Action Index.

## 60. Leadership Concentration Boundary
Leadership Concentration is deliberately NOT an independent numeric term in C4 v1.

Reason:
Concentration is not inherently bearish; `Concentrated Leadership Bull` is a valid Market Regime. Penalizing concentration mechanically could misclassify a strong but narrow bull phase.

Permitted qualitative/context states under E4 include:
- BROAD
- NORMAL
- CONCENTRATED
- EXTREME

No unvalidated concentration ratio is adopted in C4 v1. Concentration may inform E4/Transition analysis but does not alter C4 weights or add a third numeric term.

## 61. SAI-C4 Conflict / Shock Rules
### C4 Conflict
Raise `C4 Conflict: ACTIVE` when:
- `SD` and `RL` have opposite signs, and
- `|SD| >= 0.50` and `|RL| >= 0.50`.

Interpretation examples:
- strongly positive SD + strongly negative RL → broad nominal gains but meaningful KOSPI-relative lag; possible headline-index/large-cap concentration
- strongly negative SD + strongly positive RL → broad nominal losses but relative resilience; possible internal stabilization/rotation

When active:
- keep the formula unchanged
- disclose the conflict
- do not interpret a near-zero aggregate as absence of information
- pass the conflict to ADAPTIVE_VALIDATION_RULE
- do not alter weights ad hoc.

### C4 Shock / Weight Shift Candidate
Raise `C4 Shock: ACTIVE` when either:
1. `|SD| >= 0.75`, or
2. SD and RL have the same sign and both satisfy `|SD| >= 0.60` and `|RL| >= 0.60`.

C4 Shock is a Change Detection / Transition / Weight Shift candidate only.
It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 62. SAI-C4 Anti-Double-Counting and Anti-Circularity
For C4 numeric scoring:
- each fixed benchmark return is used once as source data for derived SD/RL
- SD and RL are two predefined transforms of the same fixed sector-return set and must not be presented as two independent Evidence Groups
- KOSPI return is comparator only
- individual Samsung Electronics / SK hynix or other constituent returns are not separately added
- Foreign/Institution flow remains C1/E1
- Program/Arbitrage/Non-Arbitrage remains C2/E2
- issue advance/decline breadth / ADL remains C3/E3
- MA/VWAP/RSI/MACD/Elliott/Fibonacci remain E5 / future technical component
- HBM/DRAM/NAND/CAPEX/inventory/AI-demand fundamentals remain AI Cycle / future leading-cycle component
- options/OI/volatility remain E7
- Binance/SOXL/EWY/QQQ/SPY/BTC/TMF remain E8

Required separation:
`Raw Sector/KOSPI Data → C4 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C4 must not:
1. choose a Market Regime,
2. use that Regime to alter its own numeric weights,
3. use the altered C4 as the sole reason to reconfirm the same Regime.

VH/H/M/L Evidence Priority must never be converted into numeric C4 weights.

## 63. SAI-C4 Validation Cases
### Case A — Broad Bullish Leadership
Most valid sectors have `r_i > +0.20%` and most also outperform KOSPI by more than +0.20%p.
Expected: SD positive, RL positive, C4 positive, no conflict.

### Case B — Broad Market Weakness
Most valid sectors have `r_i < -0.20%` and most underperform KOSPI by more than -0.20%p.
Expected: SD negative, RL negative, C4 negative.

### Case C — Widespread Losses but Relative Resilience
Example: `SD=-1.00`, `RL=+1.00`.
`C4 = 0.60*(-1.00) + 0.40*(+1.00) = -0.20`.
Expected: not strongly bullish; `C4 Conflict: ACTIVE`.

### Case D — Strong Index / Weak Sector Participation
KOSPI strongly positive while most sector benchmarks are only modestly positive or lag KOSPI.
Expected: SD may be positive while RL is negative; concentration warning remains contextual under E4 rather than an automatic C4 penalty.

### Case E — Missing 2 of 8 Sectors
6 valid sector returns + valid same-session KOSPI return.
Expected: calculate with `N_valid=6`; Status `PARTIAL`.

### Case F — Missing 3 or More Sectors
5 or fewer valid sector returns.
Expected: `SAI-C4 = DATA UNAVAILABLE`.

### Case G — Missing KOSPI Comparator
Sector returns available but KOSPI return unavailable/invalid.
Expected: `SAI-C4 = DATA UNAVAILABLE`.

### Case H — Broad Sector Shock
`|SD| >= 0.75`.
Expected: calculate C4 normally + `C4 Shock: ACTIVE`; no automatic Regime/global SAI change.

### Case I — Mixed Session / Ambiguous Benchmark
A sector return is from another session or its index identity cannot be mapped unambiguously to the fixed universe.
Expected: exclude that sector from `N_valid`; apply the 8/6-7/<6 completeness gate; never substitute an ETF return silently.

## 64. Current Component / Global SAI Status After C4
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C4 Sector / Leadership`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

C1-C4 remain component-level formulas only.
The global SAI remains unavailable until remaining components, global aggregation, global missing/partial handling, final range/Action Bands and required regression/validation are complete.

C4 final principle:
Sector breadth measures leadership structure, not the Market Regime by itself.
Absolute direction > relative resilience in the v1 formula, while concentration remains qualitative context.
Missing/ambiguous benchmark data is never neutralized or silently substituted.
No complete global formula = no global Strategy Action Index.

## 65. SAI-C5 Technical Structure — Purpose and Boundary
`SAI-C5 Technical Structure` is the fifth formally specified numeric component for a future Strategy Action Index.

Purpose:
Measure whether KOSPI technical price structure confirms strength or deterioration using closing-confirmed price structure, validated support/resistance position and MA/VWAP trend position, while minimizing repeated scoring of price-derived indicators.

Authority boundary:
- Numeric C5 formula, component weights, numeric transforms, completeness rules and C5 conflict/shock conditions are owned by this SCORING_RULE.
- `TECHNICAL_RULE` remains the calculation/interpretation authority for Elliott/Fibonacci, swing confirmation, MA/VWAP, RSI, MACD, Ichimoku, ADX, Volume, support/resistance and breakout/breakdown confirmation.
- `E5 Technical Structure` remains the qualitative/adaptive owner for Market Regime, Transition, VH/H/M/L Evidence Priority, conflict resolution and re-validation.
- C5 does not replace E5 or TECHNICAL_RULE and cannot select/reconfirm a Market Regime by itself.

## 66. SAI-C5 Timeframe and Data Standard
Official C5 v1 uses KOSPI Daily / Closing-confirmed structure.

Intraday data may produce only `C5 Intraday Preview`.
An intraday touch, breakout or breakdown cannot overwrite the latest closing-confirmed C5 by itself.

Required data are validated outputs from TECHNICAL_RULE, based on HTS/KRX-priority market data:
- recent confirmed daily swing structure for PS
- nearest validated major Support Cluster `S` and Resistance Cluster `R` for SR when available
- MA20, MA60, VWAP20, VWAP60 for TP when available
- daily close aligned to the same session

Volume, RSI, MACD, ADX, Ichimoku and Elliott/Fibonacci may be used for confirmation/context according to TECHNICAL_RULE but are not direct C5 numeric terms in v1.

## 67. C5-A Price Structure Score
`PS` is the mandatory directional core.

Use the latest validated recent daily swing-high and swing-low structure from TECHNICAL_RULE.

Full directional classification:
- Higher High + Higher Low → `PS = +1.00`
- Lower High + Lower Low → `PS = -1.00`
- mixed HH+LL or LH+HL / non-directional structure → `PS = 0.00`

Partial one-sided structure when only one side is sufficiently validated:
- improving one-sided swing structure → `PS = +0.50`
- deteriorating one-sided swing structure → `PS = -0.50`

A closing-confirmed breakout above the relevant validated swing-high / resistance structure may set `PS = +1.00`.
A closing-confirmed breakdown below the relevant validated swing-low / support structure may set `PS = -1.00`.

Intraday touch alone cannot set PS to ±1.00.
If swing identity or confirmation is insufficient, PS is unavailable rather than guessed.

## 68. C5-B Support / Resistance Position Score
Use the nearest validated major Support Cluster `S` and Resistance Cluster `R` from TECHNICAL_RULE, with `R > S`.

When the daily close `C` remains inside an intact valid corridor:
`X = clip(2*(C-S)/(R-S)-1, -1,+1)`
`SR = 0.50*X`

Thus an intact corridor contributes only:
`-0.50 <= SR <= +0.50`.

Confirmed closing breakout above the validated Resistance Cluster → `SR = +1.00`.
Confirmed closing breakdown below the validated Support Cluster → `SR = -1.00`.

A touch alone does not create ±1.00.
Fibonacci, Elliott, MA/VWAP, previous high/low and volume concentration may help TECHNICAL_RULE validate a cluster, but their derived levels are not separately added again to C5.

If no unambiguous valid `S < R` corridor or confirmed boundary event can be established, SR is unavailable.

## 69. C5-C MA / VWAP Trend Position Score
Fixed v1 anchors:
- MA20
- MA60
- VWAP20
- VWAP60

For each valid anchor `A_j` using the same closing session:
- `Close > A_j * 1.002` → `T_j = +1`
- `Close < A_j * 0.998` → `T_j = -1`
- otherwise → `T_j = 0`

Then:
`TP = average(T_j)` across valid anchors.

Completeness for TP:
- 4/4 anchors valid → full TP
- 2 or 3 anchors valid → TP is usable, but C5 overall cannot be VERIFIED solely on a reduced TP set and is labeled PARTIAL when calculated
- fewer than 2 anchors valid → TP unavailable

The ±0.20% anchor band is a C5 v1 noise-control calibration rule.
MA/VWAP anchors form one composite TP and are not independent Evidence Groups.

## 70. SAI-C5 Formula / Missing / Partial Rule
Full formula when PS, SR and full TP are valid:
`SAI-C5 = 0.50*PS + 0.30*SR + 0.20*TP`
Status: eligible for `VERIFIED` when source/timeframe/calculation validation passes.

Component range:
`-1.00 <= SAI-C5 <= +1.00`

Internal weights:
- Price Structure: 50%
- Support / Resistance Position: 30%
- MA / VWAP Trend Position: 20%

If TP is based on only 2 or 3 valid anchors, use the same formula but label C5 `PARTIAL`.

### SR Missing Only
If PS and usable TP are valid but SR is unavailable:
`SAI-C5 = 0.70*PS + 0.30*TP`
Status: `PARTIAL`.

### TP Missing Only
If PS and SR are valid but TP is unavailable:
`SAI-C5 = 0.625*PS + 0.375*SR`
Status: `PARTIAL`.

### Mandatory / Insufficient Input
- PS unavailable/invalid → `SAI-C5 = DATA UNAVAILABLE`
- PS valid but both SR and TP unavailable → `SAI-C5 = DATA UNAVAILABLE`

Missing data is never converted to zero/Neutral.
The partial formulas above are predefined and therefore are not silent reweighting.

These internal C5 weights do not define C5's future global weight inside the complete Strategy Action Index.

## 71. C5 Confirmation / Divergence Boundary
The following are contextual validation inputs only and are not direct numeric C5 terms in v1:
- Volume → breakout/breakdown confirmation, contraction/exhaustion, weak-confirmation flag
- RSI → overbought/oversold and bullish/bearish divergence
- MACD → momentum confirmation/deceleration/divergence
- ADX → trend-strength confirmation only; ADX is not directional
- Ichimoku → supplementary structure confirmation
- Elliott/Fibonacci → S/R cluster, wave context, invalidation and Recovery Structure Failure review

A strong momentum reading or high ADX cannot reverse a confirmed price-structure failure by itself.

Raise `C5 Divergence: ACTIVE` when a price-vs-RSI/MACD divergence is validated under TECHNICAL_RULE and is material to the current structure.
Divergence does not directly change C5 weights or formula.

## 72. C5 Conflict / Shock Rules
### C5 Conflict
Raise `C5 Conflict: ACTIVE` when either condition is validated:
1. PS and SR have opposite signs and both satisfy `|value| >= 0.50`, or
2. PS and TP have opposite signs and both satisfy `|value| >= 0.50`.

When active:
- keep the formula unchanged
- disclose the conflict
- do not interpret a near-zero aggregate as absence of information
- pass the conflict to ADAPTIVE_VALIDATION_RULE / Change Detection as relevant
- do not alter C5 weights ad hoc.

### C5 Shock / Weight Shift Candidate
Raise `C5 Shock: ACTIVE` for validated structural events including:
- confirmed major Support Cluster breakdown
- confirmed major Resistance Cluster breakout
- current TECHNICAL_RULE Recovery Structure Failure review trigger, including a closing break below fixed Correction Low 5,593

C5 Shock is a Change Detection / Transition / Weight Shift candidate only.
It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 73. SAI-C5 Anti-Double-Counting and Anti-Circularity
For C5 numeric scoring:
- price/swing structure is scored once in PS
- validated S/R corridor or confirmed boundary event is scored once in SR
- MA20/60 + VWAP20/60 are compressed into one TP composite
- Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci are context/validation only in C5 v1 and are not independent numeric additions
- issue Breadth/ADL remains C3/E3
- sector leadership remains C4/E4
- Foreign/Institution flow remains C1/E1
- Program flow remains C2/E2
- Liquidity/Macro remains E6
- Options/OI/Volatility remains E7
- Binance/global leading remains E8

PS, SR and TP are predefined transforms of related technical price structure and must not be presented as three independent Evidence Groups. Together they form one E5/C5 technical evidence family.

Required separation:
`Validated Technical Data → C5 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C5 must not:
1. choose a Market Regime,
2. use that Regime to alter its own numeric weights,
3. use the altered C5 as the sole reason to reconfirm the same Regime.

VH/H/M/L Evidence Priority must never be converted into numeric C5 weights.

## 74. SAI-C5 Validation Cases
### Case A — Confirmed Bullish Structure
`PS=+1.00, SR=+0.40, TP=+1.00`
`C5 = 0.50 + 0.12 + 0.20 = +0.82`.
Expected: strong positive technical component, no conflict.

### Case B — Confirmed Bearish Structure
`PS=-1.00, SR=-1.00, TP=-1.00`
`C5=-1.00`.
Expected: strong negative technical component; structural breakdown dominates contextual oversold signals.

### Case C — Rising Structure / Support Retest
`PS=+1.00, SR=-0.40, TP=+0.50`
`C5=+0.48`.
Expected: positive but weakened technical structure; support retest does not mechanically become bearish.

### Case D — Price Structure / Trend Conflict
`PS=+1.00, SR=+0.20, TP=-0.75`
`C5=+0.41`.
Expected: positive aggregate + `C5 Conflict: ACTIVE`; do not call it clean bullish alignment.

### Case E — SR Missing
`PS=+1.00, TP=+0.50`
`C5 = 0.70*1.00 + 0.30*0.50 = +0.85`.
Status: `PARTIAL`.

### Case F — TP Missing
`PS=-1.00, SR=-0.50`
`C5 = 0.625*(-1.00) + 0.375*(-0.50) = -0.8125`.
Status: `PARTIAL`.

### Case G — PS Missing
SR and TP available but PS unavailable.
Expected: `SAI-C5 = DATA UNAVAILABLE`.

### Case H — Volume Spike Alone
Strong volume without validated directional PS/SR structure.
Expected: no independent bullish/bearish C5 numeric contribution.

### Case I — Intraday Breakout Without Close Confirmation
Intraday price exceeds resistance but the session has not closed/confirmed.
Expected: `C5 Intraday Preview` / context only; official closing-confirmed PS/SR remains unchanged.

### Case J — Recovery Structure Failure Trigger
Closing break below 5,593 under current TECHNICAL_RULE.
Expected: `C5 Shock: ACTIVE`, Recovery Structure Failure review, no automatic global SAI or Regime change.

## 75. Current Component / Global SAI Status After C5
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C4 Sector / Leadership`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C5 Technical Structure`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

C1-C5 remain component-level formulas only.
The global SAI remains unavailable until remaining components, global aggregation, global missing/partial handling, final range/Action Bands and required regression/validation are complete.

C5 final principle:
Price structure is the directional core.
Support/resistance and MA/VWAP refine confirmation without multiplying the same technical evidence into independent groups.
Momentum, Volume and Elliott/Fibonacci validate structure but do not become extra numeric terms in v1.
Intraday preview does not replace closing-confirmed structure.
No complete global formula = no global Strategy Action Index.