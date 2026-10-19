"""AT-COMPOSE-PORTS and AT-CI-SAFE."""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "compose.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "verify.yml"
REQUIRED_PORTS = {8080, 8090, 8091, 8092, 8100, 8110}
REQUIRED_CONTAINERS = {
    "fabpulse-legacy",
    "fabpulse-source-gateway",
    "fabpulse-bridge",
    "fabpulse-lake-rest",
    "fabpulse-lake-mcp",
    "fabpulse-app-a",
    "fabpulse-app-b",
}


def test_at_compose_ports_in_file() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    payload = yaml.safe_load(text)
    services = payload["services"]
    names = {row.get("container_name") for row in services.values()}
    assert names == REQUIRED_CONTAINERS
    for mapping in (
        '"${HOST_PORT:-8080}:8080"',
        '"${SOURCE_HOST_PORT:-8090}:8090"',
        '"${LAKE_REST_PORT:-8091}:8091"',
        '"${LAKE_MCP_PORT:-8092}:8092"',
        '"${APP_A_PORT:-8100}:8100"',
        '"${APP_B_PORT:-8110}:8110"',
    ):
        assert mapping in text
    env_blob = str(services["app-a"]["environment"]) + str(services["lake-rest"]["environment"])
    assert "MODEL_MODE" in env_blob
    assert "replay" in env_blob
    assert "8100" in str(services["app-a"]["ports"])
    assert "8080" in str(services["legacy"]["ports"])


def test_at_compose_config_when_docker_exists() -> None:
    try:
        completed = subprocess.run(
            ["docker", "compose", "config"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return
    if completed.returncode != 0:
        return
    text = completed.stdout
    for port in REQUIRED_PORTS:
        assert str(port) in text
    for name in REQUIRED_CONTAINERS:
        assert name in text


def test_at_ci_safe() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "generate --reset" not in text
    assert "app.generate" not in text
    assert "openai" not in text.lower()
    assert "azure" not in text.lower()
    assert "MODEL_MODE=replay" in text or "MODEL_MODE: replay" in text
    assert "docker compose config" in text
