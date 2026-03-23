# Example: Feature Brief Input

> This is a real filled-in example of the input used to trigger `/00-pipeline-orchestrator`.
> Use `/00-feature-brief-template` to generate your own, or copy this and adapt it.

---

```markdown
# Feature Brief — User Authentication Service

**Date:** 2025-03-23  
**Submitted by:** Paulo  
**Target Pipeline:** /00-pipeline-orchestrator (Full 4-Phase DevSecOps)

---

## 1. Feature Description
Build a stateless JWT-based authentication service for a B2C SaaS application.
Users authenticate via email/password. OAuth2 via Google is a future milestone, not in scope.

## 2. Technical Context
- Stack: Node.js (Express), PostgreSQL, Redis (session cache)
- Existing system: Monolith with legacy session cookies — migration path required
- Deployment: Docker containers on AWS ECS, behind an ALB

## 3. User Types & Roles
- End customers (B2C) — email/password login
- Admins — same flow, different RBAC claims in JWT payload

## 4. Compliance & Regulations
- GDPR applies (EU users — data residency in eu-west-1)
- No HIPAA, no PCI-DSS

## 5. Non-Functional Requirements
- Token expiry: 15m access token, 7d refresh token (sliding window)
- MFA: Optional TOTP (phase 2, out of scope for this brief)
- Rate limiting: Max 5 failed login attempts per IP per 15 minutes

## 6. Known Constraints
- Must integrate with existing Postgres `users` table (no schema changes to `id`, `email`, `password_hash`)
- Redis already deployed — can be used for refresh token revocation list
- `jsonwebtoken` v9 is mandated by the platform team

## 7. Open Questions for Socratic Gate
1. httpOnly cookie vs Authorization header for token delivery?
2. Should refresh token rotation be strict (1-use) or sliding?
3. What happens to existing legacy sessions on migration day?
```
