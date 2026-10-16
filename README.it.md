# 🇨🇭 Consulente Fiscale Svizzero & Dichiarazione delle Imposte (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-piattaforme-ia-supportate)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

Un **skill per agenti IA open-source, sovrano e deterministico** per la dichiarazione fiscale su reddito e sostanza in **tutti i 26 cantoni svizzeri**, pre-valutazione dei rischi fiscali cantonali e consulenza proattiva per il risparmio d'imposta. Compatibile con **Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Aider, Devin e Google Antigravity**.

> **Sovranità dei dati garantita**: Tutti i calcoli fiscali e i profili utente rimangono al 100% locali nella cartella `./user/`. Nessun dato finanziario viene trasmesso a server cloud esterni.

---

## ⚡ Guida Rapida in 30 Secondi (Quick Start)

### 1. Clonare e installare
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# Installare per la propria piattaforma IA (es. Claude Code o Cursor)
./install.sh --platform claude    # oppure cursor / cline / copilot / all
```

### 2. Avviare la conversazione
Scrivi semplicemente al tuo assistente in italiano:
> *"Buongiorno! Aiutami a preparare la mia dichiarazione fiscale svizzera per il 2025."*

### 3. Acquisizione documenti & Guida ufficiale e-Tax
Trascina il tuo certificato di salario (Lohnausweis PDF/TXT), le attestazioni del 3° pilastro A o i saldi bancari al 31.12 nella cartella `./documents/`. L'agente estrarrà automaticamente i campi rilevanti, calcolerà le imposte federali, cantonali e comunali e genererà una **guida passo-passo per inserire i codici esatti nel portale ufficiale del tuo cantone** (e-Tax TI, TaxMe, eTax.zh, VaudTax, ecc.).

---

## 🌟 Funzionalità Principali

| Modulo | Descrizione |
|---|---|
| 🧮 **Motore Deterministico** | Nessun calcolo a mente. Tariffe legali per tutti i 26 cantoni (IFD federale, imposta cantonale, moltiplicatore comunale, imposta di culto, sostanza) con arrotondamento svizzero a 5 centesimi |
| 📁 **Riconoscimento Automatico Documenti** | Inserisci i file in `./documents/`: lettura immediata del certificato di salario (punti da 1 a 15), attestazioni 3a e saldi di conti bancari |
| 💰 **Cruscotto Fiscale in Tempo Reale** | Visualizzazione costante dell'imposta stimata e del risparmio potenziale; calcolo immediato della differenza (Delta) in caso di modifiche |
| 📋 **Guide Ufficiali di Compilazione (eTax)** | Tabelle con i codici esatti per e-Tax TI (Canton Ticino), TaxMe (BE), eTax.zh (ZH), VaudTax (VD), GeTax (GE), ecc. |
| 🛡️ **Radar del Rischio Fiscale** | Simulazione degli algoritmi di screening cantonale (controllo di necessità per abbonamento generale FFS, corsi di formazione >15%) |
| 💡 **Ottimizzazione Fiscale Proattiva** | Calcolo dell'aliquota marginale del 3° pilastro A, deduzione per coniugi con doppio reddito, ottimizzazione della franchigia cassa malati (300 vs 2500) |
| ⚖️ **Valutazione Imposta alla Fonte (NOV)** | Analisi di convenienza per titolari di permesso B per richiedere la tassazione ordinaria ulteriore senza rischi di conguaglio negativo |
| 🔒 **Conformità Privacy LPD / FADP** | Esecuzione al 100% locale in `./user/`; mascheramento automatico dei numeri AVS e delle coordinate IBAN |

---

## 🤖 Piattaforme IA Supportate

| Piattaforma | Automazione | Modalità di esecuzione | Comando di installazione |
|---|---|---|---|
| **Claude Code** | 🟢 Completamente automatico | Esecuzione in background | `./install.sh --platform claude` |
| **Cursor** | 🟡 Conferma interattiva | Regole per Composer | `./install.sh --platform cursor` |
| **Cline / Roo Code** | 🟢 Completamente automatico | Esecuzione tramite terminale | `./install.sh --platform cline` |
| **Windsurf** | 🟡 Conferma interattiva | Cascade Rules | `./install.sh --platform windsurf` |
| **GitHub Copilot** | 🟡 Conferma interattiva | Istruzioni Copilot | `./install.sh --platform copilot` |
| **Aider / Devin** | 🟢 Completamente automatico | Convenzioni e playbook | `./install.sh --platform aider` |
| **Google Antigravity** | 🟢 Completamente automatico | Skill nativo | `./install.sh --platform agy` |

---

## 📄 Licenza

Rilasciato sotto licenza [Apache 2.0](LICENSE).
