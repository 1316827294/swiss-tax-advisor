#!/usr/bin/env python3
"""
parse_documents.py — LLM-facing document ingestion tool for Swiss Tax Advisor.

Scans ./documents/ for Lohnausweis (salary certs), Pillar 3a statements,
bank balance sheets (Saldoausweis), and health insurance summaries.
Extracts official Swiss tax figures and auto-persists them into ./user/tax_YYYY.json.

Usage (invoked silently by the AI agent):
  python3 scripts/parse_documents.py scan [year]
  python3 scripts/parse_documents.py parse-file <path_to_file> [year]
"""

import sys
import os
import re
import json
import subprocess
import argparse
from datetime import date
from typing import Dict, Any, List, Optional, Tuple

# ── Dynamic Root & Paths ──────────────────────────────────────────────────────
def find_project_root() -> str:
    cur = os.path.dirname(os.path.abspath(__file__))
    while cur and cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "SKILL.md")) or os.path.exists(os.path.join(cur, "scripts")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = find_project_root()
DOCS_DIR = os.path.join(ROOT_DIR, "documents")

# Add scripts to path to call user_profile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import user_profile
except ImportError:
    user_profile = None

# ── Document Extractors ────────────────────────────────────────────────────────
def extract_text_from_file(file_path: str) -> str:
    """Extract raw text from PDF, TXT, MD, or CSV."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        # 1. Try pdftotext CLI (fast, reliable layout)
        try:
            res = subprocess.run(
                ["pdftotext", "-layout", file_path, "-"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout
        except Exception:
            pass

        # 2. Try python pypdf if installed
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            if text.strip():
                return text
        except Exception:
            pass

        return ""
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""

def _clean_chf(val_str: str) -> Optional[float]:
    """Parse Swiss CHF numbers, e.g. 110'000.00, 110’000, 110000.50, 7`258."""
    if not val_str:
        return None
    s = val_str.replace("'", "").replace("’", "").replace("`", "").replace(" ", "").strip()
    try:
        return float(s)
    except ValueError:
        return None

# ── Swiss Document Parsers ────────────────────────────────────────────────────
def parse_lohnausweis(text: str) -> Dict[str, Any]:
    """
    Parses Swiss Lohnausweis (Salary Certificate / Certificat de salaire).
    Matches official Box numbers (Ziffer 1, Ziffer 9, Ziffer 11, Ziffer 13, Ziffer 15).
    """
    data = {}
    
    # 1. Box 1: Lohn / Bruttolohn / Salaire brut
    # e.g., "1. Lohn / Salaire: 125'000.00 CHF" or "Ziffer 1: 110000"
    m_gross = re.search(r'(?:1\.|Ziffer\s*1|Ziff\.\s*1|Bruttolohn|Salaire\s*brut)[^\d\n\r]{0,35}?([0-9][0-9\'’`\s]{2,12}(?:\.[0-9]{2})?)', text, re.IGNORECASE)
    if m_gross:
        val = _clean_chf(m_gross.group(1))
        if val and val > 10000:
            data["gross_income_chf"] = val

    # 2. Box 9: Beiträge BVG / 2. Säule
    m_bvg = re.search(r'(?:9\.|Ziffer\s*9|Beitr(?:ä|ae)ge\s*BVG|Cotisations\s*LPP|2\.\s*S(?:ä|ae)ule)[^\d\n\r]{0,35}?([0-9][0-9\'’`\s]{2,10}(?:\.[0-9]{2})?)', text, re.IGNORECASE)
    if m_bvg:
        val = _clean_chf(m_bvg.group(1))
        if val:
            data["pillar2_bvg_chf"] = val

    # 3. Box 13.1 / G: Canteen (Kantine / Repas à la cantine)
    if re.search(r'(?:13\.1|13\s*G|Kantine|canteen|repas\s*de\s*midi|Verbilligte\s*Verpflegung)', text, re.IGNORECASE):
        data["canteen_subsidized"] = True

    # 4. Box 13.2 / 15: Generalabonnement / GA / Firmenwagen
    if re.search(r'(?:Generalabonnement|SBB\s*GA|Gesch(?:ä|ae)ftsauto|voiture\s*de\s*service)', text, re.IGNORECASE):
        if "GA" in text or "Generalabonnement" in text:
            data["employer_provided_ga"] = True
        if "Geschäftsauto" in text or "Firmenwagen" in text:
            data["company_car"] = True

    # 5. Employer Name detection
    m_emp = re.search(r'(?:Arbeitgeber|Employeur|Employer)[\s\:\.]+([^\n\r]{3,40})', text, re.IGNORECASE)
    if m_emp:
        data["employer_name"] = m_emp.group(1).strip()

    return data

def parse_pillar_3a(text: str) -> Dict[str, Any]:
    """Parses Pillar 3a annual contribution statement (Bescheinigung Säule 3a)."""
    data = {}
    is_3a = bool(re.search(r'(?:S(?:ä|ae)ule\s*3a|Pillar\s*3a|3e\s*pilier\s*A|Vorsorgekonto\s*3a)', text, re.IGNORECASE))
    if not is_3a:
        return data

    # Look for contribution amount (e.g. 7'258 or 7056 or any amount)
    m_amt = re.search(r'(?:Einzahlung|Betrag|Contribution|Montant|Total)[\s\:\.A-Za-z]+([0-9\'’`\s]{3,8}(?:\.[0-9]{2})?)', text, re.IGNORECASE)
    if m_amt:
        val = _clean_chf(m_amt.group(1))
        if val and 100 <= val <= 36288:
            data["pillar3a_amount_chf"] = val
    elif "7'258" in text or "7258" in text:
        data["pillar3a_amount_chf"] = 7258.0

    return data

def parse_bank_statement(text: str) -> Dict[str, Any]:
    """Parses Bank Zins- und Saldoausweis per 31.12."""
    data = {}
    is_bank = bool(re.search(r'(?:Zins-\s*und\s*Saldoausweis|Steuerausweis|Relev(?:é|e)\s*fiscal|Saldo\s*per\s*31|UBS|Credit\s*Suisse|PostFinance|Raiffeisen|ZKB|Kantonalbank)', text, re.IGNORECASE))
    if not is_bank:
        return data

    m_bal = re.search(r'(?:Saldo\s*per\s*31\.12|Schlusssaldo|Guthaben\s*per\s*31|Solde\s*au\s*31\.12)[\s\:\.A-Za-z]+([0-9\'’`\s]{2,12}(?:\.[0-9]{2})?)', text, re.IGNORECASE)
    if m_bal:
        val = _clean_chf(m_bal.group(1))
        if val is not None:
            data["bank_balance_31dec_chf"] = val

    return data

# ── Master Scanner ─────────────────────────────────────────────────────────────
def scan_documents_folder(target_year: int) -> Dict[str, Any]:
    """Scans ./documents/ and auto-fills user tax profile."""
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR, exist_ok=True)
        return {
            "documents_found": 0,
            "message": "No documents folder found. Created ./documents/."
        }

    files = [f for f in os.listdir(DOCS_DIR) if not f.startswith(".") and f != "README.md"]
    if not files:
        return {
            "documents_found": 0,
            "message": "No tax files placed in ./documents/ yet."
        }

    extracted_summary = {
        "gross_income_chf": None,
        "pillar3a_chf": None,
        "canteen_subsidized": None,
        "bank_balance_chf": None,
        "employer_name": None,
        "employer_provided_ga": False,
        "company_car": False
    }

    processed_files = []

    for fname in files:
        fpath = os.path.join(DOCS_DIR, fname)
        if not os.path.isfile(fpath):
            continue

        raw_text = extract_text_from_file(fpath)
        if not raw_text.strip():
            continue

        file_findings = []

        # 1. Check Lohnausweis
        lw = parse_lohnausweis(raw_text)
        if lw:
            if "gross_income_chf" in lw and not extracted_summary["gross_income_chf"]:
                extracted_summary["gross_income_chf"] = lw["gross_income_chf"]
                file_findings.append(f"Bruttolohn (Gross): CHF {lw['gross_income_chf']:,.2f}")
            if "canteen_subsidized" in lw:
                extracted_summary["canteen_subsidized"] = True
                file_findings.append("Canteen subsidy detected (Kantine)")
            if lw.get("employer_provided_ga"):
                extracted_summary["employer_provided_ga"] = True
                file_findings.append("GA transit benefit detected in Box 13/15")
            if "employer_name" in lw and not extracted_summary["employer_name"]:
                extracted_summary["employer_name"] = lw["employer_name"]

        # 2. Check 3a
        p3a = parse_pillar_3a(raw_text)
        if p3a and "pillar3a_amount_chf" in p3a and not extracted_summary["pillar3a_chf"]:
            extracted_summary["pillar3a_chf"] = p3a["pillar3a_amount_chf"]
            file_findings.append(f"Pillar 3a: CHF {p3a['pillar3a_amount_chf']:,.2f}")

        # 3. Check Bank Saldo
        bs = parse_bank_statement(raw_text)
        if bs and "bank_balance_31dec_chf" in bs and extracted_summary["bank_balance_chf"] is None:
            extracted_summary["bank_balance_chf"] = bs["bank_balance_31dec_chf"]
            file_findings.append(f"Bank balance 31.12: CHF {bs['bank_balance_31dec_chf']:,.2f}")

        if file_findings:
            processed_files.append({
                "filename": fname,
                "identified_items": file_findings
            })

    # Auto-persist into ./user/tax_{target_year}.json via user_profile module
    auto_filled_patch = {"income": {}, "deductions": {}, "wealth": {}}
    if extracted_summary["gross_income_chf"]:
        auto_filled_patch["income"]["gross_chf"] = extracted_summary["gross_income_chf"]
    if extracted_summary["pillar3a_chf"]:
        auto_filled_patch["deductions"]["s4_pillar3a_chf"] = extracted_summary["pillar3a_chf"]
    if extracted_summary["canteen_subsidized"]:
        auto_filled_patch["deductions"]["s2_meals_chf"] = 1600.0
    if extracted_summary["bank_balance_chf"] is not None:
        auto_filled_patch["wealth"]["bank_balance_31dec_chf"] = extracted_summary["bank_balance_chf"]

    persisted = False
    if user_profile and any(auto_filled_patch.values()):
        user_profile.cmd_set("tax", auto_filled_patch, target_year)
        persisted = True

    return {
        "status": "SUCCESS",
        "documents_found": len(files),
        "processed_files": processed_files,
        "extracted_summary": extracted_summary,
        "auto_persisted_to_tax_data": persisted,
        "suggested_greeting_zh": _generate_greeting_zh(extracted_summary, processed_files),
        "suggested_greeting_en": _generate_greeting_en(extracted_summary, processed_files)
    }

def _generate_greeting_zh(ext: Dict[str, Any], files: List[Dict]) -> str:
    if not files:
        return "未能从 ./documents/ 的文件中提取到明确的税单数据，请直接通过对话告知我。"
    lines = ["🎉 已为您自动读取并解析 `./documents/` 中的税务凭证："]
    if ext.get("gross_income_chf"):
        lines.append(f"• **工资单税前收入 (Box 1)**: CHF {ext['gross_income_chf']:,.2f}")
    if ext.get("canteen_subsidized"):
        lines.append("• **食堂餐补 (Box 13G)**: 已自动对应 S2 伙食定额 CHF 1,600")
    if ext.get("pillar3a_chf"):
        lines.append(f"• **第三支柱 (Pillar 3a)**: CHF {ext['pillar3a_chf']:,.2f}")
    if ext.get("bank_balance_chf") is not None:
        lines.append(f"• **12月31日银行总余额**: CHF {ext['bank_balance_chf']:,.2f}")
    lines.append("\n上述数据已自动填入您的纳税档案中！接下来我们只需要确认少量补充信息即可完成全套申报。")
    return "\n".join(lines)

def _generate_greeting_en(ext: Dict[str, Any], files: List[Dict]) -> str:
    if not files:
        return "No tax data could be automatically extracted from ./documents/."
    lines = ["🎉 Automatically parsed your tax documents from `./documents/`:"]
    if ext.get("gross_income_chf"):
        lines.append(f"• Gross income (Lohnausweis Box 1): CHF {ext['gross_income_chf']:,.2f}")
    if ext.get("pillar3a_chf"):
        lines.append(f"• Pillar 3a contribution: CHF {ext['pillar3a_chf']:,.2f}")
    if ext.get("bank_balance_chf") is not None:
        lines.append(f"• Bank balance as of Dec 31: CHF {ext['bank_balance_chf']:,.2f}")
    lines.append("\nAll extracted values have been saved to your local tax file!")
    return "\n".join(lines)

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="LLM document ingestion parser for Swiss Tax Advisor")
    sub = parser.add_subparsers(dest="cmd")

    p_scan = sub.add_parser("scan", help="Scan ./documents/ and auto-fill tax profile")
    p_scan.add_argument("year", nargs="?", type=int, default=date.today().year)

    p_parse = sub.add_parser("parse-file", help="Parse a specific file")
    p_parse.add_argument("file_path")
    p_parse.add_argument("year", nargs="?", type=int, default=date.today().year)

    args = parser.parse_args()

    if args.cmd == "scan":
        res = scan_documents_folder(args.year)
    elif args.cmd == "parse-file":
        txt = extract_text_from_file(args.file_path)
        res = {
            "lohnausweis": parse_lohnausweis(txt),
            "pillar3a": parse_pillar_3a(txt),
            "bank_statement": parse_bank_statement(txt)
        }
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
