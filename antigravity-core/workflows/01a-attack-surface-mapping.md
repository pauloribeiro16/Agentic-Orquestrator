---
description: "Phase 1a — Attack Surface Mapping"
phase: 1
nist_ssdf: "PW.1 — Design Software to Meet Security Requirements"
asvs_reference: "asvs-v1-architecture.md (V1.1 — Secure Software Development Lifecycle)"
triggers: "Called by 00-pipeline-orchestrator.md"
---

# Phase 1a: Attack Surface Mapping

**Purpose:** Systematically identify and catalog every point where an attacker could interact with the feature under review. This creates the foundation for the Data Flow Diagram (01b) and STRIDE Analysis (01c).

---

## Step 1: Entry Point Discovery

**Action:** Analyze the feature's code, configuration, and the completed Feature Brief to identify all entry points where external data enters the system.

**Identify and catalog each of the following:**

### 1.1 HTTP/API Entry Points
For each endpoint introduced or modified by this feature, record:

| Field | What to capture |
|---|---|
| Route | The URL pattern (e.g., `POST /api/v1/users/:id/upload`) |
| HTTP Method | GET, POST, PUT, PATCH, DELETE |
| Input Sources | Query params, path params, request body, headers, cookies |
| Content-Type | What payload formats are accepted (JSON, multipart, XML) |
| Authentication | Is auth required? What mechanism? (JWT, session, API key, none) |
| Authorization | What role/permission check is enforced? |
| Rate Limiting | Is rate limiting applied? What threshold? |

### 1.2 WebSocket / Real-time Entry Points
If the feature uses WebSocket, Server-Sent Events, or similar:
- Connection endpoint and upgrade path.
- Message types accepted.
- Authentication on connection establishment.

### 1.3 Background / Async Entry Points
If the feature processes messages from queues, cron jobs, or event-driven triggers:
- Queue/topic names and message schema.
- Source of the messages (internal service, external webhook, user-triggered).
- Whether message content is validated before processing.

### 1.4 File-Based Entry Points
If the feature accepts file uploads or reads external files:
- File types accepted and maximum size limits.
- Where files are stored (local filesystem, S3, database BLOB).
- Whether file content is parsed, executed, or served back to users.

---

## Step 2: External Entity Identification

**Action:** Identify all external systems and actors that interact with this feature.

**Catalog each entity:**

| Entity Type | Examples |
|---|---|
| **Human Users** | End users, administrators, support agents |
| **External APIs** | Third-party services the feature calls (payment gateways, email services, etc.) |
| **Internal Services** | Other microservices or internal APIs the feature communicates with |
| **Data Stores** | Databases, caches, file storage, message queues |
| **CI/CD Systems** | Build pipelines, deployment hooks, monitoring agents |

For each entity, record:
- **Direction:** Inbound (sends data to the feature), Outbound (receives data from the feature), or Both.
- **Trust Level:** Trusted (internal, authenticated), Semi-Trusted (authenticated external), Untrusted (public internet).
- **Protocol:** HTTPS, gRPC, database wire protocol, AMQP, etc.

---

## Step 3: Trust Boundary Identification

**Action:** Identify every point where data crosses a change in trust level.

**Common trust boundaries to look for:**

1. **Public Internet → Application Server** — All user-facing HTTP requests.
2. **Application Server → Database** — Queries carrying user-supplied data.
3. **Application Server → External API** — Outbound calls where the response is used in business logic.
4. **Application Server → File System** — File writes, reads, or serves.
5. **Frontend → Backend** — Client-side data sent to server (never trust client-side validation alone).
6. **Service → Service** — Internal microservice communication (verify mutual auth).
7. **CI/CD → Production** — Deployment pipelines pushing to production environments.

For each boundary, note:
- **What crosses it:** Data type and sensitivity.
- **What validates it:** Authentication, encryption, schema validation.
- **What's missing:** Any boundary that lacks validation or encryption.

---

## Step 4: Data Asset Inventory

**Action:** List every piece of sensitive data this feature touches, where it lives, and how it moves.

| Data Asset | Classification | At Rest (where stored) | In Transit (how moved) | Who Can Access |
|---|---|---|---|---|
| _e.g., User password_ | _Credential_ | _PostgreSQL (hashed)_ | _HTTPS POST body_ | _Auth service only_ |
| _e.g., Session token_ | _Authentication_ | _Redis_ | _HTTP Cookie / Auth header_ | _User + server_ |
| _e.g., Uploaded file_ | _User content_ | _S3 bucket_ | _HTTPS multipart upload_ | _Owner + admin_ |

---

## Step 5: Compile Attack Surface Map

**Action:** Produce a structured attack surface map as part of the `[feature]-threat-report.md` output.

**Format:**

```markdown
## Attack Surface Map: [Feature Name]

### Entry Points
[Table from Step 1.1–1.4]

### External Entities
[Table from Step 2]

### Trust Boundaries
[List from Step 3 with notes on what's validated and what's missing]

### Data Assets
[Table from Step 4]

### Initial Observations
[List any immediately obvious gaps: unprotected endpoints, missing auth, sensitive data in transit without encryption, etc. These will be fully analyzed in the STRIDE phase.]
```

**Next:** Pass this output to `01b-data-flow-diagram.md` and `01c-stride-analysis.md`.
