<h1 align="center">Scoring Rules</h1>

The MVP uses rule-based scoring to calculate a refund approval risk score.

| Rule | Condition | Score Impact |
| --- | --- | --- |
| NO_EVIDENCE | Refund approved without evidence | +25 |
| HIGH_VALUE_REFUND | Refund amount is above threshold | +20 |
| FULL_AMOUNT_REFUND | Refund amount is close to order amount | +15 |
| FAST_APPROVAL | Approval happened too quickly | +15 |
| MANUAL_OVERRIDE | Manual override was used | +20 |
| AGENT_HIGH_APPROVAL_RATE | Agent approval rate is unusually high | +30 |
| CUSTOMER_FREQUENT_RETURNS | Customer has many refund requests | +20 |
| REPEATED_AGENT_CUSTOMER_PAIR | Same agent repeatedly approves same customer | +25 |
| SUSPICIOUS_CLUSTER | Approval belongs to suspicious graph cluster | +25 |

<h2 align="center">Risk Levels</h2>

```text
0-30 LOW
31-60 MEDIUM
61-80 HIGH
81-100 CRITICAL
```
