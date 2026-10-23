"""Shared path and environment for platform tests."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "context-lake") not in sys.path:
    sys.path.insert(0, str(ROOT / "context-lake"))

os.environ.setdefault("FABPULSE_API_KEY", "local-demo-only")
os.environ.setdefault("MODEL_MODE", "replay")

from apps.identity.crypto_util import load_or_create_key  # noqa: E402
from apps.shared.oidc_session import bearer_headers, mint_token  # noqa: E402

_KEY_DIR = Path(tempfile.mkdtemp(prefix="ff-jwks-"))
load_or_create_key(_KEY_DIR)
os.environ["FF_JWT_PRIVATE_FILE"] = str(_KEY_DIR / "signing_key.pem")
os.environ["FF_JWKS_FILE"] = str(_KEY_DIR / "jwks.json")
os.environ["FF_IDP_PUBLIC_URL"] = "http://127.0.0.1:8095"
os.environ["FF_COOKIE_SECRET"] = "test-cookie-secret"
os.environ["FF_RATE_LIMIT_PER_MIN"] = "100000"
os.environ["FF_LAKE_TOKEN"] = mint_token(
    sub="svc-lake",
    roles=["SVC"],
    sites=[],
    aud="force-fab-lake",
    acr="pwd",
    amr=["client"],
)


@pytest.fixture
def api_headers() -> dict[str, str]:
    return bearer_headers("RT-01")


@pytest.fixture
def lake_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {os.environ['FF_LAKE_TOKEN']}"}
