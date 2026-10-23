"""Token budget and recipe-value masking for a live model call.

Replay, an abstain, and a missing user do not spend the budget.
The mask hides set-points. It leaves recipe ids and the two ISO times in place.
"""
from __future__ import annotations

import contextvars
import os
import re
from datetime import date
from pathlib import Path

_ACTOR: contextvars.ContextVar[str] = contextvars.ContextVar("ff_actor", default="")
_SPEND: dict[tuple[str, str], int] = {}

_PARAM = re.compile(r"(?i)\b(temperature|pressure|power|flow|time)\s*=\s*[^,;\s]+")
_UNIT = re.compile(r"(?i)\b\d+(?:\.\d+)?\s*(?:mTorr|sccm|°C)\b")


def set_actor(actor_id: str) -> None:
    _ACTOR.set(actor_id or "")


def current_actor() -> str:
    return _ACTOR.get()


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def budget_allows(text: str) -> bool:
    actor = current_actor()
    if not actor:
        return True
    limit = int(os.environ.get("FF_LLM_DAILY_TOKENS") or "50000")
    if limit <= 0:
        return False
    key = (actor, date.today().isoformat())
    return _SPEND.get(key, 0) + estimate_tokens(text) <= limit


def charge(text: str) -> None:
    actor = current_actor()
    if not actor:
        return
    key = (actor, date.today().isoformat())
    _SPEND[key] = _SPEND.get(key, 0) + estimate_tokens(text)


def reset_budget() -> None:
    _SPEND.clear()


def mask_recipe_text(text: str) -> str:
    masked = _UNIT.sub("[set-point]", text or "")
    return _PARAM.sub(lambda match: f"{match.group(1)}=[set-point]", masked)


def save_replay(path: Path, body: str) -> str:
    if path.is_file():
        return "kept_frozen"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return "saved"
