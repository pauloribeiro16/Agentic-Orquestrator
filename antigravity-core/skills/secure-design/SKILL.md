---
name: secure-design
description: Secure architecture patterns, security requirements generation, and dependency evaluation. Phase 2 of the DevSecOps pipeline. Translates threats into controls, ASVS-traceable requirements, and supply chain assessments. Triggers on secure design, security architecture, security requirements, dependency evaluation, supply chain risk, ASVS requirements, security controls.
---

# Secure Design (Pipeline Phase 2)

> NIST SSDF: PS.1 — Protect All Forms of Code from Unauthorized Access and Tampering

**Input required:** Approved `[feature]-threat-report.md` from Phase 1.

This skill executes three steps: Secure Architecture Patterns → Security Requirements Generation → Dependency Evaluation. Outputs are `secure-design.md` and `security-requirements.md`.

---

## Step 1: Secure Architecture Patterns (02a)

**Purpose:** Translate Phase 1 threats into concrete architecture decisions and security controls.

### 1.1 Threat-to-Control Mapping

For every Critical and High threat:

| STRIDE Category | Common Control Patterns |
|-----------------|------------------------|
| Spoofing | Auth middleware, mTLS, token validation, HMAC verification |
| Tampering | Input validation (allowlist), schema enforcement, signed cookies, CSP, integrity hashes |
| Repudiation | Structured audit logging, immutable log storage, event sourcing |
| Information Disclosure | DTO response filtering, generic error handlers, field-level encryption |
| Denial of Service | Rate limiting, request size limits, pagination, timeouts, circuit breakers |
| Elevation of Privilege | RBAC/ABAC middleware, ownership verification, allowlisted fields on writes |

For each threat record: Threat ID, Risk Level, Control Pattern, Implementation guidance, Library/Tool, Where to Apply.

### 1.2 Authentication Architecture

If the feature involves user auth:

**Session-based:** Cookie attributes (`Secure`, `HttpOnly`, `SameSite=Strict`), session store (Redis, not in-memory), session ID entropy (min 128 bits).

**Token-based (JWT):** Signing algorithm (`RS256`/`ES256`, NEVER `HS256` with weak secret, NEVER `none`), short-lived access tokens, refresh token rotation, storage (HttpOnly cookie, NOT localStorage).

**Credential handling:** Argon2id preferred (bcrypt acceptable), HTTPS only, never in query strings.

**MFA:** Required for feature's risk level? TOTP or WebAuthn.

**Reference:** Load `asvs-v2-authentication.md` and `asvs-v3-session.md`.

### 1.3 Authorization Architecture

**Access Control Model:** RBAC, ABAC, or hybrid — define roles, permissions matrix, middleware.

**Enforcement Points:** Route level (middleware) AND data level (parameterized queries with ownership).

**Default Deny:** All routes require explicit auth unless deliberately public (document why).

**IDOR Prevention:** `WHERE resource.id = :input_id AND resource.owner_id = :auth_user_id`

**Reference:** Load `asvs-v4-access-control.md`.

### 1.4 Input/Output Architecture

**Input Validation:** Zod/Joi (Node.js), Pydantic (Python). Schema validation BEFORE business logic. Allowlist approach. Explicit limits (string length, array size, nested depth, file size).

**Output Encoding:** DTOs for API responses (never raw DB objects). Framework auto-escaping not bypassed. Redirect URL allowlist.

**Database:** Parameterized queries or ORM exclusively. Ban raw string concatenation.

**Reference:** Load `asvs-v5-validation.md`.

### 1.5 Data Protection Architecture

**At rest:** AES-256-GCM for sensitive data. Keys in env vars minimum, secrets manager preferred.

**In transit:** TLS 1.2+ on all connections. HSTS with `max-age >= 31536000; includeSubDomains`.

**Secrets:** No hardcoded secrets. Env vars or secrets manager. Different secrets per environment.

**Reference:** Load `asvs-v6-cryptography.md` and `asvs-v9-communications.md`.

### 1.6 Error Handling & Logging Architecture

**Errors:** Global handler, generic production messages, security failures default to deny.

**Logging:** All security events (login, access denied, permission changes, data mods). Redact sensitive data. Structured JSON. External/append-only destination.

**Reference:** Load `asvs-v7-error-handling.md` and `asvs-v8-data-protection.md`.

---

## Step 2: Security Requirements Generation (02b)

**Purpose:** Derive concrete, testable, ASVS-traceable requirements from the threat model.

### 2.1 ASVS Chapter Selection

| Feature Characteristic | ASVS Chapters |
|------------------------|---------------|
| Any feature (always) | V1 (Architecture), V5 (Validation), V14 (Configuration) |
| Has user authentication | V2 (Authentication) |
| Has session management | V3 (Session Management) |
| Has role/resource access | V4 (Access Control) |
| Sensitive data storage/transit | V6 (Cryptography), V8 (Data Protection), V9 (Communications) |
| Error handling / logging | V7 (Error Handling) |
| REST or GraphQL endpoints | V13 (API & Web Services) |

### 2.2 Requirement Transformation

Transform generic ASVS requirements into feature-specific instructions:

```
ASVS Generic:
  V2.1.1: "Verify that user set passwords are at least 12 characters in length."

Feature-Specific:
  REQ-AUTH-001: "POST /api/v1/auth/register must validate password >= 12 chars
  via Zod schema before bcrypt hashing."
  Definition of Done: z.string().min(12) on password. 400 for violations.
  Traces to: ASVS V2.1.1, Threat S-001
```

### 2.3 Requirement Domains

Organize by: REQ-AUTH-xxx (Authentication), REQ-SESS-xxx (Session), REQ-AUTHZ-xxx (Access Control), REQ-INPUT-xxx (Input Validation), REQ-OUTPUT-xxx (Output Encoding), REQ-CRYPTO-xxx (Cryptography), REQ-COMM-xxx (Communication), REQ-LOG-xxx (Logging), REQ-API-xxx (API), REQ-CONFIG-xxx (Configuration).

### 2.4 Assessment Template

Pre-generate per requirement:
```markdown
### REQ-AUTH-001: Password Minimum Length
- **ASVS Trace:** V2.1.1
- **Threat Trace:** S-001
- **Description:** [Feature-specific instruction]
- **Definition of Done:** [Concrete acceptance criteria]
- **Assessment:** [ ] PASS  [ ] FAIL  [ ] N/A
```

---

## Step 3: Dependency Evaluation (02c)

**Purpose:** Evaluate new third-party libraries BEFORE adoption (proactive, not reactive SCA).

**Trigger:** Only when the Feature Brief lists new dependencies (Section 8).

### 3.1 Supply Chain Risk Assessment

**Maintainer Health:** Last release, maintainer count, org backing. Red flag: >12 months inactive + open security issues.

**Community & Adoption:** Weekly downloads, stars/forks, issue response time. Red flag: <1,000 weekly downloads + no org backing.

**Typosquatting:** Name similarity to popular packages. Red flag: 1-2 char difference + created within 6 months.

**Known Vulnerabilities:** CVEs on specified version, advisory history, transitive risk.

### 3.2 License Compatibility

| License | Commercial | Copyleft Risk | Notes |
|---------|-----------|---------------|-------|
| MIT / Apache 2.0 / BSD / ISC | ✅ | None | Safe |
| GPL 2.0/3.0 | ⚠️ | Strong | May require source disclosure |
| AGPL | ❌ | Strong | Network use triggers copyleft |
| Unlicensed | ❌ | Unknown | No license = no permission |

### 3.3 Scoring Matrix

| Factor | Low (0) | Medium (1) | High (2) |
|--------|---------|------------|----------|
| Maintenance | Active, multiple maintainers | Active, single | Inactive >12 months |
| Adoption | >100K weekly | 10K–100K | <10K |
| Vulnerabilities | No CVEs | Past CVEs, patched | Active unpatched |
| License | MIT/Apache/BSD | LGPL | GPL/AGPL/Unlicensed |
| Dependency Depth | <10 transitive | 10–50 | >50 |
| Install Scripts | None | Benign build | Suspicious/obfuscated |

**Decision:** 0–3 → ✅ APPROVE | 4–6 → ⚠️ CONDITIONAL | 7+ → ❌ REJECT

---

## Output

Generate in `outputs/[feature-name]/`:
- `secure-design.md` — Architecture patterns, library choices, controls, dependency evaluations
- `security-requirements.md` — Full checklist with ASVS traceability and assessment templates

**⏸ HUMAN GATE:** Present for review. Do NOT proceed to Phase 3 until approved.


## 📑 Content Map

| File | Description |
|------|-------------|
| `SKILL.md` | Main Skill Definition |
