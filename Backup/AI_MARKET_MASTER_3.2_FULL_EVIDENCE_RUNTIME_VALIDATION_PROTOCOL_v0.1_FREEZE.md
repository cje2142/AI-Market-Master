# AI Market Master 3.2 — Full Evidence Runtime Validation Protocol v0.1
## Design Freeze

Date: 2026-09-17
Status: EXPERIMENTAL VALIDATION PROTOCOL / NOT OFFICIAL 3.2 AUTHORITY

## 1. Purpose
Accumulate prospective, no-hindsight Full Evidence samples so the Compounding Overlay and Risk Budget Execution layer can be validated before official 3.2 integration.

This protocol is a logging and validation layer only. It does not alter any market rule, C1-C8 formula, Regime formula, Strategy Action Index, Historical Proxy rule, or portfolio execution hierarchy.

## 2. When a runtime sample is created
Create one validation sample whenever an actual AI Market Master 3.2 Dashboard execution produces a usable market-state decision and the Full Evidence Overlay can be evaluated.

A sample is still recorded when execution is blocked or partial. Blocked observations are evidence and must not be discarded.

Do not create duplicate samples from repeated re-runs of the same underlying snapshot unless materially new market data arrived.

## 3. Signal-time fields — frozen before outcomes
Each sample must preserve the following as they existed at signal time:

### A. Identity
- sample_id
- market date
- timestamp / session checkpoint
- Data Mode and Validation Status where applicable

### B. Market evidence
- C1 Smart Money: value/status
- C2 Program Flow: value/status
- C3 Breadth/Internal: value/status
- C4 Sector Leadership: value/status
- C5 Technical Structure: value/status
- C6 Liquidity/Macro: value/status
- C7 Volatility/Derivatives: value/status
- C8 Global Leading: value/status
- explicit missing fields; missing != neutral

### C. State
- Preliminary Regime
- Validated Regime
- Transition state
- material evidence conflicts
- Evidence Gate result
- Reduction / Restoration Gate reached, if any

### D. Overlay execution intent
- target normalized risk budget
- action direction: HOLD / REDUCE / RESTORE / BLOCKED
- allowed step size
- reason codes

### E. Runtime portfolio execution inputs
Portfolio composition is execution input only and never market evidence.
Record when supplied:
- Core sleeve risk units / nominal units
- Tactical sleeve risk units / nominal units
- Leverage sleeve risk units / nominal units
- exact risk multipliers available: YES/NO
- leverage restoration authority: YES/NO
- Core reduction authority where deeper reduction requires it

### F. Mapped execution output
- before Core/Tactical/Leverage
- after Core/Tactical/Leverage
- mapper status: EXECUTABLE / PARTIAL EXECUTION CORE PROTECTED / LEVERAGE RESTORE BLOCKED / HOLD CONFLICT / DATA PARTIAL
- actual action hierarchy used
- unresolved execution constraints

## 4. Outcome fields — never known at signal time
Outcome fields remain PENDING until the relevant trading-session horizon has completed.

Primary market path: KOSPI.
Secondary confirmation where available: KOSPI200 / KOSDAQ.

Populate:
- +1 trading-session close return
- +5 trading-session close return
- +20 trading-session close return
- 5d MAE / MFE using closes
- 20d MAE / MFE using closes
- recovery / new-low notes only from observable price path

Do not impute unavailable future sessions.

## 5. No-hindsight lock
Once signal-time fields are written:
- do not alter C1-C8 values because later prices moved differently,
- do not change Regime or Gate result unless correcting a documented data/input error,
- any correction must preserve both original and corrected records with reason,
- do not remove losing or inconvenient samples,
- do not add a historical sample after seeing its outcome to improve statistics,
- do not select a new threshold from this log without versioning a new design.

## 6. Sample quality classes
### FULL
All mandatory C1-C8 inputs required by the applicable gate are available and validation completes without material missing-data dependency.

### PARTIAL
One or more relevant inputs are missing but the system can still produce a bounded partial interpretation. Missing values remain explicit.

### BLOCKED
Evidence conflict, mandatory missing data, or execution authority prevents a valid action.

All three classes remain in the dataset.

## 7. Minimum validation stages
No arbitrary success score is introduced here.

Validation proceeds in stages:

### Stage 1 — Operational verification
Minimum 20 prospective samples across more than one market regime.
Purpose: verify logging consistency, gate determinism, missing/conflict handling, and execution mapping.

### Stage 2 — Preliminary behavior review
Minimum 40 prospective samples with at least:
- 10 deterioration / risk-control observations,
- 10 recovery / restoration observations,
- representation from at least 3 materially different Regime families.
Purpose: evaluate false-positive reduction, recovery lag, Core protection, and turnover behavior.

### Stage 3 — Integration eligibility review
Minimum 60 prospective samples and at least 6 months elapsed from the first prospective sample, with mature +20d outcomes for a substantial majority.
Purpose: decide whether official integration is justified.

These are sample-adequacy gates, not performance guarantees. More data may still be required if regime diversity is poor.

## 8. Review metrics
At each review, report without inventing an AI Master Score:
- sample count by FULL / PARTIAL / BLOCKED
- sample count by Regime / action type
- reduction signals followed by meaningful downside
- reduction signals followed by rapid reversal / false positive
- restoration timing and V-rebound participation
- Core-sale frequency
- percentage of reductions satisfied entirely by Leverage + Tactical sleeves
- PARTIAL EXECUTION frequency
- LEVERAGE RESTORE BLOCKED frequency
- turnover/action count
- +1d / +5d / +20d path distributions where mature

No single metric is allowed to become an unapproved hidden score.

## 9. Integration boundary
Official 3.2 integration remains blocked until a later formal review explicitly passes architecture, evidence quality, execution behavior, and regression checks.

The Runtime Validation Protocol itself must not be treated as a seventh Authority file or a ninth Dashboard category.

## 10. Version lock
This file freezes Runtime Validation Protocol v0.1 before prospective sample accumulation.

Any change to sample creation rules, mandatory fields, no-hindsight handling, or adequacy gates requires v0.2 or later.
