---
description: "ASVS V1 — Architecture, Design and Threat Modeling Requirements"
asvs_version: "4.0.3"
chapter: "V1"
applicable_phases: "Phase 1 (Threat Modeling), Phase 2 (Secure Design)"
---

# ASVS V1: Architecture, Design and Threat Modeling

**Scope:** This chapter ensures that a verified application has a sound architecture, design, and threat model. It covers the overall security architecture, authentication, session management, access control, and input/output handling at the DESIGN level — not the implementation level (those are covered in V2–V14).

**Note:** Many V1 requirements are architectural and not directly testable against code. They are assessed by reviewing design documents, architecture diagrams, and threat models. The assessment should verify that the DESIGN addresses these requirements.

---

## V1.1 — Secure Software Development Lifecycle

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.1.1 | Verify the use of a secure software development lifecycle that addresses security in all stages of development. | L2 | No | Review: Confirm a documented SDLC exists that includes security activities (threat modeling, secure coding, testing, review). |
| V1.1.2 | Verify the use of threat modeling for every design change or sprint planning to identify threats, plan for countermeasures, facilitate appropriate risk responses, and guide security testing. | L2 | No | Review: Confirm threat modeling is performed for new features. Check for threat model artifacts. |
| V1.1.3 | Verify that all user stories and features contain functional security constraints, such as "As a user, I should be able to view and edit my profile. I should not be able to view or edit anyone else's profile." | L2 | No | Review: Check user stories/requirements for explicit security acceptance criteria. |
| V1.1.4 | Verify documentation and justification of all the application's trust boundaries, components, and significant data flows. | L2 | No | Review: Confirm architecture documentation includes trust boundaries and data flow diagrams. |
| V1.1.5 | Verify definition and security analysis of the application's high-level architecture and all connected remote services. | L2 | No | Review: Confirm high-level architecture diagram exists with security annotations. |
| V1.1.6 | Verify implementation of centralized, simple (economy of design), vetted, secure, and reusable security controls to avoid duplicate, missing, ineffective, or insecure controls. | L2 | Yes | Code Review: Check for centralized auth middleware, validation utilities, error handlers rather than ad-hoc implementations. |
| V1.1.7 | Verify availability of a secure coding checklist, security requirements, guideline, or policy to all developers and testers. | L2 | No | Review: Confirm secure coding guidelines exist and are accessible to the team. |

---

## V1.2 — Authentication Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.2.1 | Verify the use of unique or special low-privilege operating system accounts for all application components, services, and servers. | L2 | Yes | Config Review: Check Dockerfiles for USER directive, check service account configurations. |
| V1.2.2 | Verify that communications between application components, including APIs, middleware and data layers, are authenticated. Components should have the least necessary privileges needed. | L2 | Yes | Architecture Review: Check inter-service authentication (mTLS, service tokens). |
| V1.2.3 | Verify that the application uses a single vetted authentication mechanism that is known to be secure, can be extended to include strong authentication, and has sufficient logging and monitoring to detect account abuse or breaches. | L2 | Yes | Code Review: Confirm a single, centralized authentication mechanism is used across the application. |
| V1.2.4 | Verify that all authentication pathways and identity management APIs implement consistent authentication security control strength, such that there are no weaker alternatives per the risk of the application. | L2 | Yes | Code Review: Verify all auth pathways (login, API, OAuth, password reset) use the same strength controls. |

---

## V1.4 — Access Control Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.4.1 | Verify that trusted enforcement points such as access control gateways, servers, and serverless functions enforce access controls. Never enforce access controls on the client. | L2 | Yes | Code Review: Confirm all access control is server-side. No client-only permission checks. |
| V1.4.2 | Verify that the chosen access control solution is flexible enough to meet the application's needs. | L2 | No | Architecture Review: Assess if RBAC/ABAC model supports required permission granularity. |
| V1.4.3 | Verify enforcement of the principle of least privilege in functions, data files, URLs, controllers, services, and other resources. This implies protection against spoofing and elevation of privilege. | L2 | Yes | Code Review: Check that each component has only the minimum permissions it needs. |
| V1.4.4 | Verify the application uses a single and well-vetted access control mechanism for accessing protected data and resources. All requests must pass through this single mechanism to avoid copy and paste or insecure alternative paths. | L2 | Yes | Code Review: Confirm centralized authorization middleware, not ad-hoc checks scattered across controllers. |
| V1.4.5 | Verify that attribute or feature-based access control is used whereby the code checks the user's authorization for a feature/data item rather than just their role. Permissions should still be allocated using roles. | L2 | Yes | Code Review: Check that authorization checks verify specific permissions, not just role names. |

---

## V1.5 — Input and Output Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.5.1 | Verify that input and output requirements clearly define how to handle and process data based on type, content, and applicable laws, regulations, and other policy compliance. | L2 | No | Review: Check for documented data handling policies per data type. |
| V1.5.2 | Verify that serialization is not used when communicating with untrusted clients. If this is not possible, ensure that adequate integrity controls (and possibly encryption if sensitive data is sent) are enforced to prevent deserialization attacks including object injection. | L2 | Yes | Code Review: Check for unsafe deserialization of untrusted input. |
| V1.5.3 | Verify that input validation is enforced on a trusted service layer. | L2 | Yes | Code Review: Confirm validation happens server-side, not only client-side. |
| V1.5.4 | Verify that output encoding occurs close to or by the interpreter for which it is intended. | L2 | Yes | Code Review: Check that encoding happens at the point of output, not at input time. |

---

## V1.6 — Cryptographic Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.6.1 | Verify that there is an explicit policy for management of cryptographic keys and that a cryptographic key lifecycle follows a key management standard such as NIST SP 800-57. | L2 | No | Review: Check for documented key management policy. |
| V1.6.2 | Verify that consumers of cryptographic services protect key material and other secrets by using key vaults or API based alternatives. | L2 | Yes | Code Review: Check that keys are loaded from vaults/env vars, not hardcoded. |
| V1.6.3 | Verify that all keys and passwords are replaceable and are part of a well-defined process to re-encrypt sensitive data. | L2 | Yes | Architecture Review: Confirm key rotation mechanism exists. |
| V1.6.4 | Verify that the architecture treats client-side secrets — such as symmetric keys, passwords, or API tokens — as insecure and never uses them to protect or access sensitive data. | L2 | Yes | Code Review: Confirm no security-critical operations rely on client-side secrets alone. |

---

## V1.7 — Errors, Logging and Auditing Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.7.1 | Verify that a common logging format and approach is used across the system. | L2 | Yes | Code Review: Confirm a single logging library and format (structured JSON) is used everywhere. |
| V1.7.2 | Verify that logs are securely transmitted to a preferably remote system for analysis, detection, alerting, and escalation. | L2 | Yes | Config Review: Check log destination configuration (external service, not local only). |

---

## V1.8 — Data Protection and Privacy Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.8.1 | Verify that all sensitive data is identified and classified into protection levels. | L2 | No | Review: Check for data classification documentation. |
| V1.8.2 | Verify that all protection levels have an associated set of protection requirements, such as encryption requirements, integrity requirements, retention, privacy and other confidentiality requirements, and that these are applied in the architecture. | L2 | No | Review: Confirm protection requirements are documented per classification level. |

---

## V1.9 — Communications Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.9.1 | Verify the application encrypts communications between components, particularly when these components are in different containers, systems, sites, or cloud providers. | L2 | Yes | Config Review: Check for TLS on all inter-service communication. |
| V1.9.2 | Verify that application components verify the authenticity of each side in a communication link to prevent person-in-the-middle attacks. For example, application components should validate TLS certificates and chains. | L2 | Yes | Code Review: Check that TLS certificate validation is enabled (no `rejectUnauthorized: false`). |

---

## V1.11 — Business Logic Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.11.1 | Verify the definition and documentation of all application components in terms of the business or security functions they provide. | L2 | No | Review: Check for component documentation with security function descriptions. |
| V1.11.2 | Verify that all high-value business logic flows, including authentication, session management, and access control, do not share unsynchronized state. | L2 | Yes | Code Review: Check for race conditions in critical business logic. |
| V1.11.3 | Verify that all high-value business logic flows, including authentication, session management and access control are thread safe and resistant to time-of-check and time-of-use race conditions. | L2 | Yes | Code Review: Check for TOCTOU vulnerabilities in auth and access control. |

---

## V1.12 — Secure File Upload Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.12.1 | Verify that user-uploaded files are stored outside of the web root. | L2 | Yes | Config Review: Check file upload destination path is not within the web-serving directory. |
| V1.12.2 | Verify that user-uploaded files — if required to be displayed or downloaded from the application — are served by either octet stream downloads, or from an unrelated domain, such as a cloud file storage bucket. | L2 | Yes | Code Review: Check Content-Disposition headers and serving domain for uploaded files. |

---

## V1.14 — Configuration Architecture

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V1.14.1 | Verify the segregation of components of differing trust levels through well-defined security controls, firewall rules, API gateways, reverse proxies, cloud-based security groups, or similar mechanisms. | L2 | Yes | Architecture Review: Check network segmentation and trust boundary enforcement. |
| V1.14.2 | Verify that binary signatures, trusted connections, and verified endpoints are used to deploy binaries to remote devices. | L2 | Yes | Config Review: Check deployment pipeline for artifact signing and verification. |
| V1.14.3 | Verify that the build pipeline warns of out-of-date or insecure components and takes appropriate action. | L2 | Yes | Config Review: Check CI/CD for dependency audit steps (npm audit, pip-audit). |
| V1.14.4 | Verify that the build pipeline contains a build step to automatically build and verify the secure deployment of the application, particularly if the application infrastructure is software defined, such as cloud environment build scripts. | L2 | Yes | Config Review: Check for automated security checks in deployment pipeline. |
| V1.14.5 | Verify that application deployments adequately sandbox, containerize and/or isolate at the network level to delay and deter attackers from attacking other applications, especially when they are performing sensitive or dangerous actions such as deserialization. | L2 | Yes | Config Review: Check container isolation, network policies, and segmentation. |
| V1.14.6 | Verify the application does not use unsupported, insecure, or deprecated client-side technologies such as NSAPI plugins, Flash, Shockwave, ActiveX, Silverlight, NACL, or client-side Java applets. | L2 | Yes | Code Review: Scan for deprecated client-side technologies. |
