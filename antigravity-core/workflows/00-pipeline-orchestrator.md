---
description: "DevSecOps Pipeline Orchestrator — Master Workflow"
frameworks: NIST SSDF, OWASP ASVS v4.0.3 Level 2, STRIDE
stack: JavaScript/Node.js, Python
trigger: manual
---

# DevSecOps Pipeline Orchestrator

**Purpose:** This is the master orchestrator for the Antigravity DevSecOps pipeline. It sequences four phases of security work — from threat modeling to final PR review — with human approval gates between each phase. It does NOT execute audits directly. It routes to modular sub-workflows based on the feature being developed.

**Frameworks:**
- **NIST SSDF (Secure Software Development Framework):** Structural backbone. Each phase maps to a core SSDF practice.
- **OWASP ASVS v4.0.3 (Level 2):** Verification standard for applications handling sensitive data.
- **STRIDE:** Threat classification model used in Phase 1.

---

## Prerequisites

Before triggering this pipeline, the following must exist in the project:

1. **Knowledge Base** (`knowledge-base/`): Core secure coding reference files. The agent must have access to these at all times. These are NOT generated per-feature — they are maintained incrementally.
2. **ASVS Reference Files** (`asvs-reference/`): One file per ASVS chapter (V1–V14), containing the full Level 2 requirement text. The agent must NEVER search the web for ASVS requirements.
3. **A Completed Feature Brief** (`00-feature-brief-template.md`): The developer must fill this in before the pipeline starts.

---

## Pipeline Sequence

```
┌─────────────────────────────────────────────────┐
│                  INPUT                          │
│          Feature Brief Template                 │
│     (filled by developer before start)          │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              PHASE 1: Threat Modeling            │
│         NIST SSDF: PW (Produce Well-Secured)    │
│                                                  │
│  Sub-workflows:                                  │
│    01a — Attack Surface Mapping                  │
│    01b — Data Flow Diagram (Mermaid)             │
│    01c — STRIDE Analysis                         │
│                                                  │
│  Output: [feature]-threat-report.md              │
└──────────────────────┬──────────────────────────┘
                       │
                  ⏸ HUMAN GATE
              Review & Approve
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           PHASE 2: Secure Design                 │
│         NIST SSDF: PS (Protect the Software)    │
│                                                  │
│  Sub-workflows:                                  │
│    02a — Secure Architecture Patterns            │
│    02b — Security Requirements Generation        │
│    02c — Dependency Evaluation                   │
│                                                  │
│  Output: [feature]-secure-design.md              │
│          [feature]-security-requirements.md      │
└──────────────────────┬──────────────────────────┘
                       │
                  ⏸ HUMAN GATE
              Review & Approve
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│        PHASE 3: ASVS Verification & Testing      │
│         NIST SSDF: RV (Respond to Vulns)        │
│                                                  │
│  Orchestrator selects relevant sub-workflows:    │
│    03a — Auth & Session (V2, V3)                 │
│    03b — Access Control (V4)                     │
│    03c — Validation & Encoding (V5)              │
│    03d — Crypto & Communications (V6, V9)        │
│    03e — Error Handling & Logging (V7, V8)       │
│    03f — API & GraphQL (V13)                     │
│    03g — Secrets & Dependencies                  │
│    03h — Configuration (V14)                     │
│    03i — CI/CD Pipeline Security                 │
│                                                  │
│  Output: [feature]-audit-workflow.md             │
│          [feature]-security-tests.py             │
│          [feature]-security-tests.js             │
└──────────────────────┬──────────────────────────┘
                       │
                  ⏸ HUMAN GATE
              Review & Approve
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│          PHASE 4: PR Sentinel                    │
│    Lightweight final check before merge          │
│                                                  │
│  Sub-workflow:                                   │
│    04a — PR Diff Review (Micro-SAST)             │
│                                                  │
│  Output: PR comments (inline)                    │
└──────────────────────┬──────────────────────────┘
                       │
                  ⏸ HUMAN GATE
              Review & Approve
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│          PHASE 5: Evaluator-Optimizer           │
│    Automated Quality Control (Generate->Refine) │
│                                                 │
│  Sub-workflow:                                  │
│    05-evaluator-optimizer.md                    │
│                                                 │
│  Output: Refined code + Evaluation Report       │
└─────────────────────────────────────────────────┘
```

---

## Step 1: Intake — Read the Feature Brief

**Action:** Read the completed `00-feature-brief-template.md` provided by the developer.

**Extract the following:**
1. **Feature Name & Description** — what is being built.
2. **Data Classification** — what type of data does this feature handle (PII, financial, public, internal).
3. **User Roles** — who interacts with this feature and at what privilege level.
4. **Technology Stack** — Node.js, Python, or both. Specific frameworks (Express, FastAPI, etc.).
5. **External Integrations** — third-party APIs, databases, message queues, file storage.
6. **Existing Security Controls** — what authentication/authorization is already in place.

**Validation:** If any critical field is missing (Data Classification, User Roles, or Tech Stack), STOP and request the developer to complete the brief before proceeding.

---

## Step 2: Load Knowledge Base

**Action:** Load the relevant knowledge base files from `knowledge-base/` into context.

**Always load:**
- `kb-secure-coding-fundamentals.md` — universal principles.
- `kb-secrets-management.md` — applies to every feature.
- `kb-vulnerability-management.md` — classification and remediation SLAs.

**Conditionally load based on tech stack:**
- If Node.js → load `kb-nodejs-security.md`
- If Python → load `kb-python-security.md`

**Conditionally load based on feature type:**
- If the feature exposes API endpoints → load `kb-api-security.md`

---

## Step 3: Execute Phase 1 — Threat Modeling

**Action:** Execute the Phase 1 sub-workflows in sequence.

**NIST SSDF Mapping:** PW.1 (Design Software to Meet Security Requirements)

**Sub-workflow execution order:**
1. `phase1-threat-modeling/01a-attack-surface-mapping.md` — Identify all entry points, trust boundaries, and external entities.
2. `phase1-threat-modeling/01b-data-flow-diagram.md` — Generate a Mermaid.js DFD visualizing the feature's architecture.
3. `phase1-threat-modeling/01c-stride-analysis.md` — Apply STRIDE to each component identified in steps 1a and 1b.

**ASVS Reference Required:** Load `asvs-reference/asvs-v1-architecture.md` (V1 — Architecture, Design and Threat Modeling) as the verification standard for this phase.

**Output:** Generate `outputs/[feature-name]/threat-report.md` containing:
- Executive summary of the feature's risk profile.
- Attack surface map.
- Data Flow Diagram (Mermaid.js).
- STRIDE threat matrix with risk ratings (Critical / High / Medium / Low).

**⏸ HUMAN GATE:** Present the threat report to the developer/architect for review. Do NOT proceed to Phase 2 until the human explicitly approves or requests changes.

---

## Step 4: Execute Phase 2 — Secure Design

**Action:** Using the approved threat report from Phase 1, generate secure design guidelines.

**NIST SSDF Mapping:** PS.1 (Protect All Forms of Code from Unauthorized Access and Tampering)

**Sub-workflow execution order:**
1. `phase2-secure-design/02a-secure-architecture-patterns.md` — Recommend architecture decisions and security controls that directly mitigate the threats identified in Phase 1.
2. `phase2-secure-design/02b-security-requirements-generation.md` — Derive a concrete checklist of security requirements from the threat model, mapped to specific ASVS requirements.
3. `phase2-secure-design/02c-dependency-evaluation.md` — If new third-party libraries are being introduced, evaluate them before adoption.

**Output:** Generate two files in `outputs/[feature-name]/`:
- `secure-design.md` — Architecture patterns, library choices, security controls.
- `security-requirements.md` — Checklist of requirements with ASVS traceability.

**⏸ HUMAN GATE:** Present the secure design to the developer/architect for review. Do NOT proceed to Phase 3 until the human explicitly approves.

---

## Step 5: Execute Phase 3 — ASVS Verification & Testing

**Action:** Based on the feature type and the ASVS chapters identified in Phase 2, select and execute the relevant audit sub-workflows.

**NIST SSDF Mapping:** RV.1 (Identify and Confirm Vulnerabilities on an Ongoing Basis)

**Sub-workflow selection logic:**

| Feature Characteristic | Sub-workflows to Execute |
|---|---|
| Has login / registration / password flows | `03a-auth-session-audit.md` (V2, V3) |
| Has role-based or resource-based access | `03b-access-control-audit.md` (V4) |
| Accepts user input (forms, APIs, file uploads) | `03c-validation-encoding-audit.md` (V5) |
| Stores/transmits sensitive data, uses encryption | `03d-crypto-communications-audit.md` (V6, V9) |
| Has error handling, logging, or audit trails | `03e-error-logging-audit.md` (V7, V8) |
| Exposes REST or GraphQL endpoints | `03f-api-graphql-audit.md` (V13) |
| Adds new third-party dependencies | `03g-secrets-dependencies-audit.md` |
| Modifies server/container/deployment config | `03h-configuration-audit.md` (V14) |
| Modifies CI/CD pipelines or GitHub Actions | `03i-cicd-pipeline-audit.md` |

**ASVS Reference Required:** For each selected sub-workflow, load the corresponding ASVS reference files from `asvs-reference/`. The agent must have the full requirement text available — no web search.

**Assessment Matrix:** Every ASVS requirement checked must receive one of:
- `[PASS]` — The code securely implements the requirement.
- `[FAIL]` — The code fails the requirement. Must include file path, code snippet, and remediation.
- `[N/A]` — The requirement does not apply. Must include brief justification.

**Output:** Generate in `outputs/[feature-name]/`:
- `audit-workflow.md` — The full assessment matrix with findings.
- `security-tests.py` — Python test scripts for dynamic verification.
- `security-tests.js` — JavaScript test scripts for dynamic verification.

**⏸ HUMAN GATE:** Present the audit results and test scripts to the developer/security engineer for review. Do NOT proceed to Phase 4 until approved.

---

## Step 6: Execute Phase 4 — PR Sentinel

**Action:** When the feature code is ready for merge (PR opened), execute the lightweight final review.

**Sub-workflow:**
- `phase4-pr-sentinel/04a-pr-diff-review.md` — Analyze ONLY the changed lines of code (diff). Catch regressions, hardcoded secrets, missing middleware, and input sanitization gaps introduced in the final implementation.

**Output:** Inline PR comments — concise, actionable, with code suggestions.

**⏸ HUMAN GATE:** Present the PR comments to the developer for review. Do NOT proceed to Phase 5 unless requested or if the feature is highly complex.

---

## Step 7: Execute Phase 5 — Evaluator-Optimizer

**Action:** If the feature is complex or explicitly requested by the Human Gate, run the automated critique loop.

**NIST SSDF Mapping:** PW.8 (Validate and Verify Software Interfaces)

**Sub-workflow:**
- `05-evaluator-optimizer.md` — Apply Generate → Critique → Refine loop to the final artifacts based on specific thresholds.

**Output:** Generate in `outputs/[feature-name]/`:
- `evaluation-report.md` — Standardized critique report with scores.
- Code diffs reflecting the refined artifacts.

## Post-Pipeline: Knowledge Base Update

**Action:** After the pipeline completes for a feature, evaluate if any new patterns, anti-patterns, or library recommendations were discovered during the audit.

**If yes:** Update the relevant knowledge base file in `knowledge-base/` so future pipeline runs benefit from the lessons learned.

This ensures the knowledge base grows incrementally with every feature the team builds.
