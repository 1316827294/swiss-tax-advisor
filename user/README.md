# 用户数据目录 / User Data Directory

此目录由 **Swiss Tax Advisor Skill** 自动管理。所有文件均存储在您的本地设备，不会上传到任何服务器。

> This directory is managed automatically by the Swiss Tax Advisor AI skill. All data stays local — nothing is ever uploaded.

---

## 文件说明

| 文件 | 说明 |
|---|---|
| `profile.json` | 您的个人档案（canton、婚姻状态、通勤方式等）|
| `tax_YYYY.json` | 每税年的收入与抵扣数据 |
| `reports/YYYY/` | AI 生成的报税文件（Steuerdossier、eTax 指南等）|
| `profile.example.json` | 档案格式示例（参考用，不会被 AI 读取）|

---

## 隐私保护

- 所有 `.json` 文件和 `reports/` 目录已通过 `.gitignore` 排除在 git 追踪之外
- 如需备份，请手动复制此目录到安全位置
- 如需重置，删除 `profile.json` 即可：下次对话 AI 将重新进行引导面谈
