<h1 align="center">Team Roles and Weekly Reports</h1>

This document describes team workflow, responsibilities, weekly report ownership, and contribution tracking rules.

The team works on a startup-track MVP called **Fraud & Abuse Detection System**.

The current MVP domain is suspicious refund approvals in e-commerce support workflows.

<h2 align="center">Team Responsibilities</h2>

<h2 align="center">Amir - Upload / Ingestion Service + Nginx</h2>

Responsible for:

* CSV dataset upload;
* dataset metadata;
* dataset preview;
* analysis job creation;
* analysis status endpoint;
* publishing `dataset.uploaded`;
* Nginx routing for backend APIs.

<h2 align="center">Anya - ML / Data Normalization</h2>

Responsible for:

* synthetic refund dataset;
* clean and dirty business CSV examples;
* column mapping rules;
* normalization into internal refund approval format;
* publishing `dataset.normalized`.

<h2 align="center">Nikita - Graph / Relations Service</h2>

Responsible for:

* Graph DB integration;
* refund relations graph;
* entities: Customer, Order, ReturnRequest, SupportAgent, ProductCategory, Decision;
* relation features for scoring;
* publishing `refund.relations.built`.

<h2 align="center">Ernest - Kotlin Scoring Service</h2>

Responsible for:

* refund approval risk score;
* risk levels;
* scoring rules;
* explanations;
* suspicious refund approvals API;
* consuming `refund.relations.built`;
* publishing `refund.scoring.completed`.

<h2 align="center">Islam - Frontend Dashboard</h2>

Responsible for:

* upload dataset page;
* preview / mapping page;
* analysis status page;
* suspicious refund approvals table;
* refund approval details page;
* support agent and customer context UI.

<h2 align="center">Amina - DevOps / Infrastructure</h2>

Responsible for:

* Docker Compose;
* PostgreSQL;
* RabbitMQ;
* Graph DB;
* Nginx integration;
* local and VM deployment.

<h2 align="center">Working Branches</h2>

The repository uses several main working branches based on project areas:

| Branch | Responsibility |
| --- | --- |
| `backend` | Backend services, APIs, business logic, database interaction, and refund approval risk endpoints. |
| `frontend` | Analyst dashboard, upload flow, status page, suspicious refund approvals table, and details pages. |
| `devops` | Docker setup, VM deployment, environment configuration, infrastructure, and CI/CD. |
| `ml` | Synthetic refund datasets, normalization, ML-assisted scoring, anomaly detection, and validation metrics. |

The working branches are permanent and should not be deleted after merging into `main`.

<h2 align="center">Progress Reporting</h2>

Each team member should regularly report:

* what was done;
* what is currently in progress;
* what problems or blockers appeared;
* what is planned next.

Recommended update format:

```text
Done:
- ...

In progress:
- ...

Problems:
- ...

Next:
- ...
```

<h2 align="center">Weekly Report Schedule</h2>

Week 1 report is not required, so weekly report responsibility starts from Week 2.

| Week | Responsible Pair |
| --- | --- |
| Week 2 | Amir + Ernest |
| Week 3 | Anna + Aminat |
| Week 4 | Islam + Nikita |
| Week 5 | Amir + Ernest |
| Week 6 | Anna + Aminat |
| Week 7 | Islam + Nikita |

<h2 align="center">Responsibilities of the Weekly Report Pair</h2>

Each weekly report pair is responsible for organizing and preparing the weekly project update.

The responsible pair should:

* collect weekly progress information from all team members;
* prepare the weekly report using the required template;
* aggregate individual updates;
* prepare the structure for the weekly video;
* organize sprint planning notes;
* update GitHub board tasks;
* describe problems, blockers, and story points;
* prepare or record the demo.

The responsible pair coordinates the weekly report process, but every team member must still provide information about their own work.

<h2 align="center">Individual Contribution Tracking</h2>

Each team member should make their contribution visible through:

* assigned GitHub issues;
* pull requests;
* commits;
* weekly updates;
* notes in weekly reports;
* demo participation if relevant.

<h2 align="center">Documentation Updates</h2>

Documentation should be updated when changes affect:

* architecture;
* API behavior;
* data model;
* deployment;
* demo flow;
* team process;
* weekly reports.

The documentation is expected to evolve together with the MVP.
