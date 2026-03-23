# Anti-Patterns Reference

> Cross-reference this file before finalizing any implementation or agent routing decision.
> Updated as new patterns are discovered in real sessions.

---

## 🔀 Routing Anti-Patterns

### ❌ Opus for trivial tasks
```
User: "list the files in this folder"
BAD:  → Routed to Opus (8x cost)
GOOD: → Router classifies as SURVEY → Flash (0.1x cost)
```
**Rule:** Only use Opus when the task explicitly involves threat modeling, secure architecture design, or STRIDE analysis.

---

### ❌ Skipping the model tier announcement
```
BAD:  Agent silently starts working with no declaration
GOOD: 🤖 Applying knowledge of @explorer-agent... [Flash tier]
```
**Rule:** Always announce the active agent and model tier before starting any task.

---

## 📚 KB Loading Anti-Patterns

### ❌ Loading the entire KB for a simple task
```
Task: "add a console.log to debug this function"
BAD:  Load kb-api-security.md + kb-docker-security.md + kb-secrets-management.md
GOOD: No KB load needed — this is a LOW complexity debug task
```
**Rule:** Use the Selective Reading Rule in each `SKILL.md`. Load **only** the reference file relevant to the active audit domain.

---

### ❌ Re-ingesting session context on every session start
```
BAD:  Re-reading all previous conversation history to rebuild context
GOOD: Read .agent/session-state.md → resume from last checkpoint
```
**Rule:** Always write `session-state.md` at the end of a session. Always read it at the start.

---

## 🤖 Agent Anti-Patterns

### ❌ Agent scope creep
```
BAD:  @frontend-specialist starts auditing backend auth logic
GOOD: @frontend-specialist flags the concern, @security-auditor handles the audit
```
**Rule:** Each agent operates strictly within its declared authority. Cross-domain concerns are handed off, not absorbed.

---

### ❌ Parallel agents writing to the same output file
```
BAD:  @security-auditor and @performance-optimizer both writing to design-decisions.md
GOOD: Each phase has its own declared output artifact
```
**Rule:** Every workflow phase must declare a unique output artifact in its frontmatter.

---

### ❌ Skipping the Socratic Gate
```
Task: "Build me a new authentication system"
BAD:  Agent immediately starts writing code
GOOD: Agent asks ≥ 3 questions:
      1. What user types need authentication? (employees, customers, service accounts?)
      2. What compliance requirements apply? (SOC2, GDPR, HIPAA?)
      3. Are there existing sessions to migrate or is this greenfield?
```
**Rule:** No implementation starts before the design space is clarified. Minimum 3 questions for any new feature or architecture.

---

## 🔐 Security Anti-Patterns

### ❌ Secrets in session-state.md
```
BAD:  session-state.md contains API keys, tokens, or passwords
GOOD: session-state.md contains only task context, phase status, and roadmap state
```
**Rule:** `session-state.md` is committed to version control. Never put credentials there.

---

### ❌ PR Sentinel reviewing entire codebase
```
BAD:  Phase 4 runs a full SAST scan on the whole repo on every PR
GOOD: Phase 4 analyzes ONLY the changed lines in the diff
```
**Rule:** PR Sentinel is diff-only. Full audits happen in Phase 3 (ASVS), not Phase 4.

---

### ❌ Threat modeling after implementation
```
BAD:  Team writes the feature, then asks "is this secure?"
GOOD: Phase 1 (STRIDE) runs before any code is written
```
**Rule:** Security gates are sequential. Phase 1 → Phase 2 → Phase 3 → Phase 4. Skipping ahead invalidates the pipeline.

---

## 📋 Workflow Anti-Patterns

### ❌ Workflows without declared outputs
```
BAD:  A workflow completes but produces no artifact
GOOD: Every workflow frontmatter declares: output: threat-model-report.md
```

### ❌ Proceeding to the next phase without human approval
```
BAD:  Pipeline auto-advances Phase 1 → Phase 2 → Phase 3 without review
GOOD: STOP after each phase. Wait for explicit human confirmation.
```
**Rule:** Human-in-the-loop is mandatory between every phase of the pipeline.
