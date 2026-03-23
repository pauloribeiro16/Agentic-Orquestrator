---
description: "ASVS V5 — Validation, Sanitization and Encoding Verification Requirements"
asvs_version: "4.0.3"
chapter: "V5"
applicable_phases: "Phase 3 (03c-validation-encoding-audit)"
---

# ASVS V5: Validation, Sanitization and Encoding Verification Requirements

**Scope:** The most common web application security weakness is the failure to properly validate input coming from the client or the environment before directly using it. This chapter covers input validation, output encoding, and parameterized query requirements.

---

## V5.1 — Input Validation

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V5.1.1 | Verify that the application has defenses against HTTP parameter pollution attacks, particularly if the application framework makes no distinction about the source of request parameters (GET, POST, cookies, headers, or environment variables). | L1 | Yes | Dynamic Test: Send duplicate parameters with different values. Verify predictable handling. |
| V5.1.2 | Verify that frameworks protect against mass parameter assignment attacks, or that the application has countermeasures to protect against unsafe parameter assignment, such as marking fields private or similar. | L1 | Yes | Code Review: Check for allowlisted fields on create/update operations. Verify `role`, `isAdmin`, `id` cannot be set. |
| V5.1.3 | Verify that all input (HTML form fields, REST requests, URL parameters, HTTP headers, cookies, batch files, RSS feeds) is validated using positive validation (allowlists). | L1 | Yes | Code Review: Check validation approach — must define what IS allowed, not what is blocked. |
| V5.1.4 | Verify that structured data is strongly typed and validated against a defined schema including allowed characters, length, and pattern (e.g., credit card numbers, e-mail addresses, telephone numbers, or validating that two related fields are reasonable, such as checking that suburb and zip/postcode match). | L1 | Yes | Code Review: Check schema validation (Zod, Joi, Pydantic) for typed fields with format constraints. |
| V5.1.5 | Verify that URL redirects and forwards only allow destinations which appear on an allowlist, or show a warning when redirecting to potentially untrusted content. | L1 | Yes | Code Review: Check redirect logic for URL allowlist validation. Dynamic Test: Attempt open redirect. |

---

## V5.2 — Sanitization and Sandboxing

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V5.2.1 | Verify that all untrusted HTML input from WYSIWYG editors or similar is properly sanitized with an HTML sanitizer library or framework feature. | L1 | Yes | Code Review: Check HTML input handling for sanitizer usage (DOMPurify, sanitize-html, bleach). |
| V5.2.2 | Verify that unstructured data is sanitized to enforce safety measures such as allowed characters and length. | L1 | Yes | Code Review: Check that free-text inputs have character and length constraints. |
| V5.2.3 | Verify that the application sanitizes user input before passing to mail systems to protect against SMTP or IMAP injection. | L1 | Yes | Code Review: Check email-sending code for injection of headers via user input. |
| V5.2.4 | Verify that the application avoids the use of eval() or other dynamic code execution features. Where there is no alternative, any user input being included must be sanitized or sandboxed before being executed. | L1 | Yes | Code Review: Search for `eval()`, `Function()`, `exec()`, `setTimeout(string)`. Flag if user input can reach them. |
| V5.2.5 | Verify that the application protects against template injection attacks by ensuring that any user input being included is sanitized or sandboxed. | L1 | Yes | Code Review: Check server-side template rendering for unsanitized user input in template expressions. |
| V5.2.6 | Verify that the application protects against SSRF attacks, by validating or sanitizing untrusted data or HTTP file metadata, such as filenames and URL input fields, and uses allowlists of protocols, domains, paths and ports. | L1 | Yes | Code Review: Check outbound HTTP requests constructed from user input for domain allowlisting. |
| V5.2.7 | Verify that the application sanitizes, disables, or sandboxes user-supplied Scalable Vector Graphics (SVG) scriptable content, especially as they relate to XSS resulting from inline scripts, and foreignObject. | L1 | Yes | Code Review: Check SVG upload/rendering for script content stripping. |
| V5.2.8 | Verify that the application sanitizes, disables, or sandboxes user-supplied scriptable or expression template language content, such as Markdown, CSS or XSL stylesheets, BBCode, or similar. | L1 | Yes | Code Review: Check user-supplied Markdown/CSS rendering for script injection vectors. |

---

## V5.3 — Output Encoding and Injection Prevention

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V5.3.1 | Verify that output encoding is relevant for the interpreter and context required. For example, use encoders specifically for HTML values, HTML attributes, JavaScript, URL parameters, HTTP headers, SMTP, and others as the context requires, especially from untrusted inputs (e.g., names with Unicode or apostrophes, such as ねこ or O'Hara). | L1 | Yes | Code Review: Check output encoding is context-appropriate (HTML entities for HTML, URL encoding for URLs, etc.). |
| V5.3.2 | Verify that output encoding preserves the user's chosen character set and locale, such that any Unicode character point is valid and safely handled. | L1 | Yes | Code Review: Check that encoding handles Unicode correctly without data loss. |
| V5.3.3 | Verify that context-aware, preferably automated — or at worst, manual — output escaping protects against reflected, stored, and DOM based XSS. | L1 | Yes | Code Review: Check framework auto-escaping is enabled. Search for bypasses (dangerouslySetInnerHTML, v-html). |
| V5.3.4 | Verify that data selection or database queries (e.g., SQL, HQL, ORM, NoSQL) use parameterized queries, ORMs, entity frameworks, or are otherwise protected from database injection attacks. | L1 | Yes | Code Review: Verify ALL database queries use parameterized inputs. Flag any string concatenation. |
| V5.3.5 | Verify that where parameterized or safer mechanisms are not present, context-specific output encoding is used to protect against injection attacks, such as the use of SQL escaping to protect against SQL injection. | L1 | Yes | Code Review: If raw queries exist, check for proper escaping functions. |
| V5.3.6 | Verify that the application protects against JSON injection attacks, JSON eval attacks, and JavaScript expression evaluation. | L1 | Yes | Code Review: Check JSON parsing uses JSON.parse(), not eval(). Check for JSON injection in API responses. |
| V5.3.7 | Verify that the application protects against LDAP injection vulnerabilities, or that specific security controls to prevent LDAP injection have been implemented. | L1 | Yes | Code Review: If LDAP is used, check for parameterized LDAP queries. |
| V5.3.8 | Verify that the application protects against OS command injection and that operating system calls use parameterized OS queries or use contextual command line output encoding. | L1 | Yes | Code Review: Search for exec/spawn/system calls. Verify user input never reaches shell commands directly. |
| V5.3.9 | Verify that the application protects against Local File Inclusion (LFI) or Remote File Inclusion (RFI) attacks. | L1 | Yes | Code Review: Check dynamic file includes (require, import, include) for user-controlled paths. |
| V5.3.10 | Verify that the application protects against XPath injection or XML injection attacks. | L1 | Yes | Code Review: If XML/XPath is used, check for parameterized queries and disabled external entities. |

---

## V5.4 — Memory, String, and Unmanaged Code

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V5.4.1 | Verify that the application uses memory-safe string, safer memory copy and pointer arithmetic to detect or prevent stack, buffer, or heap overflows. | L2 | Yes | Code Review: If native addons or C/C++ code is used, check for safe memory handling. |
| V5.4.2 | Verify that format strings do not take potentially hostile input, and are constant. | L2 | Yes | Code Review: Check for user input in format strings (printf-style functions). |
| V5.4.3 | Verify that sign, range, and input validation techniques are used to prevent integer overflows. | L2 | Yes | Code Review: Check numeric inputs for range validation before arithmetic operations. |

---

## V5.5 — Deserialization Prevention

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V5.5.1 | Verify that serialized objects use integrity checks or are encrypted to prevent hostile object creation or data tampering. | L1 | Yes | Code Review: Check deserialization of untrusted data for integrity verification. |
| V5.5.2 | Verify that the application correctly restricts XML parsers to only use the most restrictive configuration possible and to ensure that unsafe features such as resolving external entities are disabled to prevent XML eXternal Entity (XXE) attacks. | L1 | Yes | Code Review: Check XML parser configuration for disabled external entities and DTD processing. |
| V5.5.3 | Verify that deserialization of untrusted data is avoided or is protected in both custom code and third-party libraries (such as JSON, XML and YAML parsers). | L1 | Yes | Code Review: Check for deserialization of untrusted input without schema validation. |
| V5.5.4 | Verify that when parsing JSON in browsers or JavaScript-based backends, JSON.parse is used to parse the JSON document. Do not use eval() to parse JSON. | L1 | Yes | Code Review: Search for `eval()` used on JSON strings. Must use `JSON.parse()`. |
