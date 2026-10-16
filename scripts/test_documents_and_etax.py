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
import generate_deliverables

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

    def test_deliverables_generation_all_5(self):
        user_profile.cmd_set("profile", {
            "personal": {"name": "Test User", "permit_type": "B"},
            "address": {"canton": "BE", "commune": "Bern"},
            "civil_status": {"status": "SINGLE", "children_count": 0},
            "religion": {"church_tax_liable": False}
        }, 2025)
        user_profile.cmd_set("tax", {
            "income": {"gross_chf": 120000.0},
            "deductions": {"s1_commute_chf": 3995.0, "s2_meals_chf": 3200.0, "s4_pillar3a_chf": 7258.0},
            "wealth": {"bank_balance_31dec_chf": 50000.0}
        }, 2025)

        res = generate_deliverables.generate_all_deliverables(2025)
        self.assertEqual(res["status"], "ALL_DELIVERABLES_GENERATED")
        self.assertEqual(len(res["deliverables"]), 5)

        for d_name, d_info in res["deliverables"].items():
            self.assertEqual(d_info["status"], "SUCCESS")
            path = d_info["path"]
            self.assertIsNotNone(path, f"Path was None for {d_name}")
            self.assertTrue(os.path.exists(path), f"File {path} does not exist for {d_name}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 100)
                # Ensure no unfilled curly brace templates
                import re
                placeholders = re.findall(r'\{[a-zA-Z0-9_]+\}', content)
                self.assertEqual(placeholders, [], f"Unfilled placeholders found in {d_name}: {placeholders}")

    def test_broker_statement_parsing(self):
        sample_broker = """
        eSteuerausweis 2025 / Swissquote Bank AG
        Depotnummer: SQ-998877
        Steuerwert per 31.12.2025: 150'000.00 CHF
        Bruttoertrag Dividenden: 3'500.00 CHF
        Quellensteuer USA (DA-1): 525.00 CHF
        Depotgebühren: 250.00 CHF
        """
        fpath = os.path.join(parse_documents.DOCS_DIR, "swissquote_tax_2025.txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(sample_broker)

        scan_res = parse_documents.scan_documents_folder(2025)
        self.assertEqual(scan_res["status"], "SUCCESS")
        summary = scan_res["extracted_summary"]
        self.assertEqual(summary["securities_value_chf"], 150000.0)
        self.assertEqual(summary["dividend_income_chf"], 3500.0)
        self.assertEqual(summary["us_withholding_tax_chf"], 525.0)
        self.assertEqual(summary["depotgebuehren_chf"], 250.0)

    def test_renovation_invoice_parsing(self):
        sample_reno = """
        Handwerkerrechnung / Malerbetrieb Muster GmbH
        Projekt: Sanierung Fassade und Innenanstrich
        Rechnungsbetrag: 8'500.00 CHF
        """
        fpath = os.path.join(parse_documents.DOCS_DIR, "renovation_2025.txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(sample_reno)

        scan_res = parse_documents.scan_documents_folder(2025)
        self.assertEqual(scan_res["status"], "SUCCESS")
        summary = scan_res["extracted_summary"]
        self.assertEqual(summary["property_maintenance_chf"], 8500.0)

if __name__ == "__main__":
    unittest.main()

