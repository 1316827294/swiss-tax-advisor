# 🇨🇭 Swiss Tax Advisor — Open-Source AI Tax Skill

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-platform-compatibility-matrix)

An **open-source, sovereign, and deterministic AI Agent Skill** for Swiss personal and family income tax filing, cantonal audit-risk pre-checking, and proactive tax-saving advisory. Compatible with **Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Aider, Devin, and Google Antigravity**.

> **Sovereign by design**: All tax calculations and user profiles run locally via deterministic Python scripts. No financial data is ever sent to external cloud tax services.

---

## ✨ Features

| Capability | Details |
|---|---|
| 🧮 **Deterministic Tax Engine** | Federal IFD/DBG + cantonal + communal + wealth tax across all 26 cantons, 5-Rappen precision |
| 📁 **Document Auto-Ingestion** | Drop Lohnausweis (boxes 1–15), Pillar 3a, or bank statements into `./documents/` for instant auto-filling |
| 💰 **Live Tax Dashboard & Hot-Edit** | Real-time tax countdown badge; instantly displays exact CHF savings when amounts are updated |
| 🛡️ **Audit Risk Radar** | Cantonal pre-audit safety score (0–100) before submission |
| 💡 **Tax-Saving Advisory** | Pillar 3a gap, dual-earner deduction, healthcare franchise optimizer, Quellensteuer NOV |
| 📋 **Canton eTax Filling Guides** | Box-by-box filing instructions for official portals (TaxMe, eTax.zh, VaudTax, GeTax) |
| 📝 **Official Deliverables** | Steuerdossier, eTax step-by-step guide, Fristerstreckung letter |
| 🌐 **Multilingual** | DE / FR / IT / EN / ZH auto-detection; official letters in canton's language |
| 🔒 **Privacy (DSG/FADP)** | 100% local in `./user/`; AHV and IBAN auto-masking in all summaries |

---

## ⚡ Quick Start — 3 Steps, 30 Seconds

### Step 1 — Install (pick your AI platform)

```bash
# Antigravity (global)
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash

# Claude Code / Cursor / Cline / Windsurf (run inside your project directory)
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform claude
```

### Step 2 — Ask your AI

> *"Help me with my Swiss taxes. I'm single, live in Bern, earn 95,000 CHF, and paid 7,258 CHF into Pillar 3a."*

That's it. The AI reads the instructions automatically and runs the calculation engine.

### Step 3 — Get your results

The AI immediately returns your full tax breakdown, audit risk score, and a proactive tax-saving plan. [See a real example ↓](#-what-does-the-ai-actually-do--real-session-example)

---

## 🚀 Installation

> **For AI agents**: You can ask your AI assistant to install this skill by saying:
> *"Install the swiss-tax-advisor skill from https://github.com/1316827294/swiss-tax-advisor for [your platform]"*
> The AI can run the one-line command below on your behalf.

Pick your platform:

### 🟣 Antigravity (AGY) — Global install

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash
```

Installs to `~/.gemini/config/skills/swiss-tax-advisor/`. Restart AGY — the skill appears automatically.

---

### 🟠 Claude Code — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform claude
```

Copies `CLAUDE.md` to your project root + `swiss-tax-advisor/scripts/` and `references/`. Claude Code reads `CLAUDE.md` automatically from the project root.

---

### 🔵 Cursor — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform cursor
```

Copies `.cursor/rules/swiss-tax-advisor.mdc` + scripts. Cursor reads `.cursor/rules/` automatically.

---

### 🟢 Cline (VSCode) — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform cline
```

Copies `.clinerules` to your project root + scripts. Cline reads `.clinerules` automatically.

---

### 🩵 Windsurf (Codeium) — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform windsurf
```

Copies `.windsurfrules` to your project root + scripts. Windsurf reads `.windsurfrules` automatically.

---

### ⚫ GitHub Copilot — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform copilot
```

Copies `.github/copilot-instructions.md` + scripts. Copilot Workspace reads it automatically.
> ⚠️ GitHub Copilot Chat cannot execute terminal commands — use it for guidance, then run scripts manually.

---

### 🟡 Aider — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform aider
```

Then run aider with: `aider --conventions CONVENTIONS.md`

---

### 🔴 Devin — Project install

Run this **inside your project directory**:

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform devin
```

Copies `DEVIN.md` + scripts. Devin reads `DEVIN.md` from the project root.

---

### Install for ALL platforms at once

```bash
curl -fsSL https://raw.githubusercontent.com/1316827294/swiss-tax-advisor/main/install.sh | bash -s -- --platform all
```

---

### Manual install (any platform)

```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
```

Then copy the relevant file(s) manually:

| Platform | File to copy | Destination |
|---|---|---|
| Antigravity | entire repo | `~/.gemini/config/skills/swiss-tax-advisor/` |
| Claude Code | `CLAUDE.md` + `scripts/` + `references/` | project root |
| Cursor | `.cursor/rules/swiss-tax-advisor.mdc` + `scripts/` | project root |
| Cline | `.clinerules` + `scripts/` | project root |
| Windsurf | `.windsurfrules` + `scripts/` | project root |
| Copilot | `.github/copilot-instructions.md` + `scripts/` | project root |
| Aider | `CONVENTIONS.md` + `scripts/` | project root |
| Devin | `DEVIN.md` + `scripts/` | project root |

---

## 🤖 Platform Capability Comparison

Not all AI platforms can run terminal commands. Know what to expect:

| Platform | Auto-reads instructions? | Can execute scripts? | Delivers full output? |
|---|---|---|---|
| **Antigravity (AGY)** | ✅ Automatic (SKILL.md) | ✅ Yes — bash tool | ✅ Full: dossier + tax report |
| **Claude Code** | ✅ Automatic (CLAUDE.md) | ✅ Yes — bash tool | ✅ Full |
| **Cursor** | ✅ Automatic (.cursor/rules/) | ✅ Yes — terminal | ✅ Full |
| **Cline (VSCode)** | ✅ Automatic (.clinerules) | ✅ Yes — bash tool | ✅ Full |
| **Windsurf** | ✅ Automatic (.windsurfrules) | ✅ Yes — terminal | ✅ Full |
| **Devin** | ✅ Automatic (DEVIN.md) | ✅ Yes — sandbox bash | ✅ Full |
| **Aider** | ✅ With `--conventions` flag | ✅ Yes — shell | ✅ Full |
| **GitHub Copilot** | ✅ Automatic (copilot-instructions) | ❌ No bash capability | ⚠️ Guidance only — run scripts manually |

> **Bottom line**: If your AI platform can open a terminal, it can run the tax scripts and give you precise CHF figures. If not (Copilot Chat), it will guide you on what to run.

---

## 📦 Repository Structure

```text
swiss-tax-advisor/
├── SKILL.md                        # Agent instructions (frontmatter + workflow)
├── README.md                       # This file
├── LICENSE                         # Apache 2.0
├── install.sh                      # One-line install script
│
├── scripts/                        # Deterministic Python calculation engines
│   ├── swiss_tax_math.py           # Main tax engine (IFD + cantonal + communal)
│   ├── marginal_rate_calc.py       # Marginal rate & deduction leverage calculator
│   ├── family_marriage_sim.py      # Marriage penalty / dual-earner simulator
│   ├── audit_risk_evaluator.py     # Cantonal audit risk radar (score 0–100)
│   ├── advanced_advisory.py        # NOV / franchise / relocation advisors
│   └── test_tax_engine.py          # Test suite
│
├── references/                     # Knowledge base (loaded on demand)
│   ├── deduction_taxonomy.md       # Full deduction codes S1–S23 / M1–M16
│   ├── lohnausweis_mapping.md      # Salary certificate box mapping
│   ├── bank_statement_mapping.md   # CAMT.053 / bank statement ingestion
│   ├── cantonal_caps_2025_2026.md  # Per-canton caps & deadlines
│   ├── bern_deductions_deepdive.md # Canton Bern detailed rules
│   ├── quellensteuer_nov_guide.md  # B-permit ordinary filing guide
│   ├── health_franchise_opt.md     # CHF 300 vs 2500 franchise optimizer
│   ├── audit_risk_criteria.md      # Cantonal audit trigger criteria
│   ├── tax_saving_playbook.md      # Proactive savings playbook
│   └── i18n_tax_glossary.md        # 6-language tax terminology dictionary
│
├── templates/                      # Output report templates
│   ├── steuerdossier_template.md
│   ├── etax_form_guide_template.md
│   ├── tax_saving_report_template.md
│   └── fristerstreckung_template.txt
│
└── examples/                       # Real-world usage examples
    ├── example_single_zh.md        # Single earner, Zurich
    ├── example_married_be.md       # Married dual-earner, Bern
    └── example_quellensteuer.md    # B-permit Quellensteuer NOV filing
```

---

## 🛠️ Using the Scripts Directly

All scripts require **Python 3.10+** and only use the standard library (no pip dependencies).

### Calculate your tax

```bash
python3 scripts/swiss_tax_math.py \
  --gross-income 95000 \
  --canton BE \
  --commune "Bern" \
  --civil-status SINGLE \
  --children 0 \
  --deductions '{"s4": 7258, "s1": 3300, "s2": 3200}' \
  --json
```

### Check marginal rate & deduction savings

```bash
python3 scripts/marginal_rate_calc.py \
  --income 95000 \
  --canton ZH \
  --status SINGLE \
  --deduction 7258 \
  --category PILLAR_3A \
  --json
```

### Run audit risk radar

```bash
python3 scripts/audit_risk_evaluator.py \
  --income 80000 \
  --education 8000 \
  --commute 4500 \
  --sbb-zone \
  --json
```

### Marriage penalty / dual-earner simulator

```bash
python3 scripts/family_marriage_sim.py \
  --earner-a 90000 \
  --earner-b 70000 \
  --canton VD \
  --children 1 \
  --json
```

### Advanced advisory (NOV / franchise / relocation)

```bash
# Quellensteuer NOV decision
python3 scripts/advanced_advisory.py nov --income 85000 --canton BE --deductions '{"s4": 7258}'

# Health franchise optimizer (300 vs 2500 CHF)
python3 scripts/advanced_advisory.py franchise --spend 1200

# Cross-canton relocation comparison
python3 scripts/advanced_advisory.py relocation --income 120000 --from-canton ZH --to-canton ZG
```

#### 🗺️ What do these three advisors do?

**`nov` — Quellensteuer Ordinary Filing Decision (B/L-permit holders)**

If you work in Switzerland on a B or L permit, your employer withholds a flat tax called *Quellensteuer* at source. You may optionally file an *Nachträgliche Ordentliche Veranlagung* (NOV) — switching to standard tax filing — to claim deductions like Pillar 3a that are not accessible under Quellensteuer. The script calculates whether an NOV would save or *cost* you money, accounting for your canton's Steuerfuss. **This decision is often irreversible**, so the script also issues an irrevocability warning.

**`franchise` — Health Insurance Deductible Optimizer (CHF 300 vs CHF 2,500)**

Swiss mandatory health insurance (Grundversicherung) lets you choose an annual deductible (Franchise) of CHF 300 to CHF 2,500. A higher franchise means lower monthly premiums but higher out-of-pocket costs when you need care. The script calculates the **break-even medical spending level** for your situation and tells you which franchise saves you more money annually.

**`relocation` — Cross-Canton Tax Comparison**

Switzerland's 26 cantons have dramatically different tax rates — moving from Zurich to Zug can save tens of thousands of CHF per year. The script computes your exact tax liability in two cantons and returns the **annual CHF difference**, so you can make a data-driven relocation decision.

---

## 💬 Using via Antigravity Agent

Once installed, simply ask the agent naturally:

- *"Help me file my Swiss taxes for 2025. I live in Bern, earn 95,000 CHF, and have a Lohnausweis."*
- *"What's my marginal tax rate and how much would I save by maximizing Pillar 3a?"*
- *"Run an audit risk check on my deductions before I submit."*
- *"My B-permit employer deducts Quellensteuer — should I file a NOV correction?"*
- *"Compare my tax if I move from Zurich to Zug."*
- *"我在伯尔尼工作，年收入9.5万法郎，帮我报税"* *(Chinese works too)*

See the [`examples/`](./examples/) directory for complete end-to-end session examples.

---

## 🎬 What does the AI actually do? — Real Session Example

**User asks:**
> *"I'm single, live in Bern, earn CHF 95,000 gross. I paid CHF 7,258 into Pillar 3a, commute by GA (CHF 3,300), and have standard meal deduction (CHF 3,200). What's my tax and how much did Pillar 3a save me?"*

**AI runs these scripts automatically:**
```bash
python3 scripts/swiss_tax_math.py \
  --gross-income 95000 --canton BE --commune "Bern" \
  --civil-status SINGLE --children 0 \
  --deductions '{"s4": 7258, "s1": 3300, "s2": 3200}' --json

python3 scripts/marginal_rate_calc.py \
  --income 95000 --canton BE --status SINGLE \
  --deduction 7258 --category PILLAR_3A --json

python3 scripts/audit_risk_evaluator.py \
  --income 95000 --education 0 --commute 3300 --json
```

**AI delivers — Tax Assessment (BE — Bern, 2025):**

| | CHF |
|---|---:|
| Gross Income | 95,000.00 |
| Total Deductions | −13,758.00 |
| **Taxable Income** | **81,242.00** |
| Federal Direct Tax | 1,636.00 |
| Cantonal Tax (BE) | 9,733.05 |
| Communal Tax (Bern) | 4,898.30 |
| **Total Tax Payable** | **16,267.35** |
| **Effective Rate** | **17.12%** |

**Pillar 3a Savings:**
> Your marginal rate in BE is **36.5%**. Your CHF 7,258 Pillar 3a contribution saved you **CHF 2,649.20** in taxes this year. You have already maxed the statutory cap — no additional gap to fill.

**Audit Risk Radar:**
> ✅ **Score: 100/100 — LOW RISK.** All deductions are within cantonal safe-harbour limits. Safe to file.

**Proactive Tax-Saving Tips:**
1. ✅ Pillar 3a fully maxed (CHF 7,258)
2. 💡 Health franchise: if your annual medical bills are under CHF 1,011, switching to the CHF 2,500 franchise saves you **CHF 750/year**
3. 💡 Considering relocation? Moving from BE to ZG on CHF 95,000 would save you roughly **CHF 7,000–9,000/year** in taxes

**AI then generates (using `templates/`):**
- 📄 `Steuerdossier_2025_Bern.md` — complete tax archive
- 📋 `eTax_Guide_Bern.md` — box-by-box eTax software guide
- 💰 `Tax_Saving_Report.md` — personalised optimisation plan
- 📩 `Fristerstreckung.txt` — deadline extension letter (if needed)

---

## ❓ FAQ

**Q: Are the CHF numbers accurate?**
> The scripts implement the official federal progressive tariff (DBG Art. 36) and canton-specific Steuerfuss multipliers for all 26 cantons. Statutory caps (Pillar 3a, commute, childcare) match official 2025/2026 published limits. Always verify final amounts with your cantonal tax office before filing — this tool is for planning and decision-making.

**Q: Is my financial data uploaded anywhere?**
> No. Everything runs 100% locally via Python scripts on your own machine. No income or deduction data is ever sent to any external server or API.

**Q: Which tax years are supported?**
> **2025** (return due 2026) and **2026**. For older years, statutory deduction caps may differ — check `references/cantonal_caps_2025_2026.md`.

**Q: Can I ask in German, French, or Italian?**
> Yes. The skill auto-detects your language (DE / FR / IT / EN / ZH) and replies in kind. Official submission letters are generated in your canton's official language automatically.

**Q: Does it support self-employed (Selbstständigerwerbende)?**
> Yes. The Pillar 3a cap for self-employed is CHF 36,288 (vs CHF 7,258 for employees). Mention "self-employed" to the AI, or pass `--deductions '{"s4": 36288}'`. Full S10–S23 business expense codes are in `references/deduction_taxonomy.md`.

**Q: What about wealth tax?**
> Pass `--net-wealth 250000` to `swiss_tax_math.py`. Wealth tax is calculated at ~0.25% on net assets above the CHF 100,000 exemption threshold (cantonal variation applies).

**Q: I'm on a B-permit — should I file a NOV?**
> Run `python3 scripts/advanced_advisory.py nov ...` or just ask the AI. It compares your Quellensteuer already withheld vs. your ordinary tax liability and gives a clear RECOMMEND / NOT RECOMMENDED verdict with the exact CHF difference. See the [Quellensteuer example](./examples/example_quellensteuer.md).

**Q: Why "deterministic"? Why not just let the AI estimate?**
> Swiss cantonal taxes are non-linear and depend on canton-specific Steuerfuss multipliers, communal factors, and 5-Rappen rounding rules. LLMs cannot reliably reproduce these calculations — they hallucinate percentages. The Python scripts are the single source of truth: they always return the same output for the same input.

---

## 🌐 Supported Cantons

All 26 Swiss cantons: **ZH, BE, LU, UR, SZ, OW, NW, GL, ZG, FR, SO, BS, BL, SH, AR, AI, SG, GR, AG, TG, TI, VD, VS, NE, GE, JU**

Tax year: **2025 / 2026**

---

## 🤝 Contributing

Contributions are welcome! To add a canton's precise tariff table, fix a deduction cap, or improve a reference document:

1. Fork the repo
2. Create a branch: `git checkout -b fix/canton-ge-tariff`
3. Make your changes with sources cited (official cantonal tax office links)
4. Open a Pull Request

Please keep all calculation logic deterministic and cite the legal basis (DBG article, cantonal Steuergesetz).

---

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

This skill is for **informational and planning purposes only**. For complex situations, always consult a licensed Swiss tax advisor (Treuhänder / Conseiller fiscal). Tax laws change annually — verify caps and rates against official cantonal sources before filing.
