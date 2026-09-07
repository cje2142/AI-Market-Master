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

## 9. Global Futures Sub-Engines
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

## 10. Positioning Interpretation
Only apply OI-direction logic when OI change/time-series is actually available.
- Price up + OI up: new position inflow possible; direction requires corroboration.
- Price up + OI down: short covering possible.
- Price down + OI up: new short inflow possible.
- Price down + OI down: long liquidation / position reduction possible.

A current OI snapshot alone must not be labeled OI rising or falling.

## 11. Funding Rule
Funding is a positioning/crowding indicator, not an automatic buy/sell signal. Excessive positive or negative funding may indicate overheating/crowding. Interpret with price, OI, long/short and market structure.

## 12. Mark / Index / Premium Rule
Use divergence between mark, index and premium/basis to assess futures dislocation or supply-demand imbalance. Small normal differences are not automatically meaningful.

## 13. Long/Short Ratio Labeling
Always identify the exact endpoint/type used. Do not label Top Trader Accounts as general Global Long/Short or Top Trader Positions. If the requested ratio type was not fetched, mark it DATA UNAVAILABLE.

## 14. Order Book / Trades Rule
Best bid/ask can support spread/liquidity observations, but single-level quantities must not be over-interpreted as deep order-book imbalance. Recent trades require actual trade data; if not fetched, mark DATA UNAVAILABLE.

## 15. ADL Risk
ADL status is a leverage/liquidation risk input, not a directional market signal. Keep it separate from Bull/Bear judgment.

## 16. Cross-Engine Integration
Binance results feed the existing 24-engine architecture, especially Leading Indicator, Smart Money support, Global Liquidity, Technical, Ultra Short, AI Cycle, Portfolio, Strategy, Scenario Forecast, Change Detection, Validation, Final AI Decision and Intraday Position Tracking.

Risk Assessment is a subordinate analysis/module, not a 25th official engine.

## 17. Dashboard Mapping
In the Full Dashboard, do not create a ninth Binance category.
- Global risk / Korea-leading → Observation / Judgment
- Semiconductor signals → AI Cycle
- Positioning evidence → Evidence / Smart Money / Judgment
- TMF / rates → Liquidity
- Relevant market structure → Technical
- Final consensus → Strategy

## 18. Portfolio Decision Rule
Binance alone cannot finalize aggressive portfolio decisions. Final portfolio strategy requires consensus across Binance + HTS/KRX + Technical + Smart Money + AI Cycle + Liquidity/Risk.

## 19. Conflict Rule
If Binance is bullish while HTS/KRX is bearish, or vice versa, state the divergence explicitly. Do not silently choose the more convenient signal. HTS/KRX remains final confirmation for Korean-market action.

## 20. Anti-Hallucination
Never fabricate unavailable symbol data, OI direction, funding, long/short ratios, trades, order-book depth, premium, ADL or scoring values.

## 21. Final Principle
Binance = Global Leading / Supporting Layer.
KRX/HTS = Final Korean-Market Confirmation.
Multi Engine Consensus > Single Indicator.