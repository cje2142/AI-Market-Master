# AI Market Master Version Status

## Current Version
**AI Market Master 3.2 — Unified Stable / Current Version**

## Canonical Authority
There is no single overloaded Dashboard file. Authority is split by function across exactly six official files under `Rules/`:

1. `AI_MARKET_MASTER_3.2_MASTER_RULE.md` — master architecture/integration authority
2. `AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md` — exact trigger and presentation authority
3. `AI_MARKET_MASTER_3.2_SCORING_RULE.md` — numeric scoring authority
4. `AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md` — technical calculation authority
5. `AI_MARKET_MASTER_3.2_BINANCE_RULE.md` — Binance global-leading authority
6. `AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md` — Market Regime, adaptive Evidence Priority, transition/conflict resolution and Regime re-validation authority

No legacy file may override these rules.

## Preserved Architecture
- 24 internal Analysis Engines retained
- 8 fixed user-facing Dashboard categories retained
- Adaptive Validation is a cross-engine framework, not a 25th engine
- No ninth Dashboard category created
- 3.0/3.1 validated functions restored where 3.2 became weakly specified
- Table First, English+Korean, Confidence, Dynamic KOSPI Zone, Smart Money Action Matrix, Portfolio Sell Priority, Intraday 24→16→17 retained
- Change Detection → Validation → Revision → Final AI Decision retained as closed-loop logic
- Legacy Performance Validation / qualitative Engine Reliability concept retained without inventing historical numeric formulas

## Adaptive Validation
Official 3.2 adaptive framework remains:
- 8 Market Regimes
- Primary Regime + Transition Regime / Risk
- Regime Confidence High / Medium / Low
- E1-E8 Evidence Groups
- VH/H/M/L qualitative Evidence Priority Matrix
- Conditional Evidence Escalation
- anti-double-counting
- adaptive conflict resolution
- Regime re-validation
- qualitative Regime-to-Strategy posture

VH/H/M/L are not numeric weights and must not be converted into scores unless SCORING_RULE explicitly defines a separate reproducible numeric formula.

## Fixed Technical References
- Major High 9,114 = 0% / Major Low 2,293 = 100% on Long-Term Retracement Axis
- Correction Low 5,593 = 0% / Major High 9,114 = 100% on Recovery Axis
- Both axes are mandatory
- Closing break below 5,593 requires Recovery Structure Failure review, Elliott recount and Fibonacci scenario recalculation

## Binance
Fixed 8-symbol watchlist:
`EWYUSDT / SAMSUNGUSDT / SKHYNIXUSDT / SOXLUSDT / QQQUSDT / SPYUSDT / TMFUSDT / BTCUSDT`

HTS/KRX is final Korean-market confirmation. Binance is leading/supporting data only.

## Scoring
Official global numeric formulas for `AI Master Score` and `Strategy Action Index` are not yet complete. Therefore both global scores remain `DATA UNAVAILABLE`.

Defined component-level formulas inside `SCORING_RULE`:

### SAI-C1 Smart Money
Uses:
- Foreign KOSPI cash flow
- Foreign KOSPI200 futures flow
- Institutional KOSPI cash flow

Program/Breadth/Options remain outside C1 under E2/E3/E7 ownership.

### SAI-C2 Program Flow
Uses:
- Arbitrage Program flow — supplementary/mechanical-sensitive
- Non-Arbitrage Program flow — mandatory structural core
- Total Program flow — reconciliation/context only, not an additional score

C2 full internal weighting is 30% Arbitrage / 70% Non-Arbitrage. Non-Arbitrage missing makes C2 `DATA UNAVAILABLE`; Arbitrage missing permits the predefined Non-Arbitrage-only `PARTIAL` formula.

Known expiry/index/ETF rebalance effects are disclosed through `C2 Mechanical Event` and do not automatically change numeric weights or Market Regime.

### SAI-C3 Breadth / Market Internal
Uses:
- KOSPI advance/decline breadth — mandatory structural core
- KOSDAQ advance/decline breadth — supplementary cross-market participation confirmation
- unchanged issue counts — validation/context only
- raw ADL level — contextual only in v1, not a numeric contribution without comparable history

C3 full internal weighting is 70% KOSPI breadth / 30% KOSDAQ breadth. KOSDAQ missing permits a predefined KOSPI-only `PARTIAL` formula; KOSPI breadth missing makes C3 `DATA UNAVAILABLE`.

C3 preserves explicit Cross-Market Conflict, Index/Breadth Divergence and extreme Breadth Shock flags without changing Market Regime or numeric weights automatically.

### SAI-C4 Sector / Leadership
Uses a fixed eight-benchmark universe:
- KRX Semiconductor Index
- KRX Automobile Index
- KRX Secondary Battery TOP 10 Index
- KOSPI 200 Financial Index
- iSelect Shipbuilding TOP10 Index (PR)
- iSelect Defense TOP10 Index (Price Return)
- KRX-Akros AI Power Infrastructure Index
- KRX Bio TOP 10 Index

C4 calculates:
- Sector Direction Breadth `SD`
- KOSPI-relative Leadership Breadth `RL`
- `SAI-C4 = 0.60*SD + 0.40*RL`

C4 uses an explicit 75% completeness gate: 8/8 is eligible for `VERIFIED`, 6-7/8 uses the predefined `PARTIAL` calculation, fewer than 6/8 or an invalid/asynchronous KOSPI comparator makes C4 `DATA UNAVAILABLE`.

Leadership Concentration remains qualitative/contextual under E4 and is not an independent numeric C4 term. C4 Conflict/Shock flags feed Change Detection / Transition only and do not automatically alter Market Regime, portfolio action or Base Weight.

### SAI-C5 Technical Structure
Official v1 timeframe: KOSPI Daily / Closing-confirmed structure.

Numeric terms:
- Price Structure `PS` — mandatory directional core, 50%
- Support / Resistance Position `SR` — 30%
- MA / VWAP Trend Position `TP` — 20%

Full formula:
`SAI-C5 = 0.50*PS + 0.30*SR + 0.20*TP`

Key safeguards:
- Intraday data creates `C5 Intraday Preview` only and cannot overwrite closing-confirmed C5 by itself.
- PS uses validated HH/HL, LH/LL or confirmed closing breakout/breakdown structure.
- SR uses the nearest validated major `S < R` corridor; intact-corridor score is limited to ±0.50, while confirmed closing breakout/breakdown may reach ±1.00.
- TP compresses MA20/MA60/VWAP20/VWAP60 into one composite with a ±0.20% noise-control band.
- Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci remain validation/context flags, not extra C5 numeric terms.
- predefined partial formulas apply when only SR or TP is unavailable; missing PS makes C5 `DATA UNAVAILABLE`.
- C5 Conflict/Divergence/Shock flags do not automatically change Market Regime, global SAI, portfolio action or permanent Base Weight.

C1, C2, C3, C4 and C5 remain component-level formulas only and do not activate the global Strategy Action Index.
VH/H/M/L qualitative Evidence Priority is never converted into numeric component weight.

## Restore / Design References
Non-authoritative backup references:
- `Backup/AMM_3.0_LEGACY_VALIDATION_RESTORE.md`
- `Backup/AMM_3.2_ADAPTIVE_REGIME_DESIGN_BACKUP.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C2_PROGRAM_FLOW_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C3_BREADTH_INTERNAL_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C4_SECTOR_LEADERSHIP_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C5_TECHNICAL_STRUCTURE_PREPATCH_BACKUP_2026-09-10.md`

## Final Backup Checkpoint
Verified final checkpoints:
- `Backup/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_FINAL_BACKUP_2026-09-08.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C2_PROGRAM_FLOW_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C3_BREADTH_INTERNAL_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C4_SECTOR_LEADERSHIP_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C5_TECHNICAL_STRUCTURE_FINAL_BACKUP_2026-09-10.md`

The C5 final checkpoint blob SHA is `740941c70a468c2c7638783ba282dd5b174e1250` and records the post-integration six-authority snapshot, Daily/Closing timeframe boundary, PS/SR/TP formula, 50/30/20 internal weights, predefined partial handling, Volume/Momentum/Elliott-Fibonacci non-numeric boundary, conflict/divergence/shock safeguards, anti-double-counting, anti-circularity and final validation state.

## Previous Stable
**AI Market Master Dashboard 3.1 — Stable Legacy / Previous Stable**
The original 3.1 CFB remains preserved unchanged for reference and regression verification.

## Legacy 3.2
Superseded 3.2 rule files are non-authoritative and recoverable through Git history using `Legacy/3.2-history/INDEX.md`.

Date: 2026-09-10