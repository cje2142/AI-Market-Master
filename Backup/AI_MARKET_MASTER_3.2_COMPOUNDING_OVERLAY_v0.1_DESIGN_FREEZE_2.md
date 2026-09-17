# AI Market Master 3.2 — Compounding Overlay v0.1
## Design Freeze 2

Status: EXPERIMENTAL / NOT OFFICIAL 3.2 AUTHORITY

Purpose: Freeze executable transition logic plus validation specification before any result-producing simulation.

## 1. Core Execution Chain
3.2 Regime → Evidence Gate → Exposure Map → Cost Gate → Minimum Action Threshold → Cooldown/Hysteresis → Position Transition → Execution

## 2. Allowed Exposure States
100 / 95 / 90 / 80 / 70 / 60.

No ad-hoc intermediate exposure targets are allowed in v0.1.

## 3. Position Transition Logic
Downward path:
- 100→95: R4 or worse + Reduction Gate 1 + Cost Gate
- 95→90: deterioration persists + Reduction Gate 2 + cooldown
- 90→80: R5/R6 + Strong Reduction Gate
- 80→70: R5/R6 persists + C1/C2/C5-centered deterioration + C6 or C7 confirmation
- 70→60: R6 Panic + >=5 independent deteriorating categories + strong C1 or C2 deterioration + C5 structural breakdown
- Maximum single reduction = 10 percentage points
- No direct 100→70 jump

Upward path:
- 60→70/80: R7→R8 + C1/C2 improvement + C3 improvement + C5 recovery
- 70→80/90: R8 confirmed + >=2 A-class improvements + >=4 total improvements
- 80→90: R8 persists + C7 stabilization or C8 improvement
- 90→100: R1/R2 or strong R8 + >=2 positives among C1/C2/C5 + >=4 total positives + no major conflict
- 95→100: standard restoration gate
- Strong recovery may restore up to +20 percentage points in one action

## 4. Cost Gate
Default non-emergency rule:
Expected Edge must exceed estimated total transaction cost by at least 2x.

Estimated total cost includes where applicable:
- commission
- spread
- slippage
- taxes / ETF execution costs

Confirmed R6 structural-risk control may relax this gate, but the reason must be logged.

## 5. Minimum Action Threshold
- Ignore target changes smaller than 5 percentage points.
- No micro-adjustments such as 95→92 or 90→88.

## 6. Cooldown / Hysteresis
Reduction:
- after a reduction, wait at least 1 trading day before another same-direction reduction
- exception only for materially worsening Regime/evidence, e.g. R5→R6 with new independent confirmation

Restoration:
- strong R8 Recovery may override normal cooldown

Hysteresis:
- reduction and restoration use different gates
- deterioration becoming neutral is not sufficient for restoration
- a separate Recovery Gate is mandatory

## 7. Conflict Rule
Material unresolved conflict → HOLD current exposure.

## 8. V-Rebound Priority
If a sharp selloff is followed by R7→R8 and simultaneous improvement in C1/C2/C3/C5:
- Recovery Gate may override normal cooldown
- fast restoration up to +20 percentage points is allowed

## 9. Portfolio Reduction Priority
1. Profit leverage
2. Relative-weakness / high-beta leverage
3. Loss leverage if risk remains elevated
4. Other risk assets
5. Core spot last

## 10. Simulation Specification Freeze
Benchmark set:
- Buy & Hold
- original 3.2 proxy behavior
- Compounding Overlay v0.1

Initial capital: KRW 100,000,000
Additional contribution: none
Leverage: none in Overlay validation
Cash return in primary test: 0%
Transaction cost sensitivity: 2bp / 5bp / 10bp per side
Primary default transaction cost: 5bp per side

Evaluation horizons:
- 20-year long horizon where valid data exists
- recent 10-year horizon
- rolling 5-year and 10-year windows

Primary metrics:
1. CAGR
2. terminal wealth
3. MDD
4. average market exposure
5. trade count
6. transaction-cost drag
7. Hold-beating window ratio

Secondary metrics:
- Sharpe
- Sortino
- recovery time

## 11. Predefined Pass / Fail Criteria
PASS A — Compounding Preservation:
Overlay CAGR must be no worse than Hold by more than 0.3 percentage points annually.

PASS B — Risk Improvement:
Overlay MDD must improve by at least 15% relative to Hold.

Strong PASS:
- CAGR >= Hold
- MDD < Hold

Very Strong PASS:
- CAGR >= Hold +0.5%p
- MDD improves by >=15% relative

FAIL if any major condition occurs:
- CAGR trails Hold by >=1.0%p
- average exposure <=85%
- MDD improvement is negligible
- turnover/cost destroys the edge
- repeated V-recovery re-entry failure
- performance is concentrated in only one isolated 5-year regime

## 12. Mandatory Stress Tests
- strong bull market
- gradual bear market
- crash
- V-shaped rebound
- high-volatility sideways market
- false breakdown followed by recovery

## 13. Historical Proxy Mapping Boundary
Full Evidence Test:
- use actual C1-C8 / actual historical 3.2 Dashboard evidence where available

Long-History Proxy Test:
- never fabricate missing C1/C2/C6/C7/C8 history
- use explicitly labeled Historical Regime Proxy only

Proxy axes:
P = Price / Structure
- close vs MA20/60/200
- MA alignment
- 20/60-day returns
- drawdown from high
- RSI/MACD
- daily price structure

I = Internal / Participation
- KOSPI vs KOSDAQ relative behavior
- KOSPI200 / large-cap relative strength where available
- breadth when valid breadth history exists

V = Volatility / Risk
- 20-day realized volatility
- daily shock magnitude
- drawdown
- actual VKOSPI where available

No absent foreign/program/macro variable may be silently replaced with price data.

## 14. Historical Proxy Regime Mapping
R1 Broad Risk-On Proxy:
- strong P
- broad/improving I
- stable V

R2 Concentrated Leadership Bull Proxy:
- strong P
- leadership concentrated
- weaker I than index
- stable V

R3 Rotation Proxy:
- neutral/moderately positive P
- relative-strength crossover / leadership handoff
- no broad participation collapse

R4 Distribution Proxy:
- price still high/firm
- I deteriorates
- momentum/structure weakens
- V begins rising

R5 Risk-Off Transition Proxy:
- P turns weak
- support/trend structure deteriorates
- I weakens
- V rises
- at least two independent proxy axes must confirm

R6 Panic Proxy:
- sharp decline
- high realized volatility
- large drawdown
- broad weakness

R7 Deep Correction / Support Proxy:
- large drawdown already occurred
- selling speed slows
- volatility peaks/stabilizes
- recovery not yet confirmed

R8 Recovery Proxy:
- price stabilizes/reclaims short structure
- internals improve
- volatility stabilizes

## 15. Proxy Safety Constraint
Historical Proxy alone may reduce exposure only to 80%.

Reason:
Without actual Smart Money / Program / Liquidity confirmation, price-derived proxy data must not authorize 70% or 60% exposure states.

Thus:
- Full Evidence mode: 100→95→90→80→70→60 permitted subject to rules
- Historical Proxy mode: 100→95→90→80 only

## 16. Anti-Lookahead Rule
- t-day data may only generate a trade from t+1 onward
- no same-close execution using indicators that require that same close to be known
- rolling MA/RSI/volatility use only information available up to time t

## 17. Validation Layers
Three independent validation layers are required:
1. 20-year Historical Proxy test — compounding preservation
2. actual 3.2 Dashboard backdata — Evidence Gate quality
3. synthetic structural stress test — crash/V-recovery/sideways robustness

Official 3.2 integration is prohibited unless the overlay passes the validation framework.

## 18. Explicit Exclusions
- leverage expansion above 100%
- full market exit
- sector-rotation alpha
- security-selection alpha
- OFI/BSI futures alpha engine
- MA-only exit
- RSI-only overheat selling
- mechanical drawdown-only buying

This file freezes the experimental design. Any parameter change after seeing results requires a new version, not silent modification of v0.1.
