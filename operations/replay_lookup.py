"""Look up a saved model response by the SHA-256 hash of the prompt."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

REPLAY_DIR = Path(__file__).resolve().parent / "model-replay"


def prompt_hash(prompt: str | bytes) -> str:
    data = prompt if isinstance(prompt, bytes) else prompt.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def lookup(
    prompt: str | bytes,
    *,
    directory: Path | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    """Return the saved file body in replay. Do not open a public-network socket."""
    chosen_mode = mode if mode is not None else os.environ.get("MODEL_MODE", "replay")
    store = directory or REPLAY_DIR
    digest = prompt_hash(prompt)
    if chosen_mode != "replay":
        return {
            "ok": False,
            "error_class": "replay_required",
            "event": "replay_miss",
            "message": "This platform run uses replay files only. A live model call stays later.",
            "prompt_hash": digest,
        }
    path = store / digest
    if not path.is_file():
        return {
            "ok": False,
            "error_class": "replay_miss",
            "event": "replay_miss",
            "message": "No saved file exists for this prompt hash. Replay does not call a public model.",
            "prompt_hash": digest,
        }
    return {
        "ok": True,
        "error_class": None,
        "event": "replay_hit",
        "message": None,
        "prompt_hash": digest,
        "body": path.read_text(encoding="utf-8"),
    }
