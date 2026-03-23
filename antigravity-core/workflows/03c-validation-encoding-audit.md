---
description: "Phase 3c — Validation, Sanitization & Encoding Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v5-validation.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature accepts user input"
input_required: "security-requirements.md (REQ-INPUT-xxx, REQ-OUTPUT-xxx)"
---

# Phase 3c: Validation, Sanitization & Encoding Audit

**ASVS Chapter:** V5 (Validation, Sanitization and Encoding)

**CRITICAL:** Load `asvs-reference/asvs-v5-validation.md` before starting.

---

## Step 1: Discovery

**Action:** Map the flow of user-controlled data from entry to exit.

**Identify:**
- All entry points: HTTP headers, query params, body payloads, file uploads, WebSocket messages.
- All critical exit points: database queries, OS command execution, XML parsers, HTML rendering, redirect URLs, log statements.
- Validation libraries in use (Zod, Joi, Pydantic, class-validator).
- Sanitization utilities and encoding functions.

---

## Step 2: V5.1 — Input Validation

**What to check:**

1. **Positive Validation (Allowlisting):** Does the application define what IS allowed (allowlist) rather than what is NOT allowed (denylist)?
2. **Schema Validation:** Is every input validated against a defined schema (type, length, format, range) BEFORE any business logic executes?
3. **Framework Utilization:** Does the application use established validation libraries correctly? Check for:
   - Node.js: Zod, Joi, express-validator, class-validator
   - Python: Pydantic, marshmallow, WTForms
4. **Data Limits:** Are explicit limits set for: string length, array size, numeric range, nested object depth, file upload size?
5. **Content-Type Enforcement:** Does the API reject requests with unexpected Content-Type headers?

---

## Step 3: V5.2 — Sanitization & Injection Defense

**What to check:**

1. **SQL Injection:**
   - Scan ALL database interactions. Are parameterized queries, prepared statements, or ORM methods used exclusively?
   - Flag ANY instance of string concatenation or template literals constructing SQL queries with user input.
   - Check for raw query escape hatches in ORMs (`$queryRaw`, `Model.query()`, `text()`) that may bypass parameterization.

2. **NoSQL Injection:**
   - If MongoDB/similar is used, check for operator injection (e.g., `{"$gt": ""}` in login queries).
   - Verify that query inputs are type-checked (string, number) before inclusion in NoSQL queries.

3. **OS Command Injection:**
   - Search for `exec`, `spawn`, `execSync`, `child_process`, `subprocess.run`, `os.system`, `eval`.
   - Is user input EVER passed to any of these functions? If yes, is it strictly sanitized with argument separation (not shell string)?

4. **Path Traversal:**
   - Are file paths constructed with user input validated to prevent `../` traversal?
   - Is the resolved path checked to ensure it remains within the intended directory?

5. **SSRF:**
   - Does the feature make outbound HTTP requests based on user-supplied URLs?
   - Is there a strict domain allowlist? Are internal IPs (`127.0.0.1`, `169.254.169.254`, `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`) explicitly blocked?

---

## Step 4: V5.3 — Output Encoding (XSS Defense)

**What to check:**

1. **Context-Aware Encoding:** Is data encoded appropriately for its output context?
   - HTML context: HTML entity encoding.
   - JavaScript context: JavaScript encoding.
   - URL context: URL encoding.
   - CSS context: CSS encoding.

2. **Framework Bypass Detection:** Scan for functions that bypass built-in XSS protection:
   - React: `dangerouslySetInnerHTML`
   - Vue: `v-html`
   - Angular: `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`
   - Template engines: `| safe`, `{{{ }}}` (triple mustache), `<%- %>` (unescaped EJS)

3. **Content Security Policy (CSP):** Is a CSP header configured that restricts inline scripts and unsafe-eval?

---

## Step 5: Compile Assessment

**Action:** For every Level 2 requirement in V5, record PASS/FAIL/N-A.

**Output:** Append all V5 assessments to `outputs/[feature-name]/audit-workflow.md`.
