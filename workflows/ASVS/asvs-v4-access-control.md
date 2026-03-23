---
description: "ASVS V4 — Access Control Verification Requirements"
asvs_version: "4.0.3"
chapter: "V4"
applicable_phases: "Phase 3 (03b-access-control-audit)"
---

# ASVS V4: Access Control Verification Requirements

**Scope:** Authorization is the concept of allowing access to resources only to those permitted to use them. This chapter covers access control design, operation-level checks (IDOR), and other access control concerns.

---

## V4.1 — General Access Control Design

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V4.1.1 | Verify that the application enforces access control rules on a trusted service layer, especially if client-side access control is present and could be bypassed. | L1 | Yes | Code Review: Confirm all authorization logic is server-side. Client checks are cosmetic only. |
| V4.1.2 | Verify that all user and data attributes and policy information used by access controls cannot be manipulated by end users unless specifically authorized. | L1 | Yes | Code Review: Check that role/permission attributes cannot be set via user-facing APIs (mass assignment). |
| V4.1.3 | Verify that the principle of least privilege exists — users should only be able to access functions, data files, URLs, controllers, services, and other resources, for which they possess specific authorization. This implies protection against spoofing and elevation of privilege. | L1 | Yes | Dynamic Test: Authenticate as low-privilege user and attempt to access high-privilege resources. |
| V4.1.4 | Verify that the principle of deny by default exists whereby new users/roles start with minimal or no permissions and users/roles do not receive access to new features until access is explicitly assigned. | L1 | Yes | Code Review: Check default permission state for new users/roles. Must default to no access. |
| V4.1.5 | Verify that access controls fail securely including when an exception occurs. | L1 | Yes | Code Review: Check that authorization middleware returns 403/401 on error, not a pass-through. |

---

## V4.2 — Operation Level Access Control

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V4.2.1 | Verify that sensitive data and APIs are protected against Insecure Direct Object Reference (IDOR) attacks targeting creation, reading, updating, and deletion of records, such as creating or updating someone else's record, viewing everyone's records, or deleting all records. | L1 | Yes | Dynamic Test: Authenticate as User A, attempt CRUD operations on User B's resources by changing IDs. |
| V4.2.2 | Verify that the application or framework enforces a strong anti-CSRF mechanism to protect authenticated functionality, and effective anti-automation or anti-CSRF protects unauthenticated functionality. | L1 | Yes | Dynamic Test: For cookie-auth APIs, attempt state-changing request without CSRF token. Must fail. Code Review: Check SameSite attribute and/or CSRF token implementation. |

---

## V4.3 — Other Access Control Considerations

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V4.3.1 | Verify administrative interfaces use appropriate multi-factor authentication to prevent unauthorized use. | L1 | Yes | Dynamic Test: Attempt admin access without MFA. Code Review: Check admin route auth requirements. |
| V4.3.2 | Verify that directory browsing is disabled unless deliberately desired. Additionally, applications should not allow discovery or disclosure of file or directory metadata, such as Thumbs.db, .DS_Store, .git or .svn folders. | L1 | Yes | Dynamic Test: Attempt to browse directories and access metadata files (.git, .env, etc.). |
| V4.3.3 | Verify the application has additional authorization (such as step up or adaptive authentication) for lower value systems, and/or segregation of duties for high value applications to enforce anti-fraud controls as per the risk of application and past fraud. | L2 | Yes | Code Review: Check for step-up authentication on high-value operations (payment, role change). |
