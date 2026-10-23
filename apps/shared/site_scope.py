"""Site labels on a token, and the lake site codes those labels cover.

FAB-01 and FAB-02 are access labels. They are not country names on a data row.
A row with no site stays readable. The five scenario ids stay readable for every signed-in role.
"""
from __future__ import annotations

EXEMPT_IDS = {
    "REPLAY-000000000",
    "PS000000016",
    "E-00000000",
    "FAB-00000002",
    "INC-2025-014",
}

_FAB_01_CODES = {"JP-KN", "IN-BLR", "DE-BY", "FAB-01"}
_FAB_02_CODES = {"US-TX", "BR-SP", "GB-ENG", "FAB-02"}


def path_skips_site(path: str) -> bool:
    if path == "/api/queue" or path.startswith("/api/queue/"):
        return True
    if path.startswith("/api/demo/") or path == "/api/demo":
        return True
    return False


def fab_label(site_code: str | None) -> str | None:
    if not site_code:
        return None
    if site_code in _FAB_01_CODES:
        return "FAB-01"
    if site_code in _FAB_02_CODES:
        return "FAB-02"
    return None


def site_visible(user_sites: list[str] | None, site_code: str | None, record_id: str | None = None) -> bool:
    if record_id and record_id in EXEMPT_IDS:
        return True
    if not site_code:
        return True
    label = fab_label(site_code)
    if label is None:
        return True
    return label in (user_sites or [])
