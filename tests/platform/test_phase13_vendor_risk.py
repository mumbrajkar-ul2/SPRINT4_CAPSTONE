"""Phase 13 Half B vendor-risk tests. HB-33-01. SC-33-01."""
from __future__ import annotations

import os
import socket
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from apps.app_a.agent.tools import WRITE_TOOLS
from apps.app_a.intelligence import generate as generate_mod
from apps.app_a.server import app as app_a

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "compose.yaml"
APP_B_DIR = ROOT / "apps" / "app_b"
DOCS = ROOT / "docs" / "33-vendor-risk"
INVENTORY = DOCS / "vendor-inventory.md"
CONCENTRATION = DOCS / "concentration-risk-analysis.md"
LOCK_IN = DOCS / "lock-in-analysis.md"
PORTABILITY = DOCS / "portability-assessment.md"
EXIT_PLAN = DOCS / "exit-plan.md"
VENDOR_DOCS = (INVENTORY, CONCENTRATION, LOCK_IN, PORTABILITY, EXIT_PLAN)
HIT_QUESTION = "Which port does the Context Lake REST listener use?"
MISS_QUESTION = "What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file"
HIT_CORR = "corr-p13-33b-doc-20261018-001"
MISS_CORR = "corr-p13-33b-miss-001"
PROBE_HEADERS = {
    "X-Api-Key": "local-demo-only",
    "X-Actor-Id": "demo-rt01-1",
    "X-Actor-Role": "RT-01",
    "X-Correlation-Id": HIT_CORR,
}
APP_B_PYTHONPATH = "/opt/platform:/opt/platform/context-lake"
APP_A_INHERITED = (
    "/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy"
)
MODEL_MODE_DEFAULT = "${MODEL_MODE:-replay}"
FORBIDDEN_APP_B = (
    "apps.app_a.rules",
    "fabpulse-legacy-workshop",
    "8100",
    "complete_azure",
    "azure_client",
)
TEXT_SUFFIXES = {".py", ".js", ".html", ".css", ".yaml", ".yml", ".json", ".md", ".txt"}


def _compose() -> dict:
    return yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))


def _service_env(name: str) -> dict:
    env = _compose()["services"][name]["environment"]
    assert isinstance(env, dict)
    return env


def _app_b_blob() -> str:
    parts: list[str] = []
    for path in APP_B_DIR.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


@pytest.fixture
def replay_only(monkeypatch):
    monkeypatch.setenv("MODEL_MODE", "replay")
    monkeypatch.setenv("FABPULSE_API_KEY", "local-demo-only")
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_VERSION", raising=False)

    def boom(*_args, **_kwargs):
        raise AssertionError("Azure must not be called during HB-33-01")

    def forbid(*_args, **_kwargs):
        raise AssertionError("HB-33-01 must not open a network socket")

    monkeypatch.setattr("apps.app_a.intelligence.azure_client.complete_azure", boom)
    monkeypatch.setattr("apps.app_a.intelligence.generate.complete_azure", boom)
    monkeypatch.setattr(socket, "create_connection", forbid)

    real_generate = generate_mod.generate

    def guarded_generate(*args, **kwargs):
        previous_socket = socket.socket
        socket.socket = forbid  # type: ignore[method-assign]
        try:
            return real_generate(*args, **kwargs)
        finally:
            socket.socket = previous_socket

    monkeypatch.setattr(generate_mod, "generate", guarded_generate)
    monkeypatch.setattr("apps.app_a.routes.query.generate", guarded_generate)
    yield


def test_hb33_01_compose_model_mode_replay_for_app_a_and_app_b() -> None:
    app_a_env = _service_env("app-a")
    app_b_env = _service_env("app-b")
    assert app_a_env["MODEL_MODE"] == MODEL_MODE_DEFAULT
    assert app_b_env["MODEL_MODE"] == MODEL_MODE_DEFAULT
    for name in (
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_API_VERSION",
    ):
        assert app_a_env[name] == f"${{{name}:-}}"
        assert name not in app_b_env


def test_hb33_01_compose_app_b_pythonpath_omits_inherited_tree() -> None:
    pythonpath = _service_env("app-b")["PYTHONPATH"]
    assert pythonpath == APP_B_PYTHONPATH
    assert "fabpulse-legacy" not in pythonpath
    parts = pythonpath.split(":")
    assert parts == ["/opt/platform", "/opt/platform/context-lake"]


def test_hb33_01_compose_app_a_pythonpath_keeps_inherited_tree() -> None:
    pythonpath = _service_env("app-a")["PYTHONPATH"]
    parts = pythonpath.split(":")
    assert len(parts) == 3
    assert parts[0] == "/opt/platform"
    assert parts[1] == "/opt/platform/context-lake"
    assert parts[2] == APP_A_INHERITED
    assert "fabpulse-legacy-workshop" in parts[2]


def test_hb33_01_app_b_source_omits_inherited_and_port_8100() -> None:
    blob = _app_b_blob()
    assert "apps.app_a.rules" not in blob
    assert "fabpulse-legacy-workshop" not in blob
    assert "8100" not in blob


def test_hb33_01_app_b_source_has_no_azure_client() -> None:
    blob = _app_b_blob()
    assert "complete_azure" not in blob
    assert "azure_client" not in blob
    azure_files = list(APP_B_DIR.rglob("*azure*"))
    assert azure_files == []


def test_hb33_01_app_a_query_under_replay_finishes_without_azure(replay_only) -> None:
    assert os.environ.get("MODEL_MODE") == "replay"
    assert WRITE_TOOLS == []

    client = TestClient(app_a)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"ok": True}

    miss = client.post(
        "/api/query",
        headers={**PROBE_HEADERS, "X-Correlation-Id": MISS_CORR},
        json={"question": MISS_QUESTION},
    )
    miss_body = miss.json()
    assert miss.status_code == 200
    assert miss_body["verdict"] == "ABSTAIN"
    assert miss_body["error_class"] == "replay_miss"
    assert miss_body["sentence"] == ""
    assert miss_body["correlation_id"] == MISS_CORR

    hit = client.post(
        "/api/query",
        headers=PROBE_HEADERS,
        json={"question": HIT_QUESTION},
    )
    hit_body = hit.json()
    assert hit.status_code == 200
    assert hit_body["verdict"] == "ANSWER"
    assert hit_body["error_class"] is None
    assert "arch.listener.lake_rest_8091" in (hit_body.get("citations") or [])
    assert hit_body["sentence"]
    assert hit_body["correlation_id"] == HIT_CORR


def test_hb33_01_before_snapshot_is_recorded() -> None:
    text = INVENTORY.read_text(encoding="utf-8")
    assert "HB-33-01 before" in text
    assert "Measured before" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert "unasserted by this pack" in text
    assert "tests/platform/test_phase13_vendor_risk.py" in text


def test_hb33_01_docs_keep_bo11_proposed_and_simulated_figures() -> None:
    for path in VENDOR_DOCS:
        text = path.read_text(encoding="utf-8")
        assert "BO-11" in text, path.name
        assert "PROPOSED" in text, path.name
        assert "BO-11 stays PROPOSED" in text, path.name
        assert "SIGNED" not in text, path.name
    money = INVENTORY.read_text(encoding="utf-8") + "\n" + EXIT_PLAN.read_text(encoding="utf-8")
    assert "4982.61" in money
    assert "0.603" in money
    assert "SIMULATED" in money
    assert "not vendor spend" in money.lower() or "are not vendor spend" in money


def test_hb33_01_after_snapshot_is_recorded() -> None:
    text = INVENTORY.read_text(encoding="utf-8")
    assert "HB-33-01 after" in text
    assert "Measured after" in text
    assert "Honesty | REAL" in text or "Honesty: REAL" in text
    assert MODEL_MODE_DEFAULT in text
    assert APP_B_PYTHONPATH in text
    assert APP_A_INHERITED in text
    assert "complete_azure" in text
    assert "azure_client" in text
    assert "ABSTAIN" in text
    assert "ANSWER" in text
    assert "Unknown" in text
    for path in VENDOR_DOCS:
        body = path.read_text(encoding="utf-8")
        assert "HB-33-01" in body, path.name
        assert "Honesty" in body, path.name
        assert "STOP. Wait for HALF_A_ACCEPTED" not in body, path.name
        assert "Unit price" in body or "unit price" in body, path.name
