---
name: evaluator-optimizer
description: Evaluator-Optimizer orchestration pattern for code critique and refinement. Executes the Generate -> Critique -> Refine loop. Triggers on evaluate, critique, review quality, refinar.
allowed-tools: Read, Glob, Grep, Replace, Write
---

# Evaluator-Optimizer Pattern

> **MANDATORY:** Use for quality control after implementation phases (Phase 5).

---

## Overview

This skill implements the **Evaluator-Optimizer** orchestration pattern. It takes an artifact (code, documentation, design), evaluates it against defined criteria, generates a structured critique with a score, and if the score falls below a threshold, refines the artifact.

## Refinement Loop

1. **Evaluate**: Assess the artifact against the criteria for its type.
2. **Score**: Assign a score from 0 to 100.
3. **Decide**: If the score is >= the threshold, the cycle is complete. If the score is < threshold, proceed to Refine.
4. **Refine**: Apply the suggested fixes to the artifact to improve it.
5. **Iterate**: Repeat up to a maximum number of iterations (default 2, 3 for critical features).

---

## Thresholds by Artifact Type

| Type | Approval Threshold | Criteria Focus |
|------|--------------------|----------------|
| Security Code | 90/100 | Injection, Auth/Authz, Data handling, Error leaking |
| UI/UX Code | 80/100 | Accessibility, Responsiveness, State management, Contrast |
| Documentation | 75/100 | Clarity, Structure, Completeness, Accuracy |
| Clean Code | 85/100 | Complexity, Naming, Directness, Lack of over-engineering |

---

## Critique Output Format

```markdown
# Evaluation Report: [Artifact Name]

## Score: [Score]/100
**Status:** [PASS / REFINEMENT REQUIRED]

## Summary
[Brief summary of overall quality and major issues]

## Findings by Severity

### 🔴 High Severity
- **Issue**: [Description]
- **Location**: [File:line]
- **Fix**: [Specific code suggestion or design instruction]

### 🟡 Medium Severity
- **Issue**: [Description]
- **Location**: [File:line]
- **Fix**: [Specific code suggestion or design instruction]

### 🟢 Low Severity / Nitpicks
- **Issue**: [Description]
- **Location**: [File:line]
- **Fix**: [Specific code suggestion or design instruction]
```

## Integration

- **Phase 4**: PR Sentinel provides initial Micro-SAST.
- **Phase 5**: Evaluator-Optimizer applies the automated critique and refinement loop to complex implementations.


## 📑 Content Map

| File | Description |
|------|-------------|
| `SKILL.md` | Main Skill Definition |
