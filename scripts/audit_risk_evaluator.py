#!/usr/bin/env python3
"""
Swiss Tax Audit Risk Evaluator (Pre-Check Radar)
Simulates cantonal tax administration automated risk profiling (Risikobasierte Fallauswahl)
100% locally to identify audit red flags before official tax filing.
"""

import sys
import json
import argparse
from typing import Dict, Any, List, Optional

def evaluate_tax_audit_risk(
    annual_net_income_chf: float,
    claimed_s7_education_chf: float = 0.0,
    claimed_s1_commute_chf: float = 0.0,
    is_commute_car_in_sbb_zone: bool = False,
    claimed_s9_homeoffice_chf: float = 0.0,
    employer_provides_workstation: bool = False,
    has_missing_proofs: bool = False,
    missing_proof_count: int = 0,
    canton: str = "BE"
) -> Dict[str, Any]:
    """
    Evaluates official tax return risk radar score (0-100) and flags risky items.
    """
    score = 100
    flagged_items: List[Dict[str, Any]] = []

    # Rule 1: Continuing Education (S7 Weiterbildung) > 15% net income or > 8,000 CHF
    if claimed_s7_education_chf > 0:
        ratio = (claimed_s7_education_chf / annual_net_income_chf) if annual_net_income_chf > 0 else 1.0
        if ratio > 0.15 or claimed_s7_education_chf > 8000.0:
            score -= 20
            flagged_items.append({
                "category": "S7_WEITERBILDUNG",
                "claimed_amount_chf": claimed_s7_education_chf,
                "risk_level": "HIGH",
                "risk_reason": (
                    f"Continuing education costs represent {ratio*100:.1f}% of net income "
                    f"(exceeds 15% benchmark or CHF 8,000). Tax office algorithms flag this for strict manual audit."
                ),
                "legal_reference": "DBG Art. 33 Abs. 1 j / StG BE Art. 27",
                "suggested_action": (
                    "Ensure you have: 1) Detailed course invoices with dates; "
                    "2) An employer confirmation letter (Arbeitgeberbestätigung) proving direct relevance to your current profession."
                )
            })

    # Rule 2: Missing Receipts / Proofs for claimed deductions
    if has_missing_proofs or missing_proof_count > 0:
        count = max(1, missing_proof_count)
        deduction_penalty = min(30, count * 10)
        score -= deduction_penalty
        flagged_items.append({
            "category": "MISSING_RECEIPTS",
            "claimed_amount_chf": 0.0,
            "risk_level": "HIGH",
            "risk_reason": f"Detected {count} claimed item(s) without original proof of payment or scanned receipt.",
            "legal_reference": "DBG Art. 123 / Mitwirkungspflicht",
            "suggested_action": (
                "In Switzerland, claimed expenses without receipt copies face near 100% rejection. "
                "Upload receipts or switch to standard statutory flat deductions (Pauschalabzug)."
            )
        })

    # Rule 3: Car Commute (S1) claimed in SBB Public Transit Hub
    if is_commute_car_in_sbb_zone and claimed_s1_commute_chf > 3000.0:
        score -= 15
        flagged_items.append({
            "category": "S1_FAHRKOSTEN",
            "claimed_amount_chf": claimed_s1_commute_chf,
            "risk_level": "MEDIUM",
            "risk_reason": (
                "Car commute (0.70 CHF/km) claimed in a zone with frequent public transit. "
                "Tax inspectors require proof that public transit takes at least 1 hour longer per day."
            ),
            "legal_reference": "DBG Art. 26 Abs. 1 a / Berufskostenverordnung Art. 5",
            "suggested_action": (
                "If no medical or shift work justification exists, tax administration will automatically "
                "cut deduction down to standard SBB General Abonnement / Streckenabo price."
            )
        })

    # Rule 4: Home Office deduction when employer workstation is available
    if claimed_s9_homeoffice_chf > 0 and employer_provides_workstation:
        score -= 15
        flagged_items.append({
            "category": "S9_HOMEOFFICE",
            "claimed_amount_chf": claimed_s9_homeoffice_chf,
            "risk_level": "HIGH",
            "risk_reason": (
                "Lohnausweis Field 15 indicates employer provides a suitable desk. "
                "Swiss Federal Supreme Court jurisprudence disallows private home office deductions in this case."
            ),
            "legal_reference": "BGE 140 II 157",
            "suggested_action": "Obtain written confirmation from employer that no permanent desk is available in office."
        })

    overall_score = max(0, min(100, score))
    if overall_score >= 85:
        overall_level = "LOW"
    elif overall_score >= 70:
        overall_level = "MEDIUM"
    else:
        overall_level = "HIGH"

    can_proceed = overall_score >= 75 and not any(item["risk_level"] == "HIGH" for item in flagged_items if item["category"] == "MISSING_RECEIPTS")

    return {
        "status": "success",
        "canton": canton.upper(),
        "overall_risk_score": overall_score,
        "overall_risk_level": overall_level,
        "can_proceed_safely": can_proceed,
        "flagged_items": flagged_items,
        "summary": (
            "Your tax declaration shows high audit resilience. Safe to file."
            if can_proceed else
            f"Caution: Audit safety score is {overall_score}/100. Resolve flagged items before submitting to avoid tax adjustment."
        )
    }

def main():
    parser = argparse.ArgumentParser(description="Swiss Tax Audit Risk Pre-Check Radar")
    parser.add_argument("--income", type=float, required=True, help="Annual net income in CHF")
    parser.add_argument("--education", type=float, default=0.0, help="Claimed S7 education cost in CHF")
    parser.add_argument("--commute", type=float, default=0.0, help="Claimed S1 commute cost in CHF")
    parser.add_argument("--sbb-zone", action="store_true", help="Set if commute route has direct train")
    parser.add_argument("--homeoffice", type=float, default=0.0, help="Claimed S9 homeoffice rent in CHF")
    parser.add_argument("--employer-desk", action="store_true", help="Set if employer provides desk in office")
    parser.add_argument("--missing-proofs", action="store_true", help="Set if any claimed item lacks receipt")
    parser.add_argument("--missing-count", type=int, default=0, help="Number of missing receipts")
    parser.add_argument("--canton", type=str, default="BE", help="Two-letter canton code")
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")

    args = parser.parse_args()
    res = evaluate_tax_audit_risk(
        annual_net_income_chf=args.income,
        claimed_s7_education_chf=args.education,
        claimed_s1_commute_chf=args.commute,
        is_commute_car_in_sbb_zone=args.sbb_zone,
        claimed_s9_homeoffice_chf=args.homeoffice,
        employer_provides_workstation=args.employer_desk,
        has_missing_proofs=args.missing_proofs,
        missing_proof_count=args.missing_count,
        canton=args.canton
    )

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"--- Swiss Tax Audit Risk Pre-Check Radar ({res['canton']}) ---")
        print(f"Audit Safety Score: {res['overall_risk_score']} / 100 ({res['overall_risk_level']} RISK)")
        print(f"Can Proceed Safely: {'YES' if res['can_proceed_safely'] else 'NO - ATTENTION NEEDED'}")
        print(f"{res['summary']}\n")
        if res["flagged_items"]:
            print(f"Detected {len(res['flagged_items'])} Flagged Area(s):")
            for idx, item in enumerate(res["flagged_items"], 1):
                print(f" [{idx}] {item['category']} ({item['risk_level']})")
                print(f"     Reason:    {item['risk_reason']}")
                print(f"     Legal Ref: {item['legal_reference']}")
                print(f"     Action:    {item['suggested_action']}")

if __name__ == "__main__":
    main()
