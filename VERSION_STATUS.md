# AI Market Master Version Status

## Current Version
**AI Market Master 3.2 — Unified Stable / Current Version**

## Canonical Authority
Authority is split by function across exactly six official files under `Rules/`:

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
- Adaptive Validation remains a cross-engine framework, not a 25th engine
- No ninth Dashboard category created
- Table First, English+Korean, Confidence, Dynamic KOSPI Zone, Smart Money Action Matrix, Portfolio Sell Priority and Intraday 24→16→17 retained
- Change Detection → Validation → Revision → Final AI Decision retained
- HTS/KRX remains final Korean-market confirmation
- Binance remains global leading/supporting only

## Adaptive Validation
Official framework remains:
- 8 Market Regimes
- Primary Regime + Transition Regime / Risk
- Regime Confidence High / Medium / Low
- E1-E8 Evidence Groups
- VH/H/M/L qualitative Evidence Priority
- Conditional Evidence Escalation
- anti-double-counting
- conflict resolution
- Regime re-validation
- qualitative Regime-to-Strategy posture

VH/H/M/L are not numeric weights and must never be converted into numeric component weights unless SCORING_RULE explicitly defines and validates a separate formula.

## Fixed Technical References
- Major High 9,114 = 0% / Major Low 2,293 = 100% on Long-Term Retracement Axis
- Correction Low 5,593 = 0% / Major High 9,114 = 100% on Recovery Axis
- Both axes mandatory
- Closing break below 5,593 requires Recovery Structure Failure review, Elliott recount and Fibonacci scenario recalculation

## Binance
Fixed watchlist:
`EWYUSDT / SAMSUNGUSDT / SKHYNIXUSDT / SOXLUSDT / QQQUSDT / SPYUSDT / TMFUSDT / BTCUSDT`

## Scoring
`AI Master Score` remains `DATA UNAVAILABLE` because no complete reproducible formula is adopted.

`Strategy Action Index` v1 is now **FORMULA ACTIVATED / RUNTIME DATA-DEPENDENT** under `SCORING_RULE`. A numeric SAI may be displayed only when its global data/completeness gate passes; otherwise runtime output remains `DATA UNAVAILABLE`.

Defined component-level formulas inside `SCORING_RULE`:

### SAI-C1 Smart Money
Foreign KOSPI cash + Foreign KOSPI200 futures + Institutional KOSPI cash.
Full internal weighting 40/40/20. Institution missing permits predefined 50/50 Foreign Cash/Futures PARTIAL formula.

### SAI-C2 Program Flow
Arbitrage + Non-Arbitrage Program flow; Total Program is reconciliation/context only.
Full internal weighting 30/70. Arbitrage missing permits Non-Arbitrage-only PARTIAL; Non-Arbitrage missing makes C2 DATA UNAVAILABLE.

### SAI-C3 Breadth / Market Internal
KOSPI active breadth mandatory + KOSDAQ active breadth supplementary.
Full internal weighting 70/30. KOSDAQ missing permits KOSPI-only PARTIAL. Raw ADL remains contextual in v1.

### SAI-C4 Sector / Leadership
Fixed eight-benchmark universe. Calculates Sector Direction Breadth `SD` and KOSPI-relative Leadership Breadth `RL`.
`SAI-C4 = 0.60*SD + 0.40*RL`.
8/8 eligible VERIFIED, 6-7/8 PARTIAL, <6/8 DATA UNAVAILABLE.

### SAI-C5 Technical Structure
Official v1 timeframe: KOSPI Daily / Closing-confirmed.
`SAI-C5 = 0.50*PS + 0.30*SR + 0.20*TP`.
Price Structure PS is mandatory. Predefined partial formulas apply when only SR or TP is unavailable. Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci remain validation/context.

### SAI-C6 Liquidity / Macro
Official v1 uses completed daily domestic financial-condition observations plus latest officially published Customer Deposits observation.
`SAI-C6 = 0.35*FX + 0.35*RATE + 0.30*CASH`.
FX/Rate/Cash use predefined normalization and explicit two-axis PARTIAL rules. Margin Credit remains qualitative context; Policy Rate/M2 remain Structural Macro Context.

### SAI-C7 Volatility / Derivatives Risk
Official v1 uses completed domestic volatility/derivatives observations.
Numeric terms:
- Volatility Stress `VOL` 60% — mandatory
- Fair-value-adjusted KOSPI200 Basis Stress `BASIS` 40% — optional

`VOL = -clip((VKOSPI_t / VKOSPI_MA20 - 1)/0.30,-1,+1)`
`BasisGap = ActualBasis - FairBasis`
`BG = BasisGap / KOSPI200Spot`
`BASIS = clip(BG/0.003,-1,+1)`
`SAI-C7 = 0.60*VOL + 0.40*BASIS`

VOL + BASIS valid → eligible VERIFIED; VOL valid/BASIS unavailable → `C7=VOL` / PARTIAL; VOL unavailable → DATA UNAVAILABLE.
OI/PCR/volatility futures remain contextual; Mechanical Event, Conflict and Shock safeguards remain active.

### SAI-C8 Global Leading
Numeric axes:
- Global Equity Risk `GR` 30% — SPY + QQQ composite
- Korea Leading `KR` 25% — EWY
- Semiconductor Risk `SEMI` 20% — SOXL
- Global Rate/Liquidity `GLIQ` 15% — TMF
- Crypto Risk `CRYPTO` 10% — BTC

`N_SPY = clip(r_SPY/0.015,-1,+1)`
`N_QQQ = clip(r_QQQ/0.020,-1,+1)`
`GR = 0.50*N_SPY + 0.50*N_QQQ`
`KR = clip(r_EWY/0.025,-1,+1)`
`SEMI = clip(r_SOXL/0.050,-1,+1)`
`GLIQ = clip(r_TMF/0.030,-1,+1)`
`CRYPTO = clip(r_BTC/0.040,-1,+1)`
`SAI-C8 = 0.30*GR + 0.25*KR + 0.20*SEMI + 0.15*GLIQ + 0.10*CRYPTO`

C8 full requires all five axes and both SPY/QQQ in GR. PARTIAL requires GR, at least 3/5 axes and >=60% original C8 weight coverage. FALLBACK caps C8 at PARTIAL; STALE is prohibited numerically. Samsung/SKH and G6 positioning remain confirmation/context only.

### Global Strategy Action Index v1
Base weights:
`C1/C2/C3/C4/C5/C6/C7/C8 = 18/12/15/10/20/10/8/7%`.

Base formula:
`SAI_Base = 0.18*C1 + 0.12*C2 + 0.15*C3 + 0.10*C4 + 0.20*C5 + 0.10*C6 + 0.08*C7 + 0.07*C8`.

Global VERIFIED requires 8/8 component VERIFIED.
Global PARTIAL requires C5, Flow(C1/2), Internal(C3/4), Environment(C6/7/8), at least 6/8 usable components and at least 70% original Base Weight coverage. Missing is never zero/Neutral.

Conditional Adaptive Weight:
- only with 8/8 VERIFIED, no Global SAI Conflict and validated Shock/confirmation;
- one qualifying family event -> +5pp to that family;
- two same-direction qualifying families -> +3pp each;
- opposite qualifying events -> adaptive blocked;
- three or more qualifying families -> Base Weights retained + Broad Market Shock;
- maximum total reallocation = 6pp;
- VH/H/M/L are never converted to numbers.

Action Bands:
- >=+0.60 Strong Positive Execution Bias
- +0.30 to <+0.60 Positive Execution Bias
- >-0.30 to <+0.30 Balanced / Hold Bias
- >-0.60 to <=-0.30 Negative Execution Bias
- <=-0.60 Strong Negative Execution Bias

SAI is execution bias, not an automatic trade command. PARTIAL/Conflict/Mechanical Event and portfolio/technical/Regime safeguards remain binding.

Formula/regression validation passed by rule design, including all 256 C1-C8 +/-1 corner combinations across Base and allowed one/two-family adaptive patterns. Empirical backtest optimization remains NOT ESTABLISHED.

## Restore / Design References
Non-authoritative references:
- `Backup/AMM_3.0_LEGACY_VALIDATION_RESTORE.md`
- `Backup/AMM_3.2_ADAPTIVE_REGIME_DESIGN_BACKUP.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_ADAPTIVE_DESIGN_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C2_PROGRAM_FLOW_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C3_BREADTH_INTERNAL_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C4_SECTOR_LEADERSHIP_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C5_TECHNICAL_STRUCTURE_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C6_LIQUIDITY_MACRO_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C7_VOLATILITY_DERIVATIVES_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C8_GLOBAL_LEADING_PREPATCH_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_GLOBAL_ACTIVATION_PREPATCH_BACKUP_2026-09-10.md`

## Final Backup Checkpoint
Verified final checkpoints:
- `Backup/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_FINAL_BACKUP_2026-09-08.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C1_SMART_MONEY_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C2_PROGRAM_FLOW_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C3_BREADTH_INTERNAL_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C4_SECTOR_LEADERSHIP_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C5_TECHNICAL_STRUCTURE_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C6_LIQUIDITY_MACRO_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C7_VOLATILITY_DERIVATIVES_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_C8_GLOBAL_LEADING_FINAL_BACKUP_2026-09-10.md`
- `Backup/AI_MARKET_MASTER_3.2_SAI_GLOBAL_ACTIVATION_FINAL_BACKUP_2026-09-10.md`

Global SAI final checkpoint blob SHA: `c8316a0fbc746c7ca5867073f39aacf6ef9f7878`.
It records the post-activation six-authority snapshot, global Base Weights, Missing/Partial gate, family conflict, Conditional Adaptive Weight, Action Bands, anti-circularity, formula/regression validation and empirical-backtest caveat.

## Previous Stable
**AI Market Master Dashboard 3.1 — Stable Legacy / Previous Stable**
The original 3.1 CFB remains preserved unchanged for reference and regression verification.

## Legacy 3.2
Superseded 3.2 rule files are non-authoritative and recoverable through Git history using `Legacy/3.2-history/INDEX.md`.

Date: 2026-09-10