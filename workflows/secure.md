---
description: DevSecOps Pipeline — Full 4-phase secure development lifecycle
---

# /secure — DevSecOps Pipeline

Run the full secure-by-design pipeline for a new feature. Requires a completed Feature Brief.

## Workflow

```
1. INTAKE
   └── Read Feature Brief, validate required fields, load knowledge base

2. PHASE 1: THREAT MODELING (skill: threat-modeling)
   ├── 1a. Attack Surface Mapping
   ├── 1b. Data Flow Diagram (Mermaid.js)
   └── 1c. STRIDE Threat Analysis
   Output: [feature]-threat-report.md
   ⏸ HUMAN GATE — Review & Approve

3. PHASE 2: SECURE DESIGN (skill: secure-design)
   ├── 2a. Secure Architecture Patterns
   ├── 2b. Security Requirements Generation
   └── 2c. Dependency Evaluation (if new deps)
   Output: [feature]-secure-design.md, [feature]-security-requirements.md
   ⏸ HUMAN GATE — Review & Approve

4. PHASE 3: ASVS VERIFICATION (skill: asvs-audit)
   ├── Select applicable sub-audits (03a–03i)
   ├── Execute against code
   └── Generate test scripts
   Output: [feature]-audit-workflow.md, security-tests.py, security-tests.js
   ⏸ HUMAN GATE — Review & Approve

5. PHASE 4: PR SENTINEL (skill: pr-sentinel)
   └── Micro-SAST on PR diff
   Output: Inline PR comments
```

## Intake Procedure

1. Read the completed Feature Brief
2. Extract: Feature Name, Data Classification, User Roles, Tech Stack, External Integrations, Existing Controls
3. **Validate:** If Data Classification, User Roles, or Tech Stack are missing → STOP and request completion

### Knowledge Base Loading

**Always load from `devsecops-pipeline` skill references:**
- `kb-secure-coding-fundamentals.md`
- `kb-secrets-management.md`
- `kb-vulnerability-management.md`

**Conditionally load:**
- If Node.js → `kb-nodejs-security.md`
- If Python → `kb-python-security.md`
- If API endpoints → `kb-api-security.md`
- If Docker/containers → `kb-docker-security.md`

## Phase Execution Rules

- Execute phases sequentially — never skip a phase
- Each phase MUST complete before presenting the Human Gate
- At each Human Gate, present outputs and WAIT for explicit approval
- If the human requests changes, iterate on the current phase before proceeding
- The agent must NEVER search the web for ASVS requirements — all reference data is in the `asvs-audit` skill references

## Post-Pipeline

After completion, evaluate if new patterns, anti-patterns, or library recommendations were discovered. If yes, update the relevant KB file in `devsecops-pipeline/references/` so future runs benefit.
