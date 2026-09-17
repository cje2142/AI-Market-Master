# AI Market Master 3.2 — Dashboard Candidate Runtime Pipeline v1.0
## Step 6 Validation Backup — 2026-09-17

Status: **EXPERIMENTAL PROSPECTIVE VALIDATION PIPELINE / 12 OF 12 PASS / NOT OFFICIAL 3.2 AUTHORITY**

## 1. Purpose
Complete Step 6 of the Full Evidence Candidate v1.0 implementation chain:

`Dashboard -> Candidate Input Contract -> Evidence Gate / Transition -> Risk Budget Mapper (when portfolio exists) -> Runtime Log -> Outcome Updater -> Validation Monitor`

This layer automates plumbing only. It does not change official C1-C8 formulas, Regime rules, Strategy Action Index, AI Master Score state, Candidate thresholds, Risk Budget Execution v0.1 semantics, Runtime Log semantics, or Protocol v0.2 adoption criteria.

## 2. Implemented files
Primary adapter:
`Research/dashboard_candidate_runtime_adapter_v1_0.py`

Inbox processor:
`Research/process_dashboard_candidate_runtime_inbox_v1_0.py`

Deterministic tests:
`Research/test_dashboard_candidate_runtime_adapter_v1_0.py`

Test workflow:
`.github/workflows/run_dashboard_candidate_runtime_adapter_v1_0_tests.yml`

Production ingestion workflow:
`.github/workflows/ingest_dashboard_candidate_runtime_v1_0.yml`

Candidate production inbox:
`Research/runtime/candidate_inbox/*.json`

Canonical output remains:
- `Research/runtime/full_evidence_runtime_log_v0_1.jsonl`
- `Research/runtime/full_evidence_runtime_log_v0_1.csv`

## 3. Automatic execution chain
A valid Candidate Dashboard snapshot now causes the following deterministic sequence:

1. Preserve top-level official Dashboard C1-C8 `status/value`.
2. Require explicit Candidate `trend/polarity/strength` for every C1-C8 category.
3. Require every Candidate structural flag explicitly.
4. Require explicit Previous Overlay State and Cost Gate state.
5. Build and validate frozen `CandidateInput v1.0`.
6. Run Candidate Evidence Gate / Transition Engine v1.0.
7. Produce `HOLD / REDUCE / RESTORE / BLOCKED` and one frozen target state `100/95/90/80/70/60`.
8. If portfolio context exists, run Candidate -> Risk Budget Connector v1.0 and Risk Budget Execution v0.1.
9. If portfolio context is absent, preserve the market decision and record `mapper_status = NOT MAPPED`.
10. Append the signal to the canonical append-only Runtime Log and regenerate CSV projection.
11. Existing Outcome Updater and Runtime Validation Monitor continue to consume the same canonical Runtime Log.

## 4. No hidden inference boundary
Step 6 deliberately does not derive Candidate evidence labels from raw numeric C1-C8 values.

The Dashboard snapshot must explicitly supply for every C1-C8:
- `trend`
- `polarity`
- `strength`

All Candidate structural flags are also explicit. Missing flags cannot silently default to False in the production adapter.

This preserves the Step-1/Step-2 rule that no hidden numeric threshold may be invented for improving/deteriorating/strong evidence.

## 5. Portfolio separation
Portfolio data is optional.

Without portfolio data:
- Candidate market action/target is still logged,
- no sleeve action is fabricated,
- mapper status is `NOT MAPPED`.

With portfolio data:
- Candidate decides market target/direction,
- portfolio composition controls sleeve mapping only,
- Leverage -> Tactical -> Core reduction hierarchy remains unchanged,
- Core -> Tactical -> separately-authorized Leverage restoration remains unchanged,
- Core reduction authority and Leverage restoration authority remain separate,
- missing exact risk coefficients remain `DATA PARTIAL`.

HOLD/BLOCKED can never become a portfolio trade.
REDUCE can never invert into restoration.
RESTORE can never invert into reduction.

## 6. Stable sample identity / append-only protection
Candidate v1.0 sample ID uses the Dashboard checkpoint identity:
- market date,
- signal timestamp,
- session checkpoint,
- data mode.

Portfolio state and derived Candidate execution are excluded from the ID.

Therefore reprocessing the same market checkpoint with changed portfolio/derived execution does not silently create a second prospective signal. The existing Runtime Log duplicate guard blocks the rewrite; a documented CORRECTION must be used for a genuine signal-time correction.

## 7. Legacy compatibility boundary
The pre-Candidate Dashboard inbox remains:
`Research/runtime/inbox/*.json`

Candidate v1.0 uses a separate production inbox:
`Research/runtime/candidate_inbox/*.json`

Reason:
- legacy snapshots do not contain the frozen Candidate v1.0 explicit evidence/flag contract,
- old snapshots must not be silently interpreted under new Candidate semantics,
- the 2026-09-17 prospective sample already stored in the canonical Runtime Log is preserved and is not rewritten/backfilled by Step 6.

## 8. Deterministic validation result
GitHub Actions run:
`35231305780`

Result: **SUCCESS**.

Deterministic result: **12/12 PASS**.

Validated cases:
- Dashboard -> Candidate HOLD -> Runtime sample,
- R4 reduction -> Leverage-first portfolio mapping,
- Candidate-level conflict -> HOLD / no portfolio trade,
- BLOCKED -> no execution,
- explicit evidence labels mandatory,
- explicit complete structural flags mandatory,
- sample identity independent of portfolio,
- recovery -> Core-first mapping,
- Leverage restoration authority remains separate,
- missing exact risk coefficients -> DATA PARTIAL,
- end-to-end candidate inbox -> JSONL + CSV projection,
- duplicate checkpoint -> SKIP DUPLICATE / no silent rewrite.

Reproducible results:
- `Research/results/dashboard_candidate_runtime_adapter_v1_0_test_results.md`
- `Research/results/dashboard_candidate_runtime_adapter_v1_0_test_results.json`

Result markdown blob:
`7f2a4d0bc0aefa35f7d3873067bb0562741dd6da`

## 9. Implementation commits
- Dashboard Candidate runtime adapter: `f5c419f4e2f20cfdd9daa441ddb9f90d83f967d1`
- Candidate inbox processor: `4b02cda7a61b9bf1f00ced90a78b0e76b1c98de0`
- Step 6 deterministic tests: `ba2fb3dcec88711d99719e7c124620d6d05463d9`
- Step 6 CI workflow: `dfea66ecc603a81214ba2120c772dcc0cba9b701`
- Candidate production ingestion workflow: `afbac9b05bc3d0e72c7543e8cfb13541c05f4b69`

## 10. Operational state after Step 6
Steps 1-6 are now implemented:

1. Candidate Evidence Gate evaluator — implemented.
2. Candidate Input Contract — implemented/frozen.
3. Transition Engine — implemented/frozen.
4. Deterministic transition validation — 22/22 PASS.
5. Candidate -> Risk Budget Connector — implemented, 13/13 PASS.
6. Dashboard -> Candidate -> Mapper -> Runtime Log automatic pipeline — implemented, 12/12 PASS.

The system is now ready for prospective Candidate v1.0 data accumulation under Runtime Validation Protocol v0.2.

This does **not** mean Candidate v1.0 is adopted or official. Provisional adoption remains data-dependent under Protocol v0.2, and official 3.2 integration remains separately blocked until the required validation stage is reached.
