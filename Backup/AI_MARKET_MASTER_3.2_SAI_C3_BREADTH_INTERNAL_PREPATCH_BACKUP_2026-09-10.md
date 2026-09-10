# AI Market Master 3.2 — SAI-C3 Breadth / Market Internal Pre-Patch Backup

Date: 2026-09-10
Status: PRE-PATCH DESIGN CHECKPOINT
Authority: NON-AUTHORITATIVE BACKUP
Purpose: Preserve the authority snapshot and validated design boundary before SAI-C3 integration.

## 1. Current Official State Before C3
- AI Master Score = DATA UNAVAILABLE
- Strategy Action Index = DATA UNAVAILABLE
- SAI-C1 Smart Money = FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- SAI-C2 Program Flow = FORMULA DEFINED / COMPONENT-LEVEL USE ONLY
- SAI-C3 = NOT YET INTEGRATED

## 2. Six Authority Snapshot
1. MASTER_RULE blob SHA: ea746bf62edbf61521dd26d1855d3b4aadc7b951
2. DASHBOARD_RULE blob SHA: 0ec39d1418edf09098a7a431e904fc5bdfd60230
3. SCORING_RULE blob SHA: 969f1cbd4f6ccb15925f4da51a464c604b5eb518
4. TECHNICAL_RULE blob SHA: b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f
5. BINANCE_RULE blob SHA: f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d
6. ADAPTIVE_VALIDATION_RULE blob SHA: 8833555b261e334b6b0f39d4ce272776fd97af71

Supporting files:
- VERSION_STATUS.md blob SHA: f819aee480508bc0a6b38cd9ab71750047e00ba1
- CHANGELOG.md blob SHA: cee15c77324df0e83fde7fff781c03fcd7749a64

## 3. C3 Design Objective
SAI-C3 Breadth / Market Internal measures whether market participation is broadening or deteriorating beneath the index level.

C3 must preserve E3 Breadth / Internal ownership in ADAPTIVE_VALIDATION_RULE and must not double-count Breadth/ADL inside E5 Technical or other SAI components.

## 4. Proposed Core Inputs
### C3-A KOSPI Breadth — mandatory
- advancing issues
- declining issues
- unchanged issues for validation/context

Raw active breadth:
`B_K = (ADV_K - DEC_K) / (ADV_K + DEC_K)`

Unchanged issues are not directional and therefore do not enter the numerator. `ADV_K + DEC_K` must be greater than zero.

Normalization:
`N_K = clip(B_K / 0.50, -1, +1)`

A raw active breadth of +50% or greater saturates at +1.00; -50% or lower saturates at -1.00.

### C3-B KOSDAQ Breadth — supplementary
- advancing issues
- declining issues
- unchanged issues for validation/context

`B_Q = (ADV_Q - DEC_Q) / (ADV_Q + DEC_Q)`
`N_Q = clip(B_Q / 0.50, -1, +1)`

KOSDAQ breadth is a cross-market participation confirmation and does not replace mandatory KOSPI breadth.

### ADL
Raw ADL level is contextual only in C3 v1 because an isolated absolute ADL value has no stable cross-session scale. ADL may become a numeric C3 input only in a future revision that explicitly defines comparable ADL change/trend history.

## 5. Proposed C3 Formula
When both KOSPI and KOSDAQ breadth are valid:
`SAI-C3 = 0.70*N_K + 0.30*N_Q`

Range:
`[-1.00,+1.00]`

Rationale:
- KOSPI breadth is the structural core because Strategy Action Index is primarily a Korean/KOSPI portfolio-action measure.
- KOSDAQ breadth adds broader domestic risk-participation confirmation without dominating the KOSPI structure.

If KOSDAQ breadth is missing but KOSPI breadth is valid:
`SAI-C3 = N_K`
Status: PARTIAL.

If KOSPI breadth is missing or invalid:
`SAI-C3 = DATA UNAVAILABLE`.

## 6. Conflict / Divergence / Shock Design
### C3 Cross-Market Conflict
Raise `C3 Conflict: ACTIVE` when KOSPI and KOSDAQ normalized breadth have opposite signs and both absolute normalized magnitudes are >=0.30.

### Index/Breadth Divergence
Raise `C3 Divergence: ACTIVE` when:
- KOSPI daily price return is positive while `N_K <= -0.30`, or
- KOSPI daily price return is negative while `N_K >= +0.30`.

The index return is a divergence comparator only and is not an additional C3 numeric contribution.

### C3 Shock
Raise `C3 Shock: ACTIVE` when validated raw active KOSPI breadth satisfies `|B_K| >= 0.75`.
If both KOSPI and KOSDAQ satisfy `|B| >= 0.65` in the same direction, the condition is also a broad participation shock candidate.

Shock/Divergence flags are Change Detection / Transition inputs only. They do not automatically change Market Regime, global SAI, portfolio action or permanent numeric weights.

## 7. Anti-Double-Counting Boundary
- Breadth / advance-decline belongs to C3/E3 and is scored once.
- ADL is contextual only in C3 v1 and is not separately scored in E5 Technical.
- KOSPI/KOSDAQ index returns are comparator/context only, not extra C3 contributions.
- Program remains C2/E2.
- Foreign/institution flow remains C1/E1.
- Technical MA/VWAP/momentum remains E5 and future technical SAI component.
- Volatility/options/OI remain E7.

## 8. Validation Cases Planned
A. Broad bullish participation
B. Broad bearish participation
C. KOSPI positive / KOSDAQ negative conflict
D. KOSDAQ missing partial case
E. KOSPI missing mandatory failure
F. Index up + KOSPI breadth negative divergence
G. Extreme breadth collapse/euphoria Shock
H. Flat/unchanged-heavy market with valid active breadth denominator

## 9. Compatibility Check Before Patch
- Six-authority architecture: compatible
- E3 ownership: compatible
- E5 technical Breadth reference must remain non-independent: compatible
- C1/C2 ownership separation: compatible
- VH/H/M/L numeric conversion: prohibited and not used
- Signal-count scoring: prohibited and not used
- Global Strategy Action Index activation: remains prohibited
- New ninth Dashboard category: not created
- 25th engine: not created

## 10. Stop Conditions
Integration must stop before modifying official rules if any of the following appears:
- inability to preserve the complete current SCORING_RULE text
- conflict with E3/Technical anti-double-counting boundary
- ambiguous input units/definitions that make the formula non-reproducible
- repository write conflict or unexpected concurrent modification
- requirement to change the six-authority architecture

No such stop condition was identified at pre-patch design review.
