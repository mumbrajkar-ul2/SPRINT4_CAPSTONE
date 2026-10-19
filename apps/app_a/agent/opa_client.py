"""AD-OPA. Evaluate policy/opa/app_a.rego. Verdict is one string."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
POLICY_DIR = ROOT / "policy" / "opa"
VERDICTS = ("EXECUTE", "HOLD_FOR_REVIEW", "BLOCK")
CORPUS_IDS = {"IC-01", "IC-02", "IC-02-tiny", "IC-03", "IC-04", "IC-05", "IC-06"}
WRITE_FROM_TEXT = {"approve", "release", "ignore-validation", "close-from-text"}

_OPA_PATH: str | None | bool = False


def opa_binary_path() -> str | None:
    global _OPA_PATH
    if _OPA_PATH is False:
        found = shutil.which("opa")
        _OPA_PATH = found
    return _OPA_PATH if isinstance(_OPA_PATH, str) else None


def reset_opa_path_cache() -> None:
    global _OPA_PATH
    _OPA_PATH = False


def local_evaluate(payload: dict[str, Any]) -> str:
    """Same named rules as app_a.rego. Used when the opa binary is absent."""
    injection = bool(payload.get("injection"))
    block_flag = bool(payload.get("block_flag"))
    corpus_id = str(payload.get("corpus_id") or "")
    proposed_action = str(payload.get("proposed_action") or "")
    actor_id = str(payload.get("actor_id") or "")
    proposed_by = str(payload.get("proposed_by") or "")
    owner_invented = bool(payload.get("owner_invented"))
    record_change = bool(payload.get("record_change"))

    r01 = injection or block_flag or (corpus_id in CORPUS_IDS and proposed_action in WRITE_FROM_TEXT)
    r07 = bool(actor_id) and actor_id == proposed_by
    r09 = owner_invented
    if r01 or r07 or r09:
        return "BLOCK"

    r02 = payload.get("archive_match") == "none"
    r03 = bool(payload.get("silent_threshold"))
    r04 = payload.get("archive_match") == "overlap"
    r05 = bool(payload.get("region_disagreement"))
    r10 = bool(payload.get("budget_exhausted"))
    r12 = bool(payload.get("citations_empty")) and record_change and not injection
    r06 = record_change
    if r02 or r03 or r04 or r05 or r10 or r12 or r06:
        return "HOLD_FOR_REVIEW"

    r11 = (not record_change) and (not injection) and (not block_flag) and (not bool(payload.get("budget_exhausted")))
    if r11:
        return "EXECUTE"
    if record_change:
        return "HOLD_FOR_REVIEW"
    return "EXECUTE"


def _eval_with_binary(payload: dict[str, Any], binary: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(payload, handle)
        handle.flush()
        input_path = handle.name
    try:
        completed = subprocess.run(
            [
                binary,
                "eval",
                "-d",
                str(POLICY_DIR),
                "-i",
                input_path,
                "--format",
                "json",
                "data.app_a.verdict",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    finally:
        Path(input_path).unlink(missing_ok=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or "opa eval failed")
    body = json.loads(completed.stdout)
    results = body.get("result") or []
    if not results:
        raise RuntimeError("opa eval returned no result")
    expressions = results[0].get("expressions") or []
    if not expressions:
        raise RuntimeError("opa eval returned no expression")
    value = expressions[0].get("value")
    if value not in VERDICTS:
        raise RuntimeError(f"opa eval returned {value!r}")
    return str(value)


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    """Return verdict plus which engine ran. Code calls this. The model does not."""
    binary = opa_binary_path()
    if binary:
        try:
            verdict = _eval_with_binary(payload, binary)
            return {
                "verdict": verdict,
                "engine": "opa_binary",
                "opa_binary_present": True,
                "opa_binary_path": binary,
            }
        except (RuntimeError, json.JSONDecodeError, OSError, subprocess.TimeoutExpired):
            local = local_evaluate(payload)
            return {
                "verdict": local,
                "engine": "local_evaluator",
                "opa_binary_present": True,
                "opa_binary_path": binary,
                "opa_binary_error": True,
            }
    local = local_evaluate(payload)
    return {
        "verdict": local,
        "engine": "local_evaluator",
        "opa_binary_present": False,
        "opa_binary_absent_recorded": True,
    }


def build_opa_input(state: dict[str, Any]) -> dict[str, Any]:
    scenario = str(state.get("scenario") or "")
    corpus_id = scenario if scenario in CORPUS_IDS else ""
    proposed_action = str(state.get("proposed_action") or "")
    quote_write = bool(state.get("untrusted_quotes")) and proposed_action in WRITE_FROM_TEXT
    injection = bool(corpus_id and proposed_action in WRITE_FROM_TEXT) or bool(state.get("block")) or quote_write
    archive_match = "one"
    if scenario == "SP-10":
        archive_match = "overlap"
    citations = list(state.get("citations") or [])
    return {
        "proposed_action": proposed_action,
        "record_change": bool(state.get("record_change")),
        "injection": injection,
        "corpus_id": corpus_id,
        "block_flag": bool(state.get("block")) or quote_write,
        "archive_match": archive_match,
        "region_disagreement": False,
        "silent_threshold": False,
        "finance_audit_mismatch": False,
        "actor_id": str(state.get("human_actor_id") or ""),
        "proposed_by": str(state.get("proposed_by") or "model_draft"),
        "actor_role": str(state.get("actor_role") or ""),
        "action_type": str(state.get("human_action_type") or ""),
        "owner_invented": False,
        "budget_exhausted": bool(state.get("budget_exhausted")),
        "citations_empty": len(citations) == 0,
        "untrusted_quote_present": bool(state.get("untrusted_quotes")),
    }
