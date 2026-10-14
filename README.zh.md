# 🇨🇭 瑞士智能报税与节税助手 (`swiss-tax-advisor`)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [简体中文](README.zh.md)

---

> **面向 LLM Agent 的瑞士报税底稿生成、税务局风控自检与主动节税开源 Skill。**  
> 兼容 **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor** 以及 **OpenClaw**。

---

## 🌟 核心亮点与特性

1. **零外部重依赖**：完全基于 Python 3.10+ 标准库（`math`, `argparse`, `json`, `sys`, `unittest`），免 `pip install`，任何系统克隆即跑。
2. **确定性高精度（严禁 LLM 口算心算）**：硬性门禁杜绝大模型在瑞士累进阶梯税率表（Progressionstarif）上的幻觉，统一采用**生丁（Rappen，1 CHF = 100 Rappen）与瑞士法定 5-Rappen 舍入**。
3. **税务局官方稽查风控雷达（0~100 分）**：深度模拟瑞士各州税务局初审筛选算法（*Risikobasierte Fallauswahl*），在提交申报前提前排查 S7 进修超标（>15%）、无票据抵扣、私家车与公交冲突等高危红线。
4. **六语原生自适应**：提供中文、英语、德语、法语、意大利语、西班牙语全量文档，LLM 会根据你的提问语言自动生成对应语言的申报底稿与专业报告。
5. **完整覆盖 2025/2026 瑞士全税目扣除体系**：
   - S1 通勤（公共交通实报实销、私家车 0.70/km 严格条件、自行车 700 CHF）；
   - S2 餐饮定额（外食 3,200 CHF / 食堂餐补 1,600 CHF）；
   - S3 医疗自负（5% 净收入起扣线与跨年压茬 Bunching 策略）；
   - S4 第三支柱养老金（2025/2026 雇员上限 7,258 CHF / 自雇 20% 最高 36,288 CHF，多账户分批提取策略）；
   - S6 托儿所 Kita（联邦与伯尔尼最高 25,500 CHF / 孩子）；
   - S7 职业进修（最高 12,700 CHF，附雇主证明信策略）；
   - S8 房产维护（实际费用 vs Pauschal 定额、光伏与节能改造 2 年结转新规、公寓更新基金 Erneuerungsfonds）；
   - S9 独立工作间（BGE 140 II 157 严苛双条件折算）；
   - 抚养费（Alimente）：前配偶/未成年子女 100% 扣除，成年子女严格不可抵扣；
   - 双职工特别扣除（Zweitverdienerabzug）：较低收入 50%（最高 14,100 CHF）。
6. **三大高阶决策辅助引擎**：
   - **源泉税转正申报决策器 (Quellensteuer NOV)**：测算 B 证居民转正申报是退税还是倒补税（转正终身不可撤销，防坑必备）；
   - **基础医保免赔额精算器 (Franchise 300 vs 2500)**：每年 10~11 月基于医疗年支出拐点（~1,800-2,000 CHF）精算最省钱方案；
   - **跨州/跨市镇税负对比沙盘 (Relocation What-If)**：输入不同州或市镇（如 Bern vs Zug），精算税率乘数（Steuerfuss）带来的现金差异。

---

## ⚡ 快速开始与测试

运行离线单元测试套件：
```bash
python3 skills/swiss-tax-advisor/scripts/test_tax_engine.py
```
*(预期结果：`Ran 12 tests in 0.001s, OK`)*

### 命令行常用指令

```bash
# 1. 精确计算瑞士税额（伯尔尼，已婚，毛收入 17 万，含 3a 与托儿费抵扣）
python3 skills/swiss-tax-advisor/scripts/swiss_tax_math.py \
  --gross-income 170000 --canton BE --civil-status MARRIED --children 1 \
  --deductions '{"s1": 3300, "s4": 7258, "s6": 18000}' --json

# 2. 测算当前收入区间的真实边际税率与 3a 填满能省多少现金
python3 skills/swiss-tax-advisor/scripts/marginal_rate_calc.py \
  --income 120000 --canton ZH --deduction 7258 --category PILLAR_3A --json

# 3. 模拟双职工家庭结婚税收惩罚 (Marriage Penalty)
python3 skills/swiss-tax-advisor/scripts/family_marriage_sim.py \
  --earner-a 110000 --earner-b 75000 --canton BE --children 1 --json

# 4. 运行税务局官方初审风控雷达自检
python3 skills/swiss-tax-advisor/scripts/audit_risk_evaluator.py \
  --income 85000 --education 15000 --missing-proofs --json

# 5. 评估源泉税 (Quellensteuer) 是否应该申请 NOV 转正申报
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 110000 --canton ZH --deductions '{"s4": 7258, "s1": 3300}'

# 6. 测算基础医保 Franchise 选 300 还是 2500 更省钱
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py franchise \
  --spend 1400 --premium-300 450 --premium-2500 310

# 7. 模拟跨州搬家税负差异（如从伯尔尼搬到楚格）
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py relocation \
  --income 150000 --from-canton BE --to-canton ZG
```

---

## 🔒 隐私合规与数据主权 (Swiss FADP / DSG)

所有金融运算均在本地机器执行，绝不向未授权第三方上传明细。内置瑞士数据保护法脱敏规则，自动星号脱敏瑞士社保号（AHV 756.xxxx.xxxx.xx）与银行账号（IBAN CHxx...）。

---

## 📄 开源许可证

遵循 **MIT 开源许可证**，详见 `LICENSE`。
