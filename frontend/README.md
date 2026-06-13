<h1 align="center">Frontend Dashboard</h1>

The frontend dashboard supports the analyst workflow for suspicious refund approvals in e-commerce support.

<h2 align="center">Pages</h2>

```text
Upload Dataset Page
Dataset Preview / Mapping Page
Analysis Status Page
Suspicious Refund Approvals Page
Refund Approval Details Page
Support Agent Summary Page
Customer Return History Page
```

<h2 align="center">Main Suspicious Approvals Table</h2>

Columns:

```text
returnId
orderId
customerId
supportAgentId
refundAmount
decision
riskScore
riskLevel
topReason
```

<h2 align="center">Refund Approval Details Page</h2>

The details page should show:

```text
risk score
risk level
explanations
order details
return request details
customer return history
support agent approval behavior
related refund approvals
```

<h2 align="center">Main User Flow</h2>

1. Upload an e-commerce refund dataset.
2. Review dataset preview.
3. Confirm or adjust column mapping.
4. Start analysis.
5. Watch analysis status.
6. Open suspicious refund approvals.
7. Investigate one refund approval.
8. Review customer return history, support agent approval behavior, and related refund approvals.
