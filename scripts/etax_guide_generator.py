#!/usr/bin/env python3
"""
etax_guide_generator.py — Generates canton-specific step-by-step eTax form filling guides.

Translates calculated figures into the EXACT box numbers and section names
for Swiss cantonal electronic portals:
  - Bern: TaxMe-Online (taxme.ch)
  - Zurich: eTax.zh (services.zh.ch)
  - Vaud: VaudTax (vd.ch/vaudtax)
  - Geneva: GeTax (ge.ch/getax)
  - General: Standard eTax form fallback for other cantons

Usage:
  python3 scripts/etax_guide_generator.py generate <year>
"""

import sys
import os
import json
import argparse
from datetime import date
from typing import Dict, Any

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
try:
    import user_profile
except ImportError:
    user_profile = None

def generate_etax_guide(year: int) -> Dict[str, Any]:
    if not user_profile:
        return {"error": "user_profile module not available"}

    prof = user_profile.cmd_get("profile")
    tax = user_profile.cmd_get("tax", year)

    canton = (prof.get("address", {}).get("canton") or "BE").upper().strip()
    commune = prof.get("address", {}).get("commune") or "Gemeinde"
    gross = tax.get("income", {}).get("gross_chf") or 0.0
    s1_commute = tax.get("deductions", {}).get("s1_commute_chf") or 0.0
    s2_meals = tax.get("deductions", {}).get("s2_meals_chf") or 0.0
    s4_3a = tax.get("deductions", {}).get("s4_pillar3a_chf") or 0.0
    insurance = tax.get("deductions", {}).get("insurance_premiums_chf") or 2400.0
    bank_bal = tax.get("wealth", {}).get("bank_balance_31dec_chf") or 0.0

    if canton == "BE":
        content = _guide_bern_taxme(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal)
    elif canton == "ZH":
        content = _guide_zurich_etax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal)
    elif canton == "VD":
        content = _guide_vaud_vaudtax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal)
    elif canton == "GE":
        content = _guide_geneva_getax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal)
    else:
        content = _guide_general_canton(year, canton, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal)

    # Save report
    save_res = user_profile.cmd_save_report(year, f"etax_guide_{canton.lower()}", content)
    return {
        "status": "SUCCESS",
        "canton": canton,
        "tax_year": year,
        "guide_path": save_res.get("path"),
        "guide_markdown": content
    }

def _guide_bern_taxme(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float) -> str:
    return f"""# 🇨🇭 伯尔尼州 TaxMe 网页填报对照清单 ({year} 年度)

> **官方填报网站**: [www.taxme.ch](https://www.taxme.ch)  
> 请登录 TaxMe 后，按左侧菜单逐项对照填入以下精确数值（5 分钟完成填报）：

---

### 1. 收入申报 【Einkünfte aus unselbständiger Erwerbstätigkeit】
* 打开工资单输入页面（Lohnausweis erfassen）：
  * **Ziffer 1 (Lohn / Bruttolohn)**: 填入 `CHF {gross:,.2f}`
  * **Ziffer 13.1 (Verbilligte Verpflegung)**: {'勾选 Kantine / 食堂餐补' if s2 == 1600 else '未勾选 / 外部餐饮'}

---

### 2. 职业支出扣除 【Berufskosten】
* **Ziffer 2.1 (Fahrkosten zwischen Wohn- und Arbeitsstätte)**:
  * 交通方式勾选: **ÖV (公共交通)**
  * 填入必要通勤扣除金额: `CHF {s1:,.2f}`
  * *(注: 伯尔尼州最高扣除限额为 CHF 7,000；联邦直接税系统会自动限额为 CHF 3,200)*
* **Ziffer 2.2 (Mehrkosten bei auswärtiger Verpflegung)**:
  * 填入伙食定额: `CHF {s2:,.2f}`
  * *(公司有餐补填 1,600，无餐补外食填 3,200)*

---

### 3. 养老与一般扣除 【Allgemeine Abzüge & Vorsorge】
* **Ziffer 6.1 (Beiträge an anerkannte Formen der gebundenen Selbstvorsorge - Säule 3a)**:
  * 填入第三支柱缴款: `CHF {s4:,.2f}`
* **Ziffer 6.3 (Prämien für Lebens-, Kranken- und Unfallversicherungen)**:
  * 填入实际保费支出: `CHF {ins:,.2f}` (伯尔尼法定单身限额通常为 CHF 2,400，已婚 CHF 4,800)

---

### 4. 财产税申报 【Wertschriften- und Guthabenverzeichnis】
* 添加银行活期/储蓄账户：
  * **Saldo per 31.12.{year}**: 填入 `CHF {bank:,.2f}`

---
✅ **核对与提交**:
完成上述输入后，检查 TaxMe 右上角汇总金额，确认无误后点击生成正式申报 PDF 或在线一键电子签名提交！
"""

def _guide_zurich_etax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float) -> str:
    return f"""# 🇨🇭 苏黎世州 eTax.zh 网页填报对照清单 ({year} 年度)

> **官方填报网站**: [zh.ch/steuern](https://www.zh.ch/de/steuern-finanzen/steuern.html) (eTax.zh)  
> 请登录 eTax.zh 后，按表单编号（Code）输入以下预审数值：

---

### 1. 主职业收入 【Einkünfte aus Haupterwerb】
* **Code 110 (Bruttolohn gemäss Ziffer 1 Lohnausweis)**:
  * 填入: `CHF {gross:,.2f}`

---

### 2. 职业开支 【Berufsauslagen】
* **Code 210 (Fahrkosten Wohn- / Arbeitsort)**:
  * 填入: `CHF {s1:,.2f}` *(苏黎世州法定扣除上限为 CHF 5,000)*
* **Code 220 (Mehrkosten für Verpflegung)**:
  * 填入: `CHF {s2:,.2f}` *(外食定额 3,200 / 食堂 1,600)*

---

### 3. 节税与个人扣除 【Abzüge】
* **Code 410 (Beiträge an die Säule 3a)**:
  * 填入: `CHF {s4:,.2f}` *(全额抵扣，上限 CHF 7,258)*
* **Code 440 (Krankenkassen- und Versicherungsprämien)**:
  * 填入: `CHF {ins:,.2f}` *(苏黎世法定单身上限 CHF 2,600，已婚 CHF 5,200)*

---

### 4. 财产总值 【Vermögen per 31.12.{year}】
* **Code 610 (Bank- und Postguthaben)**:
  * 填入账户年末总值: `CHF {bank:,.2f}`

---
✅ **核对与提交**: 检查应税收入 (Steuerbares Einkommen)，保存并提交审核回执。
"""

def _guide_vaud_vaudtax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float) -> str:
    return f"""# 🇨🇭 沃州 VaudTax 填报对照清单 ({year} 年度)

> **官方填报网站**: [vd.ch/vaudtax](https://www.vd.ch/themes/etat-droit-finances/impots/impots-pour-les-individus/vaudtax)  
> Saisissez les montants suivants dans votre déclaration VaudTax :

---

* **Code 100 (Salaire brut / Box 1)**: `CHF {gross:,.2f}`
* **Code 200 (Frais de déplacement / Transport)**: `CHF {s1:,.2f}`
* **Code 210 (Frais de repas hors du domicile)**: `CHF {s2:,.2f}`
* **Code 310 (Cotisations au 3e pilier A)**: `CHF {s4:,.2f}`
* **Code 330 (Primes d'assurance et intérêts de capitaux)**: `CHF {ins:,.2f}`
* **Code 600 (Fortune mobilière per 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_geneva_getax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float) -> str:
    return f"""# 🇨🇭 日内瓦州 GeTax 填报对照清单 ({year} 年度)

> **官方填报网站**: [ge.ch/getax](https://www.ge.ch/getax)  
> Remplissez les rubriques officielles de votre déclaration GeTax :

---

* **Rubrique 10.00 (Traitements et salaires bruts)**: `CHF {gross:,.2f}`
* **Rubrique 11.10 (Frais effectifs de transport)**: `CHF {min(s1, 500.0):,.2f}` *(Plafond GE: CHF 500)*
* **Rubrique 11.20 (Frais de repas)**: `CHF {s2:,.2f}`
* **Rubrique 12.10 (Cotisations 3e pilier A)**: `CHF {s4:,.2f}`
* **Rubrique 12.30 (Primes d'assurance)**: `CHF {ins:,.2f}`
* **Rubrique 50.00 (Comptes bancaires et fortune au 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_general_canton(year: int, canton: str, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float) -> str:
    return f"""# 🇨🇭 {canton} 州官方电子申报对照清单 ({year} 年度)

请登录您所在州的税务官方申报系统（eTax），在对应税目栏输入以下核准数值：

---

* **主税前年薪 (Bruttoeinkommen / Salaire brut)**: `CHF {gross:,.2f}`
* **职业交通支出 (Fahrkosten / Déplacement S1)**: `CHF {s1:,.2f}`
* **外食餐饮定额 (Auswärtige Verpflegung S2)**: `CHF {s2:,.2f}`
* **第三支柱减税养老金 (Säule 3a S4)**: `CHF {s4:,.2f}`
* **医保与寿险法定扣除 (Versicherungsabzug)**: `CHF {ins:,.2f}`
* **银行年末总存款 (Bankguthaben 31.12)**: `CHF {bank:,.2f}`
"""

def main():
    parser = argparse.ArgumentParser(description="eTax guide generator for Swiss cantons")
    parser.add_argument("cmd", choices=["generate"])
    parser.add_argument("year", nargs="?", type=int, default=date.today().year)
    args = parser.parse_args()

    if args.cmd == "generate":
        res = generate_etax_guide(args.year)
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
