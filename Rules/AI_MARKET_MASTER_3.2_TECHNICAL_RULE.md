# AI Market Master 3.2 Technical Rule

Version: 3.2 Unified Stable
Status: Technical Analysis Authority

## 1. Scope
Official authority for Elliott Wave, Fibonacci, Dynamic Swing Fibonacci, MA, VWAP, RSI/divergence, MACD, Ichimoku, ADX, ADL/Breadth, Volume, trend, support/resistance, breakout/breakdown and technical inputs to Dynamic KOSPI Strategy Zone.

## 2. Fixed Elliott Reference Values
- Major Low = 2,293
- Major High = 9,114
- Correction Low = 5,593
5,593 replaces former 6,516 until explicitly changed by the user.

## 3. Mandatory Dual-Axis Fibonacci
### Axis A — Long-Term Retracement
Major High 9,114 = 0%; Major Low 2,293 = 100%.
Levels: 0=9,114; 23.6≈7,505; 38.2≈6,509; 50≈5,704; 61.8≈4,898; 78.6≈3,902; 100=2,293.

### Axis B — Recovery Fibonacci
Correction Low 5,593 = 0%; Major High 9,114 = 100%.
Levels: 0=5,593; 23.6≈6,424; 38.2≈6,938; 50≈7,354; 61.8≈7,770; 78.6≈8,359; 100=9,114.

Every formal Elliott/Fibonacci analysis evaluates both axes. Never substitute one for the other.

## 4. Dual-Axis Output
When data permits, report:
1. Axis A position
2. Axis B position
3. next important level on each axis
4. confluence status
5. Elliott interpretation
6. confirmation
7. invalidation

## 5. Fibonacci Is Not Automatic Support/Resistance
A touch alone never confirms support, resistance, buy or sell. Require multiple independent confirmations such as Elliott, MA, VWAP, volume, previous high/low, RSI/MACD, ADX, Smart Money, program flow, breadth or global leading data.

## 6. Dynamic Swing Fibonacci
A third dynamic Fibonacci may be added from confirmed recent swing points. Do not use arbitrary intraday extremes, do not replace fixed axes, label separately, and use `Observation Swing` when confirmation is insufficient.

## 7. Elliott Wave Framework
Classify counts as:
- Confirmed Wave Count
- Preferred Wave Count
- Alternative Wave Count
- Unconfirmed / Insufficient Evidence
Do not label an unverified count as confirmed.

## 8. Elliott Confirmation Inputs
Evaluate swing structure, HH/HL or LH/LL, price extension, Fibonacci relations, momentum, RSI, MACD, volume, MA, VWAP, Smart Money, program flow, global leading and breakout/rejection behavior. Elliott alone cannot finalize strategy.

## 9. Recovery Structure Failure
A closing break below 5,593 requires review of Recovery Structure Failure, Elliott recount, Recovery Fibonacci recalculation, medium/long-term structure validation and portfolio-risk reassessment. An intraday break alone does not automatically confirm structural failure.

## 10. Moving Average
Use available MA5/20/50/60/120/200 and evaluate price location, alignment, slope, reclaim/loss and confluence. One MA cross alone does not confirm trend reversal.

## 11. VWAP
Use available VWAP/VWAP20/50/60/200. Evaluate price location, reclaim/rejection and MA+VWAP clusters. Clusters are important support/resistance candidates.

## 12. RSI / Divergence
RSI measures momentum/overbought-oversold condition but does not alone call a top/bottom or action. Evaluate bullish/bearish and hidden divergence when sufficient data exists; cross-check with price, volume, MACD and Smart Money.

## 13. MACD
Evaluate MACD line, signal line, histogram/oscillator, zero line, cross, acceleration/deceleration and divergence. A cross alone does not finalize action.

## 14. Ichimoku
When available evaluate Tenkan, Kijun, Senkou Span A/B, cloud and Chikou; price vs cloud, breakout, Tenkan/Kijun, cloud thickness and future cloud direction. Missing data = DATA UNAVAILABLE.

## 15. ADX
ADX measures trend strength, not direction. Rising ADX is not inherently bullish/bearish. Low ADX can reduce breakout confidence.

## 16. ADL / Breadth
Use advance/decline, ADL and breadth when available. Index strength with weak breadth may indicate concentration/narrow leadership; reflect breadth divergence in risk/regime judgment.

## 17. Volume
Use current volume, volume averages, breakout/reversal volume, contraction and exhaustion context. Strong price movement on weak volume may reduce confidence, subject to market-structure context.

## 18. Trend Structure
Combine price, swing, MA, VWAP, momentum, ADX and volume. Internal labels may be Strong Uptrend / Uptrend / Range-Neutral / Downtrend / Strong Downtrend, but Dashboard Signal must normalize to the canonical signal system.

## 19. Support / Resistance
Prefer zones over isolated numbers. Inputs may include Fibonacci, MA, VWAP, previous high/low, gaps, volume concentration, Elliott swing and psychological levels. Multiple nearby factors form a Cluster.

## 20. Resistance / Support Cluster
Resistance Cluster may support Dynamic KOSPI Distribution zones. Support Cluster is not an automatic buy zone; require stabilization, volume response, Smart Money, foreign futures/program, momentum and global-leading confirmation.

## 21. Breakout / Breakdown Confirmation
Do not confirm from an intraday touch alone. Consider closing basis, volume, VWAP/MA hold or failed reclaim, Smart Money, follow-through and retest.

## 22. Technical Conflict
Do not force conflicting indicators into one direction. State the conflict and reduce Confidence when appropriate.

## 23. Timeframe Separation
Separate Ultra Short, Short, Mid and Long Term. Short-term strength does not automatically cancel medium/long-term weakness and vice versa.

## 24. Dynamic KOSPI Zone Technical Inputs
Use Elliott + fixed Dual Fibonacci + Dynamic Fibonacci when available + MA + VWAP + recent high/low + support/resistance + resistance cluster + volume + momentum. MASTER_RULE adds Smart Money and Portfolio state.

## 25. Technical → Strategy Flow
Price Structure → Trend → Momentum → Elliott/Fibonacci → Support/Resistance → Confirmation/Invalidation → Dynamic KOSPI Zone → Strategy.

## 26. Required Dashboard Technical Output
When available show Signal, key indicator, Confidence, Trend, Elliott, Axis A, Axis B, Dynamic Fibonacci if relevant, RSI, MACD, Ichimoku, MA/VWAP, ADX, ADL/Breadth, Volume, Support, Resistance, Confirmation and Invalidation. Missing items = DATA UNAVAILABLE.

## 27. Anti-Hallucination
Never invent HTS indicators, historical highs/lows, Fibonacci anchors, confirmed Elliott counts, RSI/MACD values, volume, support/resistance or other unavailable technical data.

## 28. Technical Master Principle
Elliott + Dual Fibonacci + MA/VWAP + Momentum + Volume + Price Structure, cross-validated with Smart Money + Liquidity + Global Leading. A single technical indicator cannot create final portfolio action.