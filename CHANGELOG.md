# Changelog

Each skill carries its own version in `metadata.version` of its `SKILL.md`
and follows [Semantic Versioning](https://semver.org/): a new document or
report section is a minor bump, a changed rule that existing suites or models
must follow is a major bump, wording and fixes are a patch. The plugin
version in `.claude-plugin/plugin.json` is the highest skill version.

## [Unreleased]

## 2026-10-30 — first public release

### product-documentation-suite 1.1.1

- Fifteen numbered documents (00 Canonical Model through 14 Admin Guide) plus
  ADR, BACKLOG and deferred-requirements templates, written in dependency
  order from one canonical model.
- Three sizing profiles (Minimal, Standard, Full) with the documents each one
  requires and the reason a document may be omitted.
- `scripts/audit_suite.py`: mechanical checks for header blocks, identifier
  families, citations, sprint-to-requirement links, permission parity and
  the README index; `--allow-missing` for authoring time, exit 1 on any FAIL.
- Security design template (08) names every trust boundary in §2.3 and hands
  the full per-element model to `threat-modeling-stride`; the suite map and
  quality gates recognise `docs/security/threat-model/`.
- Installation and verification README.

### threat-modeling-stride 1.1.1

- STRIDE-per-element method: boundaries, elements and flows in one model
  file; the validator rejects categories an element type does not admit and
  requires a named approver on any accepted Critical or High threat.
- Data-flow diagrams (L0 and L1) generated from the model with Graphviz and
  inlined as SVG; Mermaid fallback when `dot` is absent.
- Likelihood × impact rating on written 1–5 scales, four bands, a 5×5 heat
  map and a STRIDE coverage matrix that shows unassessed cells in red.
- Two-audience HTML report: Part A for leadership (brief, posture tiles, top
  risks in plain terms, decisions needed, ownership) and Part B for
  engineering (scope, zoomable DFDs, flows, assets, filterable register,
  coverage, heat map, plan, divergences, method), with an audience switch
  and a print stylesheet.
- `threat-model-summary.md` written beside the report for linking from the
  security design document or a README.
- Divergence records (document vs document, document vs code) as first-class
  findings.
- Generator keeps the skill folder free of `__pycache__`.
- Requirements, installation and verification README.
