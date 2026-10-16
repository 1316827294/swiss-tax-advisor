#!/usr/bin/env python3
"""
equity_and_crossborder.py — RSU lockup discounts (ESTV KS 37) & overseas assets (Satzbestimmung).

Specialized high-net-worth & tech employee modules:
  1. RSU / ESPP Sperrfrist Valuation Discount according to ESTV Kreisschreiben Nr. 37:
     Discount factor = 1 / (1.06 ^ years)
     e.g., 5-year lockup grants a 25.27% discount on taxable market value!
  2. Overseas Real Estate & Foreign Assets Progression (Satzbestimmend, DBG Art. 6 & 7):
     Exempt from direct Swiss income/wealth tax, but determines worldwide progressive tax tariff.

Usage:
  python3 scripts/equity_and_crossborder.py rsu --market-value 100000 --lockup-years 3 --canton ZH
  python3 scripts/equity_and_crossborder.py foreign-property --swiss-income 150000 --foreign-rental-income 20000 --foreign-property-val 500000 --canton ZH
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import swiss_tax_math
import marginal_rate_calc

def calculate_rsu_sperrfrist_discount(
    market_value_chf: float,
    lockup_years: int,
    canton: str = "ZH",
    civil_status: str = "SINGLE",
    base_gross_salary_chf: float = 150000.0
) -> Dict[str, Any]:
    """
    Computes statutory discount on restricted stock units (RSU / ESPP / Mitarbeiteraktien)
    under Swiss Federal Tax Administration (ESTV) Kreisschreiben Nr. 37 (KS 37).
    Statutory formula:
      Steuerwert-Faktor = 1 / (1.06 ^ lockup_years)
    """
    years = max(0, min(10, lockup_years))
    discount_factor = 1.0 / (1.06 ** years)
    discount_pct = round((1.0 - discount_factor) * 100.0, 2)

    taxable_rsu_value = round(market_value_chf * discount_factor, 2)
    tax_exempt_discount_chf = round(market_value_chf - taxable_rsu_value, 2)

    # Estimate marginal tax rate savings
    try:
        marginal_calc = marginal_rate_calc.calculate_marginal_rate(
            annual_gross_income_chf=base_gross_salary_chf,
            canton=canton,
            civil_status=civil_status,
            claimed_deduction_chf=tax_exempt_discount_chf,
            category="OTHER"
        )
        marginal_rate = marginal_calc.get("marginal_rate_pct", 30.0)
    except Exception:
        marginal_rate = 30.0
    cash_saved = round(tax_exempt_discount_chf * (marginal_rate / 100.0), 2)

    return {
        "status": "SUCCESS",
        "legal_basis": "ESTV Kreisschreiben Nr. 37 (KS 37) Ziff. 4.2",
        "market_value_chf": market_value_chf,
        "lockup_years": years,
        "statutory_discount_percent": discount_pct,
        "taxable_rsu_value_chf": taxable_rsu_value,
        "tax_exempt_discount_chf": tax_exempt_discount_chf,
        "marginal_tax_rate_pct": marginal_rate,
        "estimated_tax_savings_chf": cash_saved,
        "summary_zh": (
            f"根据联邦税务局 KS 37 号通函，锁定期为 {years} 年的限制性股票（RSU）享有 "
            f"**{discount_pct}%** 的官方估值折扣（Diskontierung）。"
            f"申报应税市值从 CHF {market_value_chf:,.2f} 降至 **CHF {taxable_rsu_value:,.2f}**，"
            f"免税折价额 CHF {tax_exempt_discount_chf:,.2f}，直接为您省下约 **CHF {cash_saved:,.2f}** 税款！"
        )
    }

def calculate_foreign_property_satzbestimmung(
    swiss_income_chf: float,
    foreign_rental_income_chf: float,
    foreign_property_val_chf: float,
    canton: str = "ZH",
    commune: str = "Capital",
    civil_status: str = "SINGLE"
) -> Dict[str, Any]:
    """
    Computes tax progression impact of overseas real estate (Satzbestimmendes Auslandvermögen).
    Under DBG Art. 6 Abs. 1 & 7, foreign real estate is exempt from direct Swiss tax,
    but determines the worldwide tax rate bracket applied to Swiss-sourced income.
    """
    worldwide_income = swiss_income_chf + foreign_rental_income_chf

    # Calculate worldwide tariff rate
    worldwide_calc = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=worldwide_income,
        canton=canton,
        commune=commune,
        civil_status=civil_status
    )
    effective_worldwide_rate_pct = worldwide_calc.get("effective_tax_rate_pct", 20.0)

    # Apply worldwide rate strictly to Swiss-source income
    actual_swiss_tax = round(swiss_income_chf * (effective_worldwide_rate_pct / 100.0), 2)

    # Pure domestic tax without foreign property (for transparency)
    pure_domestic_calc = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=swiss_income_chf,
        canton=canton,
        commune=commune,
        civil_status=civil_status
    )
    pure_domestic_tax = pure_domestic_calc.get("total_tax_chf", 0.0)
    progression_delta = round(actual_swiss_tax - pure_domestic_tax, 2)

    return {
        "status": "SUCCESS",
        "legal_basis": "DBG Art. 6 Abs. 1 & Art. 7 (Freistellung unter Progressionsvorbehalt)",
        "swiss_income_chf": swiss_income_chf,
        "foreign_rental_income_chf": foreign_rental_income_chf,
        "foreign_property_valuation_chf": foreign_property_val_chf,
        "worldwide_taxable_income_chf": worldwide_income,
        "applicable_worldwide_rate_pct": effective_worldwide_rate_pct,
        "actual_swiss_tax_payable_chf": actual_swiss_tax,
        "pure_domestic_tax_chf": round(pure_domestic_tax, 2),
        "progression_tax_delta_chf": progression_delta,
        "compliance_note_zh": (
            "合规提示：海外房产及租金在瑞士【100% 免税】，但必须如实申报用于确定税率（Satzbestimmung）。"
            f"因全球合并税率微调，瑞士本国实际应纳税额为 CHF {actual_swiss_tax:,.2f}。"
            "合规披露可彻底杜绝瑞士税局反洗钱与未申报境外资产稽查风险！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="Equity (RSU/ESPP) & Cross-Border asset engine")
    sub = parser.add_subparsers(dest="cmd")

    p_rsu = sub.add_parser("rsu", help="Compute RSU Sperrfrist discount under KS 37")
    p_rsu.add_argument("--market-value", type=float, required=True)
    p_rsu.add_argument("--lockup-years", type=int, default=3)
    p_rsu.add_argument("--canton", type=str, default="ZH")
    p_rsu.add_argument("--civil-status", type=str, default="SINGLE")
    p_rsu.add_argument("--base-salary", type=float, default=150000.0)

    p_fp = sub.add_parser("foreign-property", help="Compute foreign property progression (Satzbestimmung)")
    p_fp.add_argument("--swiss-income", type=float, required=True)
    p_fp.add_argument("--foreign-rental-income", type=float, default=0.0)
    p_fp.add_argument("--foreign-property-val", type=float, default=0.0)
    p_fp.add_argument("--canton", type=str, default="ZH")
    p_fp.add_argument("--commune", type=str, default="Capital")
    p_fp.add_argument("--civil-status", type=str, default="SINGLE")

    args = parser.parse_args()

    if args.cmd == "rsu":
        res = calculate_rsu_sperrfrist_discount(
            market_value_chf=args.market_value,
            lockup_years=args.lockup_years,
            canton=args.canton,
            civil_status=args.civil_status,
            base_gross_salary_chf=args.base_salary
        )
    elif args.cmd == "foreign-property":
        res = calculate_foreign_property_satzbestimmung(
            swiss_income_chf=args.swiss_income,
            foreign_rental_income_chf=args.foreign_rental_income,
            foreign_property_val_chf=args.foreign_property_val,
            canton=args.canton,
            commune=args.commune,
            civil_status=args.civil_status
        )
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
