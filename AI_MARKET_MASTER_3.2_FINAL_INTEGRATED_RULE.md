# AI Market Master 3.2 Final Integrated Rule

Version: 3.2 Integrated Expansion
Status: Extension Layer

## Rule Authority / Single Source of Truth

This document is the master interpretation and integration layer for AI Market Master 3.2.

Rule authority is separated by function so future verification does not rely on ambiguous file precedence:

1. **Stable / engine-specific rules** control their own formal formulas, thresholds, indicator definitions, and technical calculations.
2. **Final Integrated Rule (this file)** controls cross-engine interpretation, integration, strategy vocabulary, and overall rule hierarchy.
3. **Dashboard 3.2 rule** controls the exact command triggers and the fixed eight-category user-facing output layout.
4. **Execution Integrity Patch** controls mandatory execution-safety and validation gates. It may block or downgrade execution status but does not create or alter market-scoring formulas.
5. No lower-level rule may silently override a higher-authority rule outside its defined scope.
6. If two rules conflict, the conflict must be identified explicitly and resolved according to the functional authority above; no silent rule creation or silent conflict resolution is permitted.

For future rule verification, the required interpretation chain is:
`Trigger → Preflight → Applicable Engine/Formula Rules → Binance Validation → Evidence → Cross-Engine Consensus → Score → Strategy → Final Validation → Completion`

## Core Principles
- HTS Data Priority
- Evidence Based Decision
- Reliability > Speed
- Validation First
- Multi Engine Consensus

## Architecture
- Existing 24 Engine Architecture is maintained.
- Existing 8 Core Dashboard output structure is maintained.

## Standard Output Rule
All engine outputs follow:

Signal -> Score/Indicator -> Evidence -> Judgment -> Action

## Canonical Signal System

The canonical user-facing 3.2 signal vocabulary is:
- 🟢 Strong Bull / Positive — 강한 긍정·강세
- 🔵 Bull — 긍정·강세
- 🟡 Neutral — 중립
- 🟠 Warning / Caution — 경고·주의
- 🔴 Bear / Negative — 부정·약세
- ⚫ Extreme Risk — 극단적 위험
- ⚪ DATA UNAVAILABLE — 데이터 없음

Engine-specific or legacy signal labels must be normalized to this canonical system at Dashboard presentation. Signal markers remain presentation labels unless a separate scoring rule explicitly defines their calculation. A signal marker never creates a numeric threshold or score by itself.

## Smart Money Enhancement
Detailed analysis includes:
- Foreign cash
- Foreign futures
- Institutions
- Financial investment
- Program trading
- Arbitrage / Non-arbitrage
- Options flow

Analysis flow:
Data -> Meaning -> Market Impact -> Strategy

## Technical Enhancement
Detailed:
- Elliott Wave
- Fibonacci

Compact indicators:
- RSI
- MACD
- Ichimoku
- Moving Average
- VWAP
- ADX
- ADL

Reference values:
- Major Low: 2293
- Major High: 9114
- Correction Low: 5593

## Portfolio Strategy Enhancement
Portfolio analysis includes:
- Position assessment
- Risk display
- Executable Action
- Evidence-based reasoning

## Action Vocabulary
BUY:
- 적극매수
- 분할매수
- 추가매수

HOLD:
- 보유
- 핵심보유

REDUCE:
- 점진적 비중축소
- 비중축소
- 분할매도

SELL:
- 매도
- 적극매도
- 전량매도

CASH:
- 현금대기
- 현금확보

## Score Authority
`AI Master Score` and `Strategy Action Index` formulas are authoritative only where defined by the applicable Stable/engine-specific 3.2 scoring rules. This document does not create, replace, or infer those formulas.

Numeric output is permitted only after the applicable scoring rule is identified, required inputs are validated, calculation is performed, and execution-integrity checks pass.

## Action Evidence Rule
Every final Action must include supporting evidence.

## Dashboard / Execution Rule References
`AI_MARKET_MASTER_DASHBOARD_3.2.md` is authoritative for exact Dashboard/Binance command triggers and the fixed eight-category presentation layout.

`AI_MARKET_MASTER_3.2_EXECUTION_INTEGRITY_PATCH_v1.0.md` is authoritative for execution-safety gates, validation states, and completion declaration checks within its defined scope.

## Execution Integrity Patch
`AI_MARKET_MASTER_3.2_EXECUTION_INTEGRITY_PATCH_v1.0.md` is an extension/patch layer for execution safety.

It adds mandatory:
- Preflight validation before full Dashboard generation.
- Full Binance 8-symbol completion checks when Binance is required.
- Engine completion validation.
- AI Master Score anti-hallucination/calculation gate.
- Strategy Action Index anti-hallucination/calculation gate.
- Explicit `VERIFIED`, `PARTIAL`, `UNAVAILABLE`, `PARTIAL CONSENSUS`, and `EXECUTION BLOCKED` states.
- Final completion declaration validation.

The patch does not create or alter scoring formulas. Numeric scores may only be shown when their official 3.2 definitions and validated inputs permit calculation.

## Priority Rule
Existing AI Market Master 3.2 Stable/engine-specific rules retain authority over their own formulas and technical definitions.
This Final Integrated Rule is the master integration and interpretation layer.
The Dashboard file controls trigger and fixed presentation layout.
The Execution Integrity Patch controls execution-safety gates.
No rule may silently override another rule outside its defined authority.
