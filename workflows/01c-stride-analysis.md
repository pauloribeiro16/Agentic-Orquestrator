---
description: "Phase 1c — STRIDE Threat Analysis"
phase: 1
nist_ssdf: "PW.1 — Design Software to Meet Security Requirements"
asvs_reference: "asvs-v1-architecture.md (V1.1, V1.2)"
triggers: "Called by 00-pipeline-orchestrator.md after 01a and 01b complete"
input_required: "Attack Surface Map (01a) and Data Flow Diagram (01b)"
---

# Phase 1c: STRIDE Threat Analysis

**Purpose:** Systematically apply the STRIDE threat model to every component, data flow, and trust boundary identified in Phase 1a and 1b. Each element is evaluated against all six STRIDE categories to identify specific, actionable threats.

---

## STRIDE Reference

| Category | Threat | Target | Security Property Violated |
|---|---|---|---|
| **S** — Spoofing | Attacker impersonates a user, service, or component | External Entities, Processes | Authentication |
| **T** — Tampering | Attacker modifies data in transit or at rest | Data Flows, Data Stores | Integrity |
| **R** — Repudiation | Attacker denies performing an action, no evidence exists | Processes | Non-repudiation |
| **I** — Information Disclosure | Sensitive data is exposed to unauthorized parties | Data Flows, Data Stores | Confidentiality |
| **D** — Denial of Service | Attacker makes the feature unavailable | Processes, Data Stores | Availability |
| **E** — Elevation of Privilege | Attacker gains higher permissions than authorized | Processes | Authorization |

---

## Step 1: Element-to-STRIDE Mapping

**Action:** For each element type from the DFD, evaluate the applicable STRIDE categories.

**Standard applicability matrix:**

| DFD Element Type | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External Entity | ✅ | | ✅ | | | |
| Process | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data Store | | ✅ | | ✅ | ✅ | |
| Data Flow | | ✅ | | ✅ | ✅ | |
| Trust Boundary | ✅ | ✅ | | ✅ | | ✅ |

---

## Step 2: S — Spoofing Analysis

**What to evaluate:** Can an attacker impersonate another user, an internal service, or an external entity within this feature?

**Check each of the following:**

1. **User Identity Spoofing:**
   - Are all endpoints that handle user-specific data protected by authentication middleware?
   - Does the feature rely on client-side identifiers (hidden fields, localStorage values, easily guessable IDs) instead of server-validated session tokens?
   - Can a user forge or replay an expired/stolen JWT or session cookie?

2. **Service Identity Spoofing:**
   - If this feature communicates with internal services, is mutual authentication (mTLS, signed tokens) enforced?
   - Can an attacker inject a fake webhook or callback URL to impersonate an external service?

3. **External Entity Spoofing:**
   - Does the feature verify the authenticity of incoming data from third-party APIs (signature validation, HMAC verification)?

**For each threat found, record:**
```markdown
- **Threat ID:** S-001
- **Element:** [DFD element name]
- **Description:** [What can be spoofed and how]
- **Risk:** [Critical / High / Medium / Low]
- **Mitigation:** [Specific countermeasure]
```

---

## Step 3: T — Tampering Analysis

**What to evaluate:** Can an attacker modify data as it flows through the system or while it sits in storage?

**Check each of the following:**

1. **Data in Transit:**
   - Is all communication over HTTPS/TLS? Are there any plaintext HTTP endpoints?
   - Are API request bodies validated against a strict schema before processing?
   - Can parameters (query strings, path parameters, headers) be manipulated to alter business logic?

2. **Data at Rest:**
   - Are database records integrity-protected? Can a compromised internal user modify records without detection?
   - Are client-side stored values (cookies, localStorage) signed or encrypted to prevent tampering?

3. **Code and Configuration Tampering:**
   - Can an attacker modify CI/CD pipeline definitions to inject malicious code?
   - Are dependency lockfiles integrity-checked (hash verification)?

**Record each threat in the same format as Step 2.**

---

## Step 4: R — Repudiation Analysis

**What to evaluate:** If a malicious action occurs through this feature, will the system have sufficient evidence to attribute it?

**Check each of the following:**

1. **Audit Trail Coverage:**
   - Are all state-changing operations (create, update, delete) logged with: timestamp, actor ID, action performed, affected resource?
   - Are authentication events (login, logout, failed attempts) logged?
   - Are authorization failures (403 responses) logged?

2. **Log Integrity:**
   - Can the acting user or process modify or delete their own log entries?
   - Are logs stored outside the application's write scope (append-only, external log service)?

3. **Non-repudiation Mechanisms:**
   - For high-value actions (financial transactions, permission changes), is there a mechanism beyond basic logging (e.g., signed audit records, immutable ledger)?

**Record each threat in the same format as Step 2.**

---

## Step 5: I — Information Disclosure Analysis

**What to evaluate:** Does this feature expose sensitive data to unauthorized parties through any channel?

**Check each of the following:**

1. **API Response Over-exposure:**
   - Do API responses return full database objects when only specific fields are needed? (Mass Assignment / Over-posting risk)
   - Are fields like `password_hash`, `internal_id`, `admin_notes`, or `deleted_at` being included in user-facing responses?

2. **Error Message Leakage:**
   - Do error responses include stack traces, database schema details, SQL error messages, or framework internals?
   - Are different error messages returned for "user not found" vs "wrong password"? (Account enumeration)

3. **Side Channel Leakage:**
   - Does the feature exhibit timing differences that reveal information (e.g., different response times for valid vs. invalid users)?
   - Are sensitive data values logged in application logs, monitoring dashboards, or error tracking services?

4. **Storage Exposure:**
   - Are uploaded files accessible without authentication?
   - Are database backups or cache entries containing sensitive data properly access-controlled?

**Record each threat in the same format as Step 2.**

---

## Step 6: D — Denial of Service Analysis

**What to evaluate:** Can an attacker exhaust the feature's resources or make it unavailable to legitimate users?

**Check each of the following:**

1. **Resource-Intensive Operations:**
   - Does the feature perform heavy computation (image processing, PDF generation, complex queries) that could be triggered repeatedly?
   - Are there unbounded database queries (missing pagination, no `LIMIT` clause)?
   - Does the feature accept large file uploads without size limits?

2. **Rate Limiting:**
   - Are resource-intensive endpoints protected by rate limiting?
   - Is rate limiting applied per-user, per-IP, or globally? Can it be bypassed?

3. **Cascading Failures:**
   - If the feature depends on an external service, what happens when that service is unavailable? Does the feature fail gracefully or cascade the failure?
   - Are there circuit breakers or timeouts on external calls?

4. **Algorithmic Complexity:**
   - Does the feature use any operations with worst-case exponential complexity (regex, recursive parsing, deeply nested JSON)?

**Record each threat in the same format as Step 2.**

---

## Step 7: E — Elevation of Privilege Analysis

**What to evaluate:** Can an unprivileged user use this feature to gain higher access or reach another user's data?

**Check each of the following:**

1. **Vertical Privilege Escalation:**
   - Can a regular user access admin-only functionality by manipulating the request (changing role in JWT payload, hitting admin endpoints directly)?
   - Are admin routes in a separate namespace with distinct middleware, or mixed with user routes?

2. **Horizontal Privilege Escalation (IDOR):**
   - Can a user access another user's data by changing an ID parameter in the URL or request body?
   - Does the backend verify ownership/permission for every resource access, or does it trust the provided ID?

3. **Privilege via Input Manipulation:**
   - Can a user set their own role, permissions, or account type through the registration or profile update endpoint? (Mass Assignment)
   - Are there hidden parameters that, if included in a request, would grant elevated access?

4. **Token/Session Escalation:**
   - Can a low-privilege token be exchanged for a higher-privilege one?
   - If the feature modifies user roles/permissions, does it force re-authentication or token refresh?

**Record each threat in the same format as Step 2.**

---

## Step 8: Compile STRIDE Threat Matrix

**Action:** Compile all identified threats into a single threat matrix for the `[feature]-threat-report.md`.

**Format:**

```markdown
## STRIDE Threat Matrix: [Feature Name]

| Threat ID | STRIDE Category | Element | Description | Risk Level | Mitigation |
|---|---|---|---|---|---|
| S-001 | Spoofing | Login Endpoint | No rate limiting on login allows credential stuffing | High | Implement rate limiting (5 attempts/min per IP) |
| T-001 | Tampering | User Profile API | Profile update accepts `role` field in request body | Critical | Allowlist writable fields; exclude `role`, `isAdmin` |
| R-001 | Repudiation | File Delete | File deletion not logged with actor ID | Medium | Add audit log entry with user ID and file ID |
| I-001 | Information Disclosure | Error Handler | Stack trace returned in 500 responses | High | Implement generic error messages in production |
| D-001 | Denial of Service | File Upload | No file size limit on upload endpoint | High | Enforce 10MB limit and rate limit to 5 uploads/min |
| E-001 | Elevation of Privilege | Invoice API | GET /invoices/:id has no ownership check | Critical | Add WHERE user_id = authenticated_user.id to query |
```

### Risk Rating Guide

| Level | Criteria |
|---|---|
| **Critical** | Exploitable remotely, no auth required, leads to data breach or full system compromise |
| **High** | Exploitable remotely, requires low-privilege auth, leads to significant data exposure or privilege escalation |
| **Medium** | Requires specific conditions or higher-privilege auth, leads to partial data exposure or limited escalation |
| **Low** | Requires complex setup, insider access, or leads to minimal information disclosure |

---

## Step 9: Output

**Action:** Merge the STRIDE Threat Matrix into `outputs/[feature-name]/threat-report.md` alongside the Attack Surface Map (01a) and Data Flow Diagram (01b).

**The complete threat report structure:**

```markdown
# Threat Model Report: [Feature Name]

## 1. Executive Summary
[Brief description of the feature, overall risk profile, and critical findings count]

## 2. Attack Surface Map
[Output from 01a]

## 3. Architecture Diagram
[Mermaid.js DFD from 01b]

## 4. STRIDE Threat Matrix
[Matrix from Step 8 above]

## 5. Critical Findings Summary
[List only Critical and High threats with recommended priority order for mitigation]
```

**⏸ HUMAN GATE:** This report is now presented for human review before proceeding to Phase 2.
