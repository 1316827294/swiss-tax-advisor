# 🇨🇭 Consulente Fiscale Svizzero (`swiss-tax-advisor`)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [简体中文](README.zh.md)

---

> **Agent Skill open-source per la dichiarazione fiscale svizzera, radar di rischio e ottimizzazione fiscale proattiva.**  
> Compatibile con **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor** e **OpenClaw**.

---

## 🚀 Funzionalità Principali

1. **Zero Dipendenze Esterne**: Sviluppato unicamente con la libreria standard di Python 3.10+ (`math`, `argparse`, `json`, `sys`, `unittest`).
2. **Precisione Deterministica a 5 Rappen**: Protezione completa contro errori di calcolo degli LLM sulle aliquote progressive e sui moltiplicatori cantonali.
3. **Radar di Rischio Fiscale Cantonale (Score 0–100)**: Simula i controlli automatici delle autorità fiscali per prevenire contestazioni.
4. **Tassonomia Completa delle Deduzioni (S1 a S12)**: Deduzioni per spese professionali, custodia dei figli, terzo pilastro 3a, doppio reddito coniugale e alimenti.
5. **Strumenti Decisionali Avanzati**:
   - **Valutatore NOV Imposta alla Fonte**: Analisi di convenienza per la tassazione ordinaria successiva.
   - **Ottimizzatore Franchigia Cassa Malati (300 vs 2500)**: Calcolo attuariale del punto di pareggio.
   - **Simulatore di Trasferimento Cantonale**: Confronto dei moltiplicatori d'imposta (*Steuerfuss*).

---

## ⚡ Guida Rapida

Eseguire la suite di test offline:
```bash
python3 skills/swiss-tax-advisor/scripts/test_tax_engine.py
```

### Esempi di Comandi CLI

```bash
# 1. Calcolare le imposte (Ticino, Coniugato, 170k lordi, 3° pilastro e asilo)
python3 skills/swiss-tax-advisor/scripts/swiss_tax_math.py \
  --gross-income 170000 --canton TI --civil-status MARRIED --children 1 \
  --deductions '{"s1": 3300, "s4": 7258, "s6": 18000}' --json

# 2. Valutare la tassazione ordinaria successiva (NOV)
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 110000 --canton TI --deductions '{"s4": 7258, "s1": 3300}'
```

---

## 📄 Licenza

Distribuito sotto **Licenza MIT**. Consultare `LICENSE` per maggiori dettagli.
