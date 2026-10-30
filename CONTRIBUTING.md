# Contributing

Thank you for considering a contribution. These skills are small, and the
rules below keep them that way.

## Before you open a pull request

Run the same checks the CI runs:

```bash
# documentation suite: the audit script loads and runs
python3 skills/product-documentation-suite/scripts/audit_suite.py --help

# threat modeling: the bundled example validates and builds
python3 skills/threat-modeling-stride/scripts/build_report.py skills/threat-modeling-stride/templates/model.example.yaml --check
mkdir -p /tmp/tm && cp skills/threat-modeling-stride/templates/model.example.yaml /tmp/tm/model.yaml
python3 skills/threat-modeling-stride/scripts/build_report.py /tmp/tm/model.yaml

# plugin and skill manifests
claude plugin validate .
```

If you changed `templates/model.example.yaml` or the generator, rebuild the
committed example so the two stay identical:

```bash
cp skills/threat-modeling-stride/templates/model.example.yaml examples/threat-model/model.yaml
python3 skills/threat-modeling-stride/scripts/build_report.py examples/threat-model/model.yaml
```

## Conventions

- `SKILL.md` keeps its front matter (`name`, `description`, `metadata.version`)
  and stays under 500 lines; detail belongs in `references/`.
- A rule change that existing suites or models must follow is a major version
  bump; a new document, section or report feature is minor; wording is a patch.
  Bump `metadata.version` in the skill and record the change in `CHANGELOG.md`.
- Templates are skeletons: guidance lives in `<!-- comments -->` and
  `<placeholders>` that the author deletes, never in prose the author must
  rewrite.
- Scripts use the Python standard library plus, for the threat-model
  generator, PyYAML. No other dependencies.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`,
  `refactor:`, `chore:`), scoped to the skill when it helps:
  `fix(threat-modeling): …`.

## Reporting a problem

Open an issue with the skill name, the command or prompt you used, what you
expected and what happened. For the generator, attach the model file (with any
confidential names replaced) and the exact error line.
