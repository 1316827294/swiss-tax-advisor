# Swiss Tax Advisor — Aider Conventions

## Critical Convention: Always Execute Scripts for Tax Math

This project contains deterministic Python tax calculation engines in `scripts/`. Swiss tax calculations require non-linear progressive tariffs and 5-Rappen rounding — mental arithmetic or LLM-guessed percentages are NEVER acceptable.

**Convention**: Before reporting any tax figure, run the relevant script and cite the exact JSON output.

## Script Execution Patterns

```bash
# Standard full tax run
python3 scripts/swiss_tax_math.py --gross-income 95000 --canton BE --commune "Bern" \
  --civil-status SINGLE --children 0 --deductions '{"s4": 7258}' --json

# Quick marginal rate
python3 scripts/marginal_rate_calc.py --income 95000 --canton ZH --status SINGLE \
  --deduction 7258 --category PILLAR_3A --json

# Run test suite to verify engine correctness
python3 scripts/test_tax_engine.py
```

## Code Modification Conventions

- All tax rate constants live in `scripts/swiss_tax_math.py` (STATUTORY_LIMITS_RAPPEN, CANTON_26_CONFIG)
- When updating rates for a new tax year, update the constants at the top of `swiss_tax_math.py` only
- Rounding: always use `round_to_5_rappen()` — never use Python's built-in `round()` for tax figures
- Output: always return dict with `status`, `currency`, and itemized breakdown fields

## Reference Files
- Deduction codes: `references/deduction_taxonomy.md`
- Canton caps: `references/cantonal_caps_2025_2026.md`
- Lohnausweis: `references/lohnausweis_mapping.md`

## Privacy
Never output raw AHV numbers or IBANs — always mask them.
