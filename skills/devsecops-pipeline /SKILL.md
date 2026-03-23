---
name: devsecops-pipeline
description: DevSecOps pipeline for secure-by-design development. NIST SSDF backbone + OWASP ASVS Level 2 verification. Covers threat modeling, secure design, ASVS audits, and PR review. Triggers on devsecops, security pipeline, secure development, NIST SSDF, ASVS, feature brief, security review, secure-by-design, SDL, SDLC security.
---

# DevSecOps Pipeline

> Secure-by-design development framework — NIST SSDF + OWASP ASVS Level 2

## Overview

## Overview

This skill provides the foundational knowledge for the Antigravity DevSecOps pipeline — a 5-phase secure development lifecycle for JavaScript/Node.js and Python projects.

**Frameworks:**
- **NIST SSDF** (Secure Software Development Framework) — structural backbone
- **OWASP ASVS v4.0.3** (Level 2) — verification standard for sensitive-data applications
- **STRIDE** — threat classification model

**Target stacks:** JavaScript / Node.js, Python

## Pipeline Architecture

```
Feature Brief → Phase 1: Threat Modeling → ⏸ Human Gate
             → Phase 2: Secure Design   → ⏸ Human Gate
             → Phase 3: ASVS Audit      → ⏸ Human Gate
             → Phase 4: PR Sentinel
             → Phase 5: Evaluator-Optimizer (Quality Critique)
```

| Phase | NIST SSDF Mapping | Skills Used | Output |
|-------|-------------------|-------------|--------|
| **Phase 1** — Threat Modeling | PW.1 (Design Software to Meet Security Requirements) | `threat-modeling` | `[feature]-threat-report.md` |
| **Phase 2** — Secure Design | PS.1 (Protect All Forms of Code) | `secure-design` | `[feature]-secure-design.md` + `security-requirements.md` |
| **Phase 3** — ASVS Verification | RV.1 (Identify and Confirm Vulnerabilities) | `asvs-audit` | `[feature]-audit-workflow.md` + test scripts |
| **Phase 4** — PR Sentinel | PW.7 (Review Human-Readable Code) | `pr-sentinel` | Inline PR comments |
| **Phase 5** — Evaluator-Optimizer | PW.8 (Validate Software Interfaces) | `evaluator-optimizer` | `evaluation-report.md` + Refined Artifacts |

## Knowledge Base

The `references/` directory contains 7 knowledge base files that the agent should load contextually:

| File | Always Load | When to Load |
|------|-------------|--------------|
| `kb-secure-coding-fundamentals.md` | ✅ | Every pipeline run |
| `kb-secrets-management.md` | ✅ | Every pipeline run |
| `kb-vulnerability-management.md` | ✅ | Every pipeline run |
| `kb-nodejs-security.md` | | When stack includes Node.js |
| `kb-python-security.md` | | When stack includes Python |
| `kb-api-security.md` | | When feature exposes API endpoints |
| `kb-zero-trust.md` | | Reference only — NOT a pipeline phase |
| `kb-docker-security.md` | | When feature involves Docker/containers |

## Feature Brief Template

Before triggering the pipeline, the developer must complete a Feature Brief covering:

1. **Feature Identity** — name, owner, target branch
2. **Feature Description** — user-facing behavior, business purpose
3. **Data Classification** — PII, credentials, financial, health, internal, public
4. **User Roles & Access** — roles, permissions, auth methods
5. **Technology Stack** — backend, frontend, database, ORM, infrastructure
6. **External Integrations** — third-party APIs, direction, auth method
7. **Existing Security Controls** — auth, authz, validation, rate limiting, logging
8. **New Dependencies** — package name, version, purpose, source
9. **CI/CD Impact** — pipeline modifications, Dockerfile changes, env vars
10. **Known Risks & Assumptions** — pre-identified concerns

**Validation:** If Data Classification, User Roles, or Tech Stack are missing → STOP and request completion.

## Scope Decisions

These decisions are locked — do not reverse without explicit human confirmation:

- **SAMM excluded** — too organisational for a per-feature pipeline
- **Triggers are manual** — human approval gates after each main phase
- **One output file per phase** — knowledge base is incremental
- **"Vulnerability management"** is the correct framing (not "incident response")
- **Zero Trust Architecture** is a KB reference only, not a pipeline phase

## How to Invoke

Use the `/secure` workflow command to start the full pipeline, or invoke individual skills:

```
```
/secure                          → Full 4-phase pipeline
Use threat-modeling skill        → Phase 1 only
Use secure-design skill          → Phase 2 only
Use asvs-audit skill             → Phase 3 only
Use pr-sentinel skill            → Phase 4 only
/evaluate                        → Phase 5 only (Critique & Refine)
```


## 📑 Content Map

| File | Description |
|------|-------------|
| `SKILL.md` | Main Skill Definition |
| `references/kb-nodejs-security.md` | Specialized references for kb-nodejs-security |
| `references/kb-secure-coding-fundamentals.md` | Specialized references for kb-secure-coding-fundamentals |
| `references/kb-secrets-management.md` | Specialized references for kb-secrets-management |
| `references/kb-api-security.md` | Specialized references for kb-api-security |
| `references/kb-python-security.md` | Specialized references for kb-python-security |
| `references/kb-vulnerability-management.md` | Specialized references for kb-vulnerability-management |
| `references/kb-docker-security.md` | Specialized references for kb-docker-security |
