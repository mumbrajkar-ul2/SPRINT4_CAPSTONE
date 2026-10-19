"""AT-REPLAY-HIT and AT-REPLAY-MISS."""
from __future__ import annotations

import socket

from operations.replay_lookup import lookup, prompt_hash

FIXTURE_PROMPT = "phase8-replay-fixture-prompt"
FIXTURE_HASH = "adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7"


def test_fixture_hash_matches() -> None:
    assert prompt_hash(FIXTURE_PROMPT) == FIXTURE_HASH


def test_at_replay_hit() -> None:
    result = lookup(FIXTURE_PROMPT, mode="replay")
    assert result["ok"] is True
    assert result["event"] == "replay_hit"
    assert "phase8-replay-unit-body" in result["body"]
    assert "PRECOMPUTED" in result["body"]


def test_at_replay_miss_stays_local(monkeypatch) -> None:
    def forbid(*_args, **_kwargs):
        raise AssertionError("replay must not open a network socket")

    monkeypatch.setattr(socket, "create_connection", forbid)
    monkeypatch.setattr(socket, "socket", forbid)
    result = lookup("no-saved-file-for-this-prompt", mode="replay")
    assert result["ok"] is False
    assert result["error_class"] == "replay_miss"
    assert result["event"] == "replay_miss"
