"""Package app_b. Three verdicts. Each rule cites the lake item it applies."""
from __future__ import annotations

from typing import Any

VERDICTS = ("EXECUTE", "HOLD_FOR_REVIEW", "BLOCK")
CORPUS_IDS = {"IC-01", "IC-02", "IC-02-tiny", "IC-03", "IC-04", "IC-05", "IC-06"}
WRITE_FROM_TEXT = {"approve", "release", "ignore-validation", "close-from-text"}

# Lake item each named check applies.
LAKE_ITEMS = {
    "injection": "rule.untrusted_text.block",
    "proposer": "rule.hold.person_only",
    "owner": "decision.inc_2025_014",
    "silence": "rule.recipe_release.no_match",
    "silent_threshold": "rule.threshold.silent",
    "overlap": "rule.policy.overlap_or_invalid",
    "region": "rule.region.disagreement",
    "person": "rule.hold.person_only",
    "never_999999": "rule.threshold.never_999999",
}


def local_evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    """Same three verdicts as policy/opa/app_b.rego. Used when opa is absent."""
    citations: list[str] = []
    injection = bool(payload.get("injection"))
    block_flag = bool(payload.get("block_flag"))
    corpus_id = str(payload.get("corpus_id") or "")
    proposed_action = str(payload.get("proposed_action") or "")
    actor_id = str(payload.get("actor_id") or "")
    proposed_by = str(payload.get("proposed_by") or "")
    owner_invented = bool(payload.get("owner_invented"))
    record_change = bool(payload.get("record_change"))

    r_injection = injection or block_flag or (
        corpus_id in CORPUS_IDS and proposed_action in WRITE_FROM_TEXT
    )
    r_proposer = bool(actor_id) and actor_id == proposed_by
    r_owner = owner_invented
    if r_injection or r_proposer or r_owner:
        if r_injection:
            citations.append(LAKE_ITEMS["injection"])
        if r_proposer:
            citations.append(LAKE_ITEMS["proposer"])
        if r_owner:
            citations.append(LAKE_ITEMS["owner"])
        return {"verdict": "BLOCK", "citations": citations, "engine": "local_evaluator"}

    r_silence = payload.get("archive_match") == "none"
    r_silent = bool(payload.get("silent_threshold"))
    r_overlap = payload.get("archive_match") == "overlap"
    r_region = bool(payload.get("region_disagreement"))
    r_budget = bool(payload.get("budget_exhausted"))
    r_empty = bool(payload.get("citations_empty")) and record_change and not injection
    r_person = record_change
    if r_silence or r_silent or r_overlap or r_region or r_budget or r_empty or r_person:
        if r_silence:
            citations.append(LAKE_ITEMS["silence"])
        if r_silent:
            citations.append(LAKE_ITEMS["silent_threshold"])
        if r_overlap:
            citations.append(LAKE_ITEMS["overlap"])
        if r_region:
            citations.append(LAKE_ITEMS["region"])
        if r_person or r_empty:
            citations.append(LAKE_ITEMS["person"])
        return {
            "verdict": "HOLD_FOR_REVIEW",
            "citations": citations,
            "engine": "local_evaluator",
        }
    return {"verdict": "EXECUTE", "citations": citations, "engine": "local_evaluator"}


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    result = local_evaluate(payload)
    verdict = result["verdict"]
    if verdict not in VERDICTS:
        result["verdict"] = "HOLD_FOR_REVIEW"
    return result


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
        "actor_id": str(state.get("human_actor_id") or ""),
        "proposed_by": str(state.get("proposed_by") or "model_draft"),
        "owner_invented": False,
        "budget_exhausted": bool(state.get("budget_exhausted")),
        "citations_empty": len(citations) == 0,
        "untrusted_quote_present": bool(state.get("untrusted_quotes")),
    }
