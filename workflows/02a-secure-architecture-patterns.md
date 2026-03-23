---
description: "Phase 2a — Secure Architecture Patterns"
phase: 2
nist_ssdf: "PS.1 — Protect All Forms of Code from Unauthorized Access and Tampering"
asvs_reference: "asvs-v1-architecture.md (V1.2 — Authentication Architecture, V1.4 — Access Control Architecture, V1.5 — Input and Output Architecture)"
triggers: "Called by 00-pipeline-orchestrator.md after Phase 1 Human Gate approval"
input_required: "Approved [feature]-threat-report.md from Phase 1"
---

# Phase 2a: Secure Architecture Patterns

**Purpose:** Translate the threats identified in Phase 1 into concrete architecture decisions and security controls. This sub-workflow produces a secure design document that tells the developer exactly HOW to build the feature securely — not just what to avoid.

---

## Step 1: Threat-to-Control Mapping

**Action:** For every Critical and High threat in the approved threat report, identify the specific security control that mitigates it.

**Map each threat to a control pattern:**

| STRIDE Category | Common Control Patterns |
|---|---|
| **Spoofing** | Authentication middleware, mutual TLS, token validation, HMAC signature verification |
| **Tampering** | Input validation (allowlist), schema enforcement, signed cookies/tokens, CSP headers, integrity hashes |
| **Repudiation** | Structured audit logging, immutable log storage, event sourcing |
| **Information Disclosure** | Response filtering (DTO pattern), generic error handlers, field-level encryption, access-controlled storage |
| **Denial of Service** | Rate limiting, request size limits, pagination, timeouts, circuit breakers, queue-based processing |
| **Elevation of Privilege** | RBAC/ABAC middleware, ownership verification (parameterized queries), allowlisted fields on writes |

**Output format for each threat:**

```markdown
### Threat: [Threat ID] — [Brief Description]
- **Risk Level:** [from threat report]
- **Control Pattern:** [Name of the pattern]
- **Implementation:** [Specific guidance for this feature's stack]
- **Library/Tool:** [Concrete recommendation — e.g., "express-rate-limit with Redis store"]
- **Where to Apply:** [Exact location in the architecture — e.g., "Auth middleware before route handler"]
```

---

## Step 2: Authentication Architecture

**Action:** If the feature involves user authentication in any way, define the authentication architecture.

**Evaluate and document:**

1. **Authentication Method Selection:**
   - For session-based: Define cookie attributes (`Secure`, `HttpOnly`, `SameSite=Strict`), session store (Redis, not in-memory), session ID entropy (min 128 bits).
   - For token-based (JWT): Define signing algorithm (`RS256` or `ES256`, NEVER `HS256` with a weak secret, NEVER allow `none`), expiration policy (short-lived access tokens, longer refresh tokens), token storage on client (HttpOnly cookie, NOT localStorage).

2. **Credential Handling:**
   - Password hashing: Specify algorithm (`Argon2id` preferred, `bcrypt` acceptable) with explicit work factor.
   - Credential transport: HTTPS only, never in query strings or URL parameters.

3. **Multi-Factor Authentication:**
   - Is MFA required for this feature's risk level? If so, define the mechanism (TOTP, WebAuthn).

**Reference:** Load `asvs-reference/asvs-v2-authentication.md` and `asvs-reference/asvs-v3-session.md` for specific requirements.

---

## Step 3: Authorization Architecture

**Action:** If the feature involves access control, define the authorization architecture.

**Evaluate and document:**

1. **Access Control Model:**
   - RBAC (Role-Based): Define roles, permissions matrix, and middleware implementation.
   - ABAC (Attribute-Based): Define attributes, policies, and evaluation engine.
   - Hybrid: Define which operations use which model.

2. **Enforcement Points:**
   - Where in the request lifecycle is authorization checked? (middleware, controller, service layer, database query)
   - Recommendation: Enforce at both the route level (middleware) AND the data level (parameterized queries with ownership checks).

3. **Default Deny:**
   - All routes must require explicit authorization unless deliberately public.
   - Document which routes are intentionally public and why.

4. **IDOR Prevention:**
   - For every endpoint that takes a resource ID as input, define the ownership verification logic.
   - Pattern: `WHERE resource.id = :input_id AND resource.owner_id = :authenticated_user_id`

**Reference:** Load `asvs-reference/asvs-v4-access-control.md` for specific requirements.

---

## Step 4: Input/Output Architecture

**Action:** Define how data enters and leaves the feature securely.

**Evaluate and document:**

1. **Input Validation Strategy:**
   - Define the validation library for the tech stack (Zod / Joi for Node.js, Pydantic for Python).
   - Define validation at the boundary: schema validation BEFORE any business logic executes.
   - Specify allowlist approach: define what IS allowed, reject everything else.
   - Set explicit limits: max string length, max array size, max nested depth, max file size.

2. **Output Encoding Strategy:**
   - For API responses: Define a DTO (Data Transfer Object) or response serializer that explicitly includes only the fields the client needs. Never return raw database objects.
   - For HTML rendering: Ensure framework-level auto-escaping is not bypassed (`dangerouslySetInnerHTML`, `v-html`, `| safe`).
   - For redirects: Validate redirect URLs against an allowlist of domains.

3. **Database Interaction:**
   - Mandate parameterized queries or ORM methods exclusively. Document the specific ORM/query builder pattern to use.
   - Explicitly ban raw string concatenation for all database queries.

**Reference:** Load `asvs-reference/asvs-v5-validation.md` for specific requirements.

---

## Step 5: Data Protection Architecture

**Action:** Define how sensitive data is protected at rest and in transit.

1. **Encryption at Rest:**
   - What data requires encryption? (credentials, PII, financial data)
   - Algorithm: AES-256-GCM for symmetric encryption.
   - Key management: Where are encryption keys stored? (environment variables minimum, secrets manager preferred)

2. **Encryption in Transit:**
   - TLS 1.2+ enforced on all connections (external AND internal).
   - HSTS header with `max-age >= 31536000` and `includeSubDomains`.

3. **Secrets Management:**
   - No hardcoded secrets in source code.
   - Secrets loaded from environment variables or dedicated secrets manager (AWS Secrets Manager, HashiCorp Vault).
   - Different secrets for different environments (dev, staging, production).

**Reference:** Load `asvs-reference/asvs-v6-cryptography.md` and `asvs-reference/asvs-v9-communications.md`.

---

## Step 6: Error Handling & Logging Architecture

**Action:** Define the error handling and logging strategy for this feature.

1. **Error Handling:**
   - Global error handler catches all unhandled exceptions.
   - Production responses return generic messages only (never stack traces, SQL errors, or framework internals).
   - Security-critical failures (auth, authz) default to deny.

2. **Logging:**
   - Log all security events: login success/failure, access denied, permission changes, data modifications.
   - Redact sensitive data before logging: passwords, tokens, credit card numbers, PII.
   - Use structured logging format (JSON) for machine parseability.
   - Log destination: external service or append-only file (never in web root).

**Reference:** Load `asvs-reference/asvs-v7-error-handling.md` and `asvs-reference/asvs-v8-data-protection.md`.

---

## Step 7: Compile Secure Design Document

**Action:** Generate `outputs/[feature-name]/secure-design.md` with the following structure:

```markdown
# Secure Design: [Feature Name]

## 1. Design Summary
[Brief overview of the architecture decisions and why they were made, linked to specific threats from the threat report]

## 2. Threat-to-Control Mapping
[Table from Step 1]

## 3. Authentication Architecture
[From Step 2, if applicable]

## 4. Authorization Architecture
[From Step 3, if applicable]

## 5. Input/Output Architecture
[From Step 4]

## 6. Data Protection Architecture
[From Step 5]

## 7. Error Handling & Logging Architecture
[From Step 6]

## 8. Library & Framework Decisions
[Consolidated list of all recommended libraries with versions and purpose]

| Library | Version | Purpose | Stack |
|---|---|---|---|
| bcrypt | 5.x | Password hashing | Node.js |
| zod | 3.x | Input validation | Node.js |
| helmet | 7.x | HTTP security headers | Node.js |
| pydantic | 2.x | Input validation | Python |
| argon2-cffi | 23.x | Password hashing | Python |
```

**Next:** Pass this document to `02b-security-requirements-generation.md`.
