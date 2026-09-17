# AI Market Master 3.2 — Compounding Overlay v0.1
## Simulation Formula Freeze

Status: EXPERIMENTAL / NOT OFFICIAL 3.2 AUTHORITY
Purpose: Freeze the Historical Proxy calculation formulas before any result-producing long-horizon simulation.

## 1. General Boundary
Long-history validation uses only observable historical proxy variables. Missing C1/C2/C6/C7/C8 history must never be fabricated or silently replaced by price-derived data.

Historical Proxy uses three axes only:
- P = Price / Structure
- I = Internal / Participation
- V = Volatility / Risk

All t-day signals are calculated using information available through t close only and may be executed from t+1 onward.

## 2. P — Price / Structure Axis
Inputs:
- R20 = Close / Close[-20] - 1
- R60 = Close / Close[-60] - 1
- DD252 = Close / rolling_252d_high - 1
- MA20 / MA60 / MA200

Five components are scored +1 / 0 / -1:
1. Close vs MA20
2. Close vs MA60
3. Close vs MA200
4. R20
5. R60

MA neutral band:
- Close > MA × 1.005 => +1
- Close < MA × 0.995 => -1
- otherwise 0

Return thresholds:
- R20 > +3% => +1
- R20 < -3% => -1
- otherwise 0
- R60 > +6% => +1
- R60 < -6% => -1
- otherwise 0

P = average(valid five components)
Range: [-1,+1]

Classification:
- P >= +0.40 => Bullish
- -0.40 < P < +0.40 => Neutral
- P <= -0.40 => Bearish

## 3. I — Internal / Participation Axis
Primary proxy inputs where available:
- KOSDAQ_20d_return - KOSPI_20d_return
- KOSPI200_20d_return - KOSPI_20d_return

Normalization:
- KOSDAQ relative return / 5%, clipped to [-1,+1]
- KOSPI200 relative return / 2.5%, clipped to [-1,+1]

If both are valid:
I = 0.60 × normalized_KOSDAQ_relative + 0.40 × normalized_KOSPI200_relative

If only one is valid:
- use the valid axis
- mark Internal proxy as PARTIAL

Classification:
- I >= +0.20 => Broad / Improving
- I <= -0.20 => Weak / Narrow
- otherwise => Mixed

If valid historical breadth data exists, actual breadth takes precedence over relative-strength proxy for participation interpretation.

## 4. V — Volatility / Risk Axis
RV20 = std(daily returns, 20) × sqrt(252)

RV20 percentile is calculated against the trailing 252 trading days only.

Classification:
- percentile < 60 => Stable
- 60–80 => Elevated
- >=80 => High
- >=90 => Extreme

Shock flags:
- 1-day return <= -4%
- OR 5-day cumulative return <= -8%

Drawdown DD252 is used as additional structural risk context.

## 5. Proxy Regime Priority Order
If multiple proxy regimes are simultaneously satisfied, evaluate in this order:
1. R6 Panic
2. R8 Recovery
3. R7 Deep Correction / Support
4. R5 Risk-Off Transition
5. R4 Distribution
6. R2 Concentrated Leadership Bull
7. R1 Broad Risk-On
8. R3 Rotation
9. otherwise Regime Unknown => HOLD current exposure

## 6. R6 Panic Proxy
Require:
- V percentile >=80
AND at least 2 of:
- 1-day return <= -4%
- 5-day cumulative return <= -8%
- DD252 <= -15%

Historical Proxy exposure floor remains 80%; R6 proxy alone cannot authorize 70/60 exposure states.

## 7. R8 Recovery Proxy
Require all:
- an R5/R6/R7 proxy state occurred within the prior 20 trading days
- Close > MA20
- R20 > 0
- I improved by at least +0.15 versus 10 trading days earlier OR current I > 0
- current RV20 percentile is at least 10 percentage points below the highest RV20 percentile observed during the prior 10 trading days

A simple price bounce is not sufficient.

## 8. R7 Deep Correction / Support Proxy
Require all:
- DD252 <= -15%
- current 5-day return is not <= -3%
- Close is at least +2% above the lowest close of the prior 10 trading days
- RV20 is below its highest value of the prior 5 trading days
- R8 conditions are not yet satisfied

No automatic bottom-buying is allowed.

## 9. R5 Risk-Off Transition Proxy
Require:
- P <= -0.40
AND one of:
- I <= -0.20
- V percentile >=70

At least two independent proxy axes must confirm deterioration.

## 10. R4 Distribution Proxy
Require all:
- P > 0 OR DD252 > -7%
- I <= -0.20
- Close < MA20 OR 5-day return < 0
- current RV20 percentile is above the median RV20 percentile of the prior 20 trading days

Interpretation: price remains relatively firm while internals weaken and risk begins rising.

## 11. R2 Concentrated Leadership Bull Proxy
Require all:
- P >= +0.40
- KOSPI200 relative 20-day strength > 0
- I < +0.20
- V percentile <80

## 12. R1 Broad Risk-On Proxy
Require all:
- P >= +0.40
- I >= +0.20
- V percentile <70

## 13. R3 Rotation Proxy
Require all:
- -0.40 < P < +0.40
- V percentile <80
- KOSDAQ-vs-KOSPI or large-cap-vs-market relative-strength direction crossed within the prior 10 trading days

Otherwise:
- Regime Unknown
- current exposure remains unchanged

## 14. Historical Proxy Exposure Constraint
Historical Proxy mode may use only:
100 → 95 → 90 → 80

It may not use 70 or 60 because Smart Money / Program / Liquidity confirmation is unavailable.

Full Evidence mode may use:
100 → 95 → 90 → 80 → 70 → 60
subject to the full Compounding Overlay rules.

## 15. Anti-Lookahead Rule
- t-day close and indicators derived from it may only produce execution from t+1 onward
- no same-close trade using that close as an input
- rolling averages, RSI, MACD, realized volatility, drawdown, relative strength and all percentiles use only information available through t

## 16. Historical Proxy Cost Handling
The live Full Evidence Cost Gate remains:
Expected Edge > estimated total transaction cost × 2

However, Historical Proxy backtesting does not invent an Expected Edge model.
Instead it uses:
- actual simulated transaction-cost deduction
- minimum 5 percentage-point action threshold
- cooldown / hysteresis rules

Default transaction cost sensitivity remains:
- 2bp per side
- 5bp per side primary case
- 10bp per side

## 17. Version Lock
These formulas are frozen before seeing simulation results.
Any threshold or formula modification after results are observed must create a new experimental version (v0.2 or later) and must not silently overwrite v0.1.

Next stage:
Run the first Historical Proxy simulation against Buy & Hold using these frozen formulas and the previously frozen pass/fail criteria.
