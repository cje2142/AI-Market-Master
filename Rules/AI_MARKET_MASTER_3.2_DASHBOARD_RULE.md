# AI Market Master 3.2 Dashboard Rule

Version: 3.2 Unified Stable
Status: Dashboard Presentation Authority

## 1. Scope
This file controls only exact triggers and user-facing output layout. Market Regime/adaptive evidence logic, market formulas, technical calculations, Binance interpretation/freshness and scoring belong to their dedicated rules.

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

Never omit, merge, reorder or replace these categories. Scenario, Portfolio, Global Leading, Adaptive Validation and other sub-engines/frameworks must be mapped inside them, not added as ninth-level categories.

## 4. 24 Engine / Adaptive Framework → 8 Category Mapping
- Observation: Executive Summary, Observation, Leading Indicator, Global Market, Breadth summary, relevant Intraday summary.
- Evidence: Evidence, Program Trading, derivatives evidence, Change Detection, Data Validation, Evidence Priority summary, material evidence conflict.
- Judgment: Cross-Engine Consensus, Scenario Forecast, Risk Assessment sub-analysis, Primary Market Regime, Transition Regime/Risk, Regime Confidence, Regime re-validation result.
- AI Cycle: AI Cycle, semiconductor/HBM/DRAM/NAND, CAPEX, supply/inventory/demand, semiconductor relative strength and regime-relevant leadership evidence.
- Smart Money: foreign cash/futures, institutions, financial investment and Smart Money directional interpretation. Program may be discussed but is not double-counted as independent Smart Money confirmation under ADAPTIVE_VALIDATION_RULE.
- Liquidity: Global Liquidity, rates, FX, deposits, credit/margin, Fed/M2/TGA/RRP when available, TMF support, relevant risk/liquidity escalation.
- Technical: Technical Analysis, Elliott, Fibonacci, RSI, MACD, Ichimoku, MA, VWAP, ADX, support/resistance, price-structure confirmation/invalidation. ADL/Breadth may be referenced technically but adaptive confirmation ownership is E3 under ADAPTIVE_VALIDATION_RULE.
- Strategy: Portfolio, Strategy, Dynamic KOSPI Zone, Portfolio Risk Priority, Scenario implication, qualitative Strategy posture, Validation, Revision, Final AI Decision, Dashboard Checklist.

The 24 engines are internal analysis; the 8 categories are presentation. ADAPTIVE_VALIDATION_RULE is a cross-engine framework, not a ninth category or 25th engine.

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

Market Regime labels and qualitative Strategy postures are also separate from Validation Status.

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
Use an official score only when SCORING_RULE permits it. Otherwise show verified indicators such as foreign spot/futures, Program flow, Breadth, RSI, MACD, ADX, funding, OI, deposits, credit, support/resistance and qualitative Evidence Priority.

Never invent 83 points, 72%, 8.4/10 or similar unofficial numbers.
VH/H/M/L Evidence Priority is allowed as a qualitative Indicator only and must not be displayed as a numeric weight or score.

## 11. Confidence
Use:
- High — 높음
- Medium — 중간
- Low — 낮음

Confidence reflects completeness, source reliability, freshness, engine agreement, signal conflict and validation status. It is not a probability or market score.

Regime Confidence may also use High / Medium / Low and must remain non-numeric.
If Binance FALLBACK is used, apply the Confidence downgrade defined by BINANCE_RULE. Dashboard presentation must not hide that downgrade.

## 12. Missing Data
Never delete a required category because data is missing. Mark the relevant item `DATA UNAVAILABLE`; for partial retrieval use PARTIAL or PARTIAL CONSENSUS as applicable. Never estimate missing values.

If available data cannot support a reliable Market Regime, explicitly mark Regime status as DATA UNAVAILABLE / PARTIAL rather than force a classification.

## 13. Evidence / Judgment / Action
Evidence should prioritize HTS/KRX, verified official data, then verified Binance supporting data.
Judgment must reflect cross-engine consensus, current Market Regime/Transition when valid, and explicitly state material conflicts.
Action must use the MASTER_RULE vocabulary and include evidence/conditions.

Signal Count alone must not override Regime-relevant high-priority independent evidence.
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
12. Primary Market Regime when validated
13. Transition Regime / Transition Risk when material
14. Qualitative Strategy Posture when applicable

If official scores cannot be calculated, display `DATA UNAVAILABLE` rather than inventing numbers.
Qualitative Strategy posture must not be represented as a numeric Strategy Action Index.

## 15. Adaptive Validation Presentation
When sufficient data exists, present compactly inside existing categories:
- `Primary Market Regime`
- `Transition Regime / Risk`
- `Regime Confidence`
- `Evidence Priority` — only the most decision-relevant VH/H groups need be shown
- `Material Conflict`
- `Regime Re-validation`
- `Revision Status`

Do not dump the full E1-E8 matrix unless it materially helps the user or the user asks for full detail.

Recommended compact form:
`Primary Regime: Concentrated Leadership Bull / Transition Risk: Distribution / Confidence: Medium`
`Priority Evidence: Smart Money VH, Breadth VH, Sector VH, Technical H`
`Conflict: Flow Bull vs Breadth Warning`
`Re-validation: Regime Maintained with Warning`

## 16. Portfolio / Scenario / Binance Placement
- Portfolio actions belong mainly in Strategy.
- Scenarios belong mainly in Judgment/Strategy and do not become a ninth category.
- Adaptive Validation belongs mainly in Evidence/Judgment/Strategy.
- Binance results must be mapped into the existing 8 categories: global risk into Observation/Judgment, semiconductor signals into AI Cycle, TMF/rates into Liquidity, positioning evidence into Evidence/Smart Money/Judgment, final consensus into Strategy.

## 17. Binance Status Presentation
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

## 18. Technical Presentation
Technical should show, when available: Trend, Elliott, Dual Fibonacci, Dynamic Fibonacci if relevant, RSI, MACD, Ichimoku, MA/VWAP, ADX, ADL/Breadth reference, Volume, Support, Resistance, Confirmation and Invalidation.

For adaptive confirmation, Breadth/ADL belongs to the E3 Evidence Group and must not be double-counted as a second independent Technical confirmation.

## 19. Density Rule
Large HTS input does not change the 8-category structure. Remove duplicated raw data, prioritize decision-relevant evidence and avoid repeating the same conclusion across categories.

Adaptive presentation should normally show only Primary Regime, material Transition, highest-priority evidence and unresolved conflict rather than all internal calculations.

## 20. Completion Declaration
Only declare `AI Market Master 3.2 Dashboard 실행 완료` after confirming:
- 8 categories complete
- summary table complete
- canonical signal applied
- score/indicator shown
- confidence shown where applicable
- missing data marked
- Strategy mandatory fields checked
- validation status checked
- Market Regime/Transition status validated or explicitly partial/unavailable
- Evidence Priority is qualitative only
- adaptive evidence was not double-counted
- material high-priority conflicts were disclosed/resolved
- Regime re-validation completed when Full adaptive analysis is used
- when Binance is required, its Data Mode/freshness disclosure is consistent with BINANCE_RULE
- final action evidence-backed

Otherwise use PARTIAL DATA, PARTIAL CONSENSUS or EXECUTION BLOCKED.

## 21. Dashboard Master Principle
Table First → 8 Fixed Categories → English + Korean → Canonical Signal → Score/Indicator → Confidence → Evidence → Market Regime / Transition → Judgment → Action.
