<h1 align="center">Project Plan</h1>

This document describes the 7-week MVP plan for **Fraud & Abuse Detection System** after the domain clarification.

The project name remains **Fraud & Abuse Detection System**.

The MVP domain is focused on detecting **suspicious refund approvals in e-commerce support workflows**. The system analyzes order history, return requests, refund amounts, customer behavior, support agent decisions, and relation patterns in order to calculate refund approval risk scores and explain why specific refund approvals may be suspicious.

---

<h2 align="center">Week 1 - Organization, Skeletons, and Domain Alignment</h2>

<h3 align="center">Focus</h3>

* finalize the suspicious refund approval domain;
* keep the project name as **Fraud & Abuse Detection System**;
* update root README and project documentation according to the new MVP domain;
* define the main MVP flow from dataset upload to suspicious refund approval investigation;
* define the first version of the refund dataset format;
* prepare initial synthetic refund datasets:

  * clean synthetic dataset with standard internal column names;
  * dirty business dataset with realistic business-style column names;
* define the first version of column mapping rules;
* create initial service skeletons;
* create basic health-check endpoints;
* prepare mock endpoints for frontend integration;
* prepare Docker Compose skeleton;
* include PostgreSQL, RabbitMQ, Graph DB, Nginx, and service placeholders in the infrastructure plan.

<h3 align="center">Expected Result</h3>

* all team members understand the new refund approval domain;
* documentation is aligned with the new use case;
* service skeletons are started;
* clean and dirty dataset formats are defined;
* mock APIs are agreed and partially prepared;
* RabbitMQ pipeline events are agreed;
* Graph DB role is clear;
* MVP flow is clear and can be explained to TA or mentor.

---

<h2 align="center">Week 2 - Data Format, Upload, and Normalization</h2>

<h3 align="center">Focus</h3>

* finalize CSV format for orders, return requests, and support decisions;
* support a combined refund approval dataset or separate files such as:

  * `orders.csv`;
  * `returns.csv`;
  * `support_decisions.csv`;
* implement dataset upload in Upload / Ingestion Service;
* implement dataset preview for uploaded CSV files;
* create analysis job after dataset upload;
* publish `dataset.uploaded` event from Upload / Ingestion Service;
* consume `dataset.uploaded` in ML / Normalization Service;
* implement normalization from dirty business columns to internal refund approval records;
* validate that both clean and dirty datasets can be processed;
* save normalized refund approval records;
* publish `dataset.normalized` event.

<h3 align="center">Expected Result</h3>

* refund dataset can be uploaded;
* dataset preview works;
* analysis job is created after upload;
* clean synthetic dataset can be processed directly;
* dirty business dataset can be mapped and normalized;
* normalized refund approval records are saved;
* RabbitMQ event flow starts;
* ML / Normalization Service provides a clear normalized data format for other backend services.

---

<h2 align="center">Week 3 - Graph / Relations Model</h2>

<h3 align="center">Focus</h3>

* define graph entities and edges for refund approval analysis;
* use the following core graph entities:

  * Customer;
  * Order;
  * ReturnRequest;
  * SupportAgent;
  * Decision;
  * ProductCategory;
* build relations between customers, orders, return requests, support agents, decisions, and product categories;
* integrate or prepare Graph DB storage;
* consume `dataset.normalized` event;
* generate refund relation features for the scoring service;
* prepare endpoints or mock endpoints for return, customer, and support agent relations;
* publish `refund.relations.built` event.

<h3 align="center">Expected Result</h3>

* graph model works on synthetic refund dataset;
* customer-order-return-agent relations can be represented;
* relation features are available for scoring;
* suspicious relation patterns can be represented;
* Graph / Relations Service can return mock or initial real relation data;
* `refund.relations.built` event is published.

---

<h2 align="center">Week 4 - Scoring and Explanations</h2>

<h3 align="center">Focus</h3>

* implement refund approval risk scoring;
* define risk levels;
* define rule-based scoring logic for suspicious refund approvals;
* consume `refund.relations.built` event;
* calculate risk score for refund approvals;
* generate explanations for risky approvals;
* expose suspicious refund approval endpoints;
* expose refund approval details endpoint;
* expose support agent risk summary endpoint or placeholder;
* publish `refund.scoring.completed` event.

<h3 align="center">Expected Result</h3>

* suspicious refund approvals can be retrieved;
* each suspicious approval has risk score, risk level, and reasons;
* scoring service can explain why a refund approval is risky;
* frontend can consume scoring endpoints through Nginx;
* scoring result is connected to graph relation features.

---

<h2 align="center">Week 5 - Frontend Dashboard and Integration</h2>

<h3 align="center">Focus</h3>

* implement Upload Dataset page;
* implement Dataset Preview / Mapping page;
* implement Analysis Status page;
* implement Suspicious Refund Approvals Dashboard;
* implement Refund Approval Details page;
* prepare Support Agent Summary page or component;
* prepare Customer Return History page or component;
* connect frontend to backend through `/api/...` routes and Nginx;
* display risk score, risk level, explanations, customer history, support agent behavior, and related refund approvals;
* keep mock data fallback where backend endpoints are not fully ready.

<h3 align="center">Expected Result</h3>

* analyst can go through the main MVP flow from upload to investigation;
* frontend works with backend endpoints or mock fallback;
* suspicious refund approvals are visible in dashboard;
* refund approval details page explains the risk;
* frontend uses only `/api/...` routes through Nginx.

---

<h2 align="center">Week 6 - Deployment, Validation, and Stabilization</h2>

<h3 align="center">Focus</h3>

* deploy MVP on VM;
* finalize Docker Compose integration;
* stabilize PostgreSQL, RabbitMQ, Graph DB, Nginx, and services;
* validate the system on synthetic scenarios;
* check that known suspicious cases are detected;
* validate clean and dirty datasets;
* collect validation evidence;
* fix integration bugs;
* improve frontend UX;
* improve project documentation;
* prepare the project for final demo.

<h3 align="center">Expected Result</h3>

* MVP is deployed and can be demonstrated;
* validation evidence is prepared;
* core suspicious refund scenarios are detected;
* system is stable enough for final demo preparation;
* documentation explains how to run, test, and demonstrate the project.

---

<h2 align="center">Week 7 - Final Polish and Video</h2>

<h3 align="center">Focus</h3>

* finalize demo flow;
* prepare final video;
* polish dashboard and explanations;
* finalize documentation;
* prepare personal contribution evidence;
* check that all services are aligned with the MVP domain;
* optionally add bonus features.

<h3 align="center">Expected Result</h3>

* stable final MVP;
* final demo video;
* complete documentation;
* clear personal contribution evidence;
* optional bonus functionality is documented if implemented.

---

<h2 align="center">Final MVP Flow</h2>

By the end of the project, the MVP should demonstrate the following flow:

1. A business user uploads an e-commerce refund dataset.
2. The system shows dataset preview.
3. The system detects or applies column mapping.
4. Raw data is normalized into internal order, return, customer, support agent, and decision entities.
5. The system builds relationships between customers, orders, return requests, support agents, decisions, and product categories.
6. Refund relation features are prepared for scoring.
7. A refund approval risk score is calculated.
8. The system explains why a refund approval is suspicious.
9. An analyst views suspicious refund approvals in the dashboard.
10. The analyst opens a refund approval details page and sees risk score, explanations, customer return history, support agent behavior, and related refund approvals.
11. The project is deployed on a VM and can be demonstrated.

---

<h2 align="center">Main Pipeline Events</h2>

The backend pipeline is asynchronous and uses RabbitMQ.

Main events:

```text
dataset.uploaded
dataset.normalized
refund.relations.built
refund.scoring.completed
pipeline.failed
```

Expected pipeline:

```text
Upload / Ingestion Service
→ publishes dataset.uploaded

ML / Normalization Service
→ consumes dataset.uploaded
→ publishes dataset.normalized

Graph / Relations Service
→ consumes dataset.normalized
→ publishes refund.relations.built

Scoring Service
→ consumes refund.relations.built
→ publishes refund.scoring.completed
```

---

<h2 align="center">Main Analysis Statuses</h2>

The analysis job may use the following statuses:

```text
UPLOADED
NORMALIZING
NORMALIZED
BUILDING_RELATIONS
SCORING
COMPLETED
FAILED
```

---

<h2 align="center">Domain Consistency Rules</h2>

The project name remains:

```text
Fraud & Abuse Detection System
```

The main MVP domain is:

```text
suspicious refund approvals in e-commerce support
```

Primary terms to use across documentation:

```text
orders
return requests
refund approvals
support decisions
support agents
customer return history
support agent approval behavior
refund approval risk score
refund relation graph
suspicious refund approvals
```

Avoid using old generic fraud terms as the main project focus:

```text
multi-accounting
self-referral
promo abuse
shared IP
shared device
suspicious users
related accounts
generic user behavior fraud
```

These terms may only be mentioned as historical context or possible future expansion, not as the current MVP focus.
