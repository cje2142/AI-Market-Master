# AI Market Master Dashboard 3.2

## Command Trigger Standard

### Full Dashboard Trigger

- Exact command: `AI Market Master 3.2 Dashboard 실행`
- This exact command is the official trigger for the full AI Market Master Dashboard 3.2 workflow.
- The full workflow must apply the 3.2 fixed dashboard layout, HTS Data Priority, Validation First, and Multi Engine Consensus rules.
- Similar or abbreviated phrases must not be treated as an exact trigger and must not silently execute the full Dashboard workflow.

### Binance Engine Trigger

- Exact command: `AI Market Master 3.2 Binance Engine 실행`
- This exact command is the official trigger for the Binance Engine workflow defined below.
- Similar or abbreviated phrases must not be treated as an exact trigger and must not silently execute the Binance Engine workflow.

## Fixed Dashboard Output Layout

Every exact `AI Market Master 3.2 Dashboard 실행` trigger must use the following eight categories, in exactly this order:

1. `Observation` — Market observation
2. `Evidence` — Key evidence
3. `Judgment` — Integrated market judgment
4. `AI Cycle` — AI/semiconductor cycle
5. `Smart Money` — Foreign/institutional/individual/program/derivatives flow
6. `Liquidity` — Liquidity, leverage and funding conditions
7. `Technical` — Technical analysis
8. `Strategy` — Strategy and execution

### Fixed Layout Rules

- The eight categories must never be omitted, merged, reordered, or replaced by ad-hoc sections during a full Dashboard execution.
- HTS input volume must not change the output structure. When HTS data is large, summarize and prioritize within the eight categories rather than dropping or restructuring categories.
- When a required data item is unavailable, keep the relevant category and mark the item `DATA UNAVAILABLE`; never invent or infer unavailable data as if it were observed.
- `Sector Rotation`, `Portfolio Analysis`, `Risk Assessment`, `Forecast`, `Elliott Wave`, `Fibonacci`, `Ichimoku`, and other sub-engines are subordinate analyses and must be placed inside the eight fixed categories rather than becoming additional top-level categories.
- Binance Engine results must also be mapped into the eight fixed categories. Do not create a separate ninth Binance category in the full Dashboard output.
- The final `Strategy` category must include `AI Master Score`, `Strategy Action Index`, final action, key support/resistance or decision levels when available, and the next validation conditions.
- The fixed layout applies regardless of whether the input contains a small or large amount of HTS data.

## Output Visualization and Language Standard

- The official rule names, engine names, and category identifiers remain in English for consistency and machine-readable execution.
- User-facing Dashboard output must be Korean-first. Each official English category/engine name should be accompanied by a concise Korean meaning where useful, e.g. `Observation (관찰)`, `Evidence (근거)`, `Judgment (판단)`.
- User-facing analytical labels, explanations, judgments, actions, and validation conditions should be written in Korean unless the original market/data term is conventionally expressed in English.
- Use a consistent signal-marker system throughout the Dashboard:
  - `🟢` Positive / Bullish — 긍정·강세
  - `🟡` Neutral — 중립
  - `🟠` Caution — 주의
  - `🔴` Negative / Bearish — 부정·약세
  - `⚪` DATA UNAVAILABLE — 데이터 없음
- Signal markers are presentation labels only unless a separate scoring rule explicitly defines their calculation. Do not invent numerical thresholds merely from the presence of a marker.
- Each of the eight top-level categories should present, when applicable, the following compact order: `상태(Signal) → Score/지표(available data only) → 핵심 근거 → 판단`. If a category has no defined numerical score, do not fabricate one; use the signal marker and qualitative judgment instead.
- `AI Master Score` and `Strategy Action Index` must be displayed with their official English names plus Korean descriptions, e.g. `AI Master Score (AI 종합점수)` and `Strategy Action Index (전략 실행지수)`.
- Numerical scoring must follow the definitions established elsewhere in the 3.2 rules. This visualization rule does not create new scoring formulas or score bands.
- The final Strategy section must keep the same signal, score, action, decision levels, and next-validation presentation order on every full Dashboard execution.
- The visualization standard must remain unchanged regardless of HTS input volume.

## Binance Engine Execution Standard

- `AI Market Master 3.2 Binance Engine 실행`은 지정된 8개 대표종목 전체를 기본 분석한다.
- 대표종목: EWYUSDT / SAMSUNGUSDT / SKHYNIXUSDT / SOXLUSDT / QQQUSDT / SPYUSDT / TMFUSDT / BTCUSDT
- 각 종목은 가능한 범위에서 Price, OHLCV, Volume, OI, Funding, Long/Short, Top Trader, Premium, Order Book, Recent Trades, ADL Risk를 확인한다.
- 종목별 분석 → Global Leading Consensus → 국내시장/HTS 교차검증 순서로 판단한다.
- 특정 종목을 명시한 경우에만 단일종목 분석으로 전환한다.
- 데이터가 없는 항목은 추정하지 않고 `DATA UNAVAILABLE`로 표시한다.
- 일부 종목만 조회된 경우 `PARTIAL CONSENSUS`로 명시한다.
- 최종 판단은 AI Master Score와 Strategy Action Index에 반영한다.

## Execution Integrity Patch v1.0

The full Dashboard workflow is additionally governed by `AI_MARKET_MASTER_3.2_EXECUTION_INTEGRITY_PATCH_v1.0.md` (Patch ID: `3.2-EIP-v1.0`).

### Mandatory Preflight Gate

Before generating a full Dashboard, validate the exact trigger, HTS input, mandatory engines, Binance Engine when required, scoring inputs, and each required component status. Use `VERIFIED`, `PARTIAL`, or `UNAVAILABLE` status. If a mandatory preflight check fails, do not claim normal completion; use `EXECUTION BLOCKED` or the applicable partial status.

### Binance Mandatory Gate

For a full Dashboard using the Binance Global Futures Layer, all eight fixed watchlist symbols must be checked: `EWYUSDT / SAMSUNGUSDT / SKHYNIXUSDT / SOXLUSDT / QQQUSDT / SPYUSDT / TMFUSDT / BTCUSDT`.

- 8/8 successfully queried at the required minimum level → `BINANCE ENGINE VERIFIED`
- 1–7/8 successfully queried → `PARTIAL CONSENSUS` and list missing symbols
- 0/8 successfully queried → `BINANCE DATA UNAVAILABLE`

A single successfully queried symbol never constitutes full Binance Engine completion.

### Engine Completion Gate

Eight output categories alone do not establish completion. Before declaring completion, validate required engine execution, evidence, cross-engine consensus inputs, Binance status when required, scoring inputs, and final validation status.

### AI Master Score Anti-Hallucination Gate

Numeric `AI Master Score` output is permitted only when the official 3.2 scoring definition applies, all mandatory inputs are available or explicitly allowed as partial, the calculation is actually performed, and the result passes validation. Otherwise output `AI Master Score: DATA UNAVAILABLE` or an explicitly permitted partial status. Never substitute an analyst-created percentage.

### Strategy Action Index Gate

`Strategy Action Index` follows the same validation requirement. If its official calculation cannot be performed from validated inputs, output `Strategy Action Index: DATA UNAVAILABLE`. Qualitative strategy may continue only where existing 3.2 rules permit it; qualitative judgment must never be converted into an invented numeric index.

### Completion Declaration Rule

The assistant may state `AI Market Master 3.2 Dashboard 실행 완료` only after the eight categories, required HTS data, required engines, Binance status when required, AI Master Score status, Strategy Action Index status, unavailable/partial inputs, and evidence-backed final Action have all passed final validation.

Otherwise use `EXECUTION BLOCKED`, `PARTIAL DATA`, or `PARTIAL CONSENSUS` as applicable.

### Regression Protection

Minimum regression checks for every future 3.2 Dashboard execution:
1. HTS-only input with Binance required → no full completion without Binance validation.
2. One Binance symbol available → `PARTIAL CONSENSUS`, never full Binance completion.
3. Incomplete score inputs → numeric AI Master Score prohibited.
4. Incomplete strategy-index inputs → numeric Strategy Action Index prohibited.
5. Missing data → `DATA UNAVAILABLE`, never invented values.
6. Complete validated inputs → normal Dashboard completion permitted.

This patch changes execution integrity only; the fixed eight-category output layout remains unchanged.
