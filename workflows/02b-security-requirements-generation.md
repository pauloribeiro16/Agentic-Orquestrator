---
description: "Phase 2b — Security Requirements Generation"
phase: 2
nist_ssdf: "PS.1 — Protect All Forms of Code"
asvs_reference: "Multiple chapters — selected based on feature type"
triggers: "Called by 00-pipeline-orchestrator.md after 02a completes"
input_required: "Secure Design (02a) + Threat Report (Phase 1)"
---

# Phase 2b: Security Requirements Generation

**Purpose:** Derive a concrete, testable checklist of security requirements from the threat model and secure design. Each requirement is traceable to a specific ASVS control, making it directly verifiable in Phase 3.

---

## Step 1: Identify Applicable ASVS Chapters

**Action:** Based on the feature brief and the secure design document, determine which ASVS chapters are relevant.

**Selection logic:**

| Feature Characteristic | ASVS Chapters to Load |
|---|---|
| Any feature (always applicable) | V1 (Architecture), V5 (Validation), V14 (Configuration) |
| Has user authentication | V2 (Authentication) |
| Has session management | V3 (Session Management) |
| Has role/resource-based access | V4 (Access Control) |
| Stores/transmits sensitive data | V6 (Cryptography), V8 (Data Protection), V9 (Communications) |
| Has error handling or logging | V7 (Error Handling) |
| Exposes REST or GraphQL endpoints | V13 (API & Web Services) |

**Action:** Load the corresponding files from `asvs-reference/` for each applicable chapter. Extract all Level 2 requirements from those files.

---

## Step 2: Map ASVS Requirements to Feature Components

**Action:** For each loaded ASVS requirement, determine if it applies to this specific feature.

**For each requirement, assess:**

1. **Applicable?** — Does this requirement relate to any component, data flow, or control in the feature's architecture?
2. **Component** — Which specific part of the feature does this requirement apply to? (e.g., login endpoint, file upload service, user profile API)
3. **Priority** — Based on the threat report's risk ratings, which requirements address Critical/High threats first?

**Output format:**

```markdown
| Req ID | Requirement Text | Applicable | Component | Priority | Notes |
|---|---|---|---|---|---|
| V2.1.1 | [Full ASVS requirement text] | Yes | Login endpoint | High | Addresses threat S-001 |
| V5.1.3 | [Full ASVS requirement text] | Yes | Profile update API | Critical | Addresses threat T-001 |
| V3.2.1 | [Full ASVS requirement text] | N/A | — | — | Feature uses JWT, not cookies |
```

---

## Step 3: Derive Feature-Specific Security Requirements

**Action:** Transform the applicable ASVS requirements into concrete, feature-specific implementation requirements that a developer can act on directly.

**Transformation rules:**
- ASVS requirements are generic by design. Rewrite each applicable one as a specific instruction for THIS feature with THIS stack.
- Include the specific library, function, or configuration to use.
- Include a clear "definition of done" — what does passing look like?

**Example transformation:**

```
ASVS Generic:
  V2.1.1: "Verify that user set passwords are at least 12 characters in length."

Feature-Specific Requirement:
  REQ-AUTH-001: "The registration endpoint (POST /api/v1/auth/register) must validate
  that the 'password' field is a minimum of 12 characters using Zod schema validation
  before passing to the bcrypt hashing function."
  
  Definition of Done: Zod schema enforces z.string().min(12) on the password field.
  Requests with shorter passwords receive a 400 response with a generic validation error.
  
  Traces to: ASVS V2.1.1, Threat S-001
```

---

## Step 4: Organize Requirements by Domain

**Action:** Group all feature-specific requirements into logical domains for clarity.

**Standard domains:**

1. **Authentication Requirements (REQ-AUTH-xxx)**
   - Password policies, credential storage, brute force protection, MFA.

2. **Session Requirements (REQ-SESS-xxx)**
   - Token generation, validation, expiration, revocation.

3. **Access Control Requirements (REQ-AUTHZ-xxx)**
   - Role checks, ownership verification, IDOR prevention, default deny.

4. **Input Validation Requirements (REQ-INPUT-xxx)**
   - Schema validation, type checking, size limits, allowlisting.

5. **Output Encoding Requirements (REQ-OUTPUT-xxx)**
   - Response filtering, XSS prevention, error message sanitization.

6. **Cryptography Requirements (REQ-CRYPTO-xxx)**
   - Hashing algorithms, encryption at rest, key management.

7. **Communication Requirements (REQ-COMM-xxx)**
   - TLS enforcement, HSTS, internal service encryption.

8. **Logging Requirements (REQ-LOG-xxx)**
   - Event coverage, data redaction, log integrity.

9. **API Requirements (REQ-API-xxx)**
   - Content-type enforcement, schema validation, rate limiting.

10. **Configuration Requirements (REQ-CONFIG-xxx)**
    - Security headers, debug mode, default accounts.

---

## Step 5: Generate Assessment Template

**Action:** For each requirement, pre-generate the assessment template that Phase 3 will fill in.

**Template per requirement:**

```markdown
### REQ-AUTH-001: Password Minimum Length
- **ASVS Trace:** V2.1.1
- **Threat Trace:** S-001
- **Description:** Registration endpoint must enforce minimum 12-character passwords via Zod schema validation.
- **Definition of Done:** Zod schema with z.string().min(12) on password field. 400 response for violations.
- **Assessment:**
  - [ ] PASS — Requirement is securely implemented.
  - [ ] FAIL — Requirement is not met. File: ___ Line: ___ Evidence: ___
  - [ ] N/A — Requirement does not apply. Justification: ___
```

---

## Step 6: Compile Security Requirements Document

**Action:** Generate `outputs/[feature-name]/security-requirements.md` with the following structure:

```markdown
# Security Requirements: [Feature Name]

## Summary
- **Total Requirements:** [count]
- **Critical Priority:** [count]
- **High Priority:** [count]
- **Medium Priority:** [count]
- **ASVS Chapters Covered:** [list]

## ASVS Mapping Table
[Table from Step 2]

## Requirements by Domain

### Authentication Requirements
[REQ-AUTH-001 through REQ-AUTH-xxx with assessment templates]

### Session Requirements
[REQ-SESS-001 through REQ-SESS-xxx with assessment templates]

### Access Control Requirements
[REQ-AUTHZ-001 through REQ-AUTHZ-xxx with assessment templates]

[... continue for each applicable domain ...]

## Traceability Matrix
| Requirement ID | ASVS Control | Threat ID | Priority |
|---|---|---|---|
| REQ-AUTH-001 | V2.1.1 | S-001 | High |
| REQ-AUTHZ-001 | V4.2.1 | E-001 | Critical |
```

**Next:** This document feeds directly into Phase 3 (`03-asvs-audit-orchestrator.md`) where each requirement is verified against the actual code.
