# 08 — Security Design

| | |
|---|---|
| **Document ID** | {{PREFIX}}-SEC-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Security Architecture |
| **Last updated** | {{DATE}} |
| **Audience** | Engineering, security review, compliance |
| **Depends on** | `00-canonical-model.md`, `03-architecture.md` §1, `04-data-model.md`, `05-api-documentation.md`, `07-user-roles-and-permissions.md` |
| **Consumed by** | `09-development-plan.md` §7.7, `13-runbooks.md` §6, `14-admin-guide.md` |

> **Purpose.** Threats, controls and the evidence a reviewer needs. It owns
> the abuse cases, the alert rules and the incident severity classes. It is
> **not** the permission matrix (07) or the runbooks (13). Vocabulary
> follows `00-canonical-model.md`.

---

## Table of Contents

---

## 1. Security Objectives & Compliance

<!-- One paragraph on what the system protects and why a breach matters. -->

| Objective | Statement |
|---|---|
| Confidentiality | |
| Integrity | |
| Authenticity | |
| Availability | |
| Least privilege | |

**Target frameworks**

| Framework | Target | Mapping |
|---|---|---|
| OWASP ASVS 5.0 Level 2 | Design baseline | §1.1 |
| OWASP Top 10 (<edition year>) | No category unresolved | §2 |
| <Regulation, if any> | <safeguards in scope> | §1.2 |

### 1.1 ASVS 5.0 traceability

| ASVS 5.0 chapter | Covers | This document |
|---|---|---|
| V1 Encoding & Sanitization | output encoding, injection | §5 |
| V2 Validation & Business Logic | input validation, workflow abuse | §5, §2.2 |
| V3 Web Frontend Security | CSP, headers, cookies | §7.1–§7.3 |
| V4 API & Web Service | rate limits, CORS, idempotency | §7.4, §7.5 |
| V5 File Handling | uploads, scanning | §5.4 |
| V6 Authentication | passwords, MFA, lockout | §3.1–§3.3, §3.5 |
| V7 Session Management | tokens, rotation, logout | §3.4 |
| V8 Authorization | RBAC/ABAC, deny-by-default, RLS | §4 |
| V9 Self-contained Tokens | JWT handling | §3.4 |
| V10 OAuth & OIDC | federation | N/A — <reason> or § |
| V11 Cryptography | hashing, keys | §6 |
| V12 Secure Communication | TLS | §6.1 |
| V13 Configuration | hardening, secrets | §7.6, §6.4 |
| V14 Data Protection | at rest, retention, disposal | §6 |
| V15 Secure Coding & Architecture | SDLC gates, dependencies | §9 |
| V16 Logging & Error Handling | problem+json, audit, alerts | §8 |
| V17 WebRTC | real-time media | N/A — <reason> or § |

### 1.2 Regulation safeguard map (if a regulation applies)

| Safeguard / clause | Requirement | Control here | Evidence |
|---|---|---|---|

## 2. Threat Model

<!-- This section is the summary a reader of 08 needs. The full STRIDE-per-element model — every element × category rated, owned and disposed, with data-flow diagrams — is produced by the `threat-modeling-stride` skill into `docs/security/threat-model/` once 03, 04, 05, 07 and this document exist. Link its summary on the line below and keep the abuse-case ids (A#) and the boundary names identical in both. -->

Scope: the system in `03-architecture.md` §1. Assets: <list>. Full model: `security/threat-model/threat-model-summary.md` <version, date — or "not yet produced">.

### 2.1 STRIDE per component

<!-- One row per component in 03 §1 (add rows; do not stop at the six defaults). -->

| Component | Spoofing | Tampering | Repudiation | Information disclosure | Denial of service | Elevation of privilege |
|---|---|---|---|---|---|---|
| **Frontend** | | | | | | |
| **API** | | | | | | |
| **Workers** | | | | | | |
| **Database** | | | | | | |
| **Cache / broker** | | | | | | |
| **Object storage** | | | | | | |

### 2.2 Abuse cases (prioritised)

| # | Abuse case | Attack path | Primary controls |
|---|---|---|---|
| A1 | **<name>** | | |

### 2.3 Data flow & trust boundaries

<!-- Name every trust boundary (the threat model's B-n mirror these names) and the flows that cross it. Cite the diagram from security/threat-model/dfd-l1.svg once it exists. -->

| Boundary | Separates | Crossing flows (03 §4/§8, 05 §3) |
|---|---|---|
| Public network ↔ ingress | | |
| Ingress ↔ application network | | |
| Application ↔ data network | | |
| Application ↔ third parties | | |
| Operator plane | | |

## 3. Identity & Authentication

### 3.1 Password storage
### 3.2 Password policy (NIST SP 800-63B aligned; numbers in 00 §10)
### 3.3 MFA and one-time codes
### 3.4 Session model
### 3.5 Lockout & anomaly detection
### 3.6 External principals

## 4. Authorization

<!-- Enforcement point, deny-by-default, 404-on-invisible, row-level security as second layer, field-level layer if 00 §7 defines one, policy object shape. -->

## 5. Input Validation & Output Encoding

### 5.1 General rules
### 5.2 Rich text
### 5.3 Generated documents / templates
### 5.4 File upload validation
### 5.5 Import validation

## 6. Data Protection

### 6.1 In transit
### 6.2 At rest
### 6.3 Key management
### 6.4 Secrets hygiene
### 6.5 Retention & disposal

## 7. Application Hardening

### 7.1 Content Security Policy
### 7.2 Security headers
### 7.3 CORS
### 7.4 Rate limits

| Scope | Limit | Response |
|---|---|---|

### 7.5 Anti-automation & request hygiene
### 7.6 Platform hardening

## 8. Audit Logging & Monitoring

### 8.1 Audit design (append-only, tamper evidence; actions per 07 §9)
### 8.2 What is logged
### 8.3 Alert rules
### 8.4 Retention

## 9. Secure SDLC

### 9.1 CI/CD gates (blocking on default branch)
### 9.2 Process controls
### 9.3 Environment hygiene

## 10. Incident Response

### 10.1 Severity classes

| Class | Definition | Response target |
|---|---|---|
| Sev-1 | | |
| Sev-2 | | |

### 10.2 Containment playbook
### 10.3 Breach notification workflow
### 10.4 Forensics

## 11. Security Acceptance Criteria Checklist

1. <every new endpoint has strict schemas and authorization tests: unauthenticated / wrong role / unassigned 404 / cross-tenant 404 / happy path>

## 12. Open Items

1. <question>? — *default: <default>*.

## 13. References
