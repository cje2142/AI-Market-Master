# AI Market Master Change Log

## 2026-09-10 — SAI-C6 Liquidity / Macro Component Integration

### Added
- Added the sixth formally specified Strategy Action Index sub-component: `SAI-C6 Liquidity / Macro`.
- Added three numeric axes:
  - FX Pressure 35% — USD/KRW 5-observation change, direction inverted for KRW financial-condition interpretation.
  - Domestic Rate Pressure 35% — Korea Treasury 3Y 5-observation change in basis points.
  - Cash Liquidity 30% — Customer Deposits 5-observation percentage change.
- Added full formula: `SAI-C6 = 0.35*FX + 0.35*RATE + 0.30*CASH`.
- Added completed-daily / point-in-time source rules and explicit Customer Deposits observation-date disclosure.
- Added predefined PARTIAL formulas when one of the three axes is unavailable, with a minimum two-axis gate and at least one of FX or RATE required.

### Optimization / safeguards
- Margin Credit is not a direct numeric C6 term because rising credit can represent both liquidity expansion and leverage fragility; it remains qualitative E6/E7 context.
- Policy Rate, M2 and lower-frequency macro series remain Structural Macro Context rather than being mixed directly into the daily score.
- Absolute USD/KRW, yield and deposit levels remain context; v1 numeric scoring uses changes rather than fixed long-run levels.
- Added `C6 Conflict: ACTIVE` when opposing available axes both have absolute normalized magnitude >=0.50.
- Added `C6 Shock: ACTIVE` thresholds:
  - |USD/KRW 5-observation change| >=2.5%
  - |Korea Treasury 3Y 5-observation change| >=30bp
  - |Customer Deposits 5-observation change| >=7.5%
- C6 Shock/Conflict feed Change Detection / Transition only and do not automatically change Market Regime, global SAI, portfolio action or permanent Base Weight.

### Anti-double-counting / authority safeguards
- `E6 Liquidity / Macro` remains the qualitative/adaptive interpretation owner.
- MASTER Engine 06 remains Global Liquidity analysis; no 25th engine created.
- Smart Money remains C1/E1; Program C2/E2; Breadth C3/E3; Sector Leadership C4/E4; Technical Structure C5/E5; Options/OI/Volatility E7; Binance/global-leading proxies E8.
- Korea Treasury 3Y in C6 represents domestic financial conditions; TMF remains E8 global-leading context and is not re-scored inside C6.
- VH/H/M/L remains qualitative and cannot be converted into numeric C6 weights.
- Anti-circularity preserved: C6 cannot choose a Regime, use that Regime to alter its own weights, then reconfirm the same Regime.

### Scoring firewall retained
- `AI Master Score` remains `DATA UNAVAILABLE`.
- Global `Strategy Action Index` remains `DATA UNAVAILABLE`.
- C1-C6 are component-level formulas only.
- Global aggregation, global missing/partial handling, final range/Action Bands and regression validation remain required before global SAI activation.

### Backup
- Pre-patch checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C6_LIQUIDITY_MACRO_PREPATCH_BACKUP_2026-09-10.md`
- Final post-integration checkpoint:
  - `Backup/AI_MARKET_MASTER_3.2_SAI_C6_LIQUIDITY_MACRO_FINAL_BACKUP_2026-09-10.md`
- Final checkpoint blob SHA: `3dd78dd160eb49e7cee0ad8bde97f2b31fc2ef48`.
- Final checkpoint records the post-integration six-authority snapshot, 35/35/30 FX/Rate/Cash formula, point-in-time/freshness rules, predefined partial handling, Margin Credit and Policy Rate/M2 non-numeric boundaries, Conflict/Shock safeguards, anti-double-counting, anti-circularity and final cross-authority verification.

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
