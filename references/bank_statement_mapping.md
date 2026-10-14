# Swiss Bank Statement & CAMT.053 Ingestion Mapping Guide

This guide details how to extract and categorize Swiss bank export files (CAMT.053 XML, TWINT CSV, and bank statement exports from UBS, PostFinance, Neon, and Revolut) directly into standard tax deduction codes (S1–S12).

---

## 1. Supported Formats & Parsing Signatures

| Format / Source | File Type | Key Identifying Headers / Structure | Typical Transaction Types |
| :--- | :--- | :--- | :--- |
| **ISO 20022 CAMT.053**| `.xml` | `<BkToCstmrStmt>`, `<Ntry>`, `<Amt Ccy="CHF">` | Official Swiss interbank standard statement |
| **TWINT Export** | `.csv` | `Transaktionstyp;Partner;Betrag;Datum;Status` | Mobile P2P payments, parking, donations |
| **PostFinance** | `.csv` | `Buchungsdatum;Buchungstext;Gutschrift in CHF;Lastschrift in CHF` | General salary, retail payments, mortgage |
| **UBS e-banking** | `.csv` | `Trade date;Value date;Description;Debited/Credited;Balance` | Salary, investments, international transfers |
| **Neon / Revolut** | `.csv` | `Date;Amount;Currency;Description;Category` | Daily expenses, card payments, food, transport |

---

## 2. Tax Keyword Extraction & Category Mapping

When scanning transaction descriptions, map matching merchants or booking texts to tax deduction categories:

| Target Category | Keywords & Merchant Identifiers (Regex Matchers) | Example Booking Description |
| :--- | :--- | :--- |
| **S4: Säule 3a** | `(Viac\|Finpension\|Frankly\|3a\|Säule 3a\|3e pilier\|Pilastro 3a)` | `Dauerauftrag VIAC Vorsorgestiftung 3a` |
| **S1: Commute** | `(SBB\|CFF\|FFS\|ZVV\|Libero\|Fairtiq\|EasyRide\|Bernmobil\|TL)` | `SBB CFF FFS INTERNET Bern` |
| **S6: Childcare** | `(Kita\|Kindertagesstätte\|Tagesmutter\|Crèche\|Hort\|Schulergänzende)` | `Kita Bärenhöhle Monatsbeitrag` |
| **S7: Education** | `(Weiterbildung\|Universität\|Hochschule\|CAS\|DAS\|MAS\|Akademie\|Schule)` | `Berner Fachhochschule Weiterbildung CAS` |
| **S3: Healthcare** | `(Zahnarzt\|Dentist\|Krankenkasse\|CSS\|Swica\|Helsana\|Concordia\|Visana)` | `Zahnarztpraxis Dr. Keller Rechnung 2025` |
| **S10: Custody** | `(Depotgebühr\|Depotführung\|Courtage\|Steuerverzeichnis)` | `UBS Depotgebühren Q4/2025` |
| **S11: Interest** | `(Hypothekarzins\|Schuldzinsen\|Darlehenszins\|Kreditzins)` | `Hypothekarzins Festhypothek 10J` |
| **S12: Donation** | `(Spende\|Donation\|Rotes Kreuz\|Caritas\|WWF\|Greenpeace\|SRK)` | `Spende Schweizerisches Rotes Kreuz SRK` |
| **Alimente** | `(Alimente\|Unterhaltsbeitrag\|Pensions alimentaires)` | `Unterhaltsbeitrag gemäss Scheidungsurteil` |

---

## 3. Disallowed Deductions (Negative Keyword Filtering)
Flag and filter out transactions that are commonly mistaken for deductions:
- ❌ **Leasing**: `(Leasing|Alphabet|LeasePlan|Cembra|BMW Financial)` -> Disallow as private leasing is non-deductible.
- ❌ **Traffic Fines**: `(Busse|Ordnungsbusse|Polizei|Amtsgericht)` -> Strictly non-deductible.
- ❌ **Tax Prep Fees**: `(Treuhänder|TaxPrep|Steuerberater)` -> Cannot be deducted under Swiss personal income tax.
