---
description: "Knowledge Base — Secure Coding Fundamentals"
type: "reference"
scope: "universal"
stack: "language-agnostic"
last_updated: "2025-01-01"
---

# Secure Coding Fundamentals

**Purpose:** This is the foundational reference for all secure coding practices. It applies to every feature, every language, and every phase of the pipeline. The agent must internalize these principles before generating any code, design, or audit.

---

## 1. Core Security Principles

### 1.1 Defense in Depth
Never rely on a single security control. Layer multiple independent defenses so that if one fails, others still protect the system.

**Example:** A file upload feature should have:
- Layer 1: Client-side file type validation (UX only, not security).
- Layer 2: Server-side Content-Type validation.
- Layer 3: File magic byte verification (check actual file content, not just extension).
- Layer 4: File size limit enforcement.
- Layer 5: Storage outside web root with randomized filenames.
- Layer 6: Virus/malware scanning before processing.

### 1.2 Principle of Least Privilege
Every user, process, service, and component should have only the minimum permissions required to perform its function. Nothing more.

**Application:**
- Database connections should use accounts with restricted permissions (read-only where possible, no DDL).
- API tokens should be scoped to specific actions and resources.
- Container processes should run as non-root users.
- IAM roles should grant only the exact permissions needed.

**Anti-pattern:**
```
# BAD: One database user with full access for everything
DATABASE_URL=postgres://admin:password@db:5432/myapp

# GOOD: Separate users with scoped permissions
DATABASE_READ_URL=postgres://app_reader:xxx@db:5432/myapp
DATABASE_WRITE_URL=postgres://app_writer:xxx@db:5432/myapp
DATABASE_ADMIN_URL=postgres://app_admin:xxx@db:5432/myapp  # Only used by migration scripts
```

### 1.3 Fail Secure (Fail Closed)
When a security control fails or encounters an error, the system must default to the most secure state — deny access, reject the request, close the connection.

**Application:**
- If the authentication service is unreachable, deny all requests (don't allow anonymous access).
- If input validation throws an unexpected error, reject the input (don't pass it through).
- If the authorization check encounters an exception, return 403 (don't return 200).

**Anti-pattern:**
```javascript
// BAD: Fails open — exception allows access
function isAuthorized(user, resource) {
  try {
    return checkPermission(user, resource);
  } catch (error) {
    return true; // DANGEROUS: fails open
  }
}

// GOOD: Fails closed — exception denies access
function isAuthorized(user, resource) {
  try {
    return checkPermission(user, resource);
  } catch (error) {
    logger.error('Authorization check failed', { user: user.id, resource, error });
    return false; // Safe: denies access on failure
  }
}
```

### 1.4 Zero Trust
Never trust any input, any client, any internal service, or any environment variable without explicit verification. Trust is not inherited from network location, request origin, or component identity.

**Application:**
- Validate all input on the server, even if the client already validated it.
- Authenticate inter-service communication (mTLS, signed tokens), even within a private network.
- Verify JWTs on every request, even if a previous middleware "should have" checked it.
- Don't trust HTTP headers (X-Forwarded-For, Origin) unless they come from a verified proxy.

### 1.5 Economy of Mechanism (Keep It Simple)
Security mechanisms should be as simple and small as possible. Complex code has more bugs, and security bugs are the most dangerous.

**Application:**
- Use one centralized authentication module, not auth logic scattered across controllers.
- Use one validation library consistently, not a mix of custom regex and framework validation.
- Use established security libraries, not hand-rolled implementations.

### 1.6 Complete Mediation
Every access to every resource must be checked for authorization. No caching of authorization decisions without explicit invalidation.

**Application:**
- Every API endpoint must pass through authorization middleware.
- Don't cache "user is admin" in a JWT that lives for 24 hours — if the user's role changes, the cache is stale.
- Check resource ownership on every request, not just on first access.

---

## 2. Input Handling Rules

### 2.1 The Cardinal Rule
**All input is hostile until proven otherwise.** This includes:
- HTTP request parameters (query, body, headers, cookies).
- File uploads (name, content, size, type).
- Database values (could have been injected by a previous attack).
- Environment variables (could be misconfigured or tampered with).
- Internal service responses (the service could be compromised).
- URL parameters and path segments.

### 2.2 Validation Strategy: Allowlist Over Denylist
Define what IS allowed, reject everything else. Never try to enumerate all the bad things.

```
# BAD: Denylist — always incomplete
reject if input contains: <script>, javascript:, onerror=

# GOOD: Allowlist — defines exactly what's acceptable
accept if input matches: ^[a-zA-Z0-9\s\-\.]{1,100}$
```

### 2.3 Validation Order
1. **Type check** — Is it the expected data type? (string, number, boolean, array)
2. **Length/size check** — Is it within acceptable bounds?
3. **Format check** — Does it match the expected pattern? (email, UUID, date)
4. **Range check** — Is the value within business logic bounds? (age 0–150, price > 0)
5. **Business logic check** — Is it valid in the current context? (does the referenced ID exist?)

### 2.4 Validate at the Boundary, Encode at the Output
- Input validation happens at the point of entry (API controller, form handler).
- Output encoding happens at the point of output (before rendering HTML, before building SQL).
- Never validate input and then encode it for output at the same time — the contexts may differ.

---

## 3. Authentication Fundamentals

### 3.1 Password Storage
- **NEVER** store passwords in plaintext or reversible encryption.
- **NEVER** use MD5, SHA1, or SHA256 alone for password hashing (they are too fast).
- **USE** Argon2id (preferred), bcrypt (widely supported), or PBKDF2 (last resort).
- **USE** a unique salt per password (auto-generated by Argon2id and bcrypt).
- **CONSIDER** a pepper (server-side secret added before hashing, stored separately).

### 3.2 Session Management
- Session tokens must be generated using a CSPRNG with at least 128 bits of entropy.
- Tokens should be transmitted in HttpOnly, Secure, SameSite cookies — never in URLs.
- Sessions must be invalidated on logout (server-side destruction, not just client-side deletion).
- Implement both idle timeout (e.g., 30 minutes) and absolute timeout (e.g., 8 hours).

### 3.3 JWT Best Practices
- Sign with asymmetric algorithms (RS256, ES256) when possible.
- If symmetric (HS256), the secret must be ≥ 256 bits and truly random.
- Explicitly reject the `none` algorithm.
- Set short expiration (access tokens: 5–15 minutes, refresh tokens: hours–days).
- Never store sensitive PII in the payload (JWTs are base64, not encrypted).
- Validate `iss`, `aud`, `exp`, and `iat` claims on every request.

---

## 4. Authorization Fundamentals

### 4.1 Default Deny
Every route/endpoint must require explicit authorization. If a developer forgets to add authorization, the default behavior must be to deny access.

### 4.2 IDOR Prevention Pattern
For every endpoint that takes a resource ID:
```
WRONG:  SELECT * FROM invoices WHERE id = :input_id
RIGHT:  SELECT * FROM invoices WHERE id = :input_id AND user_id = :authenticated_user_id
```

### 4.3 Mass Assignment Prevention
Never trust the client to tell you which fields to update:
```
WRONG:  User.update(req.body)  // Client can set { role: "admin", isVerified: true }
RIGHT:  User.update({ name: req.body.name, email: req.body.email })  // Explicit allowlist
```

---

## 5. Cryptography Fundamentals

### 5.1 Approved Algorithms

| Purpose | Use | Never Use |
|---|---|---|
| Password hashing | Argon2id, bcrypt, PBKDF2 | MD5, SHA1, SHA256 (alone), plain encryption |
| Symmetric encryption | AES-256-GCM, ChaCha20-Poly1305 | DES, 3DES, RC4, AES-ECB, AES-CBC without HMAC |
| Asymmetric encryption | RSA ≥ 2048 bits, ECDSA P-256+ | RSA < 2048, DSA |
| Hashing (non-password) | SHA-256, SHA-3, BLAKE2 | MD5, SHA1 |
| Random generation | CSPRNG (OS-level) | Math.random(), random.random() |
| Key exchange | ECDH, DH ≥ 2048 | Static DH < 2048 |

### 5.2 Rules
- Never implement your own cryptographic algorithms or protocols.
- Never reuse a key for multiple purposes (signing vs. encryption).
- Never reuse IVs/nonces with the same key.
- Always use authenticated encryption (GCM, not just CBC).
- Use constant-time comparison for secrets and tokens.

---

## 6. Error Handling Fundamentals

### 6.1 Rules
- **Production errors to users:** Generic message + correlation ID. Nothing else.
- **Production errors to logs:** Full details (stack trace, context, request metadata). Never passwords/tokens.
- **Development errors:** Full details everywhere (but never commit this configuration).

### 6.2 Security-Sensitive Errors
- Authentication failure: Log attempt with timestamp, IP, username attempted. Return generic "Invalid credentials."
- Authorization failure: Log with user ID, requested resource, required permission. Return 403.
- Validation failure: Log with input summary (not full input if sensitive). Return 400 with field-level errors (no internal details).

### 6.3 Account Enumeration Prevention
All of these must return identical responses and identical timing:
- Login with valid email, wrong password.
- Login with non-existent email.
- Password reset for existing email.
- Password reset for non-existing email.

---

## 7. Logging Fundamentals

### 7.1 What to Log (Always)
- Authentication events: login success, login failure, logout, password change, MFA enrollment.
- Authorization events: access denied (403), permission elevation, role changes.
- Data events: create, update, delete of sensitive records.
- System events: application start/stop, configuration changes, deployment events.
- Security events: input validation failures, rate limit triggers, suspicious activity.

### 7.2 What to NEVER Log
- Passwords (plaintext or hashed).
- Session tokens, JWTs, API keys.
- Credit card numbers (log last 4 digits only if needed).
- Social Security Numbers or equivalent national IDs.
- Full PII (mask email: `j***@example.com`, mask phone: `***-***-1234`).

### 7.3 Log Format
Use structured logging (JSON) with consistent fields:
```json
{
  "timestamp": "2025-01-15T10:30:00.000Z",
  "level": "warn",
  "event": "auth.login.failed",
  "actor": "user@example.com",
  "ip": "192.168.1.100",
  "userAgent": "Mozilla/5.0...",
  "correlationId": "req-abc-123",
  "message": "Failed login attempt — invalid password"
}
```

---

## 8. Secure Communication Fundamentals

### 8.1 TLS Requirements
- TLS 1.2 minimum. TLS 1.3 preferred. TLS 1.0 and 1.1 disabled.
- HSTS header with `max-age >= 31536000`, `includeSubDomains`.
- HTTP → HTTPS redirect on all endpoints.
- Certificate validation enabled on all outbound connections (never disable it).

### 8.2 Internal Communications
- Service-to-service communication should use TLS or mTLS, even within a private network.
- Database connections should use TLS (`?sslmode=require` for PostgreSQL).
- Cache connections (Redis) should use TLS in production.

---

## 9. Secure File Handling Fundamentals

### 9.1 Upload Rules
- Validate file type by magic bytes, not just extension or Content-Type header.
- Enforce strict file size limits (server-side, not just client-side).
- Store uploads outside the web root.
- Rename files to random UUIDs — never use the original filename in storage.
- Serve files with `Content-Disposition: attachment` and from a separate domain if possible.
- Scan for malware before processing.

### 9.2 Anti-patterns
```
# BAD: Using original filename (path traversal risk)
const path = `/uploads/${req.file.originalname}`;

# BAD: Trusting Content-Type header
if (req.file.mimetype === 'image/png') { /* process */ }

# GOOD: Random name + magic byte check
const filename = `${crypto.randomUUID()}.bin`;
const magic = readMagicBytes(req.file.buffer);
if (!ALLOWED_MAGIC_BYTES.includes(magic)) throw new ValidationError('Invalid file type');
```

---

## 10. Dependency Management Fundamentals

### 10.1 Rules
- Pin dependencies to exact versions in production.
- Commit lockfiles to version control.
- Run `npm audit` / `pip-audit` in CI/CD — fail the build on Critical/High findings.
- Review new dependencies before adding (see Phase 2c workflow).
- Monitor for new CVEs continuously (Dependabot, Snyk, Renovate).
- Remove unused dependencies — every package is attack surface.

### 10.2 Supply Chain Attacks to Watch For
- **Typosquatting:** `requets` instead of `requests`.
- **Dependency Confusion:** Private package name published publicly.
- **Compromised Maintainer:** Legitimate package updated with malicious code.
- **Install Scripts:** Packages running arbitrary code during `npm install`.
