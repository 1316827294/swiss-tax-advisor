#!/usr/bin/env python3
"""
etax_guide_generator.py — Comprehensive 26-canton eTax box-by-box filling guide generator.

Generates exact step-by-step instructions for all 26 Swiss cantons, matching the exact
software portals and section codes (TaxMe, eTax.zh, EasyTax, BalTax, eTax.zug, VaudTax, GeTax, FriTax, ValTax, e-Tax TI, etc.).

Usage:
  python3 scripts/etax_guide_generator.py generate <year>
"""

import sys
import os
import json
import argparse
from datetime import date
from typing import Dict, Any, Optional

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
try:
    import user_profile
except ImportError:
    user_profile = None

# ── Master 26-Canton eTax Portal Registry ──────────────────────────────────────
CANTON_ETAX_REGISTRY = {
    "ZH": {"name_zh": "苏黎世州", "portal": "eTax.zh", "url": "https://www.zh.ch/de/steuern-finanzen/steuern.html", "lang": "DE", "commute_cap": 5000.0},
    "BE": {"name_zh": "伯尔尼州", "portal": "TaxMe-Online", "url": "https://www.taxme.ch", "lang": "DE", "commute_cap": 7000.0},
    "LU": {"name_zh": "卢塞恩州", "portal": "eTax.luzern", "url": "https://steuern.lu.ch", "lang": "DE", "commute_cap": 6000.0},
    "UR": {"name_zh": "乌里州", "portal": "eTax.ur", "url": "https://www.ur.ch/dienstleistungen/3321", "lang": "DE", "commute_cap": None},
    "SZ": {"name_zh": "施维茨州", "portal": "eTax.sz", "url": "https://www.sz.ch/steuern", "lang": "DE", "commute_cap": 6000.0},
    "OW": {"name_zh": "上瓦尔登州", "portal": "eTax.ow", "url": "https://www.ow.ch", "lang": "DE", "commute_cap": None},
    "NW": {"name_zh": "下瓦尔登州", "portal": "eTax.nw", "url": "https://www.nw.ch", "lang": "DE", "commute_cap": None},
    "GL": {"name_zh": "格拉鲁斯州", "portal": "eTax.gl", "url": "https://www.gl.ch", "lang": "DE", "commute_cap": None},
    "ZG": {"name_zh": "楚格州 (低税)", "portal": "eTax.zug", "url": "https://www.zg.ch/tax", "lang": "DE", "commute_cap": None},
    "FR": {"name_zh": "弗里堡州", "portal": "FriTax", "url": "https://www.fr.ch/de/fritax", "lang": "FR/DE", "commute_cap": 3300.0},
    "SO": {"name_zh": "索洛图恩州", "portal": "eTax.so", "url": "https://so.ch/verwaltung/finanzdepartement/steueramt", "lang": "DE", "commute_cap": 7000.0},
    "BS": {"name_zh": "巴塞尔城市州", "portal": "BalTax / eTax.bs", "url": "https://www.steuerverwaltung.bs.ch/baltax", "lang": "DE", "commute_cap": 3300.0},
    "BL": {"name_zh": "巴塞尔乡村州", "portal": "eTax.bl", "url": "https://www.baselland.ch/steuern", "lang": "DE", "commute_cap": None},
    "SH": {"name_zh": "沙夫豪森州", "portal": "eTax.sh", "url": "https://sh.ch/steuern", "lang": "DE", "commute_cap": 6000.0},
    "AR": {"name_zh": "外阿彭策尔州", "portal": "eTax.ar", "url": "https://www.ar.ch/steuern", "lang": "DE", "commute_cap": 6000.0},
    "AI": {"name_zh": "内阿彭策尔州", "portal": "eTax.ai", "url": "https://www.ai.ch", "lang": "DE", "commute_cap": 6000.0},
    "SG": {"name_zh": "圣加仑州", "portal": "eTax.sg", "url": "https://steuern.sg.ch", "lang": "DE", "commute_cap": 4460.0},
    "GR": {"name_zh": "格劳宾登州", "portal": "eTax.gr", "url": "https://www.stv.gr.ch", "lang": "DE/IT", "commute_cap": 5000.0},
    "AG": {"name_zh": "阿尔高州", "portal": "EasyTax AG", "url": "https://www.ag.ch/steuern", "lang": "DE", "commute_cap": 7000.0},
    "TG": {"name_zh": "图尔高州", "portal": "eTax.tg", "url": "https://steuerverwaltung.tg.ch", "lang": "DE", "commute_cap": 6000.0},
    "TI": {"name_zh": "提契诺州", "portal": "e-Tax TI", "url": "https://www.ti.ch/fisco", "lang": "IT", "commute_cap": 3300.0},
    "VD": {"name_zh": "沃州", "portal": "VaudTax", "url": "https://www.vd.ch/vaudtax", "lang": "FR", "commute_cap": 3300.0},
    "VS": {"name_zh": "瓦莱州", "portal": "ValTax", "url": "https://www.vs.ch/impots", "lang": "FR/DE", "commute_cap": 3300.0},
    "NE": {"name_zh": "纳沙泰尔州", "portal": "Clic&Tax", "url": "https://www.ne.ch/impots", "lang": "FR", "commute_cap": 3300.0},
    "GE": {"name_zh": "日内瓦州", "portal": "GeTax", "url": "https://www.ge.ch/getax", "lang": "FR", "commute_cap": 500.0},
    "JU": {"name_zh": "汝拉州", "portal": "JuraTax", "url": "https://www.jura.ch/finances/impots", "lang": "FR", "commute_cap": 3300.0}
}

# ── Guide Dispatcher ──────────────────────────────────────────────────────────
def generate_etax_guide(year: int) -> Dict[str, Any]:
    if not user_profile:
        return {"error": "user_profile module not available"}

    prof = user_profile.cmd_get("profile")
    tax = user_profile.cmd_get("tax", year)

    canton = (prof.get("address", {}).get("canton") or "BE").upper().strip()
    if canton not in CANTON_ETAX_REGISTRY:
        canton = "BE"

    commune = prof.get("address", {}).get("commune") or "Gemeinde"
    gross = tax.get("income", {}).get("gross_chf") or 0.0
    s1_commute = tax.get("deductions", {}).get("s1_commute_chf") or 0.0
    s2_meals = tax.get("deductions", {}).get("s2_meals_chf") or 0.0
    s4_3a = tax.get("deductions", {}).get("s4_pillar3a_chf") or 0.0
    insurance = tax.get("deductions", {}).get("insurance_premiums_chf") or 2400.0
    bank_bal = tax.get("wealth", {}).get("bank_balance_31dec_chf") or 0.0

    meta = CANTON_ETAX_REGISTRY[canton]

    # Canton specific generator router
    if canton == "BE":
        content = _guide_bern_taxme(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "ZH":
        content = _guide_zurich_etax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "ZG":
        content = _guide_zug_etax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "BS":
        content = _guide_basel_baltax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "AG":
        content = _guide_aargau_easytax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "LU":
        content = _guide_luzern_etax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "VD":
        content = _guide_vaud_vaudtax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "GE":
        content = _guide_geneva_getax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton in ("FR", "VS"):
        content = _guide_bilingual_fr_vs(year, canton, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton == "TI":
        content = _guide_ticino_etax(year, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    elif canton in ("NE", "JU"):
        content = _guide_romandie_general(year, canton, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)
    else:
        # Standard Swiss German eTax suite (SG, SO, TG, SZ, GR, BL, SH, AR, AI, GL, UR, OW, NW)
        content = _guide_standard_german_etax(year, canton, gross, s1_commute, s2_meals, s4_3a, insurance, bank_bal, meta)

    # Save report
    save_res = user_profile.cmd_save_report(year, f"etax_guide_{canton.lower()}", content)
    return {
        "status": "SUCCESS",
        "canton": canton,
        "canton_name": meta["name_zh"],
        "portal_name": meta["portal"],
        "portal_url": meta["url"],
        "tax_year": year,
        "guide_path": save_res.get("path"),
        "guide_markdown": content
    }

# ── Canton Implementation Details ─────────────────────────────────────────────

def _guide_bern_taxme(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (BE) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']})  
> 登录 TaxMe 后，按左侧菜单逐项对照填入以下数值（5 分钟完成网报）：

---

### 1. 收入申报 【Einkünfte aus unselbständiger Erwerbstätigkeit】
* **Ziffer 1 (Lohn / Bruttolohn)**: 填入 `CHF {gross:,.2f}`
* **Ziffer 13.1 (Verbilligte Verpflegung)**: {'勾选 Kantine / 食堂餐补' if s2 == 1600 else '未勾选 / 外部餐饮'}

### 2. 职业支出扣除 【Berufskosten】
* **Ziffer 2.1 (Fahrkosten)**: 交通方式勾选 **ÖV**，填入 `CHF {s1:,.2f}` *(伯尔尼上限 CHF 7,000；联邦直接税系统自动限额为 CHF 3,200)*
* **Ziffer 2.2 (Mehrkosten Verpflegung)**: 填入伙食定额 `CHF {s2:,.2f}` *(餐补 1,600 / 外食 3,200)*

### 3. 养老与一般扣除 【Vorsorge & Abzüge】
* **Ziffer 6.1 (Säule 3a)**: 填入 `CHF {s4:,.2f}` *(全额免税)*
* **Ziffer 6.3 (Versicherungsprämien)**: 填入 `CHF {ins:,.2f}`

### 4. 财产税申报 【Wertschriften- und Guthabenverzeichnis】
* **Saldo per 31.12.{year}**: 填入所有账户年末存款余额 `CHF {bank:,.2f}`
"""

def _guide_zurich_etax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (ZH) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']}) (eTax.zh)  
> 登录 eTax.zh 后，按表单编号（Code）输入以下审核数值：

---

* **Code 110 (Bruttolohn gemäss Box 1)**: 填入 `CHF {gross:,.2f}`
* **Code 210 (Fahrkosten)**: 填入 `CHF {s1:,.2f}` *(苏黎世上限 CHF 5,000；联邦上限 CHF 3,200)*
* **Code 220 (Verpflegung)**: 填入 `CHF {s2:,.2f}` *(外食 3,200 / 食堂 1,600)*
* **Code 410 (Beiträge Säule 3a)**: 填入 `CHF {s4:,.2f}`
* **Code 440 (Versicherungsabzug)**: 填入 `CHF {ins:,.2f}` *(法定单身上限 CHF 2,600，已婚 CHF 5,200)*
* **Code 610 (Bankguthaben 31.12)**: 填入 `CHF {bank:,.2f}`
"""

def _guide_zug_etax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (ZG) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']}) (eTax.zug)  
> 楚格州是全瑞士税率最低的州之一（无州级通勤扣除上限）：

---

* **Ziffer 1 (Bruttoerwerbseinkommen)**: 填入 `CHF {gross:,.2f}`
* **Ziffer 2.1 (Fahrkosten)**: 填入必要公交通勤费用 `CHF {s1:,.2f}` *(楚格州本级无上限；联邦税由系统自动截断至 3,200 CHF)*
* **Ziffer 2.2 (Auswärtige Verpflegung)**: 填入 `CHF {s2:,.2f}`
* **Ziffer 6.1 (Säule 3a)**: 填入 `CHF {s4:,.2f}`
* **Ziffer 6.3 (Versicherungsabzug)**: 填入 `CHF {ins:,.2f}`
* **Wertschriftenverzeichnis (Guthaben 31.12)**: 填入年末存款 `CHF {bank:,.2f}`
"""

def _guide_basel_baltax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (BS) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']}) (BalTax)  
> 巴塞尔城市州官方系统对应输入栏目：

---

* **Code 100 (Haupterwerb Bruttolohn)**: `CHF {gross:,.2f}`
* **Code 200 (Fahrkosten)**: `CHF {s1:,.2f}` *(州限额 CHF 3,300；联邦限额 CHF 3,200)*
* **Code 210 (Mehrkosten Verpflegung)**: `CHF {s2:,.2f}`
* **Code 400 (Säule 3a)**: `CHF {s4:,.2f}`
* **Code 420 (Krankenkassen- und Versicherungsabzug)**: `CHF {ins:,.2f}`
* **Code 600 (Guthaben bei Banken per 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_aargau_easytax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (AG) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']}) (EasyTax AG)  
> 阿尔高州官方软件填报代码：

---

* **Ziffer 1 (Bruttolohn)**: `CHF {gross:,.2f}`
* **Ziffer 2.1 (Fahrkosten)**: `CHF {s1:,.2f}` *(阿尔高州上限 CHF 7,000；联邦上限 CHF 3,200)*
* **Ziffer 2.2 (Verpflegung)**: `CHF {s2:,.2f}`
* **Ziffer 6.1 (Säule 3a)**: `CHF {s4:,.2f}`
* **Ziffer 6.4 (Versicherungsabzug)**: `CHF {ins:,.2f}`
* **Wertschriftenverzeichnis**: 年末存款余额填入 `CHF {bank:,.2f}`
"""

def _guide_luzern_etax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (LU) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']}) (eTax.luzern)  
> 卢塞恩州官方申报系统代码：

---

* **Ziffer 101 (Bruttolohn)**: `CHF {gross:,.2f}`
* **Ziffer 201 (Fahrkosten)**: `CHF {s1:,.2f}` *(卢塞恩州上限 CHF 6,000；联邦上限 CHF 3,200)*
* **Ziffer 202 (Verpflegung)**: `CHF {s2:,.2f}`
* **Ziffer 401 (Säule 3a)**: `CHF {s4:,.2f}`
* **Ziffer 404 (Versicherungsprämien)**: `CHF {ins:,.2f}`
* **Ziffer 601 (Guthaben per 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_vaud_vaudtax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (VD) 官方申报指南 ({year} 年度)

> **Portail officiel**: [{meta['portal']}]({meta['url']})  
> Saisissez les montants suivants dans votre déclaration VaudTax :

---

* **Code 100 (Salaire brut / Box 1)**: `CHF {gross:,.2f}`
* **Code 200 (Frais de déplacement / Transport)**: `CHF {s1:,.2f}` *(Plafond fédéral: CHF 3,200)*
* **Code 210 (Frais de repas hors du domicile)**: `CHF {s2:,.2f}` *(Kantine: 1,600 / Restaurant: 3,200)*
* **Code 310 (Cotisations au 3e pilier A)**: `CHF {s4:,.2f}`
* **Code 330 (Primes d'assurance et intérêts de capitaux)**: `CHF {ins:,.2f}`
* **Code 600 (Fortune mobilière per 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_geneva_getax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (GE) 官方申报指南 ({year} 年度)

> **Portail officiel**: [{meta['portal']}]({meta['url']})  
> Remplissez les rubriques officielles de votre déclaration GeTax :

---

* **Rubrique 10.00 (Traitements et salaires bruts)**: `CHF {gross:,.2f}`
* **Rubrique 11.10 (Frais de transport)**: `CHF {min(s1, 500.0):,.2f}` *(⚠️ Plafond cantonal GE très strict: CHF 500)*
* **Rubrique 11.20 (Frais de repas)**: `CHF {s2:,.2f}`
* **Rubrique 12.10 (Cotisations 3e pilier A)**: `CHF {s4:,.2f}`
* **Rubrique 12.30 (Primes d'assurance)**: `CHF {ins:,.2f}`
* **Rubrique 50.00 (Comptes bancaires per 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_bilingual_fr_vs(year: int, canton: str, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} ({canton}) 双语官方申报指南 ({year} 年度)

> **Portail officiel / Offizielles Portal**: [{meta['portal']}]({meta['url']})  
> 弗里堡/瓦莱州为德法双语州，系统支持语言切换：

---

* **Ziffer/Code 1 (Bruttolohn / Salaire brut)**: `CHF {gross:,.2f}`
* **Ziffer/Code 2.1 (Fahrkosten / Déplacement)**: `CHF {s1:,.2f}` *(州限额 CHF 3,300；联邦限额 CHF 3,200)*
* **Ziffer/Code 2.2 (Verpflegung / Repas)**: `CHF {s2:,.2f}`
* **Ziffer/Code 6.1 (Säule 3a / 3e pilier A)**: `CHF {s4:,.2f}`
* **Ziffer/Code 6.3 (Versicherungen / Assurances)**: `CHF {ins:,.2f}`
* **Guthaben / Fortune bancaire (31.12)**: `CHF {bank:,.2f}`
"""

def _guide_ticino_etax(year: int, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} (TI) 官方申报指南 ({year} 年度)

> **Portale ufficiale**: [{meta['portal']}]({meta['url']}) (e-Tax TI)  
> Inserire i seguenti valori nella dichiarazione d'imposta ufficiale del Cantone Ticino:

---

* **Codice 100 (Redditi da attività lucrativa dipendente)**: `CHF {gross:,.2f}`
* **Codice 200 (Spese di trasporto)**: `CHF {s1:,.2f}` *(Plafond TI: CHF 3,300; federale: CHF 3,200)*
* **Codice 210 (Spese di vitto fuori casa)**: `CHF {s2:,.2f}`
* **Codice 310 (Contributi al 3° pilastro A)**: `CHF {s4:,.2f}`
* **Codice 330 (Premi di assicurazione malattia)**: `CHF {ins:,.2f}`
* **Codice 500 (Saldi bancari e postali al 31.12)**: `CHF {bank:,.2f}`
"""

def _guide_romandie_general(year: int, canton: str, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    return f"""# 🇨🇭 {meta['name_zh']} ({canton}) 官方申报指南 ({year} 年度)

> **Portail officiel**: [{meta['portal']}]({meta['url']})  
> Déclaration d'impôts cantonale pour les personnes physiques :

---

* **Salaire brut (Box 1)**: `CHF {gross:,.2f}`
* **Frais de transport (S1)**: `CHF {s1:,.2f}` *(Plafond fédéral: CHF 3,200)*
* **Frais de repas (S2)**: `CHF {s2:,.2f}`
* **Prévoyance liée 3e pilier A (S4)**: `CHF {s4:,.2f}`
* **Primes d'assurance-maladie**: `CHF {ins:,.2f}`
* **Fortune mobilière au 31.12**: `CHF {bank:,.2f}`
"""

def _guide_standard_german_etax(year: int, canton: str, gross: float, s1: float, s2: float, s4: float, ins: float, bank: float, meta: Dict) -> str:
    cap_str = f"CHF {meta['commute_cap']:,.0f}" if meta['commute_cap'] else "无上限"
    return f"""# 🇨🇭 {meta['name_zh']} ({canton}) 官方申报指南 ({year} 年度)

> **官方软件/门户**: [{meta['portal']}]({meta['url']})  
> 本州使用瑞士标准 eTax 报税系统（Ringler 统一套件），请在官方系统逐项录入以下数值：

---

### 1. 职业收入 【Haupterwerb】
* **Ziffer 1 (Bruttoeinkommen gemäss Lohnausweis)**: `CHF {gross:,.2f}`

### 2. 职业开支扣除 【Berufsauslagen】
* **Ziffer 2.1 (Fahrkosten Wohn- / Arbeitsort)**: `CHF {s1:,.2f}`
  * *(注: {meta['name_zh']}本级通勤扣除限额为: {cap_str}；联邦直接税自动限额为 CHF 3,200)*
* **Ziffer 2.2 (Auswärtige Verpflegung)**: `CHF {s2:,.2f}` *(食堂餐补 1,600 / 自费外食 3,200)*

### 3. 养老与保险扣除 【Vorsorge & Abzüge】
* **Ziffer 6.1 (Beiträge an Säule 3a)**: `CHF {s4:,.2f}` *(全额税前扣除，上限 CHF 7,258)*
* **Ziffer 6.3 (Krankenkassen- und Versicherungsabzug)**: `CHF {ins:,.2f}`

### 4. 银行存款与财产 【Wertschriftenverzeichnis】
* **Guthaben per 31.12.{year}**: 填入 `CHF {bank:,.2f}`
"""

def main():
    parser = argparse.ArgumentParser(description="eTax guide generator for all 26 Swiss cantons")
    parser.add_argument("cmd", choices=["generate", "list-cantons"])
    parser.add_argument("year", nargs="?", type=int, default=date.today().year)
    args = parser.parse_args()

    if args.cmd == "generate":
        res = generate_etax_guide(args.year)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.cmd == "list-cantons":
        print(json.dumps(CANTON_ETAX_REGISTRY, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
