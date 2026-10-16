#!/usr/bin/env python3
"""
Unit tests for user_profile.py state machine and onboarding pipeline.
"""

import unittest
import os
import shutil
import tempfile
from datetime import date

import user_profile

class TestUserProfilePipeline(unittest.TestCase):
    def setUp(self):
        # Use a temporary user directory for tests
        self.orig_user_dir = user_profile.USER_DIR
        self.orig_profile_path = user_profile.PROFILE_PATH
        self.orig_reports_dir = user_profile.REPORTS_DIR

        self.test_dir = tempfile.mkdtemp()
        user_profile.USER_DIR = self.test_dir
        user_profile.PROFILE_PATH = os.path.join(self.test_dir, "profile.json")
        user_profile.REPORTS_DIR = os.path.join(self.test_dir, "reports")

    def tearDown(self):
        user_profile.USER_DIR = self.orig_user_dir
        user_profile.PROFILE_PATH = self.orig_profile_path
        user_profile.REPORTS_DIR = self.orig_reports_dir
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_initial_state_and_next_question(self):
        nq = user_profile.cmd_next_question(2025)
        self.assertEqual(nq["status"], "IN_PROGRESS")
        self.assertEqual(nq["field"], "address.canton")
        self.assertIn("□", nq["progress_bar"])
        self.assertIn("zh", nq["prompts"])

    def test_progressive_profile_flow(self):
        # Set canton & commune
        res = user_profile.cmd_set("profile", {"address": {"canton": "zh", "commune": "Zürich"}}, 2025)
        self.assertFalse(res["is_ready_to_calculate"])
        self.assertGreater(res["progress_percent"], 0)

        # Check canton uppercase heuristic
        prof = user_profile.cmd_get("profile")
        self.assertEqual(prof["address"]["canton"], "ZH")

        # Set religion none heuristic
        user_profile.cmd_set("profile", {"religion": {"denomination": "none"}}, 2025)
        prof = user_profile.cmd_get("profile")
        self.assertFalse(prof["religion"]["church_tax_liable"])

    def test_report_saving(self):
        res = user_profile.cmd_save_report(2025, "steuerdossier", "# Test Report Content")
        self.assertEqual(res["status"], "saved")
        self.assertTrue(os.path.exists(res["path"]))
        with open(res["path"], "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "# Test Report Content")

if __name__ == "__main__":
    unittest.main()
