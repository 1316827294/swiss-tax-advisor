# 📁 用户税务凭证投放目录 (Documents Ingestion)

在此目录下放入您的瑞士税务相关电子文档，AI 助手在每次启动时会**自动读取、提取关键数据并预填申报表**，帮您跳过繁琐的人工问答。

---

## 📄 支持投放的文件类型与命名建议

| 凭证类型 | 官方德语/法语名称 | 常见文件名示例 | AI 自动提取字段 |
|---|---|---|---|
| **工资单** | Lohnausweis / Certificat de salaire | `Lohnausweis_2025.pdf`, `salary.txt` | 税前收入 (Box 1)、养老金扣缴 (Box 9)、餐补/交通报销 (Box 13G/15) |
| **第三支柱养老金凭据** | Säule 3a Bescheinigung / Attestation 3a | `3a_Frankly_2025.pdf`, `pillar3a.txt` | 2025 年度缴费总额 (S4 扣除) |
| **银行年结单** | Zins- und Saldoausweis / Relevé fiscal | `UBS_Saldo_2025.pdf`, `bank.txt` | 12月31日账户净资产余额 (财产税申报)、利息预扣税 |
| **医保自付与保费单** | Prämienabrechnung & Kostenbeteiligung | `Swica_2025.pdf`, `health.txt` | 全年自付医疗花费 (S3 扣除)、医保保费总额 |
| **托儿所账单** | Kita-Rechnungen / Frais de garde | `Kita_Bern_2025.pdf` | 年度托儿所支出 (S6 子女照看扣除) |

---

## 🔒 隐私与安全承诺
* 此目录已在项目根目录和本目录的 `.gitignore` 中受到**双重严格保护**；
* 无论您存放什么凭证或 PDF，**绝不会被 git 追踪或提交到 GitHub 远端仓库**；
* 所有文本抽取与数值解析均在您本机的 Python 环境中**本地执行**，零外传。
