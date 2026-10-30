# 09 — Development Plan

| | |
|---|---|
| **Document ID** | {{PREFIX}}-DVP-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Delivery Lead / Tech Lead |
| **Last updated** | {{DATE}} |
| **Audience** | Delivery, engineering, approver |
| **Depends on** | `00-canonical-model.md`, `01-product-design-document.md` §6, §8, `06-features-and-functions.md`, `08-security-design.md` §11, `03-architecture.md` §9.3 |
| **Consumed by** | `06-features-and-functions.md` Appendix A, `README.md`, `02-product-documentation.md`, `11-frontend-design-system.md`, `12-frontend-screen-specifications.md`, `13-runbooks.md`, `14-admin-guide.md` |

> **Purpose.** Translates the product design into an executable delivery
> programme: phases, sprints with requirement links, team, quality gates,
> risks, procurement, change control. Phase definitions follow
> `01-product-design-document.md` §6 exactly; where they disagree, 01 wins
> and this plan is corrected via change control (§10). It is **not** the
> requirements document; it links to it.

---

## Table of Contents

---

## 1. Delivery Approach

### 1.1 Cadence and calendar

<!-- Sprint length, kickoff date, sprint-end weekday, holidays with reduced capacity. -->

### 1.2 Phase mapping (binding)

| Phase (01 §6) | Sprints | Exit gate |
|---|---|---|

### 1.3 Module ID map and row conventions

Modules are `F1–Fn` exactly as catalogued in `06-features-and-functions.md`
§1.4 (copy the table; 06 owns the ids). Each backlog row's *Notes* cell ends
with `FRs: <ids>` (behaviour the row text names) and/or `implied: <ids>`
(covered by the row's scope); ranges within a module are allowed. Foundation
rows may carry none. `06-features-and-functions.md` Appendix A mirrors the
rows; this plan wins on disagreement. Unscheduled requirements go to
`deferred.md`.

| ID | Module | Phase |
|---|---|---|
| F1 | <Module> | 1 |

### 1.4 Definition of Ready (DoR)

A backlog item enters a sprint only when:
1. It uses canonical vocabulary (`00-canonical-model.md`).
2. Its acceptance criteria trace to `06-features-and-functions.md` FR ids.
3. UI items have a screen in `12-frontend-screen-specifications.md` (or a wireframe in `03-architecture.md` §11); API items have an OpenAPI sketch.
4. Permissions are specified (checkable against `07-user-roles-and-permissions.md` §4).
5. It is small enough to finish and demo within one sprint.

### 1.5 Definition of Done (DoD)

An item is done only when ALL of:
1. Merged to trunk via a reviewed PR; no direct pushes.
2. Unit tests pass with ≥ 80 % coverage on the changed service layer; bug fixes carry a regression test.
3. `api/openapi.yaml` updated and contract tests green, if any endpoint changed.
4. Permission matrix test extended for any new capability; deny-by-default verified.
5. Audit emission verified for every state-changing endpoint.
6. UI: keyboard accessible, axe-clean; theme variants clean when `11-frontend-design-system.md` defines them.
7. CI gates green: lint, types, unit, SAST, SCA, image scan — zero criticals.
8. `02-product-documentation.md`, `13-runbooks.md`, `14-admin-guide.md` updated when user-visible, operational or administrative behaviour changed.
9. Behind the correct feature flag if phase-gated (§1.9).

### 1.6 Branching and code review
### 1.7 Environments — see `03-architecture.md` §9.3
### 1.8 Release cadence and versioning
### 1.9 Feature flags

## 2. Team & Capacity

### 2.1 Proposed team (from `01-product-design-document.md` §8)
### 2.2 RACI for key artifact types

R = Responsible, A = Accountable, C = Consulted, I = Informed. Columns follow the team in §2.1.

| Artifact | TL | BE | FE | QA/Ops | PM |
|---|---|---|---|---|---|
| Architecture ADR | A/R | C | C | I | I |
| API contract | A | R | C | C | I |
| Permission matrix & tests | A | C | I | R | I |
| CI/CD & environments | C | C | I | A/R | I |
| Sprint plan / backlog | C | C | C | C | A/R |

## 3. Phase 1 — <name> (Sprints S01–S0n)

Exit gate (end S0n, = 01 §6 Phase 1 exit criteria): **<verifiable statement>**.

### S01 — Foundations (YYYY-MM-DD → YYYY-MM-DD)

**Goal:** a running skeleton every subsequent sprint builds on.

| ID | Backlog item | Modules | Notes |
|---|---|---|---|
| S01-B1 | Repository scaffold, tooling, pre-commit | — | Per `00-canonical-model.md` §5 stack |
| S01-B2 | Dev stack (compose): db, cache, storage, mail; one-command boot | — | `03-architecture.md` §9.1 |
| S01-B3 | CI gates: lint, type-check, unit, SAST, SCA, image scan | — | DoD §1.5 enforcement |
| S01-B4 | API skeleton: base path, problem+json errors, pagination envelope, idempotency middleware | — | `00-canonical-model.md` §6 |
| S01-B5 | Application shell: auth layout, navigation, theming | — | `12-frontend-screen-specifications.md` shell screens |
| S01-B6 | Migrations bootstrap, structured logs + trace ids, health/readiness; first-admin bootstrap command | — | `04-data-model.md` §7.1, `13-runbooks.md` §4 |

**Demo/exit:** <what is shown at sprint review>.

### S02 — <name> (YYYY-MM-DD → YYYY-MM-DD)

**Goal:** <…>

| ID | Backlog item | Modules | Notes |
|---|---|---|---|
| S02-B1 | <item> | F1 | <ref> · FRs: FR-1.1 · implied: FR-1.2 |

**Demo/exit:** <…>

## 4. Phase 2 — <name> (Sprints …)

## 5. Later Phases & Reserve

<!-- Phases beyond 2, hardening/buffer sprints, and the capacity reserve (≥ 10 %) for pilot findings. -->

## 6. Milestone Summary

Dates assume kickoff **YYYY-MM-DD**; a kickoff slip shifts all dates 1:1.

| Milestone | Meaning | Gate at end of | Date |
|---|---|---|---|
| **M1** | <internal alpha> | S0n | |
| **M2** | <Phase 1 GA> | S0n | |

## 7. Quality Strategy

### 7.1 Test pyramid
### 7.2 Critical E2E journeys (must be green to ship)
### 7.3 Permission matrix as automated tests
### 7.4 Golden-file tests (if generated artifacts)
### 7.5 Load testing
### 7.6 Accessibility
### 7.7 Security testing gates (`08-security-design.md` §11)

## 8. Risk Register

| # | Risk | Prob. | Impact | Owner | Mitigation | Trigger (escalate when) |
|---|---|---|---|---|---|---|
| R1 | | | | | | |

## 9. Dependency & Procurement List

## 10. Change Control

1. **Raise** a Change Request (`CR-n`): description, affected rows or milestones, root cause, options.
2. **Impact analysis** by Tech Lead (architecture, canonical consistency) and PM (schedule/capacity).
3. **Approve/Reject** — CRs affecting a phase's exit criteria require <approvers>; sprint-internal reordering needs PM + Tech Lead.
4. **Record** — approved CRs bump this document's version (minor for schedule, major for phase changes), update §6 and regenerate `06-features-and-functions.md` Appendix A.
5. **Communicate** — milestone-affecting CRs announced at the next sprint review.

### 10.1 Change log

| CR | Date | Change | Affected rows / milestones | Version bump |
|---|---|---|---|---|

## 11. Open Items

1. <question>? — *default: <default>*.
