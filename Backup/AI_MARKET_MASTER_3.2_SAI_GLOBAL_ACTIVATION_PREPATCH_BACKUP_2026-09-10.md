# AI Market Master 3.2 — Global Strategy Action Index Activation Pre-patch Backup

Date: 2026-09-10
Status: NON-AUTHORITATIVE / PRE-PATCH / RULE-DESIGN VERIFIED
Purpose: Recovery and regression checkpoint before global Strategy Action Index activation.

## 1. Current Official State Before Patch
- AI Master Score = DATA UNAVAILABLE
- Strategy Action Index = DATA UNAVAILABLE
- C1-C8 component formulas exist and cover E1-E8 at component level.
- Global aggregation, Base Weights, Missing/Partial, Conditional Adaptive Weight, Action Bands and regression must be formally adopted before global SAI activation.

Current official blob SHAs:
- MASTER_RULE: ea746bf62edbf61521dd26d1855d3b4aadc7b951
- DASHBOARD_RULE: 0ec39d1418edf09098a7a431e904fc5bdfd60230
- SCORING_RULE: fa51e24dd54bacc2c3aacc613f30ef6451a9e426
- TECHNICAL_RULE: b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f
- BINANCE_RULE: f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d
- ADAPTIVE_VALIDATION_RULE: 8833555b261e334b6b0f39d4ce272776fd97af71
- VERSION_STATUS: 81052544bc9c602e1481a3fb670733a400f70e6e
- CHANGELOG: 675779fbdff3fd611f8bad0f4c15d5d9e2fc9e78

## 2. Global Base Weights v1
Base component weights:
- C1 Smart Money: 18%
- C2 Program Flow: 12%
- C3 Breadth / Internal: 15%
- C4 Sector / Leadership: 10%
- C5 Technical Structure: 20%
- C6 Liquidity / Macro: 10%
- C7 Volatility / Derivatives Risk: 8%
- C8 Global Leading: 7%

Sum = 100%.

Base formula:
`SAI_Base = 0.18*C1 + 0.12*C2 + 0.15*C3 + 0.10*C4 + 0.20*C5 + 0.10*C6 + 0.08*C7 + 0.07*C8`

Range: `[-1.00,+1.00]`.
These are v1 design-calibration weights, not empirical backtest-optimal weights.

## 3. Global Missing / Partial Gate
Global VERIFIED requires all C1-C8 usable and each component status VERIFIED with current source/freshness validation satisfied.

A component whose own predefined PARTIAL formula succeeds is globally usable, but its presence forces global SAI status to PARTIAL.

Global PARTIAL calculation uses:
`SAI_Partial = sum(w_i*C_i for usable components) / sum(w_i for usable components)`

PARTIAL is allowed only when all are true:
1. C5 Technical Structure is usable;
2. at least one of C1/C2 is usable (Flow family);
3. at least one of C3/C4 is usable (Internal family);
4. at least one of C6/C7/C8 is usable (Risk/Environment family);
5. at least 6 of 8 components are usable;
6. original Base Weight coverage is at least 70%.

Otherwise Strategy Action Index = DATA UNAVAILABLE.
Missing is never converted to zero/Neutral.

## 4. Evidence Family Scores
For conflict and conditional-weight logic only when all C1-C8 are VERIFIED:
- `F_FLOW = 0.60*C1 + 0.40*C2`
- `F_INTERNAL = 0.60*C3 + 0.40*C4`
- `F_STRUCTURE = C5`
- `F_ENV = 0.40*C6 + 0.32*C7 + 0.28*C8`

Base family weights are 30% / 25% / 20% / 25%.
These four family scores are analytical aggregation helpers inside SCORING_RULE; they are not additional Evidence Groups and do not replace E1-E8.

## 5. Global Conflict
`Global SAI Conflict: ACTIVE` when any two independent family scores have opposite signs and both satisfy `|F| >= 0.50`.

When active:
- keep the mathematically calculated Base/Partial score;
- do not interpret near-zero as absence of information;
- block Conditional Adaptive Weight;
- disclose conflict and reduce execution confidence when decision-relevant;
- resolve action through ADAPTIVE_VALIDATION and MASTER portfolio rules.

## 6. Conditional Adaptive Weight v1
Adaptive numeric weighting is permitted only when:
- C1-C8 are all VERIFIED;
- Global SAI Conflict is not ACTIVE;
- qualifying Shock/confirmation data are validated;
- no qualifying trigger depends solely on a mechanical event distortion.

Adaptive family events:
- Flow Event: C1 and C2 same direction; one has Shock ACTIVE and the other has |C|>=0.50.
- Internal Event: C3 and C4 same direction; one has Shock ACTIVE and the other has |C|>=0.50.
- Structure Event: C5 Shock ACTIVE plus at least one independent family score (Flow/Internal/Environment) with same direction and |F|>=0.50.
- Environment Event: at least two of C6/C7/C8 same direction, both |C|>=0.50, and at least one has Shock ACTIVE.

Mechanical Event guard:
A C2 or C7 Shock accompanied by its Mechanical Event flag cannot be the sole qualifying Shock for numeric reweighting unless structural confirmation survives the event review under the owning rules.

Adjustment:
- no event -> Base Weights unchanged;
- exactly one qualifying family event -> that family +5 percentage points; the other three families are reduced proportionally to their Base family weights;
- exactly two qualifying family events with the same direction -> each active family +3 percentage points; the other two are reduced proportionally;
- exactly two qualifying events with opposite directions -> Adaptive Weight BLOCKED; Base Weights retained + conflict/transition review;
- three or more qualifying family events -> Base Weights retained and `Broad Market Shock: ACTIVE`; no additional reweighting because broad alignment no longer requires preference among families.

Maximum total family-weight reallocation = 6 percentage points.
Component ratios inside each family remain fixed at their Base proportions.
All adjusted component weights must be non-negative and sum to 1.00.

Adaptive weighting must never use VH/H/M/L as numbers and must never use the resulting Final SAI as the sole reason to reconfirm the same Market Regime.

## 7. Required Anti-Circularity Order
`C1-C8 calculation -> Base SAI -> Preliminary Regime -> Adaptive Validation / Transition / Conflict -> Regime Re-validation -> Conditional Adaptive Event check -> Final SAI -> Strategy / Portfolio Response`

Prohibited loop:
`Regime -> numeric reweight -> Final SAI -> same Regime reconfirmed solely from that Final SAI`.

## 8. Action Bands v1
Action Bands express SAI execution bias, not automatic trade commands.

- `+0.60 <= SAI <= +1.00` -> Strong Positive Execution Bias
- `+0.30 <= SAI < +0.60` -> Positive Execution Bias
- `-0.30 < SAI < +0.30` -> Balanced / Hold Bias
- `-0.60 < SAI <= -0.30` -> Negative Execution Bias
- `-1.00 <= SAI <= -0.60` -> Strong Negative Execution Bias

Suggested MASTER vocabulary after independent confirmation:
- Strong Positive -> 적극매수 / 비중확대 검토
- Positive -> 분할매수 / 보유강화 검토
- Balanced -> 보유 / 현금대기 / 다음 확인
- Negative -> 비중축소 / 분할매도 검토
- Strong Negative -> 적극 비중축소 / 현금확보 검토, leverage first

Safeguards:
- SAI band never overrides Market Regime, Transition, Technical location, material conflict or portfolio exposure.
- PARTIAL SAI may show a numeric bias but cannot by itself authorize the strongest aggressive action.
- Global Conflict ACTIVE blocks adaptive weighting and prevents score-only execution.
- Mechanical Event ACTIVE requires structural re-validation before event-sensitive evidence drives strong action.
- Final portfolio action remains owned by MASTER_RULE + ADAPTIVE_VALIDATION_RULE.

Action Band thresholds are v1 design calibrations, not empirically optimized cutoffs.

## 9. Regression / Stress Validation
Mathematical checks performed before patch:
- Base weights sum exactly to 1.00.
- Family weights sum to 1.00.
- All allowed one-family and two-family adaptive reweight patterns preserve total weight 1.00 and all component weights remain positive.
- Exhaustive corner test across all 256 combinations of C1-C8 values at {-1,+1}, repeated across Base and all allowed one/two-family weight patterns, keeps Final SAI inside [-1,+1].
- all C_i=+1 -> SAI=+1.00.
- all C_i=-1 -> SAI=-1.00.
- one-family +5pp redistribution has theoretical score displacement bounded by 0.10 versus Base for component values in [-1,+1].
- two-family total +6pp redistribution has theoretical score displacement bounded by 0.12 versus Base.
- conflict case with Flow/Internal strongly positive and Structure/Environment strongly negative can yield near-neutral arithmetic while Global Conflict remains ACTIVE, preventing false neutral interpretation.
- Partial gate rejects C5-missing states even with seven other components.
- Partial gate rejects fewer than six usable components even if all required families are represented.
- Partial gate accepts valid six-plus-component states only when family and 70% coverage gates pass.
- any component PARTIAL -> global status PARTIAL; Conditional Adaptive Weight blocked.
- Action Bands are monotonic and sign-symmetric around the neutral interval.

This is formula/regression validation, not empirical market-performance backtesting.

## 10. Activation Decision
Architecture: READY BY RULE DESIGN.
Global Base Weight: READY.
Global Missing/Partial Gate: READY.
Global Conflict: READY.
Conditional Adaptive Weight: READY.
Action Bands: READY.
Mathematical regression/stress tests: PASS.
Empirical backtest optimization: NOT ESTABLISHED.

If officially patched, Strategy Action Index may become a reproducible numeric output when the runtime data gate passes. AI Master Score remains DATA UNAVAILABLE.
