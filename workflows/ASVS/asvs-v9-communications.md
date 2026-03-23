---
description: "ASVS V9 — Communication Verification Requirements"
asvs_version: "4.0.3"
chapter: "V9"
applicable_phases: "Phase 3 (03d-crypto-communications-audit)"
---

# ASVS V9: Communication Verification Requirements

**Scope:** This chapter ensures that a verified application encrypts all communications, especially when communicating with external services, and uses TLS to protect sensitive data in transit.

---

## V9.1 — Client Communication Security

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V9.1.1 | Verify that TLS is used for all client connectivity, and does not fall back to insecure or unencrypted communications. | L1 | Yes | Dynamic Test: Attempt HTTP connection to the application. Must redirect to HTTPS or refuse connection. |
| V9.1.2 | Verify using up to date TLS testing tools that only strong cipher suites are enabled, with the strongest cipher suites set as preferred. | L1 | Yes | Config/Dynamic Test: Check TLS configuration for enabled cipher suites. Disable weak ciphers (RC4, 3DES, NULL). |
| V9.1.3 | Verify that only the latest recommended versions of the TLS protocol are enabled, such as TLS 1.2 and TLS 1.3. The latest version of the TLS protocol should be the preferred option. | L1 | Yes | Config Review: Check that TLS 1.0 and 1.1 are disabled. TLS 1.2 minimum, TLS 1.3 preferred. |

---

## V9.2 — Server Communication Security

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V9.2.1 | Verify that connections to and from the server use trusted TLS certificates. Where internally generated or self-signed certificates are used, the server must be configured to only trust specific internal CAs and specific self-signed certificates. All others should be rejected. | L2 | Yes | Config Review: Check TLS certificate configuration. Verify certificate chain validation is enabled. |
| V9.2.2 | Verify that encrypted communications such as TLS is used for all inbound and outbound connections, including for management ports, monitoring, authentication, API, or web service calls, database, cloud, serverless, mainframe, external, and partner connections. The server must not fall back to insecure or unencrypted protocols. | L2 | Yes | Config Review: Check ALL connection strings and client configurations for TLS usage. Flag any plaintext connections. |
| V9.2.3 | Verify that all encrypted connections to external systems that involve sensitive information or functions are authenticated. | L2 | Yes | Code Review: Check outbound HTTPS connections validate certificates. Flag `rejectUnauthorized: false` (Node.js) or `verify=False` (Python). |
| V9.2.4 | Verify that proper certification revocation, such as Online Certificate Status Protocol (OCSP) Stapling, is enabled and configured. | L2 | Yes | Config Review: Check for OCSP stapling configuration on the web server. |
| V9.2.5 | Verify that backend TLS connection failures are logged. | L2 | Yes | Code Review: Check that TLS handshake failures on outbound connections are caught and logged. |
