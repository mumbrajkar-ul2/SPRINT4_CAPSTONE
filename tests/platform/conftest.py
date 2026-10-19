"""Shared path and environment for platform tests."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "context-lake") not in sys.path:
    sys.path.insert(0, str(ROOT / "context-lake"))

os.environ.setdefault("FABPULSE_API_KEY", "local-demo-only")
os.environ.setdefault("MODEL_MODE", "replay")


@pytest.fixture
def api_headers() -> dict[str, str]:
    return {
        "X-Api-Key": os.environ["FABPULSE_API_KEY"],
        "X-Actor-Id": "demo-rt01-1",
        "X-Actor-Role": "RT-01",
    }


@pytest.fixture
def lake_headers() -> dict[str, str]:
    return {"X-Api-Key": os.environ["FABPULSE_API_KEY"]}
