"""Presenter layout for the Phase 17 console."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PANELS = ("Situation", "Evidence table", "One action", "Result", "Audit rows")


def test_both_apps_have_the_console_layout() -> None:
    for folder in ("app_a", "app_b"):
        page = (ROOT / "apps" / folder / "ui" / "src" / "App.jsx").read_text(encoding="utf-8")
        style = (ROOT / "apps" / folder / "ui" / "public" / "assets" / "styles.css").read_text(encoding="utf-8")
        assert "console-header" in page
        assert "scenario-current" in page
        assert 'className="primary"' in page
        assert "later-checks" in page
        assert "result-sentence" in page
        for name in PANELS:
            assert name in page
        assert "background: #f4f6f8" in style
        assert "color: #1a1a1a" in style


def test_application_b_source_has_no_port_8100() -> None:
    hits: list[str] = []
    root = ROOT / "apps" / "app_b"
    for path in root.rglob("*"):
        if "node_modules" in path.parts:
            continue
        if not path.is_file() or path.suffix.lower() not in {".py", ".js", ".jsx", ".html", ".css"}:
            continue
        if "8100" in path.read_text(encoding="utf-8"):
            hits.append(str(path.relative_to(ROOT)))
    assert hits == []
