---
description: "ASVS V14 — Configuration Verification Requirements"
asvs_version: "4.0.3"
chapter: "V14"
applicable_phases: "Phase 3 (03h-configuration-audit)"
---

# ASVS V14: Configuration Verification Requirements

**Scope:** This chapter covers the secure configuration of the application, build pipeline, dependencies, HTTP security headers, and deployment environment.

---

## V14.1 — Build and Deploy

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V14.1.1 | Verify that the application build and deployment processes are performed in a secure fashion as appropriate, such as CI/CD automation, automated configuration management, and automated deployment scripts. | L2 | Yes | Config Review: Check CI/CD pipeline for automated, reproducible builds with security steps. |
| V14.1.2 | Verify that compiler flags are configured to enable all available buffer overflow protections and warnings, including stack randomization, data execution prevention, and to break the build if an unsafe pointer, memory, format string, integer, or string operation is found. | L2 | Yes | Config Review: If C/C++ native addons are used, check compiler flags for security hardening (-fstack-protector, -D_FORTIFY_SOURCE, etc.). |
| V14.1.3 | Verify that server configuration is hardened as per the recommendations of the application server and frameworks in use. | L2 | Yes | Config Review: Check web server and framework security settings against vendor hardening guides. |
| V14.1.4 | Verify that the application, configuration, and all dependencies can be re-deployed using automated deployment scripts, built from a documented and tested runbook in a reasonable time, or restored from backups in a timely fashion. | L2 | No | Operations Review: Verify deployment is scripted and tested, not manual. |
| V14.1.5 | Verify that authorized administrators can verify the integrity of all security-relevant configurations to detect tampering. | L2 | Yes | Config Review: Check for configuration integrity verification (checksums, git tracking of config). |

---

## V14.2 — Dependency

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V14.2.1 | Verify that all components are up to date, preferably using a dependency checker during build or compile time. | L1 | Yes | CI Review: Check for `npm audit`, `pip-audit`, `safety check`, or Snyk/Dependabot integration in build pipeline. |
| V14.2.2 | Verify that all unneeded features, documentation, sample applications and configurations are removed. | L1 | Yes | Code Review: Check for sample code, default pages, unused routes, and development utilities in production build. |
| V14.2.3 | Verify that if application assets, such as JavaScript libraries, CSS or web fonts, are hosted externally on a Content Delivery Network (CDN) or external provider, Subresource Integrity (SRI) is used to validate the integrity of the asset. | L1 | Yes | Code Review: Check `<script>` and `<link>` tags for CDN resources — must have `integrity` and `crossorigin` attributes. |
| V14.2.4 | Verify that third party components come from pre-defined, trusted and continually maintained repositories. | L2 | Yes | Config Review: Check that package registries are configured to use official sources only (npmjs.com, pypi.org). No untrusted registries. |
| V14.2.5 | Verify that a Software Bill of Materials (SBOM) is maintained of all third party libraries in use. | L2 | Yes | CI Review: Check for SBOM generation in build process (e.g., CycloneDX, SPDX). |
| V14.2.6 | Verify that the attack surface is reduced by sandboxing or encapsulating third party libraries to expose only the required behaviour into the application. | L2 | Yes | Code Review: Check that third-party libraries are wrapped/abstracted rather than used directly throughout the codebase. |

---

## V14.3 — Unintended Security Disclosure

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V14.3.1 | Verify that web or application server and framework error messages are configured to deliver user actionable, customized responses to eliminate any unintended security disclosures. | L1 | Yes | Dynamic Test: Trigger errors. Verify responses are generic, no stack traces or internal details. |
| V14.3.2 | Verify that web or application server and application framework debug modes are disabled in production to eliminate debug features, developer consoles, and unintended security disclosures. | L1 | Yes | Config Review: Check for `NODE_ENV=production`, `DEBUG=false`, Django `DEBUG=False`, Flask `debug=False`. |
| V14.3.3 | Verify that the HTTP headers or any part of the HTTP response do not expose detailed version information of system components. | L1 | Yes | Dynamic Test: Check response headers for `X-Powered-By`, `Server` version strings. Must be suppressed. |

---

## V14.4 — HTTP Security Headers

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V14.4.1 | Verify that every HTTP response contains a Content-Type header. Also specify a safe character set (e.g., UTF-8, ISO-8859-1) if the content types are text/*, /+xml and application/xml. Content must match with the provided Content-Type header. | L1 | Yes | Dynamic Test: Check all API responses for `Content-Type` header with charset specification. |
| V14.4.2 | Verify that all API responses contain a Content-Disposition: attachment; filename="api.json" header (or other appropriate filename for the content type). | L1 | Yes | Dynamic Test: Check API responses for Content-Disposition header to prevent MIME sniffing attacks. |
| V14.4.3 | Verify that a Content Security Policy (CSP) response header is in place that helps mitigate impact for XSS attacks like HTML, DOM, JSON, and JavaScript injection vulnerabilities. | L1 | Yes | Dynamic Test: Check for `Content-Security-Policy` header. Verify it restricts `unsafe-inline` and `unsafe-eval`. |
| V14.4.4 | Verify that all responses contain a X-Content-Type-Options: nosniff header. | L1 | Yes | Dynamic Test: Check all responses for `X-Content-Type-Options: nosniff` header. |
| V14.4.5 | Verify that a Strict-Transport-Security header is included on all responses and for all subdomains, such as Strict-Transport-Security: max-age=15724800; includeSubdomains. | L1 | Yes | Dynamic Test: Check for `Strict-Transport-Security` header with `max-age >= 15724800` and `includeSubdomains`. |
| V14.4.6 | Verify that a suitable Referrer-Policy header is included to avoid exposing sensitive information in the URL through the Referer header to untrusted parties. | L1 | Yes | Dynamic Test: Check for `Referrer-Policy` header (recommended: `strict-origin-when-cross-origin` or `no-referrer`). |
| V14.4.7 | Verify that the content of a web application cannot be embedded in a third-party site by default and that embedding of the exact resources is only allowed where necessary by using suitable Content-Security-Policy: frame-ancestors and X-Frame-Options response headers. | L1 | Yes | Dynamic Test: Check for `X-Frame-Options: DENY` or `SAMEORIGIN`, and/or CSP `frame-ancestors` directive. |

---

## V14.5 — HTTP Request Header Validation

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V14.5.1 | Verify that the application server only accepts the HTTP methods in use by the application/API, including pre-flight OPTIONS, and logs/alerts on any requests that are not valid for the application context. | L1 | Yes | Dynamic Test: Send TRACE, TRACK, and other unusual HTTP methods. Must return 405 Method Not Allowed. |
| V14.5.2 | Verify that the supplied Origin header is not used for authentication or access control decisions, as the Origin header can easily be changed by an attacker. | L1 | Yes | Code Review: Check that Origin header is not used as an authorization mechanism. |
| V14.5.3 | Verify that the Cross-Origin Resource Sharing (CORS) Access-Control-Allow-Origin header uses a strict allowlist of trusted domains and subdomains to match against and does not support the "null" origin. | L1 | Yes | Config Review: Check CORS configuration — must not use `*` for credentialed requests, must not allow `null` origin. |
| V14.5.4 | Verify that HTTP headers added by a trusted proxy or SSO devices, such as a bearer token, are authenticated by the application. | L2 | Yes | Code Review: Check that proxy-supplied headers (X-Forwarded-For, X-Real-IP) are only trusted from known proxy IPs. |
