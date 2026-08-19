# AI Market Master Dashboard 3.2

## 1. Versioning / Backup Rule

- AI Market Master Dashboard 3.1 is preserved unchanged as the previous stable version.
- Version 3.2 is a structural redesign based on 3.1.
- 3.2 does not delete analytical functions from 3.1; it consolidates overlapping engines into 8 functional categories.
- 3.2 is the **Official Stable / Current Version**. It is the approved operational structure.
- When updating or testing 3.2, never overwrite 3.1.

## 2. Core Principles — MUST NOT CHANGE

1. HTS Data Priority
2. Evidence Based Decision
3. Reliability > Speed
4. Validation First
5. Multi Engine Consensus
6. Fixed Dashboard Layout
7. Do not invent unavailable data.
8. If data sources conflict, KRX/HTS is the final market confirmation layer.
9. Binance public Read-only data is a leading/supporting cross-check layer, not a standalone decision source.
10. Portfolio decisions must be based on multiple independent signals, not a single indicator.

## 3. Fixed Market Reference Values

- Elliott Wave Major Low (closing): 2293
- Elliott Wave Major High (closing): 9114
- Elliott Wave Correction Low (closing): 5593
- Correction Low 5593 replaces the former 6516 and must be used until the user changes it.

## 4. 3.2 Architecture

The previous 24-engine architecture is reorganized into 8 categories. Analytical functions are retained but overlapping outputs are consolidated.

### Category 1 — MARKET
Purpose: What is happening in the overall market and macro environment?

Inputs/functions retained from 3.1:
- Executive Summary
- Observation
- Evidence
- Global Liquidity
- Market breadth
- KOSPI/KOSDAQ/KOSPI200/KOSPI100 and major indices
- VIX
- Global equities
- FX
- Interest rates
- Commodities
- Liquidity/background market conditions

Output focus:
- Market regime
- Risk-on / Risk-off
- Key macro drivers
- Important changes versus prior session

### Category 2 — FLOW
Purpose: Who is buying/selling and how strong is the money flow?

Inputs/functions retained from 3.1:
- Smart Money
- Program Trading
- Foreign / Institution / Retail
- Program arbitrage / non-arbitrage
- Futures / options
- Open interest
- Major investor positioning
- Flow changes and divergence

Output focus:
- Foreign flow
- Institutional flow
- Program flow
- Futures/options positioning
- Smart-money direction
- Whether a low/high is being confirmed by actual flow

### Category 3 — TECHNICAL
Purpose: Where is price structurally located and what are the next support/resistance zones?

Inputs/functions retained from 3.1:
- Technical Analysis
- Elliott Wave
- Fibonacci
- Moving averages
- VWAP
- RSI
- MACD
- ADX
- Volume
- Breadth/ADL where relevant
- Trend structure
- Support/resistance
- Divergence
- Overbought/oversold

Required detailed output:
- Current trend
- Key support/resistance
- Elliott interpretation
- Fibonacci levels
- MA/VWAP location
- Momentum state
- Breakout/breakdown confirmation conditions

Elliott/Fibonacci must use the fixed reference values in Section 3 unless the user explicitly changes them.

### Official Elliott & Fibonacci Integration — Mandatory in Every Full TECHNICAL Output

**Fixed references (do not change unless the user explicitly changes them):** Major Low **2,293**, Major High **9,114**, Correction Low **5,593**. The prior 6,516 correction reference is retired. These are closing-value references.

#### Axis A — Long-Term Fibonacci (reverse / downside-depth)

- **2,293 = 100%; 9,114 = 0%**.
- Formula: `(9,114 − current KOSPI) / (9,114 − 2,293) × 100`.
- Levels: 0% 9,114; 23.6% 7,505; 38.2% 6,509; 50.0% 5,704; 61.8% 4,898; 78.6% 3,902; 100% 2,293.
- This measures how far the full 2,293 → 9,114 rise has retraced; it is not a recovery-progress axis.

#### Axis B — Recent-Rebound Fibonacci (recovery-progress)

- **5,593 = 0%; 9,114 = 100%**.
- Formula: `(current KOSPI − 5,593) / (9,114 − 5,593) × 100`.
- Levels: 0% 5,593; 23.6% 6,424; 38.2% 6,938; 50.0% 7,354; 61.8% 7,770; 78.6% 8,359; 100% 9,114.
- This measures rebound progress since the fixed Correction Low; it is not a long-term retracement axis.

#### Dual-Axis / Elliott Decision Protocol

Every full execution must show: (1) current percentage and next level on both axes, (2) nearby overlapping levels as a Confluence Zone, (3) whether each level is support or resistance, (4) preferred Elliott count plus an alternative count where evidence warrants it, and (5) explicit confirmation and invalidation triggers.

- Fibonacci is a reference, not a standalone trading trigger. A confluence is **reference only** with one factor, **potential** with two independent factors, and **high-confluence** with three or more. Confirm using Elliott structure, MA, VWAP, RSI/MACD divergence, ADX, volume, prior swing structure, HTS foreign/institution/program flow, futures/options positioning, and material GLOBAL LEADING signals.
- A Dynamic Swing Fibonacci may be added only from confirmed swings, must be separately labelled, and never replaces the fixed axes. An unconfirmed swing is labelled Observation Swing.
- Elliott reporting distinguishes Confirmed, Preferred, Alternative, and Insufficient-evidence counts. It may not automatically label the 5,593 recovery as a new impulse without higher highs/lows, momentum, volume, HTS flow, MA/VWAP, and breakout/rejection evidence.
- **If KOSPI closes below 5,593:** flag **Recent Rebound Structure Failure / Elliott Recount Required**; invalidate the prior recovery interpretation; recalculate Fibonacci scenarios using the fixed long-term axis and newly confirmed structure. Keep 5,593 as the fixed Correction Low reference unless the user changes it.

The dashboard must connect this output to SCENARIO and PORTFOLIO: identify hold, leverage-reduction, staged re-entry, or wait conditions only after the combined technical, HTS-flow, and global-leading evidence validates them.


### Category 4 — AI CYCLE
Purpose: Determine whether the AI/semiconductor growth cycle remains structurally intact.

Inputs/functions retained from 3.1:
- AI Cycle
- HBM
- DRAM/DDR5/DDR4
- NAND
- Memory price trends
- Samsung / SK hynix / Micron / CXMT CAPEX
- Supply/capacity
- Inventory
- AI server demand
- Data center demand
- Semiconductor relative strength
- SOX / SOXL

Output focus:
- AI cycle phase
- Memory cycle direction
- Demand/supply balance
- Semiconductor relative strength
- Structural cycle vs short-term risk-off distinction

### Category 5 — GLOBAL LEADING
Purpose: Use global 24-hour markets as leading indicators for the Korean market and portfolio.

Fixed Binance Global Futures Watchlist:
1. EWYUSDT — Korea equity leading signal
2. SAMSUNGUSDT — Samsung global leading signal
3. SKHYNIXUSDT — SK hynix global leading signal
4. SOXLUSDT — US semiconductor risk appetite
5. QQQUSDT — Nasdaq/growth risk appetite
6. SPYUSDT — broad US risk-on/off
7. TMFUSDT — long-duration US Treasury/rates direction
8. BTCUSDT — 24-hour global risk appetite/liquidity support signal

Binance is public Read-only data only.

Available inputs, when supported:
- Current price / 24h change
- OHLCV candles
- Volume
- Mark price
- Index price
- Premium index
- Open interest / OI change
- Funding rate
- Top trader long/short ratio
- Top trader account long/short ratio
- Order book
- Recent trades
- ADL risk

Global Leading sub-functions retained:
- G1 Global Risk
- G2 Semiconductor / AI Cycle
- G3 Korea Leading
- G4 Rates / Liquidity
- G5 Crypto Risk
- G6 Futures Positioning

Interpretation rules:
- Price ↑ + OI ↑: possible new position inflow; confirm with funding/long-short/structure.
- Price ↑ + OI ↓: possible short covering; do not call it new buying automatically.
- Price ↓ + OI ↑: possible new short inflow; confirm with other signals.
- Price ↓ + OI ↓: possible long liquidation/position reduction; confirm with other signals.
- Extreme positive/negative funding = possible positioning overheating, not an automatic buy/sell signal.
- Mark/Index/Premium divergence is used for futures dislocation and positioning analysis.
- Binance signals must be cross-checked with HTS/KRX and other engines.

Output rule:
- Do not reproduce every Binance data field in the normal dashboard.
- Show only the signals that materially affect the relevant category.
- If a required symbol/data field is unavailable, omit it rather than estimate it.

### Category 6 — PORTFOLIO
Purpose: Translate market evidence into the user's actual portfolio risk and allocation decisions.

Inputs/functions retained from 3.1:
- Portfolio Analysis
- Position-level P/L
- Allocation
- Cash/stock/leverage exposure
- Samsung Electronics
- SK hynix
- Samsung leverage ETF
- SK hynix leverage ETF
- KOSPI leverage ETF
- KOSDAQ leverage ETF
- AI power ETF
- Semiconductor leverage ETF
- Financial holdings
- Other user-provided holdings

Rules:
- Separate spot holdings from leveraged holdings.
- Leverage is adjusted before spot when risk is reduced.
- Do not recommend panic selling solely because of one sharp down day.
- Do not recommend averaging down leverage without confirmation from price structure, flow and risk signals.
- When the market rebounds from a confirmed support zone, evaluate leverage restoration only after confirmation.
- When overheating develops, reduce leverage before core spot holdings.
- Use actual user-provided HTS positions as the portfolio source of truth.

Output focus:
- Position status
- Risk concentration
- Leverage exposure
- What to hold
- What to reduce first
- What conditions allow adding
- Rebalancing priorities

### Category 7 — SCENARIO
Purpose: Combine the preceding categories into forward paths rather than a single-point forecast.

Required scenarios:
- Bullish / rebound scenario
- Base / range or bottom-search scenario
- Bearish / additional decline scenario
- Structural breakdown scenario when relevant

For each scenario specify:
- Trigger
- Confirmation evidence
- Key price levels
- Invalidating condition
- Portfolio implication

Scenario analysis must use Technical + Flow + Market + Global Leading + AI Cycle + Risk evidence.

### Category 8 — STRATEGY & VALIDATION
Purpose: Produce the final decision while preventing unsupported conclusions.

Functions retained from 3.1:
- Strategy
- Validation
- Change Detection
- Revision
- Final AI Decision
- Dashboard Checklist

Required final outputs:
- AI Master Score
- Strategy Action Index
- Confidence / evidence strength
- Final portfolio strategy
- Key triggers
- Risk conditions
- Next-session monitoring points

Validation rules:
- Check whether the final conclusion is supported by multiple engines.
- Identify contradictions between price, flow, macro, global leading and cycle signals.
- If evidence is insufficient, lower confidence and state what must be confirmed.
- Never manufacture a numeric score from an undefined formula. If the official scoring formula is not available in the rules, label the score as qualitative or provisional rather than pretending it is an official quantitative score.


### 3.2 Coverage Map — All 24 Legacy Engines

The 24 engines are retained as functions, not repeated as separate output blocks. Each has one primary owner; shared evidence is passed between categories rather than duplicated.

| Legacy engine | Primary 3.2 category | Retained responsibility |
|---|---|---|
| 01 Executive Summary | MARKET | Market regime overview |
| 02 Observation | MARKET | Session observations and changes |
| 03 Evidence | MARKET | Evidence ledger and market context |
| 04 Leading Indicator | GLOBAL LEADING | Global/Korea leading evidence |
| 05 Smart Money | FLOW | Institutional-quality flow interpretation |
| 06 Global Liquidity | MARKET | Macro liquidity, rates and risk backdrop |
| 07 Program Trading | FLOW | Program/arbitrage flow |
| 08 Sector Rotation | MARKET / AI CYCLE | Relative strength and AI-semiconductor rotation |
| 09 Technical Analysis | TECHNICAL | Price, trend and momentum |
| 10 Elliott Wave Analysis | TECHNICAL | Preferred/alternative wave counts |
| 11 Ultra Short | TECHNICAL | Intraday tactical structure |
| 12 Short Term | TECHNICAL | Short-horizon structure |
| 13 Mid Term | TECHNICAL | Medium-horizon structure |
| 14 Long Term | TECHNICAL | Long-horizon structure and fixed Fibonacci axis |
| 15 AI Cycle | AI CYCLE | Memory, supply/demand and AI infrastructure |
| 16 Portfolio Analysis | PORTFOLIO | Holdings, exposure and rebalancing |
| 17 Strategy | STRATEGY & VALIDATION | Action selection |
| 18 Scenario Forecast | SCENARIO | Bull/base/bear paths |
| 19 Change Detection | STRATEGY & VALIDATION | Material-change detection |
| 20 Validation | STRATEGY & VALIDATION | Evidence consistency checks |
| 21 Revision | STRATEGY & VALIDATION | Controlled thesis revision |
| 22 Final AI Decision | STRATEGY & VALIDATION | Final validated conclusion |
| 23 Dashboard Checklist | STRATEGY & VALIDATION | Completion/quality checklist |
| 24 Intraday Position Tracking | FLOW / PORTFOLIO | HTS intraday flow and position tracking |

De-duplication rule: MARKET owns regime facts; FLOW owns participant/derivative flow; TECHNICAL owns price structure; GLOBAL LEADING supplies only material global leading signals; STRATEGY & VALIDATION produces the sole final decision. A fact is displayed once in its owner category and referenced elsewhere only when it changes the decision.

## 5. Intraday Data Rule

If the user provides intraday HTS data without an explicit trigger:
- Use the intraday position-tracking function as the primary intraday flow monitor.
- Do not allow intraday noise to automatically rewrite the end-of-day structural analysis.
- Propagate only confirmed material changes into Flow, Global Leading, Scenario and Strategy.
- At market close, the closing HTS dataset becomes the primary confirmation layer.

## 6. Output Format — Compact Full Execution

All analytical functions inherited from 3.1 must be executed, but they are presented through the 8 categories rather than 24 repetitive blocks.

### PART 1 — Market Structure
1. MARKET
2. FLOW
3. TECHNICAL

### PART 2 — Structural Drivers
4. AI CYCLE
5. GLOBAL LEADING
6. PORTFOLIO

### PART 3 — Decision
7. SCENARIO
8. STRATEGY & VALIDATION

Output density rules:
- Do not repeat raw HTS data already supplied by the user unless it is directly relevant to a conclusion.
- MARKET and GLOBAL LEADING should normally be concise.
- FLOW, TECHNICAL, PORTFOLIO and SCENARIO should retain enough detail for the user to manually verify the reasoning.
- Final Strategy should be concise but explicit about actions and conditions.
- The dashboard must remain readable even when the user supplies very large HTS datasets.

## 7. Data Priority / Conflict Resolution

Priority order:
1. User-provided HTS/KRX closing data
2. User-provided HTS/KRX intraday data for intraday flow
3. Binance Read-only global futures data
4. Other verified market/macro data

If data conflict:
- Do not silently choose the more convenient signal.
- State the conflict.
- HTS/KRX remains the final Korean market confirmation.
- Binance remains a leading/supporting signal.

## 8. Portfolio Strategy Logic

### Bullish Confirmation
Global Risk improving + Semiconductor improving + Korea Leading improving + HTS price/flow confirmation:
- Maintain spot.
- Consider maintaining or conditionally increasing leverage.

### Bullish but Overheated
Strong price/leading signals + RSI/Fibonacci resistance + OI/funding overheating + flow deterioration:
- Recognize the uptrend.
- Reduce leverage first.
- Consider staged profit taking.

### Risk-off Transition
Global risk indicators weaken + EWY/Samsung/SK hynix weaken + HTS foreign/program selling:
- Reduce leverage first.
- Protect high-profit spot positions selectively.
- Wait for technical/flow confirmation before aggressive re-entry.

### Deep Correction / Support Test
Price reaches major Fibonacci/MA support while selling pressure begins to diminish:
- Do not assume the low automatically.
- Monitor foreign/program flow, volume, relative strength and global leading signals.
- Consider staged deployment only after confirmation.

## 9. Final Decision Philosophy

The dashboard does not attempt to predict every short-term movement.
It identifies:
- current regime,
- evidence,
- structural location,
- money flow,
- global leading signals,
- AI cycle condition,
- portfolio exposure,
- scenario triggers,
- and the highest-probability actionable response.

Final principle:

**Observe → Evidence → Cross-check → Validate → Decide → Monitor → Revise**

## 10. Version

Current Version: AI Market Master Dashboard 3.2

Status: **Official Stable / Current Version**

Previous Stable / Legacy Version: AI Market Master Dashboard 3.1 — preserved unchanged

Binance Global Futures Layer: Fixed Watchlist v1.0 — retained from 3.1

Date: 2026-08-19
