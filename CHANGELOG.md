# AI Market Master Change Log

## 2026-09-08 — Binance Latest Re-query & Fallback Policy

### Added
- Full Dashboard now requires a fresh Binance 8-symbol re-query attempt before any prior Binance result may be reused.
- Added Binance Data Mode: `LIVE / FALLBACK / STALE`, kept separate from official Validation Status.
- Added fallback freshness windows:
  - Intraday: prior validated Binance data may be reused for up to 60 minutes.
  - Post-close structural analysis: prior validated Binance data may be reused for up to 2 hours.
- FALLBACK requires a known prior query time, known prior Validation Status and preserved symbol/field-depth status.
- FALLBACK lowers Binance-related Confidence by at least one level.
- STALE data is historical/context-only and cannot be the primary basis for current aggressive portfolio action, leverage expansion or numeric score inputs.
- Dashboard now discloses Binance Data Mode, data age, prior query time/status, symbol availability, field depth and Confidence when applicable.
- MASTER Completion Gate now verifies latest re-query attempt, fallback freshness, Confidence downgrade and stale-data restrictions.

### Compatibility / No structural change
- Official five-rule architecture remains unchanged.
- No new ninth Dashboard category was created.
- Existing Validation States remain: `VERIFIED / PARTIAL / UNAVAILABLE / PARTIAL CONSENSUS / EXECUTION BLOCKED`.
- `SCORING_RULE` and `TECHNICAL_RULE` were not changed.
- HTS/KRX remains the final Korean-market confirmation layer.

## 2026-09-07 — 3.2 Unified Stable

### Rule architecture optimized
- Consolidated active rule authority into five files under `Rules/`.
- Removed duplicate/overlapping 3.2 authority from root, Extensions and old execution-flow files.
- Added `Legacy/3.2-history/INDEX.md` with exact historical blob SHAs for recovery.

### Restored legacy-compatible rules
- Table First layout
- English + Korean presentation
- Confidence
- Intraday `24 → 16 → 17`
- Full-dashboard restriction for ordinary intraday input
- Dynamic KOSPI Strategy Zone
- Smart Money Action Matrix
- Portfolio Sell Priority

### Preserved 3.2 improvements
- 24 internal Analysis Engines
- 8 fixed Dashboard categories
- HTS/KRX final confirmation
- Binance 8-symbol global-leading layer
- G1-G6 sub-engines
- Dual-axis Elliott/Fibonacci
- Execution Integrity / completion gates
- DATA UNAVAILABLE anti-hallucination behavior

### Scoring correction
No complete reproducible legacy formula for `AI Master Score` or `Strategy Action Index` has yet been verified. Numeric scoring remains disabled and must output `DATA UNAVAILABLE` until a formal formula is verified and adopted in `SCORING_RULE`.

### Authority
Current authoritative files:
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`

## Historical
Earlier 3.2 Integrated Expansion and 3.1 history remain recoverable from Git history / legacy references.