<h2 align="center">Branch Structure</h2>

The repository uses several main working branches based on project areas:

```text
backend
frontend
devops
ml
```

Each branch is responsible for a specific part of the project:

<table align="center">
  <tr>
    <th align="center">Branch</th>
    <th align="center">Responsibility</th>
  </tr>
  <tr>
    <td align="center"><code>backend</code></td>
    <td align="center">Backend services, APIs, business logic, database interaction</td>
  </tr>
  <tr>
    <td align="center"><code>frontend</code></td>
    <td align="center">Analyst dashboard, UI components, frontend logic</td>
  </tr>
  <tr>
    <td align="center"><code>devops</code></td>
    <td align="center">Deployment, Docker, VM configuration, CI/CD, infrastructure</td>
  </tr>
  <tr>
    <td align="center"><code>ml</code></td>
    <td align="center">Synthetic data generation, ML-assisted scoring, anomaly detection, validation metrics</td>
  </tr>
</table>

---

<h2 align="center">Working with Branches</h2>

All changes should be committed to the branch that matches the area of work.

Examples:

```text
backend  -> event ingestion API, database models, scoring endpoints
frontend -> dashboard pages, tables, filters, user details UI
devops   -> Docker setup, VM deployment, environment configuration
ml       -> dataset generator, anomaly detection, metrics calculation
```

If a task affects multiple areas, the team should decide where the main change belongs. If needed, the task can be split into several pull requests across different branches.

---

<h2 align="center">Pull Request Flow</h2>

The usual flow is:

```text
backend / frontend / devops / ml -> main
```

Each pull request should be created from one of the working branches into `main`.

Before merging into `main`, the pull request should be reviewed by at least one team member.

The working branches `backend`, `frontend`, `devops`, and `ml` are permanent branches and should not be deleted after merging.

---

<h2 align="center">Commit Messages</h2>

Commit messages should be short and clear.

Recommended format:

```text
type: short description
```

Examples:

```text
feat: add event ingestion endpoint
fix: correct risk score calculation
docs: update architecture overview
chore: add initial project structure
refactor: simplify user risk service
test: add scoring tests
```

Recommended commit types:

* `feat` — new functionality;
* `fix` — bug fixes;
* `docs` — documentation changes;
* `chore` — repository setup, configuration, maintenance;
* `refactor` — code improvements without changing behavior;
* `test` — tests.
