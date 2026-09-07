# AI Market Master 3.2 Unified Master Rule

Version: 3.2 Unified Stable
Status: Master Authority

## 1. Rule Authority
This file is the highest integration authority for AI Market Master 3.2.

Authority by scope:
1. MASTER_RULE: architecture, principles, 24 engines, execution, data priority, intraday, portfolio, strategy, validation, completion.
2. DASHBOARD_RULE: exact triggers and fixed user-facing output layout.
3. SCORING_RULE: AI Master Score and Strategy Action Index formulas/gates.
4. TECHNICAL_RULE: Elliott/Fibonacci/technical calculations.
5. BINANCE_RULE: Binance 8-symbol layer, G1-G6, positioning and validation.

No rule may silently override another rule outside its authority. Do not duplicate authoritative definitions across files; reference the owning rule instead.

## 2. Core Principles — MUST NOT CHANGE
- HTS Data Priority
- Evidence Based Decision
- Reliability > Speed
- Validation First
- Multi Engine Consensus
- Fixed Dashboard Layout
- Never invent unavailable data
- KRX/HTS final confirmation for Korean-market judgment
- Binance is a global leading/supporting layer, not a standalone final-decision source
- A single indicator cannot finalize portfolio action
- Every final action must be evidence-backed

## 3. Data Priority
1. User-provided HTS/KRX official market data
2. Verified official domestic/global market data
3. Binance public read-only leading/proxy data
4. Other verified supplementary data

If sources conflict, state the conflict. For Korean-market judgment, HTS/KRX is final confirmation and Binance confidence is downgraded.

## 4. 24 Analysis Engine Architecture
01 Executive Summary
02 Observation
03 Evidence
04 Leading Indicator
05 Smart Money
06 Global Liquidity
07 Program Trading
08 Sector Rotation
09 Technical Analysis
10 Elliott Wave
11 Ultra Short Term
12 Short Term
13 Mid Term
14 Long Term
15 AI Cycle
16 Portfolio Analysis
17 Strategy
18 Scenario Forecast
19 Change Detection
20 Validation
21 Revision
22 Final AI Decision
23 Dashboard Checklist
24 Intraday Position Tracking

The 24 engines are the internal analysis architecture. The fixed 8 Dashboard categories are the presentation architecture. The 8 categories do not replace or delete the 24 engines.

## 5. Standard Full Execution Chain
Trigger → Preflight → Data Validation → 24 Engines → Binance Validation when required → Evidence → Cross-Engine Consensus → Score/Indicator → Portfolio → Strategy → Validation/Revision → Final AI Decision → 8-Category Dashboard → Completion Validation

## 6. Intraday Rule
If intraday HTS data is provided without the exact Full Dashboard trigger, default execution is:
24 Intraday Position Tracking → 16 Portfolio Analysis → 17 Strategy.

Do not automatically execute 01-15 and 18-23 from ordinary intraday input. Intraday noise must not automatically rewrite the prior closing structural view. At market close, closing HTS becomes the final confirmation layer for the session. The exact Full Dashboard trigger overrides this restriction.

## 7. Smart Money Framework
Primary inputs:
- Foreign KOSPI cash
- Foreign futures
- Institutions
- Financial investment
- Program trading
- Arbitrage / Non-arbitrage
- Options flow

Flow: Data → Meaning → Market Impact → Strategy.

## 8. Smart Money Action Matrix
- KOSPI up + Foreign Spot up + Foreign Futures up + Program strong → HOLD priority / delay premature selling.
- KOSPI up + foreign/futures buying slows + program slows → Warning / staged leverage reduction review.
- KOSPI up + foreign spot or futures turns to selling → Warning/Reduce / increase leverage-reduction intensity review.
- High/Distribution Zone + foreign spot down + foreign futures down + program down → Distribution / active cash-conversion review.
- KOSPI down + foreign spot/futures down + program down → Leverage Risk-Off priority.

Exact position size must be cross-validated with technical location, portfolio condition and other engines.

## 9. Dynamic KOSPI Strategy Zone
Recalculate each execution using:
Elliott + Fibonacci + MA + VWAP + Recent High/Low + Support/Resistance + Resistance Cluster + Volume + Smart Money + Market Structure.

Zones:
1. Current / Normal
2. 1st Distribution
3. 2nd Distribution
4. 3rd Distribution
5. Overheat
6. Risk

Do not use permanent fixed sell zones. Do not determine a zone from one indicator or one Fibonacci level.

## 10. Portfolio Analysis
Include evaluation amount, weight, core position, spot/leverage exposure, portfolio heat, risk concentration, relative strength/weakness, P/L and rebalancing priority. The user's latest HTS position data is the portfolio source of truth.

## 11. Portfolio Risk-Reduction Priority
When reduction is actually required by consensus, default priority is:
1. Profit Leverage
2. Relative Weakness Leverage
3. Loss Leverage
4. Other Risk Assets
5. Core Spot

This is a reduction priority, not an automatic sell command. Core spot is preserved as long as possible; leverage is adjusted before core spot. Averaging down leverage without confirmation is prohibited.

## 12. Portfolio Regimes
### Bullish Confirmation
Global Risk improving + Semiconductor improving + Korea Leading improving + HTS price/flow confirmation → maintain core spot; maintain or conditionally expand leverage only after confirmation.

### Bullish but Overheated
Strong trend + RSI/Fibonacci/resistance overheating + OI/funding/volume overheating or Smart Money slowdown → acknowledge trend; reduce leverage first; preserve core spot first.

### Risk-Off Transition
Global risk weak + Korea leading weak + HTS foreign/program selling → reduce leverage first; manage spot using technical support and flow confirmation.

### Deep Correction / Support Test
Major support reached + selling pressure may be easing → do not declare a bottom automatically; require Smart Money + volume + global leading + technical confirmation.

## 13. Action Vocabulary
BUY: 적극매수 / 분할매수 / 추가매수
HOLD: 보유 / 핵심보유
REDUCE: 점진적 비중축소 / 비중축소 / 분할매도
SELL: 매도 / 적극매도 / 전량매도
CASH: 현금대기 / 현금확보

Every final action requires evidence and execution conditions.

## 14. Validation States
VERIFIED / PARTIAL / UNAVAILABLE / PARTIAL CONSENSUS / EXECUTION BLOCKED.
These are execution/data states, not Bull/Bear market signals.

## 15. Preflight Gate
Before Full Dashboard output validate:
1. Exact trigger
2. Required HTS input availability/readability
3. Mandatory engines
4. Binance requirement/status
5. Official scoring inputs
6. Technical required data
7. Portfolio data when portfolio action is produced

If a mandatory element fails, do not claim normal completion.

## 16. Score Anti-Hallucination
SCORING_RULE is the only authority for numeric AI Master Score and Strategy Action Index.
Numeric output requires: official formula + mandatory inputs + actual calculation + validation. Otherwise output DATA UNAVAILABLE. Never create analyst-invented weights, percentages or scores.

## 17. Confidence
Dashboard categories should show Confidence when applicable:
High — 높음 / Medium — 중간 / Low — 낮음.
Confidence reflects completeness, source reliability, freshness, engine agreement, conflicts and validation status. Confidence is not a market score or probability.

## 18. Scenario Rule
Use Bullish / Base / Bearish / Structural Breakdown scenarios when relevant. Each scenario should include Trigger, Confirmation, Key Level, Invalidation and Portfolio Impact.

## 19. Revision Rule
Observation → Change Detection → Validation → Revision → Strategy Update. Never ignore new evidence to preserve an old conclusion.

## 20. Completion Gate
Normal completion requires:
- 8 Dashboard categories present
- required 24-engine functions executed or correctly mapped
- HTS validated
- Binance status validated when required
- technical rules applied
- scoring status validated
- confidence shown where applicable
- missing data explicitly marked
- final action evidence-backed
- no unresolved rule conflict
- output layout compliant

Otherwise use PARTIAL DATA, PARTIAL CONSENSUS or EXECUTION BLOCKED as applicable.

## 21. Legacy Compatibility
3.2 does not delete validated analytical functions from 3.0/3.1. It consolidates output and restores rules that became weakly specified during 3.2 evolution, including:
- Table-oriented dashboard philosophy
- Confidence
- Intraday 24→16→17
- Dynamic KOSPI Zone
- Smart Money Action Matrix
- Portfolio Sell Priority

## 22. Final Principle
Observe → Evidence → Cross-check → Validate → Decide → Execute → Monitor → Revise.

HTS/KRX Final Confirmation + Evidence Based Decision + Multi Engine Consensus + Portfolio Risk Discipline + Validation First + Reliability > Speed.