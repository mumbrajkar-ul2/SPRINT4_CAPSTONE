"""Azure OpenAI live path. Tests never call this with a key. Replay never imports a socket here."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

REQUIRED_VARS = (
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_DEPLOYMENT",
    "AZURE_OPENAI_API_VERSION",
)


def azure_config() -> dict[str, str] | None:
    values = {name: (os.environ.get(name) or "").strip() for name in REQUIRED_VARS}
    if any(not values[name] for name in REQUIRED_VARS):
        return None
    return values


def complete_azure(prompt_bytes: bytes, *, timeout_s: float = 30.0) -> dict[str, Any]:
    """Send the canonical prompt to Azure OpenAI. Caller must set MODEL_MODE=azure."""
    cfg = azure_config()
    if cfg is None:
        return {
            "ok": False,
            "error_class": "missing_model_config",
            "message": "Azure variables are missing. A person supplies them. Replay stays the laptop path.",
            "body": None,
        }
    endpoint = cfg["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    url = (
        f"{endpoint}/openai/deployments/{cfg['AZURE_OPENAI_DEPLOYMENT']}"
        f"/chat/completions?api-version={cfg['AZURE_OPENAI_API_VERSION']}"
    )
    payload = {
        "temperature": 0,
        "max_tokens": 800,
        "messages": [
            {"role": "user", "content": prompt_bytes.decode("utf-8")},
        ],
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "api-key": cfg["AZURE_OPENAI_API_KEY"],
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "error_class": "azure_call_failed",
            "message": f"Azure call failed: {type(exc).__name__}",
            "body": None,
        }
    try:
        text = raw["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return {
            "ok": False,
            "error_class": "azure_call_failed",
            "message": "Azure response had no message content.",
            "body": None,
        }
    return {"ok": True, "error_class": None, "message": None, "body": text}
