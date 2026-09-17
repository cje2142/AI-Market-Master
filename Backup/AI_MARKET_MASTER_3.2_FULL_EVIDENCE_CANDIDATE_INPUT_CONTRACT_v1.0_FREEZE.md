# AI Market Master 3.2 — Full Evidence Candidate Input Contract v1.0
## Step 2 Freeze

Date: 2026-09-17
Status: **EXPERIMENTAL CANDIDATE INPUT CONTRACT / NOT OFFICIAL 3.2 AUTHORITY**

## 1. Purpose
Freeze the normalized input that Candidate v1.0 receives before Step 3 target/action logic is implemented.

This contract does not change C1-C8 formulas, Regime rules, Strategy Action Index, official Dashboard rules, or Risk Budget Execution v0.1.

Implementation:
`Research/full_evidence_candidate_input_contract_v1_0.py`

Evaluator consumed by this contract:
`Research/full_evidence_candidate_evaluator_v1_0.py`

## 2. Current market identity
Every Candidate evaluation input must carry:
- `market_date`
- `timestamp`
- `session_checkpoint`
- `data_mode`
- `validation_status`
- `quality = FULL / PARTIAL / BLOCKED`

Signal time remains explicit. No later outcome may be used to rewrite these fields except a documented input/data correction under the existing Runtime protocol.

## 3. C1-C8 evidence contract
Exactly C1 through C8 are required.

Each category carries:
- `status`
- `value`
- `trend = DETERIORATING / IMPROVING / STABLE / UNKNOWN`
- `polarity = POSITIVE / NEGATIVE / NEUTRAL / CONFLICT / MISSING / UNKNOWN`
- `strength = NORMAL / STRONG / SHOCK / UNKNOWN`

Important boundary:
- official C1-C8 numeric `value` and `status` remain the original market evidence,
- Candidate v1.0 does **not** invent numeric thresholds to convert raw C1-C8 values into trend, polarity, or strength,
- trend/polarity/strength must therefore be supplied explicitly by the normalized upstream Dashboard/evidence layer,
- `UNKNOWN` remains unknown and is not converted to Neutral/Zero,
- FULL quality cannot contain a missing C1-C8 numeric value.

## 4. Regime / transition contract
Required:
- `preliminary_regime`
- `validated_regime`
- `transition_state`

Both Regime fields must resolve to R1-R8.

Candidate structural flags include:
- `r4_r5_persistence`
- `r8_entry`
- `r7_to_r8_transition`
- `r8_persistence`
- `strong_r8`

Consistency locks:
- R8 entry / R7->R8 / R8 persistence / strong R8 flags require validated R8,
- R4/R5 persistence requires validated R4 or R5.

No new Regime is calculated by the Candidate input layer.

## 5. Conflict contract
Candidate-wide unresolved conflict is explicit:
- `flags.material_conflict`
- `candidate_conflict_reasons[]`

These two fields must agree.

Only unresolved Candidate-level material conflicts belong in this list. Category-internal context such as a C2 arbitrage/non-arbitrage disagreement is not automatically promoted to Candidate-wide HOLD unless the upstream evidence review explicitly marks it material and unresolved.

Additional frozen flags include:
- `c5_reduction_conflict`
- `c5_structural_breakdown`
- `c5_structure_recovery`
- `c6_liquidity_deterioration`
- `c7_volatility_expansion`
- `c7_stabilization`

The input layer records these explicit states; it does not derive them from hidden thresholds.

## 6. Previous Overlay state
Step 3 requires an explicit prior state. The input contract therefore requires:
- `current_target_risk_budget`
- `previous_action_direction`
- `previous_validated_regime` where available
- `previous_market_date` where available
- `trading_sessions_since_last_reduction`
- `trading_sessions_since_last_restoration`

Allowed current target states are exactly:
`100 / 95 / 90 / 80 / 70 / 60`

For the first prospective Candidate evaluation, the caller must explicitly supply `current_target_risk_budget = 100`; the parser does not silently fabricate a previous state.

Cooldown counters are non-negative observed trading-session counts. Calendar-day substitution is not allowed.

## 7. Cost Gate context
The frozen Candidate rule requires non-emergency Expected Edge to exceed estimated total transaction cost by more than 2x when the gate can be estimated.

The input contract supports:
- `PASS`
- `FAIL`
- `UNAVAILABLE`
- `EMERGENCY_BYPASS`

PASS/FAIL require explicit `expected_edge_bps` and `estimated_total_cost_bps`, and the parser checks consistency with:
`Expected Edge > 2 x Total Cost`.

`UNAVAILABLE` preserves missing information.

`EMERGENCY_BYPASS` requires an explicit reason. The input contract records such authority but does not invent it.

## 8. Strict parsing locks
- String `false` cannot silently become boolean True.
- Risk-budget values cannot be rounded/snapped into an allowed state.
- Missing category status is rejected.
- FULL with missing C1-C8 numeric evidence is rejected.
- R8/R4-R5 structural flags inconsistent with validated Regime are rejected.
- Candidate conflict boolean/reasons mismatch is rejected.
- Missing or invalid previous-state cooldown values are rejected.

## 9. Step boundary
Step 2 ends after producing a validated `CandidateInput` and converting its market-evidence portion into the Step 1 `CandidateState`.

Step 2 does **not** yet calculate:
- Evidence Gate -> final action priority,
- Target Risk Budget,
- HOLD / REDUCE / RESTORE decision,
- Cost Gate enforcement on an action,
- cooldown bypass decision,
- portfolio sleeve mapping,
- Runtime Log append.

Those begin in Step 3 and later steps.

## 10. Version lock
This file freezes the Candidate v1.0 input schema for prospective validation.

Any future change that adds/removes mandatory market evidence, changes the meaning of trend/polarity/strength, changes previous-state semantics, or changes Cost Gate input semantics requires a new contract version rather than silent modification.
