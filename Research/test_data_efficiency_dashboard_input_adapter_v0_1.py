import unittest

import data_efficiency_dashboard_input_adapter_v0_1 as de


def comp(status, value):
    return {"status": status, "value": value}


BASE = {
    "C1": comp("VERIFIED", 0.04),
    "C2": comp("VERIFIED", 1.00),
    "C3": comp("VERIFIED", 1.00),
    "C5": comp("PARTIAL", 0.21),
    "C7": comp("PARTIAL", 0.06),
}


class DataEfficiencyDashboardInputTests(unittest.TestCase):
    def test_full_c4_and_c6_inputs(self):
        raw = {
            "r_kospi": 0.0236,
            "r_kosdaq": 0.0123,
            "r_kospi200": 0.0250,
            "r_krx100": 0.0240,
            "r_usdkrw": -0.0007,
            "d_ktb3y_bp": 2.0,
        }
        out = de.build_candidate_snapshot(BASE, raw)
        self.assertEqual(out["candidate"]["C4"]["status"], "VERIFIED")
        self.assertEqual(out["candidate"]["C6"]["status"], "VERIFIED")
        self.assertEqual(out["candidate_status"], "PARTIAL")  # C5/C7 are preview/partial
        self.assertAlmostEqual(out["candidate_coverage"], 1.0)

    def test_missing_three_new_fields_reproduces_first_e2e_gap(self):
        raw = {
            "r_kospi": 0.0236,
            "r_kosdaq": 0.0123,
            "r_kospi200": None,
            "r_krx100": None,
            "r_usdkrw": -0.0007,
            "d_ktb3y_bp": None,
        }
        out = de.build_candidate_snapshot(BASE, raw)
        self.assertEqual(out["candidate"]["C4"]["status"], "DATA UNAVAILABLE")
        self.assertEqual(out["candidate"]["C6"]["status"], "PARTIAL")
        self.assertGreater(out["candidate_coverage"], 0.70)
        self.assertEqual(out["candidate_status"], "PARTIAL")

    def test_c4_partial_with_one_large_cap_index(self):
        raw = {
            "r_kospi": 0.01,
            "r_kosdaq": 0.008,
            "r_kospi200": 0.012,
            "r_krx100": None,
            "r_usdkrw": 0.0,
            "d_ktb3y_bp": 0.0,
        }
        out = de.build_candidate_snapshot(BASE, raw)
        self.assertEqual(out["candidate"]["C4"]["status"], "PARTIAL")

    def test_c6_fx_only_is_partial(self):
        raw = {
            "r_kospi": 0.01,
            "r_kosdaq": 0.008,
            "r_kospi200": 0.012,
            "r_krx100": 0.011,
            "r_usdkrw": 0.004,
            "d_ktb3y_bp": None,
        }
        out = de.build_candidate_snapshot(BASE, raw)
        self.assertEqual(out["candidate"]["C6"]["status"], "PARTIAL")
        self.assertAlmostEqual(out["candidate"]["C6"]["value"], -0.5)

    def test_fx_sign_is_inverted(self):
        c6 = de.compute_c6({"r_usdkrw": 0.008, "d_ktb3y_bp": 0.0})
        self.assertAlmostEqual(c6["details"]["FX"], -1.0)

    def test_ktb_sign_is_inverted(self):
        c6 = de.compute_c6({"r_usdkrw": 0.0, "d_ktb3y_bp": 10.0})
        self.assertAlmostEqual(c6["details"]["KTB"], -1.0)


if __name__ == "__main__":
    unittest.main()
