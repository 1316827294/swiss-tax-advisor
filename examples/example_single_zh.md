# Example: Single Earner — Zurich (ZH)

This example shows a complete tax session for a single employee living in Zurich.

## Scenario

| Parameter | Value |
|---|---|
| Canton | ZH (Zürich) |
| Commune | Zürich |
| Gross Income | CHF 95,000 |
| Civil Status | Single |
| Children | 0 |
| Pillar 3a | CHF 7,258 (max) |
| Commute | CHF 3,300 (train, federal cap) |
| Meals | CHF 3,200 (standard) |

## Script Execution

```bash
python3 scripts/swiss_tax_math.py \
  --gross-income 95000 \
  --canton ZH \
  --commune "Zürich" \
  --civil-status SINGLE \
  --children 0 \
  --deductions '{"s4": 7258, "s1": 3300, "s2": 3200}' \
  --json
```

## Expected Output

```json
{
  "status": "success",
  "currency": "CHF",
  "canton": "ZH",
  "commune": "Zürich",
  "civil_status": "SINGLE",
  "children_count": 0,
  "gross_income_chf": 95000.0,
  "total_deductions_chf": 13758.0,
  "taxable_income_chf": 81242.0,
  "itemized_deductions_chf": {
    "s4": 7258.0,
    "s1": 3300.0,
    "s2": 3200.0
  },
  "federal_tax_chf": 1894.50,
  "cantonal_tax_chf": 3210.75,
  "communal_tax_chf": 3820.80,
  "church_tax_chf": 0.0,
  "wealth_tax_chf": 0.0,
  "total_tax_chf": 8926.05,
  "effective_tax_rate_pct": 9.40
}
```

## Marginal Rate Check

```bash
python3 scripts/marginal_rate_calc.py \
  --income 95000 \
  --canton ZH \
  --status SINGLE \
  --deduction 7258 \
  --category PILLAR_3A \
  --json
```

## Agent Prompt

> "Ich wohne in Zürich, bin ledig, verdiene 95'000 CHF brutto und habe bereits 7'258 CHF in die Säule 3a eingezahlt. Mein Arbeitsweg ist mit dem GA. Bitte erstelle mein Steuerdossier und zeige mir, wo ich noch optimieren kann."
