# threat-modeling-stride

A Claude Code skill that produces a threat model as **a data-flow diagram
with trust boundaries, every element of which has been asked the six STRIDE
questions, with each answer rated, owned and disposed**, from a product's
planning documents or from an existing codebase. Part of
[Secure by Design Skills](https://github.com/Cy-S3c/secure-by-design-skills).

The layout is the [Agent Skills](https://agentskills.io) one: `SKILL.md`
holds the instructions Claude follows, `references/` the rules (STRIDE per
element, DFD rules, risk rating, workflow), `templates/model.example.yaml`
the model shape, and `scripts/` the generator. The version is
`metadata.version` in `SKILL.md`.

## What it produces

One model file and, generated from it beside the model:

| File | Contents |
|---|---|
| `model.yaml` | scope, boundaries `B-n`, elements (`E-n` entities, `P-n` processes, `D-n` stores), flows `F-n`, assets, assumptions, threats `T-n`, explicit `no_threat` decisions, divergences `V-n` |
| `threat-model.html` | one self-contained page with an audience switch and a print stylesheet. **Part A, for leadership:** executive brief, posture tiles, top risks in plain terms, decisions needed, who owns what, how to read the report. **Part B, for engineering:** scope and assumptions, zoomable L0 and L1 data-flow diagrams, boundaries and components, flows, assets, a filterable threat register with expandable records, the STRIDE coverage matrix, the 5×5 heat map, the mitigation plan, divergences, method |
| `dfd-l0.svg`, `dfd-l1.svg` | the diagrams, generated from the model so they can never disagree with it |
| `threat-model-summary.md` | counts, open Critical/High, decisions, ownership table, all threats, coverage gaps, divergences; the file the security design document or a README links |

Rating is likelihood × impact on written 1–5 scales. Bands: **Critical**
20–25, **High** 12–19, **Medium** 6–11, **Low** 1–5. Statuses: `open` (with
a sprint row or plan item), `mitigated` (control cited; in a codebase, present
in the code), `accepted` (named approver and revisit date), `transferred`
(agreement named). The validator refuses a category the element type cannot
have (entities: S R; stores: T R I D; flows: T I D) and an accepted Critical
or High threat without an approver.

## How Claude uses it

1. **Scope**: system, version, date, source (suite version or commit),
   what is in and out.
2. **Draws the DFD in the model file**: boundaries, external entities,
   processes, stores, one flow per principal per API surface at the public
   edge and one per hop inside, with data classification. Runs
   `build_report.py --check` until it validates.
3. **Enumerates threats per element**, cross-boundary flows and processes
   first, importing the abuse cases from the security design document, and
   recording every disagreement between sources as a divergence.
4. **Rates and disposes** each threat: likelihood, impact, existing controls
   with citations, mitigation naming the control, status, owner, plan. Writes
   the plain-language `headline`, `plain`, `plain_fix` and `effort` for every
   open Critical/High, plus `meta.summary` and `meta.decisions` for leadership.
5. **Generates** the report, reads the coverage matrix and heat map (red cells
   are unassessed, not safe), and fixes every `WARN`.
6. **Review and file**: a second reader, then `docs/security/threat-model/`
   holds the files and the summary is linked from 08 §2 (greenfield) or the
   README (brownfield). Open threats become sprint rows or BACKLOG items.

## Requirements

| Need | Why | Install |
|---|---|---|
| Python 3.9+ | runs the generator | system package or python.org |
| PyYAML | reads `model.yaml` (a model written as JSON needs no extra package) | `pip install pyyaml` |
| Graphviz `dot` | draws the data-flow diagrams inline, so the report is one self-contained file | `sudo apt install graphviz` · `brew install graphviz` · `choco install graphviz` |

Without Graphviz the report still builds; the diagrams fall back to a
Mermaid block loaded from a CDN, so that page needs network access to show
them.

## Install

From a clone of this repository, user level (every project on this machine):

```bash
cp -r skills/threat-modeling-stride ~/.claude/skills/
```

Project level (committed with the repository):

```bash
mkdir -p .claude/skills && cp -r skills/threat-modeling-stride .claude/skills/
```

Or install the whole repository as a plugin; see the
[root README](https://github.com/Cy-S3c/secure-by-design-skills#installation). Start a new Claude Code session
afterwards. The skill loads when a request matches its description (a threat
model, STRIDE, a DFD, "is the security design complete") or on request: "use
the threat-modeling-stride skill".

## Verify

Validate the bundled example model (prints one `OK` line and exits 0):

```bash
python3 ~/.claude/skills/threat-modeling-stride/scripts/build_report.py \
  ~/.claude/skills/threat-modeling-stride/templates/model.example.yaml --check
```

Build the full report from it into a scratch folder and open the HTML:

```bash
mkdir -p /tmp/tm-demo
cp ~/.claude/skills/threat-modeling-stride/templates/model.example.yaml /tmp/tm-demo/model.yaml
python3 ~/.claude/skills/threat-modeling-stride/scripts/build_report.py /tmp/tm-demo/model.yaml
```

The same build, committed, is in [`examples/threat-model/`](https://github.com/Cy-S3c/secure-by-design-skills/tree/main/examples/threat-model).

## Inputs

**Greenfield**: the `product-documentation-suite` documents (00 principals,
03 components and flows, 04 data classes, 05 endpoints, 07 roles, 08 abuse
cases and boundaries, 09 sprint rows for open threats, 13 configuration).
**Brownfield**: the deployable units, module list and configuration of the
codebase, with every document-versus-code disagreement recorded as a
divergence and `mitigated` meaning the control exists in design **and** code.

## Files

| Path | Contents |
|---|---|
| `SKILL.md` | the workflow Claude follows, the model shape, common mistakes |
| `references/stride-per-element.md` | applicability matrix, prompts per category, mitigation vocabulary with CWE and ASVS references |
| `references/dfd-rules.md` | which document feeds which element, diagram levels, validation rules |
| `references/risk-rating.md` | likelihood and impact anchors, bands, status rules |
| `references/workflow.md` | end-to-end steps, greenfield versus brownfield, report contents |
| `templates/model.example.yaml` | a complete small model to copy from |
| `scripts/build_report.py` | validate, derive, render, write |
| `scripts/report_html.py`, `scripts/tm_common.py`, `scripts/assets/` | the two-part page, shared rules, CSS and JS inlined into the page |

## Update or remove

Replace or delete the folder; the skill stores nothing elsewhere. Models and
reports live in the project (`docs/security/threat-model/`).
