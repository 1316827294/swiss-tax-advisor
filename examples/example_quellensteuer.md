# Example: Quellensteuer B-Permit — NOV Ordinary Filing

This example shows a B-permit foreign national having Quellensteuer deducted at source, and evaluating whether to file a NOV (Nachträgliche Ordentliche Veranlagung) to reclaim overpaid taxes.

## Scenario

| Parameter | Value |
|---|---|
| Canton | BE (Bern) |
| Permit | B-Permit (foreign national) |
| Gross Income | CHF 85,000 |
| Quellensteuer Deducted | CHF 14,200 (by employer) |
| Pillar 3a contributions | CHF 7,258 |
| Commute | CHF 3,300 |

## NOV Decision Advisor

```bash
python3 scripts/advanced_advisory.py nov \
  --income 85000 \
  --canton BE \
  --deductions '{"s4": 7258, "s1": 3300, "s2": 3200}'
```

The script returns:
- Estimated total tax if ordinary filing is applied
- Comparison vs. Quellensteuer already deducted
- **Recommendation**: file NOV if estimated refund > CHF 500

## Agent Prompt (English)

> "I'm on a B-permit in Bern. My employer deducts Quellensteuer from my CHF 85,000 salary. I've paid CHF 7,258 into Pillar 3a this year. Should I file a NOV to get a refund? If yes, help me calculate the expected refund and what documents I need."

## Agent Prompt (German)

> "Ich habe eine B-Bewilligung und wohne in Bern. Mein Arbeitgeber zieht Quellensteuer von meinem Lohn ab (85'000 CHF). Ich habe 7'258 CHF in die Säule 3a eingezahlt. Lohnt sich eine NOV-Einreichung und wie viel bekomme ich zurück?"

## Reference

See [`references/quellensteuer_nov_guide.md`](../references/quellensteuer_nov_guide.md) for the full B-permit NOV filing guide including required documents and deadlines.
