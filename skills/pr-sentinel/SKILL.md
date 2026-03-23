---
name: pr-sentinel
description: Lightweight micro-SAST for pull request diffs. Phase 4 of the DevSecOps pipeline. Analyzes only changed lines for injection, missing auth, error leaks, and hardcoded secrets. Triggers on PR review, pull request security, code review security, diff review, pre-merge check, SAST, security PR.
---

# PR Sentinel — Micro-SAST (Pipeline Phase 4)

> NIST SSDF: PW.7 — Review and/or Analyze Human-Readable Code

**Purpose:** Fast, final security check before merge. Analyzes ONLY the diff and immediate context. This is NOT a full audit — it catches regressions and human errors.

---

## Step 1: Diff Extraction & Scope

**In scope:**
- New or modified functions, classes, methods
- New or modified API routes, controllers, middleware chains
- New or modified database queries
- New or modified security-affecting configuration

**Out of scope (unless explicitly requested):**
- Documentation (`.md`)
- Test files (`.spec.ts`, `.test.js`, `test_*.py`) — unless testing security controls
- Auto-generated files (lockfiles, build outputs)

---

## Step 2: Input Sanitization & Injection Check

Scan new/modified functions accepting external parameters.

**Flag patterns:**

```javascript
// FAIL: SQL concatenation
const query = `SELECT * FROM users WHERE id = '${req.params.id}'`;

// FAIL: Command injection
exec(`convert ${req.body.filename} output.png`);

// FAIL: XSS via dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// FAIL: Path traversal
const filePath = path.join('/uploads', req.params.filename);
// Missing: path.resolve() + startsWith() check
```

Check for:
1. Raw user input in SQL/NoSQL queries or shell commands
2. User input rendered in HTML without encoding
3. User input in file paths without validation
4. User input in outbound URLs without allowlisting

---

## Step 3: Authorization & Middleware Verification

For each new route in the diff:

1. Authentication middleware attached (unless intentionally public — must be documented)
2. Authorization middleware checks correct role/permission
3. Middleware chain order correct (auth before business logic)

**Flag pattern:**
```javascript
// FAIL: No auth middleware
router.get('/api/users/:id/invoices', invoiceController.getByUser);

// PASS: Auth + authz middleware
router.get('/api/users/:id/invoices', authenticate, authorize('read:invoices'), invoiceController.getByUser);
```

---

## Step 4: Sensitive Data & Error Handling

**Error responses:** Flag stack traces, DB errors, framework internals returned to client. Flag different error messages enabling enumeration.

**Secret sniffing in diff:** Scan for variable names (`api_key`, `password`, `secret`, `token`, `bearer`, `private_key`) and value patterns (AWS `AKIA`, long hex/base64 strings assigned to constants).

---

## Step 5: Regression Check Against Phase 3

If Phase 3 audit results exist for this feature:
- Were remediation suggestions from the audit actually implemented?
- Did the implementation introduce new issues not caught in Phase 3?

---

## Step 6: Generate PR Comments

**Format per finding — concise:**

```markdown
---
**📍 File:** `src/controllers/invoice.controller.ts` — Line 47
**🔴 Issue:** Missing ownership check — IDOR vulnerability.
**⚡ Risk:** High
**✅ Suggested Fix:**
// Before: fetches any invoice
const invoice = await Invoice.findById(req.params.id);
// After: scoped to authenticated user
const invoice = await Invoice.findOne({ _id: req.params.id, userId: req.user.id });
---
```

**Rules:**
1. Specific — exact file and line number
2. Constructive — always include a code suggestion
3. Concise — one issue per comment block
4. Rated — Low / Medium / High / Critical
5. Minimal — only flag issues in the diff, no massive reports
6. If no issues found, explicitly state the PR passes


## 📑 Content Map

| File | Description |
|------|-------------|
| `SKILL.md` | Main Skill Definition |
