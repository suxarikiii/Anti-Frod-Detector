<h1 align="center">API Contracts</h1>

This document lists MVP API endpoints for Fraud & Abuse Detection System.

<h2 align="center">Upload Service</h2>

```text
GET /api/datasets/health
POST /api/datasets/upload
GET /api/datasets/{datasetId}/preview
GET /api/analysis/{jobId}/status
```

Example analysis status response:

```json
{
  "jobId": "job_456",
  "datasetId": "dataset_123",
  "status": "SCORING",
  "updatedAt": "2026-06-01T10:12:00Z"
}
```

<h2 align="center">Scoring Service</h2>

```text
GET /api/scoring/health
GET /api/scoring/datasets/{datasetId}/suspicious-approvals
GET /api/scoring/returns/{returnId}/risk
GET /api/scoring/agents/{agentId}/risk-summary
POST /api/scoring/datasets/{datasetId}/recalculate
```

Example suspicious approvals response:

```json
[
  {
    "returnId": "return_123",
    "orderId": "order_456",
    "customerId": "customer_789",
    "supportAgentId": "agent_001",
    "refundAmount": 249.99,
    "decision": "APPROVED",
    "riskScore": 84,
    "riskLevel": "HIGH",
    "topReason": "Refund approved without evidence for a high-value order"
  }
]
```

<h2 align="center">Relations Service</h2>

```text
GET /api/relations/health
GET /api/relations/returns/{returnId}
GET /api/relations/customers/{customerId}
GET /api/relations/agents/{agentId}
POST /api/relations/datasets/{datasetId}/rebuild
```

Example relation summary response:

```json
{
  "returnId": "return_123",
  "customerReturnCount": 8,
  "agentApprovalRate": 0.94,
  "agentCustomerInteractionCount": 5,
  "strongestRelationType": "REPEATED_AGENT_CUSTOMER_PAIR"
}
```

<h2 align="center">ML Service</h2>

```text
GET /api/ml/health
GET /api/ml/datasets/{datasetId}/mapping
```

Example mapping response:

```json
{
  "datasetId": "dataset_123",
  "mapping": {
    "buyer_id": "customer_id",
    "purchase_id": "order_id",
    "refund_request_id": "return_id",
    "support_user_id": "support_agent_id",
    "approval_status": "decision"
  }
}
```
