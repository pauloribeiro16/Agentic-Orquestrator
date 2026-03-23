---
description: "Phase 3e — Error Handling & Logging Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v7-error-handling.md, asvs-v8-data-protection.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature has error handling or logging"
input_required: "security-requirements.md (REQ-LOG-xxx)"
---

# Phase 3e: Error Handling & Logging Audit

**ASVS Chapters:** V7 (Error Handling), V8 (Data Protection)

**CRITICAL:** Load `asvs-reference/asvs-v7-error-handling.md` and `asvs-reference/asvs-v8-data-protection.md` before starting.

---

## Step 1: Discovery

**Locate:**
- Global error-handling middleware and custom exception classes.
- `try/catch` blocks in critical controllers.
- Logging utility configuration (Winston, Pino, Morgan, structlog, logging module).
- Log output destinations (files, stdout, external services).
- Monitoring and alerting integrations (Sentry, Datadog, etc.).

---

## Step 2: V7.1 — Error Handling Verification

**What to check:**

1. **Stack Trace Leakage:** Do global error handlers prevent stack traces, SQL errors, and framework internals from reaching the end-user in production?
2. **Generic Error Messages:** Are user-facing errors generic ("An unexpected error occurred") rather than specific ("SQL syntax error near SELECT")?
3. **Fail-Secure:** When authentication or authorization modules throw errors, does the system default to denying access?
4. **Consistent Handling:** Do all error paths (sync, async, promise rejections, unhandled exceptions) converge to the same secure error handler?

---

## Step 3: V8.1 — Log Content & Sanitization

**What to check:**

1. **Event Coverage:** Are these events logged? Login success/failure, password changes, access control failures (403), critical data modifications, admin actions.
2. **Data Redaction:** Scan ALL log statements to ensure the following are NEVER logged in plaintext: passwords, JWT tokens, session cookies, credit card numbers, SSNs, API keys.
3. **Log Injection:** Is user-supplied input sanitized before being written to logs? Can an attacker inject newline characters (`\n`, `\r`) to forge log entries?
4. **Log Format:** Are logs structured (JSON format) for machine parseability and SIEM ingestion?

---

## Step 4: V8.2 — Log Integrity

**What to check:**

1. **Storage Location:** Are logs stored outside the web root? Can they be directly downloaded via browser?
2. **Access Control:** Does the application process have append-only permissions to log files (cannot modify or delete)?
3. **Sensitive Data in Monitoring:** Are error tracking services (Sentry, Bugsnag) configured to scrub sensitive data before transmission?

---

## Step 5: Compile Assessment

**Action:** For every Level 2 requirement in V7 and V8, record PASS/FAIL/N-A.

**Output:** Append all V7 and V8 assessments to `outputs/[feature-name]/audit-workflow.md`.
