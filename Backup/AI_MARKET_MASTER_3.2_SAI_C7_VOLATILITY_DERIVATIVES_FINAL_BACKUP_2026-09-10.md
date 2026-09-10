# AI Market Master 3.2 — SAI-C7 Volatility / Derivatives Risk Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression verification for the SAI-C7 Volatility / Derivatives Risk integration.

## 1. Integration Result
`SAI-C7 Volatility / Derivatives Risk` has been formally integrated into `SCORING_RULE` as the seventh numeric sub-component for a future Strategy Action Index.

Official global numeric state remains:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

C1-C7 are component-level formulas only. Global aggregation, global missing/partial handling, final range/Action Bands and regression validation are still required before global Strategy Action Index activation.

## 2. Six Official Authority Snapshot
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `a937363a88aeb3373449f6e31964c00db84c4345`
   - C1-C7 numeric component authority
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`

Supporting files before final-backup registration:
- `VERSION_STATUS.md`: `d666b3a31f9c9bc271f4bd559e0b4f060e9f392c`
- `CHANGELOG.md`: `b08bf5b21363c2139ab893d712658dcac4abab36`

## 3. C7 Numeric Structure
Numeric axes:
- Volatility Stress `VOL`: 60%, mandatory
- Fair-value-adjusted KOSPI200 Basis Stress `BASIS`: 40%, optional

Full formula:
`SAI-C7 = 0.60*VOL + 0.40*BASIS`
Range: `[-1.00,+1.00]`

### VOL
Primary input: VKOSPI spot / validated official equivalent.
`VOL_REL = VKOSPI_t / VKOSPI_MA20 - 1`
`VOL = -clip(VOL_REL / 0.30,-1,+1)`

VKOSPI absolute level is context only. VKOSPI futures are term-structure/confirmation context and do not silently replace spot VKOSPI.

### BASIS
Required when used:
- Actual KOSPI200 futures basis
- Theoretical/Fair basis
- same-session KOSPI200 spot/index denominator

`BasisGap = ActualBasis - FairBasis`
`BG = BasisGap / KOSPI200Spot`
`BASIS = clip(BG / 0.003,-1,+1)`

Raw actual basis sign alone is prohibited as a directional score because normal basis depends on rates, dividends and time to expiry.

## 4. Missing / Partial Rule
- VOL + BASIS valid → eligible VERIFIED when source/session/unit validation passes
- VOL valid + BASIS unavailable → `C7=VOL` / PARTIAL
- VOL unavailable/invalid → `SAI-C7 = DATA UNAVAILABLE`, even if BASIS is available

Missing data is never neutralized. VOL-only PARTIAL is predefined, not silent renormalization.

## 5. Context / Flag Boundary
Not direct numeric terms in C7 v1:
- KOSPI200 futures OI / OI change
- isolated Call/Put strike OI or volume
- full-market Put/Call Ratio
- volatility futures / term structure
- rollover / expiry positioning

Reasoning boundary:
- OI direction is ambiguous without price/position context
- one option strike cannot represent market PCR
- PCR can reflect fear/hedging or contrarian extremes
- volatility futures contain expiry/term-structure effects

Permitted contextual labels include new short/hedge expansion, new long expansion, long liquidation, volatility confirmation and mechanical-event distortion.

## 6. Conflict / Shock / Mechanical Event
`C7 Conflict: ACTIVE` when VOL and BASIS have opposite signs and both `|value| >= 0.50`. Formula remains unchanged; decision-relevant conflict is disclosed and passed to Adaptive Validation / Change Detection.

`C7 Shock: ACTIVE` when validated conditions include:
- `|VKOSPI/VKOSPI_MA20 - 1| >= 45%`, or
- `|BasisGap/KOSPI200Spot| >= 0.45%`, or
- VOL and BASIS are both <=-0.80 with independent derivatives-risk confirmation.

`C7 Mechanical Event: ACTIVE` for derivatives expiry, rollover, major index/sector rebalance or comparable market-structure event that can distort OI, option prices or basis.

Shock and Mechanical Event feed Change Detection / Transition / Regime re-validation only. They do not automatically change Market Regime, global SAI, portfolio action or permanent Base Weight.

## 7. Anti-Double-Counting / Anti-Circularity
- VKOSPI relative stress is scored once in VOL
- VKOSPI absolute level / volatility futures are contextual only
- fair-value-adjusted KOSPI200 basis is scored once in BASIS
- OI / PCR / isolated strikes remain context or flags
- C1/E1 Smart Money remains separate
- C2/E2 Program remains separate
- C3/E3 Breadth remains separate
- C4/E4 Sector Leadership remains separate
- C5/E5 Technical remains separate
- C6/E6 Liquidity/Macro remains separate
- Binance OI/Funding/Long-Short and TMF/SPY/QQQ/BTC/EWY/SOXL remain E8 and are not re-scored in C7

Anti-circularity preserved:
`Validated Domestic Volatility/Derivatives Data -> C7 Calculation`
remains separate from
`Raw HTS + other Evidence -> Preliminary Regime -> Adaptive Priority -> Transition/Conflict -> Regime Re-validation`.

C7 cannot select a Regime, alter itself from that Regime and then use altered C7 as the sole reason to reconfirm the same Regime. VH/H/M/L remains qualitative only.

## 8. Validation Cases
A. VOL=-1, BASIS=-1 → C7=-1.00
B. VOL=+1, BASIS=+0.50 → C7=+0.80
C. VOL=-0.80, BASIS=+0.70 → C7=-0.20 + Conflict
D. VOL=-0.60, BASIS unavailable → C7=-0.60 / PARTIAL
E. VOL unavailable, BASIS=-1 → DATA UNAVAILABLE
F. OI surge alone → no directional C7 numeric contribution
G. one ATM Call/Put strike only → no official PCR
H. volatility futures move without VKOSPI spot → context only; cannot create VERIFIED C7
I. expiry/rollover distortion → Mechanical Event; no structural Regime conclusion by itself
J. `|VKOSPI/MA20-1|>=45%` → C7 Shock while VOL remains clipped at ±1

Result: PASS BY RULE DESIGN.

## 9. Cross-Authority Validation
- MASTER architecture: PASS
- exactly 24 engines preserved: PASS
- exactly 8 Dashboard categories preserved: PASS
- E7 adaptive ownership preserved: PASS
- E8/Binance boundary preserved: PASS
- Technical authority unchanged: PASS
- HTS/KRX priority preserved: PASS
- no seventh authority file introduced: PASS
- global SAI activation firewall preserved: PASS
- Global Strategy Action Index remains DATA UNAVAILABLE: PASS

## 10. Final Seal
C7 Architecture: VERIFIED
C7 Formula: DEFINED v1
VOL mandatory rule: VERIFIED
BASIS optional/fair-value adjustment: VERIFIED BY DESIGN
Missing/Partial: VERIFIED
Conflict/Shock/Mechanical Event: VERIFIED
Anti-double-counting: PASS
Anti-circularity: PASS
C1-C6 regression boundary: PASS
E7/E8 authority conflict: NONE
Global SAI: DATA UNAVAILABLE
