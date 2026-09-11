# AI Market Master Change Log

## 2026-09-11 — Dashboard Execution Priority Hard Gate

### Why
- Prevent Full Dashboard runs from drifting into a scoring-first/free-form response when analytical complexity increases.
- Preserve the exact 8-category Dashboard layout before detailed calculations without changing any analytical authority or formula order.

### Changes
- DASHBOARD_RULE now initializes a fixed 8-category presentation skeleton immediately after the exact Full Dashboard trigger is recognized.
- Presentation Initialization is explicitly layout reservation only; it does not move SCORING, ADAPTIVE, TECHNICAL or BINANCE calculations ahead of their owning-rule sequence.
- MASTER_RULE Full Execution Chain now references Dashboard Presentation Initialization before Preflight, then maps validated results into the reserved Dashboard structure after Strategy.
- Added a Completion Hard Gate: normal completion is prohibited when required Dashboard structure, scoring status, Regime/Transition status, Binance disclosure, Strategy fields or final action validation fail.
- `AI Master Score` display is explicitly fixed to `DATA UNAVAILABLE — 공식 산식 미정의` until SCORING_RULE formally activates a reproducible formula.
- `Strategy Action Index` remains HTS-Operational v2 / runtime data-dependent.

### Validation
- Cross-authority regression: PASS.
- 6 official Authority files preserved.
- 24 internal Analysis Engines preserved.
- 8 Dashboard categories preserved.
- C1-C8 / Global SAI formulas and weights unchanged.
- ADAPTIVE Regime/Transition/conflict sequence unchanged.
- BINANCE Latest Re-query/Fallback/Freshness rules unchanged.
- TECHNICAL calculation authority unchanged.
- Intraday `24 → 16 → 17` path unchanged.
- No 25th engine or ninth Dashboard category created.

### Patch snapshot
- MASTER_RULE blob: `2c601ed6c5beb0c4937bf85f5b265f5f4b68957f`
- DASHBOARD_RULE blob: `c8a88f6046a975d2ec48757e89d0ee14333ae89b`
- Pre-patch backup creation commit: `dc81ca6558c0ccf36e227deb89a29bc3bd08f992`
- Final backup/seal: PENDING at this changelog registration step.

## 2026-09-10 — SAI HTS-Operational v2 Redesign

### Why
- Reworked C1-C8 around HTS fields the user can repeatedly provide.
- Replaced non-repeatable theoretical dependencies while preserving strict Missing, Conflict, Shock, Mechanical Event and anti-circularity safeguards.

### C1 Smart Money v2
- Replaced futures-flow/OI-unit normalization with participant-direction shares.
- Added cash-flow activity guard so tiny absolute cash flows cannot create an outsized score merely from participant-share dominance.
- `D_FC = Foreign KOSPI / (|Individual|+|Foreign|+|Institution|)`.
- `A_C = clip((Gross Cash Participant Flow / KOSPI Traded Value)/5%,0,1)`.
- `FC = A_C*D_FC`.
- `FF = Foreign Futures / (|IndividualF|+|ForeignF|+|InstitutionF|)`.
- `C1=0.55*FC+0.45*FF`.
- Institution sub-rows remain context only.

### C2 Program Flow v2
- `N_ARB=clip((ARB/KTV)/3%,-1,+1)`.
- `N_NONARB=clip((NONARB/KTV)/10%,-1,+1)`.
- `C2=0.25*N_ARB+0.75*N_NONARB`.
- Non-Arbitrage remains structural core; Mechanical Event safeguard retained.

### C3 Breadth v2
- Kept `(ADV-DEC)/(ADV+DEC)` architecture.
- Changed normalization saturation to ±0.40.
- `C3=0.70*N_K+0.30*N_Q`.
- Absolute ADL remains context only.

### C4 Market Leadership / Rotation v2
- Removed the non-repeatable mandatory eight-sector benchmark set from numeric C4.
- Large-cap axis: KOSPI100/KOSPI200/KTOP30/KRX100 relative to KOSPI.
- Growth/rotation axis: KOSDAQ/KOSDAQ150 relative to KOSPI.
- `C4=0.40*N_LC+0.60*N_GR`.
- Full sector analysis remains qualitative E4 context.

### C5 Technical Structure v2
- Trend Position 55% from MA20/50/60/200 + VWAP20/50/60/200.
- Momentum 25% from RSI9 + MACD/Signal/Oscillator.
- Session Structure 20% from close-location-in-range + daily return.
- `C5=0.55*TP+0.25*MOM+0.20*SES`.
- ADX, volume, Elliott/Fibonacci and support/resistance remain validation/context; structural break Shock retained.

### C6 Liquidity / Macro v2
- `FX=-clip(r_USDKRW/0.8%,-1,+1)`.
- KTB3Y/CD91 absolute HTS changes converted from percentage points to bp.
- `RATE=0.70*KTB+0.30*CD`.
- `CASH=clip(DEP5/5%,-1,+1)`.
- `C6=0.35*FX+0.35*RATE+0.30*CASH`.
- Margin Credit/receivables/futures deposits remain context/risk flags.

### C7 Volatility / Derivatives v2
- Removed mandatory VKOSPI MA20 and fair-basis requirements.
- `VOL=-clip(r_VKOSPI/10%,-1,+1)`.
- `FLEAD=clip((r_KOSPI200_Futures-r_KOSPI200_Spot)/0.5%p,-1,+1)`.
- `C7=0.70*VOL+0.30*FLEAD`.
- Raw basis without fair basis, current OI snapshot, isolated option strike/PCR and thin volatility futures remain context only.

### C8 Global Leading v2
- HTS global-market panel is primary numeric C8 source.
- US Futures 40% = Mini S&P500 + Mini Nasdaq.
- Prior US Close 25% = S&P500 + Nasdaq.
- Semiconductor 20% = SOX.
- Asia 15% = Nikkei + China/HK composite.
- `C8=0.40*USF+0.25*USC+0.20*SEMI+0.15*ASIA`.
- Binance remains supporting/confirmation under BINANCE_RULE and is no longer mandatory for numeric C8.
- WTI, Gold, DAX/CAC and Binance positioning remain context.

### Global SAI
- Base weights remain `18/12/15/10/20/10/8/7%` for C1-C8.
- Global VERIFIED/PARTIAL gate remains strict: C5 required, Flow/Internal/Environment represented, >=6/8 usable, >=70% Base Weight coverage.
- Conditional Adaptive Weight architecture unchanged: one family +5pp; two same-direction +3pp each; opposite blocked; 3+ retain Base + Broad Market Shock; max 6pp.
- Action Bands remain ±0.30 / ±0.60.

### Validation / optimization
- Double counting rechecked: institution sub-rows -> C1 context; ADL -> C3 context; volume/ADX -> C5 context; Margin Credit -> C6 context; raw basis/OI/single-strike options -> C7 context; Binance -> C8 confirmation.
- All component formulas bounded to [-1,+1].
- Global SAI remains inside [-1,+1] under Base and allowed adaptive reallocations.
- The supplied 2026-09-10 HTS sample is executable under v2 and yields a near-balanced Base SAI while retaining the material conflict between negative Smart Money/Non-Arbitrage and positive technical/rotation/volatility-normalization evidence.
- Validation = `PASS BY RULE DESIGN`; empirical out-of-sample optimization is not established.

### Backup
- Pre-patch: `Backup/AI_MARKET_MASTER_3.2_SAI_HTS_V2_PREPATCH_BACKUP_2026-09-10.md` / blob `173e86d3d1af1c52130f2abbdf7f191da5319429`.
- Final: `Backup/AI_MARKET_MASTER_3.2_SAI_HTS_V2_FINAL_BACKUP_2026-09-10.md` / blob `95d44a3569d426421b2709b2a1818ef4aaf52550`.

## 2026-09-10 — Global Strategy Action Index v1 Activation
- Activated reproducible global SAI v1 while keeping AI Master Score DATA UNAVAILABLE.
- Added Base weights, Global Missing/Partial Gate, family conflict, Conditional Adaptive Weight and Action Bands.
- Final checkpoint: `Backup/AI_MARKET_MASTER_3.2_SAI_GLOBAL_ACTIVATION_FINAL_BACKUP_2026-09-10.md` / blob `c8316a0fbc746c7ca5867073f39aacf6ef9f7878`.

## 2026-09-10 — SAI-C1~C8 v1 Component Integrations
- Original C1-C8 formulas remain preserved through Git history and individual final backups.
- C1/C4/C5/C6/C7/C8 v1 operational dependencies are superseded by HTS-Operational v2 for current numeric execution.

## 2026-09-08 — Adaptive Validation & Regime Evidence Priority Integration
- Added 8 Market Regimes, E1-E8 Evidence Groups, VH/H/M/L qualitative Evidence Priority, Transition, conflict resolution and Regime re-validation.
- Adaptive Validation remains cross-engine, not a 25th engine.

## 2026-09-08 — Binance Latest Re-query & Fallback Policy
- Added fresh re-query first, LIVE/FALLBACK/STALE and freshness/Confidence rules.
- HTS/KRX remains final Korean-market confirmation.

## 2026-09-07 — 3.2 Unified Stable
- Consolidated authority into six official rule files while preserving 24 internal engines and 8 Dashboard categories.

## Historical
Earlier 3.2 and 3.1 history remain recoverable through Git history / legacy references.