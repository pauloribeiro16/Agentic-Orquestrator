---
description: "Phase 4a — PR Diff Review (Micro-SAST)"
phase: 4
nist_ssdf: "PW.7 — Review and/or Analyze Human-Readable Code"
triggers: "Called by 00-pipeline-orchestrator.md when PR is opened for merge"
input_required: "PR diff / changed files"
---

# Phase 4a: PR Diff Review (Micro-SAST)

**Purpose:** Lightweight, fast, final security check before code is merged. Analyzes ONLY the changed lines (diff) and their immediate context. This is NOT a full audit — it catches regressions and human errors introduced in the final implementation.

---

## Step 1: Diff Extraction & Scope

**Action:** Extract and analyze only the changed lines and their surrounding functions for context.

**In scope:**
- New or modified functions, classes, and methods.
- New or modified API routes, controllers, and middleware chains.
- New or modified database queries.
- New or modified configuration files that affect security.

**Out of scope (unless explicitly requested):**
- Documentation files (`.md`).
- Test files (`.spec.ts`, `.test.js`, `test_*.py`) — unless they test security controls.
- Auto-generated files (lockfiles, build outputs).

---

## Step 2: Input Sanitization & Injection Check

**Action:** Scan new/modified functions that accept external parameters.

**Check for:**
1. Raw user input concatenated into SQL queries, NoSQL queries, or shell commands.
2. User input rendered in HTML without encoding.
3. User input used to construct file paths without validation.
4. User input used to build URLs for outbound requests without allowlisting.

**Flag pattern examples:**

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

---

## Step 3: Authorization & Middleware Verification

**Action:** Identify if any new routes or endpoints were added in the diff.

**For each new route, verify:**
1. Authentication middleware is attached (unless intentionally public — must be documented).
2. Authorization middleware checks the correct role/permission.
3. The middleware chain order is correct (auth before business logic).

**Flag pattern:**
```javascript
// FAIL: No auth middleware
router.get('/api/users/:id/invoices', invoiceController.getByUser);

// PASS: Auth + authz middleware present
router.get('/api/users/:id/invoices', authenticate, authorize('read:invoices'), invoiceController.getByUser);
```

---

## Step 4: Sensitive Data & Error Handling

**Action:** Review new `try/catch` blocks and error responses.

**Check for:**
1. Stack traces, database errors, or framework internals returned to the client.
2. Different error messages that enable account/resource enumeration.

**Secret Sniffing in Diff:**
Scan changed lines for strings matching:
- Variable names: `api_key`, `password`, `secret`, `token`, `bearer`, `private_key`.
- Value patterns: AWS keys (`AKIA`), long hex/base64 strings assigned to constants.

---

## Step 5: Regression Check Against Phase 3

**Action:** If Phase 3 audit results exist for this feature, cross-reference the PR diff against the FAIL findings.

**Verify:**
- Were the remediation suggestions from the audit report actually implemented?
- Did the implementation introduce any new issues not caught in Phase 3?

---

## Step 6: Generate PR Comments

**Action:** Output findings as direct, constructive PR review comments.

**Format per finding — keep it concise:**

```markdown
---
**📍 File:** `src/controllers/invoice.controller.ts` — Line 47
**🔴 Issue:** Missing ownership check — IDOR vulnerability. Any authenticated user can access any invoice by changing the `:id` parameter.
**⚡ Risk:** High
**✅ Suggested Fix:**
```typescript
// Before: fetches any invoice
const invoice = await Invoice.findById(req.params.id);

// After: scoped to authenticated user
const invoice = await Invoice.findOne({
  _id: req.params.id,
  userId: req.user.id
});
if (!invoice) return res.status(404).json({ error: "Not found" });
```
---
```

**Rules for PR comments:**
1. Be specific — exact file and line number.
2. Be constructive — always include a code suggestion.
3. Be concise — one issue per comment block.
4. Rate severity — Low / Medium / High / Critical.
5. Do NOT generate a massive report — only flag issues found in the diff.
6. If no issues are found, explicitly state the PR passes the security review.
