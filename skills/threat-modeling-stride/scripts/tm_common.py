"""Constants and helpers shared by build_report.py (validation, diagrams) and report_html.py (page)."""
from __future__ import annotations

import html

APPLICABLE = {"entity": "SR", "process": "STRIDE", "store": "TRID", "flow": "TID"}   # categories a threat may target
REQUIRED = {"entity": "SR", "process": "STRIDE", "store": "TID", "flow": "TID"}       # cells the coverage matrix demands; a store with `audit: true` also requires R
CLASSES = {"public", "internal", "confidential", "restricted"}
STATUSES = {"open", "mitigated", "accepted", "transferred"}
STATUSES_NEED = {"open": ("sprint", "plan"), "accepted": ("approver",), "transferred": ("agreement",)}
CATEGORY = {"S": "Spoofing", "T": "Tampering", "R": "Repudiation", "I": "Information disclosure", "D": "Denial of service", "E": "Elevation of privilege"}
BANDS = [(20, "Critical"), (12, "High"), (6, "Medium"), (1, "Low")]
BAND_ORDER = ("Critical", "High", "Medium", "Low")
EFFORTS = {"S", "M", "L"}
SHAPE = {"entity": "box", "process": "ellipse", "store": "cylinder"}


def esc(s) -> str:
    """HTML-escape any value (None becomes the empty string)."""
    return html.escape("" if s is None else str(s), quote=True)


def band(score: int) -> str:
    return next(b for lo, b in BANDS if score >= lo)


def plan_of(t: dict) -> str:
    return str(t.get("sprint") or t.get("plan") or "")
