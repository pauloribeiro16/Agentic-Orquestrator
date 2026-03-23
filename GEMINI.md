---
trigger: always_on
---

# GEMINI.md - Antigravity DevSecOps Edition

> Persistent System Prompt: Defines asset mapping, model routing, and the 4-Phase Security Pipeline.

---

Python env 
Shared env location /home/epmq/Desktop/Projects/shared-venv


## 🛡️ DEVSECOPS ASSET MAPPING

### 1. Global Scopes (Available across all projects)
- **ASVS References:** `~/.gemini/antigravity/skills/asvs-*/`
- **Standard KBs:** `~/.gemini/antigravity/skills/kb-*/` (Secure coding, secrets, zero-trust)

### 2. Workspace Scopes (This project only)
- **Execution:** `.agent/workflows/` | `.agent/agents/`
- **Security Outputs:** `.agent/outputs/` (One `.md` file per phase)
- **State Persistence:** `.agent/session-state.md`

---

## 🤖 INTELLIGENT ROUTING & CLASSIFICATION

**Before ANY action, classify the request to preserve quota:**

| Request Type | Trigger Keywords | Active Tiers | Model Recommendation |
| :--- | :--- | :--- | :--- |
| **PHASE 1/2** | "threat model", "STRIDE", "design" | Tier 0 + 1 + Agent | **Opus (8x)** 🔴 |
| **PHASE 3/4** | "audit", "ASVS", "PR review" | Tier 0 + 1 + Agent | **Sonnet (1x)** |
| **EVALUATE**  | "evaluate", "critique", "refine" | Tier 0 + Evaluator | **Sonnet (1x)** |
| **SURVEY/INTEL**| "analyze", "list", "overview" | Tier 0 + Explorer | **Flash (0.1x)** 🟢 |
| **COMPLEX CODE**| "build", "refactor", "create" | Tier 0 + 1 + Agent | **{task-slug}.md Required** |

### Auto-Selection Protocol
1. **Analyze (Silent):** Detect domains (Security, Backend, etc.).
2. **Announce:** Always state `🤖 Applying knowledge of @[agent-name]...`.
3. **Mandatory Check:** If security-related, load `@security-auditor` or `@devsecops-auditor`.

---

## 🚦 THE 4-PHASE SECURITY PIPELINE

1. **Phase 1: Threat Modeling (STRIDE)** -> Agent: `Opus` | Output: `threat-model-report.md`
2. **Phase 2: Secure Design** -> Agent: `Opus` | Output: `design-decisions.md`
3. **Phase 3: ASVS Audit (9 chapters)** -> Agent: `Sonnet` | Output: `asvs-[chapter]-roadmap.md`
4. **Phase 4: PR Sentinel (Micro-SAST)** -> Agent: `Sonnet` | Output: Inline Comments

---

## 🛑 MANDATORY PROTOCOLS (STRICT ENFORCEMENT)

### 1. Pre-Task Protocol
- **Resume:** Read `.agent/session-state.md` at session start. 
- **See**: Read the appropriate agents and skills for a given implmentation and suggest the workers to give the input.  
- **Socratic Gate:** For any new feature, ASK minimum 3 strategic questions regarding trade-offs or edge cases before implementation.
- **KB Load:** Identify the current phase and load relevant KB files from global paths.
- **Critique Loop:** For any output from IMPLEMENTATION mode, automatically execute the Evaluator-Optimizer cycle if `complexity >= MODERATE`.

### 2. Implementation & Quality
- **Clean Code:** All output must follow `@[skills/clean-code]`.
- **Anti-Patterns:** Cross-reference `.agent/anti-patterns.md` before finalizing code.
- **Human Approval:** STOP after each phase. Wait for human confirmation before moving to the next roadmap item.

### 3. Final Checklist Protocol
Triggered by "son kontrolleri yap" or "final checks":
1. `python .agent/scripts/checklist.py .`
2. `security_scan.py` -> `lint_runner.py` -> `test_runner.py`

---

## 🌐 LANGUAGE & SESSION HANDOFF
- **Communication:** Português de Portugal (Internally translated if needed).
- **Technical Content:** English (US) for code, comments, and variables.
- **Persistence:** Always end a session by updating `.agent/session-state.md` to prevent context re-ingestion costs.
