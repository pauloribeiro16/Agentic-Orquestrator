---
description: "Phase 3d — Cryptography & Communications Security Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v6-cryptography.md, asvs-v9-communications.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature stores/transmits sensitive data"
input_required: "security-requirements.md (REQ-CRYPTO-xxx, REQ-COMM-xxx)"
---

# Phase 3d: Cryptography & Communications Security Audit

**ASVS Chapters:** V6 (Cryptography), V9 (Communications)

**CRITICAL:** Load `asvs-reference/asvs-v6-cryptography.md` and `asvs-reference/asvs-v9-communications.md` before starting.

---

## Step 1: Discovery

**Locate:**
- Encryption/decryption functions and hashing utilities.
- Database connection strings and their encryption settings.
- TLS/SSL configuration files.
- HTTP client configurations for outbound requests.
- Key/secret storage mechanisms (env vars, vaults, config files).
- Random number generation functions.

---

## Step 2: V6.1 — Cryptographic Algorithm Verification

**What to check:**

1. **Deprecated Algorithms:** Scan for and flag: MD5, SHA1 (for security purposes), DES, 3DES, RC4, RSA < 2048 bits, ECB mode.
2. **Approved Algorithms:** Verify usage of: AES-128/256-GCM, SHA-256+, ChaCha20-Poly1305, RSA ≥ 2048, ECDSA P-256+.
3. **Custom Cryptography:** Flag any hand-rolled cryptographic implementations. The application must use established libraries (libsodium, WebCrypto API, `crypto` module in Node.js, `cryptography` in Python).
4. **Randomness:** Verify all random values (tokens, keys, nonces, IDs) use CSPRNG:
   - Node.js: `crypto.randomBytes()`, `crypto.randomUUID()` — NOT `Math.random()`.
   - Python: `secrets.token_bytes()`, `secrets.token_hex()` — NOT `random.random()`.

---

## Step 3: V6.2 — Key Management

**What to check:**

1. **Hardcoded Secrets:** Scan for hardcoded API keys, database passwords, JWT signing secrets, encryption keys in source code.
2. **Environment Variables:** Verify secrets are loaded from environment variables or a secrets manager — not from config files committed to version control.
3. **Key Purpose Separation:** Is the same key reused for multiple purposes (e.g., JWT signing AND database encryption)? Each purpose must have its own key.
4. **Key Rotation:** Is there a mechanism to rotate keys without downtime?

---

## Step 4: V9.1 — Communications Security

**What to check:**

1. **TLS Enforcement:** Is HTTPS enforced on all endpoints? Is there HTTP → HTTPS redirect logic?
2. **HSTS Header:** Is `Strict-Transport-Security` sent with `max-age >= 31536000` and `includeSubDomains`?
3. **TLS Version:** Is TLS 1.2 the minimum version? Is TLS 1.0/1.1 explicitly disabled?
4. **Certificate Validation:** For outbound HTTPS requests, is certificate validation enabled? Flag any `rejectUnauthorized: false` (Node.js) or `verify=False` (Python requests).
5. **Internal Communications:** If the feature communicates with internal services, is TLS/mTLS used for inter-service traffic?

---

## Step 5: Compile Assessment

**Action:** For every Level 2 requirement in V6 and V9, record PASS/FAIL/N-A.

**Output:** Append all V6 and V9 assessments to `outputs/[feature-name]/audit-workflow.md`.
