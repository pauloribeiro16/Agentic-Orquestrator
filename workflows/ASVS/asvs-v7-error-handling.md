---
description: "ASVS V7 — Error Handling and Logging Verification Requirements"
asvs_version: "4.0.3"
chapter: "V7"
applicable_phases: "Phase 3 (03e-error-logging-audit)"
---

# ASVS V7: Error Handling and Logging Verification Requirements

**Scope:** The primary objective of error handling and logging is to provide useful information for the user, administrators, and incident response teams while not leaking sensitive data.

---

## V7.1 — Log Content

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V7.1.1 | Verify that the application does not log credentials or payment details. Session tokens should only be stored in logs in an irreversible, hashed form. | L1 | Yes | Code Review: Search all log statements for password, token, credit card, or session data. Must be absent or redacted. |
| V7.1.2 | Verify that the application does not log other sensitive data as defined under local privacy laws or relevant security policy. | L1 | Yes | Code Review: Check log statements for PII (email, phone, SSN, address) — must be masked or excluded. |
| V7.1.3 | Verify that the application logs security relevant events including successful and failed authentication events, access control failures, deserialization failures, and input validation failures. | L2 | Yes | Code Review: Verify logging exists for: login success/failure, 403 errors, validation rejections, deserialization errors. |
| V7.1.4 | Verify that each log event includes necessary information that would allow for a detailed investigation of the timeline when an event happens. | L2 | Yes | Code Review: Check log entries contain: timestamp (ISO 8601), event type, actor ID, source IP, resource affected, outcome. |

---

## V7.2 — Log Processing

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V7.2.1 | Verify that all authentication decisions are logged, without storing sensitive session tokens or passwords. This should include requests with relevant metadata needed for security investigations. | L2 | Yes | Code Review: Check auth handler logging — must log decisions with metadata but not credentials. |
| V7.2.2 | Verify that all access control decisions can be logged and all failed decisions are logged. This should include requests with relevant metadata needed for security investigations. | L2 | Yes | Code Review: Check authorization middleware logging — all denials must be logged with request context. |

---

## V7.3 — Log Protection

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V7.3.1 | Verify that all logging components appropriately encode data to prevent log injection. | L2 | Yes | Code Review: Check that user-supplied data is sanitized before logging (strip newlines, encode special chars). |
| V7.3.2 | Verify that all events are protected from injection when viewed in log viewing software. | L2 | Yes | Code Review: Check that log format (JSON structured) prevents injection of fake entries. |
| V7.3.3 | Verify that security logs are protected from unauthorized access and modification. | L2 | Yes | Config Review: Check log file permissions and storage location (outside web root, append-only). |
| V7.3.4 | Verify that time sources are synchronized to the correct time and time zone. Strongly consider logging only in UTC if systems are global to assist with post-incident forensic analysis. | L2 | Yes | Config Review: Check timestamp format in logs — should be UTC ISO 8601. Check NTP configuration. |

---

## V7.4 — Error Handling

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V7.4.1 | Verify that a generic message is shown when an unexpected or security sensitive error occurs, potentially with a unique ID which support personnel can use to investigate. | L1 | Yes | Dynamic Test: Trigger an error (malformed request, division by zero). Check response for generic message with correlation ID. No stack trace. |
| V7.4.2 | Verify that exception handling (or a functional equivalent) is used across the codebase to account for expected and unexpected error conditions. | L1 | Yes | Code Review: Verify global error handler exists. Check critical paths have try/catch or error middleware. |
| V7.4.3 | Verify that a "last resort" error handler is defined which will catch all unhandled exceptions. | L1 | Yes | Code Review: Check for `process.on('uncaughtException')` / `process.on('unhandledRejection')` (Node.js) or equivalent global handler. |
