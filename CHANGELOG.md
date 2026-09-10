# AI Market Master Change Log

## 2026-09-10 — SAI-C8 Global Leading Component Integration

### Added
- Added the eighth formally specified Strategy Action Index sub-component: `SAI-C8 Global Leading`.
- Added five numeric axes:
  - Global Equity Risk `GR` 30% — SPY + QQQ composite
  - Korea Leading `KR` 25% — EWY
  - Semiconductor Risk `SEMI` 20% — SOXL
  - Global Rate/Liquidity `GLIQ` 15% — TMF
  - Crypto Risk `CRYPTO` 10% — BTC
- Added full formula: `SAI-C8 = 0.30*GR + 0.25*KR + 0.20*SEMI + 0.15*GLIQ + 0.10*CRYPTO`.
- Added explicit v1 normalization boundaries for SPY, QQQ, EWY, SOXL, TMF and BTC.
- Added aligned-observation-window and query-time validation.

### Optimization / safeguards
- SPY and QQQ are compressed into one GR composite instead of being counted as two independent Evidence Groups.
- SAMSUNGUSDT and SKHYNIXUSDT remain G2/G3 Korea/Semiconductor confirmation only and are not added as extra numeric axes after EWY/SOXL.
- OI, Funding, Long/Short, Premium, ADL risk, order book and recent trades remain G6 positioning/crowding context rather than additional numeric C8 terms.
- BTC is retained as a high-beta auxiliary proxy with the smallest fixed internal C8 weight of 10%.
- TMF remains E8 global rates/liquidity proxy; C6 Korea Treasury 3Y remains domestic financial-condition input.
- C8 axes remain one E8 evidence family and are not counted as five independent Evidence Groups.

### Freshness / missing-data safeguards
- LIVE Binance data is eligible for normal numeric C8 use.
- Valid FALLBACK inside BINANCE_RULE TTL may be used but caps C8 status at PARTIAL and preserves the Confidence downgrade.
- STALE Binance data is prohibited from numeric C8 input.
- Predefined PARTIAL formula renormalizes only explicitly valid axes and is allowed only when GR exists, at least 3/5 axes exist and original fixed-weight coverage is at least 60%.
- If GR uses only SPY or only QQQ, overall C8 is PARTIAL.
- GR missing, fewer than 3 axes, <60% coverage or STALE-only completion makes C8 DATA UNAVAILABLE.

### Conflict / shock safeguards
- Added `C8 Conflict: ACTIVE` for material GR-vs-KR or GR-vs-SEMI disagreement.
- Added Korea/Semiconductor confirmation-conflict flags when EWY/SOXL materially disagree with both available Samsung/SK hynix confirmation signals.
- Added `C8 Shock: ACTIVE` for aligned extreme GR/KR/SEMI moves or comparable extreme global-leading movement with independent G6 confirmation.
- Conflict/Shock feed Change Detection / Transition / Regime re-validation only and do not automatically change Regime, global SAI, portfolio action or permanent Base Weight.

### Scoring firewall retained
- `AI Master Score` remains `DATA UNAVAILABLE`.
- Global `Strategy Action Index` remains `DATA UNAVAILABLE`.
- C1-C8 now cover E1-E8 as component-level formulas only.
- Global aggregation, C1-C8 global Base Weights, global missing/partial handling, any Conditional Numeric Weight logic, final range/Action Bands and regression validation remain required before global SAI activation.

### Backup
- Pre-patch checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C8_GLOBAL_LEADING_PREPATCH_BACKUP_2026-09-10.md`
- Final post-integration checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C8_GLOBAL_LEADING_FINAL_BACKUP_2026-09-10.md`
- Final checkpoint blob SHA: `c40b37ffba7d025a7ed9e2711d7f9a4a6009a4a6`.
- Final checkpoint records the post-integration six-authority snapshot, five-axis 30/25/20/15/10 formula, aligned-window normalization, LIVE/FALLBACK/STALE firewall, GR-mandatory 3-axis/60% PARTIAL gate, Samsung/SK hynix and G6 context-only boundaries, conflict/shock safeguards, anti-double-counting, anti-circularity and final cross-authority verification.

## 2026-09-10 — SAI-C7 Volatility / Derivatives Risk Component Integration
- Added `SAI-C7 Volatility / Derivatives Risk`.
- Formula: `0.60*VOL + 0.40*BASIS`.
- VKOSPI mandatory; fair-value-adjusted Basis optional; VOL-only predefined PARTIAL.
- OI/PCR/volatility-futures remain contextual; added Conflict/Shock/Mechanical Event safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C7_VOLATILITY_DERIVATIVES_FINAL_BACKUP_2026-09-10.md`.
- Final checkpoint blob SHA: `3f9ee5985a46dbb3e2f2bd8b7c714b20e67f2bd6`.

## 2026-09-10 — SAI-C6 Liquidity / Macro Component Integration
- Added `SAI-C6 Liquidity / Macro`.
- Formula: `0.35*FX + 0.35*RATE + 0.30*CASH`.
- Added point-in-time/freshness, predefined PARTIAL, Margin Credit context-only, Policy Rate/M2 structural-context, Conflict/Shock and anti-double-counting safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C6_LIQUIDITY_MACRO_FINAL_BACKUP_2026-09-10.md`.
- Final checkpoint blob SHA: `3dd78dd160eb49e7cee0ad8bde97f2b31fc2ef48`.

## 2026-09-10 — SAI-C5 Technical Structure Component Integration
- Added `SAI-C5 Technical Structure`.
- Formula: `0.50*PS + 0.30*SR + 0.20*TP`.
- Official timeframe: KOSPI Daily / Closing-confirmed.
- PS mandatory; predefined SR/TP missing PARTIAL formulas.
- Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci remain confirmation/context, not additional numeric C5 terms.
- Added C5 Conflict/Divergence/Shock, anti-double-counting, anti-circularity and Intraday Preview safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C5_TECHNICAL_STRUCTURE_FINAL_BACKUP_2026-09-10.md`.

## 2026-09-10 — SAI-C4 Sector / Leadership Component Integration
- Added `SAI-C4 Sector / Leadership` with fixed eight-benchmark universe.
- Formula: `0.60*SD + 0.40*RL`.
- 8/8 eligible VERIFIED, 6-7/8 PARTIAL, <6/8 DATA UNAVAILABLE.
- Leadership Concentration remains qualitative/contextual under E4.
- Added C4 Conflict/Shock and anti-double-counting/anti-circularity safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C4_SECTOR_LEADERSHIP_FINAL_BACKUP_2026-09-10.md`.

## 2026-09-10 — SAI-C3 Breadth / Market Internal Component Integration
- Added `SAI-C3 Breadth / Market Internal`.
- Formula: `0.70*N_K + 0.30*N_Q` with KOSPI breadth mandatory and KOSDAQ supplementary.
- KOSDAQ missing permits KOSPI-only PARTIAL; KOSPI missing makes C3 DATA UNAVAILABLE.
- Raw ADL remains contextual in v1.
- Added Cross-Market Conflict, Index/Breadth Divergence and Shock safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C3_BREADTH_INTERNAL_FINAL_BACKUP_2026-09-10.md`.

## 2026-09-10 — SAI-C2 Program Flow Component Integration
- Added `SAI-C2 Program Flow`.
- Formula: `0.30*N_ARB + 0.70*N_NONARB`.
- Non-Arbitrage is structural core; Arbitrage missing permits predefined PARTIAL, Non-Arbitrage missing makes C2 DATA UNAVAILABLE.
- Total Program is reconciliation/context only.
- Added Conflict/Shock/Mechanical Event safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C2_PROGRAM_FLOW_FINAL_BACKUP_2026-09-10.md`.

## 2026-09-10 — SAI-C1 Smart Money Component Integration
- Added `SAI-C1 Smart Money`.
- Formula: `0.40*N_FC + 0.40*N_FF + 0.20*N_IC`.
- Foreign Cash and Foreign Futures are mandatory; institution missing permits predefined 50/50 PARTIAL.
- Added Conflict/Shock and anti-double-counting safeguards.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_FINAL_BACKUP_2026-09-10.md`.

## 2026-09-08 — Adaptive Validation & Regime Evidence Priority Integration
- Restored Change Detection → Validation → Revision → Final AI Decision closed-loop behavior.
- Added six-authority architecture with `AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`.
- Added 8 Market Regimes, E1-E8 Evidence Groups, VH/H/M/L qualitative Evidence Priority Matrix, Transition framework, conflict resolution, anti-double-counting and Regime re-validation.
- Adaptive Validation remains cross-engine, not a 25th engine.
- Global numeric scoring remains disabled until SCORING_RULE activation gate is complete.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_FINAL_BACKUP_2026-09-08.md`.

## 2026-09-08 — Binance Latest Re-query & Fallback Policy
- Added mandatory fresh re-query attempt before prior Binance reuse in Full Dashboard.
- Added LIVE/FALLBACK/STALE Data Modes, freshness windows, fallback confidence downgrade and stale-data restrictions.
- HTS/KRX remains final Korean-market confirmation.

## 2026-09-07 — 3.2 Unified Stable
- Consolidated authority into dedicated rule files, preserving 24 internal engines and fixed 8 Dashboard categories.
- Retained Dynamic KOSPI Zone, Smart Money Action Matrix, Portfolio Sell Priority, Intraday 24→16→17, dual-axis Elliott/Fibonacci and anti-hallucination gates.
- Numeric global AI Master Score / Strategy Action Index remained DATA UNAVAILABLE pending reproducible formal formulas.

## Historical
Earlier 3.2 Integrated Expansion and 3.1 history remain recoverable through Git history / legacy references.