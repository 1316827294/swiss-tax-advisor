# 🇨🇭 Swiss Tax Advisor — Antigravity Agent Skill

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Skill Format](https://img.shields.io/badge/format-Antigravity%20Skill-green.svg)](https://antigravity.dev/docs/skills)

An **open-source, sovereign, and deterministic Agent Skill** for Swiss personal and family income tax filing, cantonal audit-risk pre-checking, and proactive tax-saving advisory — usable with [Antigravity (AGY)](https://antigravity.dev).

> **Sovereign by design**: All tax calculations run locally via deterministic Python scripts. No financial data is ever sent to a third-party endpoint.

---

## ✨ Features

| Capability | Details |
|---|---|
| 🧮 **Deterministic Tax Engine** | Federal IFD/DBG + cantonal + communal + wealth tax across all 26 cantons, 5-Rappen precision |
| 📄 **Document Parsing** | Lohnausweis (boxes 1–15), bank statements (CAMT.053), receipts → deduction codes S1–S23 |
| 🛡️ **Audit Risk Radar** | Cantonal pre-audit safety score (0–100) before submission |
| 💰 **Tax-Saving Advisory** | Pillar 3a gap, dual-earner deduction, healthcare franchise optimizer, Quellensteuer NOV |
| 📝 **Official Deliverables** | Steuerdossier, eTax step-by-step guide, Fristerstreckung letter |
| 🌐 **Multilingual** | DE / FR / IT / EN auto-detection; official letters in canton's language |
| 🔒 **Privacy (DSG/FADP)** | AHV and IBAN auto-masking in all summaries |

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

---

## 💬 Using via Antigravity Agent

Once installed, simply ask the agent naturally:

- *"Help me file my Swiss taxes for 2025. I live in Bern, earn 95,000 CHF, and have a Lohnausweis."*
- *"What's my marginal tax rate and how much would I save by maximizing Pillar 3a?"*
- *"Run an audit risk check on my deductions before I submit."*
- *"My B-permit employer deducts Quellensteuer — should I file a NOV correction?"*
- *"Compare my tax if I move from Zurich to Zug."*

See the [`examples/`](./examples/) directory for complete end-to-end session examples.

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
