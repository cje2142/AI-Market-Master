# AI Market Master 3.2 — SAI-C8 Global Leading Pre-Patch Backup

Date: 2026-09-10
Status: PRE-PATCH DESIGN CHECKPOINT / READY
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery checkpoint before official SAI-C8 integration.

## 1. Design Result
SAI-C8 Global Leading v1 is ready for official integration after design, authority-boundary review, anti-double-counting review, missing/partial design, stale-data firewall review and synthetic validation.

Global `AI Master Score` and global `Strategy Action Index` remain `DATA UNAVAILABLE` until the separate global activation gate is completed.

## 2. C8 Numeric Axes
- Global Equity Risk `GR`: 30%
- Korea Leading `KR`: 25%
- Semiconductor Risk `SEMI`: 20%
- Global Rate/Liquidity `GLIQ`: 15%
- Crypto Risk `CRYPTO`: 10%

Full formula:
`SAI-C8 = 0.30*GR + 0.25*KR + 0.20*SEMI + 0.15*GLIQ + 0.10*CRYPTO`
Range: `[-1,+1]`.

## 3. Canonical Symbol Mapping
- GR = SPYUSDT + QQQUSDT composite
- KR = EWYUSDT
- SEMI = SOXLUSDT
- GLIQ = TMFUSDT
- CRYPTO = BTCUSDT
- SAMSUNGUSDT and SKHYNIXUSDT remain Korea/Semiconductor confirmation only, not extra numeric axes.

All 8 Binance symbols remain required for a full Binance Engine execution under BINANCE_RULE. C8 numeric design does not reduce the fixed 8-symbol watchlist.

## 4. Normalization
Use the same validated observation window across C8 numeric inputs whenever possible. For Binance, use same-query rolling 24h return or an equivalently computed aligned 24h return.

`N_SPY = clip(r_SPY / 0.015,-1,+1)`
`N_QQQ = clip(r_QQQ / 0.020,-1,+1)`
`GR = 0.50*N_SPY + 0.50*N_QQQ`

`KR = clip(r_EWY / 0.025,-1,+1)`
`SEMI = clip(r_SOXL / 0.050,-1,+1)`
`GLIQ = clip(r_TMF / 0.030,-1,+1)`
`CRYPTO = clip(r_BTC / 0.040,-1,+1)`

These are v1 calibration boundaries, not empirically backtested constants.

## 5. Missing / Partial Gate
Full five-axis valid set -> eligible VERIFIED when source/window/freshness validation passes.

Partial formula:
`C8_partial = sum(w_i*X_i for valid axes) / sum(w_i for valid axes)`

PARTIAL is allowed only when all are true:
1. GR is available;
2. at least 3 of 5 axes are valid;
3. original fixed-weight coverage is at least 60%;
4. no STALE input is used numerically.

Within GR, if only SPY or QQQ is valid, GR may equal the single available equity index but the overall C8 status is PARTIAL.

If GR is unavailable, fewer than 3 axes are valid, weight coverage <60%, or only STALE inputs would satisfy the gate -> `SAI-C8 = DATA UNAVAILABLE`.
Missing data is never zero/Neutral.

## 6. Binance Freshness Boundary
- LIVE: eligible for normal C8 numeric use.
- FALLBACK: may be used only when BINANCE_RULE fallback eligibility and TTL are satisfied; C8 status is capped at PARTIAL and Binance Confidence downgrade must be preserved.
- STALE: numeric C8 use prohibited; historical context only.

## 7. Positioning / Confirmation Boundary
Not direct numeric C8 terms in v1:
- SAMSUNGUSDT / SKHYNIXUSDT returns
- OI / OI change
- Funding
- Long/Short ratios
- Premium / Mark-Index spread
- ADL risk
- Order book / recent trades

These remain G2/G3/G6 confirmation, crowding or positioning context under BINANCE_RULE.

## 8. Conflict / Shock
Raise `C8 Conflict: ACTIVE` for material cross-axis disagreement such as GR and KR opposite with both |value|>=0.50, or GR and SEMI opposite with both |value|>=0.50.

Raise `C8 Korea Confirmation Conflict: ACTIVE` when EWY numeric direction materially conflicts with both available Samsung/SK hynix Binance confirmation signals.

Raise `C8 Shock: ACTIVE` for broad aligned extreme moves such as GR/KR/SEMI all <=-0.80 or all >=+0.80, or other extreme aligned global-leading moves with independent G6 confirmation.

Conflict/Shock feed Change Detection, Transition and Regime re-validation only. No automatic Regime, portfolio action, global SAI override or permanent weight change.

## 9. Anti-Double-Counting / Anti-Circularity
- SPY/QQQ form one GR composite, not two independent Evidence Groups.
- Samsung/SKH are not re-added after EWY/SOXL.
- TMF remains E8 global rates/liquidity proxy; C6 Korea Treasury 3Y remains domestic liquidity/macro.
- BTC is auxiliary and capped at 10% fixed internal C8 weight.
- G6 positioning data are contextual, not extra C8 numeric terms.
- C8 remains one E8 evidence family.
- C8 cannot choose a Regime, use that Regime to alter itself, then reconfirm the same Regime.
- VH/H/M/L remains qualitative and is never converted to numeric C8 weight.

## 10. Validation Cases
A. All axes +1 -> C8=+1.00.
B. All axes -1 -> C8=-1.00.
C. GR=+0.8, KR=-0.8, SEMI=-0.6, GLIQ=+0.2, CRYPTO=0 -> aggregate retained + Conflict.
D. GR+KR+SEMI only -> 75% coverage -> predefined renormalized PARTIAL allowed.
E. KR+SEMI+GLIQ+CRYPTO without GR -> DATA UNAVAILABLE despite 70% weight coverage.
F. GR+KR only -> only 2 axes -> DATA UNAVAILABLE.
G. one of SPY/QQQ missing -> GR single-index fallback allowed but overall C8 PARTIAL.
H. valid FALLBACK data inside TTL -> numeric use allowed but overall C8 capped PARTIAL and Confidence downgraded.
I. STALE Binance data -> numeric use prohibited.
J. Samsung/SKH disagreement -> confirmation conflict only; no direct numeric weight change.

Result: PASS by rule design.

## 11. Official Integration Plan
1. Patch SCORING_RULE only for numeric C8 authority.
2. Preserve MASTER/DASHBOARD/TECHNICAL/BINANCE/ADAPTIVE authority boundaries.
3. Update VERSION_STATUS.
4. Update CHANGELOG.
5. Re-fetch and cross-validate six authorities.
6. Create C8 Final Backup.
7. Register Final Backup SHA in VERSION_STATUS and CHANGELOG.
8. Keep global AI Master Score and global Strategy Action Index DATA UNAVAILABLE.

Reliability > Speed.