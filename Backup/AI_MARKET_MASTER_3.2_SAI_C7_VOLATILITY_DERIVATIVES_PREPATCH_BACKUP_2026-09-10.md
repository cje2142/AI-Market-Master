# AI Market Master 3.2 — SAI-C7 Volatility / Derivatives Risk Pre-patch Backup

Date: 2026-09-10
Status: NON-AUTHORITATIVE PRE-PATCH DESIGN CHECKPOINT
Purpose: Recovery / regression reference before official C7 integration.

## Current Authority Snapshot
- MASTER_RULE: ea746bf62edbf61521dd26d1855d3b4aadc7b951
- DASHBOARD_RULE: 0ec39d1418edf09098a7a431e904fc5bdfd60230
- SCORING_RULE: f0cd4f4d53d355b48c1c7e70b765933fbf560e91
- TECHNICAL_RULE: b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f
- BINANCE_RULE: f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d
- ADAPTIVE_VALIDATION_RULE: 8833555b261e334b6b0f39d4ce272776fd97af71

## C7 v1 Design
Purpose: quantify domestic volatility and derivatives-price stress without double-counting C1-C6 or E8.

Numeric axes:
1. Volatility Stress `VOL` — mandatory, 60%
2. Basis Stress `BASIS` — optional, 40%

Full formula:
`SAI-C7 = 0.60*VOL + 0.40*BASIS`
Range: `[-1.00,+1.00]`

### VOL
Primary input: VKOSPI spot/official equivalent.
`VOL_REL = VKOSPI_t / VKOSPI_MA20 - 1`
`VOL = -clip(VOL_REL / 0.30,-1,+1)`

VKOSPI futures are confirmation/context only and do not silently replace spot VKOSPI.

### BASIS
Preferred input:
- actual KOSPI200 futures basis
- theoretical/fair basis
- same-session KOSPI200 spot/index denominator

`BasisGap = ActualBasis - FairBasis`
`BG = BasisGap / KOSPI200Spot`
`BASIS = clip(BG / 0.003,-1,+1)`

Raw actual basis sign alone is not sufficient because normal basis depends on rates, dividends and time to expiry.

### Missing / Partial
- VOL + BASIS valid → VERIFIED
- VOL valid, BASIS unavailable → `C7 = VOL` / PARTIAL
- VOL unavailable → DATA UNAVAILABLE

### Context-only / Flags
- KOSPI200 futures OI change: positioning flag, not directional numeric score by itself
- single-strike Call/Put OI or volume: context only, never official market PCR
- full-market Put/Call Ratio: risk/context flag only in v1
- volatility futures: term-structure / confirmation only
- expiry, rollover and major rebalance: `C7 Mechanical Event`

### Conflict
`C7 Conflict: ACTIVE` when VOL and BASIS have opposite signs and both absolute values are at least 0.50. Formula remains unchanged.

### Shock
`C7 Shock: ACTIVE` when a validated condition includes:
- `|VKOSPI/VKOSPI_MA20 - 1| >= 45%`, or
- `|BasisGap/KOSPI200Spot| >= 0.45%`, or
- validated same-direction extreme VOL/BASIS deterioration supported by derivatives stress context.

Shock feeds Change Detection / Transition / Regime re-validation only. No automatic Regime change, portfolio action, global SAI override or permanent weight change.

### Anti-double-counting
- C1/E1 Smart Money stays separate
- C2/E2 Program stays separate
- C3/E3 Breadth stays separate
- C4/E4 Sector Leadership stays separate
- C5/E5 Technical stays separate
- C6/E6 Liquidity/Macro stays separate
- Binance OI/Funding/Long-Short and TMF/SPY/QQQ/BTC/EWY/SOXL remain E8 and are not re-scored in C7
- OI is not direction by itself
- VKOSPI spot relative stress is scored once; its absolute level and futures are contextual only

### Anti-circularity
C7 cannot choose a Market Regime, use that Regime to alter C7 weights, and then use altered C7 as the sole reason to reconfirm the same Regime. VH/H/M/L remains qualitative only.

## Validation Cases
A. VOL=-1, BASIS=-1 → C7=-1.00
B. VOL=+1, BASIS=+0.50 → C7=+0.80
C. VOL=-0.80, BASIS=+0.70 → C7=-0.20 + Conflict
D. VOL=-0.60, BASIS unavailable → C7=-0.60 / PARTIAL
E. VOL unavailable, BASIS=-1 → DATA UNAVAILABLE
F. OI surge alone → no direct C7 direction
G. one ATM Call/Put strike only → no official PCR
H. volatility futures move without VKOSPI spot → context only
I. expiry/rollover distortion → Mechanical Event; no structural Regime conclusion by itself
J. 45% VKOSPI-vs-MA20 stress → C7 Shock while numeric range remains clipped.

## Readiness
Architecture: VERIFIED BY DESIGN
Formula: DEFINED v1
Missing/Partial: VERIFIED BY RULE
Conflict/Shock/Mechanical Event: VERIFIED BY RULE
Anti-double-counting: PASS
Anti-circularity: PASS
E7/E8 boundary: PASS
Global Strategy Action Index remains DATA UNAVAILABLE.
