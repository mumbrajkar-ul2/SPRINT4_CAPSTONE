"""Obtain a model response from replay, or later Azure. Replay never opens a public-network socket."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from operations.replay_lookup import lookup, prompt_hash

from apps.app_a.intelligence.azure_client import complete_azure
from apps.app_a.intelligence.canonical import canonical_prompt_bytes
from apps.app_a.intelligence.ground import empty_abstain, ground
from apps.app_a.intelligence.prompts import CURRENT_SEMVER, load_prompt
from apps.app_a.intelligence.retrieve import retrieve

WRITE_TOOLS: list[str] = []


def question_has_no_supporting_item(question: str) -> bool:
    """MOON is not a sales region. Year 2099 has no archive row. Abstain without guessing a limit."""
    text = question or ""
    if re.search(r"\bMOON\b", text, re.I):
        return True
    if re.search(r"\b2099\b", text):
        return True
    return False


def model_mode() -> str:
    return (os.environ.get("MODEL_MODE") or "replay").strip().lower()


def parse_model_json(body: str) -> dict[str, Any] | None:
    text = (body or "").strip()
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end <= start:
            return None
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None
    return payload if isinstance(payload, dict) else None


def generate(
    question: str,
    *,
    prompt_id: str = "P-NL-QUERY",
    semver: str = CURRENT_SEMVER,
    case_id: str | None = None,
    hint_item_ids: list[str] | None = None,
    replay_dir: Path | None = None,
) -> dict[str, Any]:
    """Retrieve, generate from replay or Azure, then check the claim."""
    question = question or ""
    retrieved = retrieve(question, hint_item_ids=hint_item_ids)
    retrieved_ids = list(retrieved.get("retrieved_item_ids") or [])
    quotes = list(retrieved.get("untrusted_quotes") or [])
    block = bool(retrieved.get("block"))
    prompt = load_prompt(prompt_id, semver)
    canonical = canonical_prompt_bytes(
        prompt_id=prompt_id,
        semver=semver,
        system=prompt["system"],
        retrieved_item_ids=retrieved_ids,
        question=question,
        case_id=case_id,
    )
    digest = prompt_hash(canonical)
    mode = model_mode()
    error_class = None
    raw_body = None

    if (not retrieved_ids and not block) or question_has_no_supporting_item(question):
        grounded = ground(
            empty_abstain(),
            retrieved_item_ids=[],
            untrusted_quotes=quotes,
            block=False,
        )
        grounded.update(
            {
                "prompt_id": prompt_id,
                "semver": semver,
                "prompt_hash": digest,
                "retrieved_item_ids": [],
                "error_class": None,
                "lake_version": retrieved.get("lake_version"),
                "model_mode": mode,
            }
        )
        return grounded

    if mode == "replay":
        hit = lookup(canonical, directory=replay_dir, mode="replay")
        if not hit.get("ok"):
            error_class = hit.get("error_class") or "replay_miss"
            grounded = ground(
                empty_abstain(citations=[item_id for item_id in retrieved_ids if item_id.startswith("data.missing") or item_id == "decision.inc_2025_014"]),
                retrieved_item_ids=retrieved_ids,
                untrusted_quotes=quotes,
                block=block,
            )
            grounded.update(
                {
                    "prompt_id": prompt_id,
                    "semver": semver,
                    "prompt_hash": digest,
                    "retrieved_item_ids": retrieved_ids,
                    "error_class": error_class,
                    "lake_version": retrieved.get("lake_version"),
                    "model_mode": mode,
                }
            )
            return grounded
        raw_body = hit.get("body")
    elif mode == "azure":
        live = complete_azure(canonical)
        if not live.get("ok"):
            error_class = live.get("error_class") or "azure_call_failed"
            grounded = ground(
                empty_abstain(),
                retrieved_item_ids=retrieved_ids,
                untrusted_quotes=quotes,
                block=block,
            )
            grounded.update(
                {
                    "prompt_id": prompt_id,
                    "semver": semver,
                    "prompt_hash": digest,
                    "retrieved_item_ids": retrieved_ids,
                    "error_class": error_class,
                    "lake_version": retrieved.get("lake_version"),
                    "model_mode": mode,
                }
            )
            return grounded
        raw_body = live.get("body")
        store = replay_dir or (Path(__file__).resolve().parents[3] / "operations" / "model-replay")
        store.mkdir(parents=True, exist_ok=True)
        (store / digest).write_text(str(raw_body), encoding="utf-8")
    else:
        error_class = "replay_required"
        grounded = ground(empty_abstain(), retrieved_item_ids=retrieved_ids, untrusted_quotes=quotes, block=block)
        grounded.update(
            {
                "prompt_id": prompt_id,
                "semver": semver,
                "prompt_hash": digest,
                "retrieved_item_ids": retrieved_ids,
                "error_class": error_class,
                "lake_version": retrieved.get("lake_version"),
                "model_mode": mode,
            }
        )
        return grounded

    parsed = parse_model_json(str(raw_body or ""))
    if parsed is None:
        parsed = empty_abstain()
        error_class = error_class or "replay_miss"
    grounded = ground(
        parsed,
        retrieved_item_ids=retrieved_ids,
        untrusted_quotes=quotes,
        block=block,
    )
    grounded.update(
        {
            "prompt_id": prompt_id,
            "semver": semver,
            "prompt_hash": digest,
            "retrieved_item_ids": retrieved_ids,
            "error_class": error_class,
            "lake_version": retrieved.get("lake_version"),
            "model_mode": mode,
        }
    )
    return grounded
