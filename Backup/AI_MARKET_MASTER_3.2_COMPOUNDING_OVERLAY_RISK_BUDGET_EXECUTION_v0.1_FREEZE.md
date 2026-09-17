# AI Market Master 3.2 — Compounding Overlay Risk Budget Execution v0.1
## Design Freeze

Date: 2026-09-17
Status: EXPERIMENTAL EXECUTION LAYER / NOT OFFICIAL 3.2 AUTHORITY

## 1. Purpose
Translate a validated Compounding Overlay exposure target into portfolio actions without changing C1-C8, Regime, Strategy Action Index, or market-state logic.

This layer is portfolio execution only.

Market Intelligence and Portfolio Execution remain separated:
`3.2 Market State -> Full Evidence Gate -> Overlay Target Risk Budget -> Portfolio Execution Mapper`

The portfolio may change without changing any market rule.

## 2. Core principle
An Overlay target such as 95, 90, or 80 is a **normalized portfolio risk-budget target**, not an instruction to sell every holding pro-rata and not automatically a cash-weight target.

`100 = the portfolio's fully-authorized strategic risk baseline`

Therefore:
- 95 means retain 95% of the baseline authorized risk budget,
- 90 means retain 90%,
- 80 means retain 80%,
- the execution mapper decides where the reduction comes from,
- the market engine does not know or care which individual holdings are currently owned.

## 3. Three execution sleeves
### Core Sleeve
Long-horizon strategic positions whose primary role is compounding and persistent market participation.

Core is protected longest and reduced last.

### Tactical Sleeve
Non-core positions used for sector, theme, high-beta, rotation, or shorter-horizon opportunity exposure.

Instrument type does not alone determine classification. A security is classified by its portfolio role.

### Leverage Sleeve
Leveraged ETFs, leveraged single-name products, futures or other explicitly leveraged risk exposure.

Leverage is reduced first.

## 4. Frozen reduction hierarchy
When the Full Evidence Gate authorizes a reduction, consume the required risk-budget reduction in this order:

1. profitable leverage exposure
2. relative-weakness / high-beta leverage exposure
3. other leverage exposure, including losing leverage when risk remains elevated
4. tactical high-beta / weak-relative-strength exposure
5. other tactical exposure
6. Core spot only for any residual reduction that cannot be satisfied above

This preserves the already-frozen Portfolio Reduction Priority.

No regime by itself may bypass the Full Evidence Gate and force Core liquidation.

## 5. Core Preservation Gate
Core reduction is permitted only when BOTH are true:

A. the validated Overlay target is below the risk budget that can be reached by removing eligible Leverage + Tactical exposure, AND
B. the applicable Full Evidence Reduction Gate already grants the reduction.

If non-core exposure is insufficient but the Full Evidence Gate does not authorize deeper Core reduction:
- do not fabricate authority,
- stop at the achievable risk level,
- return `PARTIAL EXECUTION / CORE PROTECTED`.

Panic or oversold context alone never authorizes chase-selling Core.

## 6. Restoration hierarchy
Recovery remains asymmetric: restoration is allowed to be faster than reduction.

When the Overlay target rises:
1. restore any previously reduced Core toward its strategic baseline first,
2. restore Tactical exposure toward its authorized baseline,
3. restore Leverage last and only under the separate existing portfolio/leverage authorization.

The Overlay does not create new leverage merely because target risk returns to 100.
It may only restore leverage that is separately authorized by the portfolio execution framework.

## 7. Risk-unit calculation boundary
When reliable risk multipliers are available, normalized portfolio risk exposure may be calculated as:

`Risk Exposure = SUM(capital weight_i × validated risk multiplier_i)`

Examples of acceptable structural multipliers:
- unleveraged broad-market spot: structural multiplier 1.0 may be used,
- explicit 2x leveraged product: structural leverage factor 2.0 may be used for leverage translation.

For individual stocks, sectors, themes, covered-call products, or other instruments:
- do not invent beta or volatility multipliers,
- use a validated multiplier only if an approved portfolio-risk source provides it,
- otherwise perform nominal sleeve mapping and mark numeric risk translation `PARTIAL`.

Missing risk coefficient != 1.0 by default unless the instrument structurally represents 1x broad-market exposure.

## 8. Target translation
Let:
- `B = baseline authorized risk budget = 100`
- `C = current normalized risk budget`
- `T = validated Overlay target`

Required reduction:
`max(0, C - T)`

Required restoration:
`max(0, T - C)`

Execution always follows sleeve hierarchy rather than pro-rata sale.

## 9. Frozen examples
### Example A — mild reduction
Strategic baseline:
- Core 80 risk units
- Tactical 10
- Leverage 10
- Total 100

Overlay target 95:
- reduce 5 from Leverage
- Core remains 80
- Tactical remains 10
- Leverage becomes 5

### Example B — target 90
Same baseline, target 90:
- remove 10 Leverage
- Core remains 80
- Tactical remains 10
- Leverage becomes 0

### Example C — target 80
Same baseline, target 80:
- remove 10 Leverage
- remove 10 Tactical
- Core remains 80

This is the preferred defensive outcome because the entire required reduction is achieved without selling Core.

### Example D — non-core exposure insufficient
Baseline:
- Core 90
- Tactical 5
- Leverage 5
- Total 100

Overlay target 80 requires 20 risk units of reduction.
Leverage + Tactical provide only 10.

After removing them, a further 10 Core reduction is required to reach 80.
- if the Full Evidence Gate authorizes that depth: Core may reduce 90 -> 80,
- if not: stop at 90 total and return `PARTIAL EXECUTION / CORE PROTECTED`.

### Example E — recovery
Assume Example D actually reached Core 80 / Tactical 0 / Leverage 0.
When target returns to 100:
- restore Core toward strategic baseline 90 first,
- restore Tactical toward baseline 5,
- restore Leverage up to baseline 5 only if separate leverage authorization is valid.

## 10. Execution statuses
Every mapped action must end in one of these statuses:

- `EXECUTABLE` — target can be achieved under existing authority.
- `PARTIAL EXECUTION / CORE PROTECTED` — target cannot be fully achieved without unauthorized Core sale.
- `LEVERAGE RESTORE BLOCKED` — risk target recovered but leverage-specific authorization is absent.
- `HOLD / CONFLICT` — Full Evidence conflict rule blocks action.
- `DATA PARTIAL` — portfolio risk coefficients are insufficient for exact risk-unit translation.

No silent fallback is allowed.

## 11. Anti-double-counting / anti-drift
- Market evidence must never be altered because the current portfolio has more or less leverage.
- Portfolio composition affects execution size/order only.
- The same exposure target must map differently across portfolios if sleeve composition differs.
- Sleeve classification must not create a new C1-C8 signal.
- Current holdings or current user weights must not be hardcoded into 3.2 rules.
- Portfolio weights may be updated at runtime without versioning the market engine.

## 12. Validation requirements before official integration
The mapper must pass deterministic tests for:
1. 100 -> 95 with sufficient leverage: Core unchanged.
2. 100 -> 90 with sufficient non-core: Core unchanged.
3. 100 -> 80 with sufficient Leverage+Tactical: Core unchanged.
4. target below achievable non-core floor: explicit Core Preservation Gate behavior.
5. 80 -> 100 recovery: Core restored before Tactical; Leverage restored last.
6. missing risk multipliers: DATA PARTIAL, never fabricated.
7. portfolio composition changes: same market target, different execution mapping, market rules unchanged.
8. R6/Panic without Full Evidence execution permission: no automatic Core chase-sell.

## 13. Version lock
This file freezes Risk Budget Execution v0.1 before implementation testing.

Any change to sleeve order, Core Preservation Gate, restoration order, or risk-unit semantics requires v0.2 or later.

No C1-C8 threshold, Regime formula, Historical Proxy threshold, or official 3.2 Authority file is changed by this design.
