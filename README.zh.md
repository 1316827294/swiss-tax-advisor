# 🇨🇭 瑞士智能报税与节税助手 (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-支持的-ai-平台矩阵)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

专为 **AI Agent（Claude Code、Cursor、GitHub Copilot、Cline、Windsurf、Aider、Devin、Google Antigravity）** 打造的瑞士个人与家庭所得税申报底稿生成、税务局初审风控自检、以及主动节税规划的**开源、主权安全、确定性高精度技能库**。

> **数据完全本地化主权**：所有税额计算和用户档案均在本地通过确定性 Python 脚本执行，任何个人税务数据绝不会上传至外部云端报税平台。

---

## ⚡ 30 秒快速上手 (Quick Start)

只需 3 步即可在任意支持的 AI 环境中开启瑞士报税：

### 1. 克隆并安装
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# 自动安装到你的 AI 环境（例如 Claude Code、Cursor、或全部平台）
./install.sh --platform claude    # 或 cursor / cline / copilot / all
```

### 2. 启动对话
在终端或 AI 对话框中，直接说：
> *"你好，帮我做 2025 年的瑞士报税"* 或 *"Hello, help me file my Swiss taxes for 2025"*

### 3. AI 主动引导与自动归档
AI 会自动检测你的税务档案并主动向你提问引导（所住州与市镇、婚姻状况、子女、收入、3a 扣除等），并在后台静默计算，输出包含州税、市镇税、联邦直接税与节税建议的完整报税底稿（Steuerdossier）。数据自动保存在本地 `./user/` 目录，下次对话无需重复输入。

---

## 🌟 核心特性

| 功能模块 | 详细说明 |
|---|---|
| 🧮 **确定性计算引擎** | 严禁 AI 口算心算，覆盖全瑞士 26 州的联邦直接税 (IFD/DBG)、州税、市镇税 (Steuerfuss) 及财富税，法定 5 生丁 (5-Rappen) 舍入 |
| 📁 **凭证自动识别预填** | 将工资单 (Lohnausweis PDF/TXT)、3a 凭据或银行年结单拖入 `./documents/`，AI 启动时秒读预填，直接免去 80% 提问 |
| 💰 **实时税负看板与热修改** | 对话全程常驻动态税负与节税徽章；修改任何数字（如 3a 或通勤），AI 秒级反馈精准节省的 CHF 税金 |
| 👤 **本地档案持久化** | 自动管理 `./user/profile.json` 与 `./user/tax_YYYY.json`，跨会话记忆，隐私 100% 留存本地 |
| 🛡️ **税务局风控雷达** | 模拟州税务局初审筛选算法 (*Risikobasierte Fallauswahl*)，提前预警高危扣除（0~100 风险分，含同城虚报 GA 预警） |
| 💡 **主动节税建议** | 测算第三支柱养老金 (3a) 缺口、双职工家庭特别扣除、医保免赔额 (Franchise 300 vs 2500) 临界点 |
| 📋 **各州 eTax 逐框照抄单** | 针对伯尔尼 TaxMe、苏黎世 eTax.zh、沃州 VaudTax、日内瓦 GeTax 生成官方对应方框编号（Ziffer/Code）的直抄指南 |
| 📑 **官方合规交付物** | 自动输出 Steuerdossier 申报底稿、各州 eTax 填报指南、Fristerstreckung 延期申请信 |
| 🌐 **多语言支持** | 提问自动识别中/英/德/法/意/西；官方公函自动使用所在州官方语言（德/法/意） |
| 🔒 **隐私脱敏合规** | 符合瑞士联邦数据保护法 (DSG/FADP)，自动星号脱敏 AHV 与 IBAN 账号 |

---

## 🤖 支持的 AI 平台矩阵

| 平台 | 自动化水平 | 执行机制 | 安装命令 |
|---|---|---|---|
| **Claude Code** | 🟢 完全自动 | 自动后台运行脚本，无需人工干预 | `./install.sh --platform claude` |
| **Google Antigravity** | 🟢 完全自动 | 运行时感知 `SKILL.md`，自动调用脚本 | 原生支持 / `./install.sh --platform agy` |
| **Cursor** | 🟡 交互确认 | 根据 `.cursor/rules` 提示在 Composer 中运行 | `./install.sh --platform cursor` |
| **Cline / Roo Code** | 🟢 完全自动 | 通过 MCP/终端执行器自动执行 | `./install.sh --platform cline` |
| **Windsurf** | 🟡 交互确认 | Cascade 规则驱动 | `./install.sh --platform windsurf` |
| **GitHub Copilot** | 🟡 交互确认 | 基于 Copilot Instructions 引导 | `./install.sh --platform copilot` |
| **Aider / Devin** | 🟢 完全自动 | 按照指令规范自动调用测试与脚本 | `./install.sh --platform aider` |

---

## 💬 实际使用效果展示

```
用户: 你好，帮我做 2025 年的瑞士报税。

AI: 您好！我是您的瑞士税务助手。在开始前，我需要了解您的基本情况：
    请问您目前住在哪个州（Canton）和哪个市镇？

用户: 伯尔尼州，Bern 市。

AI: 好的，已为您记录（伯尔尼州 Bern 市）。
    请问您的婚姻状况是？（单身 / 已婚 / 注册伴侣）

用户: 单身，没有孩子，持有 B 证，年薪 95,000 CHF。

AI: 明白！正在为您生成 2025 年度报税测算底稿...
    （AI 在后台静默运行脚本，计算联邦直接税、伯尔尼州税、市镇税及 3a 节税潜力）

    📊 2025 伯尔尼预估税额一览：
    ────────────────────────────────────────
    • 联邦直接税 (Bund):         CHF  1,420.00
    • 伯尔尼州税 (Kanton):        CHF  6,850.00
    • 市镇税 (Gemeinde Bern):    CHF  6,920.00
    • 预估税额合计:               CHF 15,190.00
    ────────────────────────────────────────
    💡 节税提醒：
    您尚未填报第三支柱 (Pillar 3a)。2025 年最高限额为 CHF 7,258。
    若全额缴纳，按您约 28.5% 的边际税率，可直接为您节省约 CHF 2,068 的税款！
```

---

## 🔒 隐私与本地数据安全承诺

1. **绝对离线优先**：所有税率表与算法均硬编码或离线引用在 `scripts/` 与 `references/` 中，计算时无需网络请求。
2. **严格的 Git 忽略规则**：根目录与 `user/` 均配备严格的 `.gitignore`，您的 `profile.json`、历史税单数据、以及任何生成的 `reports/` 绝对不会被意外 commit 或 push 到公共仓库。
3. **开源透明**：完全基于 Python 标准库，代码行行可审计。

---

## 🤝 参与贡献

欢迎瑞士税务专家、软件工程师与跨国通勤者参与完善！
请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何新增各州税率表（Canton Tariffs）与市镇乘数（Steuerfuss）。

---

## 📄 开源许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。
