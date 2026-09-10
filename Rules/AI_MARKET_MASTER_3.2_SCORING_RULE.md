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

`SAI-C1 Smart Money` is defined below as a component specification only. It must not be presented as the final Strategy Action Index.

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

## 27. Final Principle
No complete official global formula = no official global number.
A validated sub-component does not equal Strategy Action Index.
Adaptive priority ≠ numeric weight.
Reliability > Speed.
DATA UNAVAILABLE is preferable to fabricated precision.
