# AI Market Master 3.2 — Compounding Overlay v0.2
## Design Freeze 1

Status: EXPERIMENTAL / NOT OFFICIAL 3.2 AUTHORITY

Purpose: Correct the v0.1 weakness identified in the first Historical Proxy backtest without changing the frozen P/I/V formulas or Regime classification thresholds.

## 1. v0.1 Evidence
Primary 20-year test at 5bp/side:
- Hold CAGR: 6.31%
- v0.1 CAGR: 6.02% (-0.29%p)
- Hold MDD: -52.92%
- v0.1 MDD: -47.51% (10.22% relative improvement)
- Average exposure: 92.54%
- Trades: 628

Interpretation:
- compounding preservation nearly passed the predefined threshold
- risk improvement was real but below the 15% target
- turnover and underexposure were too high relative to defensive benefit

## 2. Exactly Three v0.2 Changes
Only these three structural changes are authorized before the v0.2 result is seen.

### Change A — Weaken R3/R4 defense
Historical Proxy target exposure:
- R1 = 100%
- R2 = 100%
- R3 = 100%  (v0.1: 95%)
- R4 = 95%   (v0.1: 90%)

Purpose: prevent routine Rotation/weak Distribution states from creating persistent compounding drag.

### Change B — Concentrate defense in R5/R6
Historical Proxy target exposure:
- R5 = 90%   (v0.1 effectively allowed 80%)
- R6 = 80%
- R7 = 90%

Purpose: reserve material defense for genuine Risk-Off/Panic states instead of using cash broadly across ambiguous regimes.

### Change C — Immediate R8 recovery
- Any confirmed R8 Historical Proxy signal restores exposure directly to 100% on the next executable session.
- Allowed examples: 80→100, 90→100, 95→100.

Purpose: reduce V-rebound underparticipation.

## 3. Unchanged Rules
The following remain identical to v0.1:
- P/I/V formulas
- R1–R8 Historical Proxy definitions and priority order
- t-close signal → t+1 execution
- transaction-cost assumptions: 2bp / 5bp / 10bp per side
- Historical Proxy floor: 80%
- no leverage above 100%
- cash return = 0% in primary validation
- initial capital and benchmark framework
- no fabricated C1/C2/C6/C7/C8 data

## 4. v0.2 Exposure Targets
| Regime | v0.2 Historical Proxy target |
|---|---:|
| R1 | 100% |
| R2 | 100% |
| R3 | 100% |
| R4 | 95% |
| R5 | 90% |
| R6 | 80% |
| R7 | 90% |
| R8 | 100% immediately |
| Unknown | HOLD current exposure |

## 5. Transition Rules
Reduction:
- maximum single reduction remains 10%p
- same-direction reduction retains the v0.1 cooldown
- R6 may progress 100→95→90→80 across confirmed sessions; no direct 100→80 jump

Restoration:
- R8 overrides the normal staged-restoration rule and restores directly to 100%
- R1/R2/R3 may restore toward 100% using the normal upward path

## 6. Predefined Targets
Target behavior, not guaranteed results:
- average exposure: 95–98%
- trades: preferably <=300 over the 20-year test
- CAGR: no worse than Hold by more than 0.3%p
- MDD relative improvement: >=15%

The original v0.1 pass/fail framework remains the comparison framework. Results must not be used to silently alter v0.2 parameters.

## 7. Version Lock
This file freezes v0.2 before its first result-producing backtest. Any later parameter modification must create v0.3 or a separately named experimental branch, not overwrite v0.2.
