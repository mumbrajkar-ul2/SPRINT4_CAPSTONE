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
        assert "background: #e8eef2" in style
        assert "color: #1c2833" in style
        assert "Answer source:" in page
        assert "action-status" in page
        assert "function openScenario" in page
        assert "openScenario(name)" in page
        assert "C00001646" in page
        assert "L00000016" in page
        assert "E-00000000" in page
        assert "FAB-00000002" in page
        assert "INC-2025-014" in page
        assert "Recipe rule path" in page
        assert "Both apps" in page
        assert "Review this delivery" in page
        assert "This delivery" in page
        assert "Drop is recorded only by RT-05 Operations Analyst." in page
        assert "Hold is recorded only by RT-03 Process Engineer, and that person must differ from the draft author." in page
        assert "A policy decision is recorded only by RT-04 Policy Owner." in page
        assert "The owner is recorded only by RT-06 Operations Lead." in page
        assert "not recorded" in page
        assert "Record the owner" in page
        assert "onClick={onHold}" in page
        assert "disabled={holdDisabled}" not in page
        assert "Access and untrusted text" in page
    agent = (ROOT / "apps" / "app_a" / "routes" / "agent.py").read_text(encoding="utf-8")
    assert 'os.environ["MODEL_MODE"] = "replay"' not in agent


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
