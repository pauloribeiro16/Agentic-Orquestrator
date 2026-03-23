---
description: "ASVS V2 — Authentication Verification Requirements"
asvs_version: "4.0.3"
chapter: "V2"
applicable_phases: "Phase 3 (03a-auth-session-audit)"
---

# ASVS V2: Authentication Verification Requirements

**Scope:** This chapter covers verification of authentication mechanisms including password policies, credential storage, credential recovery, session-based and token-based authentication, and defense against automated attacks.

---

## V2.1 — Password Security

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.1.1 | Verify that user set passwords are at least 12 characters in length (after multiple spaces are combined). | L1 | Yes | Dynamic Test: Attempt registration with passwords < 12 chars. Expect rejection. |
| V2.1.2 | Verify that passwords of at least 64 characters are permitted, and that passwords of more than 128 characters are denied. | L1 | Yes | Dynamic Test: Submit 64-char and 129-char passwords. 64 accepted, 129 rejected. |
| V2.1.3 | Verify that password truncation is not performed. However, consecutive multiple spaces may be replaced by a single space. | L1 | Yes | Dynamic Test: Set password with trailing characters, verify all are stored/checked. |
| V2.1.4 | Verify that any printable Unicode character, including language neutral characters such as spaces and Emojis are permitted in passwords. | L1 | Yes | Dynamic Test: Set password with Unicode, spaces, emojis. Verify they are accepted and work on login. |
| V2.1.5 | Verify users can change their password. | L1 | Yes | Dynamic Test: Use password change endpoint. Verify success. |
| V2.1.6 | Verify that password change functionality requires the user's current and new password. | L1 | Yes | Dynamic Test: Attempt password change without current password. Expect rejection. |
| V2.1.7 | Verify that passwords submitted during account registration, login, and password change are checked against a set of breached passwords either locally (such as the top 1,000 or 10,000 most common passwords which match the system's password policy) or using an external API. If using an API, a zero knowledge proof or other mechanism should be used to ensure that the plain text password is not sent or used in verifying the breach status of the password. If the password is breached, the application must require the user to set a new non-breached password. | L1 | Yes | Dynamic Test: Attempt to set a known breached password (e.g., "password123456"). Expect rejection. |
| V2.1.8 | Verify that a password strength meter is provided to help users set a stronger password. | L1 | Yes | UI Review: Check registration/password change forms for strength meter component. |
| V2.1.9 | Verify that there are no password composition rules limiting the type of characters permitted. There should be no requirement for upper or lower case or numbers or special characters. | L1 | Yes | Dynamic Test: Set password using only lowercase letters (12+ chars). Verify acceptance. |
| V2.1.10 | Verify that there are no periodic credential rotation or password history requirements. | L1 | Yes | Config Review: Check for forced password rotation policies. Should not exist. |
| V2.1.11 | Verify that "paste" functionality, browser password helpers, and external password managers are permitted. | L1 | Yes | UI Review: Check for `autocomplete="off"` or paste-blocking JavaScript on password fields. Should not be present. |
| V2.1.12 | Verify that the user can choose to either temporarily view the entire masked password, or temporarily view the last typed character of the password on platforms that do not have this as built-in functionality. | L1 | Yes | UI Review: Check for password visibility toggle. |

---

## V2.2 — General Authenticator Security

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.2.1 | Verify that anti-automation controls are effective at mitigating breached credential testing, brute force, and account lockout attacks. Such controls include blocking the most common breached passwords, soft lockouts, rate limiting, CAPTCHA, ever increasing delays between attempts, IP address restrictions, or risk-based restrictions such as location, first login on a device, recent attempts to unlock the account, or similar. Verify that no more than 100 failed attempts per hour is possible on a single account. | L1 | Yes | Dynamic Test: Send 101 failed login attempts for a single account within an hour. Verify blocking occurs. |
| V2.2.2 | Verify that the use of weak authenticators (such as SMS and email) is limited to secondary verification and transaction approval and not as a replacement for more secure authentication methods. Verify that stronger methods are offered before weak methods, users are aware of the risks, or that proper measures are in place to limit the risks of account compromise. | L2 | Yes | Code Review: Check if SMS/email is the sole authentication factor. Should be supplementary only. |
| V2.2.3 | Verify that secure notifications are sent to users after updates to authentication details, such as credential resets, email or address changes, logging in from unknown or risky locations. The use of push notifications — rather than SMS or email — is preferred, but in the absence of push notifications, SMS or email is acceptable as long as no sensitive information is disclosed in the notification. | L1 | Yes | Dynamic Test: Trigger a password change and verify notification is sent. Check notification content for sensitive data. |
| V2.2.4 | Verify impersonation resistance against phishing, such as the use of multi-factor authentication, cryptographic devices with intent (such as connected keys with a push to authenticate), or at higher AAL levels, client-side certificates. | L3 | — | L3 only — out of scope for Level 2 audit. |
| V2.2.5 | Verify that where a Credential Service Provider (CSP) and the application verifying authentication are separated, mutually authenticated TLS is in place between the two endpoints. | L2 | Yes | Config Review: Check TLS configuration between auth service and application. |
| V2.2.6 | Verify replay resistance through the mandated use of One-time Passwords (OTP) devices, cryptographic authenticators, or lookup codes. | L2 | Yes | Code Review: Check that tokens/codes are single-use and invalidated after use. |
| V2.2.7 | Verify intent to authenticate by requiring the entry of an OTP token or user-initiated action such as a button press on a FIDO hardware key. | L2 | Yes | Code Review: Check MFA implementation requires explicit user action. |

---

## V2.3 — Authenticator Lifecycle

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.3.1 | Verify system generated initial passwords or activation codes SHOULD be securely randomly generated, SHOULD be at least 6 characters long, and MAY contain letters and numbers, and expire after a short period of time. These initial secrets must not be permitted to become the long term password. | L1 | Yes | Code Review: Check initial password generation for entropy and expiration. |
| V2.3.2 | Verify that enrollment and use of subscriber-provided authentication devices are supported, such as a U2F or FIDO tokens. | L2 | Yes | Feature Review: Check for WebAuthn/FIDO2 registration and authentication support. |
| V2.3.3 | Verify that renewal instructions are sent with sufficient time to renew time bound authenticators. | L2 | Yes | Code Review: Check expiration notification logic for time-bound tokens/certificates. |

---

## V2.4 — Credential Storage

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.4.1 | Verify that passwords are stored in a form that is resistant to offline attacks. Passwords SHALL be salted and hashed using an approved one-way key derivation or password hashing function. Key derivation and password hashing functions take a password, a salt, and a cost factor as inputs when generating a password hash. | L2 | Yes | Code Review: Check password hashing implementation for approved algorithm with salt and cost factor. |
| V2.4.2 | Verify that the salt is at least 32 bits in length and be arbitrarily chosen to minimize salt value collisions among stored hashes. For each credential, a unique salt value and the resulting hash SHALL be stored. | L2 | Yes | Code Review: Check salt generation — must be unique per credential, at least 32 bits. |
| V2.4.3 | Verify that if PBKDF2 is used, the iteration count SHOULD be as large as verification server performance will allow, typically at least 310,000 iterations. | L2 | Yes | Code Review: Check PBKDF2 iteration count if used. |
| V2.4.4 | Verify that if bcrypt is used, the work factor SHOULD be as large as verification server performance will allow, with a minimum of 10. | L2 | Yes | Code Review: Check bcrypt cost/rounds parameter. Must be ≥ 10. |
| V2.4.5 | Verify that an additional iteration of a key derivation function is performed, using a salt value that is secret and known only to the verifier. Generate the salt value using an approved random bit generator [SP 800-90Ar1] and provide at least the minimum security strength specified in the latest revision of SP 800-131A. The secret salt value SHALL be stored separately from the hashed passwords (e.g., in a specialized device like a hardware security module). | L2 | Yes | Code Review: Check for pepper/secret salt stored separately from password hashes. |

---

## V2.5 — Credential Recovery

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.5.1 | Verify that a system generated initial activation or recovery secret is not sent in clear text to the user. | L1 | Yes | Dynamic Test: Trigger password recovery. Verify the secret is not in the HTTP response body. |
| V2.5.2 | Verify password hints or knowledge-based authentication (so-called "secret questions") are not present. | L1 | Yes | UI/Code Review: Check for security questions in recovery flow. Must not exist. |
| V2.5.3 | Verify password credential recovery does not reveal the current password in any way. | L1 | Yes | Dynamic Test: Trigger recovery for existing and non-existing accounts. Responses must be identical. |
| V2.5.4 | Verify shared or default accounts are not present (e.g., "root", "admin", or "sa"). | L1 | Yes | Code/Config Review: Search for default credentials in code and database seeds. |
| V2.5.5 | Verify that if an authentication factor is changed or replaced, that the user is notified of this event. | L1 | Yes | Dynamic Test: Change password. Verify notification sent to user. |
| V2.5.6 | Verify forgotten password, and other recovery paths use a secure recovery mechanism, such as time-based OTP (TOTP) or other soft token, mobile push, or another offline recovery mechanism. | L1 | Yes | Code Review: Check recovery mechanism uses secure token, not knowledge-based. |
| V2.5.7 | Verify that if OTP or multi-factor authentication factors are lost, that evidence of identity proofing is performed at the same level as during enrollment. | L2 | Yes | Code Review: Check MFA recovery flow for identity verification requirements. |

---

## V2.6 — Look-up Secret Verifier

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.6.1 | Verify that lookup secrets can be used only once. | L2 | Yes | Dynamic Test: Use a backup/recovery code twice. Second use must fail. |
| V2.6.2 | Verify that lookup secrets have sufficient randomness (112 bits of entropy), or if less than 112 bits of entropy, salted with a unique and random 32-bit salt and hashed with an approved one-way hash. | L2 | Yes | Code Review: Check backup code generation for entropy. |
| V2.6.3 | Verify that lookup secrets are resistant to offline attacks, such as predictable values. | L2 | Yes | Code Review: Verify backup codes use CSPRNG, not sequential or predictable values. |

---

## V2.7 — Out of Band Verifier

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.7.1 | Verify that clear text out of band (NIST "restricted") authenticators, such as SMS or PSTN, are not offered by default, and stronger alternatives such as push notifications are offered first. | L1 | Yes | UI Review: Check MFA setup flow — push/TOTP should be offered before SMS. |
| V2.7.2 | Verify that the out of band verifier expires out of band authentication requests, codes, or tokens after 10 minutes. | L1 | Yes | Dynamic Test: Request OOB code, wait 11 minutes, attempt to use it. Must fail. |
| V2.7.3 | Verify that the out of band verifier authentication requests, codes, or tokens are only usable once, and only for the original authentication request. | L1 | Yes | Dynamic Test: Use OOB code once, attempt reuse. Must fail. |
| V2.7.4 | Verify that the out of band authenticator and verifier communicates over a secure independent channel. | L1 | Yes | Code Review: Check that OOB channel (email, SMS) is separate from primary auth channel. |
| V2.7.5 | Verify that the out of band verifier retains only a hashed version of the authentication code. | L2 | Yes | Code Review: Check that OTP/OOB codes are stored hashed, not in plaintext. |
| V2.7.6 | Verify that the initial authentication code is generated by a secure random number generator, containing at least 20 bits of entropy (typically a six digital random number is sufficient). | L2 | Yes | Code Review: Check OTP generation uses CSPRNG with sufficient entropy. |

---

## V2.8 — One-Time Verifier

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.8.1 | Verify that time-based OTPs have a defined lifetime before expiring. | L1 | Yes | Code Review: Check TOTP configuration for step/window size. |
| V2.8.2 | Verify that symmetric keys used to verify submitted OTPs are highly protected, such as by using a hardware security module or secure operating system based key storage. | L2 | Yes | Code Review: Check where TOTP seed secrets are stored. Must be encrypted at rest. |
| V2.8.3 | Verify that approved cryptographic algorithms are used in the generation, seeding, and verification. | L2 | Yes | Code Review: Check TOTP implementation uses HMAC-SHA1/SHA256/SHA512 as per RFC 6238. |
| V2.8.4 | Verify that time-based OTP can be used only once within the validity period. | L2 | Yes | Dynamic Test: Use a TOTP code, immediately reuse it. Must fail on second attempt. |
| V2.8.5 | Verify that if a time-based multi-factor OTP token is re-used during the validity period, it is logged. | L2 | Yes | Code Review: Check logging for TOTP replay attempts. |
| V2.8.6 | Verify physical single-factor OTP generator can be revoked in case of theft or other loss. Ensure that revocation is immediately effective across logged in sessions, regardless of location. | L2 | Yes | Code Review: Check OTP device revocation flow and session invalidation. |
| V2.8.7 | Verify that biometric authenticators are limited to use only as secondary factors in conjunction with either something you have and something you know. | L2 | Yes | Code Review: Verify biometrics are never the sole authentication factor. |

---

## V2.9 — Cryptographic Verifier

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.9.1 | Verify that cryptographic keys used in verification are stored securely and protected against disclosure, such as using a Trusted Platform Module (TPM) or Hardware Security Module (HSM), or an OS service that can use this secure storage. | L2 | Yes | Config Review: Check key storage mechanism for cryptographic verifiers. |
| V2.9.2 | Verify that the challenge nonce is at least 64 bits in length, and statistically unique or unique over the lifetime of the cryptographic device. | L2 | Yes | Code Review: Check nonce generation length and uniqueness. |
| V2.9.3 | Verify that approved cryptographic algorithms are used in the generation, seeding, and verification. | L2 | Yes | Code Review: Check algorithms used in cryptographic authentication. |

---

## V2.10 — Service Authentication

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V2.10.1 | Verify that intra-service secrets do not rely on unchanging credentials such as passwords, API keys or shared accounts with privileged access. | L2 | Yes | Code/Config Review: Check inter-service auth uses rotating credentials, not static keys. |
| V2.10.2 | Verify that if passwords are required for service authentication, the service account used is not a default credential (e.g., root/root or admin/admin are default in some services during installation). | L2 | Yes | Config Review: Check for default credentials in service configurations. |
| V2.10.3 | Verify that passwords are stored with sufficient protection to prevent offline recovery attacks, including local system access. | L2 | Yes | Config Review: Check service account password storage (hashed, not plaintext config). |
| V2.10.4 | Verify passwords, integrations with databases and third-party systems, seeds and internal secrets, and API keys are managed securely and not included in the source code or stored within source code repositories. Such storage SHOULD resist offline attacks. The use of a secure software key store (L1), hardware TPM, or an HSM (L3) is recommended for password storage. | L2 | Yes | Code Review: Scan source code for hardcoded credentials. Check for secrets manager integration. |
