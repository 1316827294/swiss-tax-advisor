# 🇨🇭 Conseiller Fiscal Suisse & Déclaration d'Impôts (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-plateformes-dia-compatibles)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

Un **skill d'agent IA open-source, souverain et déterministe** pour la déclaration d'impôt sur le revenu et la fortune dans les **26 cantons suisses**, l'auto-contrôle des risques fiscaux cantonaux et le conseil en optimisation fiscale proactive. Compatible avec **Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Aider, Devin et Google Antigravity**.

> **Souveraineté des données garantie** : Tous les calculs d'impôts et les dossiers fiscaux restent 100% locaux dans `./user/`. Aucune donnée financière n'est transmise à des serveurs tiers.

---

## ⚡ Prise en main en 30 secondes (Quick Start)

### 1. Cloner et installer
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# Installer pour votre plateforme (ex. Claude Code ou Cursor)
./install.sh --platform claude    # ou cursor / cline / copilot / all
```

### 2. Démarrer la conversation
Écrivez simplement à votre agent en français :
> *"Bonjour ! Peux-tu m'aider à préparer ma déclaration d'impôts suisse pour 2025 ?"*

### 3. Traitement automatique des justificatifs & Guide eTax
Déposez votre certificat de salaire (Lohnausweis PDF/TXT), vos attestations du 3e pilier A ou vos relevés bancaires au 31.12 dans le dossier `./documents/`. L'agent extrait automatiquement les cases clés (salaire brut, cotisations LPP, repas), calcule votre impôt fédéral, cantonal et communal, et génère un **guide pas-à-pas pour recopier les montants dans votre logiciel officiel** (VaudTax, GeTax, TaxMe, FriTax, ValTax, etc.).

---

## 🌟 Fonctionnalités Clés

| Module | Description |
|---|---|
| 🧮 **Moteur Déterministe** | Aucun calcul approximatif. Barèmes officiels pour les 26 cantons (impôt fédéral direct IFD, impôt cantonal, coefficient communal, impôt ecclésiastique, fortune) avec arrondi légal suisse à 5 centimes |
| 📁 **Ingestion Automatique de Documents** | Déposez vos pièces dans `./documents/` : extraction instantanée du certificat de salaire (cases 1 à 15), attestations 3a et soldes bancaires |
| 💰 **Tableau de Bord Fiscal en Direct** | Badge permanent affichant l'impôt estimé et l'économie potentielle ; calcul immédiat de la variation d'impôt (Delta) lors d'une modification |
| 📋 **Guides Officiels Pas-à-Pas (eTax)** | Génération de listes de saisie case par case pour VaudTax (VD), GeTax (GE), TaxMe (BE), FriTax (FR), ValTax (VS), eTax.zh (ZH), etc. |
| 🛡️ **Radar de Risque Fiscal** | Évaluation préalable des déclarations selon les algorithmes de filtrage cantonal (contrôle de nécessité pour l'AG CFF, formations continues >15%) |
| 💡 **Optimisation Fiscale Proactive** | Calcul de l'économie marginale du 3e pilier A, déduction pour couple avec double revenu, optimisation de franchise d'assurance maladie (300 vs 2500) |
| ⚖️ **Arbitrage Impôt à la Source (TOU / NOV)** | Analyse pour les titulaires de permis B : évalue si une demande de taxation ordinaire ultérieure (TOU) est avantageuse ou risquée |
| 🔒 **Confidentialité LPD / FADP** | Traitement 100% hors-ligne dans `./user/` ; masquage automatique des numéros AVS et coordonnées IBAN |

---

## 🤖 Plateformes d'IA Compatibles

| Plateforme | Automatisation | Mécanisme | Commande d'installation |
|---|---|---|---|
| **Claude Code** | 🟢 Entièrement automatique | Exécution en arrière-plan | `./install.sh --platform claude` |
| **Cursor** | 🟡 Confirmation interactive | Piloté par règles Composer | `./install.sh --platform cursor` |
| **Cline / Roo Code** | 🟢 Entièrement automatique | Exécution terminal directe | `./install.sh --platform cline` |
| **Windsurf** | 🟡 Confirmation interactive | Cascade Rules | `./install.sh --platform windsurf` |
| **GitHub Copilot** | 🟡 Confirmation interactive | Copilot Instructions | `./install.sh --platform copilot` |
| **Aider / Devin** | 🟢 Entièrement automatique | Conventions & playbooks | `./install.sh --platform aider` |
| **Google Antigravity** | 🟢 Entièrement automatique | Skill natif | `./install.sh --platform agy` |

---

## 📄 Licence

Ce projet est publié sous [Licence Apache 2.0](LICENSE).
