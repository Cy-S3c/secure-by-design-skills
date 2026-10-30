# STRIDE per element — what applies where, what to ask, what usually fixes it

STRIDE is applied **per element of the data-flow diagram**, not per
component in prose. Each element type is exposed to a fixed subset of the
six categories (Shostack, *Threat Modeling: Designing for Security*, ch. 3).
A threat model is complete when every required cell of the element ×
category matrix holds at least one threat **or** an explicit
`no_threat` entry with a reason.

| Element type | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External entity (person, browser, third-party system) | ✓ | | ✓ | | | |
| Process (service, worker, function, gateway) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data store (database, bucket, cache, log, queue) | | ✓ | ✓* | ✓ | ✓ | |
| Data flow (request, message, file transfer) | | ✓ | | ✓ | ✓ | |

\* Repudiation is **required** for a store marked `audit: true` (it holds audit or log data) and optional for other stores; the matrix shows *opt* for the optional cells.

## Prompts per category

| Category | Property violated | Ask | Typical findings |
|---|---|---|---|
| **S**poofing | Authenticity | Can a caller pretend to be another principal, host or service? How is identity established on this flow? | missing mutual auth between services; forged webhooks; session fixation; magic links without binding |
| **T**ampering | Integrity | Can data be altered in transit, at rest or in the queue? Is there a check on read? | unsigned job payloads; mass assignment; editable IDs; no hash on stored evidence |
| **R**epudiation | Non-repudiation | Can an actor deny an action? Is the actor, time and before/after state recorded tamper-evidently? | missing audit on state changes; audit rows mutable; shared accounts |
| **I**nformation disclosure | Confidentiality | What leaks through this flow, store or error? Who else can read it? | PII in logs or URLs; IDOR; verbose problem+json; cross-tenant reads; presigned URLs forwarded |
| **D**enial of service | Availability | What exhausts this process or store? What is unbounded? | no rate limit; unbounded page size; zip bombs; render loops; queue flooding |
| **E**levation of privilege | Authorization | Can a lower principal reach a higher capability? Where is the policy decision? | missing object-level check; role change without second approver; policy bypass in an unguarded router |

## Mitigation vocabulary (cite the control, not the wish)

Chapter numbers below are ASVS 5.0; when the project's security design maps
to an older ASVS, cite that edition's chapter instead and say which.

| Category | Control families | Standard refs |
|---|---|---|
| S | MFA, token binding, mTLS between services, signed webhooks (HMAC), nonce + expiry | ASVS 5.0 V6, V7, V9; CWE-287, CWE-290 |
| T | input schemas with `extra=forbid`, signed/hashed payloads, immutable artifacts, integrity on read, `If-Match` | ASVS V2, V5, V14; CWE-345, CWE-915 |
| R | append-only hash-chained audit, actor + trace id on every state change, clock sync | ASVS V16; CWE-778 |
| I | deny-by-default authorization, 404-on-invisible, field-level redaction, encryption at rest, short presign TTL, scrubbed logs | ASVS V8, V11, V14; CWE-200, CWE-639 |
| D | rate limits, size and time budgets, bounded pagination, queue back-pressure, circuit breakers | ASVS V4; CWE-400, CWE-770 |
| E | policy at the service layer, object-level checks, dual control, RLS as second layer, least-privilege DB roles | ASVS V8; CWE-862, CWE-863, CWE-269 |

## Threat record (one per cell finding)

Fields the model file carries for every threat: `id` (`T-<n>`), `target`
(an element or flow id), `category` (S/T/R/I/D/E), `title`, `description` (attacker,
precondition, action, effect), `likelihood` 1–5, `impact` 1–5, `existing`
controls (cite `08-security-design.md` §n or code paths), `mitigation`
(what to add), `status` (`open` · `mitigated` · `accepted` · `transferred`),
`owner`, `refs` (CWE, ASVS chapter, abuse case `A#`), `sprint` (the 09 row that delivers the mitigation) or `plan` (free text:
a BACKLOG item, a ticket) for brownfield. Optional, for the executive brief:
`headline` (a plain-language title, under ~60 characters), `plain` (what could happen, in business terms, one or two sentences), `plain_fix`
(what we recommend, likewise) and `effort` (`S` · `M` · `L`) — expected on every
open Critical/High and on the top open threats. Rating rules:
`references/risk-rating.md`.
