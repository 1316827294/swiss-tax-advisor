#!/usr/bin/env python3
"""
Unit tests for advanced features:
  1. What-If Simulator (Marriage, Child, Relocation, Capital Withdrawal)
  2. Equity & Cross-Border (RSU lockup discounts under KS 37, Foreign Property Satzbestimmung)
  3. Einsprache Objection Generator (Diff comparison & BGE-grounded legal appeal letters)
"""

import unittest
import os
import shutil
import tempfile
import json

import whatif_simulator
import equity_and_crossborder
import einsprache_generator
import user_profile

class TestAdvancedFeatures(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.orig_user_dir = user_profile.USER_DIR
        self.orig_profile_path = user_profile.PROFILE_PATH
        self.orig_reports_dir = user_profile.REPORTS_DIR

        user_profile.USER_DIR = os.path.join(self.test_dir, "user")
        user_profile.PROFILE_PATH = os.path.join(user_profile.USER_DIR, "profile.json")
        user_profile.REPORTS_DIR = os.path.join(user_profile.USER_DIR, "reports")

        os.makedirs(user_profile.USER_DIR, exist_ok=True)
        user_profile.cmd_set("profile", {
            "personal": {"name": "Anna Meier", "ahv_masked": "756.9999.8888.77"},
            "address": {"canton": "ZH", "commune": "Zürich"},
            "civil_status": {"status": "SINGLE", "children_count": 0}
        }, 2025)
        user_profile.cmd_set("tax", {
            "income": {"gross_chf": 140000.0}
        }, 2025)

    def tearDown(self):
        user_profile.USER_DIR = self.orig_user_dir
        user_profile.PROFILE_PATH = self.orig_profile_path
        user_profile.REPORTS_DIR = self.orig_reports_dir
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_whatif_marriage(self):
        res = whatif_simulator.simulate_marriage(120000.0, 90000.0, "ZH")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreater(res["tax_as_singles_chf"], 0)
        self.assertGreater(res["tax_as_married_chf"], 0)
        self.assertIn("HEIRAT", res["outcome"])

    def test_whatif_child(self):
        res = whatif_simulator.simulate_child(1, 15000.0, 2025)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreater(res["annual_tax_saving_chf"], 0)
        self.assertLess(res["new_tax_chf"], res["base_tax_chf"])

    def test_whatif_relocation(self):
        res = whatif_simulator.simulate_relocation("ZG", "Zug", 2025)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["is_saving"])
        self.assertGreater(res["annual_difference_chf"], 0)

    def test_whatif_capital_withdrawal(self):
        res = whatif_simulator.simulate_capital_withdrawal(300000.0, "BE", years=3)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreater(res["tax_saved_chf"], 0)
        self.assertLess(res["staggered_total_tax_chf"], res["lump_sum_tax_chf"])

    def test_rsu_sperrfrist_discount_ks37(self):
        # 5 year lockup should give ~25.27% discount
        res = equity_and_crossborder.calculate_rsu_sperrfrist_discount(100000.0, 5, "ZH")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["statutory_discount_percent"], 25.27)
        self.assertEqual(res["taxable_rsu_value_chf"], 74725.82)
        self.assertGreater(res["estimated_tax_savings_chf"], 5000.0)

    def test_foreign_property_satzbestimmung(self):
        res = equity_and_crossborder.calculate_foreign_property_satzbestimmung(
            swiss_income_chf=120000.0,
            foreign_rental_income_chf=20000.0,
            foreign_property_val_chf=300000.0,
            canton="ZH"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreater(res["actual_swiss_tax_payable_chf"], 0)
        self.assertGreaterEqual(res["progression_tax_delta_chf"], 0)

    def test_einsprache_diff_and_letter(self):
        diff_res = einsprache_generator.compare_assessment(2025, {"commute": 3995.0, "training": 4000.0})
        self.assertEqual(diff_res["status"], "SUCCESS")
        self.assertEqual(diff_res["total_disputed_deductions_chf"], 7995.0)

        letter_res = einsprache_generator.generate_einsprache_letter(2025, ["commute", "homeoffice", "training"])
        self.assertEqual(letter_res["status"], "SUCCESS")
        self.assertTrue(os.path.exists(letter_res["path"]))
        self.assertIn("EINSPRACHE", letter_res["content"])
        self.assertIn("BGE 140 II 157", letter_res["content"])

if __name__ == "__main__":
    unittest.main()
