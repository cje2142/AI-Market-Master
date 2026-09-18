import tempfile
import unittest
from pathlib import Path

import data_efficiency_runtime_comparator_v0_3 as cmp


def comp(status="VERIFIED", value=0.1):
    return {"status": status, "value": value}


def snapshot(sample_id="S1"):
    official = {f"C{i}": comp(value=0.1) for i in range(1, 9)}
    candidate = {f"C{i}": comp(value=0.1) for i in range(1, 8)}
    official["SAI"] = 0.20
    candidate["SAI_DE"] = 0.25
    return {
        "sample_id": sample_id,
        "market_date": "2026-09-18",
        "timestamp": "2026-09-18T09:03:00+09:00",
        "session_checkpoint": "09:03",
        "official": official,
        "candidate": candidate,
        "official_regime": "R7",
        "candidate_regime": "R7",
    }


class ComparatorCorrectionTests(unittest.TestCase):
    def test_append_correction_and_projection(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.jsonl"
            cmp.append_comparison(p, snapshot())
            cmp.append_correction(
                p,
                "S1",
                {"candidate_de_v01": {"SAI_DE": 0.40}},
                "fix test",
            )
            row = cmp.build_projection(p)[0]
            self.assertEqual(row["candidate_de_v01"]["SAI_DE"], 0.40)
            self.assertEqual(row["last_revision"], 1)
            self.assertEqual(row["last_correction_reason"], "fix test")

    def test_correction_requires_reason(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.jsonl"
            cmp.append_comparison(p, snapshot())
            with self.assertRaises(ValueError):
                cmp.append_correction(p, "S1", {"x": 1}, "")

    def test_correction_unknown_sample_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "log.jsonl"
            with self.assertRaises(ValueError):
                cmp.append_correction(p, "NOPE", {"x": 1}, "reason")


if __name__ == "__main__":
    unittest.main()
