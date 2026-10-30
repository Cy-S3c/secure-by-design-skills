---
name: threat-modeling-stride
description: Use when a system needs a threat model — before development from its planning documents (architecture, data model, API, roles, security design) or on an existing codebase — producing a STRIDE-per-element analysis, data-flow diagrams with trust boundaries, a rated and owned threat register, and a self-contained HTML report; also when someone asks "what are the threats", "do a DFD", or "is the security design complete".
metadata:
  origin: personal
  version: 1.1.1
---

# Threat Modeling (STRIDE per element)

## Overview

A threat model is **a data-flow diagram with trust boundaries, every
element of which has been asked the six STRIDE questions, with each answer
rated, owned and disposed**. It is a design-time activity: the planning
suite (`product-documentation-suite`) already contains every input a DFD
needs — components and flows (03), data and its sensitivity (04), entry
points (05), principals (07), boundaries and abuse cases (08) — so the model
is built and reviewed before code exists and re-run at each architecture
change. Output is one model file and one generated HTML report.

## When to use

- A planning suite reaches `Pending approval` and 08 §2 needs to be more than a table: produce the model, link the summary from 08 §2.
- An existing system has no threat model, or a new store, flow across a boundary or third party is added.
- A release gate or audit asks for evidence that STRIDE coverage is complete.

Not for: penetration-test planning (use the security test report), code review of one function, or compliance mapping on its own (08 §1.2).

## Workflow

1. **Scope** — fill `meta` in a copy of `templates/model.example.yaml`: system, version, date, source (suite version or commit hash), scope in/out, authors.
2. **Draw the DFD in the model file** (`references/dfd-rules.md`): boundaries from 08 §2.3 (or the default six), external entities from 00 §2, processes and stores from 03 §1, flows from 03 §4/§8 and 05 §3 (at the public edge one flow per principal per API surface, endpoint groups listed in `data`; one flow per hop between processes and stores), classification from 04 §6. Run `python3 scripts/build_report.py model.yaml --check` until it validates: no orphan element, every flow between known elements, every element in a boundary.
3. **Enumerate threats per element** (`references/stride-per-element.md`), recording every source disagreement you meet as a `divergences` entry (document vs document, document vs code — each is a finding): walk the element × category matrix cell by cell, cross-boundary flows and processes first; import 08 §2.2 abuse cases as threats with their `A#` in `refs`. Every threat has a `target` id, a category the element type admits, a description with attacker, precondition, action and effect.
4. **Rate and dispose** (`references/risk-rating.md`): likelihood and impact 1–5, existing controls with citations (08 §n or code path), mitigation naming the control, status, owner, plan row when open. Record `no_threat` entries with a reason for cells you assessed and found empty, so the coverage matrix shows judgement rather than omission. For leadership, add `headline` (a short plain title), `plain` (what could happen, in business terms), `plain_fix` and `effort` (S/M/L) to every open Critical/High and to the top open threats, and write `meta.summary` (two or three paragraphs) and `meta.decisions` (what leadership must approve: ask, why, owner, by, threats); the validator warns when they are missing.
5. **Generate**: `python3 scripts/build_report.py model.yaml -o threat-model.html` writes the HTML (default name `threat-model.html` beside the model) in two parts — Part A for leadership (brief, posture tiles, top risks in plain terms, decisions needed, ownership, glossary) and Part B for engineering (scope, zoomable DFDs, components, flows, assets, filterable register with expandable records, coverage matrix, heat map, plan, divergences, method) — with an audience switch and a print stylesheet; inline SVG DFDs via Graphviz — without Graphviz the page falls back to a Mermaid block loaded from a CDN and is no longer self-contained), `dfd-l0.svg`, `dfd-l1.svg` and `threat-model-summary.md`. `WARN` lines are rule reminders; fix them before filing. Read the coverage matrix and the heat map in the report: red cells are unassessed, not safe.
6. **Review and file** (`references/workflow.md` §7–§9): second reader, then `docs/security/threat-model/` holds the four files; the summary is linked from 08 §2 or the README; open threats become 09 rows or BACKLOG items.

Script path is relative to this skill. Requirements: Python 3.9+, PyYAML (or write the model as JSON), Graphviz `dot` for inline diagrams.

## Model file (shape)

`meta` (system, version, date, source, authors, scope_in/out; optional `classification`, `status`, `summary`, `decisions[]` with ask/why/owner/by/threats) · `boundaries[]` (`B-n`) · `elements[]` (`E-n` entity, `P-n` process, `D-n` store; each with `boundary`; optional `principal`, `doc`, `classification`, `audit: true` for stores holding audit data) · `flows[]` (`F-n`: from, to, name, protocol, data, classification) · `assets[]` · `assumptions[]` · `threats[]` (`T-n`: target, category, title, description, likelihood, impact, existing, mitigation, status, owner, refs; `sprint` or `plan` when open, `approver` + `revisit` when accepted, `agreement` when transferred; optional `headline`, `plain`, `plain_fix`, `effort` for the executive brief) · `no_threat[]` (target, category, reason) · `divergences[]` (`V-n`: between, description, resolution, threats). Full example: `templates/model.example.yaml`.

## Common mistakes

| Mistake | What this skill does instead |
|---|---|
| One diagram with no trust boundaries, threats listed per component in prose | Boundaries are first-class; every flow crossing one is marked; STRIDE is applied per element, and the matrix shows every cell |
| "Spoofing of the database", "tampering by the user" | The validator rejects categories the element type does not admit (entities: S R; stores: T R I D; flows: T I D) |
| Severity words without a scale | Likelihood × impact on 1–5 scales with written anchors; bands computed, heat map drawn |
| Mitigation = "validate input", "use encryption" | Mitigation names the control and where it lives (08 §n or a code path); open ones carry an owner and a `sprint` or `plan`; brownfield `mitigated` means designed **and** present in code |
| Abuse cases in 08 and threats in the model drift apart | 08 §2.2 cases are imported as threats with their `A#`; the summary links back from 08 §2 |
| Critical risk quietly "accepted" | The validator requires a named approver on any accepted Critical/High |
| Diagram and model disagree | The diagram is generated from the model; edges carry flow ids and the flow table is the legend; nothing is drawn by hand |
| Model written once | `meta.version` bumps at every architecture change; the previous HTML is kept |

## Files in this skill

`references/stride-per-element.md` (applicability matrix, prompts, mitigation vocabulary with CWE/ASVS), `dfd-rules.md` (sources, levels, rules), `risk-rating.md` (scales, statuses), `workflow.md` (end-to-end steps, greenfield vs brownfield, report contents). `templates/model.example.yaml`. `scripts/build_report.py` (validate, derive, render, write) with `report_html.py` (the two-part page), `tm_common.py` (shared rules) and `assets/report.css`, `assets/report.js` (inlined into the page). `README.md` — requirements, installation and verification.
