# AI Market Master 3.2 — Full Evidence Candidate Transition Engine v1.0
## Step 3 Freeze

Date: 2026-09-17
Status: **EXPERIMENTAL CANDIDATE TRANSITION ENGINE / NOT OFFICIAL 3.2 AUTHORITY**

Implementation:
`Research/full_evidence_candidate_transition_engine_v1_0.py`

Inputs:
- Step 1 `GateResult` from `full_evidence_candidate_evaluator_v1_0.py`
- Step 2 `CandidateInput` from `full_evidence_candidate_input_contract_v1_0.py`

This layer does not alter official C1-C8 formulas, Regime rules, Strategy Action Index, AI Master Score state, Risk Budget Mapper, or Runtime Log semantics.

## 1. Output contract
Every evaluation returns:
- `action_direction = HOLD / REDUCE / RESTORE / BLOCKED`
- previous target risk budget
- new target risk budget
- allowed step size
- Evidence Gate result
- Gate reached
- Cost Gate status
- cooldown status
- fast-recovery flag
- explicit reason codes

Allowed target states remain exactly:
`100 / 95 / 90 / 80 / 70 / 60`.

## 2. Reduction transition table
The frozen downward path is interpreted deterministically as:
- 100 -> 95 when Reduction Gate 5 or a stronger reduction gate is present
- 95 -> 90 when Additional-5 or Strong-10 gate is present
- 90 -> 80 only with Strong-10
- 80 -> 70 only with Strong-10
- 70 -> 60 only with Deepest-70-to-60 gate

A stronger reduction gate may satisfy a shallower state transition when the full nominal gate size would land outside the frozen state path. The engine never creates an ad-hoc target and never exceeds the frozen ordinary maximum reduction of 10 percentage points.

This interpretation prevents an abrupt R6 deterioration from becoming stuck at 95 merely because the weaker R4/R5 persistence gate is no longer applicable.

## 3. Restoration transition table
The upward path preserves the already-frozen staged recovery logic:
- 60 -> 70 with the base Restoration-10 gate
- 60 -> 80 only through Fast V-Rebound qualification
- 70 -> 80 with Additional-Restoration-10
- 70 -> 90 only through Fast V-Rebound qualification
- 80 -> 90 with Additional-Restoration-10
- 90 -> 100 only with Return-100 gate
- 95 -> 100 with the standard Restoration-10 or Return-100 gate

No generic positive market state can create a +20pp jump.

## 4. Fast V-Rebound lock
The +20pp fast-restoration allowance is restricted to the already-frozen V-Rebound pattern:
- R7 -> R8 transition explicitly flagged,
- base Restoration-10 gate valid,
- C1 improving,
- C2 improving,
- C3 improving,
- C5 improving,
- C5 structure recovery confirmed.

Only the 60 -> 80 and 70 -> 90 transitions use this +20pp path.

## 5. Conflict and blocked behavior
- `quality = BLOCKED` -> action `BLOCKED`, target unchanged.
- Candidate-level material unresolved conflict -> `HOLD`, target unchanged.
- If a reduction and restoration transition are simultaneously eligible -> `HOLD / GATE DIRECTION CONFLICT`.

The engine never chooses one side silently.

## 6. Cost Gate enforcement
The Step-2 Cost Gate states are interpreted as:
- `PASS` -> action may proceed.
- `FAIL` -> otherwise-valid action is held.
- `UNAVAILABLE` -> remains explicit but does not become an invented FAIL or PASS. Candidate v1.0 states the 2x rule applies when the Cost Gate can be estimated.
- `EMERGENCY_BYPASS` -> valid only for R6 structural-risk reduction with Strong-10 or Deepest gate confirmation and an explicit reason already required by Step 2.

Emergency bypass is not valid for restoration.

## 7. Cooldown / hysteresis
Reduction:
- a same-direction reduction is blocked when `trading_sessions_since_last_reduction = 0`,
- exception: previous validated R5 -> current validated R6 with Strong-10 or Deepest independent Full Evidence confirmation,
- one or more observed trading sessions clears the normal reduction cooldown,
- `None` means no observed active reduction cooldown is supplied and is not silently converted to zero.

Restoration:
- Candidate v1.0 does not define a numeric restoration cooldown duration,
- therefore Step 3 does not invent one,
- separate Recovery Gates provide hysteresis,
- Fast V-Rebound uses the explicit frozen recovery override.

## 8. Minimum action threshold
All executable transitions are at least 5 percentage points.
No 95 -> 92, 90 -> 88 or other micro-adjustment is possible.

Reduction step maximum remains 10pp.
Restoration step maximum remains 20pp and is available only to the Fast V-Rebound path defined above.

## 9. Step boundary
Step 3 ends with Candidate market action and target-risk-budget selection.

Step 3 does **not** yet:
- run deterministic transition test suites,
- map target risk budget into Core/Tactical/Leverage sleeves,
- modify the existing Risk Budget Mapper,
- append or rewrite Runtime Log records,
- change Dashboard ingestion.

Those belong to Steps 4-6.

## 10. Version lock
Any change to:
- state-transition mapping,
- stronger-gate fallback behavior,
- fast V-Rebound qualification,
- Cost Gate interpretation,
- cooldown exception,
- conflict precedence,
requires a new Transition Engine version rather than silent modification.
