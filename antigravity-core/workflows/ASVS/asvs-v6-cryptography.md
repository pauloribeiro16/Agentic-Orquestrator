---
description: "ASVS V6 — Stored Cryptography Verification Requirements"
asvs_version: "4.0.3"
chapter: "V6"
applicable_phases: "Phase 3 (03d-crypto-communications-audit)"
---

# ASVS V6: Stored Cryptography Verification Requirements

**Scope:** This chapter ensures that a verified application uses strong cryptographic algorithms, proper key management, and sufficient random number generation.

---

## V6.1 — Data Classification

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V6.1.1 | Verify that regulated private data is stored encrypted while at rest, such as Personally Identifiable Information (PII), sensitive personal information, or data assessed likely to be subject to EU's GDPR. | L2 | Yes | Code/Config Review: Check that PII and sensitive fields are encrypted in the database. |
| V6.1.2 | Verify that regulated health data is stored encrypted while at rest, such as medical records, medical device details, or de-anonymized research records. | L2 | Yes | Code/Config Review: Check encryption of health-related data at rest. |
| V6.1.3 | Verify that regulated financial data is stored encrypted while at rest, such as financial accounts, defaults or credit history, tax records, pay history, beneficiaries, or de-anonymized market or research records. | L2 | Yes | Code/Config Review: Check encryption of financial data at rest. |

---

## V6.2 — Algorithms

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V6.2.1 | Verify that all cryptographic modules fail securely, and errors are handled in a way that does not enable Padding Oracle attacks. | L1 | Yes | Code Review: Check error handling in encryption/decryption — errors must be generic, not revealing padding status. |
| V6.2.2 | Verify that industry proven or government approved cryptographic algorithms, modes, and libraries are used, instead of custom coded cryptography. | L2 | Yes | Code Review: Check that only standard library implementations are used (Node.js `crypto`, Python `cryptography`). No hand-rolled crypto. |
| V6.2.3 | Verify that encryption initialization vector, cipher configuration, and block modes are configured securely using the latest advice. | L2 | Yes | Code Review: Check IV generation (random per operation), cipher mode (prefer GCM over CBC), no ECB mode. |
| V6.2.4 | Verify that random number, encryption or hashing algorithms, key lengths, rounds, ciphers or modes, can be reconfigured, upgraded, or swapped at any time, to protect against cryptographic breaks. | L2 | Yes | Architecture Review: Check if crypto parameters are configurable, not hardcoded throughout the codebase. |
| V6.2.5 | Verify that known insecure block modes (i.e., ECB, etc.), padding modes (i.e., PKCS#1 v1.5, etc.), ciphers with small block sizes (i.e., Triple-DES, Blowfish, etc.), and weak hashing algorithms (i.e., MD5, SHA1, etc.) are not used unless required for backwards compatibility. | L2 | Yes | Code Review: Search for MD5, SHA1, DES, 3DES, RC4, ECB mode. Flag all instances. |
| V6.2.6 | Verify that nonces, initialization vectors, and other single use numbers must not be used more than once with a given encryption key. The method of generation must be appropriate for the algorithm being used. | L2 | Yes | Code Review: Check that IVs/nonces are generated fresh per operation, not reused. |
| V6.2.7 | Verify that encrypted data is authenticated via signatures, authenticated cipher modes, or HMAC to ensure that ciphertext is not altered by an unauthorized party. | L2 | Yes | Code Review: Check for authenticated encryption (AES-GCM, ChaCha20-Poly1305) or separate HMAC verification. |
| V6.2.8 | Verify that all cryptographic operations are constant-time, with no 'short-circuit' operations in comparisons, calculations, or returns, to avoid leaking information. | L2 | Yes | Code Review: Check for timing-safe comparison functions (`crypto.timingSafeEqual`, `hmac.compare_digest`). |

---

## V6.3 — Random Values

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V6.3.1 | Verify that all random numbers, random file names, random GUIDs, and random strings are generated using the cryptographic module's approved cryptographically secure random number generator when these random values are intended to be not guessable by an attacker. | L2 | Yes | Code Review: Check that `crypto.randomBytes()` (Node.js) or `secrets.token_bytes()` (Python) is used. Flag `Math.random()` or `random.random()`. |
| V6.3.2 | Verify that random GUIDs are created using the GUID v4 algorithm, and a Cryptographically-secure Pseudo-Random Number Generator (CSPRNG). GUIDs created using other pseudo-random number generators may be predictable. | L2 | Yes | Code Review: Check UUID generation uses `crypto.randomUUID()` or equivalent CSPRNG-backed function. |
| V6.3.3 | Verify that random numbers are created with proper entropy even when the application is under heavy load, or that the application degrades gracefully in such circumstances. | L2 | Yes | Code Review: Verify CSPRNG is used (OS-level entropy), not application-level seeded PRNG. |

---

## V6.4 — Secret Management

| ID | Requirement | Level | Verifiable | Test Approach |
|---|---|---|---|---|
| V6.4.1 | Verify that a secrets management solution such as a key vault is used to securely create, store, control access to and destroy secrets. | L2 | Yes | Config Review: Check for secrets manager integration (env vars minimum, vault preferred). |
| V6.4.2 | Verify that key material is not exposed to the application but instead uses an isolated security module like a vault for cryptographic operations. | L2 | Yes | Architecture Review: Check that application code does not directly handle raw key material where avoidable. |
