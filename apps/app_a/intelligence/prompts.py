"""Load versioned prompt JSON from apps/app_a/prompts/."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"
PROMPT_IDS = ("P-EXPLAIN-CONFLICT", "P-NL-QUERY", "P-DRAFT-PLAN")
CURRENT_SEMVER = "1.0.0"


def prompt_path(prompt_id: str, semver: str = CURRENT_SEMVER) -> Path:
    return PROMPT_DIR / f"{prompt_id}.v{semver}.json"


def load_prompt(prompt_id: str, semver: str = CURRENT_SEMVER) -> dict[str, Any]:
    path = prompt_path(prompt_id, semver)
    body = json.loads(path.read_text(encoding="utf-8"))
    if body.get("prompt_id") != prompt_id or body.get("semver") != semver:
        raise ValueError(f"Prompt file {path.name} does not match {prompt_id} {semver}.")
    if body.get("allowed_tools"):
        raise ValueError(f"Prompt {prompt_id} must not register tools in Phase 9.")
    return body
