import tempfile
import unittest
from pathlib import Path

import data_efficiency_runtime_comparator_v0_2 as cmp


def comp(status="VERIFIED", value=0.1):
    return {"status": status, "value": value}


def snapshot(sample_id="S1", official_sai=0.20, candidate_sai=0.25):
    official = {f"C{i}": comp(value=0.1) for i in range(1, 9)}
    candidate = {f"C{i}": comp(value=0.1) for i in range(1, 8)}
    official["C4"] = comp(value=0.20)
    candidate["C4"] = comp(value=0.05)
    official["C6"] = comp(value=-0.20)
    candidate["C6"] = comp(value=0.10)
    official["C8"] = comp(value=-0.50)
    official["SAI"] = official_sai
    candidate["SAI_DE"] = candidate_sai
    return {
        "sample_id": sample_id,
        "market_date": "2026-09-18",
        "timestamp": "2026-09-18T15:30:00+09:00",
        "session_checkpoint": "CLOSE",
        "official": official,
        "candidate": candidate,
        "official_regime": "R5 Risk-Off Transition",
        "candidate_regime": "R5 Risk-Off Transition",
        "C8_effect": "SHADOW_NEGATIVE",
        "missing_data_effect": 0.0,
    }


class RuntimeComparatorTests(unittest.TestCase):
    def test_build_comparison(self):
        row = cmp.build_comparison(snapshot())
        c = row["comparison"]
        self.assertAlmostEqual(c["SAI_delta_candidate_minus_official"], 0.05)
        self.assertTrue(c["direction_agreement"])
        self.assertTrue(c["regime_agreement"])
        self.assertAlmostEqual(c["C4_delta_candidate_minus_official"], -0.15)
        self.assertAlmostEqual(c["C6_delta_candidate_minus_official"], 0.30)
        self.assertTrue(c["C6_direction_flip"])
        self.assertAlmostEqual(c["C8_nominal_weighted_contribution"], -0.035)
        self.assertAlmostEqual(c["official_data_coverage"], 1.0)
        self.assertAlmostEqual(c["candidate_data_coverage"], 1.0)
        self.assertEqual(row["outcome"]["20d"], "PENDING")

    def test_material_divergence(self):
        row = cmp.build_comparison(snapshot(official_sai=-0.10, candidate_sai=0.10))
        self.assertTrue(row["comparison"]["material_sai_divergence"])
        self.assertFalse(row["comparison"]["direction_agreement"])

    def test_missing_component_reduces_coverage(self):
        s = snapshot()
        s["candidate"]["C4"] = {"status": "DATA UNAVAILABLE", "value": None}
        row = cmp.build_comparison(s)
        self.assertLess(row["comparison"]["candidate_data_coverage"], 1.0)

    def test_verified_missing_value_rejected(self):
        s = snapshot()
        s["official"]["C1"] = {"status": "VERIFIED", "value": None}
        with self.assertRaises(ValueError):
            cmp.build_comparison(s)

    def test_append_only_duplicate_guard(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "compare.jsonl"
            cmp.append_comparison(p, snapshot())
            with self.assertRaises(ValueError):
                cmp.append_comparison(p, snapshot())

    def test_outcome_matures_projection(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "compare.jsonl"
            cmp.append_comparison(p, snapshot())
            cmp.append_outcome(p, "S1", "5d", {
                "ret_5d": -0.03,
                "mae_5d": -0.05,
                "mfe_5d": 0.01,
                "risk_warning_useful_5d": True,
                "false_warning_5d": False,
            })
            row = cmp.build_projection(p)[0]
            self.assertEqual(row["outcome"]["5d"]["status"], "MATURE")
            self.assertAlmostEqual(row["outcome"]["5d"]["ret_5d"], -0.03)
            self.assertEqual(row["outcome"]["1d"], "PENDING")

    def test_duplicate_outcome_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "compare.jsonl"
            cmp.append_comparison(p, snapshot())
            cmp.append_outcome(p, "S1", "1d", {"ret_1d": 0.01})
            with self.assertRaises(ValueError):
                cmp.append_outcome(p, "S1", "1d", {"ret_1d": 0.02})


if __name__ == "__main__":
    unittest.main()


class ActionBandDiagnosticsTests(unittest.TestCase):
    def test_balanced_vs_positive_band_disagreement(self):
        row = cmp.build_comparison(snapshot(official_sai=0.2952, candidate_sai=0.4438356164383562))
        c = row["comparison"]
        self.assertEqual(c["official_action_band"], "BALANCED")
        self.assertEqual(c["candidate_action_band"], "POSITIVE")
        self.assertFalse(c["action_band_agreement"])
        self.assertFalse(c["material_sai_divergence"])

