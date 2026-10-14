# Swiss Withholding Tax Ordinary Assessment Guide (Quellensteuer NOV Guide)

For foreign employees residing in Switzerland holding a B permit (or L permit), taxes are automatically deducted monthly at source (**Quellensteuer** / **Impôt à la source**).

Since the 2021 tax reform, taxpayers have the right to request a **Subsequent Ordinary Assessment (Nachträgliche ordentliche Veranlagung - NOV)**.

---

## 1. How NOV Works

1. Under standard Quellensteuer, taxes are levied based on flat cantonal tariff tables (Tarif A for singles, Tarif B for married sole-earners, Tarif C for dual earners). These tables include a standardized flat assumption for professional expenses and insurance.
2. **The Opportunity**: If you contribute significantly to **Pillar 3a (CHF 7,258)**, pay high third-party childcare (Kita), or pay for job-related continuing education (S7), these itemized deductions are **not** credited in the basic Quellensteuer table.
3. By applying for NOV before the strict deadline (**March 31** of the following tax year), you file a full Swiss tax return (Steuererklärung) claiming all itemized deductions, potentially triggering refunds of **CHF 1,000 to CHF 3,500+**.

---

## 2. ⚠️ The Irrevocable Risk Trap (Die NOV-Falle)

Applying for NOV carries severe structural implications that every taxpayer must understand:

1. **Irrevocability (Einmal beantragt, immer ordentlich)**:
   - Once an NOV application is granted, **you cannot revert to standard Quellensteuer in subsequent tax years**.
   - You are legally mandated to submit an ordinary tax return every single year until you depart Switzerland.
2. **Local Commune Surcharge Risk (Gemeindesteuerfuss)**:
   - Quellensteuer is calculated using a canton-wide weighted average multiplier.
   - If you live in a municipality with an above-average tax multiplier (e.g. higher-tax communes in Bern, Valais, or Jura), ordinary tax liability may be **higher** than what your employer withheld!
   - If your additional deductions do not exceed the local commune tax premium, **you will receive an unexpected tax bill (Nachzahlung) instead of a refund**.
3. **Wealth Tax Inclusion**:
   - Under standard Quellensteuer, worldwide wealth (assets, bank savings, real estate abroad) is often untaxed if below cantonal wealth thresholds.
   - In ordinary taxation (NOV), your worldwide net wealth is subject to Cantonal/Communal wealth tax.

---

## 3. Decision Matrix: Should You Apply for NOV?

Run the deterministic evaluation command:
```bash
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 120000 \
  --canton ZH \
  --commune "Zürich" \
  --deductions '{"s4": 7258, "s1": 3300, "s6": 12000}'
```

- ✅ **APPLY FOR NOV IF**:
  - You maxed out Pillar 3a (CHF 7,258) AND pay high childcare (Kita > CHF 5,000) or voluntary 2nd pillar buy-ins.
  - You live in a low-tax municipality (e.g. Zug, Schwyz, or low-tax communes in Zurich).
  - Your simulated refund exceeds CHF 800.
- 🛑 **DO NOT APPLY FOR NOV IF**:
  - You have zero or minimal Pillar 3a contributions.
  - You live in a high-multiplier municipality.
  - You possess substantial offshore assets that would trigger high Swiss wealth tax.
