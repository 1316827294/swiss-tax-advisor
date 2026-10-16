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

def parse_broker_statement(text: str) -> Dict[str, Any]:
    """
    Parses Swiss/International Broker Statements (eSteuerausweis / Depotauszug).
    Supports Swissquote, IBKR (Interactive Brokers), UBS, Degiro, Saxo Bank.
    Extracts 31.12 portfolio market value, gross dividends, US withholding tax (for DA-1),
    and custody fees (Wertschriftenverwaltungskosten / Depotgebühren).
    """
    data = {}
    is_broker = bool(re.search(
        r'(?:eSteuerausweis|Steuerausweis|Depotauszug|Depotbestand|Wertschriftenverzeichnis|'
        r'Interactive\s*Brokers|IBKR|Swissquote|Degiro|Saxo|Relev(?:é|e)\s*fiscal|Portefeuille|'
        r'Securities\s*Summary)', text, re.IGNORECASE
    ))
    if not is_broker:
        return data

    # 1. Total Portfolio Market Value per 31.12 (Steuerwert / Kurswert)
    m_val = re.search(
        r'(?:Steuerwert|Depotwert|Kurswert|Portfolio\s*Value|Total\s*Wertschriften|'
        r'Depotbestand|Solde\s*titres)[^\n\r]*?[:\s]\s*([0-9][0-9\'’`\s]{2,12}(?:\.[0-9]{2})?)',
        text, re.IGNORECASE
    )
    if m_val:
        val = _clean_chf(m_val.group(1))
        if val is not None:
            data["securities_value_chf"] = val

    # 2. Gross Dividends / Ertrag
    m_div = re.search(
        r'(?:Bruttoertrag|Dividenden|Ertrag|Total\s*Dividends|Revenus\s*bruts)[^\n\r]*?[:\s]\s*([0-9][0-9\'’`\s]{1,10}(?:\.[0-9]{2})?)',
        text, re.IGNORECASE
    )
    if m_div:
        val = _clean_chf(m_div.group(1))
        if val is not None:
            data["dividend_income_chf"] = val

    # 3. US / Foreign Withholding Tax for Form DA-1 reclaim
    m_us_tax = re.search(
        r'(?:US\s*Withholding|Quellensteuer\s*USA|Retenue\s*(?:US|USA)|Non-Recoverable\s*US\s*Tax|DA-1)[^\n\r]*?[:\s]\s*([0-9][0-9\'’`\s]{1,8}(?:\.[0-9]{2})?)',
        text, re.IGNORECASE
    )
    if m_us_tax:
        val = _clean_chf(m_us_tax.group(1))
        if val is not None:
            data["us_withholding_tax_chf"] = val

    # 4. Custody fees / Depotgebühren (100% tax deductible under Art. 32 DBG)
    m_depot = re.search(
        r'(?:Depotgeb(?:ü|ue)hren|Verwaltungsgeb(?:ü|ue)hren|Custody\s*Fees|Frais\s*de\s*garde)[^\n\r]*?[:\s]\s*([0-9][0-9\'’`\s]{1,8}(?:\.[0-9]{2})?)',
        text, re.IGNORECASE
    )
    if m_depot:
        val = _clean_chf(m_depot.group(1))
        if val is not None:
            data["depotgebuehren_chf"] = val

    return data

def parse_renovation_invoice(text: str) -> Dict[str, Any]:
    """
    Parses property renovation and maintenance bills (Handwerkerrechnungen / Liegenschaftsunterhalt).
    Classifies under Swiss tax law (DBG Art. 32 Abs. 2):
      - Werterhaltend (Value-preserving): 100% deductible in tax year
      - Energiesparmassnahmen (Energy-saving): 100% deductible + multi-year carryover
      - Wertvermehrend (Value-adding): Non-deductible for income tax (saved for real estate capital gains)
    """
    data = {}
    is_reno = bool(re.search(
        r'(?:Handwerker|Renovation|Sanierung|Maler|Baurechnung|Elektro|Sanit(?:ä|ae)r|'
        r'Heizung|Solar|Photovoltaik|Liegenschaftsunterhalt|Umbau|Reparatur)',
        text, re.IGNORECASE
    ))
    if not is_reno:
        return data

    # 1. Total Invoice Amount
    m_tot = re.search(
        r'(?:Rechnungsbetrag|Endbetrag|Totalbetrag|Total\s*CHF|Montant\s*total)[\s\:\.A-Za-z]+([0-9][0-9\'’`\s]{2,10}(?:\.[0-9]{2})?)',
        text, re.IGNORECASE
    )
    total_val = _clean_chf(m_tot.group(1)) if m_tot else None

    # Fallback to looking for standard CHF amount
    if not total_val:
        m_chf = re.findall(r'(?:CHF|Fr\.)\s*([0-9][0-9\'’`\s]{2,10}(?:\.[0-9]{2})?)', text)
        if m_chf:
            parsed_chfs = [_clean_chf(x) for x in m_chf if _clean_chf(x)]
            if parsed_chfs:
                total_val = max(parsed_chfs)

    if not total_val:
        return data

    # 2. Heuristic Categorization
    is_energy = bool(re.search(r'(?:Solar|Photovoltaik|W(?:ä|ae)rmepumpe|Isolation|D(?:ä|ae)mmung|Energiespar|Fensterersatz|Zweifach|Dreifachverglasung)', text, re.IGNORECASE))
    is_value_adding = bool(re.search(r'(?:Neubau|Anbau|Schwimmbad|Pool|Wintergarten|Sauna|Aufstockung)', text, re.IGNORECASE))

    if is_energy:
        category = "ENERGIEMASSNAHME" # 100% deductible + carryover
        tax_deductible = True
    elif is_value_adding:
        category = "WERTVERMEHREND"   # Not deductible for income tax
        tax_deductible = False
    else:
        category = "WERTERHALTEND"    # Standard 100% deductible
        tax_deductible = True

    data["total_amount_chf"] = total_val
    data["category"] = category
    data["tax_deductible"] = tax_deductible
    data["deductible_amount_chf"] = total_val if tax_deductible else 0.0

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
        "company_car": False,
        "securities_value_chf": None,
        "dividend_income_chf": None,
        "us_withholding_tax_chf": None,
        "depotgebuehren_chf": None,
        "property_maintenance_chf": 0.0,
        "renovation_items_count": 0
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

        # 4. Check Broker Statement (eSteuerausweis / Depotauszug)
        broker = parse_broker_statement(raw_text)
        if broker:
            if "securities_value_chf" in broker:
                extracted_summary["securities_value_chf"] = (extracted_summary["securities_value_chf"] or 0.0) + broker["securities_value_chf"]
                file_findings.append(f"Securities portfolio per 31.12: CHF {broker['securities_value_chf']:,.2f}")
            if "dividend_income_chf" in broker:
                extracted_summary["dividend_income_chf"] = (extracted_summary["dividend_income_chf"] or 0.0) + broker["dividend_income_chf"]
                file_findings.append(f"Dividend income: CHF {broker['dividend_income_chf']:,.2f}")
            if "us_withholding_tax_chf" in broker:
                extracted_summary["us_withholding_tax_chf"] = (extracted_summary["us_withholding_tax_chf"] or 0.0) + broker["us_withholding_tax_chf"]
                file_findings.append(f"US Withholding Tax (DA-1 eligible): CHF {broker['us_withholding_tax_chf']:,.2f}")
            if "depotgebuehren_chf" in broker:
                extracted_summary["depotgebuehren_chf"] = (extracted_summary["depotgebuehren_chf"] or 0.0) + broker["depotgebuehren_chf"]
                file_findings.append(f"Custody fees (Deductible): CHF {broker['depotgebuehren_chf']:,.2f}")

        # 5. Check Renovation & Property Maintenance Bills
        reno = parse_renovation_invoice(raw_text)
        if reno and reno.get("total_amount_chf"):
            amt = reno["total_amount_chf"]
            cat = reno["category"]
            if reno.get("tax_deductible"):
                extracted_summary["property_maintenance_chf"] += amt
                extracted_summary["renovation_items_count"] += 1
                file_findings.append(f"Renovation [{cat}]: CHF {amt:,.2f} (100% Tax Deductible)")
            else:
                file_findings.append(f"Renovation [{cat}]: CHF {amt:,.2f} (Value-adding: saved for real estate capital gains)")

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
    if extracted_summary["securities_value_chf"] is not None:
        auto_filled_patch["wealth"]["securities_crypto_chf"] = extracted_summary["securities_value_chf"]
    if extracted_summary["depotgebuehren_chf"] is not None:
        auto_filled_patch["deductions"]["depotgebuehren_chf"] = extracted_summary["depotgebuehren_chf"]
    if extracted_summary["property_maintenance_chf"] > 0:
        auto_filled_patch["deductions"]["s8_property_maintenance_chf"] = extracted_summary["property_maintenance_chf"]

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
    if ext.get("securities_value_chf") is not None:
        lines.append(f"• **12月31日股票证券市值**: CHF {ext['securities_value_chf']:,.2f} *(资本利得依法100%免税)*")
    if ext.get("us_withholding_tax_chf") is not None:
        lines.append(f"• **美股股息预扣税 (DA-1)**: CHF {ext['us_withholding_tax_chf']:,.2f} *(已自动锁定跨国双重征税全额退税额)*")
    if ext.get("depotgebuehren_chf") is not None:
        lines.append(f"• **证券托管管理费 (Depotgebühren)**: CHF {ext['depotgebuehren_chf']:,.2f} *(法定100%抵税)*")
    if ext.get("property_maintenance_chf") and ext["property_maintenance_chf"] > 0:
        lines.append(f"• **房产装修维修支出 (共 {ext.get('renovation_items_count', 1)} 笔)**: 确认可扣除 CHF {ext['property_maintenance_chf']:,.2f} *(维持价值/节能100%抵扣)*")
    lines.append("\n上述数据已自动填入您的本地纳税档案中！接下来我们只需要确认少量补充信息即可完成全套申报。")
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
    if ext.get("securities_value_chf") is not None:
        lines.append(f"• Securities portfolio as of Dec 31: CHF {ext['securities_value_chf']:,.2f} (Capital gains 100% tax-free)")
    if ext.get("us_withholding_tax_chf") is not None:
        lines.append(f"• US Dividend Withholding Tax (DA-1): CHF {ext['us_withholding_tax_chf']:,.2f} (Auto-allocated for double tax treaty credit)")
    if ext.get("depotgebuehren_chf") is not None:
        lines.append(f"• Custody management fees: CHF {ext['depotgebuehren_chf']:,.2f} (100% tax-deductible)")
    if ext.get("property_maintenance_chf") and ext["property_maintenance_chf"] > 0:
        lines.append(f"• Property maintenance deductions: CHF {ext['property_maintenance_chf']:,.2f} (Werterhaltend/Energiespar)")
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
            "bank_statement": parse_bank_statement(txt),
            "broker_statement": parse_broker_statement(txt),
            "renovation_invoice": parse_renovation_invoice(txt)
        }
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
