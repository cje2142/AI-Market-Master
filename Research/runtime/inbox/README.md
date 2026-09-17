# Dashboard Runtime Inbox v0.1

This folder receives normalized prospective AI Market Master 3.2 Dashboard snapshot JSON files.

Production ingestion workflow:
`.github/workflows/ingest_dashboard_runtime_snapshot_v0_1.yml`

Rules:
- only signal-time snapshots belong here
- do not backfill historical outcomes as prospective samples
- missing C1-C8 values must remain explicit
- each JSON push is validated by Dashboard Runtime Logger Adapter v0.1
- valid new samples append to `full_evidence_runtime_log_v0_1.jsonl`
- duplicate samples are skipped
- invalid snapshots fail closed

The folder itself is not an official 3.2 Authority source.
