# Steuerdossier / Dossier Fiscal / Tax Dossier Template

> **Language Notice**: Render this template in the taxpayer's inquiry language:
> - German: `Steuerdossier {TAX_YEAR} (Kanton {CANTON})`
> - French: `Dossier fiscal {TAX_YEAR} (Canton {CANTON})`
> - Italian: `Dossier fiscale {TAX_YEAR} (Cantone {CANTON})`
> - English: `Tax Dossier {TAX_YEAR} (Canton {CANTON})`

---

## 1. Steuerpflichtige Person / Taxpayer Profile
- **Name / Full Name**: `{TAXPAYER_NAME}`
- **Zivilstand / État civil / Marital Status**: `{MARITAL_STATUS}`
- **Steuerjahr / Année fiscale / Tax Year**: `{TAX_YEAR}`
- **Wohnkanton / Canton de domicile**: `{CANTON}` (`{COMMUNE}`)
- **Kinder / Enfants / Children**: `{CHILDREN_COUNT}`
- **Konfession / Confession / Church Affiliation**: `{CHURCH_AFFILIATION}`
- **Erstellungsdatum / Date of Generation**: `{GENERATION_TIMESTAMP}`

---

## 2. Einkünfte / Revenus / Income Summary
| Feld / Case | Beschreibung / Description | Betrag / Amount (CHF) |
| :--- | :--- | :--- |
| **Lohnausweis 1** | Bruttolohn / Salaire brut / Gross Employment Wage | `{GROSS_INCOME_CHF}` |
| **Lohnausweis 9** | AHV/IV/ALV Beiträge / Cotisations sociales 1er pilier | `{SOCIAL_SECURITY_DEDUCTED_CHF}` |
| **Lohnausweis 10.1**| Ordentliche BVG Beiträge / Cotisations 2e pilier | `{PENSION_BVG_DEDUCTED_CHF}` |
| **Lohnausweis 11** | Nettolohn / Salaire net / Net Wage | `{NET_WAGE_CHF}` |
| **Wertschriften** | Zinsen & Dividenden / Intérêts & Dividendes / Investment Income | `{INVESTMENT_INCOME_CHF}` |
| **Total Reineinkommen** | Total Net Taxable Income Baseline | `{TOTAL_NET_INCOME_CHF}` |

---

## 3. Deklarierte Abzüge / Déductions / Itemized Deductions
| Code | Kategorie / Category | Deklariert (CHF) | Gesetzliche Grundlage (DBG / StG) | Nachweis / Proof ID |
| :--- | :--- | :--- | :--- | :--- |
| **S1** | Fahrkosten / Commute | `{S1_COMMUTE_CHF}` | DBG Art. 26 Abs. 1 a (Max `{S1_CAP}`) | `{S1_PROOF_REF}` |
| **S2** | Verpflegung / Meals | `{S2_MEALS_CHF}` | DBG Art. 26 Abs. 1 b | `{S2_PROOF_REF}` |
| **S3** | Krankheitskosten / Healthcare | `{S3_HEALTH_CHF}` | DBG Art. 33 Abs. 1 h (>5% Reineinkommen) | `{S3_PROOF_REF}` |
| **S4** | Säule 3a / Pillar 3a | `{S4_3A_CHF}` | DBG Art. 33 Abs. 1 e (Max 7'258 CHF) | `{S4_PROOF_REF}` |
| **S5** | Einkauf BVG / Pension Buy-in | `{S5_BVG_BUYIN_CHF}` | DBG Art. 33 Abs. 1 d | `{S5_PROOF_REF}` |
| **S6** | Drittbetreuung / Childcare | `{S6_CHILDCARE_CHF}` | DBG Art. 33 Abs. 3 (Max `{S6_CAP}`) | `{S6_PROOF_REF}` |
| **S7** | Weiterbildung / Education | `{S7_EDUCATION_CHF}` | DBG Art. 33 Abs. 1 j (Max 12'700 CHF) | `{S7_PROOF_REF}` |
| **S8** | Liegenschaft / Property Maintenance | `{S8_PROPERTY_CHF}` | DBG Art. 32 Abs. 2 (Werterhaltend) | `{S8_PROOF_REF}` |
| **S9** | Arbeitszimmer / Home Office | `{S9_HOMEOFFICE_CHF}`| BGE 140 II 157 | `{S9_PROOF_REF}` |
| **S10**| Depotgebühren / Custody Fees | `{S10_CUSTODY_CHF}` | DBG Art. 32 Abs. 1 | `{S10_PROOF_REF}` |
| **S11**| Schuldzinsen / Debt Interest | `{S11_INTEREST_CHF}` | DBG Art. 33 Abs. 1 a | `{S11_PROOF_REF}` |
| **S12**| Spenden / Donations | `{S12_DONATION_CHF}` | DBG Art. 33 Abs. 1 i (Max 20% Net) | `{S12_PROOF_REF}` |
| **ZW** | Zweitverdienerabzug / Dual Earner | `{DUAL_EARNER_CHF}` | DBG Art. 33 Abs. 2 | Gesetzlicher Abzug |
| **TOTAL** | **Total Abzüge / Total Deductions** | **`{TOTAL_DEDUCTIONS_CHF}`** | | |

---

## 4. Steuerberechnung / Calcul d'impôt / Tax Calculation Result
*(Computed deterministically via `swiss_tax_math.py`)*

- **Steuerbares Einkommen / Taxable Income**: `CHF {TAXABLE_INCOME_CHF}`
- **Direkte Bundessteuer (IFD)**: `CHF {FEDERAL_TAX_CHF}`
- **Kantonssteuer (Staatssteuer)**: `CHF {CANTONAL_TAX_CHF}`
- **Gemeindesteuer**: `CHF {COMMUNAL_TAX_CHF}`
- **Kirchensteuer**: `CHF {CHURCH_TAX_CHF}`
- **Vermögenssteuer**: `CHF {WEALTH_TAX_CHF}`
- **Total geschuldete Steuern / Total Tax Due**: **`CHF {TOTAL_TAX_DUE_CHF}`**
- **Effektiver Steuersatz / Effective Tax Rate**: **`{EFFECTIVE_TAX_RATE_PCT}%`**
- **Grenzsteuersatz / Marginal Tax Rate**: **`{MARGINAL_TAX_RATE_PCT}%`**

---

## 5. Steuerrisiko-Radar / Audit Pre-Check Evaluation
- **Sicherheits-Score / Audit Safety Score**: **`{AUDIT_SCORE}` / 100** (`{AUDIT_RISK_LEVEL}`)
- **Freigabeempfehlung / Status**: `{AUDIT_STATUS_TEXT}`

### Beanstandungspunkte & Empfehlungen / Flagged Items:
`{FLAGGED_ITEMS_MARKDOWN_BLOCK}`
