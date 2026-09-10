# AI Market Master 3.2 — SAI-C4 Sector / Leadership Pre-Patch Backup

Date: 2026-09-10
Status: PRE-PATCH DESIGN CHECKPOINT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Preserve the verified SAI-C4 design before any official SCORING_RULE modification.

## 1. Current Official State Before C4 Patch
- `SAI-C1 Smart Money`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C2 Program Flow`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C3 Breadth / Market Internal`: FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- `SAI-C4 Sector / Leadership`: NOT YET IN OFFICIAL SCORING_RULE
- `Strategy Action Index`: DATA UNAVAILABLE
- `AI Master Score`: DATA UNAVAILABLE

Current six-authority structure remains unchanged.

## 2. C4 Purpose
Measure Korean-market sector participation and leadership structure using sector-level price behavior, while preventing duplication with C1 Smart Money, C2 Program Flow, C3 issue Breadth, E5 Technical, E6 Liquidity, E7 Risk and E8 Global Leading.

C4 is a numeric SAI sub-component only. `E4 Sector / Leadership` remains the adaptive/qualitative owner for sector rotation, relative strength, leadership concentration/expansion, Market Regime, Transition and re-validation.

## 3. Fixed Sector Universe v1
Use a fixed verified benchmark universe of eight representative sectors:
1. Semiconductor — KRX Semiconductor Index
2. Automobile — KRX Automobile Index
3. Secondary Battery — KRX Secondary Battery TOP 10 Index
4. Financials — KOSPI 200 Financial Index
5. Shipbuilding — iSelect Shipbuilding TOP10 Index (PR)
6. Defense — iSelect Defense TOP10 Index (Price Return)
7. AI Power Infrastructure — KRX-Akros AI Power Infrastructure Index
8. Bio — KRX Bio TOP 10 Index

Identification principle:
- Official identifier is `index provider + exact benchmark index name`.
- ETF ticker/code must not be treated as an index code.
- HTS short code may be stored only as an alias after direct verification.

## 4. Data Collection Standard
Primary source priority:
1. user-provided HTS/KRX data
2. verified official index-provider/KRX data
3. verified ETF/index-provider fallback for contextual verification only

Minimum recurring input:
- KOSPI daily return
- daily return for each available C4 fixed-universe index

Preferred input format:
`Index Name | Current Level | Change | Daily Return | Source | Timestamp`

Numeric C4 calculation uses daily return only. Other fields are validation/context unless later separately defined.

## 5. C4-A Sector Direction Breadth
For each valid sector i, classify daily return:
- `r_i > +0.20%` → +1
- `r_i < -0.20%` → -1
- `-0.20% <= r_i <= +0.20%` → 0

Let:
- `UP` = number of +1 sectors
- `DOWN` = number of -1 sectors
- `N_valid` = number of valid fixed-universe sectors

Then:
`SD = (UP - DOWN) / N_valid`

Range: `[-1.00,+1.00]`.

Sector Direction Breadth measures sector participation, not issue-level breadth. C3 remains the issue-breadth owner.

## 6. C4-B Relative Leadership Breadth
For each valid sector i:
`RS_i = SectorReturn_i - KOSPIReturn`

Classify relative strength:
- `RS_i > +0.20%p` → +1
- `RS_i < -0.20%p` → -1
- `-0.20%p <= RS_i <= +0.20%p` → 0

Let:
- `OUT` = number of outperforming sectors
- `UNDER` = number of underperforming sectors

Then:
`RL = (OUT - UNDER) / N_valid`

Range: `[-1.00,+1.00]`.

KOSPI return is a comparator/denominator context and is not separately added as a numeric C4 contribution.

## 7. C4 v1 Formula
When input coverage passes the completeness gate:

`SAI-C4 = 0.60*SD + 0.40*RL`

Component range:
`-1.00 <= SAI-C4 <= +1.00`

Internal weights:
- Sector Direction Breadth: 60%
- Relative Leadership Breadth: 40%

Rationale:
- actual broad sector direction receives higher weight than relative outperformance to avoid classifying widespread losses as bullish merely because sectors fall less than KOSPI.
- relative leadership still captures concentration/rotation information.

These internal weights do not define the future global weight of C4 inside the complete Strategy Action Index.

## 8. Leadership Concentration Boundary
Leadership Concentration is NOT directly added to the C4 numeric score in v1.

Reason:
High concentration is not inherently bearish. `Concentrated Leadership Bull` is an existing valid Market Regime.

Use qualitative/context flags instead:
- BROAD
- NORMAL
- CONCENTRATED
- EXTREME

Concentration must be interpreted under E4 and Adaptive Validation together with C3 Breadth, E1/E2 flow and E5 Technical when relevant.

No unvalidated concentration ratio is adopted in v1.

## 9. C4 Conflict / Divergence
Raise `C4 Conflict: ACTIVE` when SD and RL have opposite signs and both absolute magnitudes are at least `0.50`.

Meaning examples:
- SD strongly positive + RL strongly negative: broad nominal rise but relative underperformance versus headline index, possible large-cap/index concentration.
- SD strongly negative + RL strongly positive: broad nominal weakness but relative resilience versus index, possible internal stabilization/rotation.

Keep the numeric formula unchanged. Do not treat a near-zero aggregate caused by opposition as absence of information.

## 10. C4 Shock / Weight Shift Candidate
Raise `C4 Shock: ACTIVE` when either:
1. `|SD| >= 0.75`, or
2. SD and RL have the same sign and both absolute magnitudes are at least `0.60`.

C4 Shock is a Change Detection / Transition / Weight Shift candidate only.
It is not an automatic Market Regime change, global SAI override, portfolio action or permanent Base Weight change.

## 11. Missing / Partial Rule — v1 Design
Fixed universe size = 8.

- `N_valid = 8`: full C4 calculation, eligible for `VERIFIED` when source/name/timestamp validation passes.
- `N_valid = 6 or 7`: predefined `PARTIAL` C4 calculation using only valid fixed-universe sectors in SD/RL denominators.
- `N_valid < 6`: `SAI-C4 = DATA UNAVAILABLE`.
- KOSPI daily return unavailable: `SAI-C4 = DATA UNAVAILABLE` because RL cannot be calculated.

Coverage threshold = 75% of the fixed universe (minimum 6/8).
Missing sectors are excluded from `N_valid`; they are never converted to zero/Neutral.

This is explicit predefined partial handling, not silent reweighting.

## 12. Anti-Double-Counting
Do not add the following as independent C4 numeric contributions:
- Samsung Electronics / SK hynix individual stock returns
- Foreign/Institution flow → C1/E1
- Program/Arbitrage/Non-Arbitrage → C2/E2
- issue advance/decline breadth / ADL → C3/E3
- MA/VWAP/RSI/MACD/Elliott/Fibonacci → E5 / future technical numeric component
- HBM/DRAM/NAND/CAPEX/inventory/AI demand fundamentals → AI Cycle / future leading-cycle component
- options/OI/volatility → E7
- Binance/SOXL/EWY/QQQ/SPY/BTC/TMF → E8

Sector index daily returns may be referenced by E4 and C4, but must not be re-counted as multiple independent confirmations merely because several derived labels are created from the same returns.

## 13. Anti-Circularity
Required separation:
`Raw Sector/KOSPI Data → C4 Calculation`

and independently:
`Raw HTS + other Evidence → Preliminary Regime → Adaptive Priority → Transition / Conflict → Regime Re-validation`

C4 must not:
1. choose a Market Regime,
2. use that Regime to alter its own numeric weights,
3. then use the altered C4 as the sole reason to reconfirm the same Regime.

VH/H/M/L Evidence Priority must never be converted into numeric C4 weights.

## 14. Validation Cases
### Case A — Broad Bullish Leadership
Most sectors above +0.20% and most outperform KOSPI.
Expected: SD positive, RL positive, C4 positive, no conflict.

### Case B — Broad Market Weakness
Most sectors below -0.20% and most underperform KOSPI.
Expected: SD negative, RL negative, C4 negative.

### Case C — Widespread Losses but Relative Resilience
All sectors negative while many decline less than KOSPI.
Expected: SD strongly negative, RL positive; C4 must not become strongly bullish; Conflict may activate.

### Case D — Strong Index / Weak Sector Participation
KOSPI strong, only a few sector benchmarks lead while most lag.
Expected: SD may be modest/positive, RL negative; concentration warning remains contextual under E4.

### Case E — Missing 2 of 8 sectors
6 valid sector returns + valid KOSPI return.
Expected: calculate using N_valid=6, Status PARTIAL.

### Case F — Missing 3 or more sectors
5 or fewer valid sectors.
Expected: `SAI-C4 = DATA UNAVAILABLE`.

### Case G — Missing KOSPI return
Sector returns available, KOSPI return unavailable.
Expected: `SAI-C4 = DATA UNAVAILABLE`.

### Case H — Broad Sector Shock
`|SD| >= 0.75`.
Expected: C4 calculated normally + `C4 Shock: ACTIVE`; no automatic Regime/global SAI change.

## 15. Compatibility Verification Before Patch
- SCORING_RULE remains sole numeric authority: PASS
- E4 Sector / Leadership adaptive ownership preserved: PASS
- C3 issue Breadth vs C4 sector Breadth separated: PASS
- E5 Technical duplicate scoring avoided: PASS
- E8/Binance excluded from C4 numeric formula: PASS
- AI Cycle fundamentals excluded from C4: PASS
- 24-engine architecture unchanged: PASS
- 8 Dashboard categories unchanged: PASS
- six official authority files unchanged: PASS
- global Strategy Action Index remains DATA UNAVAILABLE: PASS

## 16. Pre-Patch Decision
C4 design is ready for official SCORING_RULE integration, subject to a safe full-file update path.

If the official file cannot be updated without risking loss/truncation of existing C1-C3 content, STOP and preserve this checkpoint rather than forcing the patch.

Reliability > Speed.
No complete global formula = no global Strategy Action Index.
