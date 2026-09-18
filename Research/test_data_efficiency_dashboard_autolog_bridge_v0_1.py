import json
import tempfile
import unittest
from pathlib import Path

import data_efficiency_dashboard_autolog_bridge_v0_1 as bridge
import process_data_efficiency_dashboard_inbox_v0_1 as processor


def comp(status, value):
    return {"status": status, "value": value}


def snapshot(sample_id="AUTO-1"):
    return {
        "sample_id": sample_id,
        "market_date": "2026-09-18",
        "timestamp": "2026-09-18T10:06:00+09:00",
        "session_checkpoint": "10:06 INTRADAY PREVIEW",
        "official": {
            "C1": comp("VERIFIED", 0.27),
            "C2": comp("VERIFIED", 0.79),
            "C3": comp("VERIFIED", 0.32),
            "C4": comp("VERIFIED", -0.56),
            "C5": comp("PARTIAL", 0.21),
            "C6": comp("VERIFIED", -0.23),
            "C7": comp("PARTIAL", -0.17),
            "C8": comp("VERIFIED", 0.34),
            "SAI": 0.1646,
        },
        "official_regime": "R7 Deep Correction / R8 Transition Watch",
        "de_raw": {
            "r_kospi": 0.0215,
            "r_kosdaq": 0.0071,
            "r_kospi200": 0.0240,
            "r_krx100": None,
            "r_usdkrw": 0.0009,
            "d_ktb3y_bp": None,
        },
        "C8_effect": "POSITIVE_SHADOW_SUPPORT",
    }


class AutoLogBridgeTests(unittest.TestCase):
    def test_bridge_builds_candidate_automatically(self):
        out = bridge.build_comparator_snapshot(snapshot())
        self.assertAlmostEqual(out["candidate"]["C4"]["value"], -0.376)
        self.assertEqual(out["candidate"]["C4"]["status"], "PARTIAL")
        self.assertAlmostEqual(out["candidate"]["C6"]["value"], -0.1125)
        self.assertEqual(out["candidate"]["C6"]["status"], "PARTIAL")
        self.assertEqual(out["candidate_regime"], out["official_regime"])

    def test_append_and_duplicate_guard(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "runtime.jsonl"
            bridge.append_autolog_snapshot(snapshot(), log)
            with self.assertRaises(ValueError):
                bridge.append_autolog_snapshot(snapshot(), log)

    def test_processor_skips_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            inbox = Path(d) / "inbox"
            inbox.mkdir()
            log = Path(d) / "runtime.jsonl"
            (inbox / "a.json").write_text(
                json.dumps(snapshot("AUTO-2"), ensure_ascii=False),
                encoding="utf-8",
            )
            first = processor.process_inbox(inbox, log)
            second = processor.process_inbox(inbox, log)
            self.assertEqual(first[0]["status"], "APPENDED")
            self.assertEqual(second[0]["status"], "SKIP DUPLICATE")

    def test_missing_required_field_rejected(self):
        s = snapshot()
        del s["de_raw"]
        with self.assertRaises(ValueError):
            bridge.build_comparator_snapshot(s)


if __name__ == "__main__":
    unittest.main()
