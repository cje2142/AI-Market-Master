# AI Market Master 3.2 — SAI-C6 Liquidity / Macro Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression verification for the SAI-C6 Liquidity / Macro integration.

## 1. Integration Result
`SAI-C6 Liquidity / Macro` has been formally integrated into `SCORING_RULE` as the sixth numeric sub-component for a future Strategy Action Index.

Official global numeric state remains:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

Defined component-level formulas now cover C1-C6. No component or combination of C1-C6 activates the global Strategy Action Index until global aggregation, global missing/partial handling, range/Action Bands and regression validation are formally complete.

## 2. Six Official Authority Snapshot
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `f0cd4f4d53d355b48c1c7e70b765933fbf560e91`
   - C1-C6 numeric component authority
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`

Supporting files at final-backup creation:
- `VERSION_STATUS.md`: `b9e94b1dd950d76d0abd6c57270b547f2a59ecfd`
- `CHANGELOG.md`: `c77c8c020292dc9719007a4c40ce97a4f7b70d93`

## 3. C6 Numeric Structure
Three numeric axes:
- FX Pressure = 35%
- Domestic Rate Pressure = 35%
- Cash Liquidity = 30%

Full formula:
`SAI-C6 = 0.35*FX + 0.35*RATE + 0.30*CASH`

Range:
`[-1.00,+1.00]`

### FX Pressure
`FX_raw = USDKRW_t / USDKRW_t-5 - 1`
`FX = -clip(FX_raw / 0.020,-1,+1)`

### Domestic Rate Pressure
Let `dY5_bp` = Korea Treasury 3Y current yield minus 5-observation-prior yield in basis points.
`RATE = -clip(dY5_bp / 20,-1,+1)`

### Cash Liquidity
`DEP5 = Deposit_t / Deposit_t-5 - 1`
`CASH = clip(DEP5 / 0.05,-1,+1)`

## 4. Timeframe / Point-in-Time Standard
Official C6 v1 uses latest completed Korean-market daily observations for FX/rates.
Intraday current FX/rate values may be shown only as `C6 Intraday Preview` and cannot overwrite completed-daily C6 by themselves.

Customer Deposits use the latest officially published observation actually available at execution time. Its observation date must be disclosed when different from the market reference date. Its 5-observation change uses its own valid series dates.

Unknown source date, invalid unit or invalid 5-observation comparison makes the affected input unavailable. No look-ahead/backfill from unavailable future information is allowed.

## 5. Missing / Partial Rules
Full:
- FX + RATE + CASH valid => VERIFIED when source/date/unit validation passes.

FX missing only:
`C6 = 0.5385*RATE + 0.4615*CASH` => PARTIAL.

RATE missing only:
`C6 = 0.5385*FX + 0.4615*CASH` => PARTIAL.

CASH missing only:
`C6 = 0.50*FX + 0.50*RATE` => PARTIAL.

Minimum gate:
- at least two distinct C6 axes valid
- at least one of FX or RATE present

One axis alone, CASH alone or invalid comparison => DATA UNAVAILABLE.
Missing values are never converted to zero/Neutral.

## 6. Margin Credit Boundary
Margin Credit is not a direct numeric term in C6 v1 because increasing credit can represent both deployable buying power and leverage fragility.

It remains qualitative E6/E7 context. No fixed numeric bonus/penalty is adopted in C6 v1.

Context examples:
- deposits weakening + margin credit rising => leverage-quality / credit-stress warning
- deposits strengthening + margin credit rising rapidly => liquidity expansion with overheat watch
- deposits strengthening + margin credit stable => healthier liquidity-quality context
- deposits and margin credit contracting => deleveraging/liquidity-contraction context

## 7. Structural Macro Context Boundary
Policy Rate, M2 and other lower-frequency liquidity/macro series are Structural Macro Context, not direct daily C6 terms.
They may inform E6 interpretation or Change Detection when verified structural changes occur, but do not silently enter C6 or change weights ad hoc.

## 8. Conflict Rule
`C6 Conflict: ACTIVE` when any two available numeric C6 axes have opposite signs and both satisfy `|value| >= 0.50`.

When active:
- formula remains unchanged
- component conflict is disclosed
- near-zero aggregate is not interpreted as absence of information
- conflict feeds ADAPTIVE_VALIDATION_RULE / Change Detection
- no ad hoc weight change

## 9. Shock Rule
`C6 Shock: ACTIVE` when any validated raw input reaches:
- |USD/KRW 5-observation change| >= 2.5%
- |Korea Treasury 3Y 5-observation change| >= 30bp
- |Customer Deposits 5-observation change| >= 7.5%

Shock feeds Change Detection / Transition / Weight Shift candidate logic only. It does not automatically change Market Regime, global SAI, portfolio action or permanent Base Weight.

## 10. Anti-Double-Counting
- Foreign/Institution flow => C1/E1
- Program flow => C2/E2
- Breadth/ADL => C3/E3
- Sector Leadership => C4/E4
- Technical Structure => C5/E5
- FX/rates/deposits => C6/E6
- Margin Credit => contextual E6/E7 only in v1
- Options/OI/Volatility => E7
- Binance/TMF/SPY/QQQ/BTC/EWY/SOXL/global proxies => E8

Korea Treasury 3Y in C6 measures domestic financial conditions. TMF remains E8 global-leading context and is not re-scored numerically inside C6.

## 11. Anti-Circularity
Required separation:
`Validated Domestic Macro/Liquidity Data -> C6 Calculation`

and independently:
`Raw HTS + other Evidence -> Preliminary Regime -> Adaptive Priority -> Transition / Conflict -> Regime Re-validation`

C6 cannot select a Regime, use that Regime to alter its numeric weights, then use the altered C6 as sole confirmation of that same Regime.
VH/H/M/L remains qualitative only.

## 12. Validation Cases
A. USD/KRW -2%, 3Y -20bp, deposits +5% => C6=+1.00.
B. USD/KRW +2%, 3Y +20bp, deposits -5% => C6=-1.00.
C. FX=+1,RATE=-1,CASH=0 => C6=0 + Conflict ACTIVE.
D. CASH missing; FX=.60,RATE=.40 => C6=.50 / PARTIAL.
E. FX missing; RATE=-.80,CASH=-.50 => C6≈-.6615 / PARTIAL.
F. RATE missing; FX=.80,CASH=-.40 => C6≈+.2462 / PARTIAL; conflict only if both opposing magnitudes meet threshold.
G. only CASH available => DATA UNAVAILABLE.
H. margin-credit surge alone => no direct numeric C6 term.
I. USD/KRW 5-observation +3% => FX clipped -1 + C6 Shock ACTIVE.
J. policy-rate/M2 update => structural context only, no silent numeric insertion.

Result: PASS.

## 13. Cross-Authority Verification
### MASTER_RULE
- exactly six authority roles preserved
- 24 engines unchanged
- Engine 06 Global Liquidity retained
- HTS/KRX priority preserved
- SCORING_RULE remains sole numeric authority
- no new engine created
- PASS

### DASHBOARD_RULE
- exactly eight user-facing categories preserved
- Liquidity remains category 6
- no ninth C6 category created
- official global AI Master Score / Strategy Action Index remain DATA UNAVAILABLE
- PASS

### ADAPTIVE_VALIDATION_RULE
- E6 remains `USD/KRW, rates, deposits, margin/credit, liquidity conditions`
- E6 adaptive priority remains qualitative VH/H/M/L
- C6 cannot determine Regime alone
- no numeric conversion of adaptive priority
- PASS

### TECHNICAL_RULE
- no technical indicator imported into C6 numeric formula
- C5/E5 ownership remains separate
- PASS

### BINANCE_RULE
- TMF and other Binance symbols remain E8/global-leading support
- no Binance proxy enters C6 numeric formula
- HTS/KRX remains Korean-market final confirmation
- PASS

## 14. Scoring Rule Consolidation Verification
During C6 integration, SCORING_RULE was consolidated to reduce repeated interim status blocks while preserving the active numeric definitions and safety gates for C1-C5 and adding C6.

Verified preserved component identities/formulas:
- C1 Smart Money: 40/40/20, mandatory Foreign Cash/Futures, predefined Institution-missing PARTIAL
- C2 Program Flow: 30/70 Arbitrage/Non-Arbitrage, Non-Arbitrage structural core
- C3 Breadth: 70/30 KOSPI/KOSDAQ, KOSPI mandatory
- C4 Sector/Leadership: 60/40 SD/RL, fixed 8-sector universe, 75% completeness gate
- C5 Technical: 50/30/20 PS/SR/TP, PS mandatory, closing-confirmed structure
- C6 Liquidity/Macro: 35/35/30 FX/RATE/CASH

Global activation gate and DATA UNAVAILABLE firewall remain intact.

## 15. Integration Commits
Pre-patch backup:
`28af6c394f689b40f9c0592267d7b34291cd1194`

SCORING_RULE C6 integration/consolidation:
`00954592ec3bd3775e498f717c34dc2010f5107f`

VERSION_STATUS initial C6 registration:
`df7f158eb6f2d8bfad723aedc098df265de39ad2`

CHANGELOG initial C6 registration:
`d9083f3579c3b40399dc96643091ffdc7a1844bc`

## 16. Final Verification State
- C6 purpose/boundary: VERIFIED
- FX transform: VERIFIED BY RULE
- RATE transform: VERIFIED BY RULE
- CASH transform: VERIFIED BY RULE
- 35/35/30 internal weights: DEFINED v1
- point-in-time/freshness boundary: VERIFIED
- missing/partial rules: VERIFIED BY RULE
- Margin Credit non-numeric boundary: VERIFIED
- Policy Rate/M2 structural-context boundary: VERIFIED
- Conflict threshold: VERIFIED BY RULE
- Shock thresholds: VERIFIED BY RULE
- anti-double-counting: VERIFIED
- anti-circularity: VERIFIED
- validation cases: PASS
- C1-C5 preservation after consolidation: VERIFIED BY RULE REVIEW
- six-authority architecture: PRESERVED
- 24-engine architecture: PRESERVED
- 8-category Dashboard: PRESERVED
- global Strategy Action Index activation: NOT YET ALLOWED
- unresolved authority conflict: NONE FOUND

Reliability > Speed.
No complete global formula = no global score.
