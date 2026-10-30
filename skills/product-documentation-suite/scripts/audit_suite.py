#!/usr/bin/env python3
"""Audit a product documentation suite for its mechanical conventions.

Usage:
    python3 audit_suite.py <docs-dir> [--profile minimal|standard|full] [--allow-missing]

--allow-missing  authoring-time mode: documents not yet written, the missing
                 README, citations of unwritten documents and links to files
                 that do not exist yet report as INFO. Run without it before
                 approval.

Markers read: `FRs:` / `implied:` segments (separated by ' · ') in the last
cell of a 09 sprint row; `— (09 pending)` in 06 Appendix A; the
`**Unscheduled (n)**` line that ends that appendix's table;
`[CANON-PENDING: Term]`; `*Filled during S03*` (two-digit sprint).

Severity: FAIL = must fix (exit 1) · WARN = fix, or justify in the README ·
INFO = awareness. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

PROFILES = {
    "minimal": ["00", "01", "03", "04", "05", "06", "08", "09", "13"],
    "standard": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "13", "14"],
    "full": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"],
}
OPTIONAL_DOCS = {"10"}  # a domain specification exists only when the product has a domain standard
HEADER_FIELDS = ("Document ID", "Product", "Version", "Status", "Last updated")
LONG_DOC_LINES = 300
SIZE_TOLERANCE = 0.10

RE_TITLE = re.compile(r"^# (\d{2}) — ")
RE_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
RE_STATUS = re.compile(r"^(Draft\b|Pending approval\b|Approved v\d+\.\d+\.\d+ \(\d{4}-\d{2}-\d{2}\)|Living document — \S|Superseded by \S)")
RE_DOC_ID = re.compile(r"^([A-Z]{2,5})-[A-Z]{2,6}-\d{3}$")
RE_FR = re.compile(r"\bFR-(\d+)\.(\d+)\b")
RE_FR_RANGE = re.compile(r"\bFR-(\d+)\.(\d+)\s*(?:–|—|-|to)\s*(?:FR-)?(?:(\d+)\.)?(\d+)\b")
RE_FR_DEF = re.compile(r"\*\*FR-(\d+)\.(\d+)\*\*")
RE_ADR = re.compile(r"\bADR-(\d{3,4})\b")
RE_ADR_DEF = re.compile(r"^\|\s*ADR-(\d{3,4})\s*\|", re.M)
RE_SB = re.compile(r"\bS(\d{2})-B(\d+)\b")
RE_SPRINT_ROW = re.compile(r"^\| (S\d{2}-B\d+) \|")
RE_FILE_REF = re.compile(r"`(\d{2}-[a-z0-9-]+\.md)`")
RE_MD_LINK = re.compile(r"\]\(([^)\s#]+?\.(?:md|ya?ml|json))(?:#[^)]*)?\)")
RE_SECTION = re.compile(r"§(\d+(?:\.\d+)*)")
RE_TEMPLATE_TOKEN = re.compile(r"\{\{(?:PRODUCT|PREFIX|CODENAME|DATE)\}\}")
RE_PERM = re.compile(r"`([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)`")
PERM_IGNORE = {"resource.action"}
RE_CELL_PLACEHOLDER = re.compile(r"\|\s*<[A-Za-z][^<>|]{1,60}>\s*\|")
RE_PENDING_CELL = re.compile(r"\(09 pending\)")
RE_CANON = re.compile(r"\[CANON-PENDING(?::\s*([^\]]+))?\]")
RE_FILLED = re.compile(r"\*Filled during S\d{2}\*")
RE_PROPOSED_ADR = re.compile(r"Proposed (?:new )?ADR", re.I)
FILE_EXT = {"md", "py", "js", "ts", "tsx", "json", "yaml", "yml", "html", "css", "txt", "csv", "pdf", "docx", "svg", "png", "sh", "toml", "ini", "env", "zip"}


class Report:
    def __init__(self, allow_missing: bool) -> None:
        self.rows: list[tuple[str, str, str]] = []
        self.allow_missing = allow_missing

    def add(self, level: str, doc: str, msg: str, *, missing: bool = False) -> None:
        if missing and self.allow_missing and level in ("FAIL", "WARN"):
            level = "INFO"
        if (level, doc, msg) not in self.rows:
            self.rows.append((level, doc, msg))

    def print(self) -> int:
        order = {"FAIL": 0, "WARN": 1, "INFO": 2, "PASS": 3}
        for level, doc, msg in sorted(self.rows, key=lambda r: (order[r[0]], r[1])):
            print(f"{level:4}  {doc:40}  {msg}")
        counts = Counter(level for level, _, _ in self.rows)
        print()
        print("Summary: " + ", ".join(f"{k} {counts.get(k, 0)}" for k in ("FAIL", "WARN", "INFO", "PASS")))
        return 1 if counts.get("FAIL") else 0


# ---------------------------------------------------------------- helpers
def norm_id(ident: str) -> str:
    return re.sub(r"\d+", lambda m: str(int(m.group(0))), ident)


def anchor(title: str) -> str:
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", title.lower()))


def prose_lines(text: str) -> list[str]:
    """Lines with fenced blocks blanked and inline code removed (line count preserved)."""
    out, fenced = [], False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else re.sub(r"`[^`]*`", "", ln))
    return out


def headings(text: str) -> list[tuple[int, str, str]]:
    """(level, numeric label or '', title) for every heading outside fenced code."""
    res, fenced = [], False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            fenced = not fenced
            continue
        m = re.match(r"^(#{1,6}) (.+?)\s*$", ln)
        if m and not fenced:
            title = m.group(2)
            num = re.match(r"^(\d+(?:\.\d+)*)\.?\s", title)
            res.append((len(m.group(1)), num.group(1) if num else "", title))
    return res


def numbered_docs(docs: Path, rep: Report) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for p in sorted(docs.glob("[0-9][0-9]-*.md")):
        num = p.name[:2]
        if num in found:
            rep.add("WARN", p.name, f"duplicate document number {num} (also {found[num].name})")
        else:
            found[num] = p
    return found


def header_block(text: str) -> str:
    return "\n".join(text.split("\n")[:30])


def header_value(head: str, field: str) -> str | None:
    m = re.search(rf"\*\*{re.escape(field)}\*\*\s*\|\s*([^|]+)\|", head)
    return m.group(1).strip() if m else None


def fr_set(fragment: str) -> set[str]:
    """FR ids in a fragment, expanding ranges such as FR-1.2–FR-1.5 or FR-1.2–1.5."""
    ids = {f"FR-{a}.{b}" for a, b in RE_FR.findall(fragment)}
    for a, b, a2, c in RE_FR_RANGE.findall(fragment):
        if a2 and a2 != a:
            continue
        ids |= {f"FR-{a}.{n}" for n in range(int(b), int(c) + 1)}
    return ids


# ---------------------------------------------------------------- checks
def check_presence(docs: Path, found: dict[str, Path], profile: str, rep: Report) -> None:
    for num in PROFILES[profile]:
        if num in found:
            rep.add("PASS", found[num].name, "present")
        elif num in OPTIONAL_DOCS:
            rep.add("INFO", f"{num}-*.md", "not present (fine when the product has no domain standard; say so in the README)")
        else:
            rep.add("FAIL", f"{num}-*.md", f"missing (required by profile '{profile}')", missing=True)
    if (docs / "README.md").exists():
        rep.add("PASS", "README.md", "present")
    else:
        rep.add("FAIL", "README.md", "missing suite index", missing=True)
    if "06" in found and not (docs / "deferred.md").exists():
        rep.add("WARN", "deferred.md", "missing; required once 06 exists (unscheduled requirements go here, 'none' is fine)")
    if "01" in found and not (docs / "adr").is_dir():
        rep.add("INFO", "adr/", "no adr/ directory (fine when no decision needs a full record)")


def check_remnants(name: str, text: str, rep: Report) -> None:
    """Template tokens, guidance comments, size placeholders and <placeholders> outside code."""
    prose = prose_lines(text)
    tokens = sum(len(RE_TEMPLATE_TOKEN.findall(ln)) for ln in prose)
    comments = sum(ln.count("<!--") for ln in prose)
    sizes = sum(len(re.findall(r"— ln\b", ln)) for ln in prose)
    angle = [ln for ln in prose if (ln.startswith("#") and re.search(r"<[^>]+>", ln)) or RE_CELL_PLACEHOLDER.search(ln)]
    if tokens or comments or sizes or angle:
        parts = []
        if tokens: parts.append(f"{tokens} template token(s)")
        if comments: parts.append(f"{comments} guidance comment(s)")
        if sizes: parts.append(f"{sizes} '— ln' size(s)")
        if angle: parts.append(f"{len(angle)} heading(s)/cell(s) with <placeholder>")
        rep.add("WARN", name, "template remnants: " + ", ".join(parts))


def check_document(path: Path, text: str, rep: Report, prefixes: dict[str, str]) -> None:
    name = path.name
    lines = text.rstrip("\n").split("\n")
    first = next((ln for ln in lines if ln.strip()), "")
    m = RE_TITLE.match(first)
    if not m:
        rep.add("WARN", name, "title is not '# NN — Title'")
    elif m.group(1) != name[:2]:
        rep.add("WARN", name, f"title number {m.group(1)} differs from file number {name[:2]}")

    head = header_block(text)
    for field in HEADER_FIELDS:
        if f"**{field}**" not in head:
            rep.add("WARN", name, f"header block lacks '{field}'")
    doc_id = header_value(head, "Document ID")
    if doc_id:
        dm = RE_DOC_ID.match(doc_id)
        if not dm:
            rep.add("WARN", name, f"Document ID '{doc_id}' is not PREFIX-CODE-NNN")
        else:
            prefixes[name] = dm.group(1)
    status = header_value(head, "Status") or ""
    version = header_value(head, "Version") or ""
    if status and not RE_STATUS.match(status):
        rep.add("WARN", name, f"status '{status}' is not Draft / Pending approval / Approved vX.Y.Z (YYYY-MM-DD) / Living document — … / Superseded by …")
    if status.startswith(("Draft", "Pending approval")) and version and "-draft" not in version:
        rep.add("WARN", name, f"status '{status.split(' —')[0]}' but version '{version}' lacks '-draft'")
    if status.startswith(("Approved", "Living document")) and "-draft" in version:
        rep.add("WARN", name, f"status '{status.split(' —')[0]}' but version '{version}' still carries '-draft'")
    updated = header_value(head, "Last updated")
    if updated and not RE_DATE.search(updated):
        rep.add("WARN", name, f"'Last updated' is not an absolute ISO date: {updated}")

    hs = headings(text)
    has_toc = any(h[2] == "Table of Contents" for h in hs)
    if len(lines) > LONG_DOC_LINES and not has_toc:
        rep.add("WARN", name, f"{len(lines)} lines without a '## Table of Contents' heading")
    if has_toc:
        toc = text.split("## Table of Contents", 1)[1].split("\n## ", 1)[0]
        known = {anchor(h[2]) for h in hs}
        bad = [a for a in re.findall(r"\]\(#([^)]+)\)", toc) if a not in known]
        if bad:
            rep.add("WARN", name, f"{len(bad)} TOC link(s) do not match a heading: {', '.join(bad[:3])}")

    check_remnants(name, text, rep)
    prose = prose_lines(text)
    canon = RE_CANON.findall("\n".join(prose))
    if canon:
        terms = sorted({t.strip() for t in canon if t})
        rep.add("INFO", name, f"{len(canon)} [CANON-PENDING] marker(s)" + (f" — back-port: {', '.join(terms)}" if terms else " (use [CANON-PENDING: Term] to list the terms)"))
    filled = len(RE_FILLED.findall(text))
    if filled:
        rep.add("INFO", name, f"{filled} '*Filled during Sxx*' marker(s) (living-document skeleton)")
    if name[:2] in ("03", "04", "05") and RE_PROPOSED_ADR.search(text):
        rep.add("INFO", name, "contains a 'Proposed ADR' — number it in 01 §7 during the consistency pass")


def check_ids(found: dict[str, Path], texts: dict[str, str], rep: Report, docs: Path) -> dict[str, set[str]]:
    defs: dict[str, set[str]] = defaultdict(set)
    if "06" in found:
        ids = [f"FR-{a}.{b}" for a, b in RE_FR_DEF.findall(texts[found["06"].name])]
        for d, c in Counter(ids).items():
            if c > 1:
                rep.add("FAIL", found["06"].name, f"duplicate requirement id {d}")
        defs["FR"] = set(ids)
        rep.add("INFO", found["06"].name, f"{len(defs['FR'])} functional requirements defined")
    if "01" in found:
        defs["ADR"] = {f"ADR-{n}" for n in RE_ADR_DEF.findall(texts[found["01"].name])}
    adr_dir = docs / "adr"
    if adr_dir.is_dir():
        for p in adr_dir.glob("ADR-*.md"):
            mm = re.match(r"ADR-(\d{3,4})", p.name)
            if mm:
                defs["ADR"].add(f"ADR-{mm.group(1)}")
    plan_rows: dict[str, tuple[set[str], set[str]]] = {}
    if "09" in found:
        for ln in texts[found["09"].name].split("\n"):
            rm = RE_SPRINT_ROW.match(ln)
            if not rm:
                continue
            cells = ln.split("|")
            notes = cells[-2] if len(cells) >= 4 else ""
            named = re.search(r"FRs:\s*([^·|]+)", notes)
            implied = re.search(r"implied:\s*([^·|]+)", notes)
            plan_rows[rm.group(1)] = (fr_set(named.group(1)) if named else set(), fr_set(implied.group(1)) if implied else set())
        defs["SB"] = set(plan_rows)

    # FR coverage: sprint rows (FRs: / implied:) or deferred.md
    if defs["FR"] and "09" in found:
        named_all = set().union(*(n for n, _ in plan_rows.values())) if plan_rows else set()
        implied_all = set().union(*(i for _, i in plan_rows.values())) if plan_rows else set()
        deferred = docs / "deferred.md"
        deferred_ids = fr_set(deferred.read_text(encoding="utf-8", errors="replace")) if deferred.exists() else set()
        covered = {norm_id(x) for x in named_all | implied_all | deferred_ids}
        uncovered = sorted((f for f in defs["FR"] if norm_id(f) not in covered), key=lambda f: tuple(int(x) for x in f[3:].split(".")))
        if uncovered:
            shown = ", ".join(uncovered[:8]) + (" …" if len(uncovered) > 8 else "")
            rep.add("WARN", found["06"].name, f"{len(uncovered)} FR(s) in no {found['09'].name} sprint row (FRs:/implied:) and not in deferred.md: {shown}")
        only_implied = {f for f in implied_all if f not in named_all}
        rep.add("INFO", found["09"].name, f"sprint rows name {len(named_all)} FR(s); {len(only_implied)} covered only as implied; {len(deferred_ids)} deferred")
        # 06 Appendix A versus 09
        app_rows = {}
        stale = sum(len(RE_PENDING_CELL.findall(ln)) for ln in texts[found["06"].name].split("\n") if ln.startswith("| FR-"))
        if stale:
            rep.add("WARN", found["06"].name, f"Appendix A still has {stale} '— (09 pending)' cell(s) although {found['09'].name} exists — regenerate")
        for ln in texts[found["06"].name].split("\n"):
            if ln.startswith("**Unscheduled"):
                break
            am = re.match(r"^\| (FR-\d+\.\d+) \|", ln)
            if am:
                id_cells = [c for c in ln.split("|")[2:] if c.strip() and re.fullmatch(r"[\sS\d\-B,()a-z]*", c) and RE_SB.search(c)]
                ids = {f"S{a}-B{b}" for c in id_cells for a, b in RE_SB.findall(c)}
                if ids:
                    app_rows[am.group(1)] = ids
        if app_rows:
            plan_map = defaultdict(set)
            for row, (n, i) in plan_rows.items():
                for f in n | i:
                    plan_map[norm_id(f)].add(row)
            mismatched = [f for f, ids in app_rows.items() if ids != plan_map.get(norm_id(f), set())]
            if mismatched:
                rep.add("WARN", found["06"].name, f"Appendix A disagrees with {found['09'].name} for {len(mismatched)} FR(s) (09 wins; regenerate): {', '.join(mismatched[:6])}")

    for name, text in texts.items():
        used = {
            "FR": {f"FR-{a}.{b}" for a, b in RE_FR.findall(text)},
            "ADR": {f"ADR-{n}" for n in RE_ADR.findall(text)},
            "SB": {f"S{a}-B{b}" for a, b in RE_SB.findall(text)},
        }
        for fam, owner in (("FR", "06"), ("ADR", "01"), ("SB", "09")):
            if owner not in found or name == found[owner].name:
                continue
            defined = {norm_id(d) for d in defs[fam]}
            for u in sorted(u for u in used[fam] if norm_id(u) not in defined):
                rep.add("WARN", name, f"references {u}, not defined in {found[owner].name}")
    return defs


def check_cross_refs(docs: Path, found: dict[str, Path], texts: dict[str, str], rep: Report, profile: str) -> None:
    numbered: dict[str, set[str]] = {p.name: {h[1] for h in headings(texts[p.name]) if h[1]} for p in found.values()}
    for name, text in texts.items():
        for ln in (text.split("\n") if name != "README.md" else []):
            refs = list(RE_FILE_REF.finditer(ln))
            for i, m in enumerate(refs):
                target = m.group(1)
                if not (docs / target).exists():
                    if target[:2] in PROFILES[profile]:
                        rep.add("FAIL", name, f"cites `{target}` which does not exist", missing=True)
                    else:
                        rep.add("INFO", name, f"cites optional `{target}`, which does not exist")
                    continue
                window = ln[m.end(): refs[i + 1].start() if i + 1 < len(refs) else len(ln)]
                window = window.split(";")[0]
                window = re.split(r"\b\d{2}\s*§", window)[0]
                for sec in RE_SECTION.findall(window):
                    if sec in numbered.get(target, set()):
                        continue
                    top = sec.split(".")[0]
                    if top in numbered.get(target, set()):
                        rep.add("INFO", name, f"cites `{target}` §{sec}: no heading numbered {sec} (§{top} exists)")
                    else:
                        rep.add("WARN", name, f"cites `{target}` §{sec}: no section {sec} in that document")
        for link in set(RE_MD_LINK.findall(text)):
            if link.startswith(("http://", "https://")):
                continue
            target = (docs / unquote(link)).resolve()
            if not target.exists():
                level = "FAIL" if name == "README.md" else "WARN"
                rep.add(level, name, f"links to missing file {link}", missing=True)


def check_permissions(found: dict[str, Path], texts: dict[str, str], rep: Report) -> None:
    source = found.get("07") or found.get("05")
    if not source:
        return
    perms: set[str] = set()
    for ln in texts[source.name].split("\n"):
        if ln.startswith("| `"):
            perms |= {t for t in RE_PERM.findall(ln.split("|")[1]) if t.split(".")[1] not in FILE_EXT}
    if not perms:
        return
    prefixes = {p.split(".")[0] for p in perms}
    used: set[str] = set()
    for num in ("05", "06", "12"):
        if num not in found or found[num] == source:
            continue
        name = found[num].name
        tokens = {t for t in RE_PERM.findall(texts[name]) if t.split(".")[0] in prefixes and t.split(".")[1] not in FILE_EXT and not t.endswith("ed") and t not in PERM_IGNORE}
        used |= tokens
        missing = sorted(tokens - perms)
        if missing:
            rep.add("WARN", name, f"{len(missing)} permission string(s) not in {source.name}: {', '.join(missing[:6])}")
    orphans = sorted(perms - used)
    if orphans and used:
        rep.add("INFO", source.name, f"{len(orphans)} permission(s) no endpoint or requirement cites: {', '.join(orphans[:6])}")


def check_readme(docs: Path, found: dict[str, Path], texts: dict[str, str], rep: Report) -> None:
    readme = docs / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8", errors="replace")
    linked = {Path(unquote(l)).name for l in RE_MD_LINK.findall(text)}
    for p in found.values():
        if p.name not in linked:
            rep.add("WARN", "README.md", f"{p.name} exists but is not in the index")
    for needle, label in (("review order", "recommended review order"),
                          ("decisions needed", "'Decisions needed' (approval blockers) section"),
                          ("**status**", "status banner")):
        if needle not in text.lower():
            rep.add("WARN", "README.md", f"no {label}")
    # sizes
    for ln in text.split("\n"):
        lm = re.search(r"\]\((\d{2}-[a-z0-9-]+\.md)\)", ln)
        sm = re.search(r"\|\s*~?([\d,]+) ln\s*\|", ln)
        if lm and sm and lm.group(1) in texts:
            claimed = int(sm.group(1).replace(",", ""))
            actual = len(texts[lm.group(1)].rstrip("\n").split("\n"))
            if abs(claimed - actual) > SIZE_TOLERANCE * max(actual, 1):
                rep.add("WARN", "README.md", f"index says {lm.group(1)} is {claimed} ln, file has {actual}")
    # decisions needed vs 01 §10
    if "01" in found:
        one = texts[found["01"].name]
        sec = re.search(r"^## 10\..*?(?=^## |\Z)", one, re.S | re.M)
        dec = re.search(r"^## .*decisions needed.*?(?=^## |\Z)", text, re.S | re.M | re.I)
        if sec and dec:
            n_one = len(re.findall(r"^\d+\. ", sec.group(0), re.M))
            n_readme = len(re.findall(r"^\d+\. ", dec.group(0), re.M))
            if n_readme < n_one:
                rep.add("WARN", "README.md", f"Decisions needed lists {n_readme} item(s); 01 §10 has {n_one}")


def check_api(docs: Path, found: dict[str, Path], texts: dict[str, str], rep: Report) -> None:
    if "05" not in found or "api/openapi.yaml" not in texts[found["05"].name]:
        return
    spec = docs.parent / "api" / "openapi.yaml"
    if not spec.exists():
        rep.add("WARN", found["05"].name, "names api/openapi.yaml but the file does not exist", missing=True)
        return
    has_version = any(re.match(r"^openapi:\s*['\"]?3", ln) for ln in spec.read_text(encoding="utf-8", errors="replace").split("\n"))
    if not has_version:
        rep.add("WARN", found["05"].name, "api/openapi.yaml has no top-level 'openapi: 3.x' line")
    else:
        rep.add("PASS", "api/openapi.yaml", "present, OpenAPI 3")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docs", type=Path, help="path to the docs/ directory")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="standard")
    ap.add_argument("--allow-missing", action="store_true", help="authoring-time mode (see module docstring)")
    args = ap.parse_args(argv)
    docs: Path = args.docs
    if not docs.is_dir():
        print(f"error: {docs} is not a directory", file=sys.stderr)
        return 2

    rep = Report(args.allow_missing)
    found = numbered_docs(docs, rep)
    texts = {p.name: p.read_text(encoding="utf-8", errors="replace") for p in found.values()}
    if (docs / "README.md").exists():
        texts["README.md"] = (docs / "README.md").read_text(encoding="utf-8", errors="replace")

    check_presence(docs, found, args.profile, rep)
    extras = [docs / "README.md", docs / "deferred.md", docs.parent / "BACKLOG.md"]
    if (docs / "adr").is_dir():
        extras += sorted((docs / "adr").glob("ADR-*.md"))
    for extra in extras:
        if extra.exists():
            check_remnants(extra.name if extra.parent != docs / "adr" else f"adr/{extra.name}", extra.read_text(encoding="utf-8", errors="replace"), rep)
    prefixes: dict[str, str] = {}
    for p in found.values():
        check_document(p, texts[p.name], rep, prefixes)
    if prefixes:
        common = Counter(prefixes.values()).most_common(1)[0][0]
        for name, pre in prefixes.items():
            if pre != common:
                rep.add("WARN", name, f"Document ID prefix '{pre}' differs from the suite's '{common}'")
    check_ids(found, texts, rep, docs)
    check_cross_refs(docs, found, texts, rep, args.profile)
    check_permissions(found, texts, rep)
    check_readme(docs, found, texts, rep)
    check_api(docs, found, texts, rep)
    return rep.print()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
