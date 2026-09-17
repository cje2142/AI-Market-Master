# AI Market Master 3.2 — Compounding Overlay
## Historical Proxy Implementation Audit — 2026-09-17

Status: EXPERIMENTAL / IMPLEMENTATION AUDIT
Official 3.2 authority files are unchanged.
Frozen strategy thresholds are unchanged.

## Purpose
Before running v0.3, re-check whether the existing Python backtest exactly implements the already-frozen Historical Proxy rules.

## Finding 1 — R8 Recovery OR-condition implementation mismatch
Frozen rule:
- I improved by at least +0.15 versus 10 trading days earlier OR current I > 0.

Existing v0.1 Python expression placed the conditional expression and OR without explicit grouping. Under Python precedence, when the 10-day comparison is available the expression can evaluate only the improvement branch and fail to apply the intended `OR current I > 0` branch.

Correct implementation must be:
`(I_improved_10d >= 0.15) OR (current_I > 0)`
with the first branch treated False when the 10-day comparison is unavailable.

This is an implementation correction, not a rule change.

## Finding 2 — v0.2 staged reduction can violate the frozen max -10%p rule
Frozen rule:
- maximum single reduction = 10 percentage points
- allowed exposure states = 100 / 95 / 90 / 80 in Historical Proxy mode
- 100 toward 80 must be staged; no direct jump that exceeds -10%p.

The v0.2 Python implementation calculated `current - 0.10` and then snapped to the nearest allowed state. At current exposure 95%, an 80% target can produce an intermediate 85% and nearest-state snapping can choose 80%, creating a 95% -> 80% move (-15%p), which violates the frozen rule.

Correct staged reduction is deterministic:
- 100 -> 95
- 95 -> 90
- 90 -> 80
subject to the existing cooldown.

This is an implementation correction, not a rule change.

## Validation consequence
Previously generated v0.1/v0.2 result files remain preserved as audit history, but they must not be treated as final frozen-rule validation until the corrected implementation is rerun.

## Corrected test sequence
1. Re-run v0.2 with only the two implementation corrections above.
2. Run v0.3 on the same corrected engine.
3. Use identical KRX-derived data, t-close -> t+1-open execution, 2/5/10bp cost sensitivity, 20-year / recent-10-year / rolling / stress windows.
4. Compare Hold vs corrected-v0.2 vs v0.3.
5. Do not change any threshold after observing results.

## v0.3 frozen Strong R5 rule
Base Regime must be R5 AND:
- P <= -0.80
AND
- I <= -0.50 OR V percentile >= 85%

Historical Proxy floor remains 80%.
