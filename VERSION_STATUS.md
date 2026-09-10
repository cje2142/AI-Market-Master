# AI Market Master Version Status

## Current Version
**AI Market Master 3.2 — Unified Stable / SAI HTS-Operational v2**

## Canonical Authority
Authority remains split across exactly six official files under `Rules/`:
1. `AI_MARKET_MASTER_3.2_MASTER_RULE.md` — architecture/integration authority
2. `AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md` — trigger/presentation authority
3. `AI_MARKET_MASTER_3.2_SCORING_RULE.md` — numeric scoring authority
4. `AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md` — technical calculation authority
5. `AI_MARKET_MASTER_3.2_BINANCE_RULE.md` — Binance global-leading/supporting authority
6. `AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md` — Regime/Evidence Priority/transition/conflict authority

No legacy or Backup file overrides these authorities.

## Preserved Architecture
- 24 internal Analysis Engines unchanged
- 8 fixed Dashboard categories unchanged
- Adaptive Validation remains cross-engine, not a 25th engine
- HTS/KRX remains final Korean-market confirmation
- Binance remains a global leading/supporting layer
- Table First, Dynamic KOSPI Zone, Portfolio Risk-Reduction Priority, Intraday 24→16→17 and dual-axis Elliott/Fibonacci retained

## Numeric Status
- `Strategy Action Index`: **FORMULA ACTIVATED / RUNTIME DATA-DEPENDENT**
- `AI Master Score`: **DATA UNAVAILABLE**

Active SAI component schema: **HTS-Operational v2**. Previous v1 formulas are preserved in Git history/backups but superseded for current numeric execution.

## C1-C8 HTS-Operational v2
### C1 Smart Money
Uses recurring HTS participant flows; no futures-flow/OI-unit mixing.
`D_FC = Foreign KOSPI / (|Individual|+|Foreign|+|Institution|)`
`A_C = clip((Gross Cash Participant Flow / KOSPI Traded Value)/5%,0,1)`
`FC = A_C * D_FC`
`FF = Foreign Futures / (|IndividualF|+|ForeignF|+|InstitutionF|)`
`C1 = 0.55*FC + 0.45*FF`
Cash activity guard prevents tiny absolute flows from producing an outsized score. Institution sub-rows remain context.

### C2 Program Flow
`N_ARB=clip((ARB/KTV)/3%,-1,+1)`
`N_NONARB=clip((NONARB/KTV)/10%,-1,+1)`
`C2=0.25*N_ARB+0.75*N_NONARB`
Non-Arbitrage remains structural core; Mechanical Event safeguard retained.

### C3 Breadth / Internal
`B=(ADV-DEC)/(ADV+DEC)` with KOSPI mandatory and KOSDAQ confirmation.
Normalization saturation = ±0.40 breadth ratio.
`C3=0.70*N_K+0.30*N_Q`.
Absolute ADL remains context only.

### C4 Market Leadership / Rotation
Numeric C4 uses recurring index relative returns instead of eight mandatory sector benchmarks.
- Large-cap: KOSPI100/KOSPI200/KTOP30/KRX100 vs KOSPI
- Growth/rotation: KOSDAQ/KOSDAQ150 vs KOSPI
`C4=0.40*N_LC+0.60*N_GR`
Full sector interpretation remains qualitative E4 context.

### C5 Technical Structure
- Trend Position 55% from MA20/50/60/200 + VWAP20/50/60/200
- Momentum 25% from RSI9 + MACD/Signal/Oscillator
- Session Structure 20% from close-location-in-range + daily return
`C5=0.55*TP+0.25*MOM+0.20*SES`
ADX/volume/Elliott/Fibonacci/support-resistance remain validation/context; structural breaks can trigger Shock.

### C6 Liquidity / Macro
`FX=-clip(r_USDKRW/0.8%,-1,+1)`
KTB3Y/CD91 HTS absolute changes are converted to bp.
`RATE=0.70*KTB+0.30*CD`
`CASH=clip(DEP5/5%,-1,+1)`
`C6=0.35*FX+0.35*RATE+0.30*CASH`
Margin Credit/receivables/futures deposits remain context/risk flags.

### C7 Volatility / Derivatives Risk
`VOL=-clip(r_VKOSPI/10%,-1,+1)`
`FLEAD=clip((r_KOSPI200_Futures-r_KOSPI200_Spot)/0.5%p,-1,+1)`
`C7=0.70*VOL+0.30*FLEAD`
Raw basis without fair basis, OI snapshot, isolated option strike and thin volatility-futures data remain context only.

### C8 Global Leading
Primary numeric source is the recurring HTS global-market panel:
- US Futures 40% — Mini S&P500 + Mini Nasdaq
- Prior US Close 25% — S&P500 + Nasdaq
- Semiconductor 20% — SOX
- Asia 15% — Nikkei + China/HK composite
`C8=0.40*USF+0.25*USC+0.20*SEMI+0.15*ASIA`
Binance remains supporting/confirmation under BINANCE_RULE and is not silently re-added numerically.

## Global Strategy Action Index v2
Base weights remain `C1/C2/C3/C4/C5/C6/C7/C8 = 18/12/15/10/20/10/8/7%`.

`SAI_Base = 0.18*C1 + 0.12*C2 + 0.15*C3 + 0.10*C4 + 0.20*C5 + 0.10*C6 + 0.08*C7 + 0.07*C8`

Global VERIFIED requires 8/8 VERIFIED.
Global PARTIAL requires C5, Flow/Internal/Environment representation, >=6/8 usable and >=70% Base Weight coverage. Missing never equals Neutral. Any component PARTIAL forces global PARTIAL; adaptive numeric reweighting is blocked in PARTIAL mode.

Conditional Adaptive Weight remains: one family +5pp; two same-direction families +3pp each; opposite events blocked; 3+ events retain Base + Broad Market Shock; maximum reallocation 6pp; VH/H/M/L never becomes numeric weight.

Action Bands remain:
- >=+0.60 Strong Positive Execution Bias
- +0.30 to <+0.60 Positive Execution Bias
- >-0.30 to <+0.30 Balanced / Hold Bias
- >-0.60 to <=-0.30 Negative Execution Bias
- <=-0.60 Strong Negative Execution Bias

## Validation Boundary
HTS-Operational v2 = `VERIFIED BY RULE DESIGN` after formula, missing/conflict/shock, activity-guard and cross-authority regression.
Not empirically optimized: normalization thresholds, Shock thresholds, internal weights, Global Base Weights, Action Bands and C1 cash-activity saturation.

## Recovery / Backup
Pre-patch checkpoint:
- `Backup/AI_MARKET_MASTER_3.2_SAI_HTS_V2_PREPATCH_BACKUP_2026-09-10.md`
- blob SHA `173e86d3d1af1c52130f2abbdf7f191da5319429`

Previous Global SAI v1 final checkpoint remains preserved:
- `Backup/AI_MARKET_MASTER_3.2_SAI_GLOBAL_ACTIVATION_FINAL_BACKUP_2026-09-10.md`
- blob SHA `c8316a0fbc746c7ca5867073f39aacf6ef9f7878`

HTS-Operational v2 final backup is registered after final cross-authority verification.

Date: 2026-09-10