<h1 align="center">Team Roles and Weekly Reports</h1>

<p align="center">
  This document describes team workflow, weekly report responsibilities, and contribution tracking rules.
</p>

<p align="center">
  The document is a work in progress and may be updated as the project evolves.
</p>

---

<h2 align="center">General Team Workflow</h2>

The team works on a startup-track MVP called **Fraud & Abuse Detection System**.

The project is divided into several main areas:

* backend;
* frontend;
* DevOps;
* ML / data generation;
* documentation;
* weekly reporting and demo preparation.

Each team member is responsible for their assigned tasks and should keep the team updated about their progress, blockers, and next steps.

GitHub should be used as the main place for tracking project work:

* issues should describe concrete tasks;
* branches should match the main project areas;
* pull requests should describe completed changes;
* project board should show the current task status.

---

<h2 align="center">Working Branches</h2>

The repository uses several main working branches based on project areas:

<table align="center">
  <tr>
    <th align="center">Branch</th>
    <th align="center">Responsibility</th>
  </tr>
  <tr>
    <td align="center"><code>backend</code></td>
    <td align="center">Backend services, APIs, business logic, database interaction, and risk score endpoints.</td>
  </tr>
  <tr>
    <td align="center"><code>frontend</code></td>
    <td align="center">Analyst dashboard, UI components, frontend logic, tables, filters, and user details pages.</td>
  </tr>
  <tr>
    <td align="center"><code>devops</code></td>
    <td align="center">Docker setup, VM deployment, environment configuration, infrastructure, and CI/CD.</td>
  </tr>
  <tr>
    <td align="center"><code>ml</code></td>
    <td align="center">Synthetic dataset generation, ML-assisted scoring, anomaly detection, and validation metrics.</td>
  </tr>
</table>

The working branches are permanent and should not be deleted after merging into `main`.

---

<h2 align="center">Progress Reporting</h2>

Each team member should regularly report:

* what was done;
* what is currently in progress;
* what problems or blockers appeared;
* what is planned next.

Progress updates should be short, clear, and connected to GitHub issues whenever possible.

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

---

<h2 align="center">Weekly Report Schedule</h2>

Week 1 report is not required, so weekly report responsibility starts from Week 2.

<table align="center">
  <tr>
    <th align="center">Week</th>
    <th align="center">Responsible Pair</th>
  </tr>
  <tr>
    <td align="center">Week 2</td>
    <td align="center">Amir + Ernest</td>
  </tr>
  <tr>
    <td align="center">Week 3</td>
    <td align="center">Anna + Aminat</td>
  </tr>
  <tr>
    <td align="center">Week 4</td>
    <td align="center">Islam + Nikita</td>
  </tr>
  <tr>
    <td align="center">Week 5</td>
    <td align="center">Amir + Ernest</td>
  </tr>
  <tr>
    <td align="center">Week 6</td>
    <td align="center">Anna + Aminat</td>
  </tr>
  <tr>
    <td align="center">Week 7</td>
    <td align="center">Islam + Nikita</td>
  </tr>
</table>

---

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

---

<h2 align="center">Individual Contribution Tracking</h2>

Each team member should make their contribution visible through:

* assigned GitHub issues;
* pull requests;
* commits;
* weekly updates;
* notes in weekly reports;
* demo participation if relevant.

A good contribution update should answer:

* What task was assigned?
* What was completed?
* What is still in progress?
* What problems appeared?
* What will be done next?

---

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
