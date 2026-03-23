# Contributing to Agentic Orquestrator

> **Objective:** Maintain context hygiene, security auditing flow, and execution quota transparency.

---

## 🛠️ Workflows & Local Management

### 1. 📂 Core Directories
- **`agents/`**: Personas and triggers. Do not change authority defaults without consulting the architecture map.
- **`skills/`**: Knowledge routers (`SKILL.md`). Deep-dives go into `references/`.
- **`workflows/`**: Continuous Pipeline steps.

### 2. 🚦 Reporting Issues & Fixes
To prevent agents from repeating past mistakes, we maintain a persistent local bug registry.

*   **Rule:** When a bug is fixed, a lint error is resolved, or a failure is corrected, **ALWAYS** append the issue description to **`RESOLVED_ISSUES.md`** at the repository root.
*   **Format:** Date, Symptom, Root Cause, Resolution, and **Prevention Rule**.

---

## 🚫 Governance & Standards

### Anti-Patterns
Cross-reference **`ANTI_PATTERNS.md`** before committing any implementation. 
This file incorporates global safety thresholds with local template overrides.

### Security Gates
All pull requests must pass through the **Phase 4 — PR Sentinel** review step before being merged to `main`. This checks only the diff lines for:
- Injection vulnerabilities
- Broken Auth / Authz
- Secret leaks
- Debug error feedback leakage
