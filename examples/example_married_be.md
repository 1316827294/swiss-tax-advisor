# Example: Married Dual-Earner — Bern (BE)

This example shows a dual-earner married couple in Bern, including marriage penalty simulation and Pillar 3a optimization.

## Scenario

| Parameter | Value |
|---|---|
| Canton | BE (Bern) |
| Commune | Bern |
| Earner A Income | CHF 110,000 |
| Earner B Income | CHF 75,000 |
| Civil Status | Married |
| Children | 2 |
| Earner A Pillar 3a | CHF 7,258 |
| Childcare (KITA) | CHF 18,000 |

## Step 1 — Marriage Penalty Simulation

```bash
python3 scripts/family_marriage_sim.py \
  --earner-a 110000 \
  --earner-b 75000 \
  --canton BE \
  --children 2 \
  --json
```

## Step 2 — Full Tax Calculation

```bash
python3 scripts/swiss_tax_math.py \
  --gross-income 185000 \
  --canton BE \
  --commune "Bern" \
  --civil-status MARRIED \
  --children 2 \
  --deductions '{"s4": 7258, "s6": 18000, "s1": 3300, "s2": 3200}' \
  --json
```

## Step 3 — Audit Risk Check

```bash
python3 scripts/audit_risk_evaluator.py \
  --income 185000 \
  --education 0 \
  --commute 3300 \
  --missing-proofs \
  --json
```

## Agent Prompt

> "Wir sind verheiratet, wohnen in Bern und verdienen zusammen 185'000 CHF. Wir haben 2 Kinder und zahlen 18'000 CHF für die Kita. Kannst du unsere Steuerlast berechnen, die Heiratsstrafe prüfen und unsere Säule-3a-Lücken aufzeigen?"
