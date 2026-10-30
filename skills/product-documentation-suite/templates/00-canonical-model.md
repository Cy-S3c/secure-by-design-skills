# 00 — Canonical Model (Source of Truth)

| | |
|---|---|
| **Document ID** | {{PREFIX}}-CANON-001 |
| **Product** | {{PRODUCT}} (working codename `{{CODENAME}}`) |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Product & Engineering |
| **Last updated** | {{DATE}} |
| **Audience** | All documentation authors, architects, developers, QA |
| **Depends on** | — |
| **Consumed by** | every other document in the suite |

> **Purpose.** The single source of truth for naming, roles, entities,
> enumerations, state machines, conventions and shared parameters. Every other
> document MUST use the vocabulary defined here; a term not defined here does
> not exist until it is added. It is **not** the place for requirements
> (`06-features-and-functions.md`), permissions (`07-user-roles-and-permissions.md`)
> or physical schema (`04-data-model.md`).

---

## 1. Product Identity

| Attribute | Value |
|---|---|
| Product name | {{PRODUCT}} |
| Codename / package prefix | `{{CODENAME}}` |
| Category | <e.g. B2B SaaS, internal platform, mobile app> |
| Tenancy model | <single-tenant per instance / multi-tenant; tenant entity name> |
| Deployment model | <self-hosted / cloud / hybrid> |
| Primary users | <two or three groups> |
| Release phases | see `01-product-design-document.md` §6 (owner of phases and exit criteria) |

## 2. User Roles (closed set)

<!-- Enum names are used verbatim in DB, API, UI and every document. -->

| # | Role (enum) | Display name | Tier |
|---|---|---|---|
| 1 | `ROLE_A` | <display> | <trainee / delivery / management / platform> |
| 2 | `ROLE_B` | <display> | |

Rules:
- Every user has **exactly one global role** (RBAC baseline).
- <Which roles are platform-scope; which act within assignment scope (ABAC, §7).>
- <Which roles hold approval authority; which have zero standing access and use break-glass.>
- Full permission matrix lives in `07-user-roles-and-permissions.md` §4.

### 2.1 External principal types (not users)

| Principal | Definition | Authentication | Scope |
|---|---|---|---|
| `EXTERNAL_X` | <who they are; they are not a `User` and hold no global role> | <separate login surface / token> | <what they can see> |

<!-- If objects carry per-object positions (owner, reviewer, approver), add a positions table: Position | Eligible roles | Notes. -->

## 3. Core Domain Entities

| Entity | Definition | Owned by | Lifecycle | Key relationships |
|---|---|---|---|---|
| `Tenant` | <definition> | platform | §4.2 | has many `User` |
| `User` | <definition> | `Tenant` | invited → active → suspended → anonymized | has one role (§2) |
| `<Entity>` | | | | |

## 4. Enumerations & State Machines

### 4.1 Simple enumerations

| Enum (`Entity.field`) | Values | Notes |
|---|---|---|
| `Entity.kind` | `VALUE_ONE`, `VALUE_TWO` | |

### 4.2 `<Entity>.status` (state machine)

```
DRAFT ──submit──▶ IN_REVIEW ──approve──▶ APPROVED ──publish──▶ PUBLISHED
  ▲                  │ request changes
  └──────────────────┘
```

| Transition | From → To | Triggered by | Precondition | Side effects |
|---|---|---|---|---|
| submit | `DRAFT` → `IN_REVIEW` | <role / position> | <validation> | <audit event, notification> |

- <What is immutable once reached; how versions bump on edits after that.>

<!-- One subsection per state machine; simple three-state lifecycles may be a single bullet under 4.1. -->

## 5. Tech Stack (locked)

| Layer | Choice | Version | Notes |
|---|---|---|---|
| Frontend | | | |
| Backend | | | |
| Database | | | |
| Cache / queue | | | |
| Object storage | | | |
| Runtime / orchestration | | | <if decided in 03 §9.2, cite it> |
| Auth | | | |
| Observability | | | |

## 6. API Conventions

- Base URL `/api/v1`; external surfaces (portal, partner) under their own prefix.
- Resource naming: plural kebab-case paths; IDs UUID v7, sequential IDs never exposed.
- Tenancy: tenant scope comes from the session, never from the URL or body.
- Field naming `snake_case`; timestamps RFC 3339 UTC instants; wall-clock values carry an IANA time zone; date-only fields are `YYYY-MM-DD`.
- Pagination: cursor-based, envelope `{ "data": [...], "next_cursor": "..." }`.
- Concurrency: `ETag` / `If-Match` on mutable resources (412 on mismatch).
- Errors: RFC 9457 `application/problem+json` with `trace_id`.
- Mutations require `Idempotency-Key`; every state change emits an audit event.
- Personal or sensitive data never appears in URLs or query strings (search is a POST).
- Versioning: URL major version; deprecation via `Sunset` header.

## 7. Authorization Model (summary)

1. **RBAC baseline** — global role defines capability classes.
2. **ABAC scope** — object-level capabilities apply only to assigned / owned / tenant objects.
3. **Deny-by-default** — both layers asserted per service method; 404 (not 403) for non-visible objects.
4. <Field-level layer, if any: which fields are hidden per role and where it is enforced.>
5. <External principal types are separate principal types with their own policy.>

## 8. Document ID Register

| Document | File | Document ID |
|---|---|---|
| Canonical model | `00-canonical-model.md` | {{PREFIX}}-CANON-001 |
| Product design | `01-product-design-document.md` | {{PREFIX}}-PDD-001 |
| … | | |

The suite index with sizes and status is `README.md`.

## 9. Glossary

| Term | Definition |
|---|---|
| **<Term>** | <definition> |

## 10. Parameter Register

<!-- Every numeric limit, timeout, retention period or default that more than one document uses. Other documents cite `00 §10 PRM-n`. -->

| ID | Parameter | Value | Used by |
|---|---|---|---|
| PRM-1 | <e.g. access-token lifetime> | 15 min | 05 §2.4, 08 §3.4 |

## 11. Open Items

1. <question>? — *default: <default>*.
