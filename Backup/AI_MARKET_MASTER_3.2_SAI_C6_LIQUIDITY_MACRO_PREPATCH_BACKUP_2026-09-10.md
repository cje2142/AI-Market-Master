# AI Market Master 3.2 — SAI-C6 Liquidity / Macro Pre-Patch Backup

Date: 2026-09-10
Status: PRE-PATCH BACKUP / DESIGN VERIFIED
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery checkpoint before formal SAI-C6 integration into SCORING_RULE.

## 1. Design State
SAI-C6 Liquidity / Macro v1 is ready for formal integration subject to safe preservation of C1-C5 and cross-authority validation.

Global numeric state remains:
- AI Master Score = DATA UNAVAILABLE
- Strategy Action Index = DATA UNAVAILABLE

## 2. C6 Purpose
Measure domestic financial-condition support or pressure on Korean equities using three daily/near-daily axes while avoiding direct double-counting of investor flow, program flow, breadth, sector leadership, technical price structure, derivatives risk and Binance/global-leading data.

## 3. Numeric Inputs
C6-A FX Pressure
- USD/KRW 5-trading-day percentage change.
- FX_raw = USDKRW_t / USDKRW_t-5 - 1
- FX = -clip(FX_raw / 0.020, -1,+1)
- USD/KRW +2% over 5d or more => FX=-1.00
- USD/KRW -2% over 5d or more => FX=+1.00

C6-B Rate Pressure
- Korea Treasury 3Y yield 5-trading-day change in basis points.
- dY5 = Yield3Y_t - Yield3Y_t-5
- RATE = -clip(dY5 / 20bp, -1,+1)
- +20bp or more => RATE=-1.00
- -20bp or less => RATE=+1.00

C6-C Cash Liquidity
- customer deposits / investor cash deposits 5-trading-day percentage change.
- DEP5 = Deposit_t / Deposit_t-5 - 1
- CASH = clip(DEP5 / 0.05, -1,+1)
- +5% or more => CASH=+1.00
- -5% or less => CASH=-1.00

## 4. C6 v1 Formula
SAI-C6 = 0.35*FX + 0.35*RATE + 0.30*CASH
Range: [-1.00,+1.00]

Internal weights:
- FX Pressure 35%
- Rate Pressure 35%
- Cash Liquidity 30%

These are C6-internal weights only and do not define the future global SAI weight of C6.

## 5. Missing / Partial Rules
Full data => VERIFIED when source/freshness/unit validation passes.

FX missing only:
C6 = 0.5385*RATE + 0.4615*CASH => PARTIAL

RATE missing only:
C6 = 0.5385*FX + 0.4615*CASH => PARTIAL

CASH missing only:
C6 = 0.50*FX + 0.50*RATE => PARTIAL

Minimum requirement: at least two distinct valid C6 axes, with at least one of FX or RATE present.
One axis alone, or CASH alone, => DATA UNAVAILABLE.
Missing values are never converted to zero/Neutral.

## 6. Margin Credit Boundary
Margin credit is NOT a direct numeric term in C6 v1 because higher credit can simultaneously represent liquidity expansion and leverage risk.

Use qualitative/context flags:
- deposits down + margin credit up => Credit Stress: ACTIVE
- deposits up + margin credit surges => Credit Overheat Watch
- deposits up + margin credit stable => Liquidity Quality: HEALTHY
- deposits down + margin credit down => Liquidity Contraction / Deleveraging

Margin credit may feed E6 qualitative interpretation and E7 risk cross-validation when leverage risk is material, but is not double-scored numerically.

## 7. Structural Macro Context Boundary
Policy rate, M2 and lower-frequency macro liquidity variables remain structural context in C6 v1 and are not direct daily numeric terms because their update frequency differs materially from FX/rates/deposits.

They may alter qualitative interpretation or trigger Change Detection when a verified structural policy/liquidity regime shift occurs, but they do not silently alter C6 weights.

## 8. Conflict Rule
Raise C6 Conflict: ACTIVE when two available C6 numeric axes have opposite signs and both absolute normalized values are >=0.50.

Also disclose important composition conflict such as:
- FX/RATE improving while CASH materially deteriorates
- FX strengthening while domestic rates sharply tighten

Keep the formula unchanged and pass the conflict to ADAPTIVE_VALIDATION_RULE / Change Detection. Do not interpret a near-zero aggregate as absence of information.

## 9. Shock Rule
Raise C6 Shock: ACTIVE when any validated raw input exceeds the v1 shock threshold:
- |USD/KRW 5d change| >= 2.5%
- |Korea Treasury 3Y 5d change| >= 30bp
- |customer deposits 5d change| >= 7.5%

Shock is a Change Detection / Transition / Weight Shift candidate only. It is not an automatic Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 10. Anti-Double-Counting
Excluded from C6 numeric formula:
- Foreign/Institution flow => C1/E1
- Program/Arbitrage/Non-Arbitrage => C2/E2
- Breadth/ADL => C3/E3
- Sector leadership => C4/E4
- Price/MA/VWAP/technical => C5/E5
- Options/OI/volatility => E7
- Binance/TMF/SPY/QQQ/BTC/EWY/SOXL => E8

Korea Treasury 3Y in C6 represents domestic financial conditions. TMF remains E8 global-leading context and must not be added to C6 numerically.

## 11. Anti-Circularity
Required separation:
Validated domestic macro/liquidity data -> C6 calculation

and independently:
Raw HTS + other Evidence -> Preliminary Regime -> Adaptive Priority -> Transition / Conflict -> Regime Re-validation

C6 cannot choose a Regime, use that Regime to alter its own numeric weights, and then use the altered C6 as the sole reason to reconfirm the same Regime.
VH/H/M/L remains qualitative and must not be converted into numeric C6 weights.

## 12. Validation Cases
A. USD/KRW -2%, 3Y -20bp, deposits +5% => FX/RATE/CASH all +1 => C6=+1.00.
B. USD/KRW +2%, 3Y +20bp, deposits -5% => all -1 => C6=-1.00.
C. FX=+1, RATE=-1, CASH=0 => C6=0 but C6 Conflict ACTIVE.
D. CASH missing, FX=+0.6, RATE=+0.4 => partial C6=+0.50.
E. FX missing, RATE=-0.8, CASH=-0.5 => partial C6≈-0.6615.
F. RATE missing, FX=+0.8, CASH=-0.4 => partial C6≈+0.2462 with conflict disclosure when threshold condition is met.
G. only CASH available => DATA UNAVAILABLE.
H. margin credit surge alone => no numeric C6 contribution; qualitative Credit Overheat Watch only.
I. USD/KRW 5d +3% => C6 Shock ACTIVE while FX stays clipped at -1.00.
J. policy rate change with stale/unchanged daily market axes => structural context; no silent numeric insertion.

Result: PASS by design.

## 13. Integration Guardrails
- SCORING_RULE remains sole numeric authority.
- ADAPTIVE_VALIDATION_RULE remains E6 qualitative/adaptive interpretation authority.
- MASTER/DASHBOARD/TECHNICAL/BINANCE authorities remain unchanged.
- exactly six official authority files remain.
- 24 internal engines remain unchanged.
- 8 Dashboard categories remain unchanged.
- Global Strategy Action Index remains DATA UNAVAILABLE after C6 until global aggregation, missing/partial handling, Action Bands and regression validation are formally complete.

Reliability > Speed.