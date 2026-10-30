# Standards Map — what each document borrows from industry practice

Cite the standard in the document's purpose block or relevant section; take
the specific practice listed, not the whole standard. Verify version numbers
and clause references against the current publication before citing them.

| Doc | Standard / practice | What to take from it |
|---|---|---|
| 00 | Domain-Driven Design *ubiquitous language*; RFC 2119 keywords; RFC 3339 timestamps; RFC 9562 UUID v7 | One vocabulary shared by docs and code; enum names identical in DB, API, UI; time-ordered non-guessable IDs; a parameter register so numbers live once |
| 01 | PRD practice (goals / non-goals / metrics); personas; Nygard ADRs | Measurable goals with target and horizon; explicit non-goals as a scope-creep defence; condensed ADR table with rationale and a link to the full record |
| 07 | NIST RBAC model (ANSI INCITS 359); NIST SP 800-162 (ABAC); least privilege; separation of duties (maker–checker, dual control); zero standing access with break-glass | Global role as capability class + attribute scope on objects; deny-by-default; SoD rules as invariants; time-boxed, audited privileged access |
| 10 | Whatever standard governs the domain (CVSS 4.0, FHIR, a published template corpus, a messaging regulation) | Derive the specification from a catalogued corpus or the published rules; version it as a standard with its own ID; gate it on pilot validation when greenfield |
| 06 | ISO/IEC/IEEE 29148:2018; BDD Given/When/Then (Gherkin); requirements traceability matrix | Atomic, verifiable, uniquely identified requirements; acceptance criteria per feature; FR → sprint traceability |
| 04 | ERD (crow's foot / Mermaid `erDiagram`); normalisation; expand–contract migrations; PostgreSQL row-level security; GDPR Art. 5(1)(e) storage limitation | Principles table; composite tenant foreign keys; partial unique indexes under soft delete; per-entity retention and erasure; migration conventions |
| 05 | OpenAPI 3.1; RFC 9457 Problem Details (obsoletes RFC 7807); RFC 9110 (412 Precondition Failed, ETag / If-Match); RFC 6585 (428 Precondition Required); IETF `Idempotency-Key` header draft (400 when the key is missing, 422 on reuse with a different payload); RFC 8594 `Sunset`; semantic versioning; HMAC-signed webhooks | Conventions section; stable error `type` catalogue (409 state/duplicate, 412 precondition failed, 422 validation and idempotency mismatch, 428 precondition required, 400 missing key); idempotent mutations; no personal data in query strings (search as POST); `x-permission` / `x-scope` per operation; event envelope defined once |
| 03 | C4 model; arc42; ISO/IEC/IEEE 42010:2022; Twelve-Factor App; OpenTelemetry; SRE SLOs | Context/container/component views; module catalogue with events; config via environment; traces/logs/metrics and an SLO table |
| 08 | OWASP ASVS 5.0 (Level 2 default target; 5.0 chapters: V1 Encoding & Sanitization, V2 Validation & Business Logic, V3 Web Frontend, V4 API & Web Service, V5 File Handling, V6 Authentication, V7 Session Management, V8 Authorization, V9 Self-contained Tokens, V10 OAuth/OIDC, V11 Cryptography, V12 Secure Communication, V13 Configuration, V14 Data Protection, V15 Secure Coding & Architecture, V16 Logging & Error Handling, V17 WebRTC); OWASP Top 10 (cite the edition year); STRIDE; NIST SP 800-63B; NIST SP 800-218 SSDF; NIST CSF 2.0; ISO/IEC 27001:2022 Annex A; SOC 2 TSC; CSP Level 3; regulation as applicable (GDPR, HIPAA Security Rule safeguards 45 CFR 164.308 / .310 / .312, PCI DSS) | Objectives + framework traceability using current chapter names; a safeguard-by-safeguard regulation map; STRIDE per component; prioritised abuse cases; authenticator policy numbers; SDLC gates; severity classes; release acceptance checklist |
| 09 | Scrum (sprint, DoR, DoD); RACI; PMBOK-style risk register; trunk-based development; Conventional Commits; semantic versioning; test pyramid; WCAG 2.2 AA; change control | Binding phase mapping; numbered backlog per sprint with FR links and demo/exit; milestone table with dates; reserve; quality strategy; CR process with version bumps |
| 11 | W3C Design Tokens Community Group format; WCAG 2.2 AA (incl. 2.2.1 timing adjustable); component anatomy (shadcn/Radix-style primitives) | Token naming; reserved semantic palettes; contrast targets; per-component anatomy and states; time limits with extension controls |
| 12 | Screen-contract practice: states (loading/empty/error), keyboard maps, responsive matrices | Six-block screen format; appendices for shared copy and keys |
| 02, 14, 15 | Diátaxis (tutorial / how-to / reference / explanation); Google & Microsoft developer style guides | Task-based how-tos per module; FAQ; glossary pointing to 00; second person, present tense, one action per step |
| 13 | Google SRE runbook practice; incident severity classes; tested backup/restore; on-call and escalation | Every command verified against the repo once code exists; what is lost per store on restore; rotation procedures; alert-worthy events; rota and escalation paths |
| README | Document control practice (status banner, version, review order, sign-off) | Status banner at the top; decisions-needed list; post-approval next step |

## Numbers worth standardising on (defaults; record the chosen values in 00 §10)

| Area | Default in a new suite | Source |
|---|---|---|
| Password minimum | 12 characters, breach-corpus check, no forced rotation | NIST SP 800-63B |
| MFA | TOTP mandatory for privileged roles; recovery codes single-use, hashed | ASVS 5.0 V6 |
| Session | short-lived access token (≈15 min) + rotating refresh with reuse detection; inactivity time-out for sensitive data (≈15 min) | ASVS 5.0 V7; HIPAA 164.312(a)(2)(iii) auto-logoff (addressable) |
| Lockout | 5 failures → 15-minute lock, generic error (no enumeration) | ASVS 5.0 V6 |
| One-time codes and magic links | OTP valid ≤ 10 minutes, single use, ≤ 5 attempts; magic link single use, short expiry, bound to the requesting channel | NIST SP 800-63B (out-of-band / look-up secrets) |
| Errors | `application/problem+json` with `type`, `title`, `status`, `detail`, `instance`, `trace_id`; 409 state/duplicate, 412 precondition failed, 422 validation and idempotency mismatch, 428 precondition required, 400 missing idempotency key | RFC 9457, RFC 9110, RFC 6585, IETF idempotency draft |
| Pagination | cursor-based, `{data, next_cursor}` envelope | API practice |
| Accessibility | WCAG 2.2 AA, keyboard-complete, axe-clean in CI; user-adjustable time limits | WCAG 2.2 |
| Coverage gate | ≥ 80 % on changed service layer; regression test per bug fix | team DoD |
| Sprint | 2 weeks, demo/exit statement per sprint, ≥ 10 % reserve | Scrum |

Regulated-domain additions (confirm with counsel before adopting):

| Area | Default | Source |
|---|---|---|
| Security documentation retention | 6 years from creation or last effective date | HIPAA 45 CFR 164.316(b)(2) |
| Individual access requests | respond within 30 days (one 30-day extension) | HIPAA 45 CFR 164.524 |
| Personal data in logs, URLs, analytics | never; identifiers only | HIPAA minimum necessary; GDPR data minimisation |
| Breach notification | per the regulation's clock (HIPAA: without unreasonable delay, ≤ 60 days; GDPR: 72 hours to the authority) | HIPAA 164.404; GDPR Art. 33 |
