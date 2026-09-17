# AI Market Master 3.2 — Full Evidence Candidate v1.0
## Prospective Validation Freeze

Date: 2026-09-17
Status: **EXPERIMENTAL CANDIDATE / PROSPECTIVE VALIDATION TARGET / NOT OFFICIAL 3.2 AUTHORITY**

## 1. Purpose
Freeze one and only one Full Evidence improvement model for prospective validation under Runtime Validation Protocol v0.2.

Candidate v1.0 is the common Full Evidence evidence-gated Compounding Overlay architecture. It is **not** Historical Proxy v0.2, v0.3, or v0.4. Those proxy versions remain historical diagnostic variants only and are not competing prospective Full Evidence models.

Official AI Market Master 3.2 Authority files, C1-C8 formulas, Regime rules, Strategy Action Index, and AI Master Score state remain unchanged.

## 2. Candidate execution chain
`3.2 Market State -> Full Evidence Gate -> Overlay Target Risk Budget -> Risk Budget Execution Mapper -> Runtime Log -> Outcome Updater -> Validation Monitor`

Market Intelligence and Portfolio Execution remain separate.

## 3. Core operating philosophy
- Strategic baseline risk budget = 100.
- Preserve long-term compounding and market participation by default.
- Regime alone never authorizes a trade.
- Multiple independent Full Evidence categories are required for reduction/restoration.
- Slow Exit / Fast Re-entry is mandatory.
- Leverage and Tactical exposure are reduced before Core.
- Core is protected longest and reduced only with explicit Full Evidence authority.
- No leverage expansion above the separately authorized strategic baseline.
- Material unresolved conflict -> HOLD.
- Missing data is never converted to Neutral or Zero.

## 4. Allowed normalized risk-budget states
`100 / 95 / 90 / 80 / 70 / 60`

Rules:
- minimum normal action step = 5 percentage points,
- maximum ordinary single reduction = 10 percentage points,
- strong recovery may restore up to 20 percentage points,
- no ad-hoc intermediate target,
- no full-market exit,
- no Overlay-created leverage above 100.

Historical Proxy mode remains separately capped at 80 and is not Candidate v1.0 execution authority.

## 5. Evidence classes
A-class core evidence:
- C1 Smart Money
- C2 Program
- C5 Technical

B-class confirmation evidence:
- C3 Breadth
- C4 Leadership / Rotation

C-class environment evidence:
- C6 Liquidity / Macro
- C7 Volatility / Derivatives
- C8 Global Leading

Correlated observations must not be double-counted as independent evidence.

## 6. Frozen reduction gates
### -5 percentage points
Require all:
- R4 or worse,
- at least 1 deteriorating A-class category,
- at least 3 independent deteriorating categories total,
- C5 does not materially conflict with reduction.

### Additional -5 percentage points
Require all:
- R4/R5 persistence,
- at least 2 deteriorating A-class categories,
- at least 4 deteriorating categories total,
- confirmation from at least 2 of A/B/C evidence classes.

### Strong -10 percentage points
Require all:
- R5 or R6,
- strong deterioration in C1 or C2,
- C5 structure/trend breakdown,
- at least 5 deteriorating categories total,
- C6 liquidity deterioration or C7 volatility expansion.

### Deepest 70 -> 60 transition
Only when:
- R6 Panic,
- at least 5 independent deteriorating categories,
- strong C1 or C2 deterioration,
- C5 structural breakdown.

## 7. Frozen restoration gates
### +10 percentage points
Require all:
- R8 entry or R7 -> R8 transition,
- C1 or C2 improvement,
- C3 breadth improvement,
- C5 price-structure recovery,
- at least 3 improving categories total.

### Additional +10 percentage points
Require all:
- R8 persistence,
- at least 2 improving A-class categories,
- at least 4 improving categories total,
- C7 stabilization or C8 improvement.

### Return to 100
Require all:
- R1/R2 or strong R8,
- at least 2 positives among C1/C2/C5,
- at least 4 positive categories total,
- no unresolved major conflict.

Strong V-rebound recovery may override normal restoration cooldown when the frozen recovery gate is satisfied.

## 8. Execution hierarchy
When reduction is authorized, use this order:
1. profitable leverage,
2. relative-weakness / high-beta leverage,
3. other leverage including losing leverage if risk remains elevated,
4. Tactical high-beta / weak-relative-strength exposure,
5. other Tactical exposure,
6. Core spot last.

Core Preservation Gate:
- if Leverage + Tactical removal cannot reach the target and Full Evidence does not explicitly authorize deeper Core reduction, stop at the achievable level and return `PARTIAL EXECUTION / CORE PROTECTED`.

Restoration order:
1. restore previously reduced Core toward strategic baseline,
2. restore Tactical,
3. restore Leverage last and only with separate leverage authorization.

## 9. Cost / cooldown / hysteresis
- Non-emergency Expected Edge should exceed estimated transaction cost by at least 2x when the Cost Gate can be estimated.
- After a reduction, normal same-direction cooldown is at least 1 trading day.
- Material worsening such as R5 -> R6 with new independent confirmation may bypass normal reduction cooldown.
- Deterioration becoming merely neutral is not a restoration signal; a separate Recovery Gate is mandatory.

## 10. Runtime and no-hindsight lock
Candidate v1.0 uses:
- append-only Runtime Log,
- documented CORRECTION events only for actual data/input errors,
- +1d / +5d / +20d observed KOSPI outcomes,
- close-based 5d/20d MAE and MFE,
- no future-session imputation,
- no losing-sample deletion,
- no threshold retuning from prospective outcomes without creating Candidate v1.1 or later.

The candidate itself is frozen for the 2–3 month provisional-validation window.

## 11. Provisional-adoption review
Validation authority: `AI_MARKET_MASTER_3.2_FULL_EVIDENCE_RUNTIME_VALIDATION_PROTOCOL_v0.2_FREEZE.md`.

Earliest provisional review:
- >=30 prospective samples,
- >=2 months elapsed,
- >=8 deterioration/risk-control observations,
- >=8 recovery/restoration observations,
- >=3 materially different Regime families,
- substantial +5d maturity and enough +20d observations to inspect path quality.

Three-month preferred checkpoint:
- >=40 samples,
- >=10 deterioration/risk-control observations,
- >=10 recovery/restoration observations,
- >=3 Regime families.

Allowed review outcomes:
- `PROVISIONAL ADOPT`
- `CONTINUE VALIDATION`
- `REJECT / REDESIGN`

No hidden score and no automatic adoption are allowed.

## 12. Official integration boundary
Official 3.2 integration remains separate and requires the stricter Stage 3 review under Protocol v0.2:
- >=60 prospective samples,
- >=6 months elapsed,
- mature +20d outcomes for a substantial majority,
- adequate Regime diversity,
- formal architecture/evidence/execution/regression review.

## 13. Explicit exclusions
Candidate v1.0 does not include:
- Historical Proxy v0.2/v0.3/v0.4 as prospective competing models,
- MA-only exit,
- RSI-only selling,
- mechanical drawdown-only buying,
- full cash exit,
- leverage expansion above strategic authorization,
- sector-rotation alpha,
- security-selection alpha,
- OFI/BSI futures alpha,
- hidden adaptive thresholds derived from runtime outcomes.

## 14. Current prospective start
First prospective sample remains:
`AMM32-20260917-CLOSE-30e87244fdc5`

It is retained under the same Runtime Log and Protocol v0.2. No existing signal, correction, or outcome is rewritten by this Candidate freeze.

## 15. Version lock
This file is the single prospective Candidate v1.0 definition.

Any change to:
- Reduction/Restoration Gates,
- allowed risk-budget states,
- evidence-class requirements,
- Core Preservation Gate,
- reduction/restoration hierarchy,
- cooldown/hysteresis,
- Cost Gate,
- no-hindsight rules,
requires a new Candidate version. Silent modification is prohibited.
