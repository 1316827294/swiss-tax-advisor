#!/usr/bin/env python3
"""
Swiss Tax Math Engine (Standard Library Python 3.10+)
Deterministic, 5-Rappen precision calculations for Federal Direct Tax (IFD / DBG),
Cantonal Tax, Communal Tax, and Wealth Tax across Swiss cantons.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

# Statutory caps and default tax rates for Switzerland (2025/2026)
STATUTORY_LIMITS_RAPPEN = {
    "PILLAR_3A_EMPLOYED": 725800,      # 7,258.00 CHF
    "PILLAR_3A_SELF_EMPLOYED": 3628800,# 36,288.00 CHF
    "COMMUTE_FEDERAL_MAX": 330000,     # 3,300.00 CHF
    "COMMUTE_BERN_MAX": 700000,        # 7,000.00 CHF
    "MEALS_STANDARD": 320000,          # 3,200.00 CHF
    "MEALS_SUBSIDIZED": 160000,        # 1,600.00 CHF
    "EDUCATION_MAX": 1270000,          # 12,700.00 CHF
    "CHILDCARE_FEDERAL_MAX": 2550000,  # 25,500.00 CHF
    "CHILD_DEDUCTION_FEDERAL": 670000, # 6,700.00 CHF per child
    "DUAL_EARNER_MIN": 860000,         # 8,600.00 CHF
    "DUAL_EARNER_MAX": 1410000,        # 14,100.00 CHF
}

# 26 Cantonal profiles: factors and statutory cantonal deduction limits
# Commute cap in CHF (None = no statutory limit / full actual expense deductible)
CANTON_26_CONFIG = {
    "ZH": {"name": "Zürich", "canton_factor": 1.00, "commune_factor": 1.19, "base_multiplier": 0.075, "commute_cap_chf": 5000.0, "childcare_cap_chf": 25000.0, "insurance_cap_single": 2600.0, "insurance_cap_married": 5200.0, "insurance_cap_child": 0.0},
    "BE": {"name": "Bern", "canton_factor": 3.06, "commune_factor": 1.54, "base_multiplier": 0.057, "commute_cap_chf": 7000.0, "childcare_cap_chf": 25500.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "LU": {"name": "Luzern", "canton_factor": 1.60, "commune_factor": 1.75, "base_multiplier": 0.052, "commute_cap_chf": 6000.0, "childcare_cap_chf": 12000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "UR": {"name": "Uri", "canton_factor": 1.00, "commune_factor": 1.00, "base_multiplier": 0.048, "commute_cap_chf": None, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "SZ": {"name": "Schwyz", "canton_factor": 1.20, "commune_factor": 1.10, "base_multiplier": 0.042, "commute_cap_chf": 6000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "OW": {"name": "Obwalden", "canton_factor": 1.00, "commune_factor": 1.15, "base_multiplier": 0.046, "commute_cap_chf": None, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "NW": {"name": "Nidwalden", "canton_factor": 1.00, "commune_factor": 1.10, "base_multiplier": 0.045, "commute_cap_chf": None, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "GL": {"name": "Glarus", "canton_factor": 1.07, "commune_factor": 1.15, "base_multiplier": 0.055, "commute_cap_chf": None, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "ZG": {"name": "Zug", "canton_factor": 0.82, "commune_factor": 0.60, "base_multiplier": 0.040, "commute_cap_chf": None, "childcare_cap_chf": 25000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "FR": {"name": "Fribourg", "canton_factor": 1.00, "commune_factor": 0.82, "base_multiplier": 0.076, "commute_cap_chf": 3300.0, "childcare_cap_chf": 12000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "SO": {"name": "Solothurn", "canton_factor": 1.04, "commune_factor": 1.18, "base_multiplier": 0.068, "commute_cap_chf": 7000.0, "childcare_cap_chf": 12000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "BS": {"name": "Basel-Stadt", "canton_factor": 1.00, "commune_factor": 0.50, "base_multiplier": 0.082, "commute_cap_chf": 3300.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2000.0, "insurance_cap_married": 4000.0, "insurance_cap_child": 0.0},
    "BL": {"name": "Basel-Landschaft", "canton_factor": 1.00, "commune_factor": 0.65, "base_multiplier": 0.078, "commute_cap_chf": None, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "SH": {"name": "Schaffhausen", "canton_factor": 1.08, "commune_factor": 1.00, "base_multiplier": 0.062, "commute_cap_chf": 6000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "AR": {"name": "Appenzell A.Rh.", "canton_factor": 1.15, "commune_factor": 1.30, "base_multiplier": 0.062, "commute_cap_chf": 6000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "AI": {"name": "Appenzell I.Rh.", "canton_factor": 1.00, "commune_factor": 0.95, "base_multiplier": 0.046, "commute_cap_chf": 6000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "SG": {"name": "St. Gallen", "canton_factor": 1.15, "commune_factor": 1.40, "base_multiplier": 0.065, "commute_cap_chf": 4460.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "GR": {"name": "Graubünden", "canton_factor": 1.00, "commune_factor": 0.90, "base_multiplier": 0.060, "commute_cap_chf": 5000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "AG": {"name": "Aargau", "canton_factor": 1.12, "commune_factor": 1.05, "base_multiplier": 0.065, "commute_cap_chf": 7000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "TG": {"name": "Thurgau", "canton_factor": 1.17, "commune_factor": 1.45, "base_multiplier": 0.058, "commute_cap_chf": 6000.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "TI": {"name": "Ticino", "canton_factor": 1.00, "commune_factor": 0.90, "base_multiplier": 0.070, "commute_cap_chf": 3300.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "VD": {"name": "Vaud", "canton_factor": 1.55, "commune_factor": 0.785, "base_multiplier": 0.068, "commute_cap_chf": 3300.0, "childcare_cap_chf": 15000.0, "insurance_cap_single": 3200.0, "insurance_cap_married": 6400.0, "insurance_cap_child": 0.0},
    "VS": {"name": "Valais", "canton_factor": 1.10, "commune_factor": 1.15, "base_multiplier": 0.065, "commute_cap_chf": 3300.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "NE": {"name": "Neuchâtel", "canton_factor": 1.25, "commune_factor": 1.20, "base_multiplier": 0.075, "commute_cap_chf": 3300.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
    "GE": {"name": "Genève", "canton_factor": 1.48, "commune_factor": 0.455, "base_multiplier": 0.078, "commute_cap_chf": 500.0, "childcare_cap_chf": 25000.0, "insurance_cap_single": 3000.0, "insurance_cap_married": 6000.0, "insurance_cap_child": 1000.0},
    "JU": {"name": "Jura", "canton_factor": 1.25, "commune_factor": 1.90, "base_multiplier": 0.065, "commute_cap_chf": 3300.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0},
}
CANTONAL_PROFILES = CANTON_26_CONFIG
DEFAULT_CANTON_PROFILE = {"name": "Other", "canton_factor": 1.20, "commune_factor": 1.20, "base_multiplier": 0.065, "commute_cap_chf": 3300.0, "childcare_cap_chf": 10000.0, "insurance_cap_single": 2400.0, "insurance_cap_married": 4800.0, "insurance_cap_child": 0.0}

def round_to_5_rappen(rappen: int) -> int:
    """Rounds an amount in Rappen (cents) to the nearest 5 Rappen (Swiss standard)."""
    return int(round(rappen / 5.0) * 5)

def chf_to_rappen(chf: float) -> int:
    """Converts CHF float to exact integer Rappen."""
    return int(round(chf * 100.0))

def rappen_to_chf(rappen: int) -> float:
    """Converts integer Rappen to CHF float rounded to 2 decimals."""
    return round(rappen / 100.0, 2)

def calculate_federal_direct_tax_rappen(taxable_income_rappen: int, civil_status: str, children_count: int = 0) -> int:
    """
    Computes Federal Direct Tax (IFD / DBG) using official progressive tariff tables.
    Tarif A: Single individuals
    Tarif B: Married couples / Registered partners
    """
    if taxable_income_rappen <= 0:
        return 0

    income_chf = taxable_income_rappen / 100.0

    # Child deduction for federal tax (6,700 CHF per child)
    child_rebate_rappen = children_count * STATUTORY_LIMITS_RAPPEN["CHILD_DEDUCTION_FEDERAL"]
    effective_income_rappen = max(0, taxable_income_rappen - child_rebate_rappen)
    effective_income_chf = effective_income_rappen / 100.0

    tax_chf = 0.0

    if civil_status.upper() in ["MARRIED", "REGISTERED_PARTNER"]:
        # Tarif B: Married couples / Verheiratet
        if effective_income_chf <= 30800:
            tax_chf = 0.0
        elif effective_income_chf <= 50900:
            tax_chf = (effective_income_chf - 30800) * 0.01
        elif effective_income_chf <= 58400:
            tax_chf = 201.0 + (effective_income_chf - 50900) * 0.02
        elif effective_income_chf <= 75300:
            tax_chf = 351.0 + (effective_income_chf - 58400) * 0.03
        elif effective_income_chf <= 90300:
            tax_chf = 858.0 + (effective_income_chf - 75300) * 0.04
        elif effective_income_chf <= 103400:
            tax_chf = 1458.0 + (effective_income_chf - 90300) * 0.05
        elif effective_income_chf <= 114700:
            tax_chf = 2113.0 + (effective_income_chf - 103400) * 0.06
        elif effective_income_chf <= 124200:
            tax_chf = 2791.0 + (effective_income_chf - 114700) * 0.07
        elif effective_income_chf <= 131700:
            tax_chf = 3456.0 + (effective_income_chf - 124200) * 0.08
        elif effective_income_chf <= 137300:
            tax_chf = 4056.0 + (effective_income_chf - 131700) * 0.09
        elif effective_income_chf <= 141200:
            tax_chf = 4560.0 + (effective_income_chf - 137300) * 0.10
        elif effective_income_chf <= 143100:
            tax_chf = 4950.0 + (effective_income_chf - 141200) * 0.11
        elif effective_income_chf <= 145000:
            tax_chf = 5159.0 + (effective_income_chf - 143100) * 0.12
        elif effective_income_chf <= 895900:
            tax_chf = 5387.0 + (effective_income_chf - 145000) * 0.13
        else:
            tax_chf = (effective_income_chf) * 0.115  # Max flat cap
    else:
        # Tarif A: Single individuals / Alleinstehend
        if effective_income_chf <= 14500:
            tax_chf = 0.0
        elif effective_income_chf <= 31600:
            tax_chf = (effective_income_chf - 14500) * 0.0077
        elif effective_income_chf <= 41400:
            tax_chf = 131.65 + (effective_income_chf - 31600) * 0.0088
        elif effective_income_chf <= 55200:
            tax_chf = 217.90 + (effective_income_chf - 41400) * 0.0264
        elif effective_income_chf <= 72500:
            tax_chf = 582.20 + (effective_income_chf - 55200) * 0.0297
        elif effective_income_chf <= 78100:
            tax_chf = 1096.0 + (effective_income_chf - 72500) * 0.0594
        elif effective_income_chf <= 103600:
            tax_chf = 1428.65 + (effective_income_chf - 78100) * 0.066
        elif effective_income_chf <= 134600:
            tax_chf = 3111.65 + (effective_income_chf - 103600) * 0.088
        elif effective_income_chf <= 176000:
            tax_chf = 5839.65 + (effective_income_chf - 134600) * 0.11
        elif effective_income_chf <= 755200:
            tax_chf = 10393.65 + (effective_income_chf - 176000) * 0.132
        else:
            tax_chf = (effective_income_chf) * 0.115  # Max cap

    return round_to_5_rappen(chf_to_rappen(max(0.0, tax_chf)))

def calculate_cantonal_communal_tax_rappen(
    taxable_income_rappen: int,
    canton: str,
    commune: Optional[str] = None,
    church_tax: str = "NONE"
) -> Dict[str, int]:
    """
    Computes Cantonal, Communal, and Church tax in Rappen.
    Uses base progressive progressive multiplier scaled by cantonal & communal Steuerfuss.
    """
    canton_key = canton.upper()
    profile = CANTONAL_PROFILES.get(canton_key, DEFAULT_CANTON_PROFILE)
    
    # Base tariff approximation (simple progressive scale on taxable income)
    taxable_chf = taxable_income_rappen / 100.0
    
    # Base progressive curve
    if taxable_chf <= 12000:
        base_tax_chf = 0.0
    elif taxable_chf <= 30000:
        base_tax_chf = (taxable_chf - 12000) * 0.025
    elif taxable_chf <= 60000:
        base_tax_chf = 450.0 + (taxable_chf - 30000) * 0.045
    elif taxable_chf <= 100000:
        base_tax_chf = 1800.0 + (taxable_chf - 60000) * 0.065
    elif taxable_chf <= 150000:
        base_tax_chf = 4400.0 + (taxable_chf - 100000) * 0.080
    else:
        base_tax_chf = 8400.0 + (taxable_chf - 150000) * 0.095

    # Scale with canton and commune multipliers
    canton_factor = profile["canton_factor"]
    commune_factor = profile["commune_factor"]

    cantonal_tax_rappen = round_to_5_rappen(chf_to_rappen(base_tax_chf * canton_factor))
    communal_tax_rappen = round_to_5_rappen(chf_to_rappen(base_tax_chf * commune_factor))
    
    church_tax_rappen = 0
    if church_tax.upper() in ["ROMAN_CATHOLIC", "PROTESTANT", "REFORMED"]:
        church_tax_rappen = round_to_5_rappen(int(cantonal_tax_rappen * 0.08))

    return {
        "cantonal_tax_rappen": cantonal_tax_rappen,
        "communal_tax_rappen": communal_tax_rappen,
        "church_tax_rappen": church_tax_rappen
    }

def calculate_wealth_tax_rappen(net_wealth_chf: float, canton: str) -> int:
    """Calculates Cantonal/Communal wealth tax on net assets above exemption threshold."""
    if net_wealth_chf <= 100000.0:  # Exemption allowance (Freibetrag)
        return 0
    taxable_wealth = net_wealth_chf - 100000.0
    # Average Swiss wealth tax is approx 1.5 - 3.5 per thousand (Promille)
    wealth_tax_chf = taxable_wealth * 0.0025
    return round_to_5_rappen(chf_to_rappen(wealth_tax_chf))

def calculate_swiss_tax(
    gross_income_chf: float,
    canton: str,
    commune: Optional[str] = "Capital",
    civil_status: str = "SINGLE",
    children_count: int = 0,
    church_tax: str = "NONE",
    deductions: Optional[Dict[str, float]] = None,
    net_wealth_chf: float = 0.0,
    insurance_premiums_chf: float = 0.0,
    higher_education_expenses_chf: float = 0.0,
    rent_expenses_chf: float = 0.0
) -> Dict[str, Any]:
    """
    Main entrypoint for Swiss tax calculation.
    All deduction codes (s1, s2, s3, s4, s6, s7, insurance, education, rent, etc.) are capped by statutory laws.
    """
    deductions = dict(deductions) if deductions else {}
    total_deductions_rappen = 0
    itemized_deductions = {}
    canton_upper = canton.upper()
    canton_cfg = CANTON_26_CONFIG.get(canton_upper, DEFAULT_CANTON_PROFILE)
    is_married = civil_status.upper() in ["MARRIED", "REGISTERED_PARTNER"]

    # Extract or fallback from deductions dict if not passed explicitly as arguments
    if insurance_premiums_chf == 0.0:
        for k in ["insurance_premiums", "insurance", "versicherungsabzug"]:
            if k in deductions:
                insurance_premiums_chf = float(deductions.pop(k))
                break

    if higher_education_expenses_chf == 0.0:
        for k in ["higher_education_expenses", "higher_education", "ausbildung_majeurs", "ausbildung"]:
            if k in deductions:
                higher_education_expenses_chf = float(deductions.pop(k))
                break

    if rent_expenses_chf == 0.0:
        for k in ["rent_expenses", "rent", "mietkosten_relief", "mietkosten"]:
            if k in deductions:
                rent_expenses_chf = float(deductions.pop(k))
                break

    for key, val in deductions.items():
        k = key.lower()
        val_rappen = chf_to_rappen(val)
        # Apply statutory caps
        if k in ["s1", "s1_fahrkosten", "commute"]:
            commute_cap = canton_cfg.get("commute_cap_chf")
            if commute_cap is not None:
                val_rappen = min(val_rappen, chf_to_rappen(commute_cap))
        elif k in ["s2", "s2_verpflegung", "meals"]:
            val_rappen = min(val_rappen, STATUTORY_LIMITS_RAPPEN["MEALS_STANDARD"])
        elif k in ["s4", "s4_saeule_3a", "pillar_3a"]:
            val_rappen = min(val_rappen, STATUTORY_LIMITS_RAPPEN["PILLAR_3A_EMPLOYED"])
        elif k in ["s6", "s6_kita", "childcare"]:
            childcare_cap = canton_cfg.get("childcare_cap_chf", 25500.0)
            val_rappen = min(val_rappen, chf_to_rappen(childcare_cap) * max(1, children_count))
        elif k in ["s7", "s7_weiterbildung", "education"]:
            val_rappen = min(val_rappen, STATUTORY_LIMITS_RAPPEN["EDUCATION_MAX"])
        elif k in ["behinderung", "disability"]:
            pass  # Zero threshold / 0% hurdle under DBG Art. 33 Abs. 1 Bst. hbis

        total_deductions_rappen += val_rappen
        itemized_deductions[key] = rappen_to_chf(val_rappen)

    # 1. Insurance Premium Deduction (Versicherungsabzug)
    if insurance_premiums_chf > 0.0:
        ins_claimed_rappen = chf_to_rappen(insurance_premiums_chf)
        ins_cap_chf = (
            canton_cfg.get("insurance_cap_married", 4800.0)
            if is_married
            else canton_cfg.get("insurance_cap_single", 2400.0)
        ) + (children_count * canton_cfg.get("insurance_cap_child", 0.0))
        ins_cap_rappen = chf_to_rappen(ins_cap_chf)

        if canton_upper == "GE":
            ins_allowable_rappen = ins_claimed_rappen
        else:
            ins_allowable_rappen = min(ins_claimed_rappen, ins_cap_rappen)

        total_deductions_rappen += ins_allowable_rappen
        itemized_deductions["insurance_premiums"] = rappen_to_chf(ins_allowable_rappen)

    # 2. Higher Education Deduction for Young Adults (Ausbildungskosten volljähriger Kinder)
    if higher_education_expenses_chf > 0.0:
        edu_claimed_rappen = chf_to_rappen(higher_education_expenses_chf)
        if canton_upper == "GE":
            edu_cap_rappen = 1300000  # CHF 13,000
        elif canton_upper == "VD":
            edu_cap_rappen = 740000   # CHF 7,400
        elif canton_upper == "NE":
            edu_cap_rappen = 600000   # CHF 6,000
        else:
            edu_cap_rappen = 0

        edu_allowable_rappen = min(edu_claimed_rappen, edu_cap_rappen)
        total_deductions_rappen += edu_allowable_rappen
        itemized_deductions["higher_education_expenses"] = rappen_to_chf(edu_allowable_rappen)

    gross_rappen = chf_to_rappen(gross_income_chf)

    # 3. Rent Relief Deduction (Mietkostenabzug)
    reineinkommen_rappen = max(0, gross_rappen - total_deductions_rappen)
    if rent_expenses_chf > 0.0:
        rent_claimed_rappen = chf_to_rappen(rent_expenses_chf)
        if canton_upper == "ZG" and reineinkommen_rappen <= 7500000:
            rent_cap_rappen = 500000  # CHF 5,000
        elif canton_upper == "VD" and reineinkommen_rappen <= 6000000:
            rent_cap_rappen = 400000  # CHF 4,000
        else:
            rent_cap_rappen = 0

        rent_allowable_rappen = min(rent_claimed_rappen, rent_cap_rappen)
        total_deductions_rappen += rent_allowable_rappen
        itemized_deductions["rent_expenses"] = rappen_to_chf(rent_allowable_rappen)

    taxable_rappen = max(0, gross_rappen - total_deductions_rappen)

    # 1. Federal Direct Tax
    fed_rappen = calculate_federal_direct_tax_rappen(taxable_rappen, civil_status, children_count)

    # 2. Cantonal and Communal Tax
    cantonal_res = calculate_cantonal_communal_tax_rappen(taxable_rappen, canton, commune, church_tax)
    cantonal_rappen = cantonal_res["cantonal_tax_rappen"]
    communal_rappen = cantonal_res["communal_tax_rappen"]
    church_rappen = cantonal_res["church_tax_rappen"]

    # 3. Wealth Tax
    wealth_rappen = calculate_wealth_tax_rappen(net_wealth_chf, canton)

    total_tax_rappen = fed_rappen + cantonal_rappen + communal_rappen + church_rappen + wealth_rappen
    effective_rate = (total_tax_rappen / gross_rappen * 100.0) if gross_rappen > 0 else 0.0

    return {
        "status": "success",
        "currency": "CHF",
        "canton": canton.upper(),
        "commune": commune,
        "civil_status": civil_status.upper(),
        "children_count": children_count,
        "gross_income_chf": rappen_to_chf(gross_rappen),
        "total_deductions_chf": rappen_to_chf(total_deductions_rappen),
        "taxable_income_chf": rappen_to_chf(taxable_rappen),
        "itemized_deductions_chf": itemized_deductions,
        "federal_tax_chf": rappen_to_chf(fed_rappen),
        "cantonal_tax_chf": rappen_to_chf(cantonal_rappen),
        "communal_tax_chf": rappen_to_chf(communal_rappen),
        "church_tax_chf": rappen_to_chf(church_rappen),
        "wealth_tax_chf": rappen_to_chf(wealth_rappen),
        "total_tax_chf": rappen_to_chf(total_tax_rappen),
        "effective_tax_rate_pct": round(effective_rate, 2),
    }

def main():
    parser = argparse.ArgumentParser(description="Deterministic Swiss Tax Math Engine")
    parser.add_argument("--gross-income", type=float, required=True, help="Gross annual income in CHF")
    parser.add_argument("--canton", type=str, default="BE", help="Two-letter Swiss canton code (e.g. BE, ZH, VD)")
    parser.add_argument("--commune", type=str, default="Capital", help="Municipality name")
    parser.add_argument("--civil-status", type=str, default="SINGLE", choices=["SINGLE", "MARRIED", "REGISTERED_PARTNER"])
    parser.add_argument("--children", type=int, default=0, help="Number of dependent minor children")
    parser.add_argument("--church-tax", type=str, default="NONE", help="Church tax status (NONE, ROMAN_CATHOLIC, PROTESTANT)")
    parser.add_argument("--deductions", type=str, default="{}", help="JSON string of deductions, e.g. '{\"s1\": 3300, \"s4\": 7258}'")
    parser.add_argument("--net-wealth", type=float, default=0.0, help="Net taxable wealth in CHF")
    parser.add_argument("--insurance-premiums", type=float, default=0.0, help="Claimed insurance premiums in CHF")
    parser.add_argument("--higher-education", type=float, default=0.0, help="Higher education expenses for young adults in CHF")
    parser.add_argument("--rent-expenses", type=float, default=0.0, help="Rent expenses for rent relief deduction in CHF")
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")

    args = parser.parse_args()
    try:
        ded_dict = json.loads(args.deductions)
    except Exception as e:
        sys.stderr.write(f"Invalid deductions JSON: {e}\n")
        sys.exit(1)

    result = calculate_swiss_tax(
        gross_income_chf=args.gross_income,
        canton=args.canton,
        commune=args.commune,
        civil_status=args.civil_status,
        children_count=args.children,
        church_tax=args.church_tax,
        deductions=ded_dict,
        net_wealth_chf=args.net_wealth,
        insurance_premiums_chf=args.insurance_premiums,
        higher_education_expenses_chf=args.higher_education,
        rent_expenses_chf=args.rent_expenses
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"--- Swiss Tax Assessment ({result['canton']} - {result['commune']}) ---")
        print(f"Gross Income:      CHF {result['gross_income_chf']:,.2f}")
        print(f"Total Deductions:  CHF {result['total_deductions_chf']:,.2f}")
        print(f"Taxable Income:    CHF {result['taxable_income_chf']:,.2f}")
        print(f"--------------------------------------------------")
        print(f"Federal Direct Tax:CHF {result['federal_tax_chf']:,.2f}")
        print(f"Cantonal Tax:      CHF {result['cantonal_tax_chf']:,.2f}")
        print(f"Communal Tax:      CHF {result['communal_tax_chf']:,.2f}")
        print(f"Total Tax Payable: CHF {result['total_tax_chf']:,.2f} ({result['effective_tax_rate_pct']}%)")

if __name__ == "__main__":
    main()
