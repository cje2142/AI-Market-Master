# AI Market Master 3.2 — SAI-C3 Breadth / Market Internal Final Backup

Date: 2026-09-10
Status: FINAL BACKUP / VERIFIED SNAPSHOT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Recovery / regression verification for the SAI-C3 Breadth / Market Internal integration.

## 1. Integration Result
`SAI-C3 Breadth / Market Internal` has been formally specified in `SCORING_RULE` as the third numeric sub-component for a future Strategy Action Index.

The global numeric state remains:
- `AI Master Score = DATA UNAVAILABLE`
- `Strategy Action Index = DATA UNAVAILABLE`

Defined component-level formulas:
- `SAI-C1 Smart Money`
- `SAI-C2 Program Flow`
- `SAI-C3 Breadth / Market Internal`

No component alone or combination of C1-C3 activates the global SAI.

## 2. Six Official Authority Snapshot
1. `Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md`
   - blob SHA: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
   - unchanged by C3 integration
2. `Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md`
   - blob SHA: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
   - unchanged by C3 integration
3. `Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md`
   - blob SHA: `8427b9f5ac5efede8c53df72dc63a4bbff1ec6ae`
   - C1 + C2 + C3 numeric component authority
4. `Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md`
   - blob SHA: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
   - unchanged
5. `Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md`
   - blob SHA: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
   - unchanged
6. `Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md`
   - blob SHA: `8833555b261e334b6b0f39d4ce272776fd97af71`
   - unchanged; retains E3 Breadth/Regime/Transition authority

Supporting files at final-backup creation:
- `VERSION_STATUS.md`: `2de4f4b985de3f5a9801a9bf5a67fa7945c02cd5`
- `CHANGELOG.md`: `5c373d7ff2ff5f775dd8362f014614883fd35679`

## 3. SAI-C3 Formula
Inputs:
- KOSPI advancing / declining issues — mandatory
- KOSDAQ advancing / declining issues — supplementary
- unchanged issue counts — validation/context only
- raw ADL level — contextual only in v1

Raw active breadth:
- `B_K = (ADV_K - DEC_K) / (ADV_K + DEC_K)`
- `B_Q = (ADV_Q - DEC_Q) / (ADV_Q + DEC_Q)`

Normalization:
- `N_K = clip(B_K / 0.50, -1, +1)`
- `N_Q = clip(B_Q / 0.50, -1, +1)`

Full formula:
`SAI-C3 = 0.70*N_K + 0.30*N_Q`

Range:
`[-1.00,+1.00]`

Structural principle:
KOSPI breadth is the core participation measure; KOSDAQ breadth is supplementary domestic risk-participation confirmation.

## 4. Missing / Partial Rule
- KOSPI + KOSDAQ breadth valid → full C3 / `VERIFIED` when count/source validation passes
- KOSDAQ missing, KOSPI valid → `C3 = N_K / PARTIAL`
- KOSPI missing/invalid or `ADV_K + DEC_K <= 0` → `SAI-C3 = DATA UNAVAILABLE`
- Missing never equals Neutral

## 5. ADL / Unchanged Boundary
- unchanged counts do not create directional points
- raw ADL absolute level is not independently scored in C3 v1
- isolated ADL level lacks a stable cross-session scale without comparable history
- ADL may remain contextual under E3 and Technical reference but cannot be double-counted as independent numeric confirmation

## 6. Conflict / Divergence / Shock
### Cross-Market Conflict
`C3 Conflict: ACTIVE` when KOSPI and KOSDAQ normalized breadth have opposite signs and both absolute magnitudes are >=0.30.

### Index/Breadth Divergence
`C3 Divergence: ACTIVE` when:
- KOSPI daily return >0 and `N_K <= -0.30`, or
- KOSPI daily return <0 and `N_K >= +0.30`.

Index return is comparator/context only, not an added C3 score.

### Shock
`C3 Shock: ACTIVE` when:
- `|B_K| >= 0.75`, or
- KOSPI and KOSDAQ breadth have the same direction and both `|B| >= 0.65`.

Conflict/Divergence/Shock are Change Detection / Transition inputs only. They cannot automatically change Market Regime, global SAI, portfolio action or permanent Base Weight.

## 7. Anti-Double-Counting Boundary
- KOSPI Breadth → C3/E3 only
- KOSDAQ Breadth → C3 supplementary confirmation only
- raw ADL → contextual only in C3 v1
- KOSPI/KOSDAQ index return → divergence comparator only
- Program → C2/E2
- Foreign/Institution flow → C1/E1
- MA/VWAP/momentum/price structure → E5/future technical component
- options/OI/volatility → E7

E5 Technical may reference Breadth/ADL contextually but must not count it again as independent numeric confirmation.

## 8. Validation Cases Verified by Formula
A. Bullish participation:
- KOSPI ADV 600 / DEC 300 → `N_K≈+0.6667`
- KOSDAQ ADV 1000 / DEC 600 → `N_Q=+0.50`
- `C3≈+0.6167`

B. Bearish participation:
- KOSPI ADV 250 / DEC 650 → `N_K≈-0.8889`
- KOSDAQ ADV 500 / DEC 1100 → `N_Q=-0.75`
- `C3≈-0.8472`

C. Cross-market conflict:
- `N_K=+0.60, N_Q=-0.50 → C3=+0.27 + Conflict ACTIVE`

D. KOSDAQ missing:
- `N_K=-0.55 → C3=-0.55 / PARTIAL`

E. KOSPI missing:
- `C3 = DATA UNAVAILABLE`

F. Index up / breadth weak:
- KOSPI return positive + `N_K=-0.45` → `Divergence ACTIVE`

G. Extreme breadth:
- `B_K<=-0.75` → `N_K=-1.00 + C3 Shock ACTIVE`

H. Many unchanged issues:
- no artificial Bull/Bear point from unchanged counts; active denominator remains ADV+DEC when valid.

## 9. Real HTS Sanity Check
Using the recent supplied breadth example:
- KOSPI ADV 326 / DEC 540 → `B_K≈-0.2471`, `N_K≈-0.4942`
- KOSDAQ ADV 643 / DEC 1005 → `B_Q≈-0.2197`, `N_Q≈-0.4393`
- `SAI-C3≈-0.4778`

Interpretation: materially weak internal participation but not an extreme breadth shock. This is consistent with the earlier qualitative observation of narrow/concentrated index strength and deteriorating breadth.

This sanity check does not activate the global Strategy Action Index.

## 10. Existing Rule Compatibility Verification
### MASTER_RULE
- 24 engines unchanged
- HTS/KRX priority unchanged
- scoring authority remains solely in SCORING_RULE
- no new engine or execution category introduced
- no conflict found

### DASHBOARD_RULE
- 8 categories unchanged
- Breadth remains mapped inside existing Observation/Evidence/Technical context as already defined
- global Strategy Action Index remains DATA UNAVAILABLE
- no ninth category added
- no conflict found

### ADAPTIVE_VALIDATION_RULE
- E3 Breadth / Internal remains qualitative/adaptive owner
- existing rule preserved: index strength + weak breadth = concentration/divergence warning
- index weakness + improving breadth = possible internal stabilization
- breadth alone cannot finalize portfolio action
- Regime/Transition/re-validation remains independent from C3 numeric formula
- no conflict found

### TECHNICAL_RULE
- ADL/Breadth may be referenced technically
- adaptive/numeric independent confirmation ownership remains E3/C3
- no double-counting permitted
- no scoring ownership overlap
- no conflict found

### BINANCE_RULE
- Binance remains outside C3 formula
- no naming or authority conflict

## 11. Scoring Firewall Verification
Still prohibited:
- VH/H/M/L → numeric C3/global SAI weight
- signal color → number
- signal count → number
- Market Regime → score band
- qualitative Strategy posture → Strategy Action Index
- C1/C2/C3 alone → global Strategy Action Index
- Breadth + ADL double counting without a future explicit history formula
- index return added to C3 after being used as a divergence comparator
- silent missing-data renormalization outside the predefined C3 partial formula

Result: PASS.

## 12. Recovery / Integration References
Pre-patch checkpoint:
`Backup/AI_MARKET_MASTER_3.2_SAI_C3_BREADTH_INTERNAL_PREPATCH_BACKUP_2026-09-10.md`

Pre-patch creation commit:
`9bfb20e688269a859e425541c7745d4f07ea0a7f`

SCORING_RULE integration commit:
`952ef858270149804c9ea9cd7129888c2f1b7d35`

VERSION_STATUS integration commit:
`a98bf4291742684018306edaedcfcf528119008a`

CHANGELOG integration commit:
`8f1ec41c8df7f1f1eb2704d68192a432654cb008`

## 13. Final Verification State
- C3 purpose/boundary: VERIFIED
- KOSPI/KOSDAQ input definitions: VERIFIED BY RULE
- active breadth normalization: VERIFIED BY RULE
- internal weights 70/30: DEFINED v1
- missing/partial behavior: VERIFIED BY RULE
- ADL non-numeric boundary: VERIFIED
- unchanged-count boundary: VERIFIED
- conflict threshold: VERIFIED BY RULE
- divergence threshold: VERIFIED BY RULE
- shock threshold: VERIFIED BY RULE
- formula validation cases: VERIFIED
- real HTS sanity check: PASS
- six-authority architecture: PRESERVED
- 24-engine architecture: PRESERVED
- 8-category Dashboard: PRESERVED
- global Strategy Action Index activation: NOT YET ALLOWED
- unresolved authority conflict: NONE FOUND

## 14. Next Development Boundary
The next SAI component must preserve C1 Smart Money, C2 Program Flow and C3 Breadth ownership separation.
The complete Strategy Action Index remains `DATA UNAVAILABLE` until remaining components, global aggregation, global missing/partial handling, output range/Action Bands and required validation are formally defined.

Reliability > Speed.
No complete global formula = no global score.
