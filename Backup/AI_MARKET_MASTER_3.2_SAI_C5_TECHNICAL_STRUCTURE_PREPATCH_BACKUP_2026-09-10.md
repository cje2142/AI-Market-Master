# AI Market Master 3.2 — SAI-C5 Technical Structure Pre-Patch Backup

Date: 2026-09-10
Status: PRE-PATCH DESIGN CHECKPOINT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Preserve the verified SAI-C5 design before official SCORING_RULE integration.

## 1. Current Official State Before C5 Patch
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C4 Sector / Leadership`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C5 Technical Structure`: NOT YET IN OFFICIAL SCORING_RULE
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

Current six-authority structure remains unchanged.

## 2. C5 Purpose
Measure whether KOSPI technical price structure is confirming strength or deterioration using price structure, support/resistance location and MA/VWAP trend position while avoiding repeated scoring of price-derived momentum indicators.

`TECHNICAL_RULE` remains the calculation authority for Elliott/Fibonacci, MA/VWAP, RSI, MACD, Ichimoku, ADX, Volume, trend, support/resistance and breakout/breakdown interpretation. `SCORING_RULE` owns only the C5 numeric transform.

## 3. Timeframe Boundary
Official `SAI-C5 v1` uses Daily / Closing-confirmed structure.
Intraday data may produce only `C5 Intraday Preview` and cannot overwrite the latest closing-confirmed C5 by itself.

## 4. C5 v1 Numeric Structure
Three numeric sub-components only:
- C5-A Price Structure `PS`: 50%
- C5-B Support/Resistance Position `SR`: 30%
- C5-C MA/VWAP Trend Position `TP`: 20%

Formula:
`SAI-C5 = 0.50*PS + 0.30*SR + 0.20*TP`

Range:
`-1.00 <= SAI-C5 <= +1.00`

Volume, RSI, MACD, ADX, Ichimoku, Elliott and Fibonacci are not independent numeric terms in C5 v1.

## 5. C5-A Price Structure
Primary directional structure from validated recent KOSPI daily swings.

Full-state classification:
- Higher High + Higher Low → `PS = +1.00`
- Lower High + Lower Low → `PS = -1.00`
- mixed HH+LL or LH+HL / non-directional structure → `PS = 0.00`

Partial one-sided swing evidence:
- validated improving one-sided structure → `PS = +0.50 / PARTIAL`
- validated deteriorating one-sided structure → `PS = -0.50 / PARTIAL`

Closing-confirmed breakout above the relevant validated swing-high / resistance structure may set `PS = +1.00`.
Closing-confirmed breakdown below the relevant validated swing-low / support structure may set `PS = -1.00`.
Intraday touch alone cannot create ±1.00.

## 6. C5-B Support / Resistance Position
Use the nearest validated major Support Cluster `S` and Resistance Cluster `R` from TECHNICAL_RULE, with `R > S`.

Inside a valid corridor:
`X = clip(2*(Close-S)/(R-S)-1, -1,+1)`
`SR = 0.50*X`

Thus an intact corridor contributes only `[-0.50,+0.50]`.

Confirmed closing breakout above validated Resistance Cluster → `SR = +1.00`.
Confirmed closing breakdown below validated Support Cluster → `SR = -1.00`.

Support/resistance touch alone does not create ±1.00. Fibonacci levels may help define clusters under TECHNICAL_RULE but are not separately added again.

## 7. C5-C MA/VWAP Trend Position
Fixed v1 anchors:
- MA20
- MA60
- VWAP20
- VWAP60

For each valid anchor `A_j`:
- `Close > A_j * 1.002` → `T_j = +1`
- `Close < A_j * 0.998` → `T_j = -1`
- otherwise → `T_j = 0`

`TP = average(T_j)` across valid anchors.

Requirements:
- 4/4 valid anchors → full TP
- 2 or 3 valid anchors → TP may be used but C5 overall is PARTIAL unless other completeness rules make it DATA UNAVAILABLE
- fewer than 2 valid anchors → TP unavailable

MA/VWAP anchors form one composite TP; they are not independent Evidence Groups.

## 8. Volume / Momentum / Elliott-Fibonacci Boundary
Not independent C5 numeric terms:
- Volume → confirmation / exhaustion / weak-confirmation flag
- RSI → overbought/oversold/divergence flag
- MACD → momentum confirmation/divergence flag
- ADX → trend-strength flag only, not direction
- Ichimoku → supplementary structure confirmation
- Elliott/Fibonacci → S/R cluster, confirmation, wave invalidation and Recovery Structure Failure context

A strong Volume or momentum indicator cannot reverse confirmed price-structure failure by itself.

## 9. Missing / Partial Rules
Mandatory core = PS.

Full formula when PS, SR and TP are all valid:
`C5 = 0.50*PS + 0.30*SR + 0.20*TP`
Status eligible for `VERIFIED` when source/timeframe/calculation validation passes.

SR missing only:
`C5 = 0.70*PS + 0.30*TP`
Status: `PARTIAL`.

TP missing only:
`C5 = 0.625*PS + 0.375*SR`
Status: `PARTIAL`.

PS unavailable/invalid → `SAI-C5 = DATA UNAVAILABLE`.
PS only, with both SR and TP unavailable → `SAI-C5 = DATA UNAVAILABLE`.

Missing inputs are never converted to zero/Neutral.

## 10. Conflict / Divergence / Shock
`C5 Conflict: ACTIVE` when validated directional sub-components materially oppose, including:
- PS and SR opposite signs with both |value| >= 0.50, or
- PS and TP opposite signs with both |value| >= 0.50.

Keep formula unchanged and disclose the conflict.

`C5 Divergence: ACTIVE` may be raised for validated price-vs-RSI/MACD divergence. Divergence is contextual and does not directly change C5 numeric weights.

`C5 Shock: ACTIVE` may be raised for validated structural events such as:
- confirmed major Support Cluster breakdown
- confirmed major Resistance Cluster breakout
- Recovery Structure Failure review trigger, including closing break below fixed Correction Low 5,593 under current TECHNICAL_RULE

Shock feeds Change Detection / Transition / Weight Shift candidate logic only; it is not an automatic Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 11. Anti-Double-Counting
- Price/swing structure scored in PS once
- validated S/R corridor/breakout status scored in SR once
- MA20/60 + VWAP20/60 compressed into one TP composite
- Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci are validation/context only in C5 v1
- issue Breadth/ADL remains C3/E3
- sector leadership remains C4/E4
- Foreign/Institution flow remains C1/E1
- Program flow remains C2/E2
- Liquidity/Macro remains E6
- Options/OI/Volatility remains E7
- Binance/global leading remains E8

No derived technical label may be presented as an independent Evidence Group merely because it is derived from the same price history.

## 12. Anti-Circularity
Required separation:
`Raw/validated Technical Data → C5 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C5 cannot choose a Regime, use that Regime to change its own weights, then reconfirm the same Regime with the altered C5.
VH/H/M/L remains qualitative and is never converted into C5 numeric weight.

## 13. Validation Cases
A. HH/HL + upper intact corridor + MA/VWAP above → positive C5.
B. LH/LL + confirmed S/R breakdown + MA/VWAP below → strongly negative C5.
C. Rising structure + support retest → C5 weakens without automatic bearish reversal.
D. Structural breakdown + RSI oversold → breakdown remains negative; RSI cannot neutralize it.
E. PS strong positive + TP materially negative → `C5 Conflict: ACTIVE`.
F. Volume spike alone → no Bull/Bear numeric contribution.
G. SR missing only → predefined 70/30 PS/TP PARTIAL formula.
H. TP missing only → predefined 62.5/37.5 PS/SR PARTIAL formula.
I. PS unavailable → DATA UNAVAILABLE.
J. Intraday breakout without close confirmation → Preview/context only; no official structural ±1 confirmation.

## 14. Compatibility Verification Before Patch
- SCORING_RULE remains sole numeric authority: PASS
- TECHNICAL_RULE remains technical calculation authority: PASS
- ADAPTIVE E5 qualitative/Regime ownership preserved: PASS
- C3 Breadth duplication avoided: PASS
- C4 Sector duplication avoided: PASS
- Volume/momentum double counting reduced: PASS
- Elliott/Fibonacci duplicate numeric scoring avoided: PASS
- 24-engine architecture unchanged: PASS
- 8 Dashboard categories unchanged: PASS
- six official authority files unchanged: PASS
- global Strategy Action Index remains DATA UNAVAILABLE: PASS

## 15. Pre-Patch Decision
C5 design is ready for official SCORING_RULE integration.
If any authority conflict, formula preservation issue or source-definition problem appears during integration, stop rather than forcing the patch.

Reliability > Speed.
No complete global formula = no global Strategy Action Index.