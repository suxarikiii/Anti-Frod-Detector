<h1 align="center">Graph / Refund Relations Service</h1>

The Graph / Refund Relations Service builds a refund relations graph for suspicious refund approval detection.

It is responsible for:

* Graph DB integration;
* refund relations graph;
* entities: Customer, Order, ReturnRequest, SupportAgent, ProductCategory, Decision;
* relation features for scoring;
* consuming `dataset.normalized`;
* publishing `refund.relations.built`.

<h2 align="center">Graph Entities</h2>

```text
Customer
Order
ReturnRequest
SupportAgent
Decision
ProductCategory
```

<h2 align="center">Graph Edges</h2>

```text
Customer --PLACED_ORDER--> Order
Customer --REQUESTED_RETURN--> ReturnRequest
Order --HAS_RETURN_REQUEST--> ReturnRequest
ReturnRequest --DECIDED_BY--> SupportAgent
SupportAgent --APPROVED_RETURN--> ReturnRequest
SupportAgent --DECLINED_RETURN--> ReturnRequest
Order --CONTAINS_CATEGORY--> ProductCategory
Customer --REPEATED_REFUND_PATTERN--> Customer
SupportAgent --REPEATED_APPROVAL_PATTERN--> Customer
```

<h2 align="center">Features for Scoring</h2>

```text
customerReturnCount
customerApprovedRefundCount
agentApprovalRate
agentManualOverrideRate
agentCustomerInteractionCount
refundAmountRatio
sameReasonRefundCount
clusterSize
strongestRelationType
```

<h2 align="center">Events</h2>

Consumes:

```text
dataset.normalized
```

Publishes:

```text
refund.relations.built
```
