# AI Market Master Change Log

## 2026-09-10 — SAI HTS-Operational v2 Redesign

### Why
- Reworked C1-C8 around HTS fields the user can repeatedly provide in normal operation.
- The prior v1 formulas were reproducible but several components depended on inputs not reliably present in the user's actual HTS export, causing unnecessary `DATA UNAVAILABLE` results.
- The redesign keeps validation strict while replacing unavailable theoretical dependencies with explicit HTS-native formulas.

### C1 Smart Money v2
- Replaced futures-flow/OI-unit normalization with participant-direction shares from the HTS investor-flow panel.
- `D_FC = Foreign KOSPI / (|Individual|+|Foreign|+|Institution|)`.
- `D_FF = Foreign Futures / (|IndividualF|+|ForeignF|+|InstitutionF|)`.
- `C1 = 0.55*D_FC + 0.45*D_FF`.
- Institution sub-rows remain context to avoid double counting.

### C2 Program Flow v2
- Kept Arbitrage/Non-Arbitrage ownership but widened operational saturation to match the supplied traded-value ratios.
- `N_ARB=clip(ARB_R/3%,-1,+1)`.
- `N_NONARB=clip(NONARB_R/10%,-1,+1)`.
- `C2=0.25*N_ARB+0.75*N_NONARB`.
- Mechanical Event safeguard retained.

### C3 Breadth v2
- Kept `(ADV-DEC)/(ADV+DEC)` architecture.
- Changed breadth normalization saturation from ±0.50 to ±0.40 for more responsive recurring HTS breadth.
- `C3=0.70*N_K+0.30*N_Q`.
- ADL absolute level remains context only.

### C4 Market Leadership / Rotation v2
- Replaced the non-repeatable fixed eight-sector benchmark requirement.
- Large-cap relative axis uses KOSPI100/KOSPI200/KTOP30/KRX100 versus KOSPI.
- Growth/rotation axis uses KOSDAQ/KOSDAQ150 versus KOSPI.
- `C4=0.40*N_LC+0.60*N_GR`.
- Full sector leadership remains qualitative E4 context rather than a mandatory numeric input.

### C5 Technical Structure v2
- Replaced mandatory HH/HL + formal SR inputs with recurring HTS technical data.
- Trend Position 55% from MA20/50/60/200 + VWAP20/50/60/200.
- Momentum 25% from RSI9 + MACD/Signal/Oscillator.
- Session Structure 20% from close-location-in-range + KOSPI daily return.
- `C5=0.55*TP+0.25*MOM+0.20*SES`.
- ADX, volume, Elliott/Fibonacci and support/resistance remain validation/context; structural break can still activate C5 Shock.

### C6 Liquidity / Macro v2
- Replaced unavailable 5-day FX/rate history with recurring daily HTS changes while retaining 5-observation Customer Deposits.
- `FX=-clip(r_USDKRW/0.8%,-1,+1)`.
- KTB3Y and CD91 absolute HTS changes are converted from percentage points to bp.
- `RATE=0.70*KTB+0.30*CD`.
- `CASH=clip(DEP5/5%,-1,+1)`.
- `C6=0.35*FX+0.35*RATE+0.30*CASH`.
- Margin Credit/receivables/futures deposits remain contextual risk/liquidity flags.

### C7 Volatility / Derivatives v2
- Removed mandatory VKOSPI MA20 and fair-basis inputs.
- `VOL=-clip(r_VKOSPI/10%,-1,+1)`.
- `FLEAD=clip((r_KOSPI200_Futures-r_KOSPI200_Spot)/0.5%p,-1,+1)`.
- `C7=0.70*VOL+0.30*FLEAD`.
- Raw basis without fair basis, current OI snapshot, isolated option strike, PCR without full-market data and thin volatility futures remain context only.

### C8 Global Leading v2
- HTS global-market panel is now the primary numeric C8 source.
- US Futures 40% = Mini S&P500 + Mini Nasdaq.
- Prior US Close 25% = S&P500 + Nasdaq.
- Semiconductor 20% = SOX.
- Asia 15% = Nikkei + China/HK composite.
- `C8=0.40*USF+0.25*USC+0.20*SEMI+0.15*ASIA`.
- Binance remains supporting/confirmation under BINANCE_RULE and is no longer mandatory for numeric C8 v2.
- WTI, Gold, DAX/CAC and Binance positioning remain context unless a later explicit scoring revision adopts them.

### Global SAI impact
- Global Base Weights remain unchanged after regression: `18/12/15/10/20/10/8/7%` for C1-C8.
- Global VERIFIED/PARTIAL gate remains strict: C5 required, Flow/Internal/Environment represented, at least 6/8 usable and at least 70% Base Weight coverage.
- Conditional Adaptive Weight rules remain unchanged in architecture: one qualifying family +5pp, two same-direction families +3pp each, opposite events blocked, 3+ events retain Base + Broad Market Shock, max reallocation 6pp.
- Action Bands remain ±0.30 / ±0.60.

### Validation / optimization
- Double-counting boundaries rechecked: ADL -> C3 context, institution sub-rows -> C1 context, volume/ADX -> C5 context, Margin Credit -> C6 context, raw basis/OI/single-strike options -> C7 context, Binance -> C8 confirmation.
- Missing values remain non-neutral and never silently filled.
- C1-C8 formulas remain bounded to [-1,+1].
- Global SAI remains bounded to [-1,+1] under Base and allowed adaptive reallocations.
- The supplied 2026-09-10 HTS sample is executable under v2 and yields a near-balanced Base SAI while preserving the material conflict between negative Smart Money/Non-Arbitrage and positive technical/rotation/volatility-normalization evidence.
- Validation is `PASS BY RULE DESIGN`; empirical out-of-sample optimization is not established.

### Backup
- Pre-patch: `Backup/AI_MARKET_MASTER_3.2_SAI_HTS_V2_PREPATCH_BACKUP_2026-09-10.md`.
- Final post-patch backup is created after authority re-read and regression confirmation.

## 2026-09-10 — Global Strategy Action Index v1 Activation
- Activated reproducible global `Strategy Action Index` v1 while keeping `AI Master Score` DATA UNAVAILABLE.
- Base weights: C1-C8 = `18/12/15/10/20/10/8/7%`.
- Added Global Missing/Partial Gate, family conflict, Conditional Adaptive Weight, Action Bands and formula/regression validation.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_GLOBAL_ACTIVATION_FINAL_BACKUP_2026-09-10.md`.
- Final checkpoint blob SHA: `c8316a0fbc746c7ca5867073f39aacf6ef9f7878`.

## 2026-09-10 — SAI-C8 Global Leading Component Integration
- Added original C8 v1 Binance/global-leading five-axis formula.
- Superseded for current numeric execution by HTS-Operational v2; preserved in Git history and C8 final backup.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_C8_GLOBAL_LEADING_FINAL_BACKUP_2026-09-10.md`.
- Blob SHA: `c40b37ffba7d025a7ed9e2711d7f9a4a6009a4a6`.

## 2026-09-10 — SAI-C7 Volatility / Derivatives Risk Component Integration
- Added original C7 v1 VKOSPI-MA20/fair-basis formula.
- Superseded for current numeric execution by HTS-Operational v2; preserved in Git history and final backup.
- Final checkpoint blob SHA: `3f9ee5985a46dbb3e2f2bd8b7c714b20e67f2bd6`.

## 2026-09-10 — SAI-C6 Liquidity / Macro Component Integration
- Added original C6 v1 daily domestic financial-condition formula.
- Superseded for current numeric execution by HTS-Operational v2; preserved in Git history and final backup.
- Final checkpoint blob SHA: `3dd78dd160eb49e7cee0ad8bde97f2b31fc2ef48`.

## 2026-09-10 — SAI-C5 Technical Structure Component Integration
- Added original C5 v1 PS/SR/TP formula.
- Superseded for current numeric execution by HTS-Operational v2; preserved in Git history and final backup.

## 2026-09-10 — SAI-C4 Sector / Leadership Component Integration
- Added original C4 v1 eight-benchmark sector formula.
- Superseded for current numeric execution by HTS-Operational v2; preserved in Git history and final backup.

## 2026-09-10 — SAI-C3 Breadth / Market Internal
- Added original C3 breadth formula; core ownership retained and normalization revised in v2.

## 2026-09-10 — SAI-C2 Program Flow Component Integration
- Added original C2 Program formula; ownership retained and normalization/weights revised in v2.

## 2026-09-10 — SAI-C1 Smart Money Component Integration
- Added original C1 Smart Money formula; superseded by participant-share v2.

## 2026-09-08 — Adaptive Validation & Regime Evidence Priority Integration
- Added 8 Market Regimes, E1-E8 Evidence Groups, VH/H/M/L qualitative Evidence Priority, Transition, conflict resolution and Regime re-validation.
- Adaptive Validation remains cross-engine, not a 25th engine.

## 2026-09-08 — Binance Latest Re-query & Fallback Policy
- Added fresh re-query first, LIVE/FALLBACK/STALE, freshness windows and Confidence downgrade.
- HTS/KRX remains final Korean-market confirmation.

## 2026-09-07 — 3.2 Unified Stable
- Consolidated authority into six dedicated rule files while preserving 24 internal engines and 8 Dashboard categories.

## Historical
Earlier 3.2 and 3.1 history remain recoverable through Git history / legacy references.