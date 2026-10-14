#!/usr/bin/env python3
"""
Swiss Marginal Tax Rate & Deduction Savings Calculator
Calculates exact marginal tax rates and direct cash savings for any Swiss canton
using deterministic delta calculations.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

from swiss_tax_math import calculate_swiss_tax, STATUTORY_LIMITS_RAPPEN

def calculate_marginal_rate(
    annual_gross_income_chf: float,
    canton: str = "BE",
    commune: Optional[str] = "Capital",
    civil_status: str = "SINGLE",
    children_count: int = 0,
    claimed_deduction_chf: float = 1000.0,
    category: str = "GENERAL"
) -> Dict[str, Any]:
    """
    Calculates the exact marginal tax rate by evaluating the delta tax reduction
    for an additional increment of deduction.
    """
    if annual_gross_income_chf <= 0:
        return {
            "status": "error",
            "message": "Gross income must be greater than zero."
        }

    # Base tax calculation with zero additional deduction
    base_calc = calculate_swiss_tax(
        gross_income_chf=annual_gross_income_chf,
        canton=canton,
        commune=commune,
        civil_status=civil_status,
        children_count=children_count,
        deductions={}
    )
    base_tax = base_calc["total_tax_chf"]

    # Delta test amount (standard 1,000 CHF delta to capture bracket slope accurately)
    delta_chf = 1000.0
    reduced_calc = calculate_swiss_tax(
        gross_income_chf=annual_gross_income_chf,
        canton=canton,
        commune=commune,
        civil_status=civil_status,
        children_count=children_count,
        deductions={"test_delta": delta_chf}
    )
    reduced_tax = reduced_calc["total_tax_chf"]

    tax_difference = max(0.0, base_tax - reduced_tax)
    marginal_rate = round((tax_difference / delta_chf) * 100.0, 2)
    cash_saved_per_100 = round((marginal_rate / 100.0) * 100.0, 2)

    # Actual deduction simulation for requested claimed amount
    claimed_calc = calculate_swiss_tax(
        gross_income_chf=annual_gross_income_chf,
        canton=canton,
        commune=commune,
        civil_status=civil_status,
        children_count=children_count,
        deductions={"claimed": claimed_deduction_chf}
    )
    total_cash_saved = round(max(0.0, base_tax - claimed_calc["total_tax_chf"]), 2)

    # Pillar 3a specific advice if category is PILLAR_3A
    pillar_3a_analysis = None
    if category.upper() in ["PILLAR_3A", "S4", "S4_SAEULE_3A"]:
        cap_chf = STATUTORY_LIMITS_RAPPEN["PILLAR_3A_EMPLOYED"] / 100.0
        remaining_gap_chf = max(0.0, cap_chf - claimed_deduction_chf)
        full_cap_calc = calculate_swiss_tax(
            gross_income_chf=annual_gross_income_chf,
            canton=canton,
            commune=commune,
            civil_status=civil_status,
            children_count=children_count,
            deductions={"s4": cap_chf}
        )
        potential_max_saved = round(max(0.0, base_tax - full_cap_calc["total_tax_chf"]), 2)
        additional_saving_opportunity = round(max(0.0, potential_max_saved - total_cash_saved), 2)
        pillar_3a_analysis = {
            "statutory_cap_chf": cap_chf,
            "already_claimed_chf": claimed_deduction_chf,
            "remaining_gap_chf": remaining_gap_chf,
            "potential_max_cash_saved_chf": potential_max_saved,
            "additional_saving_if_maxed_chf": additional_saving_opportunity
        }

    return {
        "status": "success",
        "canton": canton.upper(),
        "gross_income_chf": annual_gross_income_chf,
        "marginal_rate_pct": marginal_rate,
        "cash_saved_per_100_chf": cash_saved_per_100,
        "claimed_deduction_chf": claimed_deduction_chf,
        "estimated_total_cash_saved_chf": total_cash_saved,
        "pillar_3a_analysis": pillar_3a_analysis
    }

def main():
    parser = argparse.ArgumentParser(description="Swiss Marginal Tax Rate & Savings Calculator")
    parser.add_argument("--income", type=float, required=True, help="Annual gross income in CHF")
    parser.add_argument("--canton", type=str, default="BE", help="Two-letter canton code (e.g. BE, ZH, VD)")
    parser.add_argument("--commune", type=str, default="Capital", help="Municipality name")
    parser.add_argument("--status", type=str, default="SINGLE", choices=["SINGLE", "MARRIED", "REGISTERED_PARTNER"])
    parser.add_argument("--children", type=int, default=0, help="Number of dependent minor children")
    parser.add_argument("--deduction", type=float, default=1000.0, help="Proposed deductible expense in CHF")
    parser.add_argument("--category", type=str, default="GENERAL", help="Tax category (e.g. PILLAR_3A, S7_WEITERBILDUNG)")
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")

    args = parser.parse_args()
    res = calculate_marginal_rate(
        annual_gross_income_chf=args.income,
        canton=args.canton,
        commune=args.commune,
        civil_status=args.status,
        children_count=args.children,
        claimed_deduction_chf=args.deduction,
        category=args.category
    )

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"--- Marginal Tax Rate & Cash Savings Analysis ({res['canton']}) ---")
        print(f"Gross Income:             CHF {res['gross_income_chf']:,.2f}")
        print(f"Marginal Tax Rate:        {res['marginal_rate_pct']}%")
        print(f"Cash Saved per 100 CHF:   CHF {res['cash_saved_per_100_chf']:,.2f}")
        print(f"Claimed Expense:          CHF {res['claimed_deduction_chf']:,.2f}")
        print(f"Direct Tax Refund Cash:   CHF {res['estimated_total_cash_saved_chf']:,.2f}")
        if res["pillar_3a_analysis"]:
            p3 = res["pillar_3a_analysis"]
            print(f"Pillar 3a Max Potential:  CHF {p3['potential_max_cash_saved_chf']:,.2f}")
            print(f"Additional Savings Gap:   CHF {p3['additional_saving_if_maxed_chf']:,.2f} (Gap: CHF {p3['remaining_gap_chf']:,.2f})")

if __name__ == "__main__":
    main()
