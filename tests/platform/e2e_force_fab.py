"""Opt-in cookie-jar smoke. Set FF_E2E=1 when identity and both apps are already running.

This file does not start the stack and does not copy a database.
"""
from __future__ import annotations

import http.cookiejar
import os
import urllib.request

import pytest

pytestmark = pytest.mark.skipif(os.environ.get("FF_E2E") != "1", reason="Set FF_E2E=1 to run the live cookie-jar smoke.")


def test_live_sign_in_uses_one_cookie_jar() -> None:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    me = opener.open("http://127.0.0.1:8100/auth/me", timeout=5)
    assert me.status in {200, 401}
    health = opener.open("http://127.0.0.1:8095/health", timeout=5)
    assert health.status == 200
    other = opener.open("http://127.0.0.1:8110/healthz", timeout=5)
    assert other.status == 200
