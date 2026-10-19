"""DB-02 environment defaults sit in .env.example."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / ".env.example").read_text(encoding="utf-8")


def test_env_example_lists_required_defaults() -> None:
    assert "FABPULSE_API_KEY=local-demo-only" in TEXT
    assert "MODEL_MODE=replay" in TEXT
    assert "HOST_PORT=8080" in TEXT
    assert "SOURCE_HOST_PORT=8090" in TEXT
    assert "LAKE_REST_PORT=8091" in TEXT
    assert "LAKE_MCP_PORT=8092" in TEXT
    assert "APP_A_PORT=8100" in TEXT
    assert "APP_B_PORT=8110" in TEXT
