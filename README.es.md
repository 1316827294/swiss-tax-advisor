# 🇨🇭 Asesor Fiscal Suizo & Declaración de Impuestos (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-plataformas-de-ia-compatibles)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

Un **skill de agente IA de código abierto, soberano y determinista** para la declaración de impuestos sobre la renta y el patrimonio en los **26 cantones suizos**, pre-auditoría de riesgos fiscales y asesoría proactiva para optimizar el ahorro fiscal. Compatible con **Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Aider, Devin y Google Antigravity**.

> **Soberanía de datos garantizada**: Todos los cálculos y expedientes fiscales permanecen 100% locales en la carpeta `./user/`. Ningún dato financiero se envía a servidores de terceros.

---

## ⚡ Inicio Rápido en 30 Segundos (Quick Start)

### 1. Clonar e instalar
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# Instale en su plataforma favorita (ej. Claude Code o Cursor)
./install.sh --platform claude    # o cursor / cline / copilot / all
```

### 2. Iniciar la conversación
Hable con su asistente en español:
> *"¡Hola! Ayúdame a rellenar mi declaración de impuestos en Suiza para el año 2025."*

### 3. Ingesta automática de documentos y Guía eTax
Coloque su certificado de salario (Lohnausweis PDF/TXT), justificantes del 3er pilar o extractos bancarios al 31.12 en la carpeta `./documents/`. El asistente leerá automáticamente las casillas oficiales, calculará los impuestos federales, cantonales y comunales, y generará una **guía casilla por casilla para rellenar el portal oficial de su cantón** (TaxMe, eTax.zh, VaudTax, GeTax, etc.).

---

## 🌟 Características Principales

| Módulo | Descripción |
|---|---|
| 🧮 **Motor Determinista** | Sin estimaciones mentales. Baremos oficiales para los 26 cantones (impuesto federal directo IFD, cantonal, coeficiente municipal, eclesiástico, patrimonio) con redondeo suizo legal a 5 céntimos |
| 📁 **Ingesta Automática de Documentos** | Coloque archivos en `./documents/`: extracción instantánea del certificado de salario (casillas 1 a 15), 3er pilar y saldos bancarios |
| 💰 **Panel Fiscal en Tiempo Real** | Visualización continua del impuesto estimado y del ahorro potencial; cálculo inmediato de la diferencia (Delta) al modificar datos |
| 📋 **Guías Oficiales Casilla por Casilla (eTax)** | Tablas de equivalencia para TaxMe (BE), eTax.zh (ZH), VaudTax (VD), GeTax (GE), EasyTax (AG), BalTax (BS), eTax.zug (ZG), etc. |
| 🛡️ **Radar de Riesgo de Auditoría** | Simulación del cribado cantonal (*Risikobasierte Fallauswahl*, principio de necesidad para el abono general GA de SBB, formación >15%) |
| 💡 **Optimización Fiscal Proactiva** | Cálculo del tipo marginal y ahorro por el 3er pilar A, deducción por doble ingreso conyugal, optimización de franquicia del seguro médico (300 vs 2500) |
| ⚖️ **Decisión sobre Impuesto en la Fuente (NOV)** | Evaluación para titulares de permiso B: calcula si conviene solicitar la tributación ordinaria posterior (NOV) sin riesgo de pagar más |
| 🔒 **Privacidad LPD / FADP** | Ejecución 100% local en `./user/`; enmascaramiento automático de números AVS y cuentas IBAN |

---

## 📄 Licencia

Publicado bajo la [Licencia Apache 2.0](LICENSE).
