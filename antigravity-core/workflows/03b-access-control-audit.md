---
description: "Phase 3b — Access Control Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v4-access-control.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature has role/resource-based access"
input_required: "security-requirements.md (REQ-AUTHZ-xxx)"
---

# Phase 3b: Access Control Audit

**ASVS Chapter:** V4 (Access Control)

**CRITICAL:** Load `asvs-reference/asvs-v4-access-control.md` before starting.

---

## Step 1: Discovery

**Action:** Locate all authorization-related code.

**Files to find:**
- RBAC/ABAC middleware and decorators.
- Route guards and permission checks.
- Controllers handling CRUD operations on user-owned resources.
- Admin-only routes and administrative interfaces.
- CORS configuration files.

---

## Step 2: V4.1 — General Access Control Design

**What to check:**

1. **Default Deny:** Are all endpoints protected by default? Is authorization explicitly required, not implicitly granted?
2. **Principle of Least Privilege:** Does each role have only the minimum permissions necessary?
3. **Admin Segregation:** Are admin routes in a separate namespace (e.g., `/api/admin/*`) with distinct, stricter middleware?
4. **Consistent Enforcement:** Is access control enforced at a trusted layer (server-side middleware/service), never relying on client-side checks alone?

---

## Step 3: V4.2 — Operation Level Access Control (IDOR)

**What to check:**

1. **Data Ownership Validation:** For every endpoint that accepts a resource ID (`/api/resources/:id`), does the backend verify that the authenticated user owns or has permission to access that specific resource?
2. **Pattern to verify:** The database query must include an ownership clause:
   - `WHERE resource.id = :input_id AND resource.owner_id = :authenticated_user_id`
   - Or equivalent ORM check.
3. **Bulk Operations:** If the feature supports batch operations (delete multiple, update multiple), does each item in the batch go through individual authorization checks?
4. **Indirect References:** Does the application use indirect references (mapping internal IDs to user-facing tokens) for sensitive resources?

---

## Step 4: V4.3 — Other Access Control Issues

**What to check:**

1. **Path Traversal:** If the application serves files based on user input, are inputs validated to prevent `../` or `%2e%2e%2f` escapes?
2. **CORS Configuration:**
   - Does `Access-Control-Allow-Origin` avoid wildcard `*` for credentialed endpoints?
   - Is the `Origin` header validated against a strict allowlist (not dynamically echoed)?
   - Are `Access-Control-Allow-Methods` restricted to only necessary HTTP methods?
3. **Forced Browsing:** Can unauthenticated users access protected resources by directly navigating to the URL?

---

## Step 5: Compile Assessment

**Action:** For every Level 2 requirement in V4, record PASS/FAIL/N-A.

**Output:** Append all V4 assessments to `outputs/[feature-name]/audit-workflow.md`.
