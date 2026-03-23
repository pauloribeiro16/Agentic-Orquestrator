---
description: "ASVS V13 — API and Web Service Verification Requirements"
asvs_version: "4.0.3"
chapter: "V13"
applicable_phases: "Phase 3 (03f-api-graphql-audit)"
---

# ASVS V13: API and Web Service Verification Requirements

**Scope:** This chapter covers API-specific verification for RESTful, GraphQL, SOAP, and generic web services. It focuses on safe data parsing, proper authentication, content-type enforcement, and API-specific abuse prevention.

---

## V13.1 — Generic Web Service Security

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V13.1.1 | Verify that all application components use the same encodings and parsers to avoid parsing attacks that exploit different URI or file parsing behavior that could be used in SSRF and RFI attacks. | L1 | Yes | Code Review: Verify consistent URL/path parsing across all components. Check for double-encoding vulnerabilities. |
| V13.1.2 | Verify that access to administration and management functions is limited to authorized administrators. | L1 | Yes | Dynamic Test: Attempt to access admin API endpoints as a non-admin user. Must return 403. |
| V13.1.3 | Verify that API URLs do not expose sensitive information, such as the API key, session tokens etc. | L1 | Yes | Code Review: Check that tokens and keys are sent in headers or body, never in URL query parameters. |
| V13.1.4 | Verify that authorization decisions are made at both the URI, enforced by programmatic or declarative security at the controller or router, and at the resource level, enforced by model-based permissions. | L2 | Yes | Code Review: Check for both route-level middleware AND resource-level ownership checks in database queries. |
| V13.1.5 | Verify that requests containing unexpected or missing content types are rejected with appropriate headers (HTTP response status 406 Unacceptable or 415 Unsupported Media Type). | L2 | Yes | Dynamic Test: Send request with wrong Content-Type. Verify 406 or 415 response. |

---

## V13.2 — RESTful Web Service

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V13.2.1 | Verify that enabled RESTful HTTP methods are a valid choice for the user or action, such as preventing normal users using DELETE or PUT on protected API or resources. | L1 | Yes | Dynamic Test: Send DELETE/PUT requests as low-privilege user to protected endpoints. Must return 403/405. |
| V13.2.2 | Verify that JSON schema validation is in place and verified before accepting input. | L1 | Yes | Code Review: Check that request bodies are validated against a schema (Zod, Joi, JSON Schema, Pydantic) before business logic. |
| V13.2.3 | Verify that RESTful web services that utilize cookies are protected from Cross-Site Request Forgery via the use of at least one or more of the following: double submit cookie pattern, CSRF nonces, or Origin request header checks. | L1 | Yes | Code Review: If cookies are used for API auth, check for CSRF protection (SameSite, CSRF tokens, Origin header check). |
| V13.2.5 | Verify that REST services explicitly check the incoming Content-Type to be the expected one, such as application/xml or application/json. | L2 | Yes | Dynamic Test: Send JSON endpoint a request with `Content-Type: text/xml`. Must be rejected. |
| V13.2.6 | Verify that the message headers and payload are trustworthy and not modified in transit. Requiring strong encryption for transport (TLS only) may be sufficient in many cases as it provides both confidentiality and integrity protection. Per-message digital signatures can provide additional assurance on top of the transport protections for high-security applications but bring with them additional complexity and risks to weigh against the benefits. | L2 | Yes | Config Review: Verify TLS enforcement on all API endpoints. For high-security: check for request signing. |

---

## V13.3 — SOAP Web Service

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V13.3.1 | Verify that XSD schema validation takes place to ensure a properly formed XML document, followed by validation of each input field before any processing of that data takes place. | L1 | Yes | Code Review: If SOAP/XML is used, check for schema validation before processing. |
| V13.3.2 | Verify that the message payload is signed using WS-Security to ensure reliable transport between client and service. | L2 | Yes | Code Review: If SOAP is used, check for WS-Security message signing. |

---

## V13.4 — GraphQL

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V13.4.1 | Verify that a query allowlist or a combination of depth limiting and amount limiting is used to prevent GraphQL or data layer expression Denial of Service (DoS) as a result of expensive, nested queries. For more advanced scenarios, query cost analysis should be used. | L2 | Yes | Config Review: Check GraphQL server for depth limiting (graphql-depth-limit) and/or complexity analysis (graphql-query-complexity). |
| V13.4.2 | Verify that GraphQL or other data layer authorization logic should be implemented at the business logic layer instead of the GraphQL layer. | L2 | Yes | Code Review: Check that authorization is in resolvers or service layer, not in schema directives alone. |
