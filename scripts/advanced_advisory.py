#!/usr/bin/env python3
"""
Swiss Advanced Tax Advisory & Decision Engine
Includes:
1. Quellensteuer NOV (Nachträgliche ordentliche Veranlagung) Decision Evaluator
2. Healthcare Franchise Optimizer (Franchise 300 vs. 2500 inflection point)
3. Cantonal / Communal Relocation & Steuerfuss What-If Simulator
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

from swiss_tax_math import calculate_swiss_tax, CANTONAL_PROFILES

def evaluate_quellensteuer_nov(
    annual_gross_income_chf: float,
    canton: str,
    commune: Optional[str] = "Capital",
    civil_status: str = "SINGLE",
    children_count: int = 0,
    withheld_quellensteuer_chf: Optional[float] = None,
    additional_deductions: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Evaluates whether a B-permit resident should apply for NOV (Ordinary Tax Assessment).
    Important: In Switzerland, filing NOV is irrevocable once approved and applies for all future years!
    """
    additional_deductions = additional_deductions or {}

    # Estimate default Quellensteuer paid if not provided (typical flat withholding is 12% - 18%)
    if withheld_quellensteuer_chf is None or withheld_quellensteuer_chf <= 0:
        base_rate = 0.14 if canton.upper() in ["ZH", "BE", "VD", "GE"] else 0.11
        withheld_quellensteuer_chf = round(annual_gross_income_chf * base_rate, 2)

    # Calculate ordinary tax liability with all claimed deductions (e.g. 3a, commute, Kita)
    ordinary_calc = calculate_swiss_tax(
        gross_income_chf=annual_gross_income_chf,
        canton=canton,
        commune=commune,
        civil_status=civil_status,
        children_count=children_count,
        deductions=additional_deductions
    )
    ordinary_total_tax = ordinary_calc["total_tax_chf"]

    # Difference: Positive = Refund (Advantage), Negative = Tax Clawback / Surcharge (Disadvantage)
    net_difference_chf = round(withheld_quellensteuer_chf - ordinary_total_tax, 2)
    is_favorable = net_difference_chf > 0

    recommendation = (
        f"RECOMMENDED: You stand to receive an estimated tax refund of CHF {net_difference_chf:,.2f} "
        f"by declaring ordinary deductions (especially Pillar 3a and childcare)."
        if is_favorable else
        f"NOT RECOMMENDED (HIGH RISK): In ordinary taxation, you would owe an additional CHF {abs(net_difference_chf):,.2f} "
        f"due to local communal multipliers (Steuerfuss) in {commune}. Keep paying standard Quellensteuer!"
    )

    return {
        "status": "success",
        "canton": canton.upper(),
        "commune": commune,
        "gross_income_chf": annual_gross_income_chf,
        "withheld_quellensteuer_chf": withheld_quellensteuer_chf,
        "ordinary_tax_liability_chf": ordinary_total_tax,
        "net_difference_chf": net_difference_chf,
        "action": "PROCEED_WITH_NOV" if is_favorable else "RETAIN_QUELLENSTEUER",
        "recommendation": recommendation,
        "irrevocability_warning": (
            "Caution: Once an NOV application is granted, you are permanently bound to filing "
            "ordinary Swiss tax returns in all future years as long as you reside in Switzerland."
        )
    }

def optimize_health_franchise(
    expected_annual_medical_cost_chf: float,
    monthly_premium_franchise_300_chf: float = 450.0,
    monthly_premium_franchise_2500_chf: float = 320.0
) -> Dict[str, Any]:
    """
    Calculates the exact total financial burden between Franchise 300 and Franchise 2500,
    and identifies the break-even medical expense point (typically between CHF 1,800 and CHF 2,000).
    Total Cost = (12 * Monthly Premium) + Out-of-pocket (Franchise + 10% co-pay up to 700 CHF cap)
    """
    def calc_total_cost(premium_monthly: float, franchise: float, medical_spend: float) -> float:
        fixed_premium = premium_monthly * 12.0
        # Patient pays 100% of costs up to franchise
        deductible_portion = min(medical_spend, franchise)
        remaining = max(0.0, medical_spend - deductible_portion)
        # 10% Selbstbehalt up to 700 CHF max
        copay_portion = min(700.0, remaining * 0.10)
        return round(fixed_premium + deductible_portion + copay_portion, 2)

    cost_300 = calc_total_cost(monthly_premium_franchise_300_chf, 300.0, expected_annual_medical_cost_chf)
    cost_2500 = calc_total_cost(monthly_premium_franchise_2500_chf, 2500.0, expected_annual_medical_cost_chf)

    # Mathematical break-even inflection threshold
    annual_premium_diff = (monthly_premium_franchise_300_chf - monthly_premium_franchise_2500_chf) * 12.0
    # Difference in franchise = 2200. At 10% copay, the inflection point is approx 300 + (2200 - annual_premium_diff)/0.9
    break_even_spend = round(300.0 + max(0.0, (2200.0 - annual_premium_diff) / 0.9), 2)

    preferred = "FRANCHISE_2500" if cost_2500 <= cost_300 else "FRANCHISE_300"
    savings_chf = round(abs(cost_300 - cost_2500), 2)

    return {
        "status": "success",
        "expected_medical_spend_chf": expected_annual_medical_cost_chf,
        "total_annual_cost_franchise_300_chf": cost_300,
        "total_annual_cost_franchise_2500_chf": cost_2500,
        "recommended_franchise": preferred,
        "annual_savings_chf": savings_chf,
        "break_even_spend_chf": break_even_spend,
        "explanation": (
            f"If your expected annual health bills are under CHF {break_even_spend:,.2f}, Franchise 2500 saves you money. "
            f"Currently Franchise {preferred.replace('FRANCHISE_', '')} saves you CHF {savings_chf:,.2f} per year."
        )
    }

def simulate_relocation_tax_impact(
    gross_income_chf: float,
    current_canton: str,
    target_canton: str,
    civil_status: str = "SINGLE",
    children_count: int = 0
) -> Dict[str, Any]:
    """
    Simulates the relocation tax delta between two Swiss cantons/communes (e.g. Bern vs. Zug or Zurich).
    """
    tax_current = calculate_swiss_tax(
        gross_income_chf=gross_income_chf,
        canton=current_canton,
        civil_status=civil_status,
        children_count=children_count
    )
    tax_target = calculate_swiss_tax(
        gross_income_chf=gross_income_chf,
        canton=target_canton,
        civil_status=civil_status,
        children_count=children_count
    )

    diff_chf = round(tax_current["total_tax_chf"] - tax_target["total_tax_chf"], 2)

    return {
        "status": "success",
        "gross_income_chf": gross_income_chf,
        "origin_canton": current_canton.upper(),
        "origin_tax_chf": tax_current["total_tax_chf"],
        "origin_effective_rate": tax_current["effective_tax_rate_pct"],
        "target_canton": target_canton.upper(),
        "target_tax_chf": tax_target["total_tax_chf"],
        "target_effective_rate": tax_target["effective_tax_rate_pct"],
        "annual_tax_difference_chf": diff_chf,
        "financial_verdict": (
            f"Moving from {current_canton.upper()} to {target_canton.upper()} SAVES you CHF {diff_chf:,.2f} per year in taxes."
            if diff_chf > 0 else
            f"Moving from {current_canton.upper()} to {target_canton.upper()} INCREASES your annual taxes by CHF {abs(diff_chf):,.2f}."
        )
    }

def main():
    parser = argparse.ArgumentParser(description="Advanced Swiss Tax Advisory Decision Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: nov
    nov_p = subparsers.add_parser("nov", help="Evaluate Quellensteuer NOV application")
    nov_p.add_argument("--income", type=float, required=True, help="Annual gross income in CHF")
    nov_p.add_argument("--canton", type=str, default="BE")
    nov_p.add_argument("--commune", type=str, default="Capital")
    nov_p.add_argument("--deductions", type=str, default="{\"s4\": 7258}", help="JSON string of deductions")
    nov_p.add_argument("--withheld", type=float, default=None, help="Quellensteuer withheld in CHF")

    # Subcommand: franchise
    fr_p = subparsers.add_parser("franchise", help="Optimize health insurance franchise (300 vs 2500)")
    fr_p.add_argument("--spend", type=float, required=True, help="Expected annual healthcare costs in CHF")
    fr_p.add_argument("--premium-300", type=float, default=450.0, help="Monthly basic premium for Franchise 300")
    fr_p.add_argument("--premium-2500", type=float, default=320.0, help="Monthly basic premium for Franchise 2500")

    # Subcommand: relocation
    rel_p = subparsers.add_parser("relocation", help="Simulate tax delta of moving to another canton")
    rel_p.add_argument("--income", type=float, required=True, help="Annual gross income in CHF")
    rel_p.add_argument("--from-canton", type=str, required=True)
    rel_p.add_argument("--to-canton", type=str, required=True)

    args = parser.parse_args()

    if args.command == "nov":
        deds = json.loads(args.deductions)
        res = evaluate_quellensteuer_nov(
            annual_gross_income_chf=args.income,
            canton=args.canton,
            commune=args.commune,
            withheld_quellensteuer_chf=args.withheld,
            additional_deductions=deds
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "franchise":
        res = optimize_health_franchise(
            expected_annual_medical_cost_chf=args.spend,
            monthly_premium_franchise_300_chf=args.premium_300,
            monthly_premium_franchise_2500_chf=args.premium_2500
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "relocation":
        res = simulate_relocation_tax_impact(
            gross_income_chf=args.income,
            current_canton=args.from_canton,
            target_canton=args.to_canton
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
