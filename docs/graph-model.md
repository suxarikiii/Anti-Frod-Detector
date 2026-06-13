<h1 align="center">Graph Model</h1>

Graph DB stores refund-related relationships used for suspicious refund approval detection.

<h2 align="center">Vertices</h2>

```text
Customer
Order
ReturnRequest
SupportAgent
ProductCategory
Decision
```

<h2 align="center">Edges</h2>

```text
Customer --PLACED_ORDER--> Order
Customer --REQUESTED_RETURN--> ReturnRequest
Order --HAS_RETURN_REQUEST--> ReturnRequest
ReturnRequest --DECIDED_BY--> SupportAgent
SupportAgent --APPROVED_RETURN--> ReturnRequest
SupportAgent --DECLINED_RETURN--> ReturnRequest
Order --CONTAINS_CATEGORY--> ProductCategory
SupportAgent --REPEATED_APPROVAL_PATTERN--> Customer
```

<h2 align="center">Use Cases</h2>

* find customers with frequent refunds;
* find agents with abnormal approval behavior;
* find repeated customer-agent approval patterns;
* find suspicious approval clusters;
* provide relation features to scoring service.
