<h1 align="center">Data Format</h1>

The MVP dataset format describes e-commerce orders, return requests, and support decisions used for suspicious refund approval detection.

<h2 align="center">Combined CSV Columns</h2>

```text
order_id
customer_id
return_id
support_agent_id
order_amount
refund_amount
product_category
return_reason
evidence_provided
decision
manual_override
decision_time_minutes
timestamp
```

<h2 align="center">Example CSV</h2>

```csv
order_id,customer_id,return_id,support_agent_id,order_amount,refund_amount,product_category,return_reason,evidence_provided,decision,manual_override,decision_time_minutes,timestamp
order_001,cust_001,ret_001,agent_001,249.99,249.99,electronics,item_not_as_described,false,APPROVED,true,2,2026-06-01T10:00:00Z
order_002,cust_002,ret_002,agent_002,39.99,10.00,clothing,size_issue,true,APPROVED,false,15,2026-06-01T10:30:00Z
```

Synthetic data should include normal and suspicious cases.

<h2 align="center">Suspicious Scenarios</h2>

* high-value refund without evidence;
* fast approval;
* manual override;
* customer with frequent refunds;
* support agent with high approval rate;
* repeated customer-agent approvals;
* suspicious refund cluster.
