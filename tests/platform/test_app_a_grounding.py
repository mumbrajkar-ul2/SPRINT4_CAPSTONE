"""FD-14: empty citations on ANSWER become ABSTAIN. Replay miss does not open a socket."""
from __future__ import annotations

import socket

from fastapi.testclient import TestClient

from apps.app_a.intelligence.canonical import KEY_ORDER, canonical_prompt_bytes
from apps.app_a.intelligence.generate import WRITE_TOOLS, generate
from apps.app_a.intelligence.ground import ground
from apps.app_a.intelligence.prompts import CURRENT_SEMVER, PROMPT_IDS, load_prompt
from apps.app_a.server import app as app_a
from operations.replay_lookup import prompt_hash


def test_prompts_versioned_and_have_no_write_tools() -> None:
    assert WRITE_TOOLS == []
    for prompt_id in PROMPT_IDS:
        body = load_prompt(prompt_id, CURRENT_SEMVER)
        assert body["allowed_tools"] == []
        assert body["semver"] == "1.0.0"
        assert "check_claim" in body["system"] or "write" in body["system"]


def test_canonical_hash_includes_prompt_id_and_semver() -> None:
    assert KEY_ORDER[:2] == ("prompt_id", "semver")
    one = canonical_prompt_bytes(
        prompt_id="P-NL-QUERY",
        semver="1.0.0",
        system="sys",
        retrieved_item_ids=["b", "a"],
        question="q",
        case_id="",
    )
    two = canonical_prompt_bytes(
        prompt_id="P-NL-QUERY",
        semver="1.0.1",
        system="sys",
        retrieved_item_ids=["b", "a"],
        question="q",
        case_id="",
    )
    assert prompt_hash(one) != prompt_hash(two)
    assert b'"retrieved_item_ids": ["a", "b"]' in one


def test_empty_citations_on_answer_become_abstain() -> None:
    result = ground(
        {
            "sentence": "The 2023 EMEA recipe_release limit is 18600 USD.",
            "citations": [],
            "verdict": "ANSWER",
            "block": False,
            "untrusted_quotes": [],
        },
        retrieved_item_ids=["rule.recipe_release.limit.v2023.emea"],
    )
    assert result["verdict"] == "ABSTAIN"
    assert result["sentence"] == ""
    assert result["reject_reason"] == "missing_citation"


def test_uq03_moon_2099_abstains(api_headers) -> None:
    response = TestClient(app_a).post(
        "/api/query",
        headers=api_headers,
        json={"question": "What is the recipe_release limit for sales region MOON on 2099-01-01"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "ABSTAIN"
    assert body["citations"] == []
    assert "18600" not in (body.get("sentence") or "")
    assert "25000" not in (body.get("sentence") or "")
    assert "999999" not in (body.get("sentence") or "")


def test_replay_miss_abstains_without_network(monkeypatch, api_headers) -> None:
    def forbid(*_args, **_kwargs):
        raise AssertionError("replay must not open a network socket")

    monkeypatch.setattr(socket, "create_connection", forbid)
    monkeypatch.setattr(socket, "socket", forbid)
    result = generate("Which port does the Context Lake REST listener use?", prompt_id="P-NL-QUERY")
    # This question has a replay file after fixtures are written. Use a unique unused question.
    result = generate("zz-no-replay-hash-question-about-port-8091-unique", prompt_id="P-NL-QUERY")
    assert result["verdict"] == "ABSTAIN"
    assert result["error_class"] in {"replay_miss", None}
    if result["retrieved_item_ids"]:
        assert result["error_class"] == "replay_miss"
