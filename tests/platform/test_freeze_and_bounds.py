"""AT-FREEZE, secret scan, and no app-feature handlers."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INHERITED = ROOT / "fabpulse-legacy-workshop-v8-Semiconductor" / "fabpulse-legacy"
REGISTER = ROOT / "sources" / "register.yaml"
PACKAGED = {
    "data/legacy.sqlite3": INHERITED / "data" / "legacy.sqlite3",
    "data/enterprise_legacy.sqlite3": INHERITED / "data" / "enterprise_legacy.sqlite3",
}
APP_B_DIR = ROOT / "apps" / "app_b"
FORBIDDEN_APP_B_STRINGS = (
    "apps.app_a.rules",
    "fabpulse-legacy-workshop",
    "8100",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hashes_from_register() -> dict[str, str]:
    found: dict[str, str] = {}
    current = None
    for raw in REGISTER.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- path:"):
            current = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("sha256:") and current in PACKAGED:
            found[current] = line.split(":", 1)[1].strip()
            current = None
    return found


def test_at_freeze_packaged_hashes() -> None:
    expected = hashes_from_register()
    for rel, path in PACKAGED.items():
        assert sha256_file(path) == expected[rel]


def test_application_source_has_no_key_literal() -> None:
    roots = [ROOT / "apps", ROOT / "context-lake" / "rest_server.py", ROOT / "context-lake" / "mcp_server.py"]
    for root in roots:
        paths = [root] if root.is_file() else root.rglob("*.py")
        for path in paths:
            text = path.read_text(encoding="utf-8")
            assert "local-demo-only" not in text, path


def test_no_app_b_feature_handlers() -> None:
    """Application B source must not import apps.app_a.rules, mention fabpulse-legacy-workshop, or call port 8100."""
    blob = "\n".join(path.read_text(encoding="utf-8") for path in APP_B_DIR.rglob("*.py"))
    for snippet in FORBIDDEN_APP_B_STRINGS:
        assert snippet not in blob
    stub = (ROOT / "apps" / "shared" / "app_stub.py").read_text(encoding="utf-8")
    assert "identity-check" in stub or "identity-check" in blob
