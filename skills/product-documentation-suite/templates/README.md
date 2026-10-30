# {{PRODUCT}} — Documentation Suite

| | |
|---|---|
| **Document ID** | {{PREFIX}}-IDX-001 |
| **Product** | {{PRODUCT}} — <one line: what it is, for whom> |
| **Version** | 1.0.0-draft (suite version) |
| **Status** | **PENDING APPROVAL — development does not start until sign-off** |
| **Last updated** | {{DATE}} |
| **Sign-off** | — (name, date, suite version at approval) |
| **Profile** | Standard <!-- Minimal / Standard / Full — references/suite-map.md §4 --> |
| **Tech stack (locked)** | <frontend · backend · database · cache · queue · storage · runtime> |

**Authoring order:** 00 → 01 → 07 → 10 → 06 → 04 → 05 → 03 → 08 → 09 → 11 → 12 → 02 → README → 13/14 skeletons.
**Recommended review order:** README → 00 → 01 → 10 → 03 → 04 → 07 → 06 → 05 → 08 → 09 → 02 → 11 → 12.

---

## Documentation Index

<!-- Sizes are real `wc -l` counts for every row, living documents included. -->

| # | Document | File | What it covers | Size |
|---|---|---|---|---|
| 0 | **Canonical Model** | [00-canonical-model.md](00-canonical-model.md) | Roles, entities, enums, state machines, stack, API conventions, parameter register, glossary | — ln |
| 1 | **Product Design Document** | [01-product-design-document.md](01-product-design-document.md) | Vision, personas, module map, master workflow, phases, ADRs, risks, open questions | — ln |
| 2 | **Product Documentation** | [02-product-documentation.md](02-product-documentation.md) | End-user guide: getting started, module how-tos, best practices, FAQ, glossary | — ln |
| 3 | **Architecture** | [03-architecture.md](03-architecture.md) | C4 views, architectural-style ADR, module catalogue, lifecycle, jobs, deployment, observability, wireframes | — ln |
| 4 | **Data Model** | [04-data-model.md](04-data-model.md) | ERD, DDL, JSON contracts, indexes, retention, migrations, volume estimates | — ln |
| 5 | **API Documentation** | [05-api-documentation.md](05-api-documentation.md) | Conventions, auth flows, endpoint catalogue, payloads, error catalogue, events, versioning | — ln |
| 5a | **OpenAPI Spec** | [../api/openapi.yaml](../api/openapi.yaml) | Machine-readable contract (skeleton pre-build) | — ln |
| 6 | **Features & Functions** | [06-features-and-functions.md](06-features-and-functions.md) | Feature modules, testable FRs, user flows, acceptance criteria, FR → sprint traceability | — ln |
| 7 | **User Roles & Permissions** | [07-user-roles-and-permissions.md](07-user-roles-and-permissions.md) | Scope legend, role definitions, permission matrix, SoD rules, audit actions | — ln |
| 8 | **Security Design** | [08-security-design.md](08-security-design.md) | Framework mapping, STRIDE, abuse cases, authN/authZ, data protection, hardening, audit, SDLC gates, IR, release checklist | — ln |
| 9 | **Development Plan** | [09-development-plan.md](09-development-plan.md) | Sprints with FR links, DoR/DoD, RACI, milestones, quality strategy, risk register, change control | — ln |
| 10 | **Domain Specification** | [10-domain-specification.md](10-domain-specification.md) | <the product's domain standard> | — ln |
| 11 | **Frontend Design System** | [11-frontend-design-system.md](11-frontend-design-system.md) | Principles, brand, colour, typography, components, motion, accessibility | — ln |
| 12 | **Screen Specifications** | [12-frontend-screen-specifications.md](12-frontend-screen-specifications.md) | Build-ready per-screen contract | — ln |
| 13 | **Operations Runbooks** | [13-runbooks.md](13-runbooks.md) | Deploy, configuration, backup/restore, incident playbooks, rotation, monitoring & on-call (skeleton pre-build) | — ln |
| 14 | **Administrator Guide** | [14-admin-guide.md](14-admin-guide.md) | Privileged-role operations (design intent until the identity sprint lands) | — ln |
| — | **Decision records** | [adr/](adr/) | Full ADRs linked from 01 §7 | n files |
| — | **Deferred / unscheduled** | [deferred.md](deferred.md) | Requirements with no sprint row, owner deferrals | — ln |

**Not applicable in this suite:** <!-- e.g. "10 — no domain standard", "12 — API-only product"; BACKLOG.md and security/ start at the first review gate --> none.

**Audit justifications:** <!-- one line per remaining WARN from scripts/audit_suite.py, or "none" --> none.

---

## Phase Summary

| Phase | Scope | Sprints | Exit criteria (01 §6) |
|---|---|---|---|
| **1 — Core** | <modules> | S01–S0n | |
| **2 — …** | <modules> | | |

## Key Decisions Snapshot

- **<ADR-001 one-liner>** — <why>.

## Decisions Needed From You (approval blockers)

<!-- 01 §10 in full, then blocking open items from other documents, each marked with its source. Every item carries the author's default. -->

1. <question> → **docs default: <default>** *(01 §10)*
2. <question> → **recommended: <default>** *(04 Appendix B)*

## Post-Approval Next Step

Sprint S01 kickoff (see `09-development-plan.md` §3): <scaffold, CI gates, contract skeleton, application shell>.
