# AI Market Master 3.2 — Compounding Overlay v0.4
## Design Freeze 1

Status: EXPERIMENTAL / NOT OFFICIAL 3.2 AUTHORITY

Purpose: Address the two structural defects identified in v0.3 diagnostics without lowering the Historical Proxy 80% floor or retuning P/I/V and R1–R8 thresholds.

## 1. Evidence from v0.3 diagnostics

Top-drawdown attribution showed that first 80% exposure was inconsistent in timing: in several major declines a large portion of the final drawdown had already occurred before 80% exposure was reached.

Strong R5 diagnostic:
- 41 clustered Strong R5 episodes
- 14 had meaningful downside follow-through under the diagnostic definition
- follow-through ratio 34.1%

Thus an immediate extra defensive action on every isolated Strong R5 observation creates substantial false-positive cost.

80% floor ceiling diagnostic:
- Perfect hindsight 80% exposure from the market peak improved major-episode MDD by only about 15.4%–19.0%.
- To achieve 15% relative MDD improvement, constant exposure from the peak generally had to be approximately 80.5%–84.1%.

Therefore the original 15% MDD target is close to the theoretical ceiling of an 80%-floor model and requires near-perfect early defense. This does NOT retroactively change v0.1–v0.3 pass/fail results.

## 2. What remains unchanged

The following are frozen unchanged from the audited v0.3 implementation:
- P / I / V formulas
- audited R1–R8 proxy regime formulas and priority
- Strong R5 raw definition: Base R5 AND P<=-0.80 AND (I<=-0.50 OR V percentile>=85%)
- t-close signal -> t+1 execution
- transaction-cost sensitivity 2/5/10bp
- Historical Proxy does not fabricate C1/C2/C6/C7/C8 history
- R1 100%, R2 100%, R3 100%, R4 95%, normal R5 90%, R6 80%, R7 90%, R8 100%
- Historical Proxy minimum exposure = 80%
- R8 immediate restoration to 100%
- no leverage expansion above 100%

## 3. v0.4 change A — Strong-R5 persistence confirmation

Raw Strong R5 alone no longer authorizes the 80% target.

Confirmed Strong R5 requires:
- raw Strong R5 is true today, AND
- raw Strong R5 was true on at least 2 of the most recent 3 trading days including today.

This is a persistence filter, not a new price/indicator threshold.

Exposure target:
- unconfirmed Strong R5: same as normal R5 = 90%
- Confirmed Strong R5: 80%
- R6: 80%

All information is available at t close and executes no earlier than t+1.

## 4. v0.4 change B — Strong-risk reduction accelerator

The previous audited staged path always began 100->95 even when the final target was 80%.

v0.4 uses the already allowed maximum single reduction of 10 percentage points when risk is Confirmed Strong R5 or R6:
- 100 -> 90
- then, subject to the existing cooldown, 90 -> 80

For ordinary R4/R5 deterioration, the prior gradual path remains:
- 100 -> 95 -> 90

No single reduction may exceed 10 percentage points.

## 5. Cooldown

The existing cooldown remains unchanged:
- after a reduction, at least one full trading day must pass before another same-direction reduction
- implementation therefore does not perform 100->90->80 on consecutive execution sessions when the frozen cooldown forbids it

R8 recovery may still restore immediately to 100% as already frozen.

## 6. Intended effect

v0.4 is designed to combine:
- lower false-positive cost than v0.3, because isolated Strong R5 does not trigger 80%
- faster response to persistent severe risk than v0.3, because confirmed strong risk may use a full -10%p first reduction step
- preservation of v0.2-like market participation in ordinary conditions

## 7. Validation boundaries

Original frozen criteria are still reported for comparability:
- PASS A: CAGR no worse than Hold by more than 0.3%p annually
- PASS B: relative MDD improvement >=15%
- Hard Fail: CAGR lag >=1.0%p or average exposure <=85%

Because the defense-ceiling study shows the 15% target is near the theoretical maximum of an 80%-floor model, v0.4 will also report diagnostic efficiency, but PASS B itself is not rewritten after the fact.

Comparative diagnostics:
- v0.4 vs audited v0.2
- v0.4 vs v0.3
- average exposure
- trade count / turnover
- rolling 5y/10y Hold-beat ratios
- major drawdown behavior

## 8. Anti-overfitting rule

The 2-of-3 persistence rule and strong-risk -10%p accelerator are frozen before v0.4 result generation.
No threshold or confirmation count may be changed after results without creating v0.5 or later.
