---
description: "Phase 5 — Evaluator-Optimizer (Critique & Refine Loop)"
phase: 5
nist_ssdf: "PW.8 — Validate and Verify Software Interfaces"
triggers: "Invocable via /evaluate or optionally after Phase 4 for complex features."
input_required: "Target file(s) or artifact to evaluate"
---

# Phase 5: Evaluator-Optimizer Cycle

**Purpose:** Applies an automated `Generate → Critique → Refine` loop to an implemented feature to ensure high standards of security, clean code, and UI/UX before finalizing the work.

---

## Step 1: Identify Artifact & Context

**Action:** Determine what artifact is being evaluated (e.g., a specific modified file, a newly created component, or a design document).

---

## Step 2: Establish Evaluation Criteria

**Action:** Select the appropriate threshold and criteria based on the artifact type.

- **Security Code:** Threshold 90/100.
- **Clean Code / Backend Logic:** Threshold 85/100.
- **UI/UX (Frontend):** Threshold 80/100.
- **Documentation:** Threshold 75/100.

---

## Step 3: Generate Structured Critique

**Action:** Evaluate the artifact and output a structured critique report. Provide a score out of 100.

**Format required:**
- Score out of 100.
- Findings categorized by High, Medium, and Low severity.
- Exact file locations and actionable fix suggestions.

---

## Step 4: Refinement Decision

**Action:** Compare the generated Score against the Threshold.

**If Score >= Threshold:**
- Pass the evaluation. No further refinement required.
- **Output:** Approved artifact.

**If Score < Threshold:**
- Initiate Refinement.
- Apply the suggested fixes to the code directly.
- **Iterate:** Go back to Step 3 (maximum of 2 iterations by default).

---

## Step 5: Final Output & Summary

**Action:** Once the artifact passes the threshold (or max iterations are reached), present the final diff of changes made during the refinement cycle and the final evaluation report.
