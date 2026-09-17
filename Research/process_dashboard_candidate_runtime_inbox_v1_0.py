"""Process Candidate v1.0 Dashboard snapshots into the canonical Runtime Log."""

import argparse
import json
from pathlib import Path

import dashboard_candidate_runtime_adapter_v1_0 as adapter


def process_inbox(inbox_dir, log_path, csv_path):
    inbox_dir = Path(inbox_dir)
    files = sorted(inbox_dir.glob("*.json")) if inbox_dir.exists() else []
    results = []

    for path in files:
        with path.open("r", encoding="utf-8") as f:
            snapshot = json.load(f)
        try:
            _, sample = adapter.append_dashboard_candidate_snapshot(snapshot, log_path, csv_path)
            results.append({
                "file": str(path),
                "sample_id": sample["sample_id"],
                "action_direction": sample["action_direction"],
                "target_risk_budget": sample["target_risk_budget"],
                "mapper_status": sample["mapper_status"],
                "status": "APPENDED",
            })
        except ValueError as exc:
            if "duplicate sample_id" in str(exc):
                results.append({
                    "file": str(path),
                    "sample_id": adapter.sample_id_for(snapshot),
                    "status": "SKIP DUPLICATE",
                })
                continue
            raise

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Process Dashboard Candidate v1.0 inbox into Full Evidence Runtime Log v0.1"
    )
    parser.add_argument("--inbox", default="Research/runtime/candidate_inbox")
    parser.add_argument("--log", default="Research/runtime/full_evidence_runtime_log_v0_1.jsonl")
    parser.add_argument("--csv", default="Research/runtime/full_evidence_runtime_log_v0_1.csv")
    args = parser.parse_args()

    results = process_inbox(args.inbox, args.log, args.csv)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
