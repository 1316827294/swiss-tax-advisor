# 🇨🇭 Schweizer Steuerberater-Agent (`swiss-tax-advisor`)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [简体中文](README.zh.md)

---

> **Open-Source Agent Skill für Schweizer Steuererklärungen, Prüfungsrisiko-Radar & proaktive Steueroptimierung.**  
> Entwickelt für **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor** und **OpenClaw**.

---

## 🚀 Hauptfunktionen

1. **Null externe Abhängigkeiten**: Reines Python 3.10+ Standardbibliothek (`math`, `argparse`, `json`, `sys`, `unittest`). Kein `pip install` nötig.
2. **Deterministische 5-Rappen-Präzision**: Schutz vor LLM-Kopfrechenfehlern bei progressiven Schweizer Tarifen und Steuerfüssen.
3. **Kantonales Steuerrisiko-Radar (Score 0–100)**: Simuliert die automatisierte *Risikobasierte Fallauswahl* kantonaler Steuerverwaltungen zur Vermeidung von Auflagen.
4. **Vollständige S1–S12 & Bern 2025/2026 Nomenklatur**: Berufs- und Krankheitskosten, Säule 3a, Zweitverdienerabzug, Photovoltaik-Verlustvortrag, Erneuerungsfonds und Alimente.
5. **Erweiterte Entscheidungsmodule**:
   - **Quellensteuer NOV-Prüfer**: Risiko- und Ertragsanalyse für die nachträgliche ordentliche Veranlagung von B-Bewilligungsträgern.
   - **Krankenkassen-Franchisen-Optimierer**: Mathematischer Break-Even-Vergleich zwischen Franchise 300 und 2500.
   - **Wohnortswechsel-Simulator**: Steuerbelastungsvergleich über Kantone und Gemeinden hinweg.

---

## ⚡ Schnellstart & Tests

Offline-Testsuite ausführen:
```bash
python3 skills/swiss-tax-advisor/scripts/test_tax_engine.py
```
*(Erwartet: `Ran 12 tests in 0.001s, OK`)*

### CLI-Befehlsbeispiele

```bash
# 1. Steuerberechnung (Bern, Verheiratet, 170k Brutto, 3a & Kita-Abzug)
python3 skills/swiss-tax-advisor/scripts/swiss_tax_math.py \
  --gross-income 170000 --canton BE --civil-status MARRIED --children 1 \
  --deductions '{"s1": 3300, "s4": 7258, "s6": 18000}' --json

# 2. Grenzsteuersatz und Säule 3a Steuerersparnis berechnen
python3 skills/swiss-tax-advisor/scripts/marginal_rate_calc.py \
  --income 120000 --canton ZH --deduction 7258 --category PILLAR_3A --json

# 3. Quellensteuer NOV-Antrag bewerten
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 110000 --canton ZH --deductions '{"s4": 7258, "s1": 3300}'

# 4. Krankenkassen-Franchise optimieren
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py franchise \
  --spend 1400 --premium-300 450 --premium-2500 310
```

---

## 📄 Lizenz

Veröffentlicht unter der **MIT-Lizenz**. Siehe `LICENSE` für Details.
