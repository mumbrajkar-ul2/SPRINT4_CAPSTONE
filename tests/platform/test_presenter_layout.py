"""Presenter layout for the Phase 17 console."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PANELS = ("Situation", "Evidence", "Actions", "Result", "Audit")
TOKENS = (
    "#ED1C24",
    "#231F20",
    "#72007D",
    "#EFBC4A",
    "#FFFFFF",
    "#F2F2F2",
    "#FDEBEC",
    "#FCF3DE",
    "#666666",
    "#E0E0E0",
)
HEADER_FIELDS = (
    "Birlasoft",
    "Application",
    "Location",
    "Role picker",
    "Actor id",
    "Runtime mode",
    "Start this shift again",
)


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
        for token in TOKENS:
            assert token in style
        assert "font-family: Calibri" in style
        assert "background: #e8eef2" not in style
        assert "color: #1c2833" not in style
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


def test_birlasoft_screen_contract() -> None:
    for folder in ("app_a", "app_b"):
        page = (ROOT / "apps" / folder / "ui" / "src" / "App.jsx").read_text(encoding="utf-8")
        style = (ROOT / "apps" / folder / "ui" / "public" / "assets" / "styles.css").read_text(encoding="utf-8")
        for field in HEADER_FIELDS:
            assert field in page
        assert 'role="tablist"' in page
        assert 'role="tab"' in page
        assert "aria-selected={scenario === name}" in page
        assert 'aria-current={scenario === name ? "page" : undefined}' in page
        assert "scenario-current" in page
        assert "function onTabKey" in page
        assert 'className="primary"' in page
        assert "button.primary" in style
        assert "background: #ED1C24" in style
        assert "font-size: 16px" in style
        assert "font-weight: 600" in style
        for token in TOKENS:
            assert token in style
        assert ".page-bar" in style
        assert "width: 16px" in style
        assert "background: #F2F2F2" in style
        assert "background: #FCF3DE" in style
        assert "border-left: 4px solid #EFBC4A" in style
        assert "border-left: 4px solid #231F20" in style
        assert "function withLead" in page
        assert 'lead = tone === "failed" ? "Failed" : "Refused"' in page
        assert "function openScenario" in page
        assert 'setActionStatus("")' in page
        assert "setExplain(emptyExplain())" in page
        assert "setAuditRows([])" in page
        assert "setOther(null)" in page
        assert "viewRef.current !== started" in page
        assert "(explain.answer_source || explain.sentence)" in page
        assert '(auditId || auditRows.length || (scenario === "Recipe" && lineage))' in page
        assert 'className="logo-word"' in page
        assert "<img" not in page
        assert page.count('className="cover-motif"') == 1
        assert "strokeWidth=\"8\"" in page or 'strokeWidth="8"' in page
        assert "#72007D" in style
        assert "action-ready" in page
        for retired in ("#143044", "#0e7c66", "#c9842a", "#e8eef2", "#1c2833", "Segoe UI"):
            assert retired not in style


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
