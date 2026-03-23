---
description: "Phase 3h — Configuration Security Audit"
phase: 3
nist_ssdf: "RV.1 — Identify and Confirm Vulnerabilities"
asvs_reference: "asvs-v14-configuration.md"
triggers: "Selected by 03-asvs-audit-orchestrator.md when feature modifies server/container/deployment config"
input_required: "security-requirements.md (REQ-CONFIG-xxx)"
---

# Phase 3h: Configuration Security Audit

**ASVS Chapter:** V14 (Configuration)

**CRITICAL:** Load `asvs-reference/asvs-v14-configuration.md` before starting.

---

## Step 1: Discovery

**Locate:**
- Web server configuration (Nginx, Apache, Express settings).
- Dockerfile and docker-compose.yml.
- Environment variable definitions and `.env` templates.
- HTTP security header configuration (Helmet, custom middleware).
- Build configuration (Webpack, Vite, esbuild settings).
- Deployment manifests (Kubernetes, Terraform, CloudFormation).

---

## Step 2: V14.1 — Build & Deploy Configuration

**What to check:**

1. **Debug Mode:** Is debug mode, development mode, or verbose error reporting disabled in production builds?
2. **Source Maps:** Are source maps excluded from production deployments? (They expose original source code)
3. **Build Artifacts:** Does the build process strip comments, test files, and development dependencies from production bundles?
4. **Environment Separation:** Are there distinct configurations for development, staging, and production? Are production secrets not present in development configs?

---

## Step 3: V14.2 — Dependency Configuration

**What to check:**

1. **Lockfile Integrity:** Are lockfiles (`package-lock.json`, `yarn.lock`, `Pipfile.lock`) committed to version control with integrity hashes?
2. **Version Pinning:** Are dependencies pinned to exact versions (not ranges) in production?
3. **Unused Dependencies:** Are there dependencies in the manifest that are not actually used? (Unnecessary attack surface)

---

## Step 4: V14.3 — Unintended Security Disclosure

**What to check:**

1. **Server Headers:** Is the server version header suppressed? (e.g., `X-Powered-By: Express` should be removed — use `helmet.hidePoweredBy()`)
2. **Directory Listing:** Is directory listing disabled on the web server?
3. **Default Files:** Are default installation files, README files, or changelog files accessible from the web root?
4. **Admin Interfaces:** Are admin panels, debug consoles (e.g., Django admin, phpMyAdmin) protected or disabled in production?

---

## Step 5: V14.4 — HTTP Security Headers

**What to check:**

| Header | Expected Value | Risk if Missing |
|---|---|---|
| `Content-Security-Policy` | Restrictive policy (no `unsafe-inline`, no `unsafe-eval`) | XSS amplification |
| `X-Content-Type-Options` | `nosniff` | MIME-type sniffing attacks |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Clickjacking |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Downgrade attacks |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or `no-referrer` | Information leakage |
| `Permissions-Policy` | Restrict camera, microphone, geolocation as needed | Feature abuse |
| `X-XSS-Protection` | `0` (deprecated, disable to prevent bypass) | — |

---

## Step 6: V14.5 — Container & Infrastructure Configuration

**What to check:**

1. **Base Image:** Is the Dockerfile using a minimal base image (`alpine`, `distroless`, `slim`)? Flag `latest` tags and bloated base images.
2. **Non-Root User:** Does the container run as a non-root user? (e.g., `USER node`, `USER appuser`)
3. **Exposed Ports:** Are only necessary ports exposed? Is the database port (5432, 3306, 27017) mapped to `0.0.0.0`? It should not be.
4. **Secrets in Images:** Are secrets baked into the Docker image (via `COPY .env` or `ENV SECRET=xxx`)? They must be injected at runtime.
5. **Multi-Stage Builds:** Is the production image built using multi-stage builds to exclude build tools and source code?
6. **Read-Only Filesystem:** Is the container filesystem mounted as read-only where possible?

---

## Step 7: Compile Assessment

**Action:** For every Level 2 requirement in V14, record PASS/FAIL/N-A.

**Output:** Append all V14 assessments to `outputs/[feature-name]/audit-workflow.md`.
