# Swiss Basic Health Insurance Franchise Optimization Guide (Franchise 300 vs. 2500)

In Switzerland, every resident must hold mandatory health insurance (KVG / LAMal). Every autumn (October–November), insured individuals have a statutory window to change their deductible model (**Franchise**) for the upcoming calendar year (deadline: **November 30**).

---

## 1. The Two Rational Choices

Adult Swiss residents can choose deductibles between CHF 300 and CHF 2,500 (300, 500, 1000, 1500, 2000, 2500).
From a pure actuarial decision perspective, **only two options are mathematically rational**:
- **Franchise 300**: Best for individuals with regular, predictable, or high medical needs.
- **Franchise 2500**: Best for young, healthy individuals with zero or minimal medical needs.
*(Intermediate franchises such as 1000, 1500, or 2000 are mathematically sub-optimal across nearly all premium structures).*

---

## 2. Actuarial Formula & The Break-Even Inflection Point

$$\text{Total Out-of-Pocket} = (12 \times \text{Monthly Premium}) + \text{Franchise Paid} + \min(\text{Remaining} \times 10\%, \text{CHF } 700)$$

### Typical Premium Spread
- Premium Difference: Choosing Franchise 2500 saves approximately **CHF 120 - CHF 150 per month** in fixed premiums, which equals **CHF 1,440 - CHF 1,800 per year** in guaranteed cash savings.
- Deductible Difference: Franchise 2500 requires you to absorb an extra **CHF 2,200** (2500 - 300) before insurance begins co-paying.
- Co-pay buffer: 10% Selbstbehalt up to max CHF 700.

### 🎯 The Inflection Point: ~ CHF 1,800 - 2,000 / year
- If your annual healthcare spending is **under CHF 1,800**: **Franchise 2500 is mathematically superior** (saves up to CHF 1,200+ net cash).
- If your annual healthcare spending exceeds **CHF 2,000**: **Franchise 300 is mathematically superior**.

---

## 3. Decision Command

Execute deterministic calculation:
```bash
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py franchise \
  --spend 1200 \
  --premium-300 450 \
  --premium-2500 310
```
