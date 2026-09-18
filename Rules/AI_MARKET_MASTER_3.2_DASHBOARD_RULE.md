# AI Market Master 3.2 Dashboard Rule

Version: 3.2 Unified Stable
Status: Dashboard Presentation Authority

## 1. Scope
This file controls only exact triggers and user-facing output layout. Market Regime/adaptive evidence logic, market formulas, technical calculations, Binance interpretation/freshness and scoring belong to their dedicated rules.

## 2. Exact Triggers
Full Dashboard: `AI Market Master 3.2 Dashboard 실행`
Binance Engine: `AI Market Master 3.2 Binance Engine 실행`
Similar or abbreviated phrases must not silently trigger the full workflows.

## 2A. Full Dashboard Execution Priority Hard Gate
When the exact Full Dashboard trigger is recognized, initialize the presentation structure before analytical execution.

Required sequence:
1. Confirm the exact Full Dashboard trigger.
2. Reserve the fixed 8-category Dashboard skeleton in the required order.
3. Execute the existing MASTER_RULE analytical chain without changing its calculation or validation order.
4. Map validated C1-C8/Strategy Action Index, Market Regime/Transition/Conflict, technical, Binance and portfolio results into the reserved categories.
5. Run the Completion Hard Gate before declaring completion.

`Reserve the Dashboard skeleton` means presentation initialization only. It does not mean outputting conclusions before analysis, and it must not move SCORING, ADAPTIVE, TECHNICAL or BINANCE calculations ahead of their owning-rule sequence.

Once initialized, the Full Dashboard may not switch to a free-form scoring-first response. Detailed calculations may be shown only after the mandatory summary table and fixed category structure are preserved.

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

`AI Master Score` must remain `DATA UNAVAILABLE — 공식 산식 미정의` until SCORING_RULE formally activates a reproducible formula. It must not be inferred from Strategy Action Index, Market Regime, signal counts, VH/H/M/L or qualitative Strategy posture.

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

## 20. Completion Declaration / Hard Gate
Only declare `AI Market Master 3.2 Dashboard 실행 완료` after confirming all of the following:
- presentation initialization preserved the fixed 8-category skeleton
- summary table contains all 8 categories in the official order
- all 8 detailed categories are present; none are omitted, merged, replaced or promoted to a ninth category
- canonical signal applied
- score/indicator status shown
- `AI Master Score` is shown as `DATA UNAVAILABLE — 공식 산식 미정의` unless SCORING_RULE is formally changed
- Strategy Action Index status is shown and numeric output appears only when SCORING_RULE runtime gates permit it
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
- final portfolio action is present when supported, or explicitly blocked/unavailable when required inputs are insufficient
- final action evidence-backed

If any required item fails, do not declare normal completion. Use PARTIAL DATA, PARTIAL CONSENSUS or EXECUTION BLOCKED as applicable and identify the failed gate.


## 20A. Data Efficiency Prospective Runtime Sidecar
When the exact Full Dashboard trigger is executed and the Data Efficiency research sidecar is available, the completed Dashboard result should also emit one machine-readable research snapshot to the Data Efficiency runtime ingestion path.

This sidecar is operational telemetry only. It is not a seventh Authority file, ninth Dashboard category, 25th engine, scoring override, Regime override or portfolio-action override.

Required boundaries:
- Official C1-C8, official Strategy Action Index, Regime/Transition and portfolio decision are finalized first under their owning rules.
- The sidecar runs only after the Official Dashboard result exists.
- It must never modify the user-facing 8-category Dashboard.
- Sidecar failure, missing GitHub write access or missing Candidate-only inputs must not alter Official Dashboard completion status.
- Missing Candidate inputs remain PARTIAL / DATA UNAVAILABLE; never infer or estimate them.
- Data Efficiency Candidate v0.1 remains research-only and must not feed back into Official 3.2 decisions during prospective validation.
- If a valid prospective snapshot is available, write it to `Research/runtime/de_inbox/*.json`; the repository ingestion workflow appends the comparison to `Research/runtime/data_efficiency_runtime_comparator_v0_3.jsonl`.
- Duplicate sample identities are skipped rather than silently rewritten.
- Correction or metadata-only payloads are not prospective samples and must not be written as ordinary inbox snapshots.

### 20A-1. Canonical Sidecar Schema — REQUIRED
New Full Dashboard sidecars MUST use these exact top-level field names:

```json
{
  "sample_id": "AMM32-DE-YYYYMMDD-CHECKPOINT",
  "market_date": "YYYY-MM-DD",
  "timestamp": "ISO-8601 with timezone",
  "session_checkpoint": "checkpoint label",
  "official": {
    "C1": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C2": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C3": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C4": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C5": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C6": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C7": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "C8": {"status": "VERIFIED|PARTIAL|DATA UNAVAILABLE", "value": 0.0},
    "SAI": 0.0
  },
  "official_regime": "validated Regime / Transition label",
  "de_raw": {
    "r_kospi": 0.0,
    "r_kosdaq": 0.0,
    "r_kospi200": 0.0,
    "r_krx100": 0.0,
    "r_usdkrw": 0.0,
    "d_ktb3y_bp": 0.0
  },
  "C8_effect": null,
  "notes": []
}
```

Canonical unit rules:
- `r_kospi`, `r_kosdaq`, `r_kospi200`, `r_krx100`, `r_usdkrw` are decimal returns, not percent numbers. Example: +2.66% → `0.0266`.
- `d_ktb3y_bp` remains basis points. Example: +1 bp → `1.0`.
- Missing raw values must be `null`; never estimated.
- Intraday C5 must preserve `PARTIAL`/Preview semantics when closing confirmation is unavailable.
- Post-close C5 may be `VERIFIED` only after the closing technical inputs are validated.
- `official.SAI` stores the numeric Official value only; Official validation/execution meaning remains determined by the C1-C8 statuses and SCORING_RULE gates.

The following legacy aliases MUST NOT be emitted by new Dashboard sidecars:
- `strategy_action_index` in place of `official.SAI`
- `regime` in place of `official_regime`
- `candidate_raw_inputs` in place of `de_raw`
- percent-valued raw keys such as `KOSPI_return_pct`, `USDKRW_return_pct`

### 20A-2. Compatibility / Ingestion Safety
The DE bridge may normalize historical legacy aliases into the canonical schema for backward compatibility. This compatibility layer is defensive only and does not authorize new Dashboard executions to emit the legacy schema.

If an inbox JSON contains `correction_of` or is otherwise a correction/metadata-only payload, the inbox processor must skip it as a non-sample rather than aborting ingestion.

The sidecar is intentionally non-blocking so the Official Dashboard remains usable even when research logging infrastructure is unavailable.

## 21. Dashboard Master Principle
Exact Trigger → Presentation Initialization → Table First → 8 Fixed Categories → Official Analysis/Validation Chain → Category Mapping → Completion Hard Gate.

Within the completed Dashboard presentation: English + Korean → Canonical Signal → Score/Indicator → Confidence → Evidence → Market Regime / Transition → Judgment → Action.
