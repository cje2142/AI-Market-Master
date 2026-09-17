# AI Market Master 3.2 — Dashboard Runtime Logger Adapter v0.1
## Design Freeze

Date: 2026-09-17
Status: EXPERIMENTAL ADAPTER LAYER / NOT OFFICIAL 3.2 AUTHORITY

## 1. Purpose
Connect a completed AI Market Master 3.2 Dashboard snapshot to the already-validated Full Evidence Runtime Log v0.1 without changing any market rule.

Execution chain:
`Dashboard Result -> Normalized Snapshot -> Runtime Logger Adapter -> Risk Budget Mapper (when portfolio inputs exist) -> Runtime JSONL/CSV`

This adapter does NOT calculate or reinterpret C1-C8, Regime, Transition, Evidence Gate, Strategy Action Index, or Overlay thresholds.

## 2. Adapter boundary
The Dashboard must provide the signal-time market decision in normalized form. The adapter may only:
- validate required fields,
- preserve explicit missing states,
- generate a deterministic sample_id from the signal snapshot,
- translate supplied portfolio sleeves through Risk Budget Execution v0.1,
- append the resulting record through Full Evidence Runtime Log v0.1,
- regenerate the CSV projection.

The adapter may NOT:
- fill missing C1-C8 values,
- convert missing to Neutral/0,
- choose a different Regime,
- infer a stronger/weaker Evidence Gate,
- change the target risk budget,
- create portfolio weights from market evidence,
- overwrite an existing sample.

## 3. Normalized Dashboard snapshot contract
Required signal fields:
- market_date
- timestamp: signal/data-as-of timestamp, NOT adapter execution time
- session_checkpoint
- data_mode
- validation_status
- quality: FULL / PARTIAL / BLOCKED
- C1..C8 each as `{status, value}`
- preliminary_regime
- validated_regime
- transition_state
- material_conflicts
- evidence_gate_result
- gate_reached
- target_risk_budget (may be null when blocked/unavailable)
- action_direction: HOLD / REDUCE / RESTORE / BLOCKED
- allowed_step_size
- reason_codes

Optional execution input:
- portfolio.baseline: core/tactical/leverage normalized risk units
- portfolio.current: core/tactical/leverage normalized risk units
- portfolio.exact_risk_multipliers: YES/NO or bool
- portfolio.leverage_restore_authority: YES/NO or bool
- portfolio.core_reduction_authority: YES/NO or bool
- portfolio.full_evidence_authorized: YES/NO or bool

If portfolio input is absent, the market sample MUST still be recorded with mapper status `NOT MAPPED`; portfolio absence must not discard the market observation.

## 4. Deterministic sample identity
The adapter generates sample_id from a canonical signal fingerprint containing:
- market_date
- signal timestamp/data-as-of
- session_checkpoint
- data/validation status
- C1-C8 status/value
- Regime/Transition
- conflicts
- Evidence Gate and gate reached
- target/action/step/reason codes

Portfolio composition is excluded from the fingerprint because portfolio state is an execution input, not market-state evidence.

Repeated execution of the same underlying signal snapshot therefore produces the same sample_id and is rejected by the existing append-only duplicate gate.

Materially new market data must carry a new signal timestamp/data-as-of and therefore creates a new prospective sample.

## 5. Quality consistency checks
- FULL is invalid if any C1-C8 value is missing.
- Missing category values require explicit unavailable/missing status; missing != neutral.
- BLOCKED samples remain valid observations and are logged.
- PARTIAL samples remain valid observations and are logged.

## 6. Portfolio mapping behavior
When complete portfolio sleeve inputs are supplied and a target exists:
- call Risk Budget Execution v0.1 semantics,
- reduction: Leverage -> Tactical -> Core only with authority,
- restoration: Core -> Tactical -> separately-authorized Leverage,
- absence of Full Evidence reduction authority prevents automatic reduction,
- absence of exact risk multipliers marks numeric translation DATA PARTIAL.

When portfolio or target is unavailable:
- no portfolio action is invented,
- before/after sleeve fields remain null as applicable,
- mapper_status = `NOT MAPPED`,
- unresolved constraint explains why.

## 7. Runtime store
Canonical journal:
`Research/runtime/full_evidence_runtime_log_v0_1.jsonl`

Projection:
`Research/runtime/full_evidence_runtime_log_v0_1.csv`

The adapter must call the already-validated Runtime Log functions rather than write around their append-only safeguards.

## 8. Mandatory deterministic tests
Before first prospective production sample, verify:
1. FULL Dashboard snapshot -> valid Runtime sample.
2. same snapshot rerun -> same sample_id / duplicate rejected.
3. new signal timestamp -> new sample_id.
4. PARTIAL snapshot with explicit missing category -> accepted, missing preserved.
5. FULL snapshot with missing category -> rejected.
6. Dashboard REDUCE + portfolio -> correct Leverage-first mapping.
7. R6/REDUCE without Full Evidence authority -> no automatic sale.
8. Dashboard HOLD without portfolio -> market sample still logged as NOT MAPPED.
9. portfolio composition change does not change sample_id for identical market snapshot.
10. CSV projection matches appended JSONL record.

Tests must use temporary stores and must not create a production prospective sample.

## 9. Integration boundary
Passing adapter tests means only that Dashboard outputs can be transferred into the prospective validation journal deterministically.

It does NOT validate market timing, performance, C1-C8 formulas, or official 3.2 integration.

Official 3.2 Authority files remain unchanged.

## 10. Version lock
This file freezes Dashboard Runtime Logger Adapter v0.1 before implementation testing.
Any change to snapshot contract, fingerprint semantics, duplicate handling, or adapter authority requires v0.2 or later.
