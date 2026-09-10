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

The active SAI component schema is now **HTS-Operational v2**. v1 is preserved through Git history and pre/final backups but is superseded for current numeric execution.

## C1-C8 HTS-Operational v2
### C1 Smart Money
Uses recurring HTS participant flows rather than mixing futures flow with OI contracts.
`D_FC = Foreign KOSPI / (|Individual|+|Foreign|+|Institution|)`
`D_FF = Foreign Futures / (|IndividualF|+|ForeignF|+|InstitutionF|)`
`C1 = 0.55*D_FC + 0.45*D_FF`
Institution sub-rows remain context to avoid double counting.

### C2 Program Flow
Uses Arbitrage/Non-Arbitrage normalized by KOSPI traded value in the same unit.
`N_ARB=clip(ARB_R/3%,-1,+1)`
`N_NONARB=clip(NONARB_R/10%,-1,+1)`
`C2=0.25*N_ARB+0.75*N_NONARB`
Non-Arbitrage remains structural core; Mechanical Event safeguard retained.

### C3 Breadth / Internal
`B=(ADV-DEC)/(ADV+DEC)` with KOSPI mandatory, KOSDAQ confirmation.
Normalization saturation changed to ±0.40 breadth ratio.
`C3=0.70*N_K+0.30*N_Q`.
ADL absolute level remains context only.

### C4 Market Leadership / Rotation
Numeric C4 no longer requires eight sector benchmark indices.
Uses recurring relative returns:
- Large-cap axis: KOSPI100/KOSPI200/KTOP30/KRX100 vs KOSPI
- Growth/rotation axis: KOSDAQ/KOSDAQ150 vs KOSPI
`C4=0.40*N_LC+0.60*N_GR`
Full sector interpretation remains qualitative E4 context.

### C5 Technical Structure
Uses repeatable KOSPI closing data:
- Trend Position 55% from MA20/50/60/200 + VWAP20/50/60/200
- Momentum 25% from RSI9 + MACD/Signal/Oscillator
- Session Structure 20% from close-location-in-range + daily return
`C5=0.55*TP+0.25*MOM+0.20*SES`
ADX/volume/Elliott/Fibonacci/support-resistance remain validation/context; structural break can still trigger C5 Shock.

### C6 Liquidity / Macro
Uses daily USD/KRW, daily KTB3Y/CD91 absolute rate changes and five-observation Customer Deposit change.
`FX=-clip(r_USDKRW/0.8%,-1,+1)`
`RATE=0.70*KTB+0.30*CD`
`CASH=clip(DEP5/5%,-1,+1)`
`C6=0.35*FX+0.35*RATE+0.30*CASH`
Margin Credit/receivables/futures deposits remain context/risk flags.

### C7 Volatility / Derivatives Risk
Removes mandatory VKOSPI-MA20 and fair-basis requirements that were not repeatably supplied.
`VOL=-clip(r_VKOSPI/10%,-1,+1)`
`FLEAD=clip((r_KOSPI200_Futures-r_KOSPI200_Spot)/0.5%p,-1,+1)`
`C7=0.70*VOL+0.30*FLEAD`
Raw basis without fair basis, current OI snapshot, isolated option strike and thin volatility-futures data remain context only.

### C8 Global Leading
Primary numeric source is the recurring HTS global-market panel, not mandatory Binance proxies.
Top-level axes:
- US Futures 40% — Mini S&P500 + Mini Nasdaq
- Prior US Close 25% — S&P500 + Nasdaq
- Semiconductor 20% — SOX
- Asia 15% — Nikkei + China/HK composite
`C8=0.40*USF+0.25*USC+0.20*SEMI+0.15*ASIA`
Binance remains supporting/confirmation under BINANCE_RULE and is not silently re-added numerically.

## Global Strategy Action Index v2
Base weights remain:
`C1/C2/C3/C4/C5/C6/C7/C8 = 18/12/15/10/20/10/8/7%`.

`SAI_Base = 0.18*C1 + 0.12*C2 + 0.15*C3 + 0.10*C4 + 0.20*C5 + 0.10*C6 + 0.08*C7 + 0.07*C8`

Global VERIFIED requires 8/8 VERIFIED.
Global PARTIAL retains the existing safety gate:
- C5 usable
- Flow family represented
- Internal family represented
- Environment family represented
- at least 6/8 usable
- at least 70% original Base Weight coverage

Missing never equals Neutral. Any component PARTIAL forces global PARTIAL. Adaptive numeric reweighting is blocked in PARTIAL mode.

Conditional Adaptive Weight remains:
- one qualifying family event -> +5pp
- two same-direction qualifying family events -> +3pp each
- opposite events -> blocked/Base retained
- 3+ events -> Base retained + Broad Market Shock
- max total reallocation 6pp
- VH/H/M/L never converted to numeric weight

Action Bands remain:
- >=+0.60 Strong Positive Execution Bias
- +0.30 to <+0.60 Positive Execution Bias
- >-0.30 to <+0.30 Balanced / Hold Bias
- >-0.60 to <=-0.30 Negative Execution Bias
- <=-0.60 Strong Negative Execution Bias

## Validation Boundary
HTS-Operational v2 is `VERIFIED BY RULE DESIGN` after formula, missing/conflict/shock and cross-authority regression.
It is **not empirically optimized**. Normalization thresholds, Shock thresholds, internal weights, Global Base Weights and Action Bands require future out-of-sample validation before statistical optimality can be claimed.

## Recovery / Backup
Pre-patch checkpoint:
- `Backup/AI_MARKET_MASTER_3.2_SAI_HTS_V2_PREPATCH_BACKUP_2026-09-10.md`

Previous Global SAI v1 final checkpoint remains preserved:
- `Backup/AI_MARKET_MASTER_3.2_SAI_GLOBAL_ACTIVATION_FINAL_BACKUP_2026-09-10.md`
- blob SHA `c8316a0fbc746c7ca5867073f39aacf6ef9f7878`

HTS-Operational v2 final backup is registered after post-patch cross-authority verification.

Date: 2026-09-10