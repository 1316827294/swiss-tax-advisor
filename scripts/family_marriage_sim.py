#!/usr/bin/env python3
"""
Swiss Family, Dual-Earner & Marriage Tax Simulator
Calculates DBG Art. 33 Abs. 2 Zweitverdienerabzug, childcare deductions,
and simulates marriage penalty/bonus comparisons.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

from swiss_tax_math import calculate_swiss_tax, STATUTORY_LIMITS_RAPPEN

def calculate_dual_earner_deduction(
    lower_spouse_net_income_chf: float,
    canton: str = "BE"
) -> Dict[str, Any]:
    """
    Computes Dual-Earner Deduction (Zweitverdienerabzug / Déduction pour double gain)
    under DBG Art. 33 Abs. 2.
    Formula: 50% of the lower spouse's earned income, min CHF 8,600, max CHF 14,100.
    """
    if lower_spouse_net_income_chf <= 0:
        return {
            "status": "success",
            "deduction_chf": 0.0,
            "legal_basis": "DBG Art. 33 Abs. 2",
            "note": "No dual earner deduction applicable when one spouse has zero earned income."
        }

    raw_50_pct = lower_spouse_net_income_chf * 0.50
    min_cap = STATUTORY_LIMITS_RAPPEN["DUAL_EARNER_MIN"] / 100.0
    max_cap = STATUTORY_LIMITS_RAPPEN["DUAL_EARNER_MAX"] / 100.0

    # If lower earner makes less than min_cap, deduction is their full income (cannot exceed income)
    deduction = max(min_cap, raw_50_pct)
    deduction = min(deduction, max_cap)
    deduction = min(deduction, lower_spouse_net_income_chf)

    return {
        "status": "success",
        "lower_spouse_income_chf": lower_spouse_net_income_chf,
        "deduction_chf": round(deduction, 2),
        "legal_basis": "DBG Art. 33 Abs. 2",
        "min_cap_chf": min_cap,
        "max_cap_chf": max_cap
    }

def calculate_childcare_deduction(
    actual_cost_chf: float,
    children_count: int = 1,
    canton: str = "BE"
) -> Dict[str, Any]:
    """
    Computes Childcare deduction (Drittbetreuungskosten / Frais de garde)
    under DBG Art. 33 Abs. 3.
    Capped at CHF 25,500 per child per year.
    """
    effective_children = max(1, children_count)
    max_allowable = (STATUTORY_LIMITS_RAPPEN["CHILDCARE_FEDERAL_MAX"] / 100.0) * effective_children
    allowed_deduction = min(actual_cost_chf, max_allowable)

    return {
        "status": "success",
        "actual_cost_chf": actual_cost_chf,
        "children_count": effective_children,
        "allowed_deduction_chf": round(allowed_deduction, 2),
        "max_allowable_cap_chf": max_allowable,
        "legal_basis": "DBG Art. 33 Abs. 3"
    }

def calculate_home_office_deduction(
    monthly_rent_chf: float,
    total_rooms: float,
    days_wfh_per_week: float
) -> Dict[str, Any]:
    """
    Computes standard Home Office rent deduction formula recognized by Swiss courts:
    Annual Deduction = Monthly Rent / (Total Rooms + 2) * (WFH Days / 5) * 12
    """
    if total_rooms <= 0 or days_wfh_per_week <= 0 or monthly_rent_chf <= 0:
        return {"status": "success", "annual_deduction_chf": 0.0}

    factor = (1.0 / (total_rooms + 2.0)) * (min(5.0, days_wfh_per_week) / 5.0)
    annual_ded = monthly_rent_chf * factor * 12.0

    return {
        "status": "success",
        "monthly_rent_chf": monthly_rent_chf,
        "total_rooms": total_rooms,
        "days_wfh_per_week": days_wfh_per_week,
        "annual_deduction_chf": round(annual_ded, 2),
        "legal_basis": "BGE 140 II 157 / Praxis StG"
    }

def simulate_marriage_tax_impact(
    earner_a_gross_chf: float,
    earner_b_gross_chf: float,
    canton: str = "BE",
    commune: Optional[str] = "Capital",
    children_count: int = 0
) -> Dict[str, Any]:
    """
    Simulates the marriage tax impact (Marriage Penalty vs Bonus)
    by contrasting two single assessments vs one joint married assessment.
    """
    # Track 1: Two independent single assessments
    # Split children if any
    child_a = children_count // 2
    child_b = children_count - child_a

    tax_single_a = calculate_swiss_tax(
        gross_income_chf=earner_a_gross_chf,
        canton=canton,
        commune=commune,
        civil_status="SINGLE",
        children_count=child_a
    )["total_tax_chf"]

    tax_single_b = calculate_swiss_tax(
        gross_income_chf=earner_b_gross_chf,
        canton=canton,
        commune=commune,
        civil_status="SINGLE",
        children_count=child_b
    )["total_tax_chf"]

    total_single_taxes = round(tax_single_a + tax_single_b, 2)

    # Track 2: Joint married assessment with Dual Earner deduction
    joint_gross = earner_a_gross_chf + earner_b_gross_chf
    lower_income = min(earner_a_gross_chf, earner_b_gross_chf)
    dual_earner_res = calculate_dual_earner_deduction(lower_income, canton)
    dual_deduction = dual_earner_res["deduction_chf"]

    married_calc = calculate_swiss_tax(
        gross_income_chf=joint_gross,
        canton=canton,
        commune=commune,
        civil_status="MARRIED",
        children_count=children_count,
        deductions={"zweitverdiener": dual_deduction}
    )
    total_married_taxes = married_calc["total_tax_chf"]

    diff_chf = round(total_married_taxes - total_single_taxes, 2)
    is_penalty = diff_chf > 0

    return {
        "status": "success",
        "canton": canton.upper(),
        "earner_a_gross_chf": earner_a_gross_chf,
        "earner_b_gross_chf": earner_b_gross_chf,
        "joint_gross_income_chf": joint_gross,
        "dual_earner_deduction_chf": dual_deduction,
        "single_filing_total_tax_chf": total_single_taxes,
        "single_a_tax_chf": tax_single_a,
        "single_b_tax_chf": tax_single_b,
        "married_filing_tax_chf": total_married_taxes,
        "marriage_impact_chf": abs(diff_chf),
        "penalty_or_bonus": "PENALTY" if is_penalty else "BONUS",
        "explanation": (
            f"Under joint married filing, you pay CHF {abs(diff_chf):,.2f} "
            + ("MORE (Marriage Penalty / Heiratsstrafe) due to progressive bracket progression." if is_penalty
               else "LESS (Marriage Bonus / Steuerbonus) thanks to married split tariffs.")
        )
    }

def main():
    parser = argparse.ArgumentParser(description="Swiss Family and Marriage Tax Simulator")
    parser.add_argument("--earner-a", type=float, required=True, help="Spouse A gross income in CHF")
    parser.add_argument("--earner-b", type=float, required=True, help="Spouse B gross income in CHF")
    parser.add_argument("--canton", type=str, default="BE", help="Two-letter canton code")
    parser.add_argument("--children", type=int, default=0, help="Number of dependent minor children")
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")

    args = parser.parse_args()
    res = simulate_marriage_tax_impact(
        earner_a_gross_chf=args.earner_a,
        earner_b_gross_chf=args.earner_b,
        canton=args.canton,
        children_count=args.children
    )

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"--- Swiss Marriage Tax Impact Simulation ({res['canton']}) ---")
        print(f"Partner A Gross:     CHF {res['earner_a_gross_chf']:,.2f}")
        print(f"Partner B Gross:     CHF {res['earner_b_gross_chf']:,.2f}")
        print(f"Combined Gross:      CHF {res['joint_gross_income_chf']:,.2f}")
        print(f"Dual-Earner Abzug:   CHF {res['dual_earner_deduction_chf']:,.2f}")
        print(f"--------------------------------------------------")
        print(f"If Co-habiting Single: CHF {res['single_filing_total_tax_chf']:,.2f}")
        print(f"If Married Filing:     CHF {res['married_filing_tax_chf']:,.2f}")
        print(f"Result: {res['penalty_or_bonus']} -> CHF {res['marriage_impact_chf']:,.2f}")
        print(res["explanation"])

if __name__ == "__main__":
    main()
