# 07 — User Roles & Permissions

| | |
|---|---|
| **Document ID** | {{PREFIX}}-RBAC-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Security Architecture |
| **Last updated** | {{DATE}} |
| **Audience** | Product, engineering, QA, security review |
| **Depends on** | `00-canonical-model.md` §2, §7 |
| **Consumed by** | `10-domain-specification.md`, `06-features-and-functions.md`, `05-api-documentation.md`, `08-security-design.md`, `12-frontend-screen-specifications.md`, `14-admin-guide.md` |

> **Purpose.** The master permission matrix, the per-role operating picture
> and the separation-of-duties invariants. It is **not** the authorization
> model (00 §7) or the enforcement design (08 §4). Endpoint gates in
> `05-api-documentation.md` cite permission strings from §4 here.

---

## Table of Contents

---

## 1. Authorization Model & Scope Legend

<!-- Recap 00 §7 in two lines, then define the matrix legend. -->

Cell legend: `✓` tenant-wide · `A` scoped (see table) · `✗` denied; footnotes `[n1]`.

| Role | What `A` covers |
|---|---|
| `ROLE_A` | own records only |
| `ROLE_B` | objects the user is assigned to |
| `ROLE_PLATFORM` | nothing standing; time-boxed break-glass (SOD-n), every access audited |

## 2. Role Definitions

### 2.1 `ROLE_A` — <Display name>

- **Mission:** <one sentence>
- **Scope:** <tenant-wide / assigned / own>
- **Typical day:** <three bullets>
- **May:** <capabilities>
- **May not:** <explicit prohibitions>

<!-- Repeat per role. A platform role with zero standing access states how it obtains access (grant by whom, for how long, audited how). -->

## 3. Positions vs Global Roles

<!-- Only if objects carry per-object positions. Eligibility table + how a position grants scope. Otherwise: "Not used." -->

## 4. Master Permission Matrix

Atomic permissions grouped by resource; legend per §1. Every string here is cited by at least one requirement or endpoint; the audit lists orphans.

### 4.1 <Resource group>

| Permission | `ROLE_A` | `ROLE_B` | `ROLE_C` |
|---|---|---|---|
| `resource.view` | ✗ | A | ✓ |
| `resource.manage` | ✗ | ✗ | ✓ |
| `resource.approve` [n1] | ✗ | ✗ | ✓ |

### 4.n Footnotes

- **[n1]** <dual control, delegation limits, etc.>

## 5. Per-Role Workflow Walkthroughs

### 5.1 `ROLE_A` (<persona name>)

<!-- A day in the life as numbered steps citing permissions and states. -->

## 6. Separation of Duties & Anti-Fraud Rules

| ID | Invariant | Enforced by |
|---|---|---|
| SOD-1 | author ≠ reviewer ≠ approver for the same object version | service layer, `08-security-design.md` §4 |
| SOD-2 | role escalation into <tier> requires a second approver | |

### 6.1 Break-glass access

<!-- Who may invoke, time limit (00 §10 PRM-n), what is logged, who is notified. -->

## 7. External Principals (if any)

### 7.1 Capabilities
### 7.2 Prohibitions (structural, not just policy)

## 8. Role → Default Landing Pages & Navigation

| Role | Landing page | Navigation items |
|---|---|---|

## 9. Audit Action Registry

<!-- `category.entity.verb` (past tense), one row per auditable action; 08 §8 and 04 cite this table. -->

| Audit action | Triggered by | Fields beyond the common envelope |
|---|---|---|
| `identity.role.changed` | role assignment | before, after, second approver |

## 10. Open Items

1. <question>? — *default: <default>*.
