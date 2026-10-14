# Swiss Salary Certificate (Lohnausweis / Certificat de salaire) Mapping Guide

The Swiss standard salary certificate (Formular 11 / Certificat de salaire) follows a federally mandated numbered layout across all 26 cantons. This guide details how to extract and map each box into tax declarations.

---

## Field Breakdown & Tax Declaration Mapping

| Field # | German Label | French Label | Italian Label | Tax Declaration Mapping & Significance |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Lohn / Gehalt | Salaire | Salario | **Gross Employment Income** (Haupterwerbseinkommen). Basis for income tax before social deductions. |
| **2** | Gelegentliche Leistungen | Prestations occasionnelles | Prestazioni occasionali | Bonuses, 13th salary if separated, jubilee gifts, golden handshakes. Taxable. |
| **3** | Unregelmässige Leistungen | Prestations non périodiques | Prestazioni non periodiche | Irregular fringe benefits. Taxable. |
| **4** | Kapitalleistungen | Prestations en capital | Prestazioni in capitale | Severance pay or capital payments. Often taxed separately under special capital tariffs. |
| **5** | Beteiligungsrechte | Droits de participation | Diritti di partecipazione | Employee stock options / shares (Mitarbeiteraktien). Taxable valuation per circular 37. |
| **8** | Bruttolohn Total | Salaire brut total | Totale salario lordo | Total gross wage = sum of fields 1 to 7. |
| **9** | AHV/IV/EO/ALV/NBUV-Beiträge | Cotisations AVS/AI/APG/AC/AANP | Contributi AVS/AI/IPG/AD/AINP | 1st Pillar & mandatory social insurance contributions deducted at source. 100% tax exempt. |
| **10.1**| Ordentliche BVG-Beiträge | Cotisations ordinaires 2e pilier | Contributi ordinari LPP | **2nd Pillar Regular Contributions**. Tax-exempt; pre-deducted before net wage. |
| **10.2**| Einkauf 2. Säule | Rachat 2e pilier | Riscatto LPP | Voluntary 2nd pillar buy-in deducted via payroll. |
| **11** | Nettolohn | Salaire net | Salario netto | **Net Wage** = Field 8 minus (Field 9 + 10.1 + 10.2). This is the key baseline entered into tax software. |
| **12** | Quellensteuerabzug | Retenue de l'impôt à la source | Ritenuta d'imposta alla fonte | Withholding tax deducted if taxpayer is on B-permit. Important for NOV adjustment filing. |
| **13.1**| Reisespesen (effektiv) | Frais de déplacement | Spese di viaggio | Actual travel expenses reimbursed by employer. If checked, commuting cannot be fully re-claimed. |
| **13.2**| Verpflegungsspesen (effektiv)| Frais de repas | Spese di vitto | Actual meal expenses reimbursed by employer. If Box G is ticked, meal deduction is cut to CHF 1,600. |
| **14** | Weitere Gehaltsnebenleistungen| Autres prestations accessoires | Altre prestazioni accessorie | Additional fringe benefits, e.g. company phone, housing allowance. |
| **15** | Bemerkungen | Remarques | Osservazioni | **Crucial Audit Field**: Contains codes like company car percentage (Feld F) or free workstation note. |

---

## Field 15 Audit Triggers
1. **Letter F (Geschäftsauto / Véhicule de service)**:
   - If ticked, taxpayer has employer-provided car.
   - Commute deduction (S1 Fahrkosten) is **disallowed**; 0.9% of vehicle value per month is already added to income.
2. **Letter G (Kantine / Repas à prix réduit)**:
   - If ticked, employer provides subsidized lunches.
   - S2 Verpflegung deduction is legally reduced from standard CHF 3,200 to subsidized rate **CHF 1,600**.
3. **Desk Availability**:
   - If remarks indicate an office desk is available, S9 Home Office private rent deduction is disallowable under BGE 140 II 157.
