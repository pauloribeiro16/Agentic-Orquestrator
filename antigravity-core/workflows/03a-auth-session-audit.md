---
description: "Phase 3a — Authentication & Session Management Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v2-authentication.md, asvs-v3-session.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature has authentication or session management"
input_required: "security-requirements.md (REQ-AUTH-xxx, REQ-SESS-xxx)"
---

# Phase 3a: Authentication & Session Management Audit

**ASVS Chapters:** V2 (Authentication), V3 (Session Management)

**CRITICAL:** Load `asvs-reference/asvs-v2-authentication.md` and `asvs-reference/asvs-v3-session.md` before starting. Every requirement must be assessed with its full text — do NOT paraphrase or abbreviate.

---

## Step 1: Discovery

**Action:** Locate all authentication and session-related code in the feature.

**Files to find:**
- Login, registration, and logout controllers/routes.
- Password reset and recovery flows.
- JWT/token generation, validation, and refresh logic.
- Session storage configuration (Redis, database, in-memory).
- Authentication middleware and decorators.
- Cookie configuration and settings.

---

## Step 2: V2 — Authentication Verification

**Action:** For each Level 2 requirement in `asvs-v2-authentication.md`, assess the code.

### 2.1 Password Security
**What to check:**
1. **Password length policy:** Does the application enforce a minimum of 12 characters? Does it allow at least 128 characters?
2. **Password composition:** Does the application allow any characters (including Unicode and spaces) without restricting character types?
3. **Password hashing:** Is the password stored using `Argon2id`, `bcrypt` (cost factor ≥ 10), or `PBKDF2` (iterations ≥ 310,000)? Flag MD5, SHA1, SHA256 without salt, or any reversible encoding.
4. **Breach password check:** Does the application check passwords against known breached password lists (e.g., Have I Been Pwned API)?

### 2.2 Brute Force Protection
**What to check:**
1. **Rate limiting:** Is the login endpoint rate-limited? What is the threshold (recommended: max 100 attempts per hour per account)?
2. **Account lockout:** After repeated failures, is the account temporarily locked or is CAPTCHA triggered?
3. **Timing attacks:** Does the login response take the same time for valid vs. invalid usernames? (Prevent username enumeration via timing)

### 2.3 Credential Recovery
**What to check:**
1. **Account enumeration:** Does the forgot-password endpoint return different messages for existing vs. non-existing accounts? It must always return a generic message (e.g., "If the email exists, a link was sent").
2. **Recovery tokens:** Are reset tokens cryptographically random, short-lived (< 1 hour), and single-use?
3. **Secure delivery:** Are reset tokens sent via a side channel (email) rather than returned in the API response?

### 2.4 Credential Storage
**What to check:**
1. **No plaintext passwords:** Verify passwords are never stored or logged in plaintext anywhere — database, logs, error messages, monitoring.
2. **No hardcoded credentials:** Scan for hardcoded passwords, API keys, or default accounts in the codebase.

---

## Step 3: V3 — Session Management Verification

**Action:** For each Level 2 requirement in `asvs-v3-session.md`, assess the code.

### 3.1 Session Token Generation
**What to check:**
1. **Entropy:** Are session IDs/tokens generated using a CSPRNG with at least 128 bits of entropy?
2. **Unpredictability:** Can session identifiers be predicted or enumerated?

### 3.2 Cookie Security (if cookies are used)
**What to check:**
1. **Secure flag:** Is `Secure` attribute set? (Only transmit over HTTPS)
2. **HttpOnly flag:** Is `HttpOnly` attribute set? (Prevent JavaScript access)
3. **SameSite attribute:** Is `SameSite=Strict` or `SameSite=Lax` set?
4. **Path and Domain:** Are path and domain attributes as restrictive as possible?

### 3.3 JWT Security (if JWTs are used)
**What to check:**
1. **Algorithm:** Is the signing algorithm explicitly set to `RS256`, `ES256`, or `HS256` with a strong secret (≥ 256 bits)? Is the `none` algorithm explicitly rejected?
2. **Expiration:** Is the `exp` claim enforced with a short lifetime (recommended: < 15 minutes for access tokens)?
3. **Validation:** Is the signature strictly validated on every request? Are claims (`iss`, `aud`, `exp`) all checked?
4. **Payload sensitivity:** Is sensitive PII excluded from the JWT payload? (JWTs are base64-encoded, NOT encrypted)

### 3.4 Logout and Invalidation
**What to check:**
1. **Server-side destruction:** On logout, is the server-side session state destroyed (not just the client-side cookie/token)?
2. **Token revocation:** For JWTs, is there a blocklist/denylist mechanism or token rotation to handle early invalidation?
3. **Idle timeout:** Do sessions expire after a configurable period of inactivity?
4. **Absolute timeout:** Is there a maximum session lifetime regardless of activity?

---

## Step 4: Compile Assessment

**Action:** For every Level 2 requirement in V2 and V3, record the assessment using the mandatory PASS/FAIL/N-A format defined in the `03-asvs-audit-orchestrator.md`.

**Output:** Append all V2 and V3 assessments to `outputs/[feature-name]/audit-workflow.md`.
