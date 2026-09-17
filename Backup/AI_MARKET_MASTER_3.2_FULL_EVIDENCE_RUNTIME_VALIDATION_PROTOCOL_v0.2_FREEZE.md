# AI Market Master 3.2 — Full Evidence Runtime Validation Protocol v0.2
## Design Freeze

Date: 2026-09-17
Status: EXPERIMENTAL VALIDATION PROTOCOL / NOT OFFICIAL 3.2 AUTHORITY
Supersedes for future prospective validation: `AI_MARKET_MASTER_3.2_FULL_EVIDENCE_RUNTIME_VALIDATION_PROTOCOL_v0.1_FREEZE.md`

## 1. Purpose
Accumulate prospective, no-hindsight Full Evidence samples so the Compounding Overlay and Risk Budget Execution layer can be validated quickly enough for practical use while preserving a stricter path for later official 3.2 integration.

This protocol is a logging and validation layer only. It does not alter any market rule, C1-C8 formula, Regime formula, Strategy Action Index, Historical Proxy rule, portfolio execution hierarchy, or official Authority file.

v0.2 adds a **provisional-adoption path within 2–3 months**. Official 3.2 integration remains a separate, stricter review.

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

Provisional adoption does not relax the no-hindsight lock.

## 6. Sample quality classes
### FULL
All mandatory C1-C8 inputs required by the applicable gate are available and validation completes without material missing-data dependency.

### PARTIAL
One or more relevant inputs are missing but the system can still produce a bounded partial interpretation. Missing values remain explicit.

### BLOCKED
Evidence conflict, mandatory missing data, or execution authority prevents a valid action.

All three classes remain in the dataset.

## 7. Validation stages
No arbitrary success score is introduced. Sample counts are adequacy gates, not performance guarantees.

### Stage 1 — Operational verification
Minimum:
- 20 prospective samples,
- representation from more than one materially different Regime family.

Purpose:
- verify logging consistency,
- gate determinism,
- missing/conflict handling,
- execution mapping,
- Outcome Updater stability.

Stage 1 can establish that the system operates correctly. It cannot by itself justify adoption.

### Stage 2A — Early provisional-adoption review
Earliest review when all are met:
- minimum 30 prospective samples,
- at least 2 months elapsed from the first prospective sample,
- at least 8 deterioration / risk-control observations,
- at least 8 recovery / restoration observations,
- representation from at least 3 materially different Regime families,
- a substantial majority of eligible +5d outcomes matured,
- enough +20d outcomes matured to inspect path quality without relying only on +1d/+5d noise.

Purpose:
- determine whether the Candidate model is suitable for **PROVISIONAL ADOPTION** in practical operation while validation continues.

Possible review results:
- `PROVISIONAL ADOPT`
- `CONTINUE VALIDATION`
- `REJECT / REDESIGN`

A provisional-adoption decision is a documented review judgment, not an automatic numeric score.

### Stage 2B — Three-month provisional checkpoint
At 3 months from the first prospective sample, conduct a mandatory provisional review if Stage 2A has not already produced a decision.

Preferred adequacy target:
- 40 or more prospective samples,
- at least 10 deterioration / risk-control observations,
- at least 10 recovery / restoration observations,
- at least 3 materially different Regime families.

If the preferred target is not met because of weak regime diversity or too few risk/recovery events, the result must be `CONTINUE VALIDATION`, not a forced adoption or rejection.

This checkpoint is designed so a practically useful decision can normally be reached within about 2–3 months when the market supplies enough varied evidence.

### Stage 3 — Official integration eligibility review
Minimum:
- 60 prospective samples,
- at least 6 months elapsed from the first prospective sample,
- mature +20d outcomes for a substantial majority,
- adequate regime diversity.

Purpose:
- decide whether official 3.2 integration is justified.

Stage 3 remains stricter than provisional adoption and is not shortened by v0.2.

## 8. Provisional-adoption boundary
`PROVISIONAL ADOPT` means:
- the Candidate overlay may be used as the default experimental execution overlay under its existing guardrails,
- prospective logging and Outcome maturation continue without interruption,
- official 3.2 Authority files remain unchanged,
- Candidate thresholds and execution rules remain frozen unless a new version is explicitly created.

Provisional adoption must not be interpreted as proof of profitability or as final official integration.

A provisional review must explicitly inspect whether there is evidence of:
- repeated false-positive reductions,
- materially delayed restoration after V-rebounds,
- unnecessary Core sales,
- excessive turnover,
- frequent execution blocking caused by missing data,
- regime-specific failure concentrated in one market family.

Material unresolved failure in these areas favors `CONTINUE VALIDATION` or `REJECT / REDESIGN` rather than provisional adoption.

## 9. Review metrics
At each review, report without inventing an AI Master Score:
- sample count by FULL / PARTIAL / BLOCKED,
- sample count by Regime / action type,
- deterioration / risk-control observation count,
- recovery / restoration observation count,
- reduction signals followed by meaningful downside,
- reduction signals followed by rapid reversal / false positive,
- restoration timing and V-rebound participation,
- Core-sale frequency,
- percentage of reductions satisfied entirely by Leverage + Tactical sleeves,
- PARTIAL EXECUTION frequency,
- LEVERAGE RESTORE BLOCKED frequency,
- turnover / action count,
- +1d / +5d / +20d path distributions where mature,
- outcome maturity coverage by horizon.

No single metric is allowed to become an unapproved hidden score.

## 10. Integration boundary
Official 3.2 integration remains blocked until a later formal Stage 3 review explicitly passes architecture, evidence quality, execution behavior, and regression checks.

The Runtime Validation Protocol itself must not be treated as a seventh Authority file or a ninth Dashboard category.

## 11. Transition from v0.1
- Existing prospective samples remain valid and continue in the same Runtime Log.
- No existing signal or outcome is rewritten because of this Protocol revision.
- Only validation adequacy and review timing changed.
- v0.1 remains preserved as historical audit evidence.
- Future adequacy reviews use v0.2 unless a later version supersedes it.

## 12. Version lock
This file freezes Runtime Validation Protocol v0.2 before additional prospective accumulation.

Any future change to sample creation rules, mandatory fields, no-hindsight handling, provisional-adoption gates, or official integration gates requires v0.3 or later.
