# 14 — Administrator Guide (<privileged roles>)

| | |
|---|---|
| **Document ID** | {{PREFIX}}-ADM-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Draft |
| **Owner** | Product |
| **Last updated** | {{DATE}} |
| **Audience** | `ROLE_ADMIN`, `ROLE_HEAD` |
| **Depends on** | `07-user-roles-and-permissions.md` §4, §6, `02-product-documentation.md`, `13-runbooks.md` |
| **Consumed by** | administrators, support |

> **Purpose.** What privileged roles can do, task by task. It is **not** the
> runbooks (13) or the design intent (07): until the identity sprint lands
> the capability table restates 07 §4 as intent; afterwards it reflects the
> implementation (<policy module path>).
>
> **Build status (pre-build; reconciled through S00).** Skeleton; sections
> that need the build are marked `*Filled during Sxx*`.

---

## Table of Contents

---

## 1. Who this guide is for — capabilities

| Capability (permission) | `ROLE_ADMIN` | `ROLE_HEAD` | Notes |
|---|---|---|---|
| `users.manage` | ✓ | ✗ | |

Rules to internalise before acting:
- **404-on-invisible** — users without a permission get 404, not 403.
- **Everything is audited** — every action writes an audit event (07 §9) with actor, IP, before/after.

## 2. User Lifecycle

### 2.1 Create → invite → enrol → assign role
### 2.2 Lock / unlock
### 2.3 Force resets

## 3. Organisation / Tenant Onboarding

### 3.1 Checklist (new instance)

## 4. <Operational Setup>

## 5. <Governance Workflows>

### 5.1 Stage-by-stage authorization (SOD-n)

## 6. Audit Log Review

## 7. Notifications

## 8. Open Items

1. <question>? — *default: <default>*.
