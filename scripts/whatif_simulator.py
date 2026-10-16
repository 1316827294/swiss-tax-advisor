#!/usr/bin/env python3
"""
whatif_simulator.py — Interactive "What-If" tax scenario simulation engine for Swiss Tax Advisor.

Simulates major life decisions before filing:
  1. Marriage Penalty / Bonus (Heiratsstrafe vs. Splitting)
  2. Having Children (Child deductions, Kita, insurance caps)
  3. Canton / Commune Relocation (Inter-cantonal & inter-communal tax delta)
  4. Pension Capital Withdrawal (Lump sum vs. 3-5 year staggered withdrawal)

Usage:
  python3 scripts/whatif_simulator.py marriage --income1 120000 --income2 90000 --canton ZH
  python3 scripts/whatif_simulator.py child --children 1 --kita 20000 [year]
  python3 scripts/whatif_simulator.py relocation --canton ZG --commune Zug [year]
  python3 scripts/whatif_simulator.py capital-withdrawal --amount 300000 --canton BE --years 3
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, Optional

# Add script dir
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import swiss_tax_math
import user_profile

def simulate_marriage(
    income1_chf: float,
    income2_chf: float,
    canton: str,
    commune: str = "Capital",
    church_tax: bool = False
) -> Dict[str, Any]:
    """
    Simulates the Swiss "Heiratsstrafe" (Marriage Penalty) or Marriage Bonus.
    Compares:
      Scenario A: Two single taxpayers filing separately (Tarif A)
      Scenario B: Married couple filing jointly (Tarif B + Zweiverdienerabzug)
    """
    canton_upper = canton.upper().strip()
    church_str = "ROMAN_CATHOLIC" if church_tax else "NONE"

    # Scenario A: Separate filing as singles
    tax1 = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=income1_chf,
        canton=canton_upper,
        commune=commune,
        civil_status="SINGLE",
        children_count=0,
        church_tax=church_str,
        deductions={"s1": 3000, "s2": 3200, "s4": 7258},
        insurance_premiums_chf=2400
    )
    tax2 = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=income2_chf,
        canton=canton_upper,
        commune=commune,
        civil_status="SINGLE",
        children_count=0,
        church_tax=church_str,
        deductions={"s1": 3000, "s2": 3200, "s4": 7258},
        insurance_premiums_chf=2400
    )
    total_tax_single = tax1.get("total_tax_chf", 0.0) + tax2.get("total_tax_chf", 0.0)

    # Scenario B: Married couple (Joint filing)
    combined_income = income1_chf + income2_chf
    # Dual-earner deduction (Zweiverdienerabzug): 50% of lower income, max 13,600 CHF
    lower_income = min(income1_chf, income2_chf)
    zweiverdiener_abzug = min(13600.0, lower_income * 0.5)

    married_deductions = {
        "s1": 6000.0,
        "s2": 6400.0,
        "s4": 14516.0, # Both contribute 3a
        "zweiverdiener": zweiverdiener_abzug
    }

    tax_married = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=combined_income,
        canton=canton_upper,
        commune=commune,
        civil_status="MARRIED",
        children_count=0,
        church_tax=church_str,
        deductions=married_deductions,
        insurance_premiums_chf=4800
    )
    total_tax_married = tax_married.get("total_tax_chf", 0.0)

    diff = total_tax_married - total_tax_single
    is_penalty = diff > 0

    return {
        "status": "SUCCESS",
        "canton": canton_upper,
        "commune": commune,
        "partner1_income_chf": income1_chf,
        "partner2_income_chf": income2_chf,
        "combined_income_chf": combined_income,
        "tax_as_singles_chf": round(total_tax_single, 2),
        "tax_as_married_chf": round(total_tax_married, 2),
        "difference_chf": round(abs(diff), 2),
        "outcome": "HEIRATSSTRAFE (Marriage Penalty)" if is_penalty else "HEIRATSBONUS (Marriage Bonus)",
        "summary_zh": (
            f"结婚后联合申报总税负为 CHF {total_tax_married:,.2f}，单身独立申报合计为 CHF {total_tax_single:,.2f}。"
            f"{'面临“婚姻惩罚税”：每年多缴 CHF ' + f'{diff:,.2f}' if is_penalty else '享受“婚姻减税红利”：每年少缴 CHF ' + f'{-diff:,.2f}'}！"
        )
    }

def simulate_child(
    additional_children: int = 1,
    annual_kita_expenses_chf: float = 0.0,
    year: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulates tax reduction from having children (Kinderabzug + Kita Drittbetreuung).
    Loads base profile from user_profile.
    """
    prof = user_profile.cmd_get("profile")
    tax_data = user_profile.cmd_get("tax", year)

    canton = (prof.get("address", {}).get("canton") or "ZH").upper().strip()
    commune = prof.get("address", {}).get("commune") or "Capital"
    status = prof.get("civil_status", {}).get("status") or "SINGLE"
    base_children = prof.get("civil_status", {}).get("children_count") or 0
    gross = tax_data.get("income", {}).get("gross_chf") or 120000.0

    # 1. Base Tax before additional child
    base_calc = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=gross,
        canton=canton,
        commune=commune,
        civil_status=status,
        children_count=base_children,
        deductions={"s1": 3000, "s2": 3200, "s4": 7258}
    )
    base_tax = base_calc.get("total_tax_chf", 0.0)

    # 2. Tax with additional children & Kita
    new_children = base_children + additional_children
    new_deductions = {
        "s1": 3000,
        "s2": 3200,
        "s4": 7258,
        "s6": annual_kita_expenses_chf
    }
    new_calc = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=gross,
        canton=canton,
        commune=commune,
        civil_status=status,
        children_count=new_children,
        deductions=new_deductions
    )
    new_tax = new_calc.get("total_tax_chf", 0.0)
    tax_saved = max(0.0, base_tax - new_tax)

    return {
        "status": "SUCCESS",
        "canton": canton,
        "additional_children": additional_children,
        "annual_kita_expenses_chf": annual_kita_expenses_chf,
        "base_tax_chf": round(base_tax, 2),
        "new_tax_chf": round(new_tax, 2),
        "annual_tax_saving_chf": round(tax_saved, 2),
        "effective_relief_pct": round((tax_saved / base_tax) * 100, 1) if base_tax else 0.0,
        "summary_zh": (
            f"迎来 {additional_children} 位宝宝（含年托儿费 CHF {annual_kita_expenses_chf:,.0f}）后，"
            f"家庭年税负将从 CHF {base_tax:,.0f} 降至 CHF {new_tax:,.0f}，每年直接减税 CHF {tax_saved:,.0f}！"
        )
    }

def simulate_relocation(
    target_canton: str,
    target_commune: str = "Capital",
    year: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulates moving to another Canton / Commune (Stichtagsprinzip 31. Dezember).
    """
    prof = user_profile.cmd_get("profile")
    tax_data = user_profile.cmd_get("tax", year)

    cur_canton = (prof.get("address", {}).get("canton") or "BE").upper().strip()
    cur_commune = prof.get("address", {}).get("commune") or "Bern"
    status = prof.get("civil_status", {}).get("status") or "SINGLE"
    children = prof.get("civil_status", {}).get("children_count") or 0
    gross = tax_data.get("income", {}).get("gross_chf") or 120000.0

    # Current tax
    cur_calc = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=gross,
        canton=cur_canton,
        commune=cur_commune,
        civil_status=status,
        children_count=children,
        deductions={"s1": 3000, "s2": 3200, "s4": 7258}
    )
    cur_tax = cur_calc.get("total_tax_chf", 0.0)

    # Target tax
    tgt_canton_upper = target_canton.upper().strip()
    tgt_calc = swiss_tax_math.calculate_swiss_tax(
        gross_income_chf=gross,
        canton=tgt_canton_upper,
        commune=target_commune,
        civil_status=status,
        children_count=children,
        deductions={"s1": 3000, "s2": 3200, "s4": 7258}
    )
    tgt_tax = tgt_calc.get("total_tax_chf", 0.0)

    delta = cur_tax - tgt_tax
    is_saving = delta > 0

    return {
        "status": "SUCCESS",
        "current_location": f"{cur_canton} ({cur_commune})",
        "target_location": f"{tgt_canton_upper} ({target_commune})",
        "current_tax_chf": round(cur_tax, 2),
        "target_tax_chf": round(tgt_tax, 2),
        "annual_difference_chf": round(abs(delta), 2),
        "is_saving": is_saving,
        "summary_zh": (
            f"若在 12 月 31 日前迁往 {tgt_canton_upper} ({target_commune})，"
            f"{'每年可节省税金 CHF ' + f'{delta:,.2f}' if is_saving else '每年税金将增加 CHF ' + f'{-delta:,.2f}'}！"
        )
    }

def simulate_capital_withdrawal(
    total_capital_chf: float,
    canton: str,
    years: int = 1
) -> Dict[str, Any]:
    """
    Simulates pension capital withdrawal tax (Kapitalauszahlungssteuer für Säule 2 / 3a).
    Swiss progressive capital withdrawal tariff is heavily non-linear.
    Compares taking all capital in 1 year vs. spreading across 3 or 5 years.
    """
    canton_upper = canton.upper().strip()

    # Model progressive capital withdrawal tax: roughly 4% to 12% depending on chunk size
    def _tax_for_chunk(chunk: float) -> float:
        if chunk <= 50000:
            rate = 0.045
        elif chunk <= 100000:
            rate = 0.058
        elif chunk <= 200000:
            rate = 0.075
        elif chunk <= 500000:
            rate = 0.098
        else:
            rate = 0.125
        # Cantonal factor adjustment
        cfg = swiss_tax_math.CANTON_26_CONFIG.get(canton_upper, {"canton_factor": 1.2})
        factor = cfg.get("canton_factor", 1.2)
        return chunk * rate * (factor / 1.2)

    # 1-year withdrawal tax
    tax_1yr = _tax_for_chunk(total_capital_chf)

    # Staggered withdrawal across N years
    chunk_size = total_capital_chf / max(1, years)
    tax_staggered = _tax_for_chunk(chunk_size) * years
    tax_saved = max(0.0, tax_1yr - tax_staggered)

    return {
        "status": "SUCCESS",
        "canton": canton_upper,
        "total_capital_chf": total_capital_chf,
        "withdrawal_years": years,
        "lump_sum_tax_chf": round(tax_1yr, 2),
        "staggered_total_tax_chf": round(tax_staggered, 2),
        "tax_saved_chf": round(tax_saved, 2),
        "summary_zh": (
            f"一次性提取 CHF {total_capital_chf:,.0f} 养老金将缴纳清算税 CHF {tax_1yr:,.0f}。"
            f"若分拆为 {years} 年分批提取（每年 CHF {chunk_size:,.0f}），"
            f"总税金降至 CHF {tax_staggered:,.0f}，直接破除累进税率、节省 CHF {tax_saved:,.0f}！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="What-If tax scenario simulator for Swiss Tax Advisor")
    sub = parser.add_subparsers(dest="scenario")

    p_marr = sub.add_parser("marriage", help="Simulate Marriage penalty/bonus")
    p_marr.add_argument("--income1", type=float, required=True)
    p_marr.add_argument("--income2", type=float, required=True)
    p_marr.add_argument("--canton", type=str, default="ZH")
    p_marr.add_argument("--commune", type=str, default="Capital")
    p_marr.add_argument("--church-tax", action="store_true")

    p_child = sub.add_parser("child", help="Simulate having children and Kita costs")
    p_child.add_argument("--children", type=int, default=1)
    p_child.add_argument("--kita", type=float, default=0.0)
    p_child.add_argument("year", nargs="?", type=int)

    p_reloc = sub.add_parser("relocation", help="Simulate moving to another canton/commune")
    p_reloc.add_argument("--canton", type=str, required=True)
    p_reloc.add_argument("--commune", type=str, default="Capital")
    p_reloc.add_argument("year", nargs="?", type=int)

    p_cap = sub.add_parser("capital-withdrawal", help="Simulate 2nd/3rd pillar lump-sum vs staggered payout")
    p_cap.add_argument("--amount", type=float, required=True)
    p_cap.add_argument("--canton", type=str, default="BE")
    p_cap.add_argument("--years", type=int, default=3)

    args = parser.parse_args()

    if args.scenario == "marriage":
        res = simulate_marriage(args.income1, args.income2, args.canton, args.commune, args.church_tax)
    elif args.scenario == "child":
        res = simulate_child(args.children, args.kita, args.year)
    elif args.scenario == "relocation":
        res = simulate_relocation(args.canton, args.commune, args.year)
    elif args.scenario == "capital-withdrawal":
        res = simulate_capital_withdrawal(args.amount, args.canton, args.years)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
