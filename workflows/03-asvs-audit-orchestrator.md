---
description: "Phase 3 Orchestrator — ASVS Verification & Testing"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities on an Ongoing Basis"
triggers: "Called by 00-pipeline-orchestrator.md after Phase 2 Human Gate approval"
input_required: "Approved secure-design.md and security-requirements.md from Phase 2"
---

# Phase 3 Orchestrator: ASVS Verification & Testing

**Purpose:** This orchestrator selects and executes the relevant ASVS audit sub-workflows based on the feature's characteristics. It then generates test scripts for dynamic verification. This phase verifies that the BUILT code matches the DESIGNED security requirements from Phase 2.

---

## Step 1: Load Phase 2 Outputs

**Action:** Read the approved outputs from Phase 2:
1. `outputs/[feature-name]/secure-design.md` — Architecture decisions and controls.
2. `outputs/[feature-name]/security-requirements.md` — The full requirements checklist with PASS/FAIL/N-A templates.

---

## Step 2: Select Applicable Sub-Workflows

**Action:** Based on the feature brief and Phase 2 outputs, select which audit sub-workflows to execute.

**Selection matrix:**

| Feature Characteristic | Sub-Workflow | ASVS Reference Files to Load |
|---|---|---|
| Has login / registration / password flows | `03a-auth-session-audit.md` | `asvs-v2-authentication.md`, `asvs-v3-session.md` |
| Has role-based or resource-based access | `03b-access-control-audit.md` | `asvs-v4-access-control.md` |
| Accepts user input (forms, APIs, uploads) | `03c-validation-encoding-audit.md` | `asvs-v5-validation.md` |
| Stores/transmits sensitive data, uses encryption | `03d-crypto-communications-audit.md` | `asvs-v6-cryptography.md`, `asvs-v9-communications.md` |
| Has error handling, logging, or audit trails | `03e-error-logging-audit.md` | `asvs-v7-error-handling.md`, `asvs-v8-data-protection.md` |
| Exposes REST or GraphQL endpoints | `03f-api-graphql-audit.md` | `asvs-v13-api.md` |
| Adds new third-party dependencies | `03g-secrets-dependencies-audit.md` | N/A (uses CVE databases) |
| Modifies server/container/deployment config | `03h-configuration-audit.md` | `asvs-v14-configuration.md` |
| Modifies CI/CD pipelines or GitHub Actions | `03i-cicd-pipeline-audit.md` | N/A |

**Always load:** `asvs-reference/asvs-v1-architecture.md` — applies to all features as the architectural baseline.

**Record the selection** in the output:
```markdown
## Phase 3 — Sub-Workflow Selection
- [x] 03a — Auth & Session Audit (V2, V3)
- [ ] 03b — Access Control Audit (V4) — SKIPPED: Feature has no resource-based access
- [x] 03c — Validation & Encoding Audit (V5)
- [x] 03d — Crypto & Communications Audit (V6, V9)
- [x] 03e — Error Handling & Logging Audit (V7, V8)
- [x] 03f — API & GraphQL Audit (V13)
- [ ] 03g — Secrets & Dependencies Audit — SKIPPED: No new dependencies
- [ ] 03h — Configuration Audit (V14) — SKIPPED: No config changes
- [ ] 03i — CI/CD Pipeline Audit — SKIPPED: No pipeline changes
```

---

## Step 3: Load ASVS Reference Files

**Action:** For each selected sub-workflow, load the corresponding ASVS reference files from `asvs-reference/`.

**CRITICAL RULES:**
1. The agent MUST have the full ASVS requirement text loaded in context. It must NEVER search the web for requirements.
2. Only Level 1 and Level 2 requirements are in scope. Level 3 requirements are informational only.
3. Each ASVS reference file contains: Requirement ID → Full Text → Level → Verifiable (Yes/No) → Suggested Test Approach.

---

## Step 4: Execute Selected Sub-Workflows (Parallel Strategy)

**Action:** To optimize execution time, group the selected sub-workflows and execute them in parallel where possible. Grouping strategy:

**Execution Groups:**
1. **Group A (Access):** `03a` (Auth) + `03b` (Access Control)
2. **Group B (Data):** `03c` (Validation) + `03d` (Crypto) + `03e` (Error/Logging)
3. **Group C (Infrastructure):** `03f` (API) + `03g` (Secrets) + `03h` (Config) + `03i` (CI/CD)

**Execution Flow:** Execute Group A. Then execute Group B and Group C *in parallel*. Consolidate findings at the end.

For each executed sub-workflow:

1. Read the corresponding ASVS reference file.
2. Analyze the feature's code against each applicable requirement.
3. Produce an assessment for every requirement using the PASS/FAIL/N-A matrix.

**Assessment matrix format (mandatory for every requirement):**

```markdown
### [Requirement ID]: [Requirement Title]
**ASVS Text:** "[Full requirement text from the reference file]"
**Level:** L2
**Verifiable:** Yes / No

**Assessment:**
- [ ] PASS — The code securely implements this requirement.
  - Evidence: [File path, code reference, configuration reference]
- [ ] FAIL — The code does not meet this requirement.
  - File: [path]
  - Line: [number]
  - Evidence: [code snippet showing the failure]
  - Remediation: [Specific fix with code suggestion]
- [ ] N/A — This requirement does not apply to this feature.
  - Justification: [Brief explanation]
```

---

## Step 5: Generate Test Scripts

**Action:** For each FAIL finding and each verifiable requirement, generate executable test scripts.

### 5.1 Python Test Scripts (`[feature]-security-tests.py`)

**Requirements:**
- Use `requests` library for HTTP tests.
- Use `pytest` as the test framework.
- Each test must be self-contained with setup, execution, and assertion.
- Include tests for:
  - Input validation boundary testing (malformed inputs, oversized payloads, injection payloads).
  - Authentication bypass attempts (missing tokens, expired tokens, forged tokens).
  - Authorization bypass attempts (accessing other users' resources, escalation attempts).
  - Error handling verification (triggering errors and verifying generic responses).

**Template:**
```python
"""
Security Tests: [Feature Name]
Generated by DevSecOps Pipeline — Phase 3
ASVS Level 2 Verification
"""

import pytest
import requests

BASE_URL = "http://localhost:3000"  # Configure per environment

class TestAuthenticationSecurity:
    """ASVS V2 — Authentication Verification"""

    def test_v2_1_1_password_minimum_length(self):
        """V2.1.1: Verify passwords are at least 12 characters."""
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": "test@example.com",
            "password": "short"  # 5 chars — should fail
        })
        assert response.status_code == 400, \
            f"FAIL V2.1.1: Server accepted a 5-character password (status {response.status_code})"
```

### 5.2 JavaScript Test Scripts (`[feature]-security-tests.js`)

**Requirements:**
- Use `fetch` or `axios` for HTTP tests.
- Use `jest` or `vitest` as the test framework.
- Mirror the same test coverage as the Python scripts.

**Template:**
```javascript
/**
 * Security Tests: [Feature Name]
 * Generated by DevSecOps Pipeline — Phase 3
 * ASVS Level 2 Verification
 */

const BASE_URL = "http://localhost:3000";

describe("ASVS V2 — Authentication Verification", () => {
  test("V2.1.1: Password minimum length enforcement", async () => {
    const response = await fetch(`${BASE_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "test@example.com", password: "short" }),
    });
    expect(response.status).toBe(400);
  });
});
```

---

## Step 6: Compile Audit Report

**Action:** Generate `outputs/[feature-name]/audit-workflow.md` with the following structure:

```markdown
# ASVS Audit Report: [Feature Name]

## Audit Metadata
- **Date:** [timestamp]
- **Feature:** [name]
- **ASVS Version:** 4.0.3
- **Audit Level:** Level 2
- **Sub-Workflows Executed:** [list]
- **ASVS Chapters Covered:** [list]

## Summary
- **Total Requirements Assessed:** [count]
- **PASS:** [count]
- **FAIL:** [count]
- **N/A:** [count]

## Critical & High Findings
[List only FAIL items rated Critical or High — these block deployment]

## Full Assessment Matrix

### V2 — Authentication
[All V2 assessments from 03a]

### V3 — Session Management
[All V3 assessments from 03a]

### V4 — Access Control
[All V4 assessments from 03b]

[... continue for each executed sub-workflow ...]

## Remediation Priority
| # | Requirement | Severity | Effort | Recommended Fix |
|---|---|---|---|---|
| 1 | V4.2.1 — IDOR in invoice API | Critical | Low | Add ownership check to query |
| 2 | V2.2.1 — No rate limiting on login | High | Medium | Add express-rate-limit middleware |
```

**Also output:**
- `outputs/[feature-name]/security-tests.py`
- `outputs/[feature-name]/security-tests.js`

**⏸ HUMAN GATE:** Present the audit report and test scripts for review.
