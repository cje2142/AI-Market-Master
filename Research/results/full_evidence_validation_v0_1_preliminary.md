# AI Market Master 3.2 — Full Evidence Validation v0.1 Preliminary Findings

Status: PARTIAL / DIAGNOSTIC / NOT OFFICIAL 3.2 INTEGRATION
Date: 2026-09-17
Basis: frozen 9-event validation set + reproducible KOSPI forward-path event study.

## 1. Architecture finding before outcome interpretation
Historical Proxy v0.2 and v0.4 are not separate Full Evidence engines. Their modifications were defined for Historical Proxy exposure behavior.

The Full Evidence candidate remains the common evidence-gated architecture inherited from v0.1:
Regime -> Evidence Gate -> Exposure Map -> Cost Gate -> Minimum Action -> Cooldown/Hysteresis -> Position Transition -> Execution.

Therefore this study does not choose v0.2 vs v0.4 as if they had different C1-C8 execution formulas.

## 2. Frozen event-study observations

### 2026-07-15 — Strong Bull / Recovery
Historical posture: HOLD / avoid chasing / partial profit management.
KOSPI: +1d -6.37%, +5d -2.57%, 5d MAE -10.54%, +20d -6.47%, 20d MAE -23.21%.
Interpretation: avoiding chase and allowing profit management was supported by the path. A full core exit is not demonstrated because the event was followed by large two-way volatility rather than a clean one-direction decline.

### 2026-07-16 — Panic / Capitulation
Historical posture: NO CHASE-SELL / reduce leverage on rebound rather than dumping core.
KOSPI: +1d -4.46%, +5d -1.91%, 5d MFE +4.05%, +20d +2.31%, 20d MAE -17.99%.
Interpretation: the path supports the distinction between panic risk control and core liquidation. There was meaningful rebound opportunity despite continued volatility. This is consistent with leverage/high-beta reduction before core spot.

### 2026-07-21 — Selective strength / weak internals
Historical posture: HOLD / SELECTIVE BUY.
KOSPI: +1d +0.74%, +5d -10.73%, 5d MFE +5.17%, +20d -4.10%, 20d MAE -17.11%.
Interpretation: selective buying without stronger recovery confirmation was vulnerable to renewed downside. This event argues for keeping Recovery Gate requirements for adding tactical risk.

### 2026-07-24 — Risk-Off Correction
Historical posture: NO AGGRESSIVE BUY.
KOSPI: +5d -1.42%, 5d MAE -16.40%, +20d +0.09%.
Interpretation: strong support for avoiding drawdown-only buying. Endpoint recovery hides a severe interim drawdown.

### 2026-07-30 — Risk / Oversold conflict
Historical posture: MANAGE LEVERAGE / WAIT RECOVERY.
KOSPI: +1d +17.91%, +5d +12.56%, +20d +21.37%.
Interpretation: this event is the clearest V-rebound warning. Any model that had materially reduced core exposure and restored slowly would suffer major opportunity cost. It supports Slow Exit / Fast Re-entry and immediate recovery restoration, not automatic bargain buying before confirmation.

### 2026-08-04 — Bullish Rebound + high volatility
Historical posture: CONFIRMATION BUY.
KOSPI: +1d +3.76%, +5d -0.21%, 5d MAE -1.58%, +20d +3.20%, 20d MFE +9.73%.
Interpretation: recovery confirmation produced a materially better entry path than the earlier 7/21 selective-buy state. This supports a separate Recovery Gate rather than symmetric sell/buy thresholds.

### 2026-09-08 — Leadership Bull -> Distribution confirmation
Historical posture: CORE HOLD / NO NEW LEVERAGE.
KOSPI: +1d +1.40%, +5d -4.71%, 5d MAE -4.71%.
Interpretation: balanced posture was consistent with the path: core participation captured the immediate strength while no-new-leverage limited exposure into the subsequent decline.

### 2026-09-10 — R2 maintained / R4 watch, C1-C8 PARTIAL
Historical posture: HOLD.
KOSPI: +1d -1.76%, +5d -4.40%, 5d MAE -5.78%, no positive close excursion during the five-session window.
Full Evidence note: C1/C2 were negative but C5 remained positive, C6 was unavailable, and R4-or-worse was not validated. The frozen Full Evidence Gate therefore did not establish reduction permission. Later weakness must not be used to retroactively overwrite the missing/conflicting evidence.
Interpretation: flow weakness contained useful warning information, but this one event is insufficient to lower the Evidence Gate or treat missing C6 as neutral.

### 2026-09-11 — R4 Distribution / R5 watch, C1-C8 FULL
Historical posture: RISK REDUCTION WATCH / technical conflict.
KOSPI: +1d -3.26%. Frozen +5d/+20d horizons remain PENDING as of this report.
Full Evidence note: multiple categories deteriorated, but positive C5 created material technical conflict for an automatic reduction. WATCH and EXECUTE remain distinct.

## 3. Cross-event findings

### Finding A — Regime alone must not liquidate core
Panic / oversold states can be followed by violent rebounds. 7/16 and especially 7/30 show why R6/R7 context cannot mechanically mean lower core exposure without evidence and execution hierarchy.

### Finding B — Recovery confirmation adds value to execution quality
7/21 versus 8/04 provides a useful contrast: early selective strength was followed by substantial downside, while the later confirmed rebound had a materially shallower adverse path. This is diagnostic support for asymmetric Recovery Gates.

### Finding C — Core and tactical exposure must remain operationally distinct
The historical decisions are better represented as:
1. leverage/high-beta tactical sleeve adjusted first,
2. core spot maintained unless strong multi-evidence deterioration persists,
3. recovery restores tactical exposure faster than core is reduced.
This is already consistent with the frozen Portfolio Reduction Priority and should be made explicit in future execution implementation rather than treated as a new timing threshold.

### Finding D — Full Evidence is more conservative than Historical Proxy by design
Historical Proxy estimates regime from P/I/V and therefore may reduce exposure when true C1-C8 conflict or missing data would block execution. Full Evidence must retain the rule that missing != neutral and material conflict -> HOLD.

## 4. Current validation status
- Historical events frozen: 9
- Exact/Partial C1-C8 runtime snapshots: 2
- 2026-09-10 +5d outcome: COMPLETE; +20d PENDING
- 2026-09-11 +5d/+20d outcomes: PENDING
- Full Evidence performance verdict: NOT YET ELIGIBLE
- Official 3.2 integration: BLOCKED pending additional runtime Full Evidence samples

## 5. Next design step allowed without threshold tuning
Formalize the execution semantics of an Overlay exposure target as a risk-budget hierarchy rather than pro-rata sale of every holding:
- Core sleeve
- Tactical/high-beta sleeve
- Leverage sleeve

This step may use the already-frozen Portfolio Reduction Priority but must not invent portfolio-specific weights in the market intelligence rules. Portfolio weights remain execution inputs, not market-state evidence.

No C1-C8 threshold change is authorized by this report.
