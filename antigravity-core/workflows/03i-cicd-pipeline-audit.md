---
description: "Phase 3i — CI/CD Pipeline Security Audit"
phase: 3
nist_ssdf: "PS.1 — Protect All Forms of Code from Unauthorized Access and Tampering"
owasp_mapping: "A08:2021 — Software and Data Integrity Failures"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature modifies CI/CD pipelines or GitHub Actions"
input_required: "CI/CD pipeline files (.github/workflows/, Jenkinsfile, .gitlab-ci.yml, etc.)"
---

# Phase 3i: CI/CD Pipeline Security Audit

**Purpose:** Audit the security of CI/CD pipelines, GitHub Actions, and deployment automation. The pipeline itself is code — and a compromised pipeline compromises everything it deploys.

**OWASP Mapping:** A08:2021 — Software and Data Integrity Failures

---

## Step 1: Discovery

**Locate:**
- `.github/workflows/*.yml` (GitHub Actions).
- `.gitlab-ci.yml` (GitLab CI).
- `Jenkinsfile` (Jenkins).
- `Dockerfile` and `docker-compose.yml` used in CI.
- Build scripts (`Makefile`, `scripts/build.sh`, `scripts/deploy.sh`).
- Secret and environment variable configuration in CI settings.

---

## Step 2: GitHub Actions Security (If Applicable)

### 2.1 Third-Party Action Pinning
**What to check:**
- Are third-party actions pinned to a specific commit SHA rather than a mutable tag (`@v3`, `@latest`)?
- **FAIL pattern:** `uses: actions/checkout@v4`
- **PASS pattern:** `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1`

**Why:** A compromised third-party action referenced by tag can be silently updated with malicious code.

### 2.2 Workflow Triggers
**What to check:**
- Does any workflow use `pull_request_target` trigger? This runs the workflow with write permissions on PR events from forks — high risk for secret exfiltration.
- Does any workflow use `workflow_dispatch` without restricting who can trigger it?
- Is `push` trigger restricted to specific branches (e.g., `main`, `release/*`)?

### 2.3 Permissions
**What to check:**
- Do workflows set explicit, minimal `permissions` blocks? (`contents: read`, `pull-requests: write`, etc.)
- Are default permissions restrictive? (GitHub's default is `write` for everything — this should be overridden).
- **FAIL pattern:** No `permissions` block (inherits overly broad defaults).
- **PASS pattern:** `permissions: { contents: read, pull-requests: write }` — only what's needed.

### 2.4 Secret Handling
**What to check:**
- Are secrets accessed via `${{ secrets.SECRET_NAME }}` and never echoed to logs?
- Are secrets masked in output? (GitHub auto-masks, but `echo` with string manipulation can bypass this)
- Are secrets scoped to the minimum environments/branches that need them?

### 2.5 Script Injection
**What to check:**
- Are user-controlled values (PR title, branch name, commit message) used directly in `run:` blocks?
- **FAIL pattern:** `run: echo "PR title: ${{ github.event.pull_request.title }}"`
  - An attacker can craft a PR title containing shell commands.
- **PASS pattern:** Set the value as an environment variable first:
  ```yaml
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "PR title: $PR_TITLE"
  ```

---

## Step 3: General Pipeline Security

### 3.1 Build Environment Integrity
**What to check:**
1. Are build dependencies installed from locked manifests (lockfiles), not resolved dynamically?
2. Are Docker images used in CI pinned to digests, not just tags?
3. Is the build environment ephemeral (fresh for each run) or shared/persistent (risk of contamination)?

### 3.2 Artifact Integrity
**What to check:**
1. Are build artifacts (Docker images, packages) signed before deployment?
2. Is there a verification step before deploying to production?
3. Are artifacts stored in a private, access-controlled registry?

### 3.3 Deployment Security
**What to check:**
1. Is production deployment restricted to specific branches (e.g., only `main`)?
2. Is there a manual approval gate for production deployments?
3. Are deployment credentials scoped to minimum necessary permissions?
4. Can a single contributor push code AND deploy it without review? (Separation of duties)

### 3.4 Secret Rotation
**What to check:**
1. Are CI/CD secrets (deploy keys, API tokens) rotated on a schedule?
2. If a secret is compromised, is there a documented procedure to revoke and rotate?
3. Are secrets stored in the CI platform's secret store (not in the repository)?

---

## Step 4: Compile Assessment

**Output format for each finding:**

```markdown
### [SEVERITY]: [Finding Title]
- **File:** [pipeline file path]
- **Line:** [line number]
- **Issue:** [description]
- **Risk:** What an attacker could achieve
- **Remediation:** [specific fix with code example]
```

**Output:** Append all CI/CD findings to `outputs/[feature-name]/audit-workflow.md`.
