---
name: product-documentation-suite
description: Use when a software product or major feature set needs industry-grade planning and product documentation before or alongside development — a canonical domain model, product design document (PRD), architecture, data model, API contract, functional requirements with acceptance criteria, roles and permissions, security design, sprint-based development plan, runbooks, admin and user guides — or when an existing docs/ folder must be audited, completed, or brought to approval.
metadata:
  origin: personal
  version: 1.1.1
---

# Product Documentation Suite

## Overview

A planning suite is **one canonical model, cited by a fixed set of numbered
documents, written in dependency order, and approved before code**. Every
other rule here follows from that sentence. The shape, templates and gates
are distilled from a 17-document suite built for a security-reporting
platform and hardened by a full dry run on a second product.

## When to use

- A product, platform or large feature set is about to be planned ("write the docs before we build", "I need a PRD / SRS / architecture / dev plan").
- A `docs/` folder exists but is partial, inconsistent or unapproved.
- One suite document is requested alone (a data model, a permission matrix, a threat model): write it in these conventions so it composes with the rest.

Not for a single ADR (use `templates/adr.md` alone), release notes, generated API reference, or a one-page brief.

## The suite

In **authoring order**; each row has a skeleton in `templates/` under the
same file name.

| # | Document | Owns |
|---|---|---|
| 00 | Canonical Model (source of truth) | roles and external principals, entities, enums, state machines, stack, API conventions, authorization model, Document ID register, glossary, parameter register `PRM-n` |
| 01 | Product Design Document | vision, goals/metrics, non-goals, personas, module map, phases with exit criteria, condensed ADRs `ADR-NNN`, risks, open questions |
| 07 | Roles & Permissions | scope legend, `resource.action` matrix, `SOD-n` rules, audit action registry |
| 10 | Domain Specification (only when a domain standard exists) | domain keys, field schema, bands, rendering contract |
| 06 | Features & Functions | `F#` modules, `FR-x.y` requirements, acceptance criteria, FR → sprint appendix |
| 04 | Data Model | tables, indexes, RLS, retention, migrations, enum → type map |
| 05 | API Documentation (+ `api/openapi.yaml`) | endpoints with `x-permission`, error `type`s, event envelope and catalogue |
| 03 | Architecture & Wireframes | C4 views, ADR-001, module catalogue, deployment, environments, observability |
| 08 | Security Design | framework mapping, STRIDE summary, abuse cases `A#`, trust boundaries (the full per-element model comes from the `threat-modeling-stride` skill into `security/threat-model/`), controls, severity classes `Sev-n`, release checklist |
| 09 | Development Plan | sprints `S##-B#` with `FRs:` links, DoR/DoD, RACI, milestones `M#`, risks `R#`, change control `CR-n` |
| 11 / 12 | Design System / Screen Specifications | `DP-n`, tokens, components, `SCR-###` |
| 02 → README → 13 / 14 | User guide (in full) → suite index → Runbooks and Admin guide (skeletons) | task how-tos; status banner and decisions needed; verified procedures |
| — | `adr/`, `deferred.md` | full decision records; unscheduled requirements |

Catalogue with must-contain lists, sizes, the approver's review order, the
sizing profiles and the stable section numbers: `references/suite-map.md`.

## Workflow

1. **Collect the inputs.** Four block the work and must come from the owner: hosting and tenancy model, compliance driver, the role set, the phases wanted. Missing → **REQUIRED SUB-SKILL:** superpowers:brainstorming. Everything else (team, dates, stack details, targets) becomes an assumption in 01 §8 or an open question in 01 §10 with a recommended default, and the work proceeds.
2. **Pick the profile** — Minimal, Standard or Full (`references/suite-map.md` §4) — and record it in the README; omitted documents are listed as *not applicable* with a reason. The suite is complete when every frozen document in the profile is written in full, 02 is written in full and 13/14 exist as skeletons (Status `Draft`, `*Filled during S03*`-style markers), where the profile includes them — not when an index of stubs exists.
3. **Write 00 first** from its template: roles as a closed enum set with tiers, external principal types, entities with owner and lifecycle, every enumeration, state machines with a transitions table, the stack with versions, API conventions, the parameter register. While 00 is unapproved, a missing term is added to 00 immediately; only after approval is it marked `[CANON-PENDING: Term]` and back-ported through change control.
4. **Write the rest in authoring order**, each from its template. Fill the header block (Document ID `PREFIX-CODE-001`, version `1.0.0-draft`, status `Pending approval`, absolute date, Owner, Audience, Depends on, Consumed by), then every section; delete the `<!-- guidance -->` comments and `<placeholders>` as you go. Cite other documents as `` `NN-file.md` §n `` (top-level sections; `references/suite-map.md` §5) and never restate their content. Requirements are `FR-<module>.<n>` "The system SHALL …" with concrete values; acceptance criteria are **Given/When/Then**; permissions are `resource.action`; numbers used twice live in 00 §10. Each 09 sprint row ends its Notes (the last column) with `FRs: …` and/or `implied: …`, segments separated by ` · `. When a size cap applies, keep every mandatory section and cut examples and catalogue rows, never structure (`references/conventions.md` §6).
5. **Write 02 in full, then the README, then the 13/14 skeletons** (refresh the README sizes once the skeletons exist). 02 is how the approver sees the product from the user's seat (labels from 12, or from 11 and 03 §11 without 12). The README is built from real `wc -l` sizes: status banner ("development does not start until sign-off"), profile, locked stack, both orders, index (with `adr/`, `deferred.md`, `api/` rows), not-applicable list, phase summary, key decisions, **Decisions needed** (01 §10 plus blocking open items from other documents, by source), audit justifications, next step.
6. **Audit.** `python3 scripts/audit_suite.py docs/ --profile <profile>` (script path relative to this skill; `--allow-missing` while writing, never for the final run). Fix every FAIL; fix or justify in the README every WARN. Then do the suite-level consistency pass in `references/quality-gates.md` §3 — vocabulary and parameter sweeps, module parity across 01/06/03/09, regenerate 06 Appendix A from 09 (no `— (09 pending)` cell survives), permission parity, number every "Proposed ADR" into 01 §7, open-item parity, dependency sanity — and run the audit again without the flag.
7. **Hand over for approval**: present the decisions-needed list; on sign-off bump every frozen document to `Approved v1.0.0 (YYYY-MM-DD)`, switch 02/13/14 to `Living document — reflects the build through S01`, drop `-draft` everywhere, set ADRs to `accepted`, flip the README banner and fill its sign-off row, and start S01. Later scope or date changes go through 09 §10 change control; `BACKLOG.md` starts at the first review gate.

**Brownfield** (a `docs/` folder already exists): pick the matching profile, run the audit with it, build a gap table (document → exists / header / missing sections / vocabulary conflicts), reconcile vocabulary into 00 first, then fill gaps in authoring order. The brownfield audit counts as the first review gate, so where the code contradicts a document, record a BACKLOG item rather than silently editing the document to match the code (`references/quality-gates.md` §5).

## Document contract

`# NN — Title` → header block table → purpose blockquote (what it is, what it is **not**, vocabulary source) → `## Table of Contents` when over 300 lines → numbered sections and appendices → Open Items last (an optional References section may follow). Status is one of `Draft` · `Pending approval` · `Approved vX.Y.Z (YYYY-MM-DD)` · `Living document — reflects the build through Sxx` · `Superseded by …`. Identifier families, matrix legend (✓ / A / ✗ with a per-role scope legend), state-machine notation, marker syntax and living-document rules: `references/conventions.md`. Standards per document (ISO/IEC/IEEE 29148, C4/arc42, OpenAPI 3.1 + RFC 9457 + RFC 9110, OWASP ASVS 5.0 chapter names, NIST SP 800-63B, Scrum DoR/DoD, Diátaxis, SRE runbooks) and default numbers, including regulated-domain ones: `references/standards.md`.

## Common mistakes

| Mistake | What the suite does instead |
|---|---|
| Index of 20+ documents, most marked *Planned* | A profile, every document in it written; omitted ones listed as not applicable |
| Business/GTM documents (pricing, legal pack, support plan) in the engineering suite | `business/` beside `docs/` with its own README, same header block, code `BIZ`; operational support (on-call, escalation, SLO monitoring) belongs in 13 §9 |
| Glossary or domain model written after the requirements | 00 first; requirements reuse its enums verbatim |
| Roles, permissions and state rules folded into the requirements document | 07 owns the matrix, 00 owns the state machines; 06 cites both |
| Requirements as a flat list by area code | Per module: purpose, FRs, user flows, acceptance criteria, edge cases, phase & dependencies |
| The same number (timeout, retention, limit) typed in four documents | One `PRM-n` row in 00 §10, cited everywhere else |
| Stack, API conventions or phases left implicit | Locked in 00 §5–6 and 01 §6; 09 binds sprints to those phases |
| A decision taken in 03/04/05 with no ADR number | "Proposed ADR (number assigned at back-port)", numbered in 01 §7 during the consistency pass |
| Forward citations judged as errors while the suite is still being written | `--allow-missing` during authoring; the final audit runs without it |
| README without a status banner or decisions-needed list | Approval by exception: defaults stated, the approver answers only what they disagree with |
| Runbook commands written from memory | Skeleton pre-build; after S01 every command verified against the repository, with the files checked named in the purpose block |
| Editing a frozen document after approval without a CR | 09 §10 change control: raise, analyse, approve, bump version, communicate |
| Living documents describing unbuilt features as present | `*Filled during S03*`-style markers pre-build; **planned (phase X)** markers afterwards, with the build-status line bumped by the Definition of Done |

## Files in this skill

`references/` — `suite-map.md` (catalogue, orders, profiles, stable sections), `conventions.md` (header, IDs, markers, language, tables, living docs), `standards.md`, `quality-gates.md` (audit checks, per-document DoD, consistency pass, approval, brownfield, blocking inputs). `templates/` — one skeleton per document plus README, ADR, BACKLOG, deferred. `scripts/audit_suite.py` — mechanical checks, `--allow-missing` for authoring, exit 1 on any FAIL. `README.md` — installation and verification.
