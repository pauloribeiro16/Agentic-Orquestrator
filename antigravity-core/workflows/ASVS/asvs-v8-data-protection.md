---
description: "ASVS V8 — Data Protection Verification Requirements"
asvs_version: "4.0.3"
chapter: "V8"
applicable_phases: "Phase 3 (03e-error-logging-audit)"
---

# ASVS V8: Data Protection Verification Requirements

**Scope:** There are three key groups of data that need protection: sensitive data (passwords, credit cards, health records), business data (financial, intellectual property), and data that must be protected per legal/regulatory requirements. This chapter covers data protection at rest and during processing.

---

## V8.1 — General Data Protection

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V8.1.1 | Verify the application protects sensitive data from being cached in server components such as load balancers and application caches. | L2 | Yes | Config Review: Check Cache-Control headers on sensitive endpoints (should include `no-store`, `no-cache`). |
| V8.1.2 | Verify that all cached or temporary copies of sensitive data stored on the server are protected from unauthorized access or purged/invalidated after the authorized user accesses the sensitive data. | L2 | Yes | Code Review: Check that cached sensitive data has TTL and access controls. |
| V8.1.3 | Verify the application minimizes the number of parameters in a request, such as hidden fields, Ajax variables, cookies and header values. | L2 | Yes | Code Review: Check for unnecessary hidden fields or cookies that could be tampered with. |
| V8.1.4 | Verify the application can detect and alert on abnormal numbers of requests, such as by IP, user, total per hour or day, or whatever makes sense for the application. | L2 | Yes | Config Review: Check for request anomaly detection (rate limiting with logging, WAF rules). |
| V8.1.5 | Verify that regular backups of important data are performed and that test restoration of data is performed. | L2 | No | Operations Review: Confirm backup and restore procedures exist and are tested. |
| V8.1.6 | Verify that backups are stored securely to prevent data from being stolen or corrupted. | L2 | No | Operations Review: Confirm backups are encrypted and access-controlled. |

---

## V8.2 — Client-side Data Protection

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V8.2.1 | Verify the application sets sufficient anti-caching headers so that sensitive data is not cached in modern browsers. | L1 | Yes | Dynamic Test: Check response headers on sensitive endpoints for `Cache-Control: no-store`. |
| V8.2.2 | Verify that data stored in browser storage (such as localStorage, sessionStorage, IndexedDB, or cookies) does not contain sensitive data or PII. | L1 | Yes | Code Review: Search frontend code for sensitive data being written to browser storage. |
| V8.2.3 | Verify that authenticated data is cleared from client storage, such as the browser DOM, after the client or session is terminated. | L1 | Yes | Code Review: Check logout handler clears all client-side state (cookies, storage, in-memory data). |

---

## V8.3 — Sensitive Private Data

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V8.3.1 | Verify that sensitive data is sent to the server in the HTTP message body or headers, and that query string parameters from any HTTP verb do not contain sensitive data. | L1 | Yes | Code Review: Check that passwords, tokens, and PII are sent in POST body or headers, never in query strings. |
| V8.3.2 | Verify that users have a method to remove or export their data on demand. | L1 | Yes | Feature Review: Check for data export and account deletion functionality (GDPR compliance). |
| V8.3.3 | Verify that users are provided clear language regarding collection and use of supplied personal information and that users have provided opt-in consent for the use of that data before it is used in any way. | L1 | Yes | UI Review: Check for privacy consent mechanism before data collection. |
| V8.3.4 | Verify that all sensitive data created and processed by the application has been identified, and ensure that a policy is in place on how to deal with sensitive data. | L1 | No | Review: Confirm data classification policy exists and covers all sensitive data in the feature. |
| V8.3.5 | Verify accessing sensitive data is audited (without logging the sensitive data itself), if the data is collected under relevant data protection directives or where logging of access is required. | L2 | Yes | Code Review: Check that access to sensitive data is logged (who accessed, when, what resource) without logging the data values. |
| V8.3.6 | Verify that sensitive information contained in memory is overwritten as soon as it is no longer required to mitigate memory dumping attacks, using zeroes or random data. | L2 | Yes | Code Review: Check that sensitive buffers (passwords, keys) are zeroed after use. In Node.js check `Buffer.fill(0)`. |
| V8.3.7 | Verify that sensitive or private information that is required to be encrypted, is encrypted using approved algorithms that provide both confidentiality and integrity. | L2 | Yes | Code Review: Check that sensitive data encryption uses authenticated encryption (AES-GCM, not just AES-CBC). |
| V8.3.8 | Verify that sensitive personal information is subject to data retention classification, such that old or out of date data is deleted automatically, on a schedule, or as the situation requires. | L2 | Yes | Code/Config Review: Check for data retention policies and automated cleanup of expired sensitive data. |
