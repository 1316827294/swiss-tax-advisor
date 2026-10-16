# 🇨🇭 スイス確定申告・節税AIアシスタント (`swiss-tax-advisor`)

[![CI](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/1316827294/swiss-tax-advisor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Multi-Platform](https://img.shields.io/badge/platforms-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Windsurf%20%7C%20Cline%20%7C%20AGY-success.svg)](#-対応aiエージェントプラットフォーム)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [简体中文](README.zh.md)

---

スイス全26カ州の所得税および富裕税申告、州税務署の監査リスク事前検証、積極的節税アドバイザリーをローカルで完結する**オープンソース・確定性AIエージェントスキル**。  
**Claude Code、Cursor、GitHub Copilot、Cline、Windsurf、Aider、Devin、Google Antigravity** に完全対応しています。

> **データ主権・完全ローカル保護**：すべての税額計算およびプロファイル情報は `./user/` 配下に完全ローカル保存されます。財務データが外部のクラウド税務サービスに送信されることは一切ありません。

---

## ⚡ 30秒クイックスタート (Quick Start)

### 1. クローンとインストール
```bash
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# お使いのAI環境に合わせてインストール（例：Claude Code または Cursor）
./install.sh --platform claude    # または cursor / cline / copilot / all
```

### 2. 対話を開始する
日本語でそのまま話しかけるだけでアシスタントが起動します：
> *「こんにちは。2025年度のスイスの確定申告（Steuererklärung）を手伝ってください。」*

### 3. 書類の自動読み込み＆州別eTax入力ガイド
給与証明書（Lohnausweis PDF/TXT）やピラー3a（第3の柱）の証明書を `./documents/` フォルダに置くだけで、AIが総支給額（Box 1）や年金控除（Box 9）、昼食手当（Box 13G）を瞬時に自動抽出します。連邦税・州税・市町村税を算出し、**各州の公式申告システム（TaxMe、eTax.zh、VaudTax、GeTax等）の番号別入力チェックシート**を自動生成します。

---

## 🌟 主な機能と特徴

| モジュール | 詳細説明 |
|---|---|
| 🧮 **確定性高精度計算エンジン** | AIによる概算・暗算を完全禁止。全26州の連邦直接税（IFD/DBG）、州税、市町村税（Steuerfuss）、教会税、富裕税をスイス法定の5ラッペン単位で正確に計算 |
| 📁 **証憑書類の自動解析（OCR）** | `./documents/` に書類を配置：給与証明書（Lohnausweis 1〜15項）、ピラー3a控除、年末銀行残高を自動抽出・自動反映 |
| 💰 **リアルタイム税額ダッシュボード** | 対話中も常にリアルタイムの概算納税額と節税可能額をバッジ表示。金額変更時も差額（Delta）を即座に算出 |
| 📋 **州別eTax入力チェックシート** | 各州の公式申告システム（ベルン州TaxMe、チューリッヒ州eTax.zh、ヴォー州VaudTax、ジュネーブ州GeTax、ツーク州eTax.zug等）の入力コード（Ziffer/Code）一覧を出力 |
| 🛡️ **税務署監査リスクレーダー** | スイス州税務署の一次審査アルゴリズム（*Risikobasierte Fallauswahl*）を再現（SBB GA全線定期の通勤必要性審査、研修費15%超過等） |
| 💡 **プロアクティブな節税アドバイス** | ピラー3a（第3の柱）満額拠出による限界節税額、共働き夫婦特別控除、基礎健康保険フランチャイズ最適化（300 vs 2500） |
| ⚖️ **源泉徴収税（Quellensteuer）確定申告判定** | B許可（B-Permit）保持者向け：事後通常課税（NOV/TOU）を申請して還付を受けるべきか、追徴リスクがないかを事前シミュレーション |
| 🔒 **スイスデータ保護法（FADP/DSG）準拠** | 完全オフライン動作。AHV番号やIBAN番号の自動マスキング機能を標準搭載 |

---

## 🤖 対応AIエージェントプラットフォーム

| プラットフォーム | 自動化レベル | 実行方式 | インストールコマンド |
|---|---|---|---|
| **Claude Code** | 🟢 完全自動 | バックグラウンド自動実行 | `./install.sh --platform claude` |
| **Cursor** | 🟡 対話確認 | Composer Rules | `./install.sh --platform cursor` |
| **Cline / Roo Code** | 🟢 完全自動 | ターミナル直接実行 | `./install.sh --platform cline` |
| **Windsurf** | 🟡 対话确认 | Cascade Rules | `./install.sh --platform windsurf` |
| **GitHub Copilot** | 🟡 対话确认 | Copilot Instructions | `./install.sh --platform copilot` |
| **Aider / Devin** | 🟢 完全自動 | 規約＆プレイブック | `./install.sh --platform aider` |
| **Google Antigravity** | 🟢 完全自動 | ネイティブSkill | `./install.sh --platform agy` |

---

## 📄 ライセンス

本プロジェクトは [Apache License 2.0](LICENSE) のもとで公開されています。
