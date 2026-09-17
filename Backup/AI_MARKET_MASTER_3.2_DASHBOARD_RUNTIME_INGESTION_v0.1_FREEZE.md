# AI Market Master 3.2 — Dashboard Runtime Ingestion v0.1
## Design Freeze

Date: 2026-09-17
Status: EXPERIMENTAL INGESTION BRIDGE / NOT OFFICIAL 3.2 AUTHORITY

## Purpose
Make a validated Dashboard snapshot append to Full Evidence Runtime Log v0.1 through the already-tested Dashboard Runtime Logger Adapter v0.1.

Flow:
`Dashboard -> normalized snapshot JSON -> Research/runtime/inbox -> GitHub Actions -> Adapter -> canonical JSONL -> CSV projection`

## Frozen rules
- Inbox files are immutable signal-time inputs and are not rewritten after outcomes are known.
- Processor scans inbox JSON files deterministically.
- Same underlying snapshot produces the same adapter sample_id; duplicate samples are skipped, never appended twice.
- Invalid snapshots fail ingestion rather than being silently repaired.
- Runtime JSONL remains the canonical prospective journal.
- CSV remains a deterministic projection.
- Processor does not calculate C1-C8, Regime, Evidence Gate, target risk budget, or portfolio weights.
- No production sample is created during bridge validation.

## Concurrency safety
GitHub Actions ingestion uses a single concurrency group with `cancel-in-progress: false` so simultaneous inbox pushes are serialized rather than cancelling an earlier prospective sample.

## Production trigger
Only new/changed `Research/runtime/inbox/*.json` files trigger production ingestion.
Adapter/test/code commits alone must not create a prospective market sample.

## Failure behavior
- invalid input -> workflow FAIL / no commit
- duplicate sample -> SKIP DUPLICATE / no second journal entry
- valid new sample -> append JSONL, regenerate CSV, commit both

## Version lock
Any change to duplicate behavior, inbox retention, production trigger, or concurrency semantics requires v0.2 or later.
