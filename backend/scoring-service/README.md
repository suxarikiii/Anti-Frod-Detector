<h1 align="center">Scoring Service</h1>

<p align="center">
  The service provides risk scores, risk levels, explanations, and mock suspicious users for the frontend during the first development stage.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kotlin-1.9.25-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Spring%20Boot-3.3.5-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot" />
  <img src="https://img.shields.io/badge/Gradle-Kotlin%20DSL-02303A?style=for-the-badge&logo=gradle&logoColor=white" alt="Gradle" />
  <img src="https://img.shields.io/badge/Java-17-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java 17" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Spring%20Web-REST%20API-6DB33F?style=for-the-badge&logo=spring&logoColor=white" alt="Spring Web" />
  <img src="https://img.shields.io/badge/Actuator-Health%20Checks-6DB33F?style=for-the-badge&logo=spring&logoColor=white" alt="Spring Boot Actuator" />
</p>

<h2 align="center">Service Flow</h2>

```mermaid
flowchart TD
    A[Frontend] -->|GET suspicious users| B[Scoring Controller]
    A -->|GET user risk| B
    A -->|POST recalculate| B

    B --> C[Scoring Service]
    C --> D[Mock Risk Features]
    D --> E[Rule-based Scoring]

    E --> F[Risk Reasons]
    F --> G[Risk Score]
    G --> H[Risk Level]

    H --> I[JSON API Response]
    F --> I
    I --> A
```

<h2 align="center">Rule-based Scoring Draft</h2>

<div align="center">

<table>
  <thead>
    <tr>
      <th align="center">Feature</th>
      <th align="center">Condition</th>
      <th align="center">Score Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">Same device usage</td>
      <td align="center"><code>sameDeviceUserCount &gt;= 3</code></td>
      <td align="center"><code>+30</code></td>
    </tr>
    <tr>
      <td align="center">Same IP usage</td>
      <td align="center"><code>sameIpUserCount &gt;= 3</code></td>
      <td align="center"><code>+20</code></td>
    </tr>
    <tr>
      <td align="center">Promo abuse</td>
      <td align="center"><code>promoUsageCount &gt;= 5</code></td>
      <td align="center"><code>+20</code></td>
    </tr>
    <tr>
      <td align="center">Suspicious referral</td>
      <td align="center"><code>hasSuspiciousReferral == true</code></td>
      <td align="center"><code>+30</code></td>
    </tr>
  </tbody>
</table>

</div>


<h2 align="center">API Endpoints</h2>

<div align="center">

<table>
  <thead>
    <tr>
      <th align="center">Endpoint</th>
      <th align="center">Command</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">Health Check</td>
      <td align="left"><code>curl http://localhost:8081/api/scoring/health</code></td>
    </tr>
    <tr>
      <td align="center">Get Suspicious Users</td>
      <td align="left"><code>curl http://localhost:8081/api/scoring/datasets/demo/suspicious-users | jq</code></td>
    </tr>
    <tr>
      <td align="center">Get User Risk</td>
      <td align="left"><code>curl http://localhost:8081/api/scoring/users/user_123/risk | jq</code></td>
    </tr>
    <tr>
      <td align="center">Recalculate Dataset</td>
      <td align="left"><code>curl -X POST http://localhost:8081/api/scoring/datasets/demo/recalculate | jq</code></td>
    </tr>
  </tbody>
</table>

</div>


<h2 align="center">Example Suspicious User Response</h2>

```json
{
  "userId": "user_123",
  "riskScore": 87,
  "riskLevel": "HIGH",
  "topReason": "Same device used by 5 users",
  "relatedUsersCount": 6
}
```

<h2 align="center">Local Run, Build and Test</h2>

<div align="center">

<table>
  <thead>
    <tr>
      <th align="center">Action</th>
      <th align="center">Command</th>
      <th align="center">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">Run service</td>
      <td align="left"><code>./gradlew bootRun</code></td>
      <td align="left">Starts the service on <code>http://localhost:8081</code></td>
    </tr>
    <tr>
      <td align="center">Build and test</td>
      <td align="left"><code>./gradlew clean build</code></td>
      <td align="left">Compiles the project and runs tests</td>
    </tr>
  </tbody>
</table>

</div>

