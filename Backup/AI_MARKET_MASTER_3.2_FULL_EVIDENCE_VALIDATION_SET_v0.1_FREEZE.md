# AI Market Master 3.2 — Compounding Overlay Full Evidence Validation Set v0.1

Status: EXPERIMENTAL VALIDATION FREEZE / NOT OFFICIAL 3.2 AUTHORITY
Date: 2026-09-17

## 1. Purpose
Validate the evidence-gated Compounding Overlay architecture against actual historical Dashboard decisions before any official 3.2 integration.

This stage does NOT retune v0.2/v0.4 Historical Proxy thresholds. It tests whether the Full Evidence architecture behaves consistently with actual 3.2 evidence and subsequent market paths.

## 2. Critical boundary
Historical Proxy versions v0.2 and v0.4 changed Historical Proxy exposure behavior. They did not replace the original Full Evidence Gate.

Therefore Full Evidence validation uses the common evidence architecture frozen in v0.1:
3.2 Regime -> Evidence Gate -> Exposure Map -> Cost Gate -> Minimum Action -> Cooldown/Hysteresis -> Position Transition -> Execution.

Regime alone never grants execution permission.

## 3. Full Evidence reduction rules under validation
A-class: C1 Smart Money / C2 Program / C5 Technical
B-class: C3 Breadth / C4 Leadership
C-class: C6 Liquidity-Macro / C7 Volatility-Derivatives / C8 Global Leading

- First -5%p: R4 or worse + >=1 deteriorating A-class + >=3 independent deteriorating categories + no material C5 conflict.
- Additional -5%p: persistent R4/R5 + >=2 deteriorating A-class + >=4 total deterioration + >=2 evidence classes.
- Strong -10%p: R5/R6 + strong C1 or C2 deterioration + C5 structural breakdown + >=5 deteriorating categories + C6 deterioration or C7 volatility expansion.
- Material unresolved conflict -> HOLD.
- Recovery remains asymmetric and faster than reduction; R8 requires independent recovery evidence.
- Portfolio reduction priority: leverage/high-beta first, core spot last.

## 4. Frozen validation events
Do not add/remove events after seeing outcomes without creating a new validation version.

| Date | Historical Dashboard state | Historical action/posture | Evidence quality |
|---|---|---|---|
| 2026-07-15 | Strong Bull / Recovery | Hold; avoid chasing; partial profit management | Regime + HTS snapshot |
| 2026-07-16 | Panic / Capitulation | No chase-selling; reduce leverage on rebound rather than dumping core | Regime + HTS snapshot |
| 2026-07-21 | Selective strength / weak internals | Hold / Selective Buy | Regime + HTS snapshot |
| 2026-07-24 | Risk-Off Correction | No aggressive buying | Regime + HTS snapshot |
| 2026-07-30 | Risk / Oversold conflict | Manage leverage; wait for structure recovery | Regime + HTS snapshot |
| 2026-08-04 | Bullish Rebound + high volatility | Confirmation Buy | Regime + HTS snapshot |
| 2026-09-08 | Leadership Bull -> Distribution confirmation | Core Hold; no new leverage | Regime-level record |
| 2026-09-10 | R2 maintained / R4 watch | HOLD | C1-C8 PARTIAL; C6 unavailable |
| 2026-09-11 | R4 Distribution / R5 watch | staged Risk Reduction WATCH, not forced liquidation | C1-C8 FULL snapshot |

## 5. Runtime snapshots recovered from prior analysis
These values are preserved only for exact-date validation and must not be silently filled when missing.

### 2026-09-10 — PARTIAL
- C1 -0.62
- C2 -0.66
- C3 -0.03
- C4 +0.51
- C5 +0.52
- C6 DATA UNAVAILABLE
- C7 +0.33
- C8 -0.02
- Preliminary/validated posture: R2 maintained, R4 watch

Implication under Full Evidence Gate: reduction permission is not established solely from negative C1/C2 because Regime is not R4-or-worse and C5 remains positive. Missing C6 is never treated as neutral.

### 2026-09-11 — FULL
- C1 -0.35
- C2 -0.86
- C3 -0.40
- C4 -0.30
- C5 +0.40
- C6 +0.12
- C7 +0.05
- C8 -0.22
- Validated posture: R4 Distribution, R5 watch

Implication under Full Evidence Gate: multiple deterioration categories exist, but positive C5 creates a material technical conflict for automatic reduction. The validation must distinguish WATCH from EXECUTE. No reduction is to be retroactively forced merely because later prices declined.

## 6. Outcome measurement frozen before event study
For each event date, using KOSPI as primary market path and KOSPI200/KOSDAQ as secondary confirmation:
- close-to-close forward return after 1, 5, and 20 trading sessions
- maximum adverse excursion (MAE) over next 5 and 20 sessions
- maximum favorable excursion (MFE) over next 5 and 20 sessions
- horizon unavailable -> PENDING, never imputed

No after-the-fact threshold determines success/failure. The event study is diagnostic.

## 7. Validation questions
1. Did HOLD / caution decisions avoid unnecessary underexposure before continued strength?
2. Did R4/R5 WATCH precede meaningful downside without forcing premature core liquidation?
3. Did Panic handling avoid selling near local lows and preserve V-rebound participation?
4. Did recovery confirmation occur early enough to restore exposure?
5. Does the Full Evidence Gate reduce false positives relative to the Historical Proxy?

## 8. Anti-overfitting lock
- No C1-C8 value is inferred for dates where it was not recorded.
- No missing value is set to zero.
- No event is removed because the later path is inconvenient.
- No new gate threshold is selected from these nine outcomes.
- Any rule change after this study requires a new Full Evidence design version.

## 9. Current architectural interpretation
v0.2 and v0.4 remain Historical Proxy research branches.
The Full Evidence candidate is the evidence-gated architecture inherited from v0.1, informed by Proxy lessons but not silently overwritten by Proxy thresholds.
