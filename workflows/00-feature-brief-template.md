---
description: "Feature Brief Template — Pipeline Input"
usage: "Copy this template, fill in all sections, and provide it to the pipeline orchestrator to begin the DevSecOps workflow."
---

# Feature Brief

> **Instructions:** Fill in every section below before triggering the DevSecOps pipeline. Fields marked with `[REQUIRED]` must be completed — the pipeline will not proceed without them. Fields marked `[OPTIONAL]` improve the quality of the analysis but are not blocking.

---

## 1. Feature Identity

- **Feature Name:** `[REQUIRED]` _A concise name (e.g., "User File Upload Service", "Password Reset Flow")_
- **Owner / Team:** `[REQUIRED]` _Who is responsible for this feature_
- **Target Branch / PR:** `[OPTIONAL]` _Branch name or PR number if code already exists_
- **Target Release Date:** `[OPTIONAL]` _When this is expected to ship_

---

## 2. Feature Description

`[REQUIRED]` _Describe what this feature does in 3–5 sentences. Focus on the user-facing behavior and the business purpose._

```
[Write here]
```

---

## 3. Data Classification

`[REQUIRED]` _Check all that apply. This determines which ASVS chapters and threat categories are activated._

- [ ] **PII (Personally Identifiable Information)** — Names, emails, phone numbers, addresses
- [ ] **Authentication Credentials** — Passwords, tokens, API keys, secrets
- [ ] **Financial Data** — Payment info, billing, transactions
- [ ] **Health / Medical Data** — PHI, health records
- [ ] **Internal / Business Confidential** — Internal docs, strategies, non-public metrics
- [ ] **Public Data** — Content intended for public consumption

**Data at rest:** _Where is this data stored? (e.g., PostgreSQL, Redis, S3, localStorage)_
```
[Write here]
```

**Data in transit:** _How does this data move? (e.g., HTTPS API calls, WebSocket, message queue)_
```
[Write here]
```

---

## 4. User Roles & Access

`[REQUIRED]` _List every user role that interacts with this feature and what they can do._

| Role | Permissions | Authentication Method |
|---|---|---|
| _e.g., Anonymous User_ | _Can view public listings_ | _None_ |
| _e.g., Authenticated User_ | _Can upload files, view own files_ | _JWT Bearer Token_ |
| _e.g., Admin_ | _Can view/delete any user's files_ | _JWT + Role Check_ |

---

## 5. Technology Stack

`[REQUIRED]` _Check all that apply and specify versions/frameworks._

**Backend:**
- [ ] **Node.js** — Framework: _________ (Express, Fastify, NestJS, Koa, etc.)
- [ ] **Python** — Framework: _________ (FastAPI, Django, Flask, etc.)
- [ ] **Other:** _________

**Frontend:**
- [ ] React / Next.js
- [ ] Vue / Nuxt
- [ ] Angular
- [ ] Server-rendered (templates)
- [ ] Other: _________

**Database:**
- [ ] PostgreSQL
- [ ] MySQL / MariaDB
- [ ] MongoDB
- [ ] Redis
- [ ] Other: _________

**ORM / Query Builder:**
```
[e.g., Prisma, Sequelize, SQLAlchemy, Mongoose]
```

**Infrastructure:**
- [ ] Docker / Docker Compose
- [ ] Kubernetes
- [ ] AWS / GCP / Azure — Services used: _________
- [ ] Serverless (Lambda, Cloud Functions)
- [ ] Other: _________

---

## 6. External Integrations

`[OPTIONAL]` _List any third-party APIs, services, or systems this feature communicates with._

| Integration | Purpose | Direction (Inbound/Outbound/Both) | Auth Method |
|---|---|---|---|
| _e.g., Stripe API_ | _Process payments_ | _Outbound_ | _API Key_ |
| _e.g., SendGrid_ | _Send emails_ | _Outbound_ | _API Key_ |
| _e.g., AWS S3_ | _File storage_ | _Both_ | _IAM Role_ |

---

## 7. Existing Security Controls

`[OPTIONAL]` _Describe what security mechanisms are already in place that this feature will use or extend._

- **Authentication:** _How are users currently authenticated? (e.g., JWT via middleware, OAuth2, session cookies)_
- **Authorization:** _How are permissions currently enforced? (e.g., RBAC middleware, ABAC policies, Casbin)_
- **Input Validation:** _Is there a validation library already in use? (e.g., Zod, Joi, Pydantic)_
- **Rate Limiting:** _Is rate limiting in place? (e.g., express-rate-limit, Redis-based)_
- **Logging:** _What logging framework is in use? (e.g., Winston, Pino, structlog)_

---

## 8. New Dependencies

`[OPTIONAL]` _List any new third-party libraries or packages being introduced with this feature._

| Package Name | Version | Purpose | Source |
|---|---|---|---|
| _e.g., multer_ | _1.4.5_ | _File upload handling_ | _npm_ |
| _e.g., sharp_ | _0.33.2_ | _Image processing_ | _npm_ |

---

## 9. CI/CD Impact

`[OPTIONAL]` _Does this feature modify any CI/CD pipelines, GitHub Actions, Dockerfiles, or deployment configurations?_

- [ ] No changes to CI/CD or infrastructure
- [ ] Modifies existing GitHub Actions / CI workflows
- [ ] Adds new GitHub Actions / CI workflows
- [ ] Modifies Dockerfile or docker-compose
- [ ] Modifies environment variables or secrets configuration
- [ ] Other: _________

---

## 10. Known Risks & Assumptions

`[OPTIONAL]` _List any security risks or assumptions you are already aware of. This helps the threat modeling phase focus on real concerns._

```
[Write here]
```

---

## Pipeline Routing (Auto-filled by Orchestrator)

> _This section is filled by the pipeline orchestrator after reading the brief. Do not modify manually._

- **Phase 1 Sub-workflows:** _[auto-filled]_
- **Phase 2 Sub-workflows:** _[auto-filled]_
- **Phase 3 Sub-workflows Selected:** _[auto-filled]_
- **ASVS Chapters Loaded:** _[auto-filled]_
- **Knowledge Base Files Loaded:** _[auto-filled]_
