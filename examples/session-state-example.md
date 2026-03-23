# Example: session-state.md

> This is a real filled-in example of what `session-state.md` looks like after completing Phase 1 of the DevSecOps pipeline for a hypothetical "User Auth Service" feature.
> Copy this to `.agent/session-state.md` and adapt to your project.

---

```markdown
# Session State — User Auth Service

**Last Updated:** 2025-03-23T14:05:00Z  
**Active Agent:** @security-auditor  
**Model Tier:** Sonnet  

---

## Current Phase
Phase 2 — Secure Design (in progress)

## Completed
- [x] Phase 1: Threat Modeling (STRIDE)
  - Output: `.agent/outputs/threat-model-report.md`
  - Key threats identified: Session fixation, JWT secret brute-force, OAuth redirect URI manipulation
  - Trust boundaries mapped: Client ↔ API Gateway, API Gateway ↔ Auth Service, Auth Service ↔ DB

## Next Steps
- [ ] Phase 2a: Select secure architecture pattern for stateless JWT + refresh token rotation
- [ ] Phase 2b: Generate ASVS-traceable security requirements
- [ ] Phase 2c: Evaluate `jsonwebtoken` and `passport.js` dependencies (SCA)

## Blockers
None currently.

## Open Decisions
1. Token storage: httpOnly cookie vs Authorization header — awaiting Product Owner input
2. Refresh token rotation: sliding window vs absolute expiry

## Socratic Gate Answers (recorded)
1. User types: End customers (B2C), no service accounts
2. Compliance: GDPR applies (EU users), no HIPAA
3. Migration: Existing sessions via legacy cookie — need migration path
```
