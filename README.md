# Antigravity DevSecOps System

> **Base framework:** [vudovn/antigravity-kit](https://github.com/vudovn/antigravity-kit)  
> **This edition** extends the original with a full 4-Phase DevSecOps Pipeline, intelligent model-tier routing, 20 specialized agents, 40+ deep skill modules, and structured evaluator-optimizer feedback loops — all built as a persistent context system for Google Gemini / Claude-based agentic workflows.

---

## How It Works — The Orchestration Flow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  GEMINI.md  —  The Persistent System Brain              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Intelligent Routing Protocol                    │   │
│  │  1. Classify request (security / code / design)  │   │
│  │  2. Assign model tier (Opus / Sonnet / Flash)    │   │
│  │  3. Enforce DevSecOps gate if needed             │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
         │                    │                  │
         ▼                    ▼                  ▼
   /workflows/         /agents/             /skills/
  (procedures)        (personas)          (knowledge)
         │                    │                  │
         └────────────────────┴──────────────────┘
                              │
                              ▼
                    Output / Deliverable
          (threat-model.md / code / ASVS audit / PR review)
```

---

## Model Routing Table

Before executing any task, the system silently classifies the request and picks the cheapest model that can handle it:

| Request Type | Keywords | Model | Cost Tier |
|:---|:---|:---|:---|
| Threat Modeling / STRIDE | `"threat model"`, `"STRIDE"`, `"design"` | Opus | 🔴 8x |
| ASVS Audit / PR Review | `"audit"`, `"ASVS"`, `"PR review"` | Sonnet | 🟡 1x |
| Evaluate / Critique | `"evaluate"`, `"critique"`, `"refine"` | Sonnet | 🟡 1x |
| Analysis / Survey | `"analyze"`, `"list"`, `"overview"` | Flash | 🟢 0.1x |
| Complex Build / Refactor | `"build"`, `"create"`, `"refactor"` | Sonnet + Agent | 🟡 1x |

---

## The 4-Phase DevSecOps Pipeline

Every new feature or architectural change that enters the system is required to pass through four mandatory security gates. Each phase produces a documented artifact.

```
                        Feature Brief
                             │
            ┌────────────────▼───────────────────┐
            │  PHASE 1 — Threat Modeling (STRIDE) │
            │  Agent: Opus                         │
            │  Workflow: /01a → /01b → /01c        │
            │  Attacks surface map + DFD + STRIDE  │
            │  Output: threat-model-report.md      │
            └────────────────┬───────────────────┘
                             │
            ┌────────────────▼───────────────────┐
            │  PHASE 2 — Secure Design            │
            │  Agent: Opus                         │
            │  Workflow: /02a → /02b → /02c        │
            │  Architecture patterns + Requirements│
            │  + Dependency evaluation (SCA)       │
            │  Output: design-decisions.md         │
            └────────────────┬───────────────────┘
                             │
            ┌────────────────▼───────────────────┐
            │  PHASE 3 — ASVS Level 2 Audit       │
            │  Agent: Sonnet                       │
            │  Workflow: /03-asvs-audit-orchestr.  │
            │  9 audit domains (see below)         │
            │  Output: asvs-[chapter]-roadmap.md   │
            └────────────────┬───────────────────┘
                             │
            ┌────────────────▼───────────────────┐
            │  PHASE 4 — PR Sentinel (Micro-SAST) │
            │  Agent: Sonnet                       │
            │  Workflow: /04a-pr-diff-review       │
            │  Analyzes ONLY the changed lines     │
            │  Checks: injection / missing auth /  │
            │  error leaks / hardcoded secrets     │
            │  Output: inline PR comments          │
            └─────────────────────────────────────┘
```

### ASVS Phase 3 — 9 Audit Domains

| # | Workflow | Domain |
|---|----------|--------|
| 3a | `/03a-auth-session-audit` | Authentication & Session Management |
| 3b | `/03b-access-control-audit` | Access Control |
| 3c | `/03c-validation-encoding-audit` | Input Validation, Sanitization & Encoding |
| 3d | `/03d-crypto-communications-audit` | Cryptography & Communications Security |
| 3e | `/03e-error-logging-audit` | Error Handling & Logging |
| 3f | `/03f-api-graphql-audit` | API & Web Services |
| 3g | `/03g-secrets-dependencies-audit` | Secrets & Software Composition Analysis |
| 3h | `/03h-configuration-audit` | Configuration Security |
| 3i | `/03i-cicd-pipeline-audit` | CI/CD Pipeline Security |

---

## The Evaluator-Optimizer Loop

For any output with `complexity >= MODERATE`, the system automatically triggers a self-critique cycle before passing the result back:

```
  Generate Answer
       │
       ▼
  Critique Output  ◄──────────────┐
  (Does it meet standards?)       │
       │                          │
  ─────┴─────                     │
 │           │                    │
 ▼           ▼                    │
Pass      Refine ─────────────────┘
 │
 ▼
Final Deliverable
```

This loop is also available as a standalone workflow: `/05-evaluator-optimizer`.

---

## Agents (20 Specialists)

Each agent has a bounded identity and a narrow scope of authority. They are called by the Orchestrator and Workflows — never directly by the user.

| Agent | Primary Responsibility |
|-------|----------------------|
| `@orchestrator` | Top-level coordinator. Routes sub-tasks to the right agents |
| `@security-auditor` | ASVS compliance, OWASP review, vuln assessment |
| `@frontend-specialist` | UI/UX, React, Next.js, animations, accessibility |
| `@backend-specialist` | APIs, microservices, auth flows, DB queries |
| `@mobile-developer` | React Native, Flutter, iOS/Android conventions |
| `@database-architect` | Schema design, indexing, ORM selection, migrations |
| `@devops-engineer` | CI/CD pipelines, Docker, deployment strategy |
| `@penetration-tester` | Red team tactics, MITRE ATT&CK, exploit chains |
| `@performance-optimizer` | Profiling, bottleneck analysis, bundle size |
| `@project-planner` | Task breakdown, dependencies, estimation |
| `@product-manager` | Requirements analysis, feature scoping |
| `@product-owner` | Backlog, acceptance criteria, user stories |
| `@qa-automation-engineer` | Test coverage, E2E, automation strategy |
| `@test-engineer` | Unit/integration tests, mocking, TDD cycles |
| `@documentation-writer` | README, API docs, ADR documentation |
| `@debugger` | Systematic root cause analysis, 4-phase debug |
| `@code-archaeologist` | Legacy code understanding and reasoning |
| `@game-developer` | Game loops, physics integration, platform targets |
| `@seo-specialist` | E-E-A-T, Core Web Vitals, GEO optimization |
| `@explorer-agent` | Lightweight analysis for survey/intel tasks |

---

## Workflows Reference (33 Workflows)

### DevSecOps Pipeline Workflows

| Workflow | Purpose |
|----------|---------|
| `/00-feature-brief-template` | Structured input to initiate the pipeline |
| `/00-pipeline-orchestrator` | Master orchestrator for the full 4-phase run |
| `/01a-attack-surface-mapping` | Enumerate all trust boundaries and entry points |
| `/01b-data-flow-diagram` | Generate Mermaid.js DFDs for threat analysis |
| `/01c-stride-analysis` | Full STRIDE per-threat classification |
| `/02a-secure-architecture-patterns` | Match architectural patterns to threat posture |
| `/02b-security-requirements-generation` | Produce ASVS-traceable, testable requirements |
| `/02c-dependency-evaluation` | SCA — assess 3rd party supply chain risk |
| `/03-asvs-audit-orchestrator` | Coordinate all 9 ASVS audit domains |
| `/03a` → `/03i` | Individual ASVS chapter audits (see table above) |
| `/04a-pr-diff-review` | Gate: micro SAST on PR diffs only |
| `/05-evaluator-optimizer` | Recursive critique + refinement loop |

### Development Workflows

| Workflow | Purpose |
|----------|---------|
| `/create` | Scaffold new application (interactive, calls `app-builder` skill) |
| `/enhance` | Add/update features in existing app |
| `/plan` | Generate structured implementation plan (no code) |
| `/brainstorm` | Structured ideation with multi-option exploration |
| `/orchestrate` | Spawn parallel agents for multi-perspective analysis |
| `/debug` | Activate systematic debug mode |
| `/test` | Generate and run test suites |
| `/deploy` | Pre-flight checks + deployment execution |
| `/preview` | Start / stop / check local dev server |
| `/secure` | Trigger the full 4-phase DevSecOps pipeline |
| `/status` | Status board — agent states and roadmap progress |
| `/ui-ux-pro-max` | Full UI/UX planning and implementation |

---

## Skills — Knowledge Base (40+ Modules)

Each skill has a `SKILL.md` router (the entry point) and a `references/` directory with deep-dive documents.

### Architecture & Design
| Skill | What it teaches |
|-------|----------------|
| `architecture` | ADR methodology, trade-off evaluation, system design patterns |
| `api-patterns` | REST vs GraphQL vs tRPC selection, pagination, auth, rate limiting |
| `database-design` | Schema design, indexing strategy, ORM/serverless DB selection |
| `frontend-design` | Color systems, typography, UX psychology, animation principles |
| `mobile-design` | iOS/Android conventions, touch psychology, mobile performance |

### Security
| Skill | What it teaches |
|-------|----------------|
| `devsecops-pipeline` | NIST SSDF backbone, OWASP ASVS Level 2 full framework |
| `asvs-audit` | Step-by-step ASVS verification, all 9 chapters |
| `threat-modeling` | STRIDE per-element, attack surface mapping, DFD generation |
| `secure-design` | Secure architecture selection, ASVS-traceable requirements |
| `pr-sentinel` | Micro-SAST patterns: injection, missing auth, secret leaks |
| `vulnerability-scanner` | OWASP 2025 Top 10, CVSS scoring, supply chain risk |
| `red-team-tactics` | MITRE ATT&CK phases, detection evasion, reporting |

### Engineering
| Skill | What it teaches |
|-------|----------------|
| `app-builder` | Full-stack orchestration, tech stack selection, scaffolding |
| `nextjs-react-expert` | Eliminating waterfalls, bundle optimization, RSC, re-render perf |
| `nodejs-best-practices` | Framework selection, async patterns, security hardening |
| `python-patterns` | FastAPI/Django selection, type hints, project structure |
| `rust-pro` | Tokio async, axum, ownership/borrowing, systems programming |
| `tailwind-patterns` | Tailwind v4 CSS-first config, container queries |
| `tdd-workflow` | RED-GREEN-REFACTOR, test pyramid, mutation testing |
| `testing-patterns` | Unit/integration/e2e strategy, mocking, coverage targets |
| `systematic-debugging` | 4-phase root cause analysis with evidence-based verification |
| `performance-profiling` | Measurement-first, bottleneck analysis, flame graphs |
| `clean-code` | Pragmatic standards: no over-engineering, no unnecessary comments |
| `bash-linux` | Critical shell patterns, piping, error handling, scripting |

### Orchestration
| Skill | What it teaches |
|-------|----------------|
| `intelligent-routing` | Agent selection logic, domain detection, quota preservation |
| `parallel-agents` | Multi-agent fan-out patterns for comprehensive analysis |
| `behavioral-modes` | BRAINSTORM / IMPLEMENT / DEBUG / REVIEW / SHIP mode switching |
| `evaluator-optimizer` | Generate → Critique → Refine loop execution |
| `brainstorming` | Socratic questioning protocol, multi-option exploration |
| `plan-writing` | Structured task breakdown with dependencies and checklists |

---

## Knowledge Base (KB) — Security Reference Library

Located in `skills/devsecops-pipeline/references/`, these KB files are the curated security references that agents consult during ASVS audits, threat modeling, and PR reviews. Each file is a focused, actionable guide — not a dump of linked documentation.

| KB File | Coverage |
|---------|---------|
| `kb-api-security.md` | OWASP API Top 10, auth/authz patterns, input validation, error leakage, rate limiting, JWT hardening |
| `kb-secure-coding-fundamentals.md` | Language-agnostic secure coding principles: injection prevention, output encoding, principle of least privilege, defense in depth |
| `kb-secrets-management.md` | Secret rotation lifecycle, Vault patterns, env-var anti-patterns, CI/CD secret injection, secret scanning |
| `kb-nodejs-security.md` | Node.js-specific: prototype pollution, `eval` avoidance, dependency hygiene, `helmet`, CSRF, async error handling |
| `kb-python-security.md` | Python-specific: SQL injection via raw queries, pickle deserialization risks, subprocess injection, dependency pinning |
| `kb-docker-security.md` | Container hardening: non-root users, `COPY` vs `ADD`, multi-stage builds, image scanning, secrets in layers, network isolation |
| `kb-vulnerability-management.md` | CVE triage process, CVSS scoring interpretation, patch prioritization, SCA toolchain (Dependabot, Trivy, Snyk) |

These KB files are **loaded selectively** per phase — the system only reads what is relevant to the active audit domain, preserving context window budget.

---

## Repository Structure

```
antigravity-core/
│
├── GEMINI.md                   # Persistent system brain — rules, routing, pipeline gates
│
├── agents/                     # 20 specialist agent personas
│   ├── orchestrator.md
│   ├── security-auditor.md
│   ├── frontend-specialist.md
│   └── ... (17 more)
│
├── workflows/                  # 33 executable procedures
│   ├── 00-pipeline-orchestrator.md
│   ├── 01a-attack-surface-mapping.md
│   ├── 03-asvs-audit-orchestrator.md
│   └── ... (30 more)
│
└── skills/                     # 40+ knowledge modules
    ├── api-patterns/
    │   ├── SKILL.md            # Entry point & content map
    │   └── references/         # Specialized deep-dives
    │       ├── rest.md
    │       ├── graphql.md
    │       ├── auth.md
    │       └── ...
    ├── devsecops-pipeline/
    │   ├── SKILL.md
    │   └── references/
    │       ├── kb-api-security.md
    │       ├── kb-secrets-management.md
    │       └── ...
    └── ... (38 more skill modules)
```

---

## 📊 Logging Protocol

Every agent execution emits a structured one-liner to `.agent/logs/orchestration.log`:

```
[TIMESTAMP] [AGENT] [MODEL_TIER] [TASK_TYPE] [COMPLEXITY] [QUOTA_ESTIMATE]
```

| Field | Example Values |
|-------|---------------|
| `TIMESTAMP` | `2025-03-23T14:05:00Z` |
| `AGENT` | `@security-auditor`, `@orchestrator`, `@frontend-specialist` |
| `MODEL_TIER` | `Opus`, `Sonnet`, `Flash` |
| `TASK_TYPE` | `PHASE_1`, `PHASE_2`, `PHASE_3`, `PHASE_4`, `SURVEY`, `BUILD`, `EVALUATE` |
| `COMPLEXITY` | `LOW`, `MODERATE`, `HIGH` |
| `QUOTA_ESTIMATE` | `0.1x`, `1x`, `8x` |

**Example:**
```
2025-03-23T14:05:00Z @security-auditor Sonnet PHASE_3 HIGH 1x — ASVS 3d: crypto audit initiated
```

> Agents log **before** starting the task. Secrets and user data are never logged. Log rotates at 5MB → `orchestration.log.bak`.

---

## 🚫 Anti-Patterns

See [`ANTI_PATTERNS.md`](./ANTI_PATTERNS.md) for the full reference. Quick examples:

| Anti-Pattern | Correct Approach |
|---|---|
| Loading all `kb-*.md` for a simple code task | Use router keywords; only load what the phase needs |
| Calling Opus for `"list files"` or `"show status"` | Let router classify → Flash tier |
| Skipping the Socratic Gate for a new feature | Ask ≥ 3 questions before any architecture decision |
| Agent chains with no defined output artifact | Every phase must declare its output file |
| Storing secrets in `session-state.md` | Use `.env` / Vault; session-state is task context only |

---

## Mandatory Protocols

### Pre-Task Gate (every session)
1. Read `.agent/session-state.md` to resume without re-ingesting context
2. Load relevant KB files for the current phase
3. Identify and announce the active agent: `🤖 Applying @[agent-name]...`

### Socratic Gate (every new feature)
Before implementation, agents are required to ask **minimum 3 strategic questions** covering trade-offs, edge cases, and constraints. No code is written until the design space is clear.

### Final Checklist (`"final checks"`)
```bash
python .agent/scripts/checklist.py .
# → security_scan.py → lint_runner.py → test_runner.py
```

### Bug Persistence Protocol
When a bug is fixed, a lint error is resolved, or a failure is corrected:
1. Append the issue to [`RESOLVED_ISSUES.md`](./RESOLVED_ISSUES.md) at the repository root.
2. Structure: Date, Symptom, Root Cause, Resolution, and **Prevention Rule**.
3. Always check `RESOLVED_ISSUES.md` at start of debugging to avoid repeating mistakes.

---

## Credits & Attribution

This system is built on top of **[vudovn/antigravity-kit](https://github.com/vudovn/antigravity-kit)** and extends it substantially with:

- Full 4-Phase DevSecOps Pipeline aligned with NIST SSDF and OWASP ASVS Level 2
- Intelligent model-tier routing to preserve API quota
- 20 bounded specialist agents with narrow authority scopes
- Socratic Gate and Evaluator-Optimizer feedback loops
- `references/` structured skill module architecture
- 9-domain ASVS audit orchestration framework
- PR Sentinel micro-SAST for diff-only security review
- Session state persistence to eliminate context re-ingestion overhead
