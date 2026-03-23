---
name: asvs-audit
description: OWASP ASVS Level 2 security audit with 9 audit domains. Phase 3 of the DevSecOps pipeline. Covers authentication, access control, validation, cryptography, error handling, APIs, secrets, configuration, and CI/CD. Triggers on ASVS audit, security audit, compliance check, OWASP verification, code audit, security testing, vulnerability assessment, ASVS compliance.
---

# ASVS Verification & Testing (Pipeline Phase 3)

> NIST SSDF: RV.1 — Identify and Confirm Vulnerabilities on an Ongoing Basis

**Input required:** Approved `secure-design.md` and `security-requirements.md` from Phase 2.

**CRITICAL:** Load ASVS reference files from `references/` before starting each sub-audit. The agent must NEVER search the web for ASVS requirements.

---

## Sub-Audit Selection Matrix

Select sub-audits based on the feature's characteristics:

| Feature Characteristic | Sub-Audit | ASVS References to Load |
|------------------------|-----------|------------------------|
| Has login / registration / passwords | **03a** — Auth & Session | `asvs-v2-authentication.md`, `asvs-v3-session.md` |
| Has role/resource-based access | **03b** — Access Control | `asvs-v4-access-control.md` |
| Accepts user input (forms, APIs, uploads) | **03c** — Validation & Encoding | `asvs-v5-validation.md` |
| Stores/transmits sensitive data | **03d** — Crypto & Communications | `asvs-v6-cryptography.md`, `asvs-v9-communications.md` |
| Has error handling, logging, audit trails | **03e** — Error Handling & Logging | `asvs-v7-error-handling.md`, `asvs-v8-data-protection.md` |
| Exposes REST or GraphQL endpoints | **03f** — API & Web Services | `asvs-v13-api.md` |
| Adds new third-party dependencies | **03g** — Secrets & Dependencies | CVE databases |
| Modifies server/container/deployment config | **03h** — Configuration | `asvs-v14-configuration.md` |
| Modifies CI/CD pipelines or GitHub Actions | **03i** — CI/CD Pipeline | N/A |

**Always load:** `asvs-v1-architecture.md` as the architectural baseline.

## Assessment Format (Mandatory for Every Requirement)

```markdown
### [Requirement ID]: [Title]
**ASVS Text:** "[Full text from reference file]"
**Level:** L2
**Assessment:**
- [ ] PASS — Evidence: [file path, code reference]
- [ ] FAIL — File: [path] Line: [#] Evidence: [snippet] Remediation: [fix]
- [ ] N/A — Justification: [reason]
```

---

## 03a: Authentication & Session Management (V2, V3)

**Discover:** Login/registration/logout controllers, password reset flows, JWT logic, session storage config, auth middleware, cookie settings.

### V2 — Authentication

**Password Security:** Min 12 chars, allow 128+, any chars including Unicode. Hash with Argon2id (preferred), bcrypt (cost ≥ 10), or PBKDF2 (≥ 310K iterations). Flag MD5/SHA1/SHA256-unsalted. Check against breached password lists.

**Brute Force Protection:** Login rate limiting (max 100 attempts/hour/account). Account lockout or CAPTCHA after repeated failures. Consistent timing for valid vs invalid usernames.

**Credential Recovery:** Generic messages ("If the email exists, a link was sent"). Tokens: cryptographically random, <1 hour, single-use. Delivery via side channel (email), never in API response.

**Credential Storage:** No plaintext passwords anywhere (DB, logs, errors). No hardcoded credentials.

### V3 — Session Management

**Token Generation:** CSPRNG with ≥ 128 bits entropy. Unpredictable identifiers.

**Cookie Security:** `Secure`, `HttpOnly`, `SameSite=Strict` or `Lax`. Restrictive path/domain.

**JWT Security:** Algorithm explicitly `RS256`/`ES256`/`HS256` (strong secret ≥ 256 bits). `none` rejected. `exp` enforced (<15 min for access tokens). Signature + claims (`iss`, `aud`, `exp`) validated. No sensitive PII in payload.

**Logout:** Server-side session destroyed. JWT blocklist/denylist for early invalidation. Idle timeout. Absolute timeout.

---

## 03b: Access Control (V4)

**Discover:** RBAC/ABAC middleware, route guards, CRUD controllers, admin routes, CORS config.

**General Design:** Default deny. Least privilege. Admin routes in separate namespace with stricter middleware. Server-side enforcement only.

**IDOR Prevention:** Every endpoint with resource ID must verify ownership: `WHERE resource.id = :input_id AND resource.owner_id = :auth_user_id`. Batch operations check each item individually. Consider indirect references for sensitive resources.

**Other:** Path traversal prevention (`../` and `%2e%2e%2f`). CORS: no wildcard `*` for credentialed endpoints, strict origin allowlist, restricted methods. Forced browsing protection.

---

## 03c: Validation, Sanitization & Encoding (V5)

**Discover:** Map user-controlled data from entry to exit. Identify entry points, critical exit points, validation libraries (Zod, Joi, Pydantic), sanitization utilities.

**Input Validation (V5.1):** Positive validation (allowlist, not denylist). Schema validation before business logic. Established libraries. Explicit limits (string length, array size, numeric range, nested depth, file size). Content-Type enforcement.

**Injection Defense (V5.2):**
- **SQL:** Parameterized queries/ORM exclusively. Flag string concatenation. Check raw query escape hatches (`$queryRaw`, `Model.query()`).
- **NoSQL:** Type-check inputs, prevent operator injection (`{"$gt": ""}`).
- **OS Command:** Flag `exec`, `spawn`, `child_process`, `subprocess.run`, `os.system`, `eval`. User input must never reach these without strict sanitization.
- **Path Traversal:** Validate file paths, check resolved path stays within intended directory.
- **SSRF:** Domain allowlist for outbound requests. Block internal IPs (`127.0.0.1`, `169.254.169.254`, `10.x`, `172.16-31.x`, `192.168.x`).

**Output Encoding (V5.3):** Context-aware encoding (HTML, JS, URL, CSS). Detect framework bypasses: `dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrustHtml`, `| safe`, `{{{ }}}`, `<%- %>`. CSP configured to restrict inline scripts and unsafe-eval.

---

## 03d: Cryptography & Communications (V6, V9)

**Discover:** Encryption/hashing functions, DB connection strings, TLS config, HTTP client config, key storage, RNG usage.

**Algorithms (V6.1):** Flag: MD5, SHA1, DES, 3DES, RC4, RSA <2048, ECB mode. Approve: AES-128/256-GCM, SHA-256+, ChaCha20-Poly1305, RSA ≥2048, ECDSA P-256+. No custom crypto. CSPRNG only: `crypto.randomBytes()` (Node.js), `secrets.token_bytes()` (Python) — NOT `Math.random()` / `random.random()`.

**Key Management (V6.2):** No hardcoded secrets. Secrets from env vars or vault. Key purpose separation. Rotation mechanism.

**Communications (V9.1):** HTTPS on all endpoints. HSTS `max-age >= 31536000; includeSubDomains`. TLS 1.2 minimum. Certificate validation enabled (no `rejectUnauthorized: false`, no `verify=False`). TLS/mTLS for internal services.

---

## 03e: Error Handling & Logging (V7, V8)

**Discover:** Global error middleware, custom exceptions, try/catch blocks, logging config (Winston, Pino, structlog), log destinations, monitoring (Sentry, Datadog).

**Error Handling (V7.1):** No stack traces to end-user in production. Generic error messages. Fail-secure on auth/authz errors. All error paths (sync, async, promise rejections) converge to same secure handler.

**Log Content (V8.1):** Events logged: login success/failure, password changes, 403s, data modifications, admin actions. NEVER log: passwords, JWTs, session cookies, credit cards, SSNs, API keys. Sanitize user input before logging (prevent log injection via `\n`, `\r`). Structured JSON format.

**Log Integrity (V8.2):** Logs outside web root. Append-only permissions. Error tracking services scrub sensitive data.

---

## 03f: API & Web Services (V13)

**Discover:** Route definitions, GraphQL schemas/resolvers, body parsers, OpenAPI specs, rate limiting config.

**Generic (V13.1):** Strict Content-Type validation. XXE disabled in XML parsers. Body parser size limits. Schema validation on all endpoints.

**RESTful (V13.2):** Reject unintended HTTP methods. CSRF protection for cookie-auth APIs. Mass assignment prevention (DTO/allowlist). Pagination with defaults and maximums.

**GraphQL (V13.4):** Query depth limit (≤ 5–7). Complexity scoring. Introspection disabled in production. Per-operation rate limiting in batches. DataLoaders for N+1 prevention.

---

## 03g: Secrets & Dependencies

**Discover:** `.env`/`.env.example`, Dockerfiles, CI/CD files, `package.json`/`requirements.txt`, config files.

**Secret Detection:** Pattern matching (AWS `AKIA`, GitHub `ghp_`, Stripe `sk_live_`, Slack webhooks, Google API keys, DB URIs with passwords, generic password variables). High entropy strings (>4.5 bits/char, >20 chars). Configuration leakage (`.env` committed, `.env.example` with real values).

**SCA:** Direct dependency CVE audit. Transitive dependency audit (note dependency chain). Malicious package detection (typosquatting, suspicious install scripts, new package with few downloads).

---

## 03h: Configuration Security (V14)

**Discover:** Web server config, Dockerfile, env templates, HTTP security headers (Helmet), build config, deployment manifests.

**Build & Deploy (V14.1):** Debug mode off in production. Source maps excluded. Build strips comments/test files/dev deps. Environment separation.

**Dependencies (V14.2):** Lockfiles committed with integrity hashes. Exact version pinning in production. No unused dependencies.

**Disclosure (V14.3):** Server version headers suppressed (`X-Powered-By` removed). Directory listing disabled. Default files not accessible. Admin interfaces protected.

**HTTP Headers (V14.4):**

| Header | Expected | Risk if Missing |
|--------|----------|-----------------|
| Content-Security-Policy | No `unsafe-inline`/`unsafe-eval` | XSS amplification |
| X-Content-Type-Options | `nosniff` | MIME sniffing |
| X-Frame-Options | `DENY` / `SAMEORIGIN` | Clickjacking |
| Strict-Transport-Security | `max-age=31536000; includeSubDomains` | Downgrade attacks |
| Referrer-Policy | `strict-origin-when-cross-origin` | Info leakage |
| Permissions-Policy | Restrict camera, mic, geo | Feature abuse |

**Container (V14.5):** Minimal base image (alpine, distroless, slim). Non-root user. Only necessary ports exposed. No secrets baked in image. Multi-stage builds. Read-only filesystem where possible.

---

## 03i: CI/CD Pipeline Security

**OWASP Mapping:** A08:2021 — Software and Data Integrity Failures

**Discover:** `.github/workflows/`, `.gitlab-ci.yml`, Jenkinsfile, CI Dockerfiles, build scripts, CI secret config.

**GitHub Actions:**
- **Action Pinning:** Pin to commit SHA, not tag. FAIL: `uses: actions/checkout@v4`. PASS: `uses: actions/checkout@b4ffde65... # v4.1.1`.
- **Triggers:** Flag `pull_request_target` (secret exfiltration risk). Restrict `workflow_dispatch`. Limit `push` to specific branches.
- **Permissions:** Explicit minimal `permissions` blocks. Override broad defaults.
- **Secrets:** Via `${{ secrets.NAME }}`, never echoed. Masked. Scoped to minimum environments.
- **Script Injection:** No user-controlled values in `run:` blocks. Use env vars instead.

**General Pipeline:**
- **Build Integrity:** Dependencies from lockfiles. Docker images pinned to digests. Ephemeral build environments.
- **Artifact Integrity:** Signed artifacts. Verification before deploy. Private access-controlled registry.
- **Deployment:** Restricted to specific branches. Manual approval for production. Scoped credentials. Separation of duties.
- **Secret Rotation:** Scheduled rotation. Documented revocation procedure. Secrets in CI platform store.

---

## Test Script Generation

For each FAIL and verifiable requirement, generate:

**Python** (`[feature]-security-tests.py`): `requests` + `pytest`. Self-contained tests for input validation boundaries, auth bypass, authz bypass, error handling.

**JavaScript** (`[feature]-security-tests.js`): `fetch` + `jest`/`vitest`. Mirror Python coverage.

---

## Output

Generate in `outputs/[feature-name]/`:
- `audit-workflow.md` — Full assessment matrix with all sub-audit findings
- `security-tests.py` — Python test scripts
- `security-tests.js` — JavaScript test scripts

**⏸ HUMAN GATE:** Present audit report and tests for review.


## 📑 Content Map

| File | Description |
|------|-------------|
| `SKILL.md` | Main Skill Definition |
