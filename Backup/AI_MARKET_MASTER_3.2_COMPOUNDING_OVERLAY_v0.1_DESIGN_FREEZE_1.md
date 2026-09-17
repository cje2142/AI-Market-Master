# AI Market Master 3.2 — Compounding Overlay v0.1
## Design Freeze 1

Status: EXPERIMENTAL / NOT OFFICIAL 3.2 AUTHORITY
Purpose: Preserve Buy & Hold compounding while allowing evidence-gated, limited exposure adjustment.

## 1. Core Philosophy
- Baseline exposure = 100%.
- Preserve market participation and long-term compounding as the default.
- Do not turn 3.2 into a broad timing engine.
- Regime alone never triggers a trade.
- Strong action requires multiple independent evidence groups.
- Slow Exit / Fast Re-entry is mandatory.
- Core spot is preserved as long as possible; leverage/high-beta exposure is adjusted before core spot.
- No single RSI, MA, volatility, global, or flow signal can trigger a strong portfolio action.

## 2. Exposure Map
| Regime | Base Exposure | Allowed Range | Principle |
|---|---:|---:|---|
| R1 Broad Risk-On | 100% | 95–100% | Hold priority; no overheat-only selling |
| R2 Leadership Bull | 100% | 95–100% | Preserve bull-market participation |
| R3 Rotation | 95% | 90–100% | Mild caution; hold priority |
| R4 Distribution | 90% | 80–95% | Reduce only with evidence confirmation |
| R5 Risk-Off Transition | 80% | 70–90% | Reduce leverage/high-beta first |
| R6 Panic | 70% | 60–80% | No full cash exit |
| R7 Deep Correction / Support | 75% | 65–85% | No buying solely because price is down |
| R8 Recovery / Accumulation | 85→100% | 80–100% | Fast staged restoration after recovery evidence |

Constraints:
- Minimum absolute exposure = 60%.
- Normal Risk-Off floor = 70%.
- Maximum single adjustment = 10 percentage points.
- Overlay v0.1 contains no leverage-expansion function.

## 3. Evidence Classes
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

Correlated observations must not automatically be counted as independent evidence.

## 4. Reduction Gates
### -5%p reduction
Requires all:
- R4 or worse
- At least 1 deteriorating A-class category
- At least 3 independent deteriorating evidence categories total
- C5 technical location does not materially conflict with reduction

### Additional -5%p reduction
Requires all:
- R4/R5 persistence
- At least 2 deteriorating A-class categories
- At least 4 deteriorating categories total
- Confirmation from at least 2 of A/B/C evidence classes

### -10%p strong reduction
Requires all:
- R5 or R6
- Strong deterioration in at least one of C1/C2
- C5 confirms trend/structure breakdown
- At least 5 deteriorating categories total
- At least one of C6 liquidity deterioration or C7 volatility expansion

## 5. Restoration Gates
Restoration is intentionally faster than reduction.

### +10%p restoration
Requires all:
- R8 entry or R7→R8 transition
- Improvement in C1 or C2
- C3 breadth improvement
- C5 price-structure recovery
- At least 3 improving categories total

### Additional +10%p restoration
Requires all:
- R8 persists
- At least 2 improving A-class categories
- At least 4 improving categories total
- C7 stabilization or C8 improvement

### Return to 100%
Requires all:
- R1/R2 or strong R8
- At least 2 positive categories among C1/C2/C5
- At least 4 positive categories total
- No unresolved major conflict

## 6. False-Signal Controls — Design Freeze 1
- Regime is direction/context, not execution permission.
- Evidence Gate grants action permission.
- Exposure Map limits action size.
- Intraday single-point spikes do not qualify by themselves.
- Require either intraday persistence across multiple checkpoints or end-of-session confirmation for strong adjustments.
- Same-source/correlated evidence must be de-duplicated before counting independent groups.

## 7. Portfolio Reduction Priority
1. Profit leverage
2. Relative-weakness leverage / high-beta exposure
3. Loss leverage where risk remains elevated
4. Other risk assets
5. Core spot last

## 8. Explicitly Excluded from v0.1
- Full market exit
- Automatic MA-only exit
- RSI-only overheat selling
- Mechanical drawdown-only buying
- Leverage expansion above 100%
- Sector rotation alpha
- OFI/BSI futures alpha engine

This file freezes the design before Cost Gate, Cooldown, Hysteresis, simulation tuning, and any official 3.2 integration.
