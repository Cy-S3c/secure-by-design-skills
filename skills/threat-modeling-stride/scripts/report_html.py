#!/usr/bin/env python3
"""The HTML page for build_report.py: Part A (executive brief) and Part B (technical detail).

Self-contained: assets/report.css and assets/report.js are inlined. Optional model
fields used here — meta.summary, meta.decisions[], meta.classification, meta.status;
threat.headline, threat.plain, threat.plain_fix, threat.effort — all fall back to the technical fields.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from tm_common import BAND_ORDER, CATEGORY, esc, band, plan_of

ASSETS = Path(__file__).resolve().parent / "assets"
BAND_CLASS = {"Critical": "crit", "High": "high", "Medium": "med", "Low": "low"}
STATUS_ORDER = ("open", "accepted", "transferred", "mitigated")
STATUS_UI = {"open": ("○", "Open", "needs action: no adequate control yet"),
             "mitigated": ("✓", "Mitigated", "a control is designed and in place"),
             "accepted": ("✎", "Accepted", "residual risk signed off by a named approver"),
             "transferred": ("⇄", "Transferred", "handled by a provider or a contract")}
CATEGORY_PLAIN = {"S": "pretending to be another user or system", "T": "changing data, code or messages without permission",
                  "R": "denying an action because there is no trustworthy record of it", "I": "exposing data to people who should not see it",
                  "D": "making the service slow or unavailable", "E": "gaining rights or access one should not have"}
KIND_LABEL = {"entity": "External entities", "process": "Processes", "store": "Data stores", "flow": "Data flows"}
LIKELIHOOD_ANCHOR = {1: "insider plus an unlikely chain", 2: "authenticated plus a misconfiguration", 3: "any authenticated user",
                     4: "unauthenticated, public tooling", 5: "trivial or automated"}
IMPACT_ANCHOR = {5: "regulated breach, legal exposure", 4: "all clients' data, audit or deliverables", 3: "one client's data, a day down",
                 2: "one user's data, hours down", 1: "minor or transient"}
META_SHOWN = {"system", "version", "date", "source", "authors", "scope_in", "scope_out", "summary", "decisions", "classification", "status"}
CWE = re.compile(r"^CWE-(\d+)$")


# ----------------------------------------------------------------- small pieces
def num(tid: str) -> int:
    return int(re.sub(r"\D", "", str(tid)) or 0)


def paras(x) -> str:
    if not x:
        return ""
    return "".join(f"<p>{esc(p)}</p>" for p in (x if isinstance(x, list) else [x]))


def chip_band(b: str, score=None) -> str:
    sc = f' <span class="sc">{score}</span>' if score is not None else ""
    return f'<span class="chip chip-{BAND_CLASS[b]}"><i></i>{b}{sc}</span>'


def chip_status(s: str) -> str:
    ic, label, _ = STATUS_UI[s]
    return f'<span class="chip chip-{s}"><span aria-hidden="true">{ic}</span>{label}</span>'


def chip_cls(c) -> str:
    return f'<span class="chip chip-cls cls-{esc(c)}">{esc(c)}</span>'


def chip_cat(c: str) -> str:
    return f'<abbr class="cat" title="{esc(CATEGORY[c])}">{c}</abbr>'


def tlink(tid) -> str:
    return f'<a class="tl id" href="#{esc(tid)}">{esc(tid)}</a>'


def tlinks(ids) -> str:
    return ", ".join(tlink(i) for i in (ids or [])) or "—"


def ref_html(r) -> str:
    m = CWE.match(str(r))
    if m:
        return f'<a href="https://cwe.mitre.org/data/definitions/{m.group(1)}.html" rel="noopener">{esc(r)}</a>'
    return esc(r)


def table(head: list, rows: list, cls: str = "", caption: str = "", tid: str = "", sortable: dict | None = None) -> str:
    ths = []
    for h in head:
        c = ' class="num"' if h.startswith("num:") else ""
        label = h[4:] if h.startswith("num:") else h
        srt = f' data-sort="{sortable[label]}" tabindex="0" title="Sort"' if sortable and label in sortable else ""
        ths.append(f"<th{c}{srt}>{esc(label)}</th>")
    cap = f"<caption>{caption}</caption>" if caption else ""
    idattr = f' id="{tid}"' if tid else ""
    return f'<div class="table-wrap"><table{idattr} class="{cls}">{cap}<thead><tr>{"".join(ths)}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def bar(title: str, segs: list) -> str:
    """Thin stacked bar: segs = [(label, count, swatch-class)]; legend carries the numbers."""
    fills = "".join(f'<div class="sw-{cls}" style="flex:{n} 0 0" title="{esc(l)}: {n}"></div>' for l, n, cls in segs if n)
    legend = "".join(f'<span class="lg"><i class="sw-{cls}"></i>{esc(l)} <b>{n}</b></span>' for l, n, cls in segs)
    aria = esc(title + ": " + ", ".join(f"{l} {n}" for l, n, _ in segs))
    return f'<figure class="bar"><figcaption>{esc(title)}</figcaption><div class="bar-track" role="img" aria-label="{aria}">{fills}</div><div class="legend">{legend}</div></figure>'


def wrap_sec(sid: str, n: int, title: str, lead: str, body: str) -> str:
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="sec" id="{sid}" aria-labelledby="{sid}-h"><h3 id="{sid}-h"><span class="num">{n}</span>{esc(title)}</h3>{lead_html}{body}</section>'


# ----------------------------------------------------------------- derived context
def auto_decisions(m: dict, open_hi: list, unplanned: list) -> list:
    out = [{"ask": f"Approve and schedule the fix for {t['id']}: {t['title']}", "why": t.get("plain") or "", "owner": t["owner"],
            "by": plan_of(t) or "not scheduled", "threats": [t["id"]]} for t in open_hi]
    if unplanned:
        out.append({"ask": f"Assign a sprint or backlog item to the {len(unplanned)} open threats that have none", "owner": "Engineering management",
                    "by": "next planning cycle", "threats": [t["id"] for t in unplanned[:8]]})
    divs = m.get("divergences") or []
    if divs:
        out.append({"ask": f"Decide which reading prevails for the {len(divs)} places where the documents and the code disagree, and fund the reconciliation",
                    "owner": "Tech Lead", "by": "next architecture review"})
    acc = [t for t in m["threats"] if t["status"] == "accepted" and not t.get("revisit")]
    if acc:
        out.append({"ask": f"Set a revisit date for the {len(acc)} accepted risks that have none", "owner": "Risk owner", "threats": [t["id"] for t in acc]})
    return out


def context(m: dict) -> dict:
    threats = sorted(m["threats"], key=lambda t: (-t["_score"], t["id"]))
    open_ = [t for t in threats if t["status"] == "open"]
    open_hi = [t for t in open_ if t["_band"] in ("Critical", "High")]
    top = open_[:max(len(open_hi), min(6, len(open_)))] if open_ else threats[:5]
    required = sum(1 for r in m["_matrix"] for v in r["cells"].values() if v not in (None, "optional"))
    cov = round(100 * (required - len(m["_gaps"])) / required) if required else 100
    unplanned = [t for t in open_ if not plan_of(t)]
    return {"threats": threats, "by_band": Counter(t["_band"] for t in threats), "by_status": Counter(t["status"] for t in threats),
            "open": open_, "open_hi": open_hi, "top": top, "cov": cov, "unplanned": unplanned,
            "owners": sorted({t["owner"] for t in threats}), "decisions": m["meta"].get("decisions") or auto_decisions(m, open_hi, unplanned)}


# ----------------------------------------------------------------- Part A: for leadership
def exec_brief(m: dict, c: dict):
    meta, bs = m["meta"], c["by_status"]
    cross = sum(1 for f in m["flows"] if f["_cross"])
    hi = len(c["open_hi"])
    s = (f"This review examined <b>{len(m['elements'])} components</b> and <b>{len(m['flows'])} data paths</b> ({cross} of them crossing a trust boundary) "
         f"of {esc(meta.get('system'))} version {esc(meta.get('version'))}, assessed on {esc(meta.get('date'))}. It identified <b>{len(c['threats'])} threats</b>: "
         f"{bs.get('mitigated', 0)} already have a control in place and <b>{bs.get('open', 0)} need action</b>"
         + (f", <b>{hi} of them high priority</b>" if hi else ", none of them high priority")
         + (f"; {bs['accepted']} are accepted as residual risk" if bs.get("accepted") else "")
         + (f"; {bs['transferred']} are transferred to a provider" if bs.get("transferred") else "") + ". "
         + ("Coverage is complete: every component and data path was assessed against every threat category that applies to it."
            if not m["_gaps"] else f"<b>{len(m['_gaps'])} required assessments are still missing</b>; the coverage matrix in Part B lists them."))
    return "brief", "Executive brief", "", f'<div class="card brief"><p class="auto">{s}</p>{paras(meta.get("summary"))}</div>'


def exec_posture(m: dict, c: dict):
    bs, bb = c["by_status"], c["by_band"]
    hi = len(c["open_hi"])
    tiles = [("Threats identified", len(c["threats"]), f"across {len(m['elements'])} components and {len(m['flows'])} data paths", ""),
             ("Need action", bs.get("open", 0), f"{hi} high priority" if hi else "none high priority", "tone-bad" if hi else "tone-act"),
             ("Controlled", bs.get("mitigated", 0), "control designed and in place", "tone-good"),
             ("Accepted or transferred", bs.get("accepted", 0) + bs.get("transferred", 0), "signed off, or handled by a provider", ""),
             ("Assessment coverage", f"{c['cov']}%", f"{len(m['_gaps'])} required cells unassessed" if m["_gaps"] else "every required cell assessed",
              "tone-warn" if m["_gaps"] else "tone-good")]
    tiles_html = "".join(f'<div class="tile {tone}"><span class="tile-label">{esc(l)}</span><span class="tile-value">{v}</span><span class="tile-sub">{esc(s)}</span></div>'
                         for l, v, s, tone in tiles)
    bars = (bar("By severity (likelihood × impact)", [(b, bb.get(b, 0), BAND_CLASS[b]) for b in BAND_ORDER])
            + bar("By status", [(STATUS_UI[s][1], bs.get(s, 0), s) for s in STATUS_ORDER]))
    lead = "How many threats were found, how severe they are, and whether a control already exists for them."
    return "posture", "Posture at a glance", lead, f'<div class="tiles">{tiles_html}</div><div class="bars">{bars}</div>'


def risk_card(i: int, t: dict) -> str:
    when = plan_of(t) or (f"accepted by {t['approver']}" if t.get("approver") else "") or (f"agreement: {t['agreement']}" if t.get("agreement") else "") or "not scheduled"
    effort = f'<span><b>Effort</b> {esc(t["effort"])}</span>' if t.get("effort") else ""
    return (f'<article class="risk"><div class="risk-head"><span class="rank">{i}</span>{chip_band(t["_band"], t["_score"])}{chip_status(t["status"])}</div>'
            f'<h4>{esc(t.get("headline") or t["title"])}</h4>' + (f'<p class="tech-title">{esc(t["title"])}</p>' if t.get("headline") else "")
            + f'<dl><dt>What could happen</dt><dd>{esc(t.get("plain") or t["description"])}</dd>'
            f'<dt>What we recommend</dt><dd>{esc(t.get("plain_fix") or t["mitigation"])}</dd></dl>'
            f'<footer><span><b>Owner</b> {esc(t["owner"])}</span><span><b>When</b> {esc(when)}</span>{effort}<span>{tlink(t["id"])} · {esc(t["_target_name"])}</span></footer></article>')


def exec_top_risks(m: dict, c: dict):
    top = c["top"]
    if not top:
        return None
    if c["open"]:
        lead = (f"The {len(top)} open threats with the highest score, ranked by likelihood × impact; {len(c['open_hi'])} of them are rated High or Critical. "
                "Each card says what could happen in business terms and what the fix is; the threat id opens the full technical record in Part B.")
    else:
        lead = "No threat is open. These are the highest-rated threats and the controls that hold them."
    return "top-risks", "Top risks", lead, '<div class="risks">' + "".join(risk_card(i, t) for i, t in enumerate(top, 1)) + "</div>"


def exec_decisions(m: dict, c: dict):
    if not c["decisions"]:
        return None
    rows = [f'<tr><td class="num">{i}</td><td><b>{esc(d.get("ask"))}</b>' + (f'<div class="why">{esc(d["why"])}</div>' if d.get("why") else "")
            + f'</td><td>{tlinks(d.get("threats"))}</td><td>{esc(d.get("owner"))}</td><td>{esc(d.get("by") or "—")}</td></tr>'
            for i, d in enumerate(c["decisions"], 1)]
    lead = "What leadership is asked to approve, fund or decide. Each decision names the threats it resolves."
    return "decisions", "Decisions needed", lead, table(["num:#", "Decision", "Resolves", "Owner", "By"], rows)


def exec_owners(m: dict, c: dict):
    rows = []
    for o in c["owners"]:
        ts = [t for t in c["threats"] if t["owner"] == o]
        op = [t for t in ts if t["status"] == "open"]
        hi = [t for t in op if t["_band"] in ("Critical", "High")]
        nxt = f'{tlink(op[0]["id"])} {esc(op[0]["title"])}' if op else "—"
        rows.append(f'<tr><td><b>{esc(o)}</b></td><td class="num">{len(op)}</td><td class="num">{len(hi)}</td>'
                    f'<td class="num">{sum(1 for t in ts if t["status"] == "mitigated")}</td>'
                    f'<td class="num">{sum(1 for t in ts if t["status"] in ("accepted", "transferred"))}</td><td>{nxt}</td></tr>')
    lead = "Open work by owner. The next action is each owner's highest-scored open threat."
    return "ownership", "Who owns what", lead, table(["Owner", "num:Open", "num:High priority", "num:Mitigated", "num:Accepted / transferred", "Next action"], rows)


def exec_reading(m: dict, c: dict):
    stride = "".join(f"<dt>{esc(CATEGORY[k])} ({k})</dt><dd>{esc(v)}</dd>" for k, v in CATEGORY_PLAIN.items())
    bands = (f"<dd>{chip_band('Critical')} 20–25 {chip_band('High')} 12–19 {chip_band('Medium')} 6–11 {chip_band('Low')} 1–5</dd>")
    statuses = "".join(f"<dt>{chip_status(s)}</dt><dd>{esc(STATUS_UI[s][2])}</dd>" for s in STATUS_ORDER)
    body = ('<div class="cols"><div class="card"><h4>The six threat categories (STRIDE)</h4><dl class="gl">' + stride + "</dl></div>"
            '<div class="card"><h4>How risk is scored</h4><dl class="gl"><dt>Score = likelihood × impact</dt><dd>Both on a 1–5 scale: likelihood is how plausible the attack is within a year given today\'s controls; impact is the worst credible outcome for the business.</dd>'
            "<dt>Severity bands</dt>" + bands + "<dt>High priority</dt><dd>An open threat rated High or Critical. A Critical or High risk can only be accepted with a named approver.</dd></dl></div>"
            '<div class="card"><h4>Status of a threat</h4><dl class="gl">' + statuses + "</dl></div>"
            '<div class="card"><h4>Terms used in this report</h4><dl class="gl"><dt>Component</dt><dd>A part of the system: a kind of user or outside party, a running service, or a place data is kept.</dd>'
            "<dt>Data path</dt><dd>Data moving from one component to another.</dd><dt>Trust boundary</dt><dd>A line where the level of trust changes, such as the public internet meeting our servers. Most threats sit on paths that cross one.</dd>"
            "<dt>Coverage</dt><dd>Every component and data path was asked every applicable STRIDE question; a cell is either a threat, a reasoned “no threat”, or a gap.</dd>"
            "<dt>Divergence</dt><dd>A place where two sources disagree (one document against another, or a document against the code). Each is a finding to resolve.</dd></dl></div></div>")
    return "reading", "How to read this report", "", body


# ----------------------------------------------------------------- Part B: for engineering
def tech_scope(m: dict):
    meta = m["meta"]
    authors = meta.get("authors")
    authors = ", ".join(authors) if isinstance(authors, list) else authors
    cards = [f'<div class="card"><h4>In scope</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in meta.get("scope_in") or [])}</ul></div>',
             f'<div class="card"><h4>Out of scope</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in meta.get("scope_out") or [])}</ul></div>']
    if m.get("assumptions"):
        cards.append(f'<div class="card"><h4>Assumptions</h4><ul>{"".join(f"<li>{esc(a)}</li>" for a in m["assumptions"])}</ul></div>')
    basis = f'<p class="lead"><b>Basis:</b> {esc(meta.get("source"))}' + (f" · <b>Authors:</b> {esc(authors)}" if authors else "") + "</p>"
    return "scope", "Scope and assumptions", "", basis + f'<div class="cols">{"".join(cards)}</div>'


def fig(title: str, sid: str, svg: str | None, fallback: str, file_name: str) -> str:
    tools = ('<div class="fig-tools"><button type="button" class="btn btn-sm" data-act="out" aria-label="Zoom out">−</button><span class="fig-zoom">fit</span>'
             '<button type="button" class="btn btn-sm" data-act="in" aria-label="Zoom in">+</button><button type="button" class="btn btn-sm" data-act="fit">Fit</button>'
             f'<button type="button" class="btn btn-sm" data-act="full">Full screen</button><a class="btn btn-sm" href="{file_name}" target="_blank" rel="noopener">Open SVG</a></div>')
    return (f'<figure class="fig" id="{sid}"><div class="fig-bar"><span class="fig-title">{esc(title)}</span>{tools if svg else ""}</div>'
            f'<div class="fig-canvas">{svg or fallback}</div></figure>')


def tech_dfd(m: dict, svg_l0, svg_l1, mmd_l1: str):
    key = ('<div class="dfd-key"><span class="k-ent">External entity</span><span class="k-proc">Process</span><span class="k-store">Data store</span>'
           '<span class="k-bnd">Trust boundary</span><span class="k-flow">Data flow</span><span class="k-cross">Flow crossing a boundary</span></div>')
    lead = ("Level 0 shows the system as one process with its external parties. Level 1 opens it up: processes, data stores, trust boundaries and every data path. "
            "Arrows carry the flow id; the data-flow table below is the legend and hovering an arrow shows its name. Use the zoom controls or open the SVG for the full-size drawing.")
    fallback0 = '<p class="muted">Graphviz was not available when this report was built; see Level 1.</p>'
    fallback1 = (f'<pre class="mermaid">{esc(mmd_l1)}</pre><script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs";mermaid.initialize({{startOnLoad:true}});</script>')
    body = key + fig("Level 0 — context", "dfd-l0", svg_l0, fallback0, "dfd-l0.svg") + fig("Level 1 — processes, stores and trust boundaries", "dfd-l1", svg_l1, fallback1, "dfd-l1.svg")
    return "dfd", "Data-flow diagrams", lead, body


def tech_elements(m: dict):
    cards = []
    for b in m["boundaries"]:
        members = [e for e in m["elements"] if e["boundary"] == b["id"]]
        if not members:
            continue
        els = []
        for e in members:
            extra = " · ".join(f"{k}: {v}" for k, v in e.items() if k not in ("id", "type", "name", "boundary"))
            els.append(f'<div class="el"><span class="id">{esc(e["id"])}</span><span><b>{esc(e["name"])}</b> <span class="kind">{esc(e["type"])}</span></span>'
                       + (f'<span class="x">{esc(extra)}</span>' if extra else "") + "</div>")
        cards.append(f'<div class="card"><h4>{esc(b["name"])}<span class="id muted">{esc(b["id"])}</span></h4>{"".join(els)}</div>')
    lead = f"{len(m['elements'])} components grouped by the {len(cards)} trust boundaries they sit in."
    return "elements", "Boundaries and components", lead, f'<div class="bnd">{"".join(cards)}</div>'


def tech_flows(m: dict):
    names = {e["id"]: e["name"] for e in m["elements"]}
    rows = []
    for f in m["flows"]:
        crosses = f'<span class="chip chip-high"><i></i>{esc(f["_from_b"])} → {esc(f["_to_b"])}</span>' if f["_cross"] else '<span class="muted">—</span>'
        rows.append(f'<tr data-cross="{1 if f["_cross"] else 0}"><td class="id">{esc(f["id"])}</td>'
                    f'<td><span class="id">{esc(f["from"])}</span> → <span class="id">{esc(f["to"])}</span><span class="target-sub">{esc(names[f["from"]])} → {esc(names[f["to"]])}</span></td>'
                    f'<td>{esc(f["name"])}</td><td>{esc(f["protocol"])}</td><td>{esc(f["data"])}</td><td>{chip_cls(f["classification"])}</td><td>{crosses}</td></tr>')
    cross = sum(1 for f in m["flows"] if f["_cross"])
    ctl = (f'<div class="filters"><label><input type="checkbox" id="flows-cross"> Cross-boundary flows only</label><span class="count" id="flows-count"></span></div>')
    lead = f"{len(m['flows'])} data paths, {cross} of which cross a trust boundary. The flow id is the label on the diagram arrows."
    return "flows", "Data flows", lead, ctl + table(["ID", "From → To", "Name", "Protocol", "Data", "Classification", "Crosses boundary"], rows, tid="flows-table")


def tech_assets(m: dict):
    assets = m.get("assets") or []
    if not assets:
        return None
    names = {e["id"]: e["name"] for e in m["elements"]}
    rows = [f'<tr><td class="id">{esc(a.get("id"))}</td><td>{esc(a.get("name"))}</td><td>{chip_cls(a.get("classification", ""))}</td>'
            f'<td>{"; ".join(f"<span class=id>{esc(s)}</span> {esc(names.get(s, s))}" for s in a.get("stored_in") or []) or "—"}</td>'
            + (f'<td class="muted">{esc(a["note"])}</td>' if a.get("note") else "<td></td>") + "</tr>" for a in assets]
    return "assets", "Assets", "What the attacker is after and where it lives.", table(["ID", "Asset", "Classification", "Stored in", "Note"], rows)


def register_row(t: dict) -> str:
    tid, det_id = t["id"], f"det-{t['id']}"
    existing = t.get("existing") or []
    ex = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in existing) + "</ul>" if existing else '<span class="muted">none</span>'
    items = [("Existing controls", ex), ("Mitigation", esc(t["mitigation"]))]
    for key, label in (("sprint", "Plan"), ("plan", "Plan"), ("approver", "Approver"), ("revisit", "Revisit"), ("agreement", "Agreement"), ("effort", "Effort")):
        if t.get(key):
            items.append((label, esc(t[key])))
    if t.get("refs"):
        items.append(("References", ", ".join(ref_html(r) for r in t["refs"])))
    if t.get("plain"):
        items.append(("In plain terms", esc(t["plain"]) + (f" <i>Fix:</i> {esc(t['plain_fix'])}" if t.get("plain_fix") else "")))
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in items)
    return (f'<tr class="t" id="row-{esc(tid)}" data-open="0" data-n="{num(tid)}" data-target="{esc(t["target"])}" data-cat="{t["category"]}" data-band="{t["_band"]}" '
            f'data-bandrank="{BAND_ORDER.index(t["_band"])}" data-status="{t["status"]}" data-owner="{esc(t["owner"])}" data-score="{t["_score"]}" data-l="{t["likelihood"]}" data-i="{t["impact"]}">'
            f'<td class="id">{esc(tid)}</td><td><span class="id">{esc(t["target"])}</span><span class="target-sub">{esc(t["_target_name"])}</span></td><td>{chip_cat(t["category"])}</td>'
            f'<td><button type="button" class="rowtoggle" aria-expanded="false" aria-controls="{det_id}">{esc(t["title"])}</button></td>'
            f'<td class="num">{t["likelihood"]}×{t["impact"]} = <b>{t["_score"]}</b></td><td>{chip_band(t["_band"])}</td><td>{chip_status(t["status"])}</td><td>{esc(t["owner"])}</td></tr>'
            f'<tr class="d" id="{det_id}" hidden><td colspan="8"><div class="detail"><p>{esc(t["description"])}</p><dl>{dl}</dl></div></td></tr>')


def tech_register(m: dict, c: dict):
    opts = lambda vals, fmt=esc: "".join(f'<option value="{esc(v)}">{fmt(v)}</option>' for v in vals)
    ctl = ('<div class="filters"><input id="f-q" type="search" placeholder="Search id, title, control, reference…" aria-label="Search threats">'
           f'<select id="f-cat" aria-label="Category"><option value="">All categories</option>{opts("STRIDE", lambda v: f"{v} · {CATEGORY[v]}")}</select>'
           f'<select id="f-band" aria-label="Severity"><option value="">All severities</option>{opts(BAND_ORDER)}</select>'
           f'<select id="f-status" aria-label="Status"><option value="">All statuses</option>{opts(STATUS_ORDER, lambda v: STATUS_UI[v][1])}</select>'
           f'<select id="f-owner" aria-label="Owner"><option value="">All owners</option>{opts(c["owners"])}</select>'
           '<span class="cell-chip" id="cell-chip" hidden><span id="cell-chip-text"></span><button type="button" id="cell-chip-x" aria-label="Clear heat-map filter">×</button></span>'
           '<button type="button" class="btn btn-sm" id="f-clear">Clear</button><button type="button" class="btn btn-sm" id="reg-expand">Expand all</button>'
           '<button type="button" class="btn btn-sm" id="reg-collapse">Collapse all</button><span class="count" id="reg-count"></span></div>')
    sortable = {"ID": "n", "Target": "target", "Cat": "cat", "Score": "score", "Severity": "bandrank", "Status": "status", "Owner": "owner"}
    lead = ("Every threat with its target, STRIDE category, score, status and owner. Click a title for the description, existing controls, mitigation, plan and references. "
            "Headers sort; the filters narrow the list; the heat map and coverage matrix link here.")
    body = ctl + table(["ID", "Target", "Cat", "Threat", "num:Score", "Severity", "Status", "Owner"], [register_row(t) for t in c["threats"]], tid="reg", sortable=sortable)
    return "register", "Threat register", lead, body


def tech_coverage(m: dict, c: dict):
    rows, kind_seen = [], None
    for row in m["_matrix"]:
        if row["kind"] != kind_seen:
            kind_seen = row["kind"]
            rows.append(f'<tr class="sub"><td colspan="7">{KIND_LABEL[kind_seen]}</td></tr>')
        cells = []
        for cat in "STRIDE":
            v = row["cells"][cat]
            if v is None:
                cells.append('<td class="cov-na" title="Category does not apply to this element type">—</td>')
            elif v == "no-threat":
                reason = next((n["reason"] for n in m.get("no_threat") or [] if n["target"] == row["id"] and n["category"] == cat), "")
                cells.append(f'<td><span class="cov-nt" title="{esc(reason)}">none</span></td>')
            elif v == "optional":
                cells.append('<td class="cov-opt" title="Optional: repudiation matters only for stores holding audit or log data">opt</td>')
            elif v == 0:
                cells.append('<td class="cov-gap" title="Required but not assessed">GAP</td>')
            else:
                cells.append(f'<td class="cov-n"><a href="#register" data-q="{esc(row["id"])}" title="Show these threats">{v}</a></td>')
        rows.append(f'<tr><td><span class="id">{esc(row["id"])}</span> {esc(row["name"])}</td>{"".join(cells)}</tr>')
    key = ('<div class="key"><span><b>n</b> threats recorded (click to list them)</span><span><span class="cov-nt">none</span> assessed, no threat (hover for the reason)</span>'
           '<span><i class="cov-opt">opt</i> optional cell</span><span><span class="sw" style="background:var(--gap-bg)"></span>GAP: required, not assessed</span><span>— does not apply</span></div>')
    gaps = f'<p><b>Gaps to close:</b> {esc("; ".join(m["_gaps"]))}</p>' if m["_gaps"] else ""
    lead = (f"Evidence that every element was asked every applicable question. Coverage {c['cov']}%: "
            + (f"{len(m['_gaps'])} required cells are unassessed." if m["_gaps"] else "no required cell is unassessed."))
    head = ["Element / flow"] + [f"{k}" for k in "STRIDE"]
    body = key + table(head, rows, cls="cov").replace("<th>S</th>", f'<th title="{CATEGORY["S"]}">S</th>') + gaps
    for k in "TRIDE":
        body = body.replace(f"<th>{k}</th>", f'<th title="{CATEGORY[k]}">{k}</th>', 1)
    return "coverage", "STRIDE coverage", lead, body


def tech_heat(m: dict, c: dict):
    head = '<tr><th class="corner">Impact ↓ &nbsp; Likelihood →</th>' + "".join(f"<th>{l}<br><span class=muted>{esc(LIKELIHOOD_ANCHOR[l])}</span></th>" for l in range(1, 6)) + "</tr>"
    rows = []
    for i in range(5, 0, -1):
        cells = []
        for l in range(1, 6):
            ids = [t["id"] for t in c["threats"] if t["likelihood"] == l and t["impact"] == i]
            cells.append(f'<td class="{band(l * i)[0].lower()}" data-l="{l}" data-i="{i}" data-n="{len(ids)}" title="{esc(", ".join(ids)) or "no threats"}">{len(ids) or "·"}</td>')
        rows.append(f'<tr><th class="y">{i} <span class=muted>{esc(IMPACT_ANCHOR[i])}</span></th>{"".join(cells)}</tr>')
    key = "".join(f"<span>{chip_band(b)}</span>" for b in BAND_ORDER)
    lead = "Number of threats at each likelihood × impact position. Click a cell to list its threats in the register."
    return "heatmap", "Risk heat map", lead, f'<div class="heat card"><table>{head}{"".join(rows)}</table><div class="key">{key}</div></div>'


def tech_plan(m: dict, c: dict):
    out = []
    for s in STATUS_ORDER:
        group = [t for t in c["threats"] if t["status"] == s]
        if not group:
            continue
        rows = [f'<tr><td>{tlink(t["id"])}</td><td>{chip_band(t["_band"], t["_score"])}</td><td>{esc(t["title"])}</td><td>{esc(t["mitigation"])}</td><td>{esc(t["owner"])}</td>'
                f'<td>{esc(plan_of(t) or t.get("approver") or t.get("agreement") or "—")}</td><td>{esc(t.get("effort") or "")}</td></tr>' for t in group]
        out.append(table(["ID", "Severity", "Threat", "Action", "Owner", "Plan / approver", "Effort"], rows, caption=f"{chip_status(s)} &nbsp;{len(group)} — {esc(STATUS_UI[s][2])}"))
    lead = "Every threat and the control that disposes of it, grouped by status and ordered by score. Open items carry the sprint or backlog reference."
    return "plan", "Mitigation plan", lead, "".join(out)


def tech_divergences(m: dict):
    divs = m.get("divergences") or []
    if not divs:
        return None
    rows = [f'<tr><td class="id">{esc(d["id"])}</td><td>{esc(d["between"])}</td><td>{esc(d["description"])}</td><td>{esc(d["resolution"])}</td><td>{tlinks(d.get("threats"))}</td></tr>' for d in divs]
    lead = f"{len(divs)} places where two sources disagree (document against document, or document against code). Each is a finding: an implementer has to pick one reading."
    return "divergences", "Divergences found while modelling", lead, table(["ID", "Between", "Description", "Resolution / owner", "Threats"], rows)


def tech_method(m: dict):
    meta = m["meta"]
    extras = {k: v for k, v in meta.items() if k not in META_SHOWN}
    rows = [f'<tr><td><b>{esc(k)}</b></td><td>{esc(", ".join(map(str, v)) if isinstance(v, list) else v)}</td></tr>' for k, v in extras.items()]
    body = ("<p>STRIDE applied per element of the Level 1 data-flow diagram: external entities are asked about Spoofing and Repudiation; processes about all six categories; "
            "data stores about Tampering, Information disclosure and Denial of service (plus Repudiation when they hold audit data); flows about Tampering, Information disclosure and Denial of service. "
            "Risk = likelihood × impact on 1–5 scales; bands Critical 20–25, High 12–19, Medium 6–11, Low 1–5. A Critical or High threat may be accepted only with a named approver. "
            f"Explicit no-threat decisions recorded: {len(m.get('no_threat') or [])}.</p>"
            "<p>The diagrams, matrix, heat map and tables are generated from <code>model.yaml</code> by <code>threat-modeling-stride/scripts/build_report.py</code>; "
            "nothing is drawn or counted by hand. Companion files beside this page: <code>dfd-l0.svg</code>, <code>dfd-l1.svg</code>, <code>threat-model-summary.md</code>.</p>")
    if rows:
        body += table(["Field", "Value"], rows, caption="Other model metadata")
    return "method", "Method and metadata", "", body


# ----------------------------------------------------------------- page
def topbar(meta: dict) -> str:
    cls = f'<span class="chip chip-open">{esc(meta["classification"])}</span>' if meta.get("classification") else ""
    return ('<header class="topbar"><div class="topbar-in"><div class="brand"><span class="eyebrow">Threat model</span><p class="brand-name">' + esc(meta.get("system")) + "</p></div>"
            f'<div class="topbar-meta"><span>v{esc(meta.get("version"))}</span><span>·</span><span>{esc(meta.get("date"))}</span>{cls}</div>'
            '<div class="switch" role="group" aria-label="Choose what to show"><button type="button" data-view="exec" aria-pressed="false">Executive brief</button>'
            '<button type="button" data-view="tech" aria-pressed="false">Technical detail</button><button type="button" data-view="all" aria-pressed="true">Everything</button></div>'
            '<button type="button" class="btn" id="print">Print / PDF</button></div></header>')


def head_html(meta: dict) -> str:
    authors = meta.get("authors")
    authors = ", ".join(authors) if isinstance(authors, list) else authors
    strip = [("Version", meta.get("version")), ("Assessed", meta.get("date")), ("Authors", authors), ("Status", meta.get("status")), ("Basis", meta.get("source"))]
    dl = "".join(f'<div><dt>{esc(k)}</dt><dd title="{esc(v)}">{esc(v)}</dd></div>' for k, v in strip if v)
    return (f'<div class="report-head"><span class="eyebrow">STRIDE threat model · design-time security review</span><h1>{esc(meta.get("system"))}</h1><dl class="meta-strip">{dl}</dl></div>')


def part_head(key: str, eyebrow: str, title: str, text: str) -> str:
    return f'<div class="part-head part-{key}"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{text}</p></div>'


def toc_html(parts: list) -> str:
    out = ['<nav class="toc" aria-label="Contents">']
    for key, label, items in parts:
        out.append(f'<div class="toc-{key}"><p class="toc-group">{esc(label)}</p>' + "".join(f'<a href="#{i}">{n}. {esc(t)}</a>' for i, t, n in items) + "</div>")
    return "".join(out) + "</nav>"


def build_html(m: dict, svg_l0: str | None, svg_l1: str | None, mmd_l1: str) -> str:
    c = context(m)
    exec_secs = [s for s in (exec_brief(m, c), exec_posture(m, c), exec_top_risks(m, c), exec_decisions(m, c), exec_owners(m, c), exec_reading(m, c)) if s]
    tech_secs = [s for s in (tech_scope(m), tech_dfd(m, svg_l0, svg_l1, mmd_l1), tech_elements(m), tech_flows(m), tech_assets(m), tech_register(m, c),
                             tech_coverage(m, c), tech_heat(m, c), tech_plan(m, c), tech_divergences(m), tech_method(m)) if s]
    n, parts, bodies = 0, [], {"exec": [], "tech": []}
    for key, label, secs in (("exec", "For leadership", exec_secs), ("tech", "For engineering", tech_secs)):
        items = []
        for sid, title, lead, body in secs:
            n += 1
            items.append((sid, title, n))
            bodies[key].append(wrap_sec(sid, n, title, lead, body))
        parts.append((key, label, items))
    css = (ASSETS / "report.css").read_text(encoding="utf-8")
    js = (ASSETS / "report.js").read_text(encoding="utf-8")
    meta = m["meta"]
    a_text = "What the review found, what it means for the business and what needs a decision. Written to be read in ten minutes; the evidence is in Part B."
    b_text = "The data-flow model, every threat with its controls and references, coverage evidence and the mitigation plan."
    foot = f'<p class="foot">Generated from model.yaml by threat-modeling-stride/scripts/build_report.py · {esc(meta.get("system"))} v{esc(meta.get("version"))} · {esc(meta.get("date"))}</p>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Threat model — {esc(meta.get("system"))}</title><style>{css}</style></head><body data-view="all"><a class="skip" href="#main">Skip to content</a>'
            + topbar(meta) + '<div class="layout">' + toc_html(parts) + '<main id="main">' + head_html(meta)
            + part_head("exec", "Part A · For leadership", "Executive brief", a_text) + "".join(bodies["exec"])
            + part_head("tech", "Part B · For engineering", "Technical detail", b_text) + "".join(bodies["tech"])
            + foot + f"</main></div><script>{js}</script></body></html>")
