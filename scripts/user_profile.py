#!/usr/bin/env python3
"""
user_profile.py — LLM-facing utility for reading, writing, and validating
the user's local profile and tax-year data under ./user/

Usage (called by the AI agent, never by the user directly):
  python3 scripts/user_profile.py status
  python3 scripts/user_profile.py get profile
  python3 scripts/user_profile.py get tax 2025
  python3 scripts/user_profile.py set profile '{"personal": {"name": "Max"}}'
  python3 scripts/user_profile.py set tax 2025 '{"income": {"gross_chf": 95000}}'
  python3 scripts/user_profile.py missing profile
  python3 scripts/user_profile.py missing tax 2025
  python3 scripts/user_profile.py save-report 2025 steuerdossier "# Steuerdossier..."
"""

import sys
import json
import os
import argparse
from datetime import date
from typing import Any, Dict, List, Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(SCRIPT_DIR)
USER_DIR   = os.path.join(ROOT_DIR, "user")
REPORTS_DIR = os.path.join(USER_DIR, "reports")

PROFILE_PATH = os.path.join(USER_DIR, "profile.json")

def tax_data_path(year: int) -> str:
    return os.path.join(USER_DIR, f"tax_{year}.json")

def report_dir(year: int) -> str:
    return os.path.join(REPORTS_DIR, str(year))

# ── Default schemas ────────────────────────────────────────────────────────────
def default_profile() -> Dict[str, Any]:
    return {
        "_version": "1.0",
        "_created": str(date.today()),
        "_updated": str(date.today()),
        "personal": {
            "name": None,
            "birth_year": None,
            "ahv_masked": None,
            "permit_type": None,   # CITIZEN / C / B / L
            "language": "EN"       # DE / FR / IT / EN / ZH
        },
        "address": {
            "canton": None,
            "commune": None,
            "zip": None
        },
        "civil_status": {
            "status": None,        # SINGLE / MARRIED / REGISTERED_PARTNER
            "partner_income_chf": None,
            "children_count": None,
            "children_ages": []
        },
        "employment": {
            "type": "EMPLOYED",    # EMPLOYED / SELF_EMPLOYED / MIXED
            "employer": None,
            "has_second_job": False
        },
        "recurring": {
            "commute_type": None,  # GA / HTA / CAR / WALK_BIKE
            "commute_km_one_way": None,
            "lunch_type": None,    # CANTEEN / SELF / RESTAURANT
            "health_franchise_chf": None,  # 300/500/1000/1500/2000/2500
            "church_member": False,
            "pillar_3a_institution": None,
            "pillar_3a_max_auto": True
        },
        "onboarding_complete": False,
        "onboarding_missing_fields": []
    }

def default_tax_data(year: int) -> Dict[str, Any]:
    return {
        "_version": "1.0",
        "tax_year": year,
        "_updated": str(date.today()),
        "income": {
            "gross_chf": None,
            "lohnausweis_box1_gross": None,
            "lohnausweis_box9_pillar2_contributions": None,
            "lohnausweis_box15_expense_reimbursement": None,
            "second_job_income_chf": 0
        },
        "deductions": {
            "s1_commute_chf": None,
            "s2_meals_chf": None,
            "s4_pillar3a_chf": None,
            "s6_kita_chf": 0,
            "s7_education_chf": 0,
            "insurance_premiums_chf": None,
            "annual_medical_spend_chf": None
        },
        "assets": {
            "net_wealth_chf": 0
        },
        "completeness_pct": 0,
        "missing_fields": []
    }

# ── Required fields for completeness check ─────────────────────────────────────
PROFILE_REQUIRED = [
    "address.canton",
    "address.commune",
    "civil_status.status",
    "civil_status.children_count",
    "personal.permit_type",
    "employment.type",
    "recurring.commute_type",
    "recurring.lunch_type",
    "recurring.health_franchise_chf",
]

TAX_REQUIRED = [
    "income.gross_chf",
    "deductions.s1_commute_chf",
    "deductions.s2_meals_chf",
    "deductions.s4_pillar3a_chf",
    "deductions.insurance_premiums_chf",
    "deductions.annual_medical_spend_chf",
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def _ensure_user_dir():
    os.makedirs(USER_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    # Create .gitignore in user/ to protect privacy
    gi = os.path.join(USER_DIR, ".gitignore")
    if not os.path.exists(gi):
        with open(gi, "w") as f:
            f.write("*.json\nreports/\n!.gitignore\n!README.md\n!profile.example.json\n")

def _get_nested(d: Dict, dotted_key: str) -> Any:
    keys = dotted_key.split(".")
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur

def _set_nested(d: Dict, dotted_key: str, value: Any):
    keys = dotted_key.split(".")
    cur = d
    for k in keys[:-1]:
        if k not in cur or not isinstance(cur[k], dict):
            cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = value

def _completeness(data: Dict, required_fields: List[str]) -> tuple:
    missing = []
    for f in required_fields:
        val = _get_nested(data, f)
        if val is None:
            missing.append(f)
    pct = int(100 * (len(required_fields) - len(missing)) / len(required_fields))
    return pct, missing

def _load_json(path: str, default_fn) -> Dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_fn()

def _save_json(path: str, data: Dict):
    _ensure_user_dir()
    data["_updated"] = str(date.today())
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Commands ───────────────────────────────────────────────────────────────────
def cmd_status() -> Dict:
    _ensure_user_dir()
    profile_exists = os.path.exists(PROFILE_PATH)
    profile = _load_json(PROFILE_PATH, default_profile) if profile_exists else default_profile()
    profile_pct, profile_missing = _completeness(profile, PROFILE_REQUIRED)

    current_year = date.today().year
    tax_path = tax_data_path(current_year)
    tax_exists = os.path.exists(tax_path)
    tax = _load_json(tax_path, lambda: default_tax_data(current_year)) if tax_exists else default_tax_data(current_year)
    tax_pct, tax_missing = _completeness(tax, TAX_REQUIRED)

    return {
        "profile": {
            "exists": profile_exists,
            "onboarding_complete": profile.get("onboarding_complete", False),
            "completeness_pct": profile_pct,
            "missing_fields": profile_missing,
            "canton": _get_nested(profile, "address.canton"),
            "civil_status": _get_nested(profile, "civil_status.status"),
            "language": _get_nested(profile, "personal.language"),
        },
        "tax_data": {
            "year": current_year,
            "exists": tax_exists,
            "completeness_pct": tax_pct,
            "missing_fields": tax_missing,
            "gross_income_chf": _get_nested(tax, "income.gross_chf"),
        },
        "next_action": _next_action(profile, profile_missing, tax, tax_missing)
    }

def _next_action(profile, profile_missing, tax, tax_missing) -> str:
    if not profile.get("onboarding_complete"):
        if profile_missing:
            return f"ONBOARDING_INCOMPLETE — ask user about: {profile_missing[0]}"
        return "ONBOARDING_MARK_COMPLETE"
    if tax_missing:
        return f"TAX_DATA_INCOMPLETE — ask user about: {tax_missing[0]}"
    return "READY_TO_CALCULATE"

def cmd_get(resource: str, year: Optional[int] = None) -> Dict:
    _ensure_user_dir()
    if resource == "profile":
        return _load_json(PROFILE_PATH, default_profile)
    elif resource == "tax":
        y = year or date.today().year
        return _load_json(tax_data_path(y), lambda: default_tax_data(y))
    else:
        return {"error": f"Unknown resource: {resource}"}

def cmd_set(resource: str, patch: Dict, year: Optional[int] = None) -> Dict:
    _ensure_user_dir()
    if resource == "profile":
        data = _load_json(PROFILE_PATH, default_profile)
        # Deep-merge patch
        def deep_merge(base, update):
            for k, v in update.items():
                if isinstance(v, dict) and isinstance(base.get(k), dict):
                    deep_merge(base[k], v)
                else:
                    base[k] = v
        deep_merge(data, patch)
        # Recompute completeness
        _, missing = _completeness(data, PROFILE_REQUIRED)
        data["onboarding_missing_fields"] = missing
        if not missing:
            data["onboarding_complete"] = True
        _save_json(PROFILE_PATH, data)
        return {"status": "saved", "onboarding_complete": data["onboarding_complete"], "missing": missing}
    elif resource == "tax":
        y = year or date.today().year
        path = tax_data_path(y)
        data = _load_json(path, lambda: default_tax_data(y))
        def deep_merge(base, update):
            for k, v in update.items():
                if isinstance(v, dict) and isinstance(base.get(k), dict):
                    deep_merge(base[k], v)
                else:
                    base[k] = v
        deep_merge(data, patch)
        pct, missing = _completeness(data, TAX_REQUIRED)
        data["completeness_pct"] = pct
        data["missing_fields"] = missing
        _save_json(path, data)
        return {"status": "saved", "completeness_pct": pct, "missing_fields": missing}
    return {"error": f"Unknown resource: {resource}"}

def cmd_missing(resource: str, year: Optional[int] = None) -> Dict:
    if resource == "profile":
        data = _load_json(PROFILE_PATH, default_profile)
        pct, missing = _completeness(data, PROFILE_REQUIRED)
        return {"completeness_pct": pct, "missing_fields": missing}
    elif resource == "tax":
        y = year or date.today().year
        data = _load_json(tax_data_path(y), lambda: default_tax_data(y))
        pct, missing = _completeness(data, TAX_REQUIRED)
        return {"completeness_pct": pct, "missing_fields": missing}
    return {"error": f"Unknown resource: {resource}"}

def cmd_save_report(year: int, report_type: str, content: str) -> Dict:
    _ensure_user_dir()
    rdir = report_dir(year)
    os.makedirs(rdir, exist_ok=True)
    ext = "txt" if report_type == "fristerstreckung" else "md"
    filename = f"{report_type}_{year}.{ext}"
    path = os.path.join(rdir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"status": "saved", "path": path}

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="LLM-facing user profile utility for Swiss Tax Advisor")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status", help="Check profile and tax-data completeness")

    p_get = sub.add_parser("get", help="Read profile or tax data")
    p_get.add_argument("resource", choices=["profile", "tax"])
    p_get.add_argument("year", nargs="?", type=int)

    p_set = sub.add_parser("set", help="Write/merge into profile or tax data")
    p_set.add_argument("resource", choices=["profile", "tax"])
    p_set.add_argument("year_or_json")
    p_set.add_argument("json_data", nargs="?")

    p_miss = sub.add_parser("missing", help="List missing required fields")
    p_miss.add_argument("resource", choices=["profile", "tax"])
    p_miss.add_argument("year", nargs="?", type=int)

    p_rep = sub.add_parser("save-report", help="Save a generated report to user/reports/")
    p_rep.add_argument("year", type=int)
    p_rep.add_argument("report_type")
    p_rep.add_argument("content")

    args = parser.parse_args()

    if args.cmd == "status":
        result = cmd_status()
    elif args.cmd == "get":
        result = cmd_get(args.resource, args.year)
    elif args.cmd == "set":
        # Handle both: set profile '{...}' and set tax 2025 '{...}'
        if args.resource == "tax" and args.json_data:
            year = int(args.year_or_json)
            patch = json.loads(args.json_data)
            result = cmd_set("tax", patch, year)
        else:
            patch = json.loads(args.year_or_json)
            result = cmd_set(args.resource, patch)
    elif args.cmd == "missing":
        result = cmd_missing(args.resource, args.year)
    elif args.cmd == "save-report":
        result = cmd_save_report(args.year, args.report_type, args.content)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
