---
description: "Knowledge Base — Secrets Management"
type: "reference"
scope: "universal"
stack: "all"
last_updated: "2025-01-01"
---

# Secrets Management

**Purpose:** Comprehensive guidance on handling secrets (API keys, database credentials, encryption keys, tokens) throughout the software development lifecycle. Applies to every feature.

---

## 1. What Qualifies as a Secret

| Category | Examples | Risk if Exposed |
|---|---|---|
| **Database Credentials** | Connection strings, usernames, passwords | Full data breach, data manipulation |
| **API Keys** | Third-party service keys (Stripe, AWS, SendGrid) | Financial loss, service abuse, data exfiltration |
| **Encryption Keys** | AES keys, RSA private keys, JWT signing secrets | Data decryption, token forgery, impersonation |
| **OAuth Credentials** | Client secrets, refresh tokens | Account takeover, unauthorized API access |
| **Infrastructure Secrets** | SSH keys, cloud IAM credentials, deploy tokens | Full infrastructure compromise |
| **Session Secrets** | Cookie signing keys, session encryption keys | Session hijacking, authentication bypass |
| **Webhook Secrets** | HMAC signing keys for webhooks | Request forgery, data injection |
| **Internal Tokens** | Service-to-service auth tokens | Lateral movement within infrastructure |

---

## 2. The Golden Rules

### Rule 1: Secrets Must NEVER Be in Source Code
No exceptions. Not "temporarily." Not "just for testing." Not in comments. Not in dead code.

### Rule 2: Secrets Must NEVER Be in Version Control History
If a secret was ever committed, it must be considered compromised and rotated immediately — even if the commit was reverted. Git history preserves everything.

### Rule 3: Every Environment Gets Its Own Secrets
Development, staging, and production must use completely different secrets. Leaking a dev secret should not compromise production.

### Rule 4: Secrets Must Be Rotatable Without Downtime
The application architecture must support secret rotation without redeployment. This means loading secrets at runtime, not compile time.

### Rule 5: Access to Secrets Must Be Audited
Every access to a secret (read, modify, rotate) must be logged.

---

## 3. Secret Storage Hierarchy (Best to Worst)

### Tier 1: Dedicated Secrets Manager (Recommended for Production)
- **AWS Secrets Manager** — Auto-rotation, fine-grained IAM policies, encryption at rest.
- **HashiCorp Vault** — Dynamic secrets, leasing, comprehensive audit logging.
- **Google Cloud Secret Manager** — IAM-based access control, versioning.
- **Azure Key Vault** — HSM-backed, access policies, certificate management.

**When to use:** Production environments, any secret that protects user data or financial transactions.

### Tier 2: Environment Variables (Acceptable Minimum)
- Set via deployment platform (Heroku, Render, Vercel), CI/CD secrets, or container orchestration.
- Secrets injected at runtime, not baked into images or artifacts.

**When to use:** Small projects, staging environments, teams without vault infrastructure.

**Caveats:**
- Environment variables can leak via process listings, crash dumps, debug endpoints, and child processes.
- Use `.env` files for local development only — never commit them.

### Tier 3: Encrypted Configuration Files (Acceptable for Some Cases)
- Tools like `sops`, `git-crypt`, or `ansible-vault` encrypt config files that can be committed to version control.
- Requires key management for the encryption key itself.

**When to use:** Infrastructure-as-code secrets, configuration that must live alongside code.

### Tier 4: Plaintext in Environment Templates (UNACCEPTABLE)
- `.env` files committed to version control with real values.
- Hardcoded strings in source code.
- Config files with embedded passwords.

**NEVER use in any environment.**

---

## 4. Implementation Patterns

### 4.1 Node.js — Loading Secrets

```javascript
// DEVELOPMENT: Load from .env file (development only)
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}

// PRODUCTION: Secrets loaded from environment (set by platform/vault)
const config = {
  database: {
    url: process.env.DATABASE_URL,
    // NEVER: url: 'postgres://admin:password123@db:5432/myapp'
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    // NEVER: secret: 'my-jwt-secret'
  },
  stripe: {
    key: process.env.STRIPE_SECRET_KEY,
    // NEVER: key: 'sk_live_xxx'
  },
};

// Validate at startup — fail fast if missing
const required = ['DATABASE_URL', 'JWT_SECRET'];
for (const key of required) {
  if (!process.env[key]) {
    console.error(`FATAL: Missing ${key}`);
    process.exit(1);
  }
}
```

### 4.2 Python — Loading Secrets

```python
import os
import sys

# DEVELOPMENT: Load from .env file
if os.environ.get("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# PRODUCTION: Secrets from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
JWT_SECRET = os.environ.get("JWT_SECRET")
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY")

# Validate at startup
required = ["DATABASE_URL", "JWT_SECRET"]
missing = [k for k in required if not os.environ.get(k)]
if missing:
    print(f"FATAL: Missing environment variables: {', '.join(missing)}")
    sys.exit(1)
```

### 4.3 AWS Secrets Manager (Runtime Loading)

```javascript
// Node.js — load secret at runtime, cache with TTL
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'us-east-1' });
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function getSecret(secretId) {
  const cached = cache.get(secretId);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.value;
  }
  
  const command = new GetSecretValueCommand({ SecretId: secretId });
  const response = await client.send(command);
  const value = JSON.parse(response.SecretString);
  
  cache.set(secretId, { value, timestamp: Date.now() });
  return value;
}
```

---

## 5. .env File Management

### 5.1 .gitignore (MANDATORY)
```
# ALWAYS ignore .env files
.env
.env.local
.env.production
.env.*.local

# Keep the template
!.env.example
```

### 5.2 .env.example (Commit This)
```bash
# .env.example — NO real values, only instructions
DATABASE_URL=postgres://user:password@localhost:5432/dbname
JWT_SECRET=generate-a-random-256-bit-key-here
STRIPE_SECRET_KEY=sk_test_your_test_key_here
SESSION_SECRET=generate-a-random-string-here

# Generate secrets with:
# node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
# python -c "import secrets; print(secrets.token_hex(32))"
```

### 5.3 Anti-patterns

```bash
# BAD: Real values in .env.example
DATABASE_URL=postgres://admin:realpassword@production-db:5432/app

# BAD: .env committed to repo (check git history!)
# BAD: Different .env files for environments committed (e.g., .env.production)
# BAD: Secrets in docker-compose.yml
```

---

## 6. CI/CD Secret Handling

### 6.1 GitHub Actions

```yaml
# GOOD: Use GitHub Secrets
- name: Deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh

# BAD: Secrets in workflow file
- name: Deploy
  env:
    DATABASE_URL: "postgres://admin:password@db:5432/app"  # EXPOSED IN REPO

# BAD: Echo secrets (can bypass masking)
- run: echo ${{ secrets.API_KEY }}  # Logged in plaintext!

# BAD: Secrets in workflow names or annotations
# BAD: String manipulation that unmasks secrets
- run: echo "${{ secrets.TOKEN }}" | base64  # Masking bypassed
```

### 6.2 Docker

```dockerfile
# BAD: Baking secrets into image
COPY .env /app/.env
ENV DATABASE_URL=postgres://admin:password@db:5432/app

# GOOD: Inject at runtime
# docker run -e DATABASE_URL=xxx -e JWT_SECRET=xxx myapp

# GOOD: Use Docker secrets (Swarm) or Kubernetes secrets
```

---

## 7. Secret Rotation Procedure

### 7.1 When to Rotate
- **Immediately:** Secret was committed to version control, leaked in logs, exposed in a breach, or an employee with access left the team.
- **Scheduled:** Every 90 days for high-value secrets (database credentials, signing keys).
- **On Demand:** When upgrading encryption algorithms or changing secret storage.

### 7.2 Rotation Steps
1. Generate new secret.
2. Update the secret in the secrets manager / environment configuration.
3. Deploy the application with the new secret (or trigger runtime refresh).
4. Verify the application works with the new secret.
5. Revoke the old secret.
6. Audit that the old secret is no longer in use anywhere.

### 7.3 Dual-Secret Support
For zero-downtime rotation, the application should support accepting both old and new secrets during a transition window:

```javascript
// Accept both old and new JWT secrets during rotation
function verifyToken(token) {
  const secrets = [process.env.JWT_SECRET, process.env.JWT_SECRET_PREVIOUS].filter(Boolean);
  for (const secret of secrets) {
    try {
      return jwt.verify(token, secret, { algorithms: ['HS256'] });
    } catch (e) { continue; }
  }
  throw new Error('Invalid token');
}
```

---

## 8. Secret Detection Patterns

### 8.1 Common Patterns to Scan For

| Secret Type | Pattern / Indicator |
|---|---|
| AWS Access Key | Starts with `AKIA` followed by 16 alphanumeric chars |
| AWS Secret Key | 40-character base64 string near AWS context |
| GitHub PAT | `ghp_` followed by 36 alphanumeric chars |
| Stripe Live Key | `sk_live_` followed by 24+ alphanumeric chars |
| Slack Webhook | `https://hooks.slack.com/services/T...` |
| Google API Key | `AIza` followed by 35 chars |
| Private Key | `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----` |
| Database URI | `postgres://`, `mysql://`, `mongodb://` with embedded credentials |
| Generic Password | Variable named `password`, `secret`, `api_key`, `token` assigned a string literal |
| High Entropy String | 20+ character string with Shannon entropy > 4.5 |

### 8.2 Tools for Detection
- **Pre-commit:** `gitleaks`, `detect-secrets`, `trufflehog` — scan before commit.
- **CI/CD:** Integrate secret scanning in the pipeline as a blocking check.
- **Repository-level:** GitHub Secret Scanning (automatic for public repos).
