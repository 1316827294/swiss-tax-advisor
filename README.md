# Swiss Tax Advisor

A Python library that provides Swiss tax advisory calculations and utilities for personal and business tax reporting. It includes functions for income tax estimation, VAT handling, and tax filing assistance.

## Features
- Income tax computation for Swiss cantons
- VAT calculation and validation
- Helper utilities for tax form generation

## Installation
```bash
pip install swiss-tax-advisor
```

## Usage
```python
from swiss_tax_advisor import calculate_income_tax

tax = calculate_income_tax(income=85000, canton='Zurich')
print(tax)
```

## License
This project is licensed under the Apache License 2.0.
