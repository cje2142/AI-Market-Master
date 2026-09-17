# AI Market Master 3.2 — Full Evidence Candidate -> Risk Budget Connector v1.0
## Step 5 Validation Backup — 2026-09-17

Status: **EXPERIMENTAL STEP-5 INTEGRATION / 13 OF 13 PASS / NOT OFFICIAL 3.2 AUTHORITY**

## 1. Purpose
Connect the validated Full Evidence Candidate v1.0 market action/target to the already-frozen Risk Budget Execution v0.1 mapper without changing official C1-C8, Regime, Strategy Action Index, Candidate gates, or portfolio execution hierarchy.

Implementation:
`Research/full_evidence_candidate_risk_budget_connector_v1_0.py`

Upstream:
- `Research/full_evidence_candidate_evaluator_v1_0.py`
- `Research/full_evidence_candidate_input_contract_v1_0.py`
- `Research/full_evidence_candidate_transition_engine_v1_0.py`

Downstream mapper:
`Research/risk_budget_execution_v0_1.py`

## 2. Frozen integration chain
`CandidateInput -> Candidate Transition Decision -> Candidate Target Risk Budget -> Step-5 Connector -> Risk Budget Execution v0.1 -> Core/Tactical/Leverage result`

Market Intelligence and Portfolio Execution remain separated.

The connector does not accept a second manual `full_evidence_authorized` market input. A Candidate `REDUCE` decision is the Full Evidence reduction permission at this boundary.

Separate portfolio authorities remain explicit and are never fabricated:
- `core_reduction_authorized`
- `leverage_restore_authorized`
- `risk_coefficients_complete`

## 3. HOLD / BLOCKED safety
- Candidate `HOLD` -> no mapper execution and portfolio unchanged.
- Candidate `BLOCKED` -> no mapper execution and portfolio unchanged.
- No market HOLD/BLOCKED state can silently become a portfolio trade.

## 4. Direction lock
The connector prevents direction inversion when actual portfolio risk differs from the logical Candidate state after prior partial execution.

- Candidate `REDUCE` can never restore risk.
- Candidate `RESTORE` can never reduce risk.
- If actual risk is already at/below a REDUCE target, no mapper action occurs.
- If actual risk is already at/above a RESTORE target, no mapper action occurs.

## 5. Candidate target vs execution target
Two targets are explicitly separated:

- `candidate_target_risk_budget`: the frozen market-state target chosen by the Transition Engine.
- `execution_target_risk_budget`: the maximum portfolio movement allowed in the current execution call.

If prior partial execution caused actual portfolio risk to lag the Candidate state, one execution call is capped by the current Candidate `allowed_step_size`.

Therefore:
- ordinary actual reduction cannot exceed the Candidate step limit,
- normal restoration cannot exceed the Candidate step limit,
- Fast V-Rebound actual restoration cannot exceed +20pp,
- the Candidate market target is not rewritten merely because the portfolio could not reach it in one call.

A remaining gap is reported explicitly as:
`PARTIAL / CANDIDATE TARGET NOT YET REACHED`.

## 6. Existing mapper hierarchy preserved
Reduction remains:
1. Leverage first,
2. Tactical second,
3. Core last and only with explicit Core reduction authority.

Restoration remains:
1. Core first,
2. Tactical second,
3. Leverage last and only with separate leverage restoration authority.

Core Preservation Gate remains unchanged.

Missing exact risk coefficients remain `DATA PARTIAL`; no beta/volatility coefficient is invented.

## 7. Deterministic validation
Test implementation:
`Research/test_full_evidence_candidate_risk_budget_connector_v1_0.py`

Workflow:
`.github/workflows/run_full_evidence_candidate_risk_budget_connector_v1_0_tests.yml`

GitHub Actions run:
`35230565533`

Workflow result: **SUCCESS**.

Reproducible result files:
- `Research/results/full_evidence_candidate_risk_budget_connector_v1_0_test_results.md`
- `Research/results/full_evidence_candidate_risk_budget_connector_v1_0_test_results.json`

Result: **13/13 PASS**.

Validated cases:
- HOLD produces no portfolio action,
- Candidate reduction consumes Leverage first,
- same Candidate target maps differently by sleeve composition without changing the market target,
- Core Preservation Gate retained,
- explicit Core authority permits residual Core reduction,
- restoration starts with Core,
- leverage restoration remains separately authorized,
- missing exact risk multipliers remain DATA PARTIAL,
- REDUCE cannot invert into restoration,
- RESTORE cannot invert into reduction,
- lagged actual portfolio execution respects Candidate step cap,
- Fast V-Rebound actual portfolio move is capped at +20pp,
- BLOCKED Candidate never executes portfolio action.

## 8. Implementation references
- Connector implementation commit: `fcfcf0b477e527920ad197dd8c8978d7f0c8f487`
- Deterministic test implementation commit: `2cd8a6fb86df64a4e0029411057e4f655389e6a5`
- CI workflow commit: `1d82c731ed694315409009323e9a98ae4fa97f10`
- Result markdown blob: `b61545539f6ef08d0cff84677b91ec24f053b78c`

## 9. Step boundary
Step 5 is complete.

Step 5 does **not** yet append the Candidate/portfolio result into the production Runtime Log or replace Dashboard ingestion.

The next implementation step is **Step 6 — connect Dashboard normalized Candidate input -> Transition -> Risk Budget Connector -> canonical Runtime Log**, while preserving append-only signal semantics, existing outcome updater/monitor compatibility, and no rewrite of the first prospective sample.

## 10. Version lock
Any future change to:
- market-authority derivation,
- direction-inversion protection,
- Candidate-target vs execution-target separation,
- actual movement cap,
- Core/Leverage authority separation,
requires a new connector version rather than silent modification.
