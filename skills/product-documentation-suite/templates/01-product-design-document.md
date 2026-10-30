# 01 — Product Design Document

| | |
|---|---|
| **Document ID** | {{PREFIX}}-PDD-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Product & Engineering |
| **Last updated** | {{DATE}} |
| **Audience** | Approver, product, engineering leads |
| **Depends on** | `00-canonical-model.md` |
| **Consumed by** | every specification document; `09-development-plan.md` §1.2 binds to §6 |

> **Purpose.** Why the product exists, for whom, and what is in and out of
> scope: vision, goals, personas, module map, phases, decisions, risks and
> the questions the approver must answer. It is **not** the functional
> specification (`06-features-and-functions.md`). Vocabulary follows
> `00-canonical-model.md`.

---

## 1. Vision

**<One bold paragraph: the whole product in three lines — what it runs, for whom, and the quality bar.>**

### 1.1 Problem statement

<!-- Today's workflow, where it breaks, what it costs. Concrete, not aspirational. -->

### 1.2 Goals & success metrics

| Goal | Metric | Target (horizon) |
|---|---|---|
| <goal> | <measurable metric, in canonical terms> | <number> (<end of Phase 1 / 12 months post-launch>) |

### 1.3 Non-goals (explicitly out of scope)

- <thing the product will not do, and what it integrates with instead>

## 2. Personas

| Persona | Role (enum) | Goal | Frustration today |
|---|---|---|---|
| <Name, title> | `ROLE_A` | | |

## 3. Product Pillars

1. **<Pillar>** — <one sentence>.

## 4. Module Map (functional surface)

<!-- Must match 06 §1.4 and 03 §3 one-to-one. -->

| Module | Purpose | Phase |
|---|---|---|
| <Module> | | 1 |

## 5. End-to-End Workflow (master user journey)

### 5.1 <Setup>
### 5.2 <Core loop>
### 5.3 <Governance / continuous>

<!-- Numbered steps naming the role (enum) and the entity/status at each step. -->

## 6. Release Phases

| Phase | Scope | Exit criteria | Target window |
|---|---|---|---|
| **1 — Core** | | <verifiable statement> | S01–S0n (`09-development-plan.md` §6) |
| **2 — …** | | | |

## 7. Key Product Decisions (condensed ADRs)

| ID | Decision | Rationale | Record |
|---|---|---|---|
| ADR-001 | <architectural style> | <why> | `03-architecture.md` §2 |
| ADR-002 | <decision> | <why> | `adr/ADR-002-<title>.md` or — |

## 8. Constraints & Assumptions

- <hosting, tenancy, data sensitivity, team shape, browser support, budget, deadline — mark each assumption as such>

## 9. Risks (top)

| Risk | Impact | Mitigation |
|---|---|---|
| <risk> | | |

## 10. Open Questions for Approval

<!-- Each with a recommended default; mirrored in README "Decisions needed". -->

1. <question>? — *default in docs: <default>*.
