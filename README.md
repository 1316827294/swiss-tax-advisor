# 🇨🇭 Swiss Tax Advisor (`swiss-tax-advisor`)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [简体中文](README.zh.md)

---

> **Open-Source Sovereign Agent Skill for Swiss Tax Filing, Pre-Audit Risk Radar & Proactive Tax Optimization.**  
> Built for **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor**, and **OpenClaw**.

---

## 🚀 Key Capabilities

1. **Zero External Dependencies**: Pure Python 3.10+ standard library (`math`, `argparse`, `json`, `sys`, `unittest`). No `pip install` required.
2. **Deterministic 5-Rappen Precision**: Hard-gate design preventing LLM mental math hallucinations on Swiss progressive cantonal tax tables.
3. **Cantonal Audit Risk Pre-Check Radar (0–100 Score)**: Simulates cantonal tax administration heuristic screening (*Risikobasierte Fallauswahl*) to eliminate audit red-flags before filing.
4. **Native Six-Language Architecture**: Full documentation and prompt templates available in **English**, **German**, **French**, **Italian**, **Spanish**, and **Chinese**. Output dynamically adapts to your inquiry language.
5. **Full S1–S12 & Canton Bern 2025/2026 Taxonomy**: Built-in statutory caps, legal citations (DBG, StHG, StG BE), and specialized provisions (Photovoltaic 2-year carryforward, Erneuerungsfonds, disability costs with zero hurdle, and dual-earner deduction).
6. **Advanced Decision Engines**:
   - **Quellensteuer NOV Evaluator**: B-permit withholding tax vs. ordinary declaration risk/benefit decision.
   - **Health Insurance Franchise Optimizer**: Actuarial break-even calculation for Franchise 300 vs. 2500.
   - **Relocation What-If Simulator**: Cross-canton tax multiplier (Steuerfuss) financial comparison.

---

## 📁 Repository Structure

```text
skills/swiss-tax-advisor/
├── SKILL.md                          # Master Agent Skill Specification (Workflow & Gate Rules)
├── README.md                         # Main Documentation (English)
├── README.de.md                      # Deutsche Dokumentation
├── README.fr.md                      # Documentation française
├── README.it.md                      # Documentazione italiana
├── README.es.md                      # Documentación en español
├── README.zh.md                      # 中文完整说明文档
├── LICENSE                           # MIT License
├── .gitignore                        # Python cache artifact filter
├── references/                       # Statutory Knowledge Base
│   ├── deduction_taxonomy.md         # S1~S12 deductions & Swiss DBG/StHG legal bases
│   ├── cantonal_caps_2025_2026.md    # 26 cantonal caps, marginal rates & deadlines
│   ├── lohnausweis_mapping.md        # Salary certificate 15-box extraction guide
│   ├── audit_risk_criteria.md        # Official cantonal audit screening heuristics
│   ├── tax_saving_playbook.md        # Actionable Swiss tax-saving strategies
│   ├── bern_deductions_deepdive.md   # Canton Bern 2025/2026 detailed rules & TaxInfo links
│   ├── quellensteuer_nov_guide.md    # Withholding tax ordinary filing (NOV) decision guide
│   ├── health_franchise_opt.md       # Health insurance deductible (300 vs 2500) optimizer
│   ├── bank_statement_mapping.md     # Swiss bank (UBS, PostFinance, TWINT, CAMT.053) ingestion
│   └── i18n_tax_glossary.md          # 6-language synchronized tax terminology dictionary
├── scripts/                          # Deterministic Offline Math Engines
│   ├── swiss_tax_math.py             # Federal/Cantonal/Communal/Wealth tax engine
│   ├── marginal_rate_calc.py         # Marginal tax rate & direct cash savings calculator
│   ├── family_marriage_sim.py        # Dual-earner deduction & marriage penalty simulator
│   ├── audit_risk_evaluator.py       # Pre-check audit risk scorer (0-100 radar)
│   ├── advanced_advisory.py          # NOV evaluator, franchise optimizer & relocation simulator
│   └── test_tax_engine.py            # Comprehensive offline unit & integration test suite (12 tests)
└── templates/                        # Multilingual Official Report Templates
    ├── steuerdossier_template.md     # Annual Tax Dossier / Steuerdossier / Dossier fiscal
    ├── etax_form_guide_template.md   # Official online tax software step-by-step form guide
    ├── tax_saving_report_template.md # Quantified actionable tax-saving playbook
    └── fristerstreckung_template.txt # Official deadline extension letter (DE/FR/IT)
```

---

## ⚡ Quickstart & Testing

Run the offline test suite:
```bash
python3 skills/swiss-tax-advisor/scripts/test_tax_engine.py
```
*(Expected: `Ran 12 tests in 0.001s, OK`)*

### CLI Command Examples

```bash
# 1. Calculate Swiss Taxes (Bern, Married, Gross 170k, with 3a and Kita deductions)
python3 skills/swiss-tax-advisor/scripts/swiss_tax_math.py \
  --gross-income 170000 --canton BE --civil-status MARRIED --children 1 \
  --deductions '{"s1": 3300, "s4": 7258, "s6": 18000}' --json

# 2. Check Marginal Tax Rate & Pillar 3a Cash Savings
python3 skills/swiss-tax-advisor/scripts/marginal_rate_calc.py \
  --income 120000 --canton ZH --deduction 7258 --category PILLAR_3A --json

# 3. Simulate Dual-Earner Marriage Tax Impact (Penalty vs. Bonus)
python3 skills/swiss-tax-advisor/scripts/family_marriage_sim.py \
  --earner-a 110000 --earner-b 75000 --canton BE --children 1 --json

# 4. Run Audit Pre-Check Radar
python3 skills/swiss-tax-advisor/scripts/audit_risk_evaluator.py \
  --income 85000 --education 15000 --missing-proofs --json

# 5. Evaluate Quellensteuer NOV Application
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 110000 --canton ZH --deductions '{"s4": 7258, "s1": 3300}'

# 6. Optimize Health Insurance Franchise
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py franchise \
  --spend 1400 --premium-300 450 --premium-2500 310

# 7. Compare Relocation Across Cantons
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py relocation \
  --income 150000 --from-canton BE --to-canton ZG
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
