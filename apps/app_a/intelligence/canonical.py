"""Canonical prompt bytes for replay hashing. ED-P9A-02."""
from __future__ import annotations

import json
from typing import Iterable

SEPARATORS = (", ", ": ")
KEY_ORDER = (
    "prompt_id",
    "semver",
    "system",
    "retrieved_item_ids",
    "question",
    "case_id",
)


def canonical_prompt_bytes(
    *,
    prompt_id: str,
    semver: str,
    system: str,
    retrieved_item_ids: Iterable[str],
    question: str,
    case_id: str | None,
) -> bytes:
    payload = {
        "prompt_id": prompt_id,
        "semver": semver,
        "system": system,
        "retrieved_item_ids": sorted(retrieved_item_ids),
        "question": question,
        "case_id": case_id or "",
    }
    ordered = {key: payload[key] for key in KEY_ORDER}
    return json.dumps(ordered, ensure_ascii=False, separators=SEPARATORS).encode("utf-8")
