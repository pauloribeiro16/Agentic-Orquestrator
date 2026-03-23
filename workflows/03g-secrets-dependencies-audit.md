---
description: "Phase 3g — Secrets & Dependencies Audit (SCA)"
phase: 3
nist_ssdf: "PW.4 — Review and Audit Third-Party Software"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature adds dependencies or handles secrets"
input_required: "Feature codebase, package manifests, lock files, config files"
---

# Phase 3g: Secrets & Dependencies Audit

**Purpose:** Reactive scan of the codebase for hardcoded secrets and vulnerable dependencies. Complements the proactive Phase 2c (Dependency Evaluation) by checking what's actually in the code.

---

## Step 1: Scope Discovery

**Locate:**
- `.env`, `.env.example`, `.env.local` files.
- `Dockerfile`, `docker-compose.yml`.
- CI/CD pipeline files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`).
- `package.json`, `package-lock.json`, `yarn.lock` (Node.js).
- `requirements.txt`, `Pipfile.lock`, `poetry.lock` (Python).
- Configuration files (`config.js`, `settings.py`, `appsettings.json`).

---

## Step 2: Secret Detection

### 2.1 Pattern Matching
**Scan for known secret formats:**

| Pattern | Regex Indicator | Example |
|---|---|---|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| AWS Secret Key | 40-character base64 string near AWS context | |
| GitHub PAT | `ghp_[A-Za-z0-9]{36}` | |
| GitHub OAuth | `gho_[A-Za-z0-9]{36}` | |
| Stripe Key | `sk_live_[A-Za-z0-9]{24,}` | |
| Slack Webhook | `https://hooks.slack.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+` | |
| Google API Key | `AIza[0-9A-Za-z\-_]{35}` | |
| JWT/Bearer Token | Long base64 string with two dots (header.payload.signature) | |
| Generic Password | Variables named `password`, `passwd`, `pwd`, `secret`, `api_key`, `apikey`, `token`, `bearer` assigned string literals | |
| Database URI | `postgres://`, `mysql://`, `mongodb://` with embedded credentials | |

### 2.2 High Entropy String Detection
**Scan for strings with high Shannon entropy** (> 4.5 bits per character) that are:
- Longer than 20 characters.
- Assigned to configuration variables.
- Not obviously code (import paths, URLs to public services).

### 2.3 Configuration Leakage
**Check:**
- Is a `.env` file committed to version control? (Check `.gitignore`)
- Does `.env.example` contain real values instead of placeholder instructions?
- Are config objects in source code (e.g., `config.js`) containing plaintext secrets?

---

## Step 3: Software Composition Analysis (SCA)

### 3.1 Direct Dependency Audit
**Action:** Analyze `package.json` / `requirements.txt` for known vulnerabilities.
- Cross-reference package names and versions against CVE databases.
- Flag any dependency with a known Critical or High severity CVE.

### 3.2 Transitive Dependency Audit
**Action:** Analyze lock files for deeply nested vulnerable dependencies.
- Check `package-lock.json` / `yarn.lock` / `Pipfile.lock` for transitive dependencies with known CVEs.
- Note the dependency chain (which direct dependency pulls in the vulnerable transitive one).

### 3.3 Malicious Package Detection
**Flag if:**
- A recently added package name is suspiciously similar to a popular package (typosquatting).
- A package has `preinstall` or `postinstall` scripts that make network requests or execute obfuscated code.
- A package was published within the last 30 days with few downloads.

---

## Step 4: Compile Findings

**Output format for each finding:**

```markdown
### [SEVERITY]: [Finding Title]
- **Type:** Secret Leak / Vulnerable Dependency / Malicious Package
- **File:** [path]
- **Evidence:** [snippet or CVE ID]
- **Impact:** [What an attacker could do]
- **Remediation:** [Specific steps — e.g., "Revoke key, rotate, move to env variable"]
- **Priority:** Immediate / Next Sprint / Backlog
```

**Output:** Append findings to `outputs/[feature-name]/audit-workflow.md`.
