---
description: "Phase 3f — API & Web Services Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v13-api.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature exposes REST or GraphQL endpoints"
input_required: "security-requirements.md (REQ-API-xxx)"
---

# Phase 3f: API & Web Services Audit

**ASVS Chapter:** V13 (API and Web Service)

**CRITICAL:** Load `asvs-reference/asvs-v13-api.md` before starting.

---

## Step 1: Discovery

**Locate:**
- Route definitions and API controllers.
- GraphQL schemas, resolvers, and server configuration.
- Body parsing middleware (body-parser, express.json, XML parsers).
- API documentation / OpenAPI specs (if they exist).
- Rate limiting and throttling configuration.

---

## Step 2: V13.1 — Generic Web Service Security

**What to check:**

1. **Content-Type Enforcement:** Does the API strictly validate the `Content-Type` header and reject unexpected formats?
2. **Safe XML Parsing:** If XML is processed, is external entity resolution (XXE) explicitly disabled?
3. **Payload Size Limits:** Is the body parser configured with explicit size limits to prevent DoS via massive payloads?
4. **Schema Validation:** Does every endpoint validate incoming payloads against a strict schema before business logic executes?

---

## Step 3: V13.2 — RESTful Security

**What to check:**

1. **Method Enforcement:** Do endpoints reject unintended HTTP methods? (e.g., GET on a POST-only endpoint)
2. **CSRF Protection:** If the API uses cookies for authentication, are anti-CSRF tokens or `SameSite` cookie attributes enforced on state-changing methods (POST, PUT, DELETE)?
3. **Mass Assignment:** Do update/create endpoints use allowlisted fields (DTO pattern) to prevent users from setting unintended properties (e.g., `role`, `isAdmin`)?
4. **Pagination:** Do list endpoints enforce pagination with reasonable defaults and maximums to prevent full-table dumps?

---

## Step 4: V13.4 — GraphQL Security (If Applicable)

**What to check:**

1. **Query Depth Limit:** Is a maximum query depth configured? (Recommended: ≤ 5–7 levels using `graphql-depth-limit` or equivalent)
2. **Query Complexity Limit:** Is query complexity scoring enabled to prevent resource-expensive queries?
3. **Introspection:** Is introspection disabled in production? (Prevents attackers from mapping the full schema)
4. **Batching Attacks:** Is rate limiting applied per-operation within batched requests, not just per HTTP request?
5. **N+1 Prevention:** Are DataLoaders or equivalent batching mechanisms used to prevent N+1 query performance issues?

---

## Step 5: Compile Assessment

**Action:** For every Level 2 requirement in V13, record PASS/FAIL/N-A.

**Output:** Append all V13 assessments to `outputs/[feature-name]/audit-workflow.md`.
