---
description: "ASVS V3 — Session Management Verification Requirements"
asvs_version: "4.0.3"
chapter: "V3"
applicable_phases: "Phase 3 (03a-auth-session-audit)"
---

# ASVS V3: Session Management Verification Requirements

**Scope:** This chapter covers the secure generation, management, and invalidation of session tokens, whether cookie-based or token-based (JWT, OAuth).

---

## V3.1 — Fundamental Session Management Security

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V3.1.1 | Verify the application never reveals session tokens in URL parameters or error messages. | L1 | Yes | Dynamic Test: Check URLs, redirects, and error responses for session token leakage. |

---

## V3.2 — Session Binding

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V3.2.1 | Verify the application generates a new session token on user authentication. | L1 | Yes | Dynamic Test: Check that session ID changes after successful login (session fixation prevention). |
| V3.2.2 | Verify that session tokens possess at least 64 bits of entropy. | L1 | Yes | Code Review: Check session token generation — must use CSPRNG with ≥ 64 bits. |
| V3.2.3 | Verify the application only stores session tokens in the browser using secure methods such as appropriately secured cookies (see section 3.4) or HTML 5 session storage. | L1 | Yes | Dynamic Test: Check where session tokens are stored. Must not be in localStorage (prefer HttpOnly cookie). |

---

## V3.3 — Session Termination

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V3.3.1 | Verify that logout and expiration invalidate the session token, such that the back button or a downstream relying party does not resume an authenticated session, including across relying parties. | L1 | Yes | Dynamic Test: Logout, then replay the old session token. Must be rejected. |
| V3.3.2 | Verify that if authenticators permit users to remain logged in, both re-authentication occurs periodically whether active or after an idle period. | L1 | Yes | Config Review: Check for session idle timeout and absolute timeout configuration. |
| V3.3.3 | Verify that the application gives the option to terminate all other active sessions after a successful password change (including change via password reset/recovery), and that this is effective across the application, federated login (if present), and any relying parties. | L1 | Yes | Dynamic Test: Change password, verify other sessions are invalidated or user is prompted. |
| V3.3.4 | Verify that users are able to view and (having re-entered login credentials) log out of any or all currently active sessions and devices. | L2 | Yes | Feature Review: Check for session management UI showing active sessions with logout capability. |

---

## V3.4 — Cookie-based Session Management

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V3.4.1 | Verify that cookie-based session tokens have the 'Secure' attribute set. | L1 | Yes | Dynamic Test: Inspect Set-Cookie header for `Secure` flag. |
| V3.4.2 | Verify that cookie-based session tokens have the 'HttpOnly' attribute set. | L1 | Yes | Dynamic Test: Inspect Set-Cookie header for `HttpOnly` flag. |
| V3.4.3 | Verify that cookie-based session tokens utilize the 'SameSite' attribute to limit exposure to cross-site request forgery attacks. | L1 | Yes | Dynamic Test: Inspect Set-Cookie header for `SameSite=Strict` or `SameSite=Lax`. |
| V3.4.4 | Verify that cookie-based session tokens use the "__Host-" prefix so cookies are only sent to the host that initially set the cookie. | L1 | Yes | Dynamic Test: Check cookie name prefix. |
| V3.4.5 | Verify that if the application is published under a domain name with other applications that set or use session cookies that might override or disclose the session cookies, set the path attribute in cookie-based session tokens using the most precise path possible. | L1 | Yes | Dynamic Test: Check cookie path attribute is restrictive. |

---

## V3.5 — Token-based Session Management

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V3.5.1 | Verify the application allows users to revoke OAuth tokens that form trust relationships with linked applications. | L2 | Yes | Feature Review: Check for OAuth token revocation UI/endpoint. |
| V3.5.2 | Verify the application uses session tokens rather than static API secrets and keys, except with legacy implementations. | L1 | Yes | Code Review: Check that APIs use dynamic session/access tokens, not static keys for user auth. |
| V3.5.3 | Verify that stateless session tokens use digital signatures, encryption, and other countermeasures to protect against tampering, enveloping, replay, null cipher, and key substitution attacks. | L1 | Yes | Code Review: Check JWT implementation — algorithm validation, signature verification, expiration checking. |

---

## V3.7 — Defenses Against Session Management Exploits

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V3.7.1 | Verify the application ensures a full, valid login session or requires re-authentication or secondary verification before allowing any sensitive transactions or account modifications. | L1 | Yes | Dynamic Test: Attempt sensitive operations (password change, email change, payment) — verify re-auth is required. |
