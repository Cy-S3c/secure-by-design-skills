# Quality Gates — definition of done per document and for the suite

## 0. The audit script

```
python3 scripts/audit_suite.py docs/ --profile <minimal|standard|full> [--allow-missing]
```

Path relative to this skill; default profile `standard`. `--allow-missing`
is the authoring-time mode: unwritten documents, the missing README and
citations of unwritten documents report as INFO. Run without it before
approval. Exit code 1 on any FAIL.

| Severity | Meaning | Checks |
|---|---|---|
| **FAIL** | must fix | required document of the profile missing; `README.md` missing; duplicate FR id in 06; a cited `` `NN-file.md` `` that does not exist (profile documents only); README index link to a missing file |
| **WARN** | fix, or justify in the README | duplicate document number; title not `# NN — Title` or numbered differently from the file; header lacking Document ID / Product / Version / Status / Last updated; Document ID not `PREFIX-CODE-NNN` or prefix differing from the suite; unknown Status; `-draft` inconsistent with status (status values are checked by prefix: `Approved vX.Y.Z (YYYY-MM-DD)` in full, `Living document — …`, `Superseded by …`); non-ISO date; > 300 lines without a `## Table of Contents` heading; TOC links not matching a heading; template remnants outside code (`{{PRODUCT}}`-style tokens, `<!--` comments, `— ln` sizes, headings with `<placeholder>`); FR / ADR / S##-B# referenced but not defined; FR in 06 but in no 09 sprint row (`FRs:` / `implied:`) and not in `deferred.md`; 06 Appendix A disagreeing with 09 or still holding `— (09 pending)` cells; a document missing from the README index; template remnants in README, `adr/`, `deferred.md` or `BACKLOG.md`; citation of a `§n` that is not a section of the target; markdown link to a missing file; permission string in 05/06/12 absent from 07 (or 05 §2.5); README missing status banner, review order or decisions-needed; README size drifting > 10 % from `wc -l`; README decisions fewer than 01 §10; `deferred.md` missing once 06 exists; `api/openapi.yaml` missing or without an `openapi: 3.x` line when 05 names it |
| **INFO** | awareness | `[CANON-PENDING: Term]` markers with the terms to back-port; `*Filled during Sxx*` markers; "Proposed ADR" phrases in 03/04/05; citations of `§n.m` where only `§n` exists; permissions no requirement or endpoint cites; counts of named / implied / deferred FRs; optional documents not present; `adr/` absent |

The judgement items below are checked by reading.

## 1. Every document

- [ ] Title `# NN — Title`; header block with the required rows and, unless there is a reason, Owner, Audience, Depends on, Consumed by.
- [ ] Purpose blockquote: what the document is, what it is not, the vocabulary source.
- [ ] Table of contents when over ~300 lines.
- [ ] No term, role, status, enum or number that is absent from its owning document (00 for vocabulary, 00 §10 for shared parameters, 10/11/12/05/07 for their owned families).
- [ ] Cross-references are `file.md §n`; none restate another document's content.
- [ ] Every ID used is defined in its owning document; every ID owned is unique.
- [ ] An Open Items section, numbered, each with a recommended default; assumptions explicit.
- [ ] Size recorded in the README index.

## 2. Per document

**00** — roles a closed set with enum names and tiers; external principals in §2.1; every entity has owner, lifecycle, relationships; every enumeration lists all values; every state machine has a transitions table and immutability rules; stack has versions; glossary covers every domain term used in 01–09; parameter register holds every shared number.

**01** — each goal has metric, target and horizon; non-goals concrete; each phase has exit criteria and a target window; ADR rows have rationale and, where a record exists, a link; risks have mitigations; each open question has a default.

**07** — scope legend defines `A` per role; matrix covers every permission string used in 05, 06 and 12; each role has may / may-not; SoD rules are `SOD-n` invariants; external principals have structural prohibitions; audit action registry complete.

**10** — sources stated (corpus, or published rules plus a pilot validation gate when greenfield); every field has type, required flag and validation; computed values have bands; a release gate exists; one block per sub-standard.

**06** — one FR per behaviour with concrete values; phase tags listed in §1.2; every module has acceptance criteria, edge cases and a phase/dependency table; the Depends/Feeds graph across modules is acyclic; feature catalogue matches 01's module map; Appendix A present (`— (09 pending)` or regenerated from 09).

**04** — every entity in 00 §3 has a table; every enum in 00 §4 appears in the enum → type map; every table has keys, temporal columns, soft-delete policy and tenancy decided; database roles and RLS stated; indexes justified by a query pattern; retention per entity; migrations and seed stated. Optional gate: the DDL runs on a throwaway database.

**05** — conventions complete; every FR with an API surface has an endpoint; every endpoint has a permission gate and idempotency column; error types stable with 409 / 412 / 422 / 428 / 400 used as `standards.md` lists; envelope defined once; `api/openapi.yaml` is a valid skeleton pre-build and reaches parity with the catalogue by the first API sprint.

**03** — C4 L1–L2 (L3 for the core service); module catalogue with events; deployment for dev and prod; observability with SLOs; wireframes per the profile rule; ADR-001 with trade-off table.

**08** — framework table with section traceability using ASVS 5.0 chapter names; regulation safeguard map when one applies; STRIDE row per component in 03 §1; abuse cases ranked with controls; §2.3 names every trust boundary; when `security/threat-model/` exists, §2 links its summary and the `A#` ids match the model's refs; every control cites its enforcement point; severity classes defined before any document cites them; release checklist QA can execute.

**09** — phases bind to 01 §6; module map equals 06 §1.4; every sprint has goal, `S##-B#` rows with Modules and Notes (`FRs:` / `implied:`), and a demo/exit line; DoR and DoD enumerated (DoD covers 02/13/14 upkeep); RACI columns follow 01 §8; milestones dated from a stated kickoff; risk register with triggers; change control with version-bump rules; a reserve or later-phases section.

**11 / 12** — tokens defined once; reserved palettes named; `DP-n` principles; every screen has route, roles, wireframe, states, interactions, API notes; appendices for shared copy and keys; open items.

**02 / 13 / 14** — pre-build rules of `conventions.md` §8 (status, build-status line, `*Filled during Sxx*`); 02 complete per module; 13 configuration reference complete (name, default, secret?); 14 capability table sourced from 07 §4.

**README** — status banner; profile; locked stack; both orders; index with real sizes incl. `adr/`, `deferred.md`, `api/`; not-applicable list with reasons; phase summary; decisions snapshot; decisions needed (01 §10 plus blocking items by source); WARN justifications; next step.

## 3. Suite-level consistency pass

Run once after the last frozen document and again before approval:

1. **Vocabulary sweep** — grep every role, status, entity and enum across `docs/`; anything not in 00 (and not in an owned vocabulary, `conventions.md` §5) is a defect. Back-port `[CANON-PENDING]` terms if 00 was already approved.
2. **Parameter sweep** — every shared number appears once in 00 §10 and is cited elsewhere.
3. **Module parity** — 01 §4 = 06 §1.4 = 03 §3 = 09 §1.3 (names may differ by layer; the 09 map lists them).
4. **Requirement coverage** — every FR appears in a 09 sprint row or `deferred.md`; 06 Appendix A regenerated from 09.
5. **Permission parity** — every `resource.action` in 05/06/12 exists in 07's matrix (05 §2.5 in Minimal); unused permissions reviewed.
6. **Security parity** — every abuse case names a control; every control names its enforcement point.
7. **Decision parity** — every ADR in 03/04/05 appears in 01 §7; every "Proposed ADR" is numbered; `adr/` files match the rows that link them.
8. **Open-item parity** — README decisions = 01 §10 plus blocking items from other documents.
9. **Dependency sanity** — 06 module graph acyclic; 09 sprint order respects it.
10. **Sizes and dates** in the README match the files; final audit without `--allow-missing` is clean or every WARN is justified in the README.

## 4. Approval workflow

1. Suite status `Pending approval`; README lists the decisions needed with the author's defaults.
2. Approver answers by exception (silence = default accepted) and records the sign-off: name, date, suite version.
3. Authors apply answers, bump each frozen document to `Approved v1.0.0 (YYYY-MM-DD)`, switch 02/13/14 to `Living document — reflects the build through S01`, remove `-draft` everywhere, set ADR status `accepted`, flip the README banner and fill its sign-off row (name, date, suite version).
4. Development starts at the first sprint in 09.
5. Afterwards, scope/phase/date changes go through 09 §10 change control: CR raised → impact analysis → approve → version bump → milestone table updated → communicated.

## 5. Brownfield audit (existing project)

1. Pick the profile that matches the product, then run the audit with it.
2. Build a gap table: suite document → exists? → header? → sections missing → vocabulary conflicts.
3. Reconcile vocabulary into 00 first (the usual finding is three names for one entity).
4. Fill gaps in authoring order; never rewrite an accurate document just to match a template.
5. The brownfield audit counts as the first review gate: where the code contradicts a document, record a BACKLOG item rather than silently editing the document to match the code.

## 6. Inputs that block, inputs that become assumptions

Before writing, four inputs must come from the owner: the hosting and
tenancy model, the compliance driver, the role set, and the phases wanted.
Without them, stop and ask (`superpowers:brainstorming`). Everything else —
team size, dates, stack details, specialities, metric targets — becomes an
assumption in 01 §8 or an open question in 01 §10 with a recommended
default, and the suite proceeds.
