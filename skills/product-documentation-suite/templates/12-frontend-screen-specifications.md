# 12 — Frontend Screen Specifications

| | |
|---|---|
| **Document ID** | {{PREFIX}}-SCR-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Frontend lead |
| **Last updated** | {{DATE}} |
| **Audience** | Frontend, QA, product |
| **Depends on** | `00-canonical-model.md` · `11-frontend-design-system.md` · `03-architecture.md` §5, §11 · `07-user-roles-and-permissions.md` §4, §8 · `05-api-documentation.md` §3 · `09-development-plan.md` §3 (sprint ids) |
| **Consumed by** | `02-product-documentation.md` (UI labels), `09-development-plan.md` §1.4 |
| **Applies to** | <route groups> |

> **Purpose.** The build-ready per-screen contract. It expands — and never
> contradicts — the journey wireframes in `03-architecture.md` §11. Tokens,
> component anatomy, motion and accessibility live once in
> `11-frontend-design-system.md`.

---

## Table of Contents

---

## 0. How to Read This Document

Every screen has six blocks: (1) identity table; (2) ASCII wireframe with
real labels and placeholder data; (3) component inventory; (4) states —
loading / empty / error; (5) interactions; (6) API & permission notes.

| Screen | Route group | FRs | Sprint (09) |
|---|---|---|---|
| SCR-001 | | FR-1.1 | S02-B1 |

## 1. <Route group>

### SCR-001 — <Screen name>

| | |
|---|---|
| **Route** | `/…` |
| **Roles / visibility** | `ROLE_A`, `ROLE_B` (per 07 §8) |
| **Purpose** | |

```
<wireframe>
```

**Components** — region → primitive / domain component (11 §9).

**States** — loading: <skeleton>; empty: <copy, CTA>; error: <copy, retry>.

**Interactions** — <action → result, keyboard>.

**API & permissions** — `GET /…` (`resource.view`); mutations require `Idempotency-Key`.

## Appendix A — Empty-state copy
## Appendix B — Keyboard map
## Appendix C — Skeletons
## Appendix D — Responsive matrix
## Appendix E — Notification routing
## Appendix F — Open Items

1. <question>? — *default: <default>*.
