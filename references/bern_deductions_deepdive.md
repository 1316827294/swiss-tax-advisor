# Canton Bern 2025/2026 Tax Deductions Deep-Dive Specification

Based on the official **Canton Bern Tax Administration Guidelines** and [`bern_tax_deduction_template_2025_v3.xlsx`](file:///Users/liyunlong/Desktop/当前任务/项目/记账报税app/bern_tax_deduction_template_2025_v3.xlsx).

---

## 1. Key Official Rules & Formulas in Bern

### Dual-Earner Calculation Divergence (Zweitverdienerabzug)
- **Federal Direct Tax (Bund)**:
  $$\text{Deduction} = \min(\max(0.50 \times \text{Lower Spouse Net Income}, \text{CHF } 8'600), \text{CHF } 14'100)$$
  *(If lower spouse net income < CHF 8,600, deduction is capped at actual net income).*
- **Canton & Commune Bern (K/G)**:
  $$\text{Deduction} = 0.02 \times (\text{Spouse A Gross} + \text{Spouse B Gross}), \quad \text{Min CHF } 1'000, \text{ Max CHF } 2'600$$

### Low & Middle Income Automatic Relief (Minderbelastungsabzug)
- **Eligibility Benchmark**: Assessed automatically in TaxMe based on "Effective Income = Net Income + 10% of Taxable Net Wealth".
- **Thresholds (2025)**:
  - Single: Baseline CHF 16,700 (CHF 1,100 maximum relief).
  - Married: Baseline CHF 22,300 (CHF 2,200 maximum relief).
  - Child surcharge: + CHF 600 per child.
  - Taper: Decreases by CHF 100 for every CHF 2,000 above the baseline.

### Disability Costs (M9) vs. General Healthcare (S3)
- Under Bern tax practice, medical bills for non-disabled taxpayers must exceed **5% of net income** before producing tax relief.
- **Disability-related expenses (Behinderungsbedingte Kosten)** under StG BE Art. 38a are exempt from the 5% threshold: 100% of the patient-paid share is deductible from the first Swiss Franc.

---

## 2. Property Maintenance (Grundstückskosten) High-Impact Rules

1. **Photovoltaic & Solar (PV-Anlagen)**:
   - Beginning in 2024, investments in solar panels, battery storage, and smart EV charging infrastructure for private homes qualify as deductible maintenance.
   - **Loss Carryforward (Verlustverrechnung)**: If solar renovation costs exceed net taxable income in year 1, the surplus is carried over into **Tax Year 2 and Tax Year 3**.
2. **Renewal Fund (Erneuerungsfonds - M13)**:
   - For condominium owners (Stockwerkeigentum), regular annual payments into the building renewal fund are fully deductible in the contribution year, provided the fund is earmarked for future capital maintenance.
3. **Vacant Room Under-Utilization (Unternutzungsabzug - M15)**:
   - Only recognized for **Federal Direct Tax (Bund)**. Canton Bern does **not** grant Unternutzungsabzug for cantonal and communal taxes.

---

## 3. Official Caveats & Misconceptions (Häufige Irrtümer)

- ❌ **Auto Leasing**: Private car leasing installments are **strictly non-deductible** in Switzerland.
- ❌ **Tax Advisor / Software Fees**: Private tax preparation costs cannot be deducted as securities management fees (Depotgebühren).
- ❌ **Home Office Double-Dipping**: Claiming private home office rent prohibits claiming commute (S1) or meal allowances (S2) on the same telecommuting days.
- ❌ **Alimony to Adult Children**: Alimony payments to children age 18 and older are legally non-deductible under DBG Art. 33 Abs. 1 c.

---

## 4. Official Bern TaxInfo Reference Registry
- [Steuerabzüge Gesamtübersicht](https://www.sv.fin.be.ch/de/start/themen/steuererklaerung/steuerabzuege.html)
- [Abzüge 2025 auf einen Blick](https://www.taxinfo.sv.fin.be.ch/taxinfo/2bb9e996-54ad-4e0a-9406-07e67640081a)
- [Familienbesteuerung Merkblatt 12](https://www.sv.fin.be.ch/content/dam/sv_fin/dokumente/de/merkblaetter/einkommens_vermoegenssteuer/aktuelles_steuerjahr/mb12_ev_familienbesteuerung_de.pdf)
- [Grundstückkosten Merkblatt 05](https://www.sv.fin.be.ch/content/dam/sv_fin/dokumente/de/merkblaetter/einkommens_vermoegenssteuer/aktuelles_steuerjahr/mb05_ev_grundstueckkosten_de.pdf)
