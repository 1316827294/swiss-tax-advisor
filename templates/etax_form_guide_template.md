# Official eTax / TaxMe Form Filing Guide Template

> **Objective**: Guides the taxpayer step-by-step through the cantonal online filing software (TaxMe BE, eTax ZH, VaudTax, GeTax, FriTax) indicating exactly which number goes into which box.

---

## Guide for Canton `{CANTON}` ({CANTON_NAME}) - Online Tax Software

### Section A: Personal & Income (Haupterwerb / Salaires)
1. **Lohnausweis Einreichen / Salary Certificate Upload**:
   - Navigate to tab: **Einkünfte aus unselbständiger Erwerbstätigkeit / Salaires**.
   - Input Box 1 (Bruttolohn): Enter **`CHF {GROSS_INCOME_CHF}`**.
   - Input Box 11 (Nettolohn): Enter **`CHF {NET_WAGE_CHF}`**.
   - Input Box 10.1 (BVG): Verify matches **`CHF {PENSION_BVG_DEDUCTED_CHF}`**.

### Section B: Professional Expenses (Berufskosten / Frais professionnels)
2. **Fahrkosten (S1 Commute)**:
   - Navigate to: **Berufsauslagen -> Fahrkosten**.
   - Public transport ticket / GA: Select *Öffentlicher Verkehr* and enter **`CHF {S1_COMMUTE_CHF}`**.
3. **Auswärtige Verpflegung (S2 Meals)**:
   - Check Lohnausweis Box 13/G: If canteen subsidized, select *Mit Verbilligung* (**CHF 1,600**), otherwise select *Ohne Verbilligung* (**CHF 3,200**).
4. **Weiterbildung (S7 Continuing Education)**:
   - Enter course descriptions and total **`CHF {S7_EDUCATION_CHF}`**.
   - Upload employer confirmation letter.

### Section C: Deductions & Pension (Allgemeine Abzüge / Déductions générales)
5. **Säule 3a (S4 Tied Pension)**:
   - Navigate to: **Vorsorgebeiträge -> Säule 3a**.
   - Enter total paid into 3a: **`CHF {S4_3A_CHF}`** (Max statutory cap: CHF 7,258).
   - Attach official Bank/Insurance tax certificate.
6. **Krankheitskosten (S3 Healthcare)**:
   - Navigate to: **Krankheits- und Unfallkosten**.
   - Enter total out-of-pocket medical bills: **`CHF {S3_HEALTH_CHF}`**. System will automatically subtract the 5% net income threshold.
7. **Drittbetreuungskosten (S6 Childcare)**:
   - Enter Kita/Daycare total: **`CHF {S6_CHILDCARE_CHF}`**. Attach payment receipts.
8. **Schuldzinsen & Depotgebühren (S10/S11)**:
   - Enter mortgage/loan interest: **`CHF {S11_INTEREST_CHF}`**.
   - Enter securities custody fee: **`CHF {S10_CUSTODY_CHF}`**.

### Section D: Bank Accounts & Wealth (Wertschriftenverzeichnis / Fortune)
9. **Bankkonten & Wertschriften**:
   - List each IBAN, balance at 31.12 (`{TAX_YEAR}`), and gross interest earned.
