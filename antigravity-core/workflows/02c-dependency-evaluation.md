---
description: "Phase 2c — Dependency Evaluation (Pre-Adoption)"
phase: 2
nist_ssdf: "PS.3 — Verify Third-Party Software Meets Security Requirements"
asvs_reference: "asvs-v14-configuration.md (V14.2 — Dependency)"
triggers: "Called by 00-pipeline-orchestrator.md when feature brief lists new dependencies"
input_required: "New Dependencies list from Feature Brief (Section 8)"
---

# Phase 2c: Dependency Evaluation (Pre-Adoption)

**Purpose:** Evaluate new third-party libraries BEFORE they are added to the project. This is a proactive assessment — unlike the reactive SCA scan in Phase 3 that checks what's already installed.

---

## Step 1: Inventory New Dependencies

**Action:** Extract all new packages listed in Section 8 of the Feature Brief.

**For each dependency, collect:**

| Field | What to Record |
|---|---|
| Package Name | Exact name as published (e.g., `express-rate-limit`) |
| Intended Version | Version or range to be installed |
| Package Registry | npm, PyPI, GitHub, etc. |
| Purpose | Why this package is being added |
| Alternatives Considered | What other options were evaluated (if known) |

---

## Step 2: Supply Chain Risk Assessment

**Action:** For each new dependency, evaluate supply chain risk indicators.

### 2.1 Maintainer Health
- **Active Maintenance:** When was the last release? Last commit? Is there a regular release cadence?
- **Maintainer Count:** How many active maintainers? Single-maintainer packages are higher risk.
- **Organization Backing:** Is the package maintained by an individual, a company, or a recognized open-source foundation?
- **Red Flag:** Package has not been updated in > 12 months AND has open security issues.

### 2.2 Community & Adoption
- **Download Volume:** Weekly downloads on npm/PyPI. Low-download packages may be less battle-tested.
- **GitHub Stars / Forks:** Indicator of community trust (not definitive, but directional).
- **Issue Response Time:** Are security issues acknowledged and addressed promptly?
- **Red Flag:** Package has < 1,000 weekly downloads and no organizational backing.

### 2.3 Typosquatting Check
- **Name Similarity:** Does the package name closely resemble a popular package? (e.g., `expres` vs `express`, `requets` vs `requests`)
- **Recent Creation:** Was the package created very recently with a name similar to an established package?
- **Red Flag:** Package name differs by 1-2 characters from a popular package AND was created within the last 6 months.

### 2.4 Known Vulnerabilities
- **CVE Check:** Does the specified version have any known CVEs?
- **Advisory History:** Has this package had frequent security advisories? This may indicate systemic code quality issues.
- **Transitive Risk:** What are the package's own dependencies? Are any of those known-vulnerable?

---

## Step 3: License Compatibility

**Action:** Verify the license is compatible with the project's license and usage model.

**Common license compatibility:**

| License | Commercial Use | Copyleft Risk | Notes |
|---|---|---|---|
| MIT | ✅ | None | Safe for any use |
| Apache 2.0 | ✅ | None | Safe, includes patent grant |
| BSD 2/3 | ✅ | None | Safe for any use |
| ISC | ✅ | None | Safe for any use |
| GPL 2.0/3.0 | ⚠️ | Strong | Copyleft — may require source disclosure |
| LGPL | ⚠️ | Weak | Generally safe if dynamically linked |
| AGPL | ❌ | Strong | Network use triggers copyleft — high risk for SaaS |
| Unlicensed | ❌ | Unknown | No license = no permission. Do not use. |

**Red Flag:** Any AGPL dependency in a SaaS product, or any package with no license specified.

---

## Step 4: Security Surface Analysis

**Action:** Evaluate what the package can do and whether it introduces unnecessary risk surface.

**Check the following:**

1. **Permission Scope:** Does the package require access to the filesystem, network, environment variables, or native bindings that are excessive for its stated purpose?
2. **Install Scripts:** Does the package run `preinstall`, `postinstall`, or similar lifecycle scripts? These can execute arbitrary code during `npm install` / `pip install`.
3. **Native Bindings:** Does the package compile native code (C/C++ addons)? This increases the attack surface and may complicate patching.
4. **Dependency Depth:** How many transitive dependencies does this package bring in? A package with 200+ transitive dependencies multiplies supply chain risk.

---

## Step 5: Evaluation Decision Matrix

**Action:** For each dependency, produce a decision using this matrix.

**Scoring:**

| Factor | Low Risk (0) | Medium Risk (1) | High Risk (2) |
|---|---|---|---|
| Maintenance | Active, multiple maintainers | Active, single maintainer | Inactive > 12 months |
| Adoption | > 100K weekly downloads | 10K–100K weekly downloads | < 10K weekly downloads |
| Vulnerabilities | No known CVEs | Past CVEs, all patched | Active unpatched CVEs |
| License | MIT/Apache/BSD | LGPL | GPL/AGPL/Unlicensed |
| Dependency Depth | < 10 transitive deps | 10–50 transitive deps | > 50 transitive deps |
| Install Scripts | None | Benign build scripts | Suspicious or obfuscated |

**Decision thresholds:**
- **Score 0–3:** ✅ APPROVE — Low risk, proceed with adoption.
- **Score 4–6:** ⚠️ CONDITIONAL — Accept with documented risk and review schedule.
- **Score 7+:** ❌ REJECT — Find an alternative or build in-house.

---

## Step 6: Compile Dependency Evaluation Report

**Action:** Add findings to the `outputs/[feature-name]/secure-design.md` under a new section.

**Format:**

```markdown
## Dependency Evaluation

### [Package Name] v[Version]
- **Purpose:** [Why it's being added]
- **Registry:** [npm / PyPI]
- **Risk Score:** [X/12] — [APPROVE / CONDITIONAL / REJECT]
- **Maintenance:** [Assessment]
- **Adoption:** [Weekly downloads, stars]
- **Vulnerabilities:** [CVE status]
- **License:** [License type and compatibility]
- **Transitive Dependencies:** [Count]
- **Install Scripts:** [Yes/No, assessment]
- **Decision:** [APPROVE / CONDITIONAL with conditions / REJECT with alternative recommendation]

### [Next Package...]
```

**If REJECTED:** Recommend a specific alternative with a brief justification.

**If CONDITIONAL:** Document the conditions (e.g., "Accepted contingent on pinning to exact version and reviewing at next quarterly dependency audit").
