import unittest
import sys
import os

# 将 scripts 目录加入 sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swiss_tax_math import calculate_swiss_tax, round_to_5_rappen
from marginal_rate_calc import calculate_marginal_rate
from family_marriage_sim import calculate_dual_earner_deduction, simulate_marriage_tax_impact
from audit_risk_evaluator import evaluate_tax_audit_risk
from advanced_advisory import evaluate_quellensteuer_nov, optimize_health_franchise, simulate_relocation_tax_impact

class TestSwissTaxMath(unittest.TestCase):
    def test_round_to_5_rappen(self):
        self.assertEqual(round_to_5_rappen(100), 100)
        self.assertEqual(round_to_5_rappen(102), 100)
        self.assertEqual(round_to_5_rappen(103), 105)
        self.assertEqual(round_to_5_rappen(107), 105)
        self.assertEqual(round_to_5_rappen(108), 110)

    def test_calculate_single_bern_tax(self):
        res = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="BE",
            commune="Bern",
            civil_status="SINGLE",
            children_count=0,
            deductions={"s1": 3300.0, "s2": 3200.0, "s4": 7258.0}
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["gross_income_chf"], 100000.0)
        self.assertEqual(res["total_deductions_chf"], 13758.0)
        self.assertEqual(res["taxable_income_chf"], 86242.0)
        self.assertGreater(res["federal_tax_chf"], 0.0)
        self.assertGreater(res["cantonal_tax_chf"], 0.0)
        self.assertGreater(res["communal_tax_chf"], 0.0)
        self.assertGreater(res["total_tax_chf"], 0.0)
        self.assertGreater(res["effective_tax_rate_pct"], 0.0)

    def test_calculate_married_zurich_tax(self):
        res = calculate_swiss_tax(
            gross_income_chf=150000.0,
            canton="ZH",
            commune="Zürich",
            civil_status="MARRIED",
            children_count=2,
            deductions={"s4": 7258.0, "s6": 15000.0}
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["civil_status"], "MARRIED")
        self.assertEqual(res["canton"], "ZH")
        self.assertGreater(res["total_tax_chf"], 0.0)

class Test26CantonsDeductionRules(unittest.TestCase):
    def test_geneva_commute_cap_500(self):
        # Geneva has a very strict 500 CHF commute cap for cantonal tax
        res = calculate_swiss_tax(
            gross_income_chf=120000.0,
            canton="GE",
            deductions={"s1": 4000.0}
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["itemized_deductions_chf"]["s1"], 500.0)

    def test_zug_unlimited_commute_deduction(self):
        # Zug allows full actual commute deduction
        res = calculate_swiss_tax(
            gross_income_chf=150000.0,
            canton="ZG",
            deductions={"s1": 8500.0}
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["itemized_deductions_chf"]["s1"], 8500.0)

    def test_disability_deduction_zero_hurdle(self):
        # Disability expenses have zero 5% threshold
        res = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="BE",
            deductions={"behinderung": 4500.0}
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["itemized_deductions_chf"]["behinderung"], 4500.0)

    def test_insurance_premiums_capping_be_zh_ge(self):
        # BE Single cap = 2400 CHF
        res_be = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="BE",
            civil_status="SINGLE",
            insurance_premiums_chf=3000.0
        )
        self.assertEqual(res_be["status"], "success")
        self.assertEqual(res_be["itemized_deductions_chf"]["insurance_premiums"], 2400.0)

        # ZH Single cap = 2600 CHF
        res_zh = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="ZH",
            civil_status="SINGLE",
            insurance_premiums_chf=3000.0
        )
        self.assertEqual(res_zh["status"], "success")
        self.assertEqual(res_zh["itemized_deductions_chf"]["insurance_premiums"], 2600.0)

        # GE Single: Geneva allows full actual KVG premium
        res_ge = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="GE",
            civil_status="SINGLE",
            insurance_premiums_chf=5000.0
        )
        self.assertEqual(res_ge["status"], "success")
        self.assertEqual(res_ge["itemized_deductions_chf"]["insurance_premiums"], 5000.0)

        # BE Married with 2 children: cap 4800 + 2*0 = 4800 CHF
        res_be_fam = calculate_swiss_tax(
            gross_income_chf=120000.0,
            canton="BE",
            civil_status="MARRIED",
            children_count=2,
            insurance_premiums_chf=6000.0
        )
        self.assertEqual(res_be_fam["itemized_deductions_chf"]["insurance_premiums"], 4800.0)

    def test_higher_education_deduction_ge_vd_ne_be(self):
        # GE: Cap 13,000 CHF
        res_ge = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="GE",
            higher_education_expenses_chf=15000.0
        )
        self.assertEqual(res_ge["itemized_deductions_chf"]["higher_education_expenses"], 13000.0)

        # VD: Cap 7,400 CHF
        res_vd = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="VD",
            higher_education_expenses_chf=10000.0
        )
        self.assertEqual(res_vd["itemized_deductions_chf"]["higher_education_expenses"], 7400.0)

        # NE: Cap 6,000 CHF
        res_ne = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="NE",
            higher_education_expenses_chf=8000.0
        )
        self.assertEqual(res_ne["itemized_deductions_chf"]["higher_education_expenses"], 6000.0)

        # BE: Cap 0 CHF
        res_be = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="BE",
            higher_education_expenses_chf=8000.0
        )
        self.assertEqual(res_be["itemized_deductions_chf"]["higher_education_expenses"], 0.0)

    def test_rent_relief_deduction_zg_vd_be(self):
        # ZG: Reineinkommen <= 75,000 CHF -> Max 5,000 CHF
        res_zg_low = calculate_swiss_tax(
            gross_income_chf=70000.0,
            canton="ZG",
            rent_expenses_chf=6000.0
        )
        self.assertEqual(res_zg_low["itemized_deductions_chf"]["rent_expenses"], 5000.0)
        self.assertEqual(res_zg_low["taxable_income_chf"], 65000.0)

        # ZG: Reineinkommen > 75,000 CHF -> 0 CHF
        res_zg_high = calculate_swiss_tax(
            gross_income_chf=100000.0,
            canton="ZG",
            rent_expenses_chf=6000.0
        )
        self.assertEqual(res_zg_high["itemized_deductions_chf"]["rent_expenses"], 0.0)

        # VD: Reineinkommen <= 60,000 CHF -> Max 4,000 CHF
        res_vd_low = calculate_swiss_tax(
            gross_income_chf=50000.0,
            canton="VD",
            rent_expenses_chf=6000.0
        )
        self.assertEqual(res_vd_low["itemized_deductions_chf"]["rent_expenses"], 4000.0)

        # VD: Reineinkommen > 60,000 CHF -> 0 CHF
        res_vd_high = calculate_swiss_tax(
            gross_income_chf=80000.0,
            canton="VD",
            rent_expenses_chf=6000.0
        )
        self.assertEqual(res_vd_high["itemized_deductions_chf"]["rent_expenses"], 0.0)

        # BE: Other cantons -> 0 CHF
        res_be = calculate_swiss_tax(
            gross_income_chf=50000.0,
            canton="BE",
            rent_expenses_chf=6000.0
        )
        self.assertEqual(res_be["itemized_deductions_chf"]["rent_expenses"], 0.0)

class TestMarginalRateCalc(unittest.TestCase):
    def test_marginal_rate_bern(self):
        res = calculate_marginal_rate(
            annual_gross_income_chf=100000.0,
            canton="BE",
            civil_status="SINGLE",
            claimed_deduction_chf=7258.0
        )
        self.assertEqual(res["status"], "success")
        self.assertGreater(res["marginal_rate_pct"], 15.0)
        self.assertLess(res["marginal_rate_pct"], 45.0)
        self.assertGreater(res["cash_saved_per_100_chf"], 15.0)
        self.assertGreater(res["estimated_total_cash_saved_chf"], 1000.0)

class TestFamilyMarriageSim(unittest.TestCase):
    def test_dual_earner_deduction(self):
        # 50% of 20,000 = 10,000 CHF
        d1 = calculate_dual_earner_deduction(lower_spouse_net_income_chf=20000.0)
        self.assertEqual(d1["deduction_chf"], 10000.0)
        # 50% of 40,000 = 20,000 -> capped at 14,100 CHF
        d2 = calculate_dual_earner_deduction(lower_spouse_net_income_chf=40000.0)
        self.assertEqual(d2["deduction_chf"], 14100.0)

    def test_simulate_marriage_tax_impact(self):
        sim = simulate_marriage_tax_impact(
            earner_a_gross_chf=110000.0,
            earner_b_gross_chf=75000.0,
            canton="BE",
            children_count=1
        )
        self.assertEqual(sim["status"], "success")
        self.assertIn("marriage_impact_chf", sim)
        self.assertIn("penalty_or_bonus", sim)

class TestAuditRiskEvaluator(unittest.TestCase):
    def test_clean_safe_assessment(self):
        res = evaluate_tax_audit_risk(
            annual_net_income_chf=90000.0,
            claimed_s7_education_chf=2500.0,
            claimed_s1_commute_chf=3000.0,
            has_missing_proofs=False
        )
        self.assertGreaterEqual(res["overall_risk_score"], 90)
        self.assertEqual(res["overall_risk_level"], "LOW")
        self.assertTrue(res["can_proceed_safely"])

    def test_high_risk_education_and_missing_proofs(self):
        res = evaluate_tax_audit_risk(
            annual_net_income_chf=80000.0,
            claimed_s7_education_chf=18000.0,
            claimed_s1_commute_chf=6500.0,
            is_commute_car_in_sbb_zone=True,
            has_missing_proofs=True,
            missing_proof_count=3
        )
        self.assertLess(res["overall_risk_score"], 70)
        self.assertEqual(res["overall_risk_level"], "HIGH")
        self.assertFalse(res["can_proceed_safely"])
        self.assertGreater(len(res["flagged_items"]), 0)

class TestAdvancedAdvisory(unittest.TestCase):
    def test_nov_evaluation(self):
        res = evaluate_quellensteuer_nov(
            annual_gross_income_chf=110000.0,
            canton="ZH",
            withheld_quellensteuer_chf=18000.0,
            additional_deductions={"s4": 7258.0, "s1": 3300.0}
        )
        self.assertEqual(res["status"], "success")
        self.assertIn("net_difference_chf", res)
        self.assertIn(res["action"], ["PROCEED_WITH_NOV", "RETAIN_QUELLENSTEUER"])

    def test_franchise_optimization(self):
        # Very low healthcare spending -> 2500 franchise should win
        low_res = optimize_health_franchise(expected_annual_medical_cost_chf=400.0)
        self.assertEqual(low_res["recommended_franchise"], "FRANCHISE_2500")

        # Very high healthcare spending -> 300 franchise should win
        high_res = optimize_health_franchise(expected_annual_medical_cost_chf=6000.0)
        self.assertEqual(high_res["recommended_franchise"], "FRANCHISE_300")

    def test_relocation_simulation(self):
        res = simulate_relocation_tax_impact(
            gross_income_chf=150000.0,
            current_canton="BE",
            target_canton="ZG"
        )
        self.assertEqual(res["status"], "success")
        # Moving from high-tax Bern to low-tax Zug should save substantial money
        self.assertGreater(res["annual_tax_difference_chf"], 5000.0)

class TestEndToEndTaxWorkflow(unittest.TestCase):
    def test_full_family_lifecycle(self):
        # 1. Math tax calculation
        tax_res = calculate_swiss_tax(
            gross_income_chf=170000.0,
            canton="BE",
            commune="Bern",
            civil_status="MARRIED",
            children_count=1,
            deductions={
                "s1": 3300.0,
                "s2": 3200.0,
                "s4": 7258.0,
                "s6": 18000.0,
                "s7": 9000.0
            }
        )
        self.assertEqual(tax_res["status"], "success")
        self.assertGreater(tax_res["total_tax_chf"], 0.0)
        self.assertEqual(tax_res["total_deductions_chf"], 40758.0)

        # 2. Marginal rate check
        m_res = calculate_marginal_rate(
            annual_gross_income_chf=170000.0,
            canton="BE",
            civil_status="MARRIED",
            children_count=1,
            claimed_deduction_chf=7258.0,
            category="PILLAR_3A"
        )
        self.assertEqual(m_res["status"], "success")
        self.assertGreater(m_res["marginal_rate_pct"], 20.0)
        self.assertEqual(m_res["pillar_3a_analysis"]["remaining_gap_chf"], 0.0)

        # 3. Dual earner deduction check
        dual_res = calculate_dual_earner_deduction(lower_spouse_net_income_chf=45000.0, canton="BE")
        self.assertEqual(dual_res["deduction_chf"], 14100.0)

        # 4. Marriage penalty check
        m_sim = simulate_marriage_tax_impact(
            earner_a_gross_chf=125000.0,
            earner_b_gross_chf=45000.0,
            canton="BE",
            children_count=1
        )
        self.assertEqual(m_sim["status"], "success")
        self.assertIn("marriage_impact_chf", m_sim)

        # 5. Audit risk radar
        risk_res = evaluate_tax_audit_risk(
            annual_net_income_chf=170000.0,
            claimed_s7_education_chf=9000.0,
            claimed_s1_commute_chf=3300.0,
            has_missing_proofs=False
        )
        self.assertEqual(risk_res["status"], "success")
        # 9,000 CHF exceeds the 8,000 CHF benchmark, should be flagged
        flagged_categories = [item["category"] for item in risk_res["flagged_items"]]
        self.assertIn("S7_WEITERBILDUNG", flagged_categories)

if __name__ == "__main__":
    unittest.main()
