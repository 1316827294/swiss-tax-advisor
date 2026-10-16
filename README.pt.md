# 🇨🇭 Consultor Fiscal Suíço & Declaração de Impostos (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-plataformas-de-ia-compat%C3%ADveis)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

Um **skill de agente de IA soberano, de código aberto e determinístico** para a declaração de impostos sobre o rendimento e a fortuna em **todos os 26 cantões suíços**, pré-verificação de riscos fiscais cantonais e consultoria proativa para poupança fiscal. Compatível com **Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Aider, Devin e Google Antigravity**.

> **Soberania e Privacidade Local**: Todos os cálculos fiscais e perfis de utilizador permanecem 100% locais na pasta `./user/`. Nenhum dado financeiro é transmitido para servidores de terceiros.

---

## ⚡ Começar em 30 Segundos (Quick Start)

### 1. Clonar e Instalar
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# Instale para a sua plataforma de IA (ex.: Claude Code ou Cursor)
./install.sh --platform claude    # ou cursor / cline / copilot / all
```

### 2. Iniciar a Conversação
Fale com o seu assistente de IA em português:
> *"Olá! Podes ajudar-me a preencher a minha declaração de impostos na Suíça para 2025?"*

### 3. Leitura Automática de Documentos & Guia eTax
Coloque o seu certificado de salário (*Certificat de salaire / Lohnausweis* em PDF/TXT), comprovativos do 3º pilar A ou extratos bancários em `./documents/`. O assistente lê automaticamente os campos oficiais, calcula os seus impostos federais, cantonais e comunais e gera um **guia passo a passo com os códigos exatos para preencher o portal oficial do seu cantão** (VaudTax, GeTax, TaxMe, FriTax, ValTax, eTax.zh, etc.).

---

## 🌟 Principais Funcionalidades

| Módulo | Descrição |
|---|---|
| 🧮 **Motor Determinístico Suíço** | Sem cálculos aproximados por IA. Aplica as tabelas oficiais de todos os 26 cantões (imposto federal IFD, imposto cantonal, coeficiente comunal, imposto eclesiástico e fortuna) com arredondamento legal suíço a 5 cêntimos |
| 📁 **Reconhecimento Automático de Ficheiros** | Basta colocar os documentos em `./documents/`: extração instantânea do salário bruto (Ziffer 1), deduções LPP (Ziffer 9), alimentação e 3º pilar |
| 💰 **Painel Fiscal em Tempo Real** | Indicação constante da estimativa de imposto e da poupança potencial; cálculo imediato da variação de imposto (Delta) ao atualizar valores |
| 📋 **Guias Oficiais Campo a Campo (eTax)** | Instruções diretas com os códigos para VaudTax (VD), GeTax (GE), TaxMe (BE), FriTax (FR), ValTax (VS), eTax.zh (ZH), EasyTax (AG), BalTax (BS), eTax.zug (ZG), etc. |
| 🛡️ **Radar de Risco de Auditoria Cantonal** | Verificação com base nos algoritmos de triagem do fisco (*Risikobasierte Fallauswahl*, princípio de necessidade do passe GA da SBB/CFF, formação contínua >15%) |
| 💡 **Otimização Fiscal Proativa** | Poupança marginal pelo 3º pilar A, dedução para casais com duplo rendimento, otimização da franquia do seguro de saúde (300 vs 2500) |
| ⚖️ **Decisão sobre Imposto na Fonte (NOV / TOU)** | Avaliação para titulares de autorização de residência B: simula se compensa pedir a tributação ordinária posterior sem risco de pagar imposto extra |
| 🔒 **Privacidade Total LPD / FADP** | Tratamento 100% offline em `./user/`; ocultação automática de números AVS e IBAN |

---

## 🤖 Plataformas de IA Compatíveis

| Plataforma | Nível de Automação | Comando de Instalação |
|---|---|---|
| **Claude Code** | 🟢 Totalmente automático | `./install.sh --platform claude` |
| **Cursor** | 🟡 Confirmação interativa | `./install.sh --platform cursor` |
| **Cline / Roo Code** | 🟢 Totalmente automático | `./install.sh --platform cline` |
| **Windsurf** | 🟡 Confirmação interativa | `./install.sh --platform windsurf` |
| **GitHub Copilot** | 🟡 Confirmação interativa | `./install.sh --platform copilot` |
| **Aider / Devin** | 🟢 Totalmente automático | `./install.sh --platform aider` |
| **Google Antigravity** | 🟢 Totalmente automático | `./install.sh --platform agy` |

---

## 📄 Licença

Distribuído sob a licença [Apache 2.0](LICENSE).
