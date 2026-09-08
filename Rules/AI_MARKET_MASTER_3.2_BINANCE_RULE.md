# AI Market Master 3.2 Binance Rule

Version: 3.2 Unified Stable
Status: Binance Global Leading Authority

## 1. Purpose
Binance public read-only futures data is a global leading/supporting layer connected to the existing 24-engine architecture. It does not replace HTS/KRX or verified official market data.

## 2. Data Priority
1. HTS / KRX official market data
2. Verified official global market data
3. Binance proxy / leading data

For Korean-market final judgment, HTS/KRX is the final confirmation layer. If Binance conflicts with HTS/KRX, state the conflict and reduce Binance confidence.

## 3. Exact Trigger
Official trigger: `AI Market Master 3.2 Binance Engine 실행`
Similar or abbreviated phrases must not silently execute the full Binance workflow.

## 4. Fixed 8-Symbol Watchlist
Default full Binance execution checks all 8 symbols unless the user explicitly requests a single symbol:
1. EWYUSDT
2. SAMSUNGUSDT
3. SKHYNIXUSDT
4. SOXLUSDT
5. QQQUSDT
6. SPYUSDT
7. TMFUSDT
8. BTCUSDT

A single successfully queried symbol never constitutes full Binance Engine completion.

## 5. Symbol Roles
- EWYUSDT: Korea equity leading proxy
- SAMSUNGUSDT: Samsung Electronics global leading proxy
- SKHYNIXUSDT: SK hynix / HBM-AI semiconductor proxy
- SOXLUSDT: semiconductor risk appetite
- QQQUSDT: Nasdaq/growth risk appetite
- SPYUSDT: broad US risk-on/off
- TMFUSDT: long-duration US Treasury / rates-liquidity proxy
- BTCUSDT: 24-hour crypto risk/liquidity auxiliary proxy

## 6. Required Data Fields When Available
For each symbol check, when supported:
- Current Price / 24h Change
- OHLCV
- Volume
- Mark Price
- Index Price
- Premium / Basis
- Open Interest
- OI Change or OI time series
- Funding Rate
- Global Long/Short Ratio
- Top Trader Position Long/Short Ratio
- Top Trader Account Long/Short Ratio
- Order Book / Best Bid-Ask
- Recent Trades / Aggregate Trades
- ADL Risk

If a field is unavailable, mark it `DATA UNAVAILABLE`. Do not infer missing values.

## 7. Minimum Completion Gate
- 8/8 symbols successfully queried at the required minimum level → `BINANCE ENGINE VERIFIED`
- 1–7/8 symbols successfully queried → `PARTIAL CONSENSUS` and list missing symbols
- 0/8 → `BINANCE DATA UNAVAILABLE`

Symbol availability and field depth are separate validation dimensions. 8/8 symbol availability does not automatically mean every field is fully validated.

## 8. Field-Depth Status
Use:
- VERIFIED: required fields for the intended judgment are validated
- PARTIAL: some required fields are unavailable
- UNAVAILABLE: intended analysis cannot be supported

Do not call a full-field execution VERIFIED when only ticker-level or snapshot-level data was retrieved.

## 9. Latest Re-query First
When the exact Full Dashboard trigger `AI Market Master 3.2 Dashboard 실행` is executed and Binance is required as a supporting layer, always attempt a fresh 8-symbol Binance query first.

Do not skip a fresh query merely because a prior Binance result is available.

Execution priority:
`Latest Re-query → Valid Fallback → Stale Reference Only → DATA UNAVAILABLE`.

The standalone Binance trigger continues to execute the current 8-symbol Binance workflow directly.

## 10. Binance Data Mode
Data freshness/source is tracked separately from the official Validation Status.

Use:
- `LIVE`: data newly queried during the current execution.
- `FALLBACK`: current re-query failed or produced unusable results and a valid prior verified result is being reused within the allowed freshness window.
- `STALE`: prior data is outside the allowed freshness window and may only be referenced as historical context.

`LIVE / FALLBACK / STALE` are Data Modes. They are not Bull/Bear signals and are not replacements for `VERIFIED / PARTIAL / UNAVAILABLE / PARTIAL CONSENSUS / EXECUTION BLOCKED`.

Do not create new official Validation States such as `FALLBACK VERIFIED` or `STALE VERIFIED`.

## 11. Fallback Eligibility
Fallback is allowed only when all of the following are satisfied:
1. A latest Binance re-query was attempted first.
2. The latest re-query failed or did not produce usable data for the intended judgment.
3. The prior result has a known query/completion timestamp.
4. The prior result has a known Validation Status and is reliable enough for reuse.
5. The prior result is inside the applicable freshness window.

Unvalidated historical data must not be promoted into fallback evidence.

If the prior result was `PARTIAL CONSENSUS` or field-depth `PARTIAL`, preserve that status. Fallback never upgrades the prior validation level.

## 12. Freshness Window
### Intraday
During market-hours / intraday analysis, prior Binance data may be used as normal fallback only when its age is **60 minutes or less**.

### Post-Close Structural Analysis
For post-close structural analysis, prior Binance data may be used as normal fallback only when its age is **2 hours or less**.

Data age is measured from the actual prior Binance query/completion time to the current analysis time.

If the prior query time is unknown, normal fallback is prohibited.

## 13. Confidence Adjustment
LIVE data uses the normal Confidence rules.

When FALLBACK data is used, downgrade the Binance-related Confidence by at least one level:
- High → Medium
- Medium → Low
- Low → Low

Fallback usage must be disclosed and must not be presented as equally fresh to LIVE data.

## 14. Stale / Expired Data Rule
If prior Binance data is older than:
- 60 minutes during intraday analysis, or
- 2 hours during post-close structural analysis,

it is not eligible for normal fallback.

Mark the Data Mode `STALE` and Confidence `Low` when historical reference is still useful.

STALE Binance data may be used only as historical/context comparison. It must not be a primary basis for:
- current Binance consensus confirmation,
- current broad Risk-On / Risk-Off confirmation,
- aggressive portfolio action,
- new leverage expansion,
- numeric scoring inputs.

If current judgment requires Binance evidence and no valid live/fallback result exists, use the existing official status `PARTIAL`, `UNAVAILABLE`, `PARTIAL CONSENSUS` or `EXECUTION BLOCKED` as appropriate.

## 15. Mandatory Fallback Disclosure
When FALLBACK or STALE data is used, show when available:
- Binance Data Mode
- Previous Query Time
- Current Analysis Time
- Data Age
- Previous Validation Status
- Symbol Availability
- Field Depth
- Current Confidence

Example:
`Binance Data Mode: FALLBACK`
`Previous Query: 10:34 KST`
`Current Analysis: 11:11 KST`
`Data Age: 37 min`
`Previous Status: 8/8 VERIFIED / Field Depth PARTIAL`
`Confidence: Medium`

## 16. Global Futures Sub-Engines
### G1 Global Risk
SPYUSDT + QQQUSDT + BTCUSDT.
Assess broad risk-on/risk-off. BTC is auxiliary and cannot alone confirm equity risk regime.

### G2 Semiconductor / AI Cycle
SOXLUSDT + SAMSUNGUSDT + SKHYNIXUSDT.
Cross-check with existing AI Cycle inputs such as HBM, DRAM/NAND, CAPEX, supply, inventory and AI-server demand.

### G3 Korea Leading
EWYUSDT + SAMSUNGUSDT + SKHYNIXUSDT.
Use as global/24-hour Korea-leading support and cross-check against HTS/KRX.

### G4 Rates / Liquidity
TMFUSDT combined with rates, USD/KRW, dollar, VIX, Fed/liquidity and oil when available.

### G5 Crypto Risk
BTCUSDT as a high-beta 24-hour risk/liquidity auxiliary signal. Never convert BTC-only movement into a broad-equity conclusion without corroboration.

### G6 Futures Positioning
Combine Price + Volume + OI + OI Change + Funding + Premium + Mark/Index + Long/Short + Order Book/Trades + ADL Risk.

## 17. Positioning Interpretation
Only apply OI-direction logic when OI change/time-series is actually available.
- Price up + OI up: new position inflow possible; direction requires corroboration.
- Price up + OI down: short covering possible.
- Price down + OI up: new short inflow possible.
- Price down + OI down: long liquidation / position reduction possible.

A current OI snapshot alone must not be labeled OI rising or falling.

## 18. Funding Rule
Funding is a positioning/crowding indicator, not an automatic buy/sell signal. Excessive positive or negative funding may indicate overheating/crowding. Interpret with price, OI, long/short and market structure.

## 19. Mark / Index / Premium Rule
Use divergence between mark, index and premium/basis to assess futures dislocation or supply-demand imbalance. Small normal differences are not automatically meaningful.

## 20. Long/Short Ratio Labeling
Always identify the exact endpoint/type used. Do not label Top Trader Accounts as general Global Long/Short or Top Trader Positions. If the requested ratio type was not fetched, mark it DATA UNAVAILABLE.

## 21. Order Book / Trades Rule
Best bid/ask can support spread/liquidity observations, but single-level quantities must not be over-interpreted as deep order-book imbalance. Recent trades require actual trade data; if not fetched, mark DATA UNAVAILABLE.

## 22. ADL Risk
ADL status is a leverage/liquidation risk input, not a directional market signal. Keep it separate from Bull/Bear judgment.

## 23. Cross-Engine Integration
Binance results feed the existing 24-engine architecture, especially Leading Indicator, Smart Money support, Global Liquidity, Technical, Ultra Short, AI Cycle, Portfolio, Strategy, Scenario Forecast, Change Detection, Validation, Final AI Decision and Intraday Position Tracking.

Risk Assessment is a subordinate analysis/module, not a 25th official engine.

## 24. Dashboard Mapping
In the Full Dashboard, do not create a ninth Binance category.
- Global risk / Korea-leading → Observation / Judgment
- Semiconductor signals → AI Cycle
- Positioning evidence → Evidence / Smart Money / Judgment
- TMF / rates → Liquidity
- Relevant market structure → Technical
- Final consensus → Strategy

## 25. Portfolio Decision Rule
Binance alone cannot finalize aggressive portfolio decisions. Final portfolio strategy requires consensus across Binance + HTS/KRX + Technical + Smart Money + AI Cycle + Liquidity/Risk.

FALLBACK Binance data has lower evidentiary weight than LIVE Binance data. STALE Binance data cannot be the primary basis of a current aggressive portfolio action.

## 26. Conflict Rule
If Binance is bullish while HTS/KRX is bearish, or vice versa, state the divergence explicitly. Do not silently choose the more convenient signal. HTS/KRX remains final confirmation for Korean-market action.

## 27. Anti-Hallucination
Never fabricate unavailable symbol data, OI direction, funding, long/short ratios, trades, order-book depth, premium, ADL, query timestamps, data age or scoring values.

## 28. Final Principle
Binance = Global Leading / Supporting Layer.
KRX/HTS = Final Korean-Market Confirmation.
Multi Engine Consensus > Single Indicator.

For Full Dashboard execution:
**Latest Re-query → Freshness Validation → Valid Fallback → Confidence Adjustment → HTS/KRX Cross-Validation → Multi Engine Consensus**.