# AI Market Master 3.2 Dashboard Rule

Version: 3.2 Unified Stable
Status: Dashboard Presentation Authority

## 1. Scope
This file controls only exact triggers and user-facing output layout. Market formulas, technical calculations, Binance interpretation/freshness and scoring belong to their dedicated rules.

## 2. Exact Triggers
Full Dashboard: `AI Market Master 3.2 Dashboard 실행`
Binance Engine: `AI Market Master 3.2 Binance Engine 실행`
Similar or abbreviated phrases must not silently trigger the full workflows.

## 3. Fixed 8 Dashboard Categories
Every Full Dashboard must output exactly, in this order:
1. Observation (시장 관찰)
2. Evidence (핵심 근거)
3. Judgment (종합 판단)
4. AI Cycle (AI·반도체 사이클)
5. Smart Money (스마트머니)
6. Liquidity (유동성)
7. Technical (기술 분석)
8. Strategy (전략)

Never omit, merge, reorder or replace these categories. Scenario, Portfolio, Global Leading, Validation and other sub-engines must be mapped inside them, not added as ninth-level categories.

## 4. 24 Engine → 8 Category Mapping
- Observation: Executive Summary, Observation, Leading Indicator, Global Market, Breadth, relevant Intraday summary.
- Evidence: Evidence, Program Trading, derivatives evidence, Change Detection, Data Validation.
- Judgment: Cross-Engine Consensus, Scenario Forecast, Risk Assessment sub-analysis, integrated market regime.
- AI Cycle: AI Cycle, semiconductor/HBM/DRAM/NAND, CAPEX, supply/inventory/demand, semiconductor relative strength.
- Smart Money: foreign cash/futures, institutions, financial investment, program, arbitrage/non-arbitrage, options.
- Liquidity: Global Liquidity, rates, FX, deposits, credit/margin, Fed/M2/TGA/RRP when available, TMF support.
- Technical: Technical Analysis, Elliott, Fibonacci, RSI, MACD, Ichimoku, MA, VWAP, ADX, ADL, support/resistance.
- Strategy: Portfolio, Strategy, Dynamic KOSPI Zone, Portfolio Risk Priority, Scenario implication, Validation, Revision, Final AI Decision, Dashboard Checklist.

The 24 engines are internal analysis; the 8 categories are presentation.

## 5. Table First
Every Full Dashboard begins with a summary table before detailed sections.
Minimum columns:
| Category | Signal | Score / Indicator | Confidence | Judgment | Action |
The table must contain all 8 categories.

## 6. Korean-First + Official English
User-facing output is Korean-first. Official category/engine/score names remain in English with Korean meaning where useful, e.g. `Observation (시장 관찰)`, `AI Master Score (AI 종합점수)`.

## 7. Canonical Signal System
Only the following labels may appear in the official Signal field:
- 🟢 Strong Bull / Positive — 강한 긍정·강세
- 🔵 Bull — 긍정·강세
- 🟡 Neutral — 중립
- 🟠 Warning / Caution — 경고·주의
- 🔴 Bear / Negative — 부정·약세
- ⚫ Extreme Risk — 극단적 위험
- ⚪ DATA UNAVAILABLE — 데이터 없음

Other descriptive wording may appear in explanation but must be normalized in the Signal field. Signal labels never create numeric scores by themselves.

## 8. Validation Status Is Separate
VERIFIED / PARTIAL / UNAVAILABLE / PARTIAL CONSENSUS / EXECUTION BLOCKED are execution/data states, not market signals.

For Binance, `LIVE / FALLBACK / STALE` are separate Data Modes defined by BINANCE_RULE. They must not replace or be merged into the official Validation Status.

## 9. Standard Category Output Order
When applicable, each category follows:
1. Signal
2. Score / Indicator
3. Confidence
4. Evidence
5. Judgment
6. Action

If direct action is not appropriate, use `Action: Strategy Category에 반영`.

## 10. Score / Indicator
Use an official score only when SCORING_RULE permits it. Otherwise show verified indicators such as foreign spot/futures, RSI, MACD, funding, OI, deposits, credit, breadth, support/resistance. Never invent 83 points, 72%, 8.4/10 or similar unofficial numbers.

## 11. Confidence
Use:
- High — 높음
- Medium — 중간
- Low — 낮음
Confidence reflects completeness, source reliability, freshness, engine agreement, signal conflict and validation status. It is not a probability or market score.

If Binance FALLBACK is used, apply the Confidence downgrade defined by BINANCE_RULE. Dashboard presentation must not hide that downgrade.

## 12. Missing Data
Never delete a required category because data is missing. Mark the relevant item `DATA UNAVAILABLE`; for partial retrieval use PARTIAL or PARTIAL CONSENSUS as applicable. Never estimate missing values.

## 13. Evidence / Judgment / Action
Evidence should prioritize HTS/KRX, verified official data, then verified Binance supporting data. Judgment must reflect cross-engine consensus and explicitly state conflicts. Action must use the MASTER_RULE vocabulary and include evidence/conditions.

LIVE Binance evidence has higher freshness than FALLBACK evidence. STALE Binance data may be shown as historical context only and must not be presented as current decisive evidence.

## 14. Strategy Mandatory Outputs
Strategy (전략) must include:
1. Final Signal
2. AI Master Score
3. Strategy Action Index
4. Confidence
5. Final Portfolio Action
6. Dynamic KOSPI Zone
7. Key Support
8. Key Resistance
9. Risk / Invalidation Conditions
10. Next Validation Conditions
11. Execution Status

If official scores cannot be calculated, display `DATA UNAVAILABLE` rather than inventing numbers.

## 15. Portfolio / Scenario / Binance Placement
- Portfolio actions belong mainly in Strategy.
- Scenarios belong mainly in Judgment/Strategy and do not become a ninth category.
- Binance results must be mapped into the existing 8 categories: global risk into Observation/Judgment, semiconductor signals into AI Cycle, TMF/rates into Liquidity, positioning evidence into Evidence/Smart Money/Judgment, final consensus into Strategy.

## 16. Binance Status Presentation
When Binance is part of a Full Dashboard execution, show its status within the existing 8-category structure or the execution/validation summary. Do not create a ninth Binance category.

Display, when available:
- `Binance Validation Status`
- `Binance Data Mode`
- `Previous Query Time` when FALLBACK/STALE
- `Current Analysis Time` when FALLBACK/STALE
- `Data Age` when FALLBACK/STALE
- `Symbol Availability`
- `Field Depth`
- `Confidence`

Recommended compact forms:

Latest query success:
`Binance: LIVE / 8/8 VERIFIED / Field Depth VERIFIED or PARTIAL`

Fallback:
`Binance: FALLBACK / 8/8 VERIFIED / 37 min old / Confidence Medium`

Stale historical reference:
`Binance: STALE / 74 min old / Confidence Low / Current-decision use restricted`

No usable current data:
`Binance: DATA UNAVAILABLE`

The exact freshness windows and fallback eligibility are owned by BINANCE_RULE and are not redefined here.

## 17. Technical Presentation
Technical should show, when available: Trend, Elliott, Dual Fibonacci, Dynamic Fibonacci if relevant, RSI, MACD, Ichimoku, MA/VWAP, ADX, ADL/Breadth, Volume, Support, Resistance, Confirmation and Invalidation.

## 18. Density Rule
Large HTS input does not change the 8-category structure. Remove duplicated raw data, prioritize decision-relevant evidence and avoid repeating the same conclusion across categories.

## 19. Completion Declaration
Only declare `AI Market Master 3.2 Dashboard 실행 완료` after confirming:
- 8 categories complete
- summary table complete
- canonical signal applied
- score/indicator shown
- confidence shown where applicable
- missing data marked
- Strategy mandatory fields checked
- validation status checked
- when Binance is required, its Data Mode/freshness disclosure is consistent with BINANCE_RULE
- final action evidence-backed
Otherwise use PARTIAL DATA, PARTIAL CONSENSUS or EXECUTION BLOCKED.

## 20. Dashboard Master Principle
Table First → 8 Fixed Categories → English + Korean → Canonical Signal → Score/Indicator → Confidence → Evidence → Judgment → Action.