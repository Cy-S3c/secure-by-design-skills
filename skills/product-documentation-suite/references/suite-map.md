# Suite Map — the documents, what each must contain, and the order to write them

The suite is a set of numbered Markdown files under `docs/`. Numbers are
stable identifiers (people say "doc 06 §2.2"). The authoring order and the
review order differ; both are given below.

## 1. The catalogue

**IDs owned** = identifier families this document is the source of truth for.
**Life**: *frozen* = versioned and approved before build; *living* = updated
every sprint. Sizes are what a complete suite typically reaches; a shorter
document keeps every mandatory section (`conventions.md` §6, size caps).

| # | Document | Purpose | Must contain | IDs owned | Depends on | Life | Typical size |
|---|---|---|---|---|---|---|---|
| 00 | **Canonical Model** | Single source of truth for vocabulary; every other document cites it and never redefines a term. | Product identity; roles (closed set, enum names, tiers) and external principal types; entities with definition, owner, lifecycle and relationships; enumerations (compact table) and state machines (diagram + transitions table); locked stack with versions; API conventions (tenancy, concurrency, time semantics); authorization model incl. any field-level layer; Document ID register; glossary; parameter register; open items | role enums, entity names, enum values, `PRM-n`, document codes | — | frozen | 200–350 |
| 01 | **Product Design Document** | Why the product exists, for whom, what is in and out of scope. | Vision; problem statement; goals with metric, target and horizon; non-goals; personas; pillars; module map; master journey; release phases with exit criteria and target windows; condensed ADR table with a record link; constraints & assumptions; top risks; numbered open questions with a recommended default | `ADR-NNN`, phase names, Phase exit criteria | 00 | frozen | 200–300 |
| 02 | **Product Documentation** (user guide) | Task-oriented end-user guide per module, non-technical. | Getting started; navigation map; one how-to per module in 06 §1.4 order (UI labels from 12); best practices; FAQ; glossary pointing to 00; open items. Written in full before approval; living after | — | 00, 01, 06, 07 §8, 12 | living | 400–1,200 |
| 03 | **Architecture** | How the system is built and deployed, with the decisions that shape it. | C4 context + container (+ component for the core service); architectural-style ADR with trade-off table (ADR-001 lives here); module catalogue (responsibility, entities, API prefix, events in/out, phase — envelope cited from 05 §6.1); request lifecycle; background jobs; caching; key data flows; deployment (dev, prod, environments table, configuration pointer, backup/DR); observability with SLOs; wireframes (≤ 6 journeys when 12 exists, else the ten most important screens); open items | module names, SLOs | 00, 01, 05 | frozen | 500–1,100 |
| 04 | **Data Model** | Physical schema and every rule the database enforces. | Principles table (keys, temporal, actor, soft delete, tenancy with composite FK pattern, enums, JSON, audit, rich text, binaries, time semantics, encryption); database roles & row-level security; ERD; per-table DDL with constraints and indexes; JSON contracts; index register and query patterns; retention & erasure; migrations & seed; cache keys; volume estimates; enum → type map; traceability to 00; open items. Optional gate: run the DDL on a throwaway database | table/column/index names, `P<n>` | 00, 01, 10, 07, 06 | frozen | 500–2,000 |
| 05 | **API Documentation** | The contract humans read; `api/openapi.yaml` is the machine copy (a skeleton pre-build, full parity by the first API sprint). | Conventions (no personal data in query strings; search as POST); authentication flows; token lifecycle; scope model (role → permission table in the Minimal profile); 401/403/404 policy; endpoint catalogue with permission and idempotency columns; payloads; error catalogue with stable `type`s (409 state/duplicate, 412 precondition failed, 422 validation and idempotency mismatch, 428 precondition required, 400 missing idempotency key); event envelope and catalogue; isolation of external surfaces; versioning & deprecation; OpenAPI conventions (`x-permission`, `x-scope`); open items | problem types, event names, envelope | 00, 04, 07, 06 | frozen | 400–900 |
| 06 | **Features & Functions** | Functional specification: every requirement testable and numbered. | Scope; phase table with tagged FR ids; conventions; feature catalogue (`F#`, phase, roles, entities); per module: purpose, `FR-x.y` requirements, user flows, Given/When/Then acceptance criteria, edge cases, phase & dependencies (acyclic across modules); Appendix A FR → sprint (`— (09 pending)` until 09 exists); open items | `F#`, `FR-x.y` | 00, 01, 07, 10 | frozen | 500–1,200 |
| 07 | **Roles & Permissions** | Who may do what, on which objects, with the separation-of-duties rules. | Authorization model with a scope legend (what `A` means per role); role definitions (mission, scope, may / may not — including zero-standing-access platform roles with break-glass); positions vs global roles; master permission matrix grouped by resource with legend and footnotes; per-role walkthroughs; separation of duties as `SOD-n` invariants; external principals with structural prohibitions; landing pages & navigation; audit action registry; open items | `resource.action`, `SOD-n`, audit actions | 00 | frozen | 300–600 |
| 08 | **Security Design** | Threats, controls, and the evidence a reviewer needs. | Objectives; framework table with traceability (ASVS 5.0 chapter names) and a regulation safeguard map when one applies; STRIDE with one row per component in 03 §1; prioritised abuse cases; trust boundaries; identity & authentication decisions; authorization enforcement; validation & encoding per context; data protection; hardening (CSP, headers, CORS, rate limits); audit & alerting; secure SDLC gates; incident response with severity classes `Sev-n`; release acceptance checklist; open items | `A#`, `Sev-n`, alert rule names | 00, 03, 04, 05, 07 | frozen | 400–800 |
| 09 | **Development Plan** | The executable delivery programme. | Cadence & calendar; phase mapping (binding, from 01 §6); module ID map copied from 06 §1.4 and the Notes syntax (`FRs:` / `implied:`); DoR; DoD (incl. 02/13/14 upkeep); branching; environments (cite 03 §9.3); release cadence; feature flags; team & RACI (columns from 01 §8); per-sprint blocks (goal, numbered `S##-B#` rows with Modules and Notes, demo/exit); later phases & reserve; milestones dated from kickoff; quality strategy; risk register `R#` with triggers; dependencies & procurement; change control `CR-n`; open items | `S##-B#`, `M#`, `R#`, `CR-n` | 00, 01, 06, 08, 03 §9.3 | frozen (re-baselined by change control) | 400–800 |
| 10 | **Domain Specification** (only when a domain standard exists) | The product's domain standard — a report format, a form schema, a message standard, a protocol — versioned as its own standard. | Sources & method (corpus or, for greenfield, the published rules it derives from and the pilot validation gate); structure; record schema; computed values, bands and rules; variants/profiles; generation or rendering contract with acceptance criteria; release gate; open items. One §2–§7 block per sub-standard when there are several | domain keys, presets, document-local rule ids | 00, 07 (when fields are permission-gated) | frozen | 150–600 |
| 11 | **Design System** | How everything looks and behaves visually, defined once. | Design principles `DP-n`; brand; colour (semantic + reserved palettes, light/dark); typography; iconography; spacing & shell; motion; theming; components with anatomy and states; UX writing; accessibility standard; open items | `DP-n`, tokens, component names | 00, 03 | frozen | 250–600 |
| 12 | **Screen Specifications** | Build-ready contract per screen. | How-to-read block; per screen: identity table, ASCII wireframe, component inventory, states, interactions, API & permission notes; appendices (empty-state copy, keyboard map, skeletons, responsive matrix, notification routing, open items) | `SCR-###` | 00, 03, 05, 07, 11 | frozen | 350–3,000 |
| 13 | **Operations Runbooks** | Copy-pasteable procedures verified against the repository (skeleton before code). | Topology & ports; deploy; configuration reference (name, default, secret?); first boot; backup & restore per store incl. what is lost; incident playbooks (severities from 08 §10.1); credential rotation; domain operations; monitoring, alerting & on-call (health endpoints, logs, alert-worthy events, SLO monitoring vs 03 §10, rota & escalation, not-yet-available list); open items | — | 03, 04, 08, code | living | 200–1,000 |
| 14 | **Administrator Guide** | What privileged roles can do, task by task (design intent from 07 until the identity sprint lands, then as implemented). | Capability table; user lifecycle; tenant onboarding checklist; operational setup; governance workflows with stage-by-stage authorization; audit review cadence; notifications; open items | — | 02, 07, 13, code | living | 150–500 |
| — | **README** (suite index) | Entry point (code IDX). | Header with Document ID, version, date and sign-off row; product one-liner; suite version; status banner; profile; locked stack; authoring and review order; index with real sizes (adr/, deferred.md, api/ rows included); not-applicable list with reasons; phase summary; decisions snapshot; **Decisions needed** (01 §10 plus blocking items from other documents, by source); WARN justifications; next step | — | all | living | 80–150 |
| — | `docs/adr/ADR-NNN-title.md` | Full records for decisions whose alternatives deserve a page (zero files is fine). | Context, decision, alternatives, consequences, status (`proposed` until suite approval) | `ADR-NNN` (shared with 01 §7) | — | frozen per record | 40–100 each |
| — | `docs/deferred.md` | Requirements with no sprint row, owner deferrals. Exists from the moment 06 does. | Header line; `none` or one entry per FR with reason and revisit trigger | — | 06, 09 | living | short |
| — | `BACKLOG.md` (repo root) | Post-review improvement backlog. Starts at the first review gate, never pre-approval. | Generation note; P0/P1/P2; items with size, problem, fix, file pointers | — | code review | living | varies |

Optional: `15-portal-guide.md` (external-user guide), `16-ai-governance.md`,
`security/S##-…-report.md` (per gate, created when the gate runs), `security/threat-model/` (the STRIDE-per-element model, DFDs, HTML report and summary that the `threat-modeling-stride` skill produces from 00/03/04/05/07/08; 08 §2 links the summary), `research/`.

## 2. Authoring order (dependency order)

Each document cites only documents already written; forward citations are
allowed only where a template header asks for *Consumed by*. Run the audit
with `--allow-missing` while writing.

1. **00 Canonical Model** — vocabulary first; add terms here before using them anywhere.
2. **01 Product Design Document** — scope, phases, condensed ADRs (create `adr/` records as decisions are numbered), open questions.
3. **07 Roles & Permissions** — the permission strings that 10, 06, 05 and 08 cite.
4. **10 Domain Specification** — only when a domain standard exists.
5. **06 Features & Functions** — requirements and acceptance criteria; Appendix A sprint cells read `— (09 pending)`; create `docs/deferred.md` (`none`).
6. **04 Data Model** — entities from 00, fields from 10, access rules from 07, ranges from 06.
7. **05 API Documentation** + `api/openapi.yaml` skeleton — resources from 04, gates from 07, flows from 06.
8. **03 Architecture** — modules, lifecycle, deployment, journey wireframes; cites 05's envelope.
9. **08 Security Design** — threat model over 03, controls over 04/05/07.
10. **09 Development Plan** — sprints sized from 06, gates from 08, decisions from 01.
11. **11 Design System → 12 Screen Specifications** — products with a UI.
12. **02 User guide (in full), then README, then 13/14 skeletons** — the approver reads the product from the user's seat; README from real sizes and 01 §10, sizes refreshed once the skeletons exist.
13. **Consistency pass** (`quality-gates.md` §3): regenerate 06 Appendix A from 09; number proposed ADRs into 01 §7; back-port `[CANON-PENDING]` terms if 00 was already approved; sweep parameters into 00 §10; run the audit without `--allow-missing`.

## 3. Review order (for the approver)

README first (the entry point), then
`00 → 01 → 10 → 03 → 04 → 07 → 06 → 05 → 08 → 09 → 02`, then `11 → 12` if
present. Living documents (13, 14, BACKLOG.md, deferred.md) are reviewed at
sprint reviews, not at suite approval.

Authoring follows **dependencies** (a document cites only what exists);
review follows **comprehension** (a reader needs vocabulary and intent before
mechanics): vocabulary, intent, domain standard, shape of the system, data,
who may touch it, what it does, the contract, how it is protected, how it
gets built.

## 4. Suite sizing

| Profile | When | Documents |
|---|---|---|
| **Minimal** | Internal tool, API-only service, or a product with ≤ 3 roles and no external users (several consuming teams do not rule this out) | 00, 01, 03, 06, 04, 05, 08, 09, 13, README, `deferred.md` — no 07: the role set stays in 00 §2, the authorization model in 00 §7, and `resource.action` strings live in a role → permission table in 05 §2.5, which the permission-parity gate checks instead. Split 07 out when a permission needs a scoped `A` cell **or** the role set grows past 3 |
| **Standard** | Multi-role product with a UI | Minimal + 07, 02, 14, 11 |
| **Full** | Multi-role, regulated or security-sensitive, external users, or a domain standard | Standard + 12, `adr/`; 10 when a domain standard exists; `BACKLOG.md` and `security/` appear at the first review gate, not before |

Record the profile in the README and list every omitted document as *not
applicable* with a one-line reason.

## 5. Stable sections (cite these; sub-sections may drift)

| Doc | Top-level sections |
|---|---|
| 00 | 1 Product Identity · 2 User Roles (2.1 external principals) · 3 Core Domain Entities · 4 Enumerations & State Machines · 5 Tech Stack · 6 API Conventions · 7 Authorization Model · 8 Document ID Register · 9 Glossary · 10 Parameter Register · 11 Open Items |
| 01 | 1 Vision (1.1 problem, 1.2 goals, 1.3 non-goals) · 2 Personas · 3 Pillars · 4 Module Map · 5 End-to-End Workflow · 6 Release Phases · 7 Key Product Decisions · 8 Constraints & Assumptions · 9 Risks · 10 Open Questions for Approval |
| 02 | 1 Getting Started · 2 Navigation Map · 3 Module How-Tos · 4 Best Practices · 5 FAQ · 6 Glossary · 7 Open Items |
| 03 | 1 Architecture Overview · 2 ADR-001 Architectural Style · 3 Module Catalogue · 4 Request Lifecycle · 5 Frontend Architecture · 6 Background Jobs · 7 Caching · 8 Data Flows · 9 Deployment (9.1 dev, 9.2 prod, 9.3 environments, 9.4 configuration, 9.5 backup & DR) · 10 Observability · 11 UI Wireframes · 12 Open Items · 13 References |
| 04 | 1 Design Principles (1.4 database roles & RLS, 1.5 tenancy pattern) · 2 ERD · 3 Table Definitions · 4 JSON Schema Contracts · 5 Indexes & Performance · 6 Data Lifecycle & Retention · 7 Migrations & Versioning (7.1 seed) · 8 Cache Key Schema · 9 Volume Estimates · 10 Enum → Type Map · Appendix A Traceability · Appendix B Open Items |
| 05 | 1 Overview · 2 Authentication & Authorization (2.4 token lifecycle, 2.5 scope model) · 3 Endpoint Catalogue · 4 Schemas · 5 Error Catalogue · 6 Webhooks & Events (6.1 envelope, 6.3 catalogue) · 7 External Surface Isolation · 8 Versioning & Deprecation · 9 OpenAPI & Collections · 10 Open Items |
| 06 | 1 Introduction (1.2 phases, 1.3 conventions, 1.4 catalogue) · 2… one section per module · Appendix A FR → Sprint · Appendix B Open Items |
| 07 | 1 Authorization Model & Scope Legend · 2 Role Definitions · 3 Positions vs Global Roles · 4 Master Permission Matrix · 5 Per-Role Walkthroughs · 6 Separation of Duties (SOD-n) · 7 External Principals · 8 Landing Pages & Navigation · 9 Audit Action Registry · 10 Open Items |
| 08 | 1 Objectives & Compliance (1.1 ASVS traceability, 1.2 regulation map) · 2 Threat Model (2.1 STRIDE, 2.2 abuse cases) · 3 Identity & Authentication (3.4 session model) · 4 Authorization · 5 Validation & Encoding · 6 Data Protection (6.3 key management) · 7 Hardening · 8 Audit Logging & Monitoring (8.3 alert rules) · 9 Secure SDLC · 10 Incident Response (10.1 severity classes) · 11 Security Acceptance Checklist · 12 Open Items · 13 References |
| 09 | 1 Delivery Approach (1.2 phase mapping, 1.3 module map, 1.4 DoR, 1.5 DoD, 1.7 environments, 1.9 flags) · 2 Team & Capacity · 3 Phase 1 · 4 Phase 2 · 5 Later Phases & Reserve · 6 Milestones · 7 Quality Strategy (7.7 security gates) · 8 Risk Register · 9 Dependencies & Procurement · 10 Change Control (10.1 change log) · 11 Open Items |
| 10 | 1 Sources & Method · 2 Structure · 3 Record Schema · 4 Computed Values, Bands & Rules · 5 Variants · 6 Generation / Rendering Contract · 7 Release Gate · 8 Open Items |
| 11 | 1 Design Principles · 2 Brand · 3 Colour · 4 Typography · 5 Iconography · 6 Spacing & Shell · 7 Motion · 8 Theming · 9 Components · 10 UX Writing · 11 Accessibility · 12 Open Items |
| 12 | 0 How to Read · route-group sections with `SCR-###` · Appendices A–E · Appendix F Open Items |
| 13 | 1 Topology & Ports · 2 Deploy · 3 Configuration Reference · 4 First Boot · 5 Backup & Restore · 6 Incident Response · 7 Credential Rotation · 8 Domain Operations · 9 Monitoring, Alerting & On-call · 10 Open Items |
| 14 | 1 Capabilities · 2 User Lifecycle · 3 Tenant Onboarding · 4 Operational Setup · 5 Governance Workflows · 6 Audit Review · 7 Notifications · 8 Open Items |
