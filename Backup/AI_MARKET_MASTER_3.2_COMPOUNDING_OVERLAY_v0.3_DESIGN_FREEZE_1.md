# AI Market Master 3.2 — Compounding Overlay v0.3
## Design Freeze 1

Status: EXPERIMENTAL / NOT OFFICIAL 3.2 AUTHORITY

Purpose: Preserve v0.2's high market participation while improving drawdown defense by moving to 80% exposure earlier only when R5 deterioration is objectively severe. Official 3.2 authority files and v0.1/v0.2 remain unchanged.

## 1. Re-validated v0.2 Problem
Primary 20-year 5bp result:
- Hold CAGR 6.31%
- v0.2 CAGR 6.19% (gap -0.12%p)
- Hold MDD -52.92%
- v0.2 MDD -49.41% (relative improvement 6.63%)
- Avg exposure 96.45%
- Trades 451

Interpretation:
- Compounding preservation materially improved versus v0.1.
- Risk reduction weakened and remains far below the pre-frozen 15% relative MDD target.
- The problem is no longer broad underexposure. The remaining weakness is insufficient/late defensive intensity before major drawdowns.
- Transaction costs are secondary: performance gap changes only modestly between 2bp and 10bp.

## 2. What MUST NOT Change in v0.3
The following remain exactly as frozen in v0.1/v0.2 historical proxy logic:
- P / I / V formulas
- R1–R8 proxy regime formulas and priority
- t-close signal -> t+1 execution
- transaction-cost sensitivity 2/5/10bp
- Historical Proxy uses no fabricated C1/C2/C6/C7/C8 data
- Historical Proxy minimum exposure remains 80%
- R8 immediate restoration to 100% remains

## 3. Exposure Map
- R1: 100%
- R2: 100%
- R3: 100%
- R4: 95%
- Normal R5: 90%
- Strong R5: 80%
- R6: 80%
- R7: 90%
- R8: 100%
- Unknown: HOLD current exposure

Thus v0.3 changes only the timing of reaching the existing 80% floor; it does NOT lower the Historical Proxy floor below 80%.

## 4. Strong R5 Definition
A day is Strong R5 only when the base proxy Regime is R5 AND:

1. Price/Structure severity is strong:
   - P <= -0.80

AND

2. At least one independent confirmation is severe:
   - I <= -0.50
   OR
   - V percentile >= 85%

This requires severe Price/Structure deterioration plus either severe Internal weakness or severe Volatility/Risk confirmation.

No single MA, RSI, drawdown, or one-day price move can create Strong R5 by itself.

## 5. Execution Rule
- Normal R5 target = 90%.
- Strong R5 target = 80%.
- Existing max single reduction of 10 percentage points and cooldown remain active.
- Therefore a move from 100% toward 80% still occurs through staged execution, not a direct 20% cut.
- R6 target remains 80%.

## 6. Restoration
- R8 -> immediate 100% restoration remains unchanged from v0.2.
- R1/R2/R3 -> normal fast restoration toward 100%.
- Loss of Strong R5 status alone does not force immediate restoration; ordinary v0.2 target logic applies.

## 7. Validation Objective
Primary question:
Can earlier 80% defense in objectively severe R5 periods improve MDD without materially damaging v0.2's compounding preservation?

Pre-existing pass criteria remain unchanged:
- PASS A: Overlay CAGR no worse than Hold by more than 0.3%p annually.
- PASS B: MDD improves by at least 15% relative to Hold.
- Hard fail if CAGR trails Hold by >=1.0%p or average exposure <=85%.

Additional monitoring targets (diagnostic, not pass criteria):
- Avg exposure preferably >=95%
- Fewer than v0.1's 628 trades
- No material V-rebound re-entry delay

## 8. Version Lock
The Strong R5 thresholds P<=-0.80 and (I<=-0.50 OR V percentile>=85%) are frozen before v0.3 result generation.
Any threshold adjustment after results requires v0.4 or later.
