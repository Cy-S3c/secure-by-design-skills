#!/usr/bin/env python3
"""Build a self-contained HTML threat-model report (with DFDs) from a model file.

Usage:
    python3 build_report.py model.yaml [-o threat-model.html] [--check]

Default output: threat-model.html beside the model file. Errors (exit 1) are
structural; WARN lines are rule reminders (open threat without a plan,
unknown classification, …) and do not fail the build.

Reads YAML (PyYAML) or JSON. Validates the model (--check only validates),
renders DFD L0 and L1 with Graphviz `dot` when available (inline SVG; falls
back to a Mermaid block that needs a CDN script), computes STRIDE coverage
and risk bands, and writes beside the output: dfd-l0.svg, dfd-l1.svg,
threat-model-summary.md. Exit 1 on validation errors. The page itself is
built by report_html.py (assets/report.css and assets/report.js inlined).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tm_common import APPLICABLE, BANDS, CATEGORY, CLASSES, EFFORTS, REQUIRED, SHAPE, STATUSES, STATUSES_NEED, band, esc, plan_of  # noqa: E402
from report_html import build_html  # noqa: E402



def dq(s) -> str:
    """Escape a string for a double-quoted Graphviz label."""
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def wrap(s: str, width: int = 18) -> str:
    out, line = [], ""
    for w in str(s).split():
        if line and len(line) + 1 + len(w) > width:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    out.append(line)
    return "\\n".join(out)


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.exit("PyYAML is not installed; convert the model to JSON or `pip install pyyaml`")
    return yaml.safe_load(text)


# ----------------------------------------------------------------- validation
def validate(m: dict) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    for key in ("meta", "boundaries", "elements", "flows", "threats"):
        if key not in m:
            errs.append(f"missing top-level key '{key}'")
    if errs:
        return errs, warns
    b_ids = {b["id"] for b in m["boundaries"]}
    e_ids = {e["id"] for e in m["elements"]}
    f_ids = {f["id"] for f in m["flows"]}
    for name, ids in (("boundary", [b["id"] for b in m["boundaries"]]), ("element", [e["id"] for e in m["elements"]]),
                      ("flow", [f["id"] for f in m["flows"]]), ("threat", [t["id"] for t in m["threats"]])):
        for d, c in Counter(ids).items():
            if c > 1:
                errs.append(f"duplicate {name} id {d}")
    if e_ids & f_ids:
        errs.append(f"ids shared between elements and flows: {sorted(e_ids & f_ids)}")
    for e in m["elements"]:
        if e.get("type") not in SHAPE:
            errs.append(f"{e['id']}: type must be entity | process | store")
        if e.get("boundary") not in b_ids:
            errs.append(f"{e['id']}: boundary '{e.get('boundary')}' is not defined")
        if not e.get("name"):
            errs.append(f"{e['id']}: missing name")
    used = set()
    for f in m["flows"]:
        for end in ("from", "to"):
            if f.get(end) not in e_ids:
                errs.append(f"{f['id']}: {end} '{f.get(end)}' is not an element")
            used.add(f.get(end))
        if f.get("from") == f.get("to"):
            errs.append(f"{f['id']}: from and to are the same element")
        for key in ("name", "protocol", "data", "classification"):
            if not f.get(key):
                errs.append(f"{f['id']}: missing {key}")
        if f.get("classification") and f["classification"] not in CLASSES:
            warns.append(f"{f['id']}: classification '{f['classification']}' is not public | internal | confidential | restricted")
    for e in m["elements"]:
        if e["id"] not in used:
            errs.append(f"{e['id']}: orphan element (no flow touches it)")
    types = {e["id"]: e["type"] for e in m["elements"]}
    for t in m["threats"]:
        tgt = t.get("target")
        if tgt in e_ids:
            kind = types[tgt]
        elif tgt in f_ids:
            kind = "flow"
        else:
            errs.append(f"{t['id']}: target '{tgt}' is neither an element nor a flow")
            continue
        cat = t.get("category")
        if cat not in CATEGORY:
            errs.append(f"{t['id']}: category must be one of S T R I D E")
        elif cat not in APPLICABLE[kind]:
            errs.append(f"{t['id']}: {CATEGORY[cat]} does not apply to a {kind} ({tgt})")
        for key in ("likelihood", "impact"):
            v = t.get(key)
            if not isinstance(v, int) or not 1 <= v <= 5:
                errs.append(f"{t['id']}: {key} must be an integer 1–5")
        if t.get("status") not in STATUSES:
            errs.append(f"{t['id']}: status must be open | mitigated | accepted | transferred")
        elif t["status"] in STATUSES_NEED and not any(t.get(k) for k in STATUSES_NEED[t["status"]]):
            warns.append(f"{t['id']}: status '{t['status']}' should carry {' or '.join(STATUSES_NEED[t['status']])}")
        if t.get("status") == "accepted" and not t.get("revisit"):
            warns.append(f"{t['id']}: accepted risk without a 'revisit' date or trigger")
        if not t.get("title") or not t.get("description") or not t.get("mitigation") or not t.get("owner"):
            errs.append(f"{t['id']}: title, description, mitigation and owner are required")
        if isinstance(t.get("likelihood"), int) and isinstance(t.get("impact"), int):
            if t.get("status") == "accepted" and band(t["likelihood"] * t["impact"]) in ("Critical", "High") and not t.get("approver"):
                errs.append(f"{t['id']}: an accepted Critical/High threat needs an 'approver'")
    for t in m["threats"]:
        if t.get("effort") and t["effort"] not in EFFORTS:
            warns.append(f"{t['id']}: effort should be S | M | L")
        if (t.get("status") == "open" and isinstance(t.get("likelihood"), int) and isinstance(t.get("impact"), int)
                and band(t["likelihood"] * t["impact"]) in ("Critical", "High") and not t.get("plain")):
            warns.append(f"{t['id']}: open {band(t['likelihood'] * t['impact'])} threat without 'plain' — the executive brief will show the technical description")
    meta = m["meta"] or {}
    if meta.get("summary") is not None and not isinstance(meta["summary"], (str, list)):
        errs.append("meta.summary must be a string or a list of paragraphs")
    for i, d in enumerate(meta.get("decisions") or [], 1):
        if not isinstance(d, dict) or not d.get("ask") or not d.get("owner"):
            errs.append(f"meta.decisions[{i}]: 'ask' and 'owner' are required")
        for tid in (d.get("threats") if isinstance(d, dict) else None) or []:
            if tid not in {t["id"] for t in m["threats"]}:
                errs.append(f"meta.decisions[{i}]: threat {tid} not defined")
    if not meta.get("decisions") and any(t.get("status") == "open" and isinstance(t.get("likelihood"), int) and isinstance(t.get("impact"), int)
                                        and band(t["likelihood"] * t["impact"]) in ("Critical", "High") for t in m["threats"]):
        warns.append("meta.decisions missing — the executive brief derives 'Decisions needed' from the register; write them for leadership")
    for a_ in m.get("assets", []) or []:
        for sid in a_.get("stored_in", []) or []:
            if sid not in e_ids:
                warns.append(f"asset {a_.get('id')}: stored_in '{sid}' is not an element")
    for d in m.get("divergences", []) or []:
        for key in ("id", "between", "description", "resolution"):
            if not d.get(key):
                errs.append(f"divergence {d.get('id', '?')}: missing {key}")
        for tid in d.get("threats", []) or []:
            if tid not in {t['id'] for t in m['threats']}:
                errs.append(f"divergence {d.get('id')}: threat {tid} not defined")
    for n in m.get("no_threat", []) or []:
        tgt = n.get("target")
        kind = types.get(tgt, "flow" if tgt in f_ids else None)
        if kind is None:
            errs.append(f"no_threat: target '{tgt}' unknown")
        elif n.get("category") not in APPLICABLE[kind]:
            errs.append(f"no_threat {tgt}/{n.get('category')}: category does not apply to a {kind}")
        if not n.get("reason"):
            errs.append(f"no_threat {tgt}/{n.get('category')}: reason required")
    return errs, warns


# ----------------------------------------------------------------- derivations
def derive(m: dict) -> dict:
    by_id = {e["id"]: e for e in m["elements"]}
    bnames = {b["id"]: b["name"] for b in m["boundaries"]}
    for f in m["flows"]:
        a, b = by_id[f["from"]], by_id[f["to"]]
        f["_cross"] = a["boundary"] != b["boundary"]
        f["_from_b"], f["_to_b"] = bnames[a["boundary"]], bnames[b["boundary"]]
    for t in m["threats"]:
        t["_score"] = t["likelihood"] * t["impact"]
        t["_band"] = band(t["_score"])
        t["_target_name"] = by_id[t["target"]]["name"] if t["target"] in by_id else next(f["name"] for f in m["flows"] if f["id"] == t["target"])
    targets = [(e["id"], e["name"], e["type"]) for e in m["elements"]] + [(f["id"], f["name"], "flow") for f in m["flows"]]
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for t in m["threats"]:
        counts[(t["target"], t["category"])] += 1
    declared = {(n["target"], n["category"]): n["reason"] for n in (m.get("no_threat") or [])}
    matrix, gaps = [], []
    for tid, name, kind in targets:
        row = {"id": tid, "name": name, "kind": kind, "cells": {}}
        required = REQUIRED[kind] + ("R" if kind == "store" and by_id[tid].get("audit") else "")
        for c in "STRIDE":
            if c not in APPLICABLE[kind]:
                row["cells"][c] = None
            elif counts.get((tid, c)):
                row["cells"][c] = counts[(tid, c)]
            elif (tid, c) in declared:
                row["cells"][c] = "no-threat"
            elif c not in required:
                row["cells"][c] = "optional"
            else:
                row["cells"][c] = 0
                gaps.append(f"{tid} × {CATEGORY[c]}")
        matrix.append(row)
    m["_matrix"], m["_gaps"], m["_bnames"] = matrix, gaps, bnames
    return m


# ----------------------------------------------------------------- diagrams
def dot_l1(m: dict) -> str:
    lines = ["digraph L1 {", "  rankdir=LR; nodesep=0.35; ranksep=0.9; splines=true; fontname=\"Helvetica\"; node [fontname=\"Helvetica\", fontsize=11]; edge [fontname=\"Helvetica\", fontsize=9, labeldistance=1.5];", "  compound=true;"]
    for b in m["boundaries"]:
        members = [e for e in m["elements"] if e["boundary"] == b["id"]]
        if not members:
            continue
        lines.append(f"  subgraph cluster_{b['id'].replace('-', '_')} {{ label=\"{dq(b['name'])} ({b['id']})\"; style=\"dashed,rounded\"; color=\"#b3261e\"; fontcolor=\"#b3261e\";")
        for e in members:
            fill = {"entity": "#e7f0fb", "process": "#eaf6ea", "store": "#fff4e0"}[e["type"]]
            lines.append(f"    \"{e['id']}\" [label=\"{e['id']}\\n{wrap(dq(e['name']))}\", shape={SHAPE[e['type']]}, style=\"filled\", fillcolor=\"{fill}\"];")
        lines.append("  }")
    for f in m["flows"]:
        style = "dashed" if f["_cross"] else "solid"
        color = "#b3261e" if f["_cross"] else "#444444"
        lines.append(f"  \"{f['from']}\" -> \"{f['to']}\" [label=\"{f['id']}\", tooltip=\"{dq(f['name'])}\", style={style}, color=\"{color}\", fontcolor=\"{color}\"];")
    lines.append("}")
    return "\n".join(lines)


def dot_l0(m: dict) -> str:
    system = m["meta"].get("system", "System")
    ext = [e for e in m["elements"] if e["type"] == "entity"]
    lines = ["digraph L0 {", "  rankdir=LR; fontname=\"Helvetica\"; node [fontname=\"Helvetica\", fontsize=11]; edge [fontname=\"Helvetica\", fontsize=9];",
             f"  \"SYS\" [label=\"{dq(system)}\", shape=ellipse, style=\"filled\", fillcolor=\"#eaf6ea\", width=2.2];"]
    for e in ext:
        lines.append(f"    \"{e['id']}\" [label=\"{e['id']}\\n{wrap(dq(e['name']))}\", shape=box, style=\"filled\", fillcolor=\"#e7f0fb\"];")
    types = {e["id"]: e["type"] for e in m["elements"]}
    inbound: dict[str, list] = defaultdict(list); outbound: dict[str, list] = defaultdict(list)
    for f in m["flows"]:
        if types[f["from"]] == "entity" and types[f["to"]] != "entity":
            inbound[f["from"]].append(f)
        if types[f["to"]] == "entity" and types[f["from"]] != "entity":
            outbound[f["to"]].append(f)
    rank = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
    top = lambda fs: max((f.get("classification", "internal") for f in fs), key=lambda c: rank.get(c, 1))
    for eid, fs in inbound.items():
        lines.append(f"  \"{eid}\" -> \"SYS\" [label=\"{len(fs)} flow(s), {top(fs)}\", style=dashed, color=\"#b3261e\"];")
    for eid, fs in outbound.items():
        lines.append(f"  \"SYS\" -> \"{eid}\" [label=\"{len(fs)} flow(s), {top(fs)}\", style=dashed, color=\"#b3261e\"];")
    lines.append("}")
    return "\n".join(lines)


def render_svg(dot_src: str, prefix: str) -> str | None:
    """Render DOT to inline SVG; element ids are prefixed so two diagrams on one page stay unique."""
    if not shutil.which("dot"):
        return None
    res = subprocess.run(["dot", "-Tsvg"], input=dot_src.encode(), capture_output=True)
    if res.returncode != 0:
        sys.stderr.write("WARN  Graphviz failed; falling back to Mermaid: " + res.stderr.decode())
        return None
    svg = res.stdout.decode()
    return svg[svg.index("<svg"):].replace(' id="', f' id="{prefix}-')


def mermaid_l1(m: dict) -> str:
    out = ["graph LR"]
    for b in m["boundaries"]:
        members = [e for e in m["elements"] if e["boundary"] == b["id"]]
        if not members:
            continue
        out.append(f"  subgraph {b['id'].replace('-', '_')}[\"{b['name']}\"]")
        for e in members:
            br = {"entity": ("[", "]"), "process": ("((", "))"), "store": ("[(", ")]")}[e["type"]]
            out.append(f"    {e['id'].replace('-', '_')}{br[0]}\"{e['id']} {e['name']}\"{br[1]}")
        out.append("  end")
    for f in m["flows"]:
        arrow = "-.->" if f["_cross"] else "-->"
        out.append(f"  {f['from'].replace('-', '_')} {arrow}|\"{f['id']} {f['name']}\"| {f['to'].replace('-', '_')}")
    return "\n".join(out)


def summary_md(m: dict) -> str:  # noqa: C901
    meta = m["meta"]; threats = sorted(m["threats"], key=lambda t: (-t["_score"], t["id"]))
    by_band = Counter(t["_band"] for t in threats)
    lines = [f"# Threat model summary — {meta.get('system')} v{meta.get('version')} ({meta.get('date')})", "",
             f"Source: {meta.get('source')}. Elements {len(m['elements'])}, flows {len(m['flows'])} ({sum(1 for f in m['flows'] if f['_cross'])} cross-boundary), threats {len(threats)}, coverage gaps {len(m['_gaps'])}.", "",
             "| Band | Count |", "|---|---|"] + [f"| {b} | {by_band.get(b, 0)} |" for b in ("Critical", "High", "Medium", "Low")] + ["", "## Open Critical / High", ""]
    oh = [t for t in threats if t["status"] == "open" and t["_band"] in ("Critical", "High")]
    lines += [f"- **{t['id']}** ({t['target']}, {t['category']}) {t['title']} — {t['_band']} {t['_score']}, owner {t['owner']}, plan {plan_of(t) or '—'}" for t in oh] or ["none"]
    if meta.get("summary"):
        lines += ["", "## Summary", ""] + [str(p) for p in (meta["summary"] if isinstance(meta["summary"], list) else [meta["summary"]])]
    if meta.get("decisions"):
        lines += ["", "## Decisions needed", ""] + [f"{i}. {d.get('ask')} — owner {d.get('owner')}" + (f", by {d['by']}" if d.get("by") else "") for i, d in enumerate(meta["decisions"], 1)]
    by_owner = Counter((t['owner'], t['status']) for t in threats)
    lines += ["", "## By owner and status", "", "| Owner | open | mitigated | accepted | transferred |", "|---|---|---|---|---|"]
    lines += [f"| {o} | " + " | ".join(str(by_owner.get((o, st), 0)) for st in ('open', 'mitigated', 'accepted', 'transferred')) + " |" for o in sorted({t['owner'] for t in threats})]
    lines += ["", f"Explicit no-threat decisions: {len(m.get('no_threat') or [])}."]
    lines += ["", "## All threats", "", "| ID | Target | Cat | Title | L×I | Band | Status | Owner |", "|---|---|---|---|---|---|---|---|"]
    lines += [f"| {t['id']} | {t['target']} | {t['category']} | {t['title']} | {t['likelihood']}×{t['impact']} | {t['_band']} | {t['status']} | {t['owner']} |" for t in threats]
    if m["_gaps"]:
        lines += ["", "## Coverage gaps", ""] + [f"- {g}" for g in m["_gaps"]]
    if m.get("divergences"):
        lines += ["", "## Divergences", ""] + [f"- **{d['id']}** ({d['between']}) {d['description']} → {d['resolution']}" for d in m["divergences"]]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", type=Path)
    ap.add_argument("-o", "--output", type=Path, default=None)
    ap.add_argument("--check", action="store_true", help="validate only")
    a = ap.parse_args(argv)
    m = load(a.model)
    errs, warns = validate(m)
    if errs:
        print("\n".join(f"ERROR  {e}" for e in errs)); return 1
    for w in warns:
        print(f"WARN   {w}")
    m = derive(m)
    print(f"OK  {len(m['elements'])} elements, {len(m['flows'])} flows ({sum(1 for f in m['flows'] if f['_cross'])} cross-boundary), {len(m['threats'])} threats, {len(m['_gaps'])} coverage gap(s)")
    if a.check:
        return 0
    out = a.output or a.model.with_name("threat-model.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    svg0, svg1 = render_svg(dot_l0(m), "l0"), render_svg(dot_l1(m), "l1")
    if svg0: (out.parent / "dfd-l0.svg").write_text(svg0, encoding="utf-8")
    if svg1: (out.parent / "dfd-l1.svg").write_text(svg1, encoding="utf-8")
    out.write_text(build_html(m, svg0, svg1, mermaid_l1(m)), encoding="utf-8")
    (out.parent / "threat-model-summary.md").write_text(summary_md(m), encoding="utf-8")
    print(f"wrote {out}" + (" + dfd-l0.svg + dfd-l1.svg" if svg1 else " (no Graphviz: Mermaid fallback)") + " + threat-model-summary.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
