# product-documentation-suite

A Claude Code skill that plans a software product as **one canonical model,
cited by a fixed set of numbered documents, written in dependency order and
approved before code**, and audits an existing `docs/` folder against the
same rules. Part of [Secure by Design Skills](https://github.com/Cy-S3c/secure-by-design-skills).

The layout is the [Agent Skills](https://agentskills.io) one: `SKILL.md`
holds the instructions Claude follows, `references/` the rules, `templates/`
one skeleton per document and `scripts/audit_suite.py` the mechanical checks.
The version is `metadata.version` in `SKILL.md`.

## What it produces

A `docs/` folder in which every document of the chosen profile is written in
full, from one canonical model, with a README that an approver can sign.

| # | Document | Owns |
|---|---|---|
| 00 | Canonical Model | roles and external principals, entities, enumerations, state machines, stack, API conventions, authorization model, document register, glossary, parameter register `PRM-n` |
| 01 | Product Design Document | vision, goals and metrics, non-goals, personas, module map, phases with exit criteria, condensed ADRs, risks, open questions |
| 02 | Product Documentation (user guide) | task how-tos from the user's seat |
| 03 | Architecture & Wireframes | C4 views, module catalogue, deployment, environments, observability |
| 04 | Data Model | tables, indexes, row-level security, retention, migrations |
| 05 | API Documentation | endpoints with `x-permission`, error types, event envelope and catalogue |
| 06 | Features & Functions | `F#` modules, `FR-x.y` requirements, Given/When/Then acceptance criteria |
| 07 | Roles & Permissions | `resource.action` matrix, separation-of-duties rules, audit action registry |
| 08 | Security Design | framework mapping, STRIDE summary, abuse cases `A#`, trust boundaries, controls, severity classes, release checklist |
| 09 | Development Plan | sprints `S##-B#` linked to requirements, DoR/DoD, RACI, milestones, risks, change control |
| 10 | Domain Specification | only when a domain standard exists |
| 11 / 12 | Design System / Screen Specifications | tokens, components, `SCR-###` |
| 13 / 14 | Runbooks / Admin Guide | verified procedures (skeletons before the first sprint) |
| — | `adr/`, `deferred.md`, `BACKLOG.md` | full decision records, unscheduled requirements, review-gate findings |

Three sizing profiles decide which documents a product needs: **Minimal**
(internal tool or API-only service), **Standard** (multi-role product with a
UI) and **Full** (regulated, security-sensitive, external users or a domain
standard). Omitted documents are listed as not applicable with a reason.

## How Claude uses it

1. Collects the four inputs only the owner can give: hosting and tenancy
   model, compliance driver, the role set, the phases wanted. Everything else
   becomes a stated assumption or an open question with a recommended default.
2. Picks the profile and records it in the README.
3. Writes 00 first, then the rest in authoring order (01, 07, 10, 06, 04, 05,
   03, 08, 09, 11/12), each from its template, deleting the guidance comments
   and placeholders as it goes. Documents cite each other by stable section
   number and never restate each other.
4. Writes 02 in full, then the README (status banner, profile, index with real
   sizes, decisions needed), then the 13/14 skeletons.
5. Runs the audit, fixes every FAIL, fixes or justifies every WARN, then does
   the suite-level consistency pass (vocabulary, parameters, module parity,
   permission parity, open items).
6. Hands over for approval; on sign-off bumps every frozen document to
   `Approved v1.0.0`, and later changes go through change control.

For an existing `docs/` folder the skill runs the audit first, builds a gap
table, reconciles vocabulary into 00, then fills gaps in authoring order.
Where the code contradicts a document it records a BACKLOG item rather than
silently editing the document.

## Requirements

Python 3.9 or newer. The audit script uses the standard library only.

## Install

From a clone of this repository, user level (every project on this machine):

```bash
cp -r skills/product-documentation-suite ~/.claude/skills/
```

Project level (committed with the repository):

```bash
mkdir -p .claude/skills && cp -r skills/product-documentation-suite .claude/skills/
```

Or install the whole repository as a plugin; see the
[root README](https://github.com/Cy-S3c/secure-by-design-skills#installation). Start a new Claude Code session
afterwards. The skill loads on its own when a request matches its description
(planning docs, PRD, architecture, data model, API contract, roles, security
design, sprint plan, runbooks, or auditing a `docs/` folder), or on request:
"use the product-documentation-suite skill".

## Verify

```bash
python3 ~/.claude/skills/product-documentation-suite/scripts/audit_suite.py --help
```

Against a documentation folder (exit 1 only when a FAIL is reported;
`--allow-missing` while the suite is still being written, never for the final
run before approval):

```bash
python3 ~/.claude/skills/product-documentation-suite/scripts/audit_suite.py docs/ --profile standard --allow-missing
```

Severities: **FAIL** must be fixed, **WARN** fixed or justified in the README,
**INFO** is awareness. The script reads the `FRs:` / `implied:` segments of
sprint rows, the `— (09 pending)` cells of 06 Appendix A, `[CANON-PENDING:
Term]` markers and `*Filled during S03*`-style living-document markers.

## Files

| Path | Contents |
|---|---|
| `SKILL.md` | the workflow Claude follows, the document contract, common mistakes |
| `references/suite-map.md` | catalogue with must-contain lists, authoring and review orders, profiles, stable section numbers |
| `references/conventions.md` | header block, identifier families, markers, language, tables, living documents |
| `references/standards.md` | the standard each document follows and the default numbers |
| `references/quality-gates.md` | audit checks, per-document definition of done, consistency pass, approval, brownfield |
| `templates/` | one skeleton per document plus README, ADR, BACKLOG and deferred |
| `scripts/audit_suite.py` | the mechanical checks |

## Companion skill

[`threat-modeling-stride`](https://github.com/Cy-S3c/secure-by-design-skills/tree/main/skills/threat-modeling-stride) reads 00, 03, 04, 05,
07 and 08 and produces the STRIDE-per-element threat model (data-flow
diagrams, rated register, HTML report) into `docs/security/threat-model/`;
08 §2 links its summary.

## Update or remove

Replace or delete the folder; the skill stores nothing elsewhere.
