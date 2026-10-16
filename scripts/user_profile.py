#!/usr/bin/env python3
"""
user_profile.py — LLM-facing state machine & utility for Swiss Tax Advisor.

Manages local profile and tax data under ./user/ with zero user friction.
Strictly intended to be invoked by the LLM Agent silently, NEVER by the end user.

Usage:
  python3 scripts/user_profile.py status
  python3 scripts/user_profile.py next-question [year]
  python3 scripts/user_profile.py get profile
  python3 scripts/user_profile.py get tax [year]
  python3 scripts/user_profile.py set profile '<json>'
  python3 scripts/user_profile.py set tax [year] '<json>'
  python3 scripts/user_profile.py save-report <year> <type> '<content>'
"""

import sys
import json
import os
import argparse
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

# ── Dynamic Project Root Resolution ───────────────────────────────────────────
def find_project_root() -> str:
    cur = os.path.dirname(os.path.abspath(__file__))
    while cur and cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "SKILL.md")) or os.path.exists(os.path.join(cur, "scripts")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = find_project_root()
USER_DIR = os.path.join(ROOT_DIR, "user")
REPORTS_DIR = os.path.join(USER_DIR, "reports")
PROFILE_PATH = os.path.join(USER_DIR, "profile.json")

def tax_data_path(year: int) -> str:
    return os.path.join(USER_DIR, f"tax_{year}.json")

def report_dir(year: int) -> str:
    return os.path.join(REPORTS_DIR, str(year))

# ── Default Schemas ────────────────────────────────────────────────────────────
def default_profile() -> Dict[str, Any]:
    return {
        "_version": "2.1",
        "_created": str(date.today()),
        "_updated": str(date.today()),
        "personal": {
            "name": None,
            "birth_year": None,
            "ahv_masked": None,
            "permit_type": None,     # CITIZEN / C / B / L
            "language": "ZH"         # ZH / EN / DE / FR / IT
        },
        "address": {
            "canton": None,          # 2-letter uppercase, e.g. ZH, BE, VD
            "commune": None,
            "zip": None
        },
        "civil_status": {
            "status": None,          # SINGLE / MARRIED / REGISTERED_PARTNER / DIVORCED
            "children_count": None,
            "spouse_employed": False,
            "spouse_gross_income_chf": 0
        },
        "religion": {
            "church_tax_liable": None, # True / False
            "denomination": None      # NONE / ROMAN_CATHOLIC / REFORMED / OTHER
        },
        "employment": {
            "type": "EMPLOYED",      # EMPLOYED / SELF_EMPLOYED / MIXED
            "work_commune": None,    # City/commune of workplace for commute necessity check
            "has_second_job": False
        },
        "recurring": {
            "commute_type": None,    # PUBLIC_TRANS / CAR / BIKE_WALK
            "commute_km_one_way": None,
            "lunch_type": None,      # CANTEEN / RESTAURANT_SELF
            "health_franchise_chf": None, # 300 / 500 / 1000 / 1500 / 2000 / 2500
            "has_real_estate": False,
            "has_securities_or_crypto": False
        },
        "onboarding_complete": False,
        "onboarding_missing_fields": []
    }

def default_tax_data(year: int) -> Dict[str, Any]:
    return {
        "_version": "2.1",
        "tax_year": year,
        "_updated": str(date.today()),
        "income": {
            "gross_chf": None,
            "bonus_chf": 0,
            "fringe_benefits_chf": 0,
            "second_job_income_chf": 0,
            "spouse_gross_chf": 0
        },
        "deductions": {
            "s1_commute_chf": None,
            "s2_meals_chf": None,
            "s4_pillar3a_chf": None,
            "s4_pillar3a_spouse_chf": 0,
            "s6_kita_chf": 0,
            "s7_education_chf": 0,
            "s8_property_maintenance_chf": 0,
            "insurance_premiums_chf": None,
            "annual_medical_spend_chf": None
        },
        "wealth": {
            "bank_balance_31dec_chf": None,
            "securities_crypto_chf": 0,
            "real_estate_value_chf": 0,
            "debts_and_mortgages_chf": 0,
            "debt_interest_chf": 0
        },
        "completeness_pct": 0,
        "missing_fields": []
    }

# ── Question Registry for Progressive Onboarding ──────────────────────────────
# Defines the ordered interview funnel, why each field matters, and questions.
QUESTION_PIPELINE = [
    # Level 1: Profile & Residency
    {
        "field": "address.canton",
        "category": "profile",
        "title_zh": "居住州 (Canton)",
        "prompt_zh": "您好！我是您的瑞士本地税务顾问。在为您生成精确的报税底稿前，我需要了解您的基本情况。\n请问您目前居住在瑞士的哪个州（Canton）？",
        "prompt_en": "Hello! I am your Swiss tax advisor. Before generating your precise tax filing, I'll guide you through a few essential questions.\nWhich canton do you currently live in?",
        "prompt_de": "Grüezi! Ich bin Ihr Schweizer Steuerassistent. In welchem Kanton haben Sie Ihren Wohnsitz?",
        "options": ["ZH (Zürich)", "BE (Bern)", "VD (Vaud)", "GE (Genève)", "BS (Basel-Stadt)", "ZG (Zug)", "其他/Other"],
        "why": "各州基础税率、抵扣上限和税表完全不同"
    },
    {
        "field": "address.commune",
        "category": "profile",
        "title_zh": "居住市镇 (Commune/Gemeinde)",
        "prompt_zh": "请问您具体住在哪个市镇（Commune / Gemeinde）？如果有邮编也可以提供。",
        "prompt_en": "Which municipality (Commune / Gemeinde) do you reside in? (Zip code is also welcome)",
        "prompt_de": "In welcher Gemeinde (oder PLZ) wohnen Sie?",
        "options": [],
        "why": "市镇税率乘数 (Steuerfuss) 决定市镇税额"
    },
    {
        "field": "civil_status.status",
        "category": "profile",
        "title_zh": "婚姻状况",
        "prompt_zh": "请问您的婚姻状况是？（单身 / 已婚 / 注册伴侣 / 离异）",
        "prompt_en": "What is your civil status? (Single / Married / Registered partner / Divorced)",
        "prompt_de": "Wie ist Ihr Zivilstand? (Ledig / Verheiratet / Eingetragene Partnerschaft / Geschieden)",
        "options": ["单身 / Ledig", "已婚 / Verheiratet", "注册伴侣", "离异 / Geschieden"],
        "why": "已婚家庭适用合并计税双人税率表及双职工扣除"
    },
    {
        "field": "civil_status.children_count",
        "category": "profile",
        "title_zh": "子女与抚养人",
        "prompt_zh": "您有几个需要共同申报或抚养的未成年子女？（若无请填 0）",
        "prompt_en": "How many dependent minor children do you declare? (Enter 0 if none)",
        "prompt_de": "Wie viele minderjährige Kinder haben Sie zu deklarieren? (0 falls keine)",
        "options": ["0", "1", "2", "3+"],
        "why": "每名子女可享受各州几千至上万法郎的子女抵扣 (Kinderabzug)"
    },
    {
        "field": "personal.permit_type",
        "category": "profile",
        "title_zh": "居留身份",
        "prompt_zh": "请问您的居留证类型是？（瑞士公民 / C 许可 / B 许可 / L 许可 / 跨境 G 证）",
        "prompt_en": "What is your residence permit? (Swiss Citizen / C permit / B permit / L permit / Cross-border G)",
        "prompt_de": "Welchen Aufenthaltsstatus haben Sie? (Schweizer Bürger / C-Ausweis / B-Ausweis / L-Ausweis / G-Grenzgänger)",
        "options": ["瑞士公民 / Schweizer", "C 许可 / C-Ausweis", "B 许可 / B-Ausweis", "L / G 许可"],
        "why": "B 许可通常被扣缴源泉税 (Quellensteuer)，需要评估是否申请转正申报 (NOV)"
    },
    {
        "field": "religion.church_tax_liable",
        "category": "profile",
        "title_zh": "宗教与教会税",
        "prompt_zh": "请问您的宗教信仰状况是？\n（无宗教信仰 / 罗马天主教 / 基督教改革宗 / 其他）\n💡 提示：在瑞士，官方承认的教会成员需缴纳约 8%~15% 的教会税（Kirchensteuer）；无宗教者依法完全免缴。",
        "prompt_en": "What is your religious affiliation? (No religion / Roman Catholic / Reformed / Other)\n💡 Note: Members of official state churches pay an 8%–15% church surcharge. Declaring no religion exempts you completely.",
        "prompt_de": "Gehören Sie einer Landeskirche an? (Keine / Römisch-katholisch / Evangelisch-reformiert)\n💡 Hinweis: Konfessionslose zahlen keine Kirchensteuer.",
        "options": ["无宗教 (免交教会税)", "罗马天主教 (Röm.-Kath.)", "基督教改革宗 (Evang.-Ref.)"],
        "why": "教会税直接影响总税额约 8%~15%"
    },
    {
        "field": "employment.type",
        "category": "profile",
        "title_zh": "职业形态",
        "prompt_zh": "您的工作性质是？（普通受雇员工 / 自由职业自雇人士 / 混合）",
        "prompt_en": "Are you primarily employed (Angestellter) or self-employed (Selbstständig)?",
        "prompt_de": "Sind Sie angestellt oder selbstständig erwerbend?",
        "options": ["受雇员工 (Angestellt)", "自雇人士 (Selbstständig)", "混合/兼职"],
        "why": "自雇人士与受雇员工的 3a 养老金扣除上限及业务成本抵扣截然不同"
    },

    # Level 2: Tax Data — Income
    {
        "field": "income.gross_chf",
        "category": "tax",
        "title_zh": "年度税前总收入 (Gross Income)",
        "prompt_zh": "接下来核对您的年度收入：请问您该年度的税前总收入（CHF）大概是多少？\n（可查看工资单 Lohnausweis 第 1 栏，若尚未拿到可提供预估年薪）",
        "prompt_en": "Now let's check your annual income: What was your gross income in CHF? (See Lohnausweis Box 1, or estimated base salary)",
        "prompt_de": "Wie hoch war Ihr Bruttolohn gemäss Lohnausweis Ziffer 1?",
        "options": [],
        "why": "瑞士个人所得税计税基石"
    },

    # Level 3: Tax Data — Deductions (Proactive Tax Saving)
    {
        "field": "deductions.s4_pillar3a_chf",
        "category": "tax",
        "title_zh": "第三支柱养老金 (Pillar 3a)",
        "prompt_zh": "您该年度向第三支柱（Pillar 3a）缴纳了多少法郎？\n💡 提示：雇员最高可存 7,258 CHF（自雇最高 36,288 CHF），这笔款项 100% 全额抵扣税前收入，是最立竿见影的节税手段。（若未存请填 0）",
        "prompt_en": "How much did you contribute to Pillar 3a? (Max 7,258 CHF for employees; 100% tax-deductible. Enter 0 if none)",
        "prompt_de": "Wie viel haben Sie in die Säule 3a einbezahlt? (Max. CHF 7'258 für Angestellte, 0 falls keine)",
        "options": ["存满上限 (CHF 7,258)", "部分存入", "未存入 (0)"],
        "why": "立竿见影的全额减税项，边际税率直接退税"
    },
    {
        "field": "recurring.commute_type",
        "category": "tax_helper",
        "title_zh": "日常通勤方式与工作地点",
        "prompt_zh": "请问您的工作地点在哪个城市/市镇？平时上下班乘坐什么交通工具？\n💡 税法实务重要核算规则：\n税务局严格按照【居住地到工作地】必要且最经济的公交通勤区间票（Streckenabo）核算。\n• 跨城通勤：若点对点年票费用 ≥ SBB GA（3,995 CHF），才可全额按 GA 申报（联邦直接税受 3,200 CHF 法定上限限制）；\n• 同城工作：通常仅认可当地交通网络月票/年票（通常 750~1,000 CHF），超出部分视为私人休闲支出剔除。\n若有具体年票/月票金额亦可直接告知。",
        "prompt_en": "Where is your workplace located (city/commune), and how do you commute?\n💡 Swiss Tax Rule: Commute deductions are based on necessity between residence and workplace. Full SBB GA (CHF 3,995) is only recognized if your cross-city point-to-point pass reaches or exceeds this cost. Intra-city commute is restricted to local network passes (approx. CHF 750–1,000). Federal tax caps at CHF 3,200.",
        "prompt_de": "Wo befindet sich Ihr Arbeitsort und wie pendeln Sie?\n💡 Hinweis: Das Generalabonnement (GA) ist nur abzugsfähig, wenn ein Streckenabonnement zwischen Wohn- und Arbeitsort mindestens so viel kosten würde. Innerorts gilt nur das lokale Verbundabonnement.",
        "options": ["公共交通 (跨城Streckenabo/GA)", "公共交通 (同城市区通勤卡)", "自驾小汽车 (需具备必要条件)", "自行车/步行 (定额 700 CHF)"],
        "why": "按工作地与居住地最经济必要交通核算 S1，防止同城虚报 GA 导致税务局稽查剔除"
    },
    {
        "field": "recurring.lunch_type",
        "category": "tax_helper",
        "title_zh": "午餐与外食",
        "prompt_zh": "关于工作日午餐：雇主是否有食堂提供餐补，还是完全需要您自费在外部就餐？\n💡 提示：自费外食法定定额抵扣 3,200 CHF，有食堂补贴定额扣 1,600 CHF。",
        "prompt_en": "For workday lunches: Does your company offer a subsidized canteen, or do you pay out-of-pocket at restaurants?\n💡 Note: External dining allows a flat CHF 3,200 deduction (canteen: CHF 1,600).",
        "prompt_de": "Verpflegung: Haben Sie eine Betriebskantine mit Verbilligung oder verpflegen Sie sich auswärts?",
        "options": ["完全外部就餐 (定额 3,200 CHF)", "公司有食堂餐补 (定额 1,600 CHF)"],
        "why": "折算 S2 伙食定额抵扣"
    },
    {
        "field": "deductions.annual_medical_spend_chf",
        "category": "tax",
        "title_zh": "自负医疗开销",
        "prompt_zh": "该年度您自费承担的医疗与牙科自付费用（扣除医保报销后）大概有多少？\n💡 提示：通常超出净收入 5% 的部分方可抵税，如无大额自费请填 0。",
        "prompt_en": "Roughly how much did you pay out-of-pocket for medical and dental expenses? (Only excess over 5% of net income is deductible; enter 0 if none)",
        "prompt_de": "Wie hoch waren Ihre selbst getragenen Krankheits- und Unfallkosten? (0 falls keine)",
        "options": ["0", "小额日常", "大额自费 (>2,000 CHF)"],
        "why": "S3 医疗自负大额抵扣"
    },

    # Level 4: Wealth & Bank Accounts
    {
        "field": "wealth.bank_balance_31dec_chf",
        "category": "tax",
        "title_zh": "年末存款与财富申报",
        "prompt_zh": "最后是财产税申报：截至 12 月 31 日，您名下所有瑞士及海外银行账户的总存款余额大概是多少？\n（若有股票、基金或房产贷款亦可一并说明；瑞士大部分州对个人存款有几万至十几万法郎的免征额）",
        "prompt_en": "Finally, for wealth tax: What was your total bank account balance across all accounts as of Dec 31? (Enter 0 or approximate balance)",
        "prompt_de": "Wie hoch waren Ihre gesamten Bankguthaben per 31. Dezember?",
        "options": ["< 50,000 CHF (通常免征)", "50,000 - 150,000 CHF", "> 150,000 CHF"],
        "why": "申报财产税及核对银行利息预扣税 (Verrechnungssteuer)"
    }
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def _ensure_user_dir():
    os.makedirs(USER_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    gi = os.path.join(USER_DIR, ".gitignore")
    if not os.path.exists(gi):
        with open(gi, "w", encoding="utf-8") as f:
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

def _load_json(path: str, default_fn) -> Dict:
    _ensure_user_dir()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_fn()
    return default_fn()

def _save_json(path: str, data: Dict):
    _ensure_user_dir()
    data["_updated"] = str(date.today())
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _deep_merge(base: Dict, update: Dict):
    for k, v in update.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v

# ── Progress and Next Question Calculation ─────────────────────────────────────
def get_onboarding_pipeline_state(year: int) -> Tuple[List[Dict], List[Dict], int]:
    profile = _load_json(PROFILE_PATH, default_profile)
    tax = _load_json(tax_data_path(year), lambda: default_tax_data(year))

    completed = []
    pending = []

    for item in QUESTION_PIPELINE:
        field = item["field"]
        target = profile if item["category"] in ("profile", "tax_helper") else tax
        val = _get_nested(target, field)
        
        # Check if field has meaningful value
        is_done = False
        if val is not None:
            is_done = True
        elif field == "deductions.s4_pillar3a_chf" and _get_nested(tax, "deductions.s4_pillar3a_chf") is not None:
            is_done = True

        if is_done:
            completed.append(item)
        else:
            pending.append(item)

    total = len(QUESTION_PIPELINE)
    percent = int(100 * len(completed) / total) if total > 0 else 0
    return completed, pending, percent

def make_progress_bar(percent: int) -> str:
    total_blocks = 10
    filled = int(percent / 10)
    return "[" + "■" * filled + "□" * (total_blocks - filled) + "]"

# ── Commands ───────────────────────────────────────────────────────────────────
def cmd_status(year: Optional[int] = None) -> Dict:
    _ensure_user_dir()
    y = year or date.today().year
    completed, pending, pct = get_onboarding_pipeline_state(y)
    profile = _load_json(PROFILE_PATH, default_profile)
    tax = _load_json(tax_data_path(y), lambda: default_tax_data(y))

    if not pending:
        next_action = "READY_TO_CALCULATE"
    else:
        next_item = pending[0]
        next_action = f"ASK_QUESTION — field: {next_item['field']}"

    return {
        "status": "READY_TO_CALCULATE" if not pending else "NEEDS_INFO",
        "tax_year": y,
        "progress_percent": pct,
        "progress_bar": make_progress_bar(pct),
        "completed_count": len(completed),
        "total_questions": len(QUESTION_PIPELINE),
        "next_field": pending[0]["field"] if pending else None,
        "next_action": next_action,
        "profile_summary": {
            "canton": _get_nested(profile, "address.canton"),
            "commune": _get_nested(profile, "address.commune"),
            "civil_status": _get_nested(profile, "civil_status.status"),
            "permit": _get_nested(profile, "personal.permit_type"),
            "church_tax_liable": _get_nested(profile, "religion.church_tax_liable")
        },
        "tax_summary": {
            "gross_income": _get_nested(tax, "income.gross_chf"),
            "pillar_3a": _get_nested(tax, "deductions.s4_pillar3a_chf")
        }
    }

def cmd_next_question(year: Optional[int] = None) -> Dict:
    _ensure_user_dir()
    y = year or date.today().year
    completed, pending, pct = get_onboarding_pipeline_state(y)

    if not pending:
        return {
            "status": "READY_TO_CALCULATE",
            "progress_percent": 100,
            "progress_bar": make_progress_bar(100),
            "message": "All required tax information is collected. You can now execute calculation scripts."
        }

    q = pending[0]
    return {
        "status": "IN_PROGRESS",
        "step_index": len(completed) + 1,
        "total_steps": len(QUESTION_PIPELINE),
        "progress_percent": pct,
        "progress_bar": make_progress_bar(pct),
        "field": q["field"],
        "category": q["category"],
        "title": q["title_zh"],
        "why_it_matters": q["why"],
        "prompts": {
            "zh": q["prompt_zh"],
            "en": q["prompt_en"],
            "de": q["prompt_de"]
        },
        "options": q["options"],
        "agent_instructions": (
            f"Ask the user this question conversationally. Attach the progress bar {make_progress_bar(pct)} {pct}%. "
            f"Do not mention code or script names. Save the answer with: "
            f"python3 scripts/user_profile.py set {'profile' if q['category'] in ('profile', 'tax_helper') else 'tax ' + str(y)} '<json>'"
        )
    }

def cmd_set(resource: str, patch: Dict, year: Optional[int] = None) -> Dict:
    _ensure_user_dir()
    y = year or date.today().year

    # Intelligent heuristics for user friendly inputs
    if resource == "profile":
        # Religion heuristic
        if "religion" in patch:
            rel = patch["religion"]
            if isinstance(rel, dict):
                denom = str(rel.get("denomination", "")).upper()
                if any(x in denom for x in ["NONE", "KEINE", "无", "NO", "WITHOUT"]):
                    patch["religion"]["church_tax_liable"] = False
                    patch["religion"]["denomination"] = "NONE"
                elif any(x in denom for x in ["CATHOLIC", "RÖM", "天主"]):
                    patch["religion"]["church_tax_liable"] = True
                    patch["religion"]["denomination"] = "ROMAN_CATHOLIC"
                elif any(x in denom for x in ["REFORM", "EVANG", "基督", "新教"]):
                    patch["religion"]["church_tax_liable"] = True
                    patch["religion"]["denomination"] = "REFORMED"

        # Canton uppercase
        if "address" in patch and isinstance(patch["address"], dict):
            if "canton" in patch["address"] and patch["address"]["canton"]:
                patch["address"]["canton"] = str(patch["address"]["canton"]).upper().strip()

        data = _load_json(PROFILE_PATH, default_profile)
        _deep_merge(data, patch)
        _save_json(PROFILE_PATH, data)

    elif resource == "tax":
        path = tax_data_path(y)
        data = _load_json(path, lambda: default_tax_data(y))

        # Commute heuristic with necessity and intra-city vs cross-city logic
        if "recurring" in patch and "commute_type" in patch["recurring"]:
            ctype = str(patch["recurring"]["commute_type"]).upper()
            prof = _load_json(PROFILE_PATH, default_profile)
            res_commune = str(_get_nested(prof, "address.commune") or "").strip().lower()
            work_commune = str(_get_nested(prof, "employment.work_commune") or "").strip().lower()

            if "deductions" not in patch or "s1_commute_chf" not in patch["deductions"]:
                if "GA" in ctype or "GENERAL" in ctype:
                    # Check if intra-commune (same city)
                    if res_commune and work_commune and res_commune == work_commune:
                        # Intra-commune: Only local network pass allowed (e.g. Libero/ZVV ~800 CHF)
                        patch.setdefault("deductions", {})["s1_commute_chf"] = 800
                    else:
                        # Cross-commune: Point-to-point Streckenabo reaches GA cost
                        patch.setdefault("deductions", {})["s1_commute_chf"] = 3995
                elif any(k in ctype for k in ["BIKE", "VELO", "WALK", "车", "步"]):
                    patch.setdefault("deductions", {})["s1_commute_chf"] = 700
                elif any(k in ctype for k in ["LOCAL", "市内", "同城", "NETZ"]):
                    patch.setdefault("deductions", {})["s1_commute_chf"] = 800

        # Lunch heuristic
        if "recurring" in patch and "lunch_type" in patch["recurring"]:
            ltype = str(patch["recurring"]["lunch_type"]).upper()
            if "CANTEEN" in ltype or "食堂" in ltype:
                patch.setdefault("deductions", {})["s2_meals_chf"] = 1600
            elif "RESTAURANT" in ltype or "外食" in ltype or "SELF" in ltype:
                patch.setdefault("deductions", {})["s2_meals_chf"] = 3200

        _deep_merge(data, patch)
        _save_json(path, data)

    _, pending, pct = get_onboarding_pipeline_state(y)
    return {
        "status": "saved",
        "progress_percent": pct,
        "progress_bar": make_progress_bar(pct),
        "is_ready_to_calculate": len(pending) == 0,
        "next_field": pending[0]["field"] if pending else None
    }

def cmd_get(resource: str, year: Optional[int] = None) -> Dict:
    _ensure_user_dir()
    if resource == "profile":
        return _load_json(PROFILE_PATH, default_profile)
    elif resource == "tax":
        y = year or date.today().year
        return _load_json(tax_data_path(y), lambda: default_tax_data(y))
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

    p_status = sub.add_parser("status", help="Check overall completeness and pipeline state")
    p_status.add_argument("year", nargs="?", type=int)

    p_next = sub.add_parser("next-question", help="Get the exact next question and progress bar for the LLM")
    p_next.add_argument("year", nargs="?", type=int)

    p_get = sub.add_parser("get", help="Read profile or tax data")
    p_get.add_argument("resource", choices=["profile", "tax"])
    p_get.add_argument("year", nargs="?", type=int)

    p_set = sub.add_parser("set", help="Write/merge into profile or tax data")
    p_set.add_argument("resource", choices=["profile", "tax"])
    p_set.add_argument("year_or_json")
    p_set.add_argument("json_data", nargs="?")

    p_rep = sub.add_parser("save-report", help="Save a generated report to user/reports/")
    p_rep.add_argument("year", type=int)
    p_rep.add_argument("report_type")
    p_rep.add_argument("content")

    args = parser.parse_args()

    if args.cmd == "status":
        result = cmd_status(args.year)
    elif args.cmd == "next-question":
        result = cmd_next_question(args.year)
    elif args.cmd == "get":
        result = cmd_get(args.resource, args.year)
    elif args.cmd == "set":
        if args.resource == "tax" and args.json_data:
            year = int(args.year_or_json)
            patch = json.loads(args.json_data)
            result = cmd_set("tax", patch, year)
        else:
            patch = json.loads(args.year_or_json)
            result = cmd_set(args.resource, patch)
    elif args.cmd == "save-report":
        result = cmd_save_report(args.year, args.report_type, args.content)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
