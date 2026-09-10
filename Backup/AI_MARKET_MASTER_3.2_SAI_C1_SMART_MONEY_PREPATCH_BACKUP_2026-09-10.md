# AI Market Master 3.2 — SAI-C1 Smart Money Pre-Patch Backup

Date: 2026-09-10
Status: NON-AUTHORITATIVE PRE-PATCH CHECKPOINT
Purpose: Recovery / regression comparison before SAI-C1 Smart Money integration.

## 1. Official Authority Snapshot
The authoritative 3.2 structure remains exactly six files under `Rules/`.

1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `a4ac88c940e00fc4aacfee6b76979887c7433d1f`
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`

Supporting files:
- `VERSION_STATUS.md` blob SHA: `3a5db834441e57d45468afc2e8ddd0dab6db06e2`
- `CHANGELOG.md` blob SHA: `aa590b79046d176569479b996578dabe0e449caf`

## 2. Pre-Patch Scoring State
At this checkpoint:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

Reason: SCORING_RULE has not yet adopted a complete reproducible global Strategy Action Index formula. SAI-C1 is only one component and must not activate the final Strategy Action Index by itself.

## 3. SAI-C1 Smart Money Design Boundary
SAI-C1 is a numeric scoring component owned only by `SCORING_RULE`.
It does not replace `E1 Smart Money` in `ADAPTIVE_VALIDATION_RULE`.

Purpose:
Measure whether directional major capital in the Korean equity market is increasing or reducing risk exposure.

Core inputs:
- Foreign KOSPI cash net flow
- Foreign KOSPI200 futures net flow
- Institutional KOSPI cash net flow

Excluded from independent C1 scoring to avoid double-counting:
- Program / arbitrage / non-arbitrage: E2 ownership
- Breadth / ADL: E3 ownership
- Options / futures OI risk structure: E7 ownership
- Financial Investment as separate score when already included in Institution total
- Foreign cumulative futures position as a separate score when current futures flow is already scored

## 4. Proposed Numeric Structure
Each core input is normalized to `[-1.00, +1.00]` from source data, not from signal color, Regime label or VH/H/M/L priority.

### C1-A Foreign Cash
Normalize foreign KOSPI cash net buy amount by KOSPI total traded value.
Provisional saturation boundary: ±1.5% of KOSPI traded value.

### C1-B Foreign Futures
Normalize foreign KOSPI200 futures net contracts by KOSPI200 futures total open interest.
Provisional saturation boundary: ±10% of total OI.

### C1-C Institution Cash
Normalize institutional KOSPI cash net buy amount by KOSPI total traded value.
Provisional saturation boundary: ±1.0% of KOSPI traded value.

Provisional internal weights:
- Foreign Cash 40%
- Foreign Futures 40%
- Institution Cash 20%

These values are design calibration values and are not yet the global SAI weight structure.

## 5. Missing Data Rule
Mandatory for numeric C1:
- Foreign Cash
- Foreign Futures

Optional:
- Institution Cash

All three present:
`C1 = 0.40*ForeignCash + 0.40*ForeignFutures + 0.20*Institution`

Institution missing only:
`C1 = 0.50*ForeignCash + 0.50*ForeignFutures`
Status must be `PARTIAL`.

If either Foreign Cash or Foreign Futures is unavailable:
`SAI-C1 = DATA UNAVAILABLE`.

Missing data must never be converted to zero/Neutral.

## 6. Conflict / Shock Handling
Foreign Cash and Foreign Futures divergence is information and must not be hidden by the aggregate score.
When they materially oppose each other, output a C1 Conflict flag and reduce scoring confidence as appropriate.

Extreme values remain clipped to ±1.00 for C1. Extreme magnitude produces a separate C1 Shock / Weight Shift candidate signal rather than expanding the numeric score beyond bounds.

No single C1 shock may change the Market Regime or global SAI by itself.

## 7. Adaptive Integration Boundary
Existing `ADAPTIVE_VALIDATION_RULE` remains authoritative for:
- E1 Smart Money interpretation
- Market Regime
- Transition Watch / Confirming / Regime Change
- Evidence Priority VH/H/M/L
- conflict resolution
- anti-double-counting
- Regime re-validation

Numeric SAI-C1 must not convert VH/H/M/L into numeric weights and must not use C1 itself to select and then reconfirm the same Regime.

## 8. Design Items Explicitly Rejected
The following earlier draft ideas are rejected:
- creating a new global G1-G6 Evidence Group system
- merging Program and Breadth into one scoring group
- converting VH/H/M/L to numeric values
- converting signal colors to numeric values
- signal-count scoring
- automatic permanent Base Weight mutation from a single new HTS input
- treating DATA UNAVAILABLE as Neutral
- allowing SAI-C1 alone to activate final Strategy Action Index

## 9. Validation Requirements Before Final Adoption
Before SAI-C1 is considered integrated:
1. SCORING_RULE must explicitly own the C1 formula.
2. Existing E1/E2/E3/E7 boundaries must remain intact.
3. Numeric C1 must remain separate from qualitative VH/H/M/L.
4. normal / reversal / missing / extreme test cases must be documented.
5. MASTER and DASHBOARD authority boundaries must remain unchanged except references/presentation when required.
6. VERSION_STATUS and CHANGELOG must reflect component activation without claiming full SAI activation.
7. Final files must be re-read after patching and cross-validated.

## 10. Pre-Patch Verification
- 24-engine architecture preserved: YES
- 8 Dashboard categories preserved: YES
- six-authority architecture preserved: YES
- current SAI global numeric state preserved: DATA UNAVAILABLE
- SAI-C1 design isolated to SCORING authority: YES
- known anti-double-counting conflicts resolved in design: YES

This file is non-authoritative and must never override `Rules/`.