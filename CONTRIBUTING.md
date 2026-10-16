# Contributing to Swiss Tax Advisor

Thank you for considering contributing to **Swiss Tax Advisor**! 🇨🇭

We welcome contributions from Swiss tax specialists, software engineers, and cross-border commuters. Whether you are adding cantonal tax formulas, fixing communal multipliers, or extending agent platform integrations, your help is appreciated.

---

## 🏛️ Guiding Principles

1. **Deterministic Accuracy**:
   - Tax calculations must **never** be generated or approximated by LLM guesswork.
   - All tax math lives inside deterministic Python scripts (`scripts/`).
   - When cantonal law or tariff tables change, scripts must cite the exact cantonal tax code (e.g., StG Art. X, DBG Art. Y) and circular (*Kreisschreiben*).

2. **Privacy First (Local Sovereignty)**:
   - User profiles and tax records (`user/`) must remain 100% local.
   - Never introduce dependencies or telemetry that transmit user tax figures to external servers.

3. **Multi-Platform Agent Compatibility**:
   - The skill should work out-of-the-box across Claude Code, Cursor, Copilot, Cline, Windsurf, Aider, Devin, and Antigravity.
   - Keep platform rules files synchronized.

---

## 🛠️ Local Development Setup

### Prerequisites
- Python 3.10+
- `git`
- (Optional) `gh` CLI

```bash
# Clone the repository
git clone https://github.com/1316827294/swiss-tax-advisor.git
cd swiss-tax-advisor

# Run tests
python3 -m unittest discover -s scripts -p "test_*.py"
```

---

## 📊 How to Add or Update Cantonal Tax Rules

Swiss tax rates change annually, and communal multipliers (*Steuerfuss*) adjust each December for the following fiscal year.

1. **References Directory** (`references/`):
   - Update or add canton Markdown reference files (e.g., `references/canton_zh.md`, `references/canton_be.md`).
   - Include tax brackets, married splitting formulas, child deductions, and official cantonal tax calculator links.

2. **Engine Scripts** (`scripts/`):
   - Add/update calculation logic in `scripts/canton_tax.py` or dedicated canton modules.
   - Ensure calculations round to the nearest 5 Rappen (0.05 CHF).

3. **Unit Tests** (`scripts/test_tax_engine.py`):
   - Add test cases with verified outputs from official cantonal calculators (e.g., Zurich ZH Services, Bern TaxMe).
   - All tests must pass before submitting a pull request.

---

## 🧪 Testing Your Changes

Run all test suites locally:

```bash
python3 -m unittest discover -s scripts -p "test_*.py"
```

Verify `user_profile.py` state machine:

```bash
python3 scripts/user_profile.py status
```

---

## 📝 Pull Request Guidelines

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/canton-ge-tariffs
   ```
2. Commit your changes with clear semantic commit messages:
   - `feat:` New tax engine capabilities or canton coverage
   - `fix:` Bug fixes in deductions or multipliers
   - `docs:` Documentation improvements
   - `test:` Additional test cases
3. Open a Pull Request on GitHub against `main`.
4. Ensure CI tests pass on all Python versions.

---

## ⚖️ License

By contributing to Swiss Tax Advisor, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
