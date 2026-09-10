# AI Market Master 3.2 — SAI-C5 Technical Structure Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression verification for the SAI-C5 Technical Structure integration.

## 1. Integration Result
`SAI-C5 Technical Structure` has been formally specified in `SCORING_RULE` as the fifth numeric sub-component for a future Strategy Action Index.

Official global numeric state remains:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

Defined component-level formulas:
- `SAI-C1 Smart Money`
- `SAI-C2 Program Flow`
- `SAI-C3 Breadth / Market Internal`
- `SAI-C4 Sector / Leadership`
- `SAI-C5 Technical Structure`

No component alone or combination of C1-C5 activates the global Strategy Action Index.

## 2. Six Official Authority Snapshot
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `b4dd28d0d76e9966c3cb5f968841c3ed9236a72f`
   - C1 + C2 + C3 + C4 + C5 numeric component authority
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
   - unchanged; technical calculation authority
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`
   - unchanged; retains E5 Technical Structure adaptive/Regime interpretation authority

Supporting files at final-backup creation:
- `VERSION_STATUS.md`: `3c5d6ba27d46d91cad169edf33330924a2815a4a`
- `CHANGELOG.md`: `8d30273f7e5c77fc9b58c5a4795592e92fc33fba`

## 3. C5 v1 Timeframe Boundary
Official C5 uses KOSPI Daily / Closing-confirmed structure.

Intraday data may produce only `C5 Intraday Preview`.
Intraday touch/breakout/breakdown cannot overwrite the latest closing-confirmed C5 by itself.

This preserves the existing distinction between ordinary intraday analysis and confirmed technical structure.

## 4. C5 Numeric Architecture
Three numeric terms:
- Price Structure `PS` — 50%, mandatory directional core
- Support / Resistance Position `SR` — 30%
- MA / VWAP Trend Position `TP` — 20%

Full formula:
`SAI-C5 = 0.50*PS + 0.30*SR + 0.20*TP`

Range:
`-1.00 <= SAI-C5 <= +1.00`

Volume, RSI, MACD, ADX, Ichimoku, Elliott and Fibonacci are not direct C5 numeric terms in v1.

## 5. Price Structure `PS`
Use latest validated daily swing structure under TECHNICAL_RULE.

Classification:
- HH + HL → `PS = +1.00`
- LH + LL → `PS = -1.00`
- mixed HH+LL or LH+HL / non-directional → `PS = 0.00`
- validated improving one-sided structure → `PS = +0.50`
- validated deteriorating one-sided structure → `PS = -0.50`

Closing-confirmed breakout above validated swing-high/resistance structure may set `PS = +1.00`.
Closing-confirmed breakdown below validated swing-low/support structure may set `PS = -1.00`.

Intraday touch alone cannot set PS to ±1.00.
Unvalidated swing identity → PS unavailable rather than guessed.

## 6. Support / Resistance Position `SR`
Use nearest validated major Support Cluster `S` and Resistance Cluster `R`, requiring `R > S`.

Inside intact corridor:
`X = clip(2*(Close-S)/(R-S)-1, -1,+1)`
`SR = 0.50*X`

Therefore intact-corridor contribution is limited to `[-0.50,+0.50]`.

Confirmed closing breakout above Resistance Cluster → `SR = +1.00`.
Confirmed closing breakdown below Support Cluster → `SR = -1.00`.

Touch alone does not create ±1.00.
Fibonacci/Elliott/MA/VWAP/previous high-low/volume concentration may validate clusters under TECHNICAL_RULE but are not separately re-added numerically.

## 7. MA / VWAP Trend Position `TP`
Fixed v1 anchors:
- MA20
- MA60
- VWAP20
- VWAP60

For each same-session valid anchor `A_j`:
- `Close > A_j * 1.002` → `T_j=+1`
- `Close < A_j * 0.998` → `T_j=-1`
- otherwise → `T_j=0`

`TP = average(T_j)`.

Completeness:
- 4/4 anchors → full TP
- 2 or 3 anchors → TP usable but overall C5 is PARTIAL
- fewer than 2 anchors → TP unavailable

The ±0.20% band is v1 noise control, not a signal-color conversion.
MA/VWAP anchors form one TP composite, not four independent Evidence Groups.

## 8. Missing / Partial Rules
Full PS + SR + full TP:
`C5 = 0.50*PS + 0.30*SR + 0.20*TP`
Eligible for `VERIFIED` when source/timeframe/calculation validation passes.

SR missing only:
`C5 = 0.70*PS + 0.30*TP`
Status `PARTIAL`.

TP missing only:
`C5 = 0.625*PS + 0.375*SR`
Status `PARTIAL`.

TP based on only 2 or 3 anchors:
use full formula but Status `PARTIAL`.

PS unavailable/invalid → `DATA UNAVAILABLE`.
PS only with both SR and TP unavailable → `DATA UNAVAILABLE`.

Missing inputs never become zero/Neutral.

## 9. Confirmation / Divergence Boundary
Contextual only, not direct numeric terms:
- Volume → confirmation/exhaustion/weak-confirmation
- RSI → overbought/oversold/divergence
- MACD → momentum confirmation/deceleration/divergence
- ADX → trend strength only, not direction
- Ichimoku → supplementary structure confirmation
- Elliott/Fibonacci → S/R cluster, wave context, invalidation, Recovery Structure Failure review

`C5 Divergence: ACTIVE` may be raised only when price-vs-RSI/MACD divergence is validated under TECHNICAL_RULE and material to current structure.
Divergence does not change numeric weights automatically.

## 10. Conflict / Shock Rules
`C5 Conflict: ACTIVE` when either:
1. PS and SR have opposite signs and both `|value| >= 0.50`, or
2. PS and TP have opposite signs and both `|value| >= 0.50`.

Formula remains unchanged; near-zero aggregate cannot hide the conflict.

`C5 Shock: ACTIVE` for validated structural events including:
- confirmed major Support Cluster breakdown
- confirmed major Resistance Cluster breakout
- current Recovery Structure Failure review trigger, including closing break below fixed Correction Low 5,593

Shock feeds Change Detection / Transition / Weight Shift candidate logic only.
It is not an automatic Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 11. Anti-Double-Counting
- PS scores swing/price structure once
- SR scores validated S/R corridor/boundary event once
- MA20/60 + VWAP20/60 are compressed into one TP composite
- Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci remain validation/context only
- Breadth/ADL remains C3/E3
- Sector leadership remains C4/E4
- Foreign/Institution flow remains C1/E1
- Program flow remains C2/E2
- Liquidity/Macro remains E6
- Options/OI/Volatility remains E7
- Binance/global leading remains E8

PS, SR and TP are one E5/C5 technical evidence family, not three independent Evidence Groups.

## 12. Anti-Circularity
Required separation:
`Validated Technical Data → C5 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C5 cannot choose a Market Regime, use that Regime to alter its own weights, then use altered C5 as sole reconfirmation.
VH/H/M/L remains qualitative and is never converted into C5 numeric weight.

## 13. Validation Cases
A. `PS=+1, SR=+0.40, TP=+1` → `C5=+0.82`; PASS.

B. `PS=-1, SR=-1, TP=-1` → `C5=-1.00`; PASS.

C. `PS=+1, SR=-0.40, TP=+0.50` → `C5=+0.48`; positive but weakened, no mechanical bearish reversal; PASS.

D. `PS=+1, SR=+0.20, TP=-0.75` → `C5=+0.41` + `C5 Conflict: ACTIVE`; PASS.

E. SR missing: `PS=+1, TP=+0.50` → `C5=+0.85 / PARTIAL`; PASS.

F. TP missing: `PS=-1, SR=-0.50` → `C5=-0.8125 / PARTIAL`; PASS.

G. PS missing → DATA UNAVAILABLE; PASS.

H. Volume spike alone → no independent directional numeric term; PASS.

I. intraday breakout without close confirmation → Preview/context only; PASS.

J. closing break below 5,593 → C5 Shock + Recovery Structure Failure review, no automatic global SAI/Regime change; PASS.

## 14. Cross-Authority Compatibility Verification
### MASTER_RULE
- exactly six authority roles preserved
- 24 engines unchanged
- HTS/KRX priority preserved
- no new engine added
- PASS

### DASHBOARD_RULE
- exactly eight user-facing categories preserved
- no ninth C5 category created
- global numeric scores remain DATA UNAVAILABLE
- PASS

### TECHNICAL_RULE
- remains sole calculation authority for technical indicators and structure confirmation
- touch-alone prohibition preserved
- ADX remains non-directional
- closing confirmation preserved
- fixed 5,593 Recovery Structure Failure trigger preserved
- PASS

### ADAPTIVE_VALIDATION_RULE
- E5 remains qualitative/adaptive Technical Structure owner
- internal technical priority hierarchy preserved
- C5 cannot independently select/reconfirm Regime
- VH/H/M/L remains qualitative
- PASS

### C1-C4 Ownership
- Smart Money, Program, issue Breadth and Sector Leadership remain outside C5 numeric formula
- PASS

### BINANCE_RULE
- global-leading layer remains outside C5 numeric formula
- PASS

## 15. Scoring Firewall Verification
Still prohibited:
- C5 or C1-C5 combination → final Strategy Action Index
- Market Regime → numeric score band
- VH/H/M/L → numeric weight
- RSI/MACD/ADX/Volume → hidden extra C5 points
- intraday preview → silent replacement of closing-confirmed C5
- missing PS → invented score
- C5 Shock/Conflict/Divergence → automatic permanent weight change

Result: PASS.

## 16. Integration Commits
Pre-patch backup creation:
`8c828612d4f04a167a561cf76c3147bf3526dc46`

SCORING_RULE integration:
`a4a2af046fc0998a9f65c9b042637114eafade2d`

VERSION_STATUS initial C5 registration:
`13512b28fd2c27e5762f442addae99737f494ccf`

CHANGELOG initial C5 registration:
`c4505a8fe8ee6f1d26381a6e7eb7c03350cadef1`

## 17. Final Verification State
- C5 purpose/boundary: VERIFIED
- Daily/Closing timeframe boundary: VERIFIED
- Price Structure PS: VERIFIED BY RULE
- Support/Resistance SR transform: VERIFIED BY RULE
- MA/VWAP TP transform: VERIFIED BY RULE
- internal weights 50/30/20: DEFINED v1
- predefined partial formulas: VERIFIED BY RULE
- mandatory PS gate: VERIFIED
- Volume/RSI/MACD/ADX/Ichimoku/Elliott/Fibonacci non-numeric boundary: VERIFIED
- Conflict rule: VERIFIED BY RULE
- Divergence boundary: VERIFIED
- Shock rule: VERIFIED BY RULE
- anti-double-counting: VERIFIED
- anti-circularity: VERIFIED
- validation cases: PASS
- six-authority architecture: PRESERVED
- 24-engine architecture: PRESERVED
- 8-category Dashboard: PRESERVED
- global Strategy Action Index activation: NOT YET ALLOWED
- unresolved authority conflict: NONE FOUND

## 18. Next Development Boundary
Any next SAI component must preserve C1 Smart Money, C2 Program Flow, C3 Breadth, C4 Sector/Leadership and C5 Technical Structure ownership separation.

The complete Strategy Action Index remains `DATA UNAVAILABLE` until remaining components, global aggregation, global missing/partial handling, final range/Action Bands and required regression validation are formally defined.

Reliability > Speed.
No complete global formula = no global score.