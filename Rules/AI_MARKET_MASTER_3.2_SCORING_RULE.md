# AI Market Master 3.2 Scoring Rule

Version: 3.2 Unified Stable
Status: Scoring Authority

## 1. Scope
This file is the only authority for numeric `AI Master Score` and `Strategy Action Index` definitions, inputs, weights, formulas, missing-data handling and validation.

## 2. Current Official Status
At the time of this unified rule creation, no previously verified authoritative 3.0/3.1/3.2 repository file has been confirmed to contain a complete reproducible numeric formula for either:
- AI Master Score
- Strategy Action Index

Therefore the official current numeric state is:
- `AI Master Score: DATA UNAVAILABLE`
- `Strategy Action Index: DATA UNAVAILABLE`

This is intentional and prevents invented scoring.

## 3. Numeric Score Activation Gate
A numeric score may be activated only after all of the following are explicitly defined and verified in this file:
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

Until then, numeric output is prohibited.

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

These are not automatically AI Master Score components unless a future verified formula explicitly defines them as such.

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

The following conversions are prohibited unless a future official formula in this SCORING_RULE explicitly defines and validates them:
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
If future official scoring formulas are activated, missing mandatory data must follow the formula's explicitly documented missing-data rule. If no such rule exists, output DATA UNAVAILABLE rather than silently reweighting.

## 10. Partial Score Rule
A partial numeric score is prohibited unless the future official formula explicitly defines:
- which inputs may be missing
- how weights are adjusted or not adjusted
- how the output is labeled
- the minimum completeness threshold

Otherwise use DATA UNAVAILABLE.

## 11. Binance Integration
Binance does not create a separate AI Market Master numeric score. Binance G1-G6 signals may feed future official scoring only if the formula explicitly defines their role. Symbol availability or Binance VERIFIED status is not itself a market score.

Binance use inside E8 Global Leading does not grant it numeric scoring authority.

## 12. Strategy Action Index Principle
Strategy Action Index, when eventually defined, must represent execution intensity according to a reproducible official formula. It must not be a disguised analyst opinion.

Qualitative Strategy postures from ADAPTIVE_VALIDATION_RULE — Defensive Observation, Hold, Constructive Hold, Accumulation, Risk Reduction Watch, Staged Reduction, Strong Risk Reduction and Extreme Risk Control — are not Strategy Action Index values.

Until an official formula is verified, output DATA UNAVAILABLE while still allowing qualitative strategy under MASTER_RULE and ADAPTIVE_VALIDATION_RULE.

## 13. AI Master Score Principle
AI Master Score, when eventually defined, must represent integrated market evidence according to a reproducible official formula and cannot be inferred from the final Signal, Market Regime, Evidence Priority Matrix or final Portfolio Action alone.

Until such formula is verified, output DATA UNAVAILABLE.

## 14. Legacy Engine Score Boundary
Legacy backups contain historical concepts such as Flow Score, Momentum Score, Risk Score, AI Score Delta and Engine Reliability Scoring, but no currently verified complete reproducible formula has been adopted here.

Therefore those historical labels/concepts do not authorize current numeric scoring or numeric adaptive weights.

## 15. Regression Protection
The following are always invalid:
- incomplete inputs + invented numeric score
- signal color converted to a number without formula
- qualitative consensus converted to a percentage
- score copied from an earlier session without recomputation
- hidden/manual analyst weighting
- silent weight renormalization
- VH/H/M/L converted to numeric values without formal adoption
- Market Regime converted into a score by intuition
- qualitative Strategy posture presented as Strategy Action Index

## 16. Future Formula Adoption Procedure
Before activating a numeric formula:
1. identify source/version
2. compare against legacy rules
3. document all inputs and weights
4. verify no conflict with MASTER/DASHBOARD/TECHNICAL/BINANCE/ADAPTIVE_VALIDATION rules
5. test known cases
6. define partial/missing handling
7. update VERSION_STATUS and CHANGELOG
8. only then change Current Official Status from DATA UNAVAILABLE

## 17. Final Principle
No official formula = no official number.
Adaptive priority ≠ numeric weight.
Reliability > Speed.
DATA UNAVAILABLE is preferable to fabricated precision.
