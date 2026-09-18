"""Process DE Dashboard auto-log inbox into Runtime Comparator v0.3 journal."""

import argparse
import json
from pathlib import Path

import data_efficiency_dashboard_autolog_bridge_v0_1 as bridge


def process_inbox(inbox_dir, log_path):
    inbox_dir = Path(inbox_dir)
    files = sorted(inbox_dir.glob("*.json")) if inbox_dir.exists() else []
    results = []

    for path in files:
        with path.open("r", encoding="utf-8") as f:
            snapshot = json.load(f)
        try:
            event, comparator_snapshot = bridge.append_autolog_snapshot(snapshot, log_path)
            results.append({
                "file": str(path),
                "sample_id": event["sample_id"],
                "status": "APPENDED",
                "candidate_sai": event["payload"]["candidate_de_v01"]["SAI_DE"],
                "action_band_agreement": event["payload"]["comparison"]["action_band_agreement"],
            })
        except ValueError as exc:
            if "duplicate comparator sample_id" in str(exc):
                results.append({
                    "file": str(path),
                    "sample_id": bridge._sample_id(snapshot),
                    "status": "SKIP DUPLICATE",
                })
                continue
            raise

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Process Data Efficiency Dashboard inbox into Runtime Comparator v0.3"
    )
    parser.add_argument("--inbox", default="Research/runtime/de_inbox")
    parser.add_argument(
        "--log",
        default="Research/runtime/data_efficiency_runtime_comparator_v0_3.jsonl",
    )
    args = parser.parse_args()
    results = process_inbox(args.inbox, args.log)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
