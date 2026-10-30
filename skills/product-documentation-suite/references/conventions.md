# Writing Conventions — what every document in the suite looks like

These conventions make the suite navigable by people and by tooling;
`scripts/audit_suite.py` checks the mechanical ones (`quality-gates.md` §0).

## 1. Files and folders

- Path `docs/NN-kebab-case-title.md`; `NN` is a stable two-digit number, never renumbered. First line `# NN — Title` (em dash). The index is `docs/README.md`.
- Supporting folders: `docs/adr/` (full decision records), `docs/research/`, `docs/security/` (per-gate reports, created at the first gate), `api/` beside `docs/` (`openapi.yaml`, collections), `design/` (assets), `business/` beside `docs/` for pricing, legal and support material that engineering does not build from (own `README.md`, same header block, code `BIZ`).

## 2. Header block

A two-column table directly under the title, then a purpose blockquote.

```markdown
# 06 — Features & Functions

| | |
|---|---|
| **Document ID** | ACME-FTR-001 |
| **Product** | Acme Scheduler (working codename `acme`) |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Product & Engineering |
| **Last updated** | 2026-10-26 |
| **Audience** | Product, engineering, QA |
| **Depends on** | `00-canonical-model.md` §2–§4, `07-user-roles-and-permissions.md` §4 |
| **Consumed by** | `04-data-model.md`, `05-api-documentation.md`, `09-development-plan.md` |

> **Purpose.** What this document is, what it is **not** (name the document
> that owns the excluded material), and which documents own the vocabulary
> it uses ("Vocabulary follows `00-canonical-model.md`").
```

Rows — **required**: Document ID, Product, Version, Status, Last updated.
**Recommended** (every template carries them; drop only with a reason):
Owner, Audience, Depends on, Consumed by. A document may add rows
(Assets, Derived from, Machine-readable artifacts).

- **Document ID** `<PREFIX>-<CODE>-001`: prefix is the product's 2–5 letter code, identical across the suite; codes: CANON (00), PDD (01), UGD (02 user guide), ARC (03), DBD (04), API (05), FTR (06), RBAC (07), SEC (08), DVP (09), DOM (10), DES (11), SCR (12), OPS (13), ADM (14), PTL (15 portal guide), AIG (16 AI governance), IDX (README), SECR (security test reports), BIZ (business documents outside the suite). The README's Status row is the approval banner and is exempt from the status set; `BACKLOG.md` and `deferred.md` carry no header block.
- **Version** is semver with `-draft` while the status is `Draft` or `Pending approval`; `-draft` is dropped at approval for every document, living ones included. Patch = wording; minor = additive content or a schedule-only change; major = scope, phase or vocabulary change.
- **Status**: `Draft` · `Pending approval` · `Approved vX.Y.Z (YYYY-MM-DD)` · `Living document — reflects the build through Sxx` · `Superseded by <file>`. Living documents (02, 13, 14) are `Draft` until the suite is approved, then `Living document — reflects the build through S01`.
- **Last updated** is an absolute ISO date. Documents over 300 lines carry a `## Table of Contents` heading with anchor links.

## 3. Identifier families

| Family | Pattern | Defined in | Example |
|---|---|---|---|
| Feature module | `F<n>` | 06 §1.4 catalogue | `F8` |
| Functional requirement | `FR-<module>.<seq>` — `<module>` is the F number | 06 per module | `FR-8.3` |
| Architecture decision | `ADR-<NNN>` (three digits everywhere, condensed row and file name; the audit tolerates four in legacy files) | 01 §7; full records `docs/adr/ADR-NNN-title.md` | `ADR-005` |
| Abuse case | `A<n>` | 08 §2.2 | `A5` |
| Data principle / design principle | `P<n>` (04 §1) / `DP-<n>` (11 §1) | 04, 11 | `P4`, `DP-2` |
| Parameter | `PRM-<n>` — every numeric limit, timeout, retention period or default that more than one document uses | 00 §10 parameter register | `PRM-7` break-glass window |
| Separation-of-duties rule | `SOD-<n>` | 07 §6 | `SOD-3` |
| Incident severity | `Sev-<n>` | 08 §10.1 | `Sev-1` |
| Risk | `R<n>` | 09 risk register (01 §9 names risks in prose) | `R3` |
| Sprint / backlog row | `S<##>` / `S<##>-B<n>` | 09 sprint blocks | `S07-B2` |
| Milestone | `M<n>` | 09 milestones | `M2` |
| Screen | `SCR-<###>` | 12 | `SCR-014` |
| Permission | `resource.action` (imperative verb); in OpenAPI as `x-permission` plus `x-scope` (`tenant` / `assigned` / `own` / `public`; unauthenticated operations carry `x-permission: none`) per operation | 07 §4 matrix (05 §2.5 in the Minimal profile) | `reports.approve` |
| Domain event | `module.entity.verb` (past tense) | 05 §6.3 catalogue; envelope in 05 §6.1 | `reports.version.published` |
| Audit action | `category.entity.verb` (past tense) | 07 §9 registry | `phi.record.viewed` |
| Problem type | stable URN slug | 05 §5 | `urn:acme:problem:conflict` |
| Change request | `CR-<n>` | 09 §10.1 change log table | `CR-4` |

Document-local rule families (a domain specification's `R-C1`, a test-vector
set `T1…`) are declared in that document's own conventions section and never
cited outside it without the document name.

Rules: IDs are **stable** (retire with a strikethrough and a note; never
renumber). One FR is one testable behaviour. Every ID used in a later
document is defined in its owning document.

**FR → sprint link.** Each 09 backlog row that delivers behaviour ends its
*Notes* cell — always the last column of the row — with `FRs: FR-2.1, FR-2.2`
(behaviour named by the row text) and/or `implied: FR-2.7` (covered by the
row's scope without being named), segments separated by ` · `; ranges within
one module are allowed (`FR-3.1–FR-3.4`). Foundation rows (scaffold, CI,
environments) may carry none. 06 Appendix A mirrors the rows: its Sprint cell
reads `— (09 pending)` until 09 exists, then lists the real `S##-B#` ids and
the basis (named / implied); a line `**Unscheduled (n)**` ends the table and
introduces the unscheduled list; 09 wins on disagreement and the appendix is
regenerated. Requirements with no row go to `docs/deferred.md`, which exists
from the moment 06 does.

## 4. Requirement and acceptance language

- RFC 2119 keywords: **SHALL** (mandatory), **SHOULD** (default unless justified), **MAY** (optional). Write "The system SHALL …" with concrete values (limits, timeouts, counts, formats), never adjectives.
- A module whose requirements straddle phases tags the exception at the end of the FR line: `… *(Phase 2)*`; 06 §1.2 lists the tagged ids per phase.
- Acceptance criteria: `- **Given** <precondition>, **when** <action>, **then** <observable result>.` Edge cases and business rules follow as their own list. Trivial modules may state `User flows: none — <reason>`.

## 5. Vocabulary discipline

- Roles, statuses, enum values and entity names appear exactly as in 00, in `code font`.
- **Missing term, one protocol.** While 00 is still `Draft`/`Pending approval` (you are writing the suite), add the term to 00 immediately and cite it. After approval, mark it `[CANON-PENDING: Term]` and back-port through change control; the audit lists the terms. A value set whose owning entity is missing names the entity it will belong to (`OutboundMessage` delivery `event_type`).
- **Numbers live once.** A numeric parameter used by more than one document is a `PRM-n` row in 00 §10; other documents cite `00 §10 PRM-n`.
- **Owned vocabularies.** 10 owns domain keys and presets, 11 owns token and component names, 12 owns `SCR` ids, 05 owns problem types and event names, 07 owns permission and audit-action strings. The vocabulary sweep checks everything else against 00.
- Cite, never restate: `` `04-data-model.md` §3.14 ``. Cite top-level sections (`§n`) by default; cite `§n.m` only when the target uses numbered `###` headings. When two documents disagree, **00 then 01 win** and the other document is corrected through change control.

## 6. Tables, matrices, diagrams

- Permission matrix cells: `✓` tenant-wide · `A` scoped · `✗` denied, with footnotes `[n1]`. Because `A` means different things per role, 07 §1 carries a **scope legend** table (role → what `A` covers: own records, assigned objects, treatment relationship, time-boxed break-glass). No emoji anywhere in the suite.
- State machines: an ASCII diagram with named transitions, then a **transitions table** — Transition | From → To | Triggered by | Precondition | Side effects — and the immutability and versioning rules. Simple lifecycles (three states, no branching) may be one bullet.
- Enumerations: one compact table for simple enums (Enum | Values | Notes); a subsection only for state machines.
- Architecture and ERD diagrams in Mermaid; wireframes in ASCII with real labels and placeholder data. In the Full profile 03 §11 holds at most six journey-level wireframes and 12 owns per-screen ones; without 12, 03 holds the ten most important screens.
- Catalogue tables keep the column set of their template; add columns rather than reinventing.
- **Size caps.** When a document must be shorter than its typical size, keep every mandatory section and cut examples to one per concept and catalogues to representative rows with a pointer to the machine-readable artifact. Never cut structure, blank lines around headings, or acceptance criteria.

## 7. Decisions, assumptions, open questions

- Every decision with alternatives is a row in 01 §7 (ID, decision, rationale, record) — the *Record* column links `adr/ADR-NNN-title.md` when a full record exists; records are created as decisions are numbered. ADR status is `proposed` until the suite is approved, then `accepted`.
- 03 §2 holds the architectural-style decision in full (its row in 01 §7 points there); other decisions that need a page go to `docs/adr/`.
- A decision that arises in a downstream document (03, 04, 05) is written as **Proposed ADR (number assigned at back-port)**; the consistency pass numbers it in 01 §7. The audit flags the phrase.
- Assumptions are listed (01 §8). Each document ends with an **Open Items** section (an optional References section may follow it): numbered, each with a recommended default; 01 §10 collects the ones that need the approver, and the README mirrors 01 §10 plus any open item that blocks another document (named per source).

## 8. Living documents (02, 13, 14, README; BACKLOG.md and deferred.md)

- Before approval, 02/13/14: `Status` `Draft`, version `1.0.0-draft`, a line **Build status (pre-build; reconciled through S00)** in the purpose block. 02 is written in full from 06, 07 §8 and 12 (UI labels come from 12; without 12, from 11 and the 03 §11 wireframes). 13 and 14 are skeletons: every heading present, sections the frozen documents already determine filled (topology from 03 §9, configuration reference, bootstrap), the rest marked exactly `*Filled during S03*` (two-digit sprint; the audit counts the markers). The README is living too and carries its own header (code IDX).
- 13's purpose block names the repository files its commands are verified against once code exists; 14's capability table shows design intent from 07 §4 until the first identity sprint lands, then the implementation.
- After approval: status `Living document — reflects the build through Sxx`, `-draft` dropped, the purpose line reads **Build status (reconciled through Sxx)**; unbuilt features marked **planned (phase X)** inline; 09 §1.5 (Definition of Done) makes a sprint update 02, 13 and 14 and bump the build-status line when user-visible, operational or administrative behaviour changes.
- `BACKLOG.md` starts at the first review gate (a brownfield audit counts as one); `deferred.md` exists from the moment 06 does. Neither carries a header block.

## 9. Dates, sizes, counts

- Dates absolute ISO (`2026-10-26`). Sprint dates derive from a stated kickoff; the plan says a kickoff slip shifts all dates 1:1.
- README index sizes are real `wc -l` counts for every document, living ones included; the audit flags drift over 10 %.
