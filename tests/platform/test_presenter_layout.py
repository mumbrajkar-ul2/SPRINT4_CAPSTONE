"""Presenter layout for the Force Fab scenario console."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHELL = ROOT / "apps" / "ui_shared" / "src" / "DemoApp.jsx"
THEME = ROOT / "apps" / "ui_shared" / "src" / "theme.css"
SCENARIOS = ("Replay", "Recipe", "Clocks", "Policy", "Outage", "Rule trace", "Compare")


def test_shared_shell_keeps_the_seven_scenario_tabs() -> None:
    page = SHELL.read_text(encoding="utf-8")
    style = THEME.read_text(encoding="utf-8")
    assert "color-scheme: dark" in style
    assert 'className="logo-word"' in page
    assert "Force Fab" in page
    assert "by TSM Corp." in page
    assert "<img" not in page
    for name in SCENARIOS:
        assert name in page
    assert "scenario-current" in page
    assert "result-sentence" in page
    assert "action-status" in page
    assert "action-ready" in page
    assert "function withLead" in page
    assert "function openScenario" in page
    assert "Start this shift again" in page
    assert "window.location.hostname" in page
    assert 'credentials: "include"' in page
    assert "8100" not in page
    reset = (ROOT / "apps" / "shared" / "demo_routes.py").read_text(encoding="utf-8")
    assert "This shift started again. The session overlay is clear." in reset
    session = (ROOT / "apps" / "shared" / "demo_session.py").read_text(encoding="utf-8")
    assert "corr-p10b-doc-20261018-001" in session


def test_both_apps_use_the_shared_shell() -> None:
    for folder in ("app_a", "app_b"):
        page = (ROOT / "apps" / folder / "ui" / "src" / "App.jsx").read_text(encoding="utf-8")
        assert '@ff/DemoApp.jsx' in page


def test_shell_menu_labels_and_theme_tokens() -> None:
    page = SHELL.read_text(encoding="utf-8")
    kit = (ROOT / "apps" / "ui_shared" / "src" / "pages" / "kit.jsx").read_text(encoding="utf-8")
    style = THEME.read_text(encoding="utf-8")
    for label in ("Home", "Dashboard", "Cases", "Approvals", "Scenarios", "Partner feeds", "Knowledge graph", "Glossary", "Audit", "Fault scenarios"):
        assert label in kit
    assert "ff-shell" in page
    assert "ff-return" in page
    for token in ("#14181d", "#1d242c", "#f4f1ea", "#b7c0c8", "#33404a", "#d85a45"):
        assert token in style
    assert "8100" not in page


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
