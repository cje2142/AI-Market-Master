# AI Market Master 3.2 — SAI-C2 Program Flow Pre-Patch Backup

Date: 2026-09-10
Status: PRE-PATCH CHECKPOINT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression reference before SAI-C2 Program Flow integration.

## 1. Current Official State
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`
- `SAI-C1 Smart Money = FORMULA DEFINED / COMPONENT-LEVEL USE ONLY`
- `SAI-C2 Program Flow = NOT YET INTEGRATED`

## 2. Six Official Authority Snapshot Before C2 Patch
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `08c2aca8546ae4f7f8569be90687497988ff8625`
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`

Supporting files before C2 patch:
- `VERSION_STATUS.md`: `c39ede3c2f5a4e6bd07e653b5ea140b6df83f764`
- `CHANGELOG.md`: `ae2d68caf415581dd2e1acdea445e9202bdffe88`

## 3. C2 Design Boundary
C2 must remain numerically owned only by `SCORING_RULE`.
Existing `E2 Program Flow` remains the adaptive/qualitative owner under `ADAPTIVE_VALIDATION_RULE`.
C2 must not replace E2, convert VH/H/M/L to weights, select a Regime by itself, or double-count total Program together with Arbitrage and Non-Arbitrage.

## 4. Planned C2 Inputs
- Arbitrage Program net buy/sell amount — supplementary/mechanical-sensitive input
- Non-Arbitrage Program net buy/sell amount — mandatory structural input
- Total Program net buy/sell — reconciliation/validation only; not a third independent score

All KRW amounts must be unit-aligned with KOSPI total traded value before ratio conversion.

## 5. Planned Numeric Structure
- Normalize Arbitrage flow by KOSPI total traded value, saturation candidate ±0.75%
- Normalize Non-Arbitrage flow by KOSPI total traded value, saturation candidate ±1.50%
- Clip each normalized input to `[-1.00,+1.00]`
- Full C2 candidate: `0.30*N_ARB + 0.70*N_NONARB`
- Non-Arbitrage available / Arbitrage missing: explicit partial formula `C2 = N_NONARB`, status `PARTIAL`
- Non-Arbitrage missing: `SAI-C2 = DATA UNAVAILABLE`

## 6. Planned Conflict / Shock / Event Safeguards
- Opposite Arbitrage vs Non-Arbitrage directions must be disclosed as C2 Conflict rather than hidden by the aggregate.
- Persistent/strong Non-Arbitrage deterioration has greater structural significance than temporary Arbitrage buying, consistent with existing Adaptive Rule.
- Extreme flow is clipped numerically and separately flagged as C2 Shock / Weight Shift candidate.
- On expiry/index-rebalance/event days, mechanical-flow context must be disclosed; Arbitrage may not independently create a structural Regime conclusion.
- Total Program is used only to reconcile source integrity against Arbitrage + Non-Arbitrage when available.

## 7. Compatibility Targets
Must preserve:
- six official authority files
- 24 internal engines
- 8 Dashboard categories
- E1/E2/E3/E7 ownership boundaries
- SCORING numeric authority
- ADAPTIVE Regime/Transition authority
- HTS/KRX priority
- anti-circularity
- global `Strategy Action Index = DATA UNAVAILABLE` until all components/global aggregation/validation are complete

## 8. Recovery Point
If C2 integration introduces unresolved conflict, restore the six-authority state recorded in Section 2 and retain C1 as the only defined SAI numeric component.

Reliability > Speed.
No complete global formula = no global score.
