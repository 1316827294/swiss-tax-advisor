# Swiss Tax Advisor — Devin Instructions

## Project Overview

This is a sovereign Swiss tax advisor agent skill. It provides deterministic income tax calculations for all 26 Swiss cantons (tax year 2025/2026) via Python scripts that run entirely locally with no external dependencies.

## Environment Setup

```bash
# Requirements: Python 3.10+ (standard library only, no pip installs needed)
python3 --version   # Must be >= 3.10

# Verify all scripts work
python3 scripts/test_tax_engine.py
```

## Core Rule: No Mental Tax Math

The scripts in `scripts/` are the single source of truth for all numeric outputs. Run them via bash — never compute tax figures through reasoning alone.

## Key Script Interfaces

```bash
# Full tax assessment
python3 scripts/swiss_tax_math.py \
  --gross-income 95000 --canton BE --commune "Bern" \
  --civil-status SINGLE --children 0 \
  --deductions '{"s4": 7258, "s1": 3300, "s2": 3200}' --json

# Marginal rate analysis
python3 scripts/marginal_rate_calc.py \
  --income 95000 --canton ZH --status SINGLE \
  --deduction 7258 --category PILLAR_3A --json

# Dual-earner / marriage penalty
python3 scripts/family_marriage_sim.py \
  --earner-a 90000 --earner-b 70000 --canton VD --children 1 --json

# Audit risk score
python3 scripts/audit_risk_evaluator.py \
  --income 80000 --education 8000 --commute 4500 --sbb-zone --json

# Advanced advisories
python3 scripts/advanced_advisory.py nov --income 85000 --canton BE --deductions '{"s4": 7258}'
python3 scripts/advanced_advisory.py franchise --spend 1200
python3 scripts/advanced_advisory.py relocation --income 120000 --from-canton ZH --to-canton ZG
```

## Codebase Map

```
scripts/          ← Deterministic Python engines (modify only to update tax year constants)
references/       ← Knowledge base MDfiles (read-only reference)
templates/        ← Output report templates (edit to update formatting)
examples/         ← Real-world usage examples (read-only)
```

## Testing

```bash
python3 scripts/test_tax_engine.py
```
All tests must pass before any PR. If updating tax year constants, update test assertions accordingly.

## Privacy & Security
- No external API calls allowed from scripts
- AHV numbers must be masked in all outputs: `756.xxxx.xxxx.xx`
- IBANs must be masked: `CHxx **** **** **** xxxx x`
- Calculations are fully local and sovereign

## Output Language
Match user's language (DE/FR/IT/EN). Official tax submission letters must be in the canton's official language.
