# AI Market Master 3.2 — SAI-C4 Sector / Leadership Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression verification for the SAI-C4 Sector / Leadership integration.

## 1. Integration Result
`SAI-C4 Sector / Leadership` has been formally specified in `SCORING_RULE` as the fourth numeric sub-component for a future Strategy Action Index.

Official global numeric state remains:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

Defined component-level formulas:
- `SAI-C1 Smart Money`
- `SAI-C2 Program Flow`
- `SAI-C3 Breadth / Market Internal`
- `SAI-C4 Sector / Leadership`

No component alone or combination of C1-C4 activates the global Strategy Action Index.

## 2. Six Official Authority Snapshot
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
   - unchanged by C4 integration
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
   - unchanged by C4 integration
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `aff3feb2220c6d4747bda043c049cc2d0c813b6e`
   - C1 + C2 + C3 + C4 numeric component authority
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
   - unchanged
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
   - unchanged
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`
   - unchanged; retains E4 Sector / Leadership, Market Regime, Transition and adaptive Evidence Priority authority

Supporting files at final-backup creation:
- `VERSION_STATUS.md`: `70bde2539317370a3a9b01a96c6e8f0fbdf0f23d`
- `CHANGELOG.md`: `c9485aca5a1691d954373020f20e26204f2a9ab2`

## 3. Fixed Sector Universe v1
Exactly eight benchmark identities:
1. Semiconductor — KRX Semiconductor Index
2. Automobile — KRX Automobile Index
3. Secondary Battery — KRX Secondary Battery TOP 10 Index
4. Financials — KOSPI 200 Financial Index
5. Shipbuilding — iSelect Shipbuilding TOP10 Index (PR)
6. Defense — iSelect Defense TOP10 Index (Price Return)
7. AI Power Infrastructure — KRX-Akros AI Power Infrastructure Index
8. Bio — KRX Bio TOP 10 Index

Canonical identity principle:
- `index provider + exact benchmark index name`
- ETF ticker/code is not the benchmark index code
- HTS short code is an alias only after direct verification
- ambiguous benchmark identity is treated as unavailable

The universe is fixed for C4 v1; ad hoc substitution is prohibited.

## 4. Data Collection Standard
Source priority:
1. user-provided HTS/KRX
2. verified official KRX/index-provider data
3. other verified supplementary data

Required numeric inputs:
- KOSPI daily return
- same-session daily return for each available fixed-universe benchmark

Preferred validation fields:
`Index Name | Current Level | Change | Daily Return | Source | Timestamp`

Optimization added during integration:
- all sector returns and the KOSPI comparator must be from the same trading session and materially aligned observation time
- mixed-session/asynchronous data is not silently combined
- ETF return is contextual verification only and cannot silently replace a missing benchmark-index return

## 5. C4-A Sector Direction Breadth
For each valid sector return `r_i`:
- `r_i > +0.20%` → +1
- `r_i < -0.20%` → -1
- otherwise → 0

Let `UP`, `DOWN`, `N_valid` be the positive, negative and valid-sector counts.

`SD = (UP - DOWN) / N_valid`

Range: `[-1.00,+1.00]`.

The ±0.20% neutral band is a v1 noise-control calibration rule.

## 6. C4-B Relative Leadership Breadth
For each valid sector:
`RS_i = SectorReturn_i - KOSPIReturn`

Classification:
- `RS_i > +0.20%p` → +1
- `RS_i < -0.20%p` → -1
- otherwise → 0

Let `OUT` and `UNDER` be outperforming and underperforming sector counts.

`RL = (OUT - UNDER) / N_valid`

Range: `[-1.00,+1.00]`.

KOSPI return is comparator only and is not a third numeric term.

## 7. C4 v1 Formula
`SAI-C4 = 0.60*SD + 0.40*RL`

Range:
`[-1.00,+1.00]`

Internal weighting:
- Sector Direction Breadth: 60%
- Relative Leadership Breadth: 40%

Rationale:
Absolute broad sector direction receives greater weight so widespread sector losses cannot become strongly bullish solely because they fall less than KOSPI.

These weights are internal C4 weights only and do not define C4's future global SAI weight.

## 8. Missing / Partial / Freshness Gate
- 8/8 valid sectors + valid same-session KOSPI comparator → eligible for `VERIFIED`
- 6/8 or 7/8 valid sectors + valid KOSPI comparator → predefined `PARTIAL`; denominators use only valid fixed-universe sectors
- fewer than 6/8 → `SAI-C4 = DATA UNAVAILABLE`
- missing/invalid/asynchronous KOSPI comparator → `SAI-C4 = DATA UNAVAILABLE`
- missing sectors never become zero/Neutral
- ambiguous index identity is unavailable
- ETF return is not a silent numeric substitute

Coverage threshold = 75%.

## 9. Leadership Concentration Boundary
Leadership Concentration is not an independent numeric C4 term in v1.

Reason:
Concentration is not inherently bearish; `R2 Concentrated Leadership Bull` is a valid Adaptive Market Regime.

Permitted qualitative/context states:
- BROAD
- NORMAL
- CONCENTRATED
- EXTREME

No unvalidated concentration ratio is used to penalize or boost C4.

## 10. Conflict / Shock Rules
### C4 Conflict
`C4 Conflict: ACTIVE` when:
- SD and RL have opposite signs
- `|SD| >= 0.50`
- `|RL| >= 0.50`

The formula remains unchanged and the conflict is disclosed/passed to Adaptive Validation.

### C4 Shock
`C4 Shock: ACTIVE` when either:
1. `|SD| >= 0.75`, or
2. SD and RL have the same sign and both absolute magnitudes are >=0.60.

Shock is a Change Detection / Transition / Weight Shift candidate only, not an automatic Regime/global SAI/portfolio/permanent-weight change.

## 11. Anti-Double-Counting Boundary
- sector benchmark returns → C4/E4 source data
- SD and RL are predefined transforms of the same sector-return set, not separate Evidence Groups
- KOSPI return → comparator only
- constituent individual returns → not separately added
- Foreign/Institution flow → C1/E1
- Program flow → C2/E2
- issue Breadth/ADL → C3/E3
- MA/VWAP/RSI/MACD/Elliott/Fibonacci → E5/future technical numeric component
- Liquidity/Macro → E6
- Options/OI/Volatility → E7
- Binance/global leading → E8
- HBM/DRAM/NAND/CAPEX/inventory/AI-demand fundamentals → AI Cycle/future leading-cycle component

No same underlying sector-return set may be presented as multiple independent confirmations simply because multiple derived labels exist.

## 12. Anti-Circularity Boundary
Required separation:
`Raw Sector/KOSPI Data → C4 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C4 cannot:
1. choose a Market Regime,
2. use that Regime to alter its own numeric weights,
3. use the altered C4 as the sole reason to reconfirm the same Regime.

VH/H/M/L remains qualitative and is never converted into C4 numeric weights.

## 13. Validation Cases
A. Broad bullish leadership → SD positive + RL positive → positive C4.

B. Broad weakness → SD negative + RL negative → negative C4.

C. Widespread losses but relative resilience:
- `SD=-1.00`, `RL=+1.00`
- `C4=-0.20`
- `C4 Conflict: ACTIVE`
- expected result prevents false strong-bull classification.

D. Strong index / weak sector participation → SD may be positive while RL negative; concentration remains E4 context rather than automatic numeric penalty.

E. 6 valid sectors + KOSPI → calculate / `PARTIAL`.

F. 5 or fewer valid sectors → `DATA UNAVAILABLE`.

G. missing KOSPI comparator → `DATA UNAVAILABLE`.

H. `|SD| >=0.75` → calculate normally + `C4 Shock: ACTIVE`.

I. mixed session or ambiguous benchmark → exclude invalid sector; apply completeness gate; no silent ETF substitution.

Result: PASS.

## 14. Existing Rule Compatibility Verification
### MASTER_RULE
- exactly six authority roles preserved
- 24 engines unchanged
- Engine 08 Sector Rotation remains internal analysis architecture
- HTS/KRX priority preserved
- SCORING_RULE remains sole numeric authority
- no conflict found

### DASHBOARD_RULE
- exactly eight Dashboard categories preserved
- no ninth C4 category created
- global Strategy Action Index remains DATA UNAVAILABLE
- no conflict found

### ADAPTIVE_VALIDATION_RULE
- E4 Sector / Leadership remains `sector rotation, relative strength, leadership concentration/expansion`
- R1/R2/R3/R4/R8 sector-leadership logic remains qualitative/adaptive
- E4 priority remains VH/H/M/L qualitative only
- C4 cannot independently determine a Regime
- no conflict found

### TECHNICAL_RULE
- technical calculation ownership unchanged
- C4 does not import MA/VWAP/RSI/MACD/Elliott/Fibonacci into its numeric formula
- no conflict found

### BINANCE_RULE
- Binance remains outside C4 numeric formula under E8 global-leading support
- no conflict found

## 15. Scoring Firewall Verification
Still prohibited:
- C4 or C1-C4 combination → final Strategy Action Index
- VH/H/M/L → numeric weight
- Market Regime → fixed score band
- qualitative concentration flag → numeric penalty/bonus
- ETF fallback → silent benchmark substitution
- incomplete coverage → invented neutral values
- C4 Conflict/Shock → automatic permanent weight change
- same sector-return data → multiple independent Evidence Groups

Result: PASS.

## 16. Integration Commits
Pre-patch backup creation:
`12f60582ec975a07187caf805bb512a67d28801c`

SCORING_RULE integration:
`ffb838ad325eac1554529c79e5ff98b2710836b6`

VERSION_STATUS initial C4 registration:
`152cd07d05fbba5e3392e6fc48f3e358d5a2ed46`

CHANGELOG initial C4 registration:
`8ef4a7f289cbc672de29dd0b03cc7a45eb103f67`

## 17. Final Verification State
- C4 purpose/boundary: VERIFIED
- fixed eight-sector universe: VERIFIED BY RULE
- benchmark identity / ETF-code boundary: VERIFIED
- data source hierarchy: VERIFIED
- same-session/freshness safeguard: VERIFIED
- SD formula: VERIFIED BY RULE
- RL formula: VERIFIED BY RULE
- internal weights 60/40: DEFINED v1
- completeness gate 8/8, 6-7/8, <6/8: VERIFIED BY RULE
- Leadership Concentration non-numeric boundary: VERIFIED
- Conflict threshold: VERIFIED BY RULE
- Shock threshold: VERIFIED BY RULE
- anti-double-counting: VERIFIED
- anti-circularity: VERIFIED
- validation cases: PASS
- six-authority architecture: PRESERVED
- 24-engine architecture: PRESERVED
- 8-category Dashboard: PRESERVED
- global Strategy Action Index activation: NOT YET ALLOWED
- unresolved authority conflict: NONE FOUND

## 18. Next Development Boundary
Any next SAI component must preserve C1 Smart Money, C2 Program Flow, C3 Breadth and C4 Sector/Leadership ownership separation.
The complete Strategy Action Index remains `DATA UNAVAILABLE` until remaining components, global aggregation, missing/partial handling, final range/Action Bands and required regression validation are formally defined.

Reliability > Speed.
No complete global formula = no global score.
