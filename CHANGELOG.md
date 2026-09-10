# AI Market Master Change Log

## 2026-09-10 — SAI-C2 Program Flow Component Integration

### Added
- Added the second formally specified Strategy Action Index sub-component: `SAI-C2 Program Flow`.
- C2 uses:
  - Arbitrage Program net flow — supplementary/mechanical-sensitive input
  - Non-Arbitrage Program net flow — mandatory structural input
  - Total Program net flow — reconciliation/context only, not an additional numeric contribution
- Added source-data normalization to `[-1.00,+1.00]` using KOSPI total traded value as denominator.
- Added v1 C2 internal weights:
  - Arbitrage 30%
  - Non-Arbitrage 70%
- Added explicit partial formula when Arbitrage is missing: `C2 = N_NONARB / PARTIAL`.
- Added mandatory-input gate: missing Non-Arbitrage → `SAI-C2 = DATA UNAVAILABLE`.
- Added explicit C2 Conflict threshold and C2 Shock thresholds.
- Added `C2 Mechanical Event` handling for derivatives expiry, index/sector rebalance, ETF rebalance and comparable mechanical-flow events.

### Anti-double-counting / authority safeguards
- Total Program is not scored in addition to Arbitrage + Non-Arbitrage.
- E2 Program Flow remains the adaptive/qualitative interpretation owner.
- Foreign/institution investor flow remains C1/E1 and is not re-added to C2.
- Breadth/ADL remains E3; Technical remains E5; Options/OI/Volatility remains E7.
- VH/H/M/L Evidence Priority remains qualitative and is not converted into C2 numeric weights.
- C2 cannot select or reconfirm a Market Regime by itself.

### Program conflict / mechanical-flow safeguards
- Existing 3.2 rule preserved: persistent Non-Arbitrage deterioration has greater structural significance than temporary Arbitrage fluctuations.
- Strong Arbitrage buying cannot hide material Non-Arbitrage selling.
- Opposing Arbitrage and Non-Arbitrage signals remain visible through `C2 Conflict` rather than being hidden by a near-zero aggregate.
- Mechanical-event flow is calculated but cannot independently create a structural Regime conclusion.

### Scoring firewall retained
- `AI Master Score` remains `DATA UNAVAILABLE`.
- Global `Strategy Action Index` remains `DATA UNAVAILABLE`.
- C1 and C2 are component-level formulas only.
- Remaining components, global aggregation, missing/partial rules, Action Bands and validation must be completed before global SAI activation.

### Backup
- Created pre-patch checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C2_PROGRAM_FLOW_PREPATCH_BACKUP_2026-09-10.md`
- A final C2 post-integration checkpoint is created after cross-validation.

## 2026-09-10 — SAI-C1 Smart Money Component Integration

### Added
- Added the first formally specified Strategy Action Index sub-component: `SAI-C1 Smart Money`.
- C1 uses three source inputs:
  - Foreign KOSPI cash net flow
  - Foreign KOSPI200 futures net flow
  - Institutional KOSPI cash net flow
- Added source-data normalization to `[-1.00, +1.00]` using market-scale ratios rather than raw amounts.
- Added v1 C1 internal weights:
  - Foreign Cash 40%
  - Foreign Futures 40%
  - Institution Cash 20%
- Added explicit institution-missing partial formula: 50% Foreign Cash + 50% Foreign Futures.
- Added mandatory-input gate: missing Foreign Cash or Foreign Futures → `SAI-C1 = DATA UNAVAILABLE`.
- Added C1 Conflict and C1 Shock flags.
- Added normal, bearish, reversal/conflict, missing-data and extreme-flow validation cases.

### Anti-double-counting / authority safeguards
- Program / Arbitrage / Non-Arbitrage remain outside C1 under E2 ownership.
- Breadth / ADL remain outside C1 under E3 ownership.
- Options / derivatives-risk structure remain outside C1 under E7 ownership.
- Financial Investment is not separately scored when already contained in total Institution flow.
- Foreign cumulative futures position is contextual only when current futures flow is already scored.
- VH/H/M/L Evidence Priority remains qualitative and is not converted into C1 numeric weights.
- SAI-C1 does not replace `E1 Smart Money` and cannot choose or reconfirm a Market Regime by itself.

### Scoring firewall retained
- `AI Master Score` remains `DATA UNAVAILABLE`.
- Global `Strategy Action Index` remains `DATA UNAVAILABLE`.
- A defined C1 component does not activate the final global score.
- Remaining global components, aggregation, missing/partial rules, Action Bands and regression validation must be completed before final SAI activation.

### Backup
- Created pre-patch checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_PREPATCH_BACKUP_2026-09-10.md`
- Created final post-integration checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_FINAL_BACKUP_2026-09-10.md`
- Final checkpoint records the post-integration authority snapshot, C1 formula boundary, anti-double-counting safeguards, conflict/shock handling and cross-validation result.

## 2026-09-08 — Adaptive Validation & Regime Evidence Priority Integration

### Final backup checkpoint
- Created `Backup/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_FINAL_BACKUP_2026-09-08.md`.
- The checkpoint records the final six-authority rule snapshot, supporting restore/design backups, integration safeguards, scoring firewall and verification state.
- The checkpoint is non-authoritative and is intended for recovery/regression comparison only.

### Legacy restore
- Restored explicit closed-loop logic: `Change Detection → Validation → Revision → Final AI Decision`.
- Restored legacy Performance Validation / Engine Reliability concept as qualitative validation intent.
- Restored outcome-review principle when prior validated expectations and later results are actually available.
- Restored Closed-loop Learning / Self-Evolution principle without inventing undocumented historical numeric formulas.
- Added non-authoritative restore reference: `Backup/AMM_3.0_LEGACY_VALIDATION_RESTORE.md`.

### New 3.2 adaptive application
- Added official `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`.
- Added 8 Market Regimes:
  - Broad Risk-On
  - Concentrated Leadership Bull
  - Rotation
  - Distribution
  - Risk-Off Transition
  - Panic / High Volatility
  - Deep Correction / Support Test
  - Recovery / Accumulation
- Added Primary Regime + Transition Regime / Risk + Regime Confidence.
- Added E1-E8 Evidence Groups and qualitative `VH / H / M / L` Regime Adaptive Evidence Priority Matrix.
- Added Conditional Evidence Escalation, anti-double-counting, adaptive conflict resolution and Regime re-validation.
- Added qualitative Strategy postures without numeric A1-A8 labels.
- Added non-authoritative design reference: `Backup/AMM_3.2_ADAPTIVE_REGIME_DESIGN_BACKUP.md`.

### Integration safeguards
- Adaptive Validation is a cross-engine framework, not a 25th engine.
- Fixed 24-engine architecture remains unchanged.
- Fixed 8 Dashboard categories remain unchanged; no ninth adaptive category was created.
- `Market Regime` is separated from the `Portfolio Response Framework` to avoid naming collisions.
- Program/Non-arbitrage and Breadth/ADL adaptive evidence receive explicit anti-double-counting boundaries.
- Full adaptive execution uses `Preliminary Regime → Adaptive Evidence Priority → Transition/Conflict → Cross-Engine Consensus → Regime Re-validation → Validation/Revision → Final AI Decision` to prevent circular reasoning.
- Signal Count cannot override higher-quality Regime-relevant independent evidence.
- HTS/KRX remains final Korean-market confirmation.
- Binance remains a global leading/supporting layer under existing LIVE/FALLBACK/STALE rules.

### Scoring firewall
- `AI Master Score` remains `DATA UNAVAILABLE`.
- `Strategy Action Index` remains `DATA UNAVAILABLE`.
- VH/H/M/L are qualitative Evidence Priority labels only, not numeric weights.
- Prohibited conversion includes VH/H/M/L → 4/3/2/1, percentages, hidden weights or unofficial scores.
- Market Regime / Transition / qualitative Strategy posture cannot be converted into numeric scoring without future formal SCORING_RULE adoption.

### Authority architecture
Official authority is now split across six files:
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`

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
- Official five-rule architecture remained unchanged at the time of this patch; it was later expanded to six authorities by the Adaptive Validation integration above.
- No new ninth Dashboard category was created.
- Existing Validation States remain: `VERIFIED / PARTIAL / UNAVAILABLE / PARTIAL CONSENSUS / EXECUTION BLOCKED`.
- `SCORING_RULE` and `TECHNICAL_RULE` were not changed by this Binance patch.
- HTS/KRX remains the final Korean-market confirmation layer.

## 2026-09-07 — 3.2 Unified Stable

### Rule architecture optimized
- Consolidated active rule authority into five files under `Rules/` at initial Unified Stable creation.
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

### Initial Authority
Initial Unified Stable authoritative files were:
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`

## Historical
Earlier 3.2 Integrated Expansion and 3.1 history remain recoverable from Git history / legacy references.
