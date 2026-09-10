# AI Market Master 3.2 — SAI HTS-Operational v2 Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED RULE-DESIGN SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery and regression checkpoint after redesigning C1-C8 for the user's repeatably available HTS data.

## 1. Final State
- `Strategy Action Index`: FORMULA ACTIVATED / RUNTIME DATA-DEPENDENT
- `AI Master Score`: DATA UNAVAILABLE
- Active component schema: HTS-Operational v2
- 24 Analysis Engines unchanged
- 8 Dashboard categories unchanged
- six official Authority files unchanged in count
- HTS/KRX remains final Korean-market confirmation
- Binance remains global leading/supporting

## 2. Post-patch Authority Snapshot
- MASTER_RULE: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
- DASHBOARD_RULE: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
- SCORING_RULE: `48f5cfea4fabd201294f3df047e6f1714f2f353d`
- TECHNICAL_RULE: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
- BINANCE_RULE: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
- ADAPTIVE_VALIDATION_RULE: `8833555b261e334b6b0f39d4ce272776fd97af71`

Supporting files at final-backup creation:
- VERSION_STATUS: `0320663a25db71ee72f0020c44c357a27485def4`
- CHANGELOG: `3102846c3a5c2d015c2507b1f0ec50dff45ee911`

Pre-patch checkpoint:
- `Backup/AI_MARKET_MASTER_3.2_SAI_HTS_V2_PREPATCH_BACKUP_2026-09-10.md`
- blob SHA: `173e86d3d1af1c52130f2abbdf7f191da5319429`

## 3. C1 Smart Money v2
Cash participant share:
`G_C=|P_C|+|F_C|+|I_C|`
`D_FC=F_C/G_C`
`A_C=clip((G_C/KOSPITradedValue)/0.05,0,1)`
`FC=A_C*D_FC`

Futures participant share:
`G_F=|P_F|+|F_F|+|I_F|`
`FF=F_F/G_F`

`C1=0.55*FC+0.45*FF`

Optimization added before final seal: the cash-activity multiplier prevents tiny absolute flows from producing a large score only because Foreign dominates a small net-flow denominator. Institution sub-rows remain context and futures OI is not mixed with flow units.

## 4. C2 Program Flow v2
`ARB_R=ARB/KOSPITradedValue`
`NONARB_R=NONARB/KOSPITradedValue`
`N_ARB=clip(ARB_R/0.03,-1,+1)`
`N_NONARB=clip(NONARB_R/0.10,-1,+1)`
`C2=0.25*N_ARB+0.75*N_NONARB`

Non-Arbitrage remains structural core. Mechanical-event guard remains binding.

## 5. C3 Breadth v2
`B_K=(ADV_K-DEC_K)/(ADV_K+DEC_K)`
`N_K=clip(B_K/0.40,-1,+1)`
`B_Q=(ADV_Q-DEC_Q)/(ADV_Q+DEC_Q)`
`N_Q=clip(B_Q/0.40,-1,+1)`
`C3=0.70*N_K+0.30*N_Q`

KOSPI is mandatory, KOSDAQ confirms. Absolute ADL remains context to avoid duplicate breadth scoring.

## 6. C4 Market Leadership / Rotation v2
Large-cap relative axis:
`LC_RAW=avg(KOSPI100,KOSPI200,KTOP30,KRX100 valid returns)-KOSPI return`
`N_LC=clip(LC_RAW/0.005,-1,+1)`

Growth/rotation axis:
`GR_RAW=avg(KOSDAQ,KOSDAQ150 valid returns)-KOSPI return`
`N_GR=clip(GR_RAW/0.015,-1,+1)`

`C4=0.40*N_LC+0.60*N_GR`

Numeric C4 no longer requires eight sector benchmark indices. Full sector leadership remains qualitative E4 context. Positive C4 is relative leadership/rotation support, not automatic broad-market bullishness.

## 7. C5 Technical Structure v2
Trend Position 55%:
- MA20/50/60/200
- VWAP20/50/60/200
- each anchor +1 above +0.2%, -1 below -0.2%, otherwise 0

Momentum 25%:
`RSI_N=clip((RSI9-50)/20,-1,+1)`
MACD direction = +1 / 0 / -1 from MACD vs Signal plus Oscillator sign.
`MOM=0.50*RSI_N+0.50*MACD_D`

Session Structure 20%:
`CLV=2*(Close-Low)/(High-Low)-1`
`DAY=clip(KOSPI daily return/0.015,-1,+1)`
`SES=0.60*CLV+0.40*DAY`

`C5=0.55*TP+0.25*MOM+0.20*SES`

ADX/volume/Elliott/Fibonacci/support-resistance remain validation/context. Structural closing break remains a Shock input.

## 8. C6 Liquidity / Macro v2
`FX=-clip(r_USDKRW/0.008,-1,+1)`
`KTB=-clip(dKTB3Y_bp/10,-1,+1)`
`CD=-clip(dCD91_bp/5,-1,+1)`
`RATE=0.70*KTB+0.30*CD`
`DEP5=Deposit_t/Deposit_t-5obs-1`
`CASH=clip(DEP5/0.05,-1,+1)`
`C6=0.35*FX+0.35*RATE+0.30*CASH`

HTS rate `대비` is interpreted as percentage-point change and explicitly converted to bp. Margin Credit, receivables and futures deposits remain context/risk flags.

## 9. C7 Volatility / Derivatives v2
`VOL=-clip(r_VKOSPI/0.10,-1,+1)`
`FLEAD=clip((r_KOSPI200_Futures-r_KOSPI200_Spot)/0.005,-1,+1)`
`C7=0.70*VOL+0.30*FLEAD`

Removed mandatory VKOSPI-MA20 and fair-basis dependencies.
Raw basis without fair basis, OI snapshot without change, isolated Call/Put strike, incomplete PCR and thin volatility futures remain context only.

## 10. C8 Global Leading v2
Primary numeric source = recurring HTS global-market panel.

US Futures 40%:
`SPF=clip(r_MiniSP500/0.0075,-1,+1)`
`NQF=clip(r_MiniNASDAQ/0.010,-1,+1)`
`USF=0.45*SPF+0.55*NQF`

Prior US Close 25%:
`SPX=clip(r_SP500/0.015,-1,+1)`
`NAS=clip(r_NASDAQ/0.020,-1,+1)`
`USC=0.50*SPX+0.50*NAS`

Semiconductor 20%:
`SEMI=clip(r_SOX/0.025,-1,+1)`

Asia 15%:
Nikkei + China/HK composite; China/HK base weights Shanghai 25%, Shenzhen 25%, Hang Seng 50%.

`C8=0.40*USF+0.25*USC+0.20*SEMI+0.15*ASIA`

Binance is supporting/confirmation only for numeric C8 v2. WTI, Gold, DAX/CAC and Binance positioning remain context.

## 11. Missing / Partial Gate Summary
Each C1-C8 has explicit VERIFIED/PARTIAL/DATA UNAVAILABLE rules. Missing never equals zero.

Global VERIFIED = all C1-C8 VERIFIED.
Global PARTIAL requires:
1. C5 usable
2. Flow family represented by C1 or C2
3. Internal family represented by C3 or C4
4. Environment family represented by C6/C7/C8
5. at least 6/8 components usable
6. at least 70% original Base Weight coverage

Any component PARTIAL forces Global PARTIAL. Adaptive numeric reweighting is blocked in PARTIAL mode.

## 12. Global SAI v2
Base weights remain unchanged:
C1 18%, C2 12%, C3 15%, C4 10%, C5 20%, C6 10%, C7 8%, C8 7%.

`SAI_Base=0.18*C1+0.12*C2+0.15*C3+0.10*C4+0.20*C5+0.10*C6+0.08*C7+0.07*C8`
Range `[-1,+1]`.

Family distribution remains Flow 30%, Internal 25%, Structure 20%, Environment 25%.

Conditional Adaptive Weight remains bounded:
- one qualifying family +5pp
- two same-direction qualifying families +3pp each
- opposite events blocked
- 3+ qualifying families retain Base + Broad Market Shock
- max total reallocation 6pp
- no VH/H/M/L numeric conversion

Action Bands remain ±0.30 / ±0.60 and are execution-bias labels, not automatic orders.

## 13. Double-Counting Verification
PASS:
- Institution sub-rows are not re-added after Institution-total in C1.
- Program stays in C2, not C1.
- ADL absolute level is not re-scored after C3 breadth.
- C4 uses index-segment relative leadership; sector detail remains qualitative E4 context.
- Volume/ADX are C5 confirmation, not extra score axes.
- Margin Credit/receivables/futures deposits are C6 context.
- Raw basis/OI/single-strike options are C7 context.
- SOX is scored once in C8.
- Binance proxies and positioning are not re-added to numeric C8 v2.
- C8 remains one E8 Evidence Group for adaptive consensus.

## 14. Cross-Authority Verification
- MASTER_RULE: PASS — HTS/KRX priority, six-authority structure, 24 engines, portfolio safeguards and score anti-hallucination preserved.
- DASHBOARD_RULE: PASS — exactly 8 categories preserved; official SAI may be shown only when SCORING permits it.
- TECHNICAL_RULE: PASS — C5 uses recurring technical inputs while TECHNICAL retains Elliott/Fibonacci/support-resistance ownership and final technical confirmation.
- BINANCE_RULE: PASS — Binance remains global leading/supporting; fixed 8-symbol workflow and LIVE/FALLBACK/STALE rules remain intact. C8 v2 does not require Binance numeric reuse.
- ADAPTIVE_VALIDATION_RULE: PASS — E1-E8 ownership, qualitative VH/H/M/L, Regime/Transition and anti-circularity remain intact.
- SCORING_RULE: PASS — sole numeric authority; v2 formulas and Global SAI gate explicitly defined.

No new Authority file, 25th engine or ninth Dashboard category created.

## 15. Regression / Stress Verification
PASS BY FORMULA / RULE DESIGN:
- every C1-C8 formula is bounded to [-1,+1]
- Global Base component weights sum exactly 1.00
- Family weights sum exactly 1.00
- allowed one-family +5pp and two-family +3pp/+3pp reallocations preserve non-negative weights and total 1.00
- all 256 C1-C8 corner combinations remain inside [-1,+1]
- Missing never neutralized
- PARTIAL blocks adaptive weighting
- Conflict remains visible even when arithmetic SAI is near zero

Provided 2026-09-10 HTS sample sanity result:
- C1 ≈ -0.61
- C2 ≈ -0.68
- C3 ≈ -0.03
- C4 ≈ +0.51
- C5 ≈ +0.52
- C6 ≈ -0.23
- C7 ≈ +0.33
- C8 ≈ -0.12
- Base SAI ≈ -0.05

Interpretation: Balanced/Hold arithmetic with meaningful internal conflict—Smart Money/Non-Arbitrage negative versus technical recovery/rotation/volatility normalization positive. This is not a claim of market-performance accuracy.

## 16. Calibration Caveat
`VERIFIED BY RULE DESIGN` does not mean statistically optimized.
Not empirically established:
- normalization saturation values
- Shock thresholds
- C1 cash-activity 5% saturation
- component internal weights
- Global Base Weights
- Action Bands

Future out-of-sample validation may justify calibration changes, but no automatic self-reweighting or silent historical optimization is permitted.

## 17. Final State
- C1-C8 HTS-Operational v2: FORMULA DEFINED
- Strategy Action Index v2: FORMULA ACTIVATED / runtime data-dependent
- AI Master Score: DATA UNAVAILABLE
- unresolved Authority conflict: NONE
- operational fit to repeatable user HTS dataset: VERIFIED BY RULE DESIGN

Reliability > Speed.
Missing != Neutral.
Conflict is information, not noise.