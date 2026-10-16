# 🇨🇭 Schweizer Steuerberater & Steuererklärungs-Assistent (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-unterst%C3%BCtzte-ki-agenten-plattformen)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

Ein **quelloffener, souveräner und deterministischer KI-Agenten-Skill** für die Schweizer Einkommens- und Vermögenssteuererklärung, kantonale Vorab-Prüfung von Steuerrisiken (Risikobasierte Fallauswahl) sowie proaktive Steueroptimierung für **alle 26 Kantone**. Kompatibel mit **Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Aider, Devin und Google Antigravity**.

> **Datensouveränität ab Werk**: Alle Steuerberechnungen und Benutzerprofile verbleiben 100% lokal unter `./user/`. Keine Finanzdaten werden jemals an externe Cloud-Dienste übermittelt.

---

## ⚡ Schnellstart in 30 Sekunden (Quick Start)

### 1. Klonen & Installieren
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# Installieren Sie für Ihre bevorzugte Plattform (z. B. Claude Code oder Cursor)
./install.sh --platform claude    # oder cursor / cline / copilot / all
```

### 2. Gespräch starten
Schreiben Sie Ihrem KI-Assistenten einfach auf Deutsch:
> *"Grüezi! Bitte hilf mir bei meiner Schweizer Steuererklärung für 2025."*

### 3. Automatische Belegerkennung & eTax-Anleitung
Werfen Sie Ihren Lohnausweis (PDF/TXT) oder Ihre Säule 3a-Bescheinigung in den Ordner `./documents/`. Der KI-Assistent liest Ziffer 1, Ziffer 9 und Ziffer 13G automatisch aus, berechnet Ihre Bundes-, Kantons- und Gemeindesteuer auf den Rappen genau und generiert eine **Schritt-für-Schritt-Ausfüllhilfe für das offizielle kantonale Steuerportal** (z. B. TaxMe, eTax.zh, EasyTax, eTax.zug, BalTax).

---

## 🌟 Hauptfunktionen

| Modul | Beschreibung |
|---|---|
| 🧮 **Deterministische Steuerberechnung** | Keine Halluzinationen oder Kopfrechnen. Präzise Tarife für alle 26 Kantone (Bund, Kanton, Gemeinde-Steuerfuss, Kirchensteuer, Vermögenssteuer) mit Schweizer 5-Rappen-Rundung |
| 📁 **Automatische Belegerkennung** | Dokumente in `./documents/` ablegen: Liest Lohnausweis (Ziffer 1–15), Säule 3a und Bank-Saldoausweise per 31.12. automatisch ein |
| 💰 **Echtzeit-Steuer-Dashboard & Hot-Edit** | Fortlaufende Anzeige der geschätzten Steuer und Ersparnis; sofortiger Ausweis der Steuerdifferenz (Delta) bei Anpassungen |
| 📋 **Kantonale eTax-Ausfüllhilfe** | Generiert eine 1:1 Übertragungsliste für offizielle Steuerportale (TaxMe BE, eTax.zh, EasyTax AG, BalTax BS, eTax.zug ZG etc.) |
| 🛡️ **Audit-Risiko-Radar** | Prüfung nach kantonalen Screening-Kriterien (Risikobasierte Fallauswahl, GA-Notwendigkeitsprüfung, Weiterbildung >15%) |
| 💡 **Proaktive Steueroptimierung** | Säule 3a Potenzialrechnung, Zweitverdienerabzug, Krankenkassen-Franchise-Optimierer (300 vs. 2500) |
| ⚖️ **Quellensteuer NOV-Rechner** | Berechnung, ob sich ein Antrag auf nachträgliche ordentliche Veranlagung (NOV) für B-Ausweis-Inhaber lohnt |
| 🔒 **DSG / FADP Datenschutz** | Vollständig lokale Datenhaltung in `./user/`; automatische Maskierung von AHV- und IBAN-Nummern |

---

## 🤖 Unterstützte KI-Agenten-Plattformen

| Plattform | Automatisierungsgrad | Installationsbefehl |
|---|---|---|
| **Claude Code** | 🟢 Vollautomatisch | `./install.sh --platform claude` |
| **Cursor** | 🟡 Interaktive Bestätigung | `./install.sh --platform cursor` |
| **Cline / Roo Code** | 🟢 Vollautomatisch | `./install.sh --platform cline` |
| **Windsurf** | 🟡 Interaktive Bestätigung | `./install.sh --platform windsurf` |
| **GitHub Copilot** | 🟡 Interaktive Bestätigung | `./install.sh --platform copilot` |
| **Aider / Devin** | 🟢 Vollautomatisch | `./install.sh --platform aider` |
| **Google Antigravity** | 🟢 Vollautomatisch | `./install.sh --platform agy` |

---

## 📄 Lizenz

Dieses Projekt ist unter der [Apache-Lizenz 2.0](LICENSE) lizenziert.
