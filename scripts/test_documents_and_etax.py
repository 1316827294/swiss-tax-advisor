#!/usr/bin/env python3
"""
Unit tests for parse_documents.py and etax_guide_generator.py.
"""

import unittest
import os
import shutil
import tempfile
import json

import parse_documents
import etax_guide_generator
import user_profile

class TestDocumentsAndEtax(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.orig_docs_dir = parse_documents.DOCS_DIR
        self.orig_user_dir = user_profile.USER_DIR
        self.orig_profile_path = user_profile.PROFILE_PATH
        self.orig_reports_dir = user_profile.REPORTS_DIR

        parse_documents.DOCS_DIR = os.path.join(self.test_dir, "documents")
        user_profile.USER_DIR = os.path.join(self.test_dir, "user")
        user_profile.PROFILE_PATH = os.path.join(user_profile.USER_DIR, "profile.json")
        user_profile.REPORTS_DIR = os.path.join(user_profile.USER_DIR, "reports")

        os.makedirs(parse_documents.DOCS_DIR, exist_ok=True)
        os.makedirs(user_profile.USER_DIR, exist_ok=True)

    def tearDown(self):
        parse_documents.DOCS_DIR = self.orig_docs_dir
        user_profile.USER_DIR = self.orig_user_dir
        user_profile.PROFILE_PATH = self.orig_profile_path
        user_profile.REPORTS_DIR = self.orig_reports_dir
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_lohnausweis_text_parsing(self):
        sample_cert = """
        Lohnausweis 2025
        Arbeitgeber: Test Company AG
        1. Lohn / Salaire: 120'000.00 CHF
        9. Beiträge BVG: 7'500.00 CHF
        13.1 Kantine: X
        """
        fpath = os.path.join(parse_documents.DOCS_DIR, "salary_2025.txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(sample_cert)

        scan_res = parse_documents.scan_documents_folder(2025)
        self.assertEqual(scan_res["status"], "SUCCESS")
        self.assertEqual(scan_res["documents_found"], 1)
        self.assertEqual(scan_res["extracted_summary"]["gross_income_chf"], 120000.0)
        self.assertTrue(scan_res["extracted_summary"]["canteen_subsidized"])

    def test_etax_guide_generation(self):
        user_profile.cmd_set("profile", {"address": {"canton": "ZH", "commune": "Zürich"}}, 2025)
        user_profile.cmd_set("tax", {
            "income": {"gross_chf": 110000},
            "deductions": {"s1_commute_chf": 3200, "s4_pillar3a_chf": 7258}
        }, 2025)

        guide_res = etax_guide_generator.generate_etax_guide(2025)
        self.assertEqual(guide_res["status"], "SUCCESS")
        self.assertEqual(guide_res["canton"], "ZH")
        self.assertIn("Code 110", guide_res["guide_markdown"])
        self.assertIn("110,000.00", guide_res["guide_markdown"])
        self.assertIn("Code 410", guide_res["guide_markdown"])
        self.assertTrue(os.path.exists(guide_res["guide_path"]))

if __name__ == "__main__":
    unittest.main()
