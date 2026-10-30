# 06 — Features & Functions

| | |
|---|---|
| **Document ID** | {{PREFIX}}-FTR-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Product & Engineering |
| **Last updated** | {{DATE}} |
| **Audience** | Product, engineering, QA, delivery leadership |
| **Depends on** | `00-canonical-model.md` (roles §2, entities §3, enums §4), `01-product-design-document.md` §4, §6, `07-user-roles-and-permissions.md` §4, `10-domain-specification.md` (field names) |
| **Consumed by** | `04-data-model.md`, `05-api-documentation.md`, `09-development-plan.md`, `02-product-documentation.md` |

> **Purpose.** The functional specification: every requirement testable and
> numbered `FR-<module>.<n>`, with acceptance criteria. It is **not** the
> permission matrix (07), the state-machine definition (00 §4) or the schema
> (04); it cites them. Vocabulary follows `00-canonical-model.md`.

---

## Table of Contents

<!-- numbered sections only; regenerate when sections change -->

---

## 1. Introduction

### 1.1 Scope of this document

### 1.2 Release phases (from `01-product-design-document.md` §6)

| Phase | Modules | FRs tagged for a later phase |
|---|---|---|
| 1 | F1–F8 | — |
| 2 | F9 | FR-3.8, FR-6.9 |

### 1.3 Conventions

- **FR numbering**: `FR-<module>.<seq>`, `<module>` is the F number (e.g. `FR-3.6`). Stable — never renumber.
- **Testability**: every FR is verifiable by inspection, automated test, or scripted manual test, and names concrete values.
- **Phase tags**: an FR delivered in a later phase than its module ends with `*(Phase 2)*` and is listed in §1.2.
- **State / enum values** in `code format`, exactly as `00-canonical-model.md` §4; **roles** by enum name; **permissions** as permission strings from `07-user-roles-and-permissions.md` §4.
- **Deny-by-default**: every requirement inherits `00-canonical-model.md` §7.

### 1.4 Feature catalogue

| # | Module | Phase | Primary roles | Key entities |
|---|---|---|---|---|
| F1 | <Module> | 1 | `ROLE_A` | `Entity` |

---

## 2. F1 — <Module name>

### 2.1 Purpose

<!-- Two to four sentences: what the module provides and which business or security baseline it enforces. -->

### 2.2 Functional requirements

**<Group heading>**

- **FR-1.1** The system SHALL <behaviour with concrete values: limits, timeouts, counts, formats>.
- **FR-1.2** The system SHALL <…> *(Phase 2)*.

### 2.3 Key user flows

**Flow A — <name>**
1. <Role> <does>.
2. System <responds; state change named>.

<!-- Trivial module: "none — <reason>". -->

### 2.4 Acceptance criteria

- **Given** <precondition>, **when** <action>, **then** <observable result>.

### 2.5 Edge cases & business rules

- <rule>

### 2.6 Phase & dependencies

| Phase | **Phase 1** |
|---|---|
| Depends on | F2 (`FR-2.3`), `10-domain-specification.md` §3 |
| Feeds | F4, F7 |

<!-- The Depends/Feeds graph across modules must be acyclic. Repeat §2 per module F2…Fn. -->

---

## Appendix A — FR → Sprint Traceability

<!-- Until 09 exists every Sprint cell reads `— (09 pending)`. Then regenerate from the 09 sprint rows (09 wins): Delivered by = the S##-B# ids; Basis = named / implied. -->

| FR | Module | Delivered by (09) | Basis |
|---|---|---|---|
| FR-1.1 | F1 | — (09 pending) | |

## Appendix B — Open Items

1. <question>? — *default: <default>*.
