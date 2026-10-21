"""Named graph nodes. The model runs only in plan_draft. Writes run only after a person resume."""
from __future__ import annotations

import os
from typing import Any

from langgraph.types import interrupt

from apps.app_a.agent.budget import (
    MAX_TOOL_INVOCATIONS,
    increment_gather,
    increment_step,
    increment_tool,
    may_gather_again,
)
from apps.app_a.agent.opa_client import build_opa_input, evaluate
from apps.app_a.agent.tools import call_tool
from apps.app_a.audit.writer import append_from_state
from apps.app_a.eval.sentences import INJECTION_LOCATORS, INJECTION_QUESTIONS
from apps.app_a.intelligence.generate import generate
from apps.app_a.intelligence.ground import empty_abstain, ground
from apps.app_a.store import SCENARIO_BINDINGS, get_case, mark_blocked, record_approval, set_draft
from apps.shared.demo_session import recipe_disagreement_sentence, recipe_explain_question, recipe_sentence_complete
from apps.shared.identity import check_write_action

os.environ.setdefault("MODEL_MODE", "replay")

SCENARIO_DEFAULTS = {
    "SP-07": {
        "case_id": "REPLAY-000000000",
        "proposed_action": "replay_drop",
        "record_change": True,
        "waiting_role": "RT-05",
        "load_event": "EV-02",
        "tools": [("get_case", {"case_id": "REPLAY-000000000"}), ("get_item", {"id": "rule.feed.replay_duplicate"})],
    },
    "SP-08": {
        "case_id": "PS000000016",
        "proposed_action": "recipe_hold_or_release",
        "record_change": True,
        "waiting_role": "RT-03",
        "load_event": "EV-04",
        "tools": [("get_case", {"case_id": "PS000000016"}), ("get_item", {"id": "rule.recipe.mismatch_show_both"})],
    },
    "SP-09": {
        "case_id": "E-00000000",
        "proposed_action": "explain",
        "record_change": False,
        "waiting_role": "",
        "load_event": "EV-05",
        "tools": [("get_case", {"case_id": "E-00000000"}), ("get_item", {"id": "rule.clock.event_vs_arrival"})],
    },
    "SP-10": {
        "case_id": "FAB-00000002",
        "proposed_action": "policy_pick",
        "record_change": True,
        "waiting_role": "RT-04",
        "load_event": "EV-06",
        "tools": [("get_case", {"case_id": "FAB-00000002"}), ("get_item", {"id": "rule.policy.overlap_or_invalid"})],
    },
    "SP-11": {
        "case_id": "INC-2025-014",
        "proposed_action": "assign_owner",
        "record_change": True,
        "waiting_role": "RT-06",
        "load_event": "EV-11",
        "tools": [
            ("get_case", {"case_id": "INC-2025-014"}),
            ("get_recovery_status", {}),
            ("get_item", {"id": "decision.inc_2025_014"}),
        ],
    },
}

RECIPE_CITES = ("rule.recipe.mismatch_show_both", "data.join.recipe_mismatch")

ACTION_FOR_CORPUS = {
    "IC-01": "approve",
    "IC-02": "approve",
    "IC-02-tiny": "approve",
    "IC-03": "approve",
    "IC-04": "release",
    "IC-05": "approve",
    "IC-06": "release",
}

WRITE_FROM_TEXT = {"approve", "release", "ignore-validation", "close-from-text"}


def _scenario_for_case(case_id: str, scenario_hint: str | None) -> str:
    if scenario_hint in SCENARIO_DEFAULTS or scenario_hint in ACTION_FOR_CORPUS:
        return str(scenario_hint)
    binding = SCENARIO_BINDINGS.get(case_id) or {}
    return str(binding.get("scenario") or "")


def load_case(state: dict[str, Any]) -> dict[str, Any]:
    case_id = str(state.get("case_id") or "")
    scenario = _scenario_for_case(case_id, state.get("scenario"))
    case = get_case(case_id)
    if case is None and scenario not in ACTION_FOR_CORPUS:
        update = {
            "error_class": "not_found",
            "record_change": False,
            "citations": [],
            "untrusted_quotes": [],
            "lake_item_ids": [],
            "block": False,
        }
        append_from_state({**state, **update}, row_kind="control", event_type="EV-08", step_name="load_case")
        return update

    defaults = SCENARIO_DEFAULTS.get(scenario) or {}
    named_corpus = scenario in ACTION_FOR_CORPUS
    proposed_action = str(state.get("proposed_action") or defaults.get("proposed_action") or "explain")
    if named_corpus:
        proposed_action = ACTION_FOR_CORPUS[scenario]
    quotes = list((case or {}).get("untrusted_quotes") or [])
    quote_write = bool(quotes) and proposed_action in WRITE_FROM_TEXT
    injection = named_corpus or quote_write
    update = {
        "scenario": scenario,
        "thread_id": state.get("correlation_id") or state.get("thread_id") or "",
        "proposed_by": "model_draft",
        "proposed_action": proposed_action,
        "record_change": bool(defaults.get("record_change", injection or proposed_action in WRITE_FROM_TEXT)),
        "waiting_role": "" if injection else str(defaults.get("waiting_role") or (case or {}).get("waiting_role") or ""),
        "untrusted_quotes": quotes,
        "citations": [],
        "lake_item_ids": list((case or {}).get("citation_targets") or []),
        "block": injection,
        "verdict": "",
        "opa_verdict": "",
        "draft_plan": "",
        "sentence": "",
        "error_class": "",
        "step_count": int(state.get("step_count") or 0),
        "tool_call_count": int(state.get("tool_call_count") or 0),
        "gather_visits": int(state.get("gather_visits") or 0),
        "budget_exhausted": bool(state.get("budget_exhausted")),
    }
    if injection:
        update["record_change"] = True
        update["waiting_role"] = ""
    event_type = "EV-12" if injection else str(defaults.get("load_event") or "EV-08")
    if not injection:
        event_type = str(defaults.get("load_event") or "EV-08")
    append_from_state({**state, **update}, row_kind="control", event_type="EV-08", step_name="load_case")
    if defaults.get("load_event"):
        append_from_state({**state, **update}, row_kind="control", event_type=str(defaults["load_event"]), step_name="load_case")
    return update


def _recipe_explanation(sentence: str, citations: list[str], targets: list[str]) -> tuple[str, list[str]]:
    text = sentence or ""
    if not recipe_sentence_complete(text):
        text = recipe_disagreement_sentence()
    allowed = [item for item in citations if item in targets and item in RECIPE_CITES]
    for item in RECIPE_CITES:
        if item in targets and item not in allowed:
            allowed.append(item)
    return text, allowed


def plan_draft(state: dict[str, Any]) -> dict[str, Any]:
    scenario = str(state.get("scenario") or "")
    case_id = str(state.get("case_id") or "")
    case = get_case(case_id) or {}
    explain_case = scenario == "SP-08"
    if scenario in INJECTION_QUESTIONS:
        question = INJECTION_QUESTIONS[scenario]
        hints = [INJECTION_LOCATORS[scenario], "rule.untrusted_text.block"]
        prompt_id = "P-DRAFT-PLAN"
    elif explain_case:
        question = recipe_explain_question()
        hints = list(case.get("citation_targets") or state.get("lake_item_ids") or [])
        prompt_id = "P-EXPLAIN-CONFLICT"
    else:
        question = str(case.get("explain_question") or f"Draft a plan for {case_id}.")
        hints = list(case.get("citation_targets") or state.get("lake_item_ids") or [])
        prompt_id = "P-DRAFT-PLAN"
    result = generate(question, prompt_id=prompt_id, case_id=case_id, hint_item_ids=hints)
    draft = result.get("draft_plan") or ""
    sentence = result.get("sentence") or ""
    citations = list(result.get("citations") or [])
    block = bool(result.get("block") or state.get("block"))
    if explain_case:
        targets = list(case.get("citation_targets") or [])
        sentence, citations = _recipe_explanation(sentence, citations, targets)
        draft = ""
        result = {**result, "verdict": "ANSWER", "error_class": ""}
    elif result.get("verdict") == "ABSTAIN":
        draft = ""
    if case_id:
        set_draft(case_id, draft)
    counters = increment_step(state)
    update = {
        **counters,
        "draft_plan": draft,
        "sentence": sentence,
        "citations": citations,
        "block": block,
        "verdict": result.get("verdict") or "ABSTAIN",
        "proposed_by": "model_draft",
        "model_mode": result.get("model_mode") or "",
        "answer_source": result.get("answer_source") or "",
        "retrieved_item_ids": list(result.get("retrieved_item_ids") or []),
        "replay_save": result.get("replay_save") or "",
        "message": result.get("message") or "",
        "untrusted_quotes": list(result.get("untrusted_quotes") or state.get("untrusted_quotes") or []),
        "error_class": "" if explain_case else (result.get("error_class") or state.get("error_class") or ""),
    }
    append_from_state({**state, **update}, row_kind="agent_step", event_type="EV-08", step_name="plan_draft")
    return update


def _planned_tools(state: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    scenario = str(state.get("scenario") or "")
    if scenario in ACTION_FOR_CORPUS:
        locator = INJECTION_LOCATORS.get(scenario)
        case_id = str(state.get("case_id") or "")
        calls: list[tuple[str, dict[str, Any]]] = []
        if case_id:
            calls.append(("get_case", {"case_id": case_id}))
        if locator:
            calls.append(("get_item", {"id": locator}))
        return calls
    defaults = SCENARIO_DEFAULTS.get(scenario) or {}
    return list(defaults.get("tools") or [("get_case", {"case_id": state.get("case_id")})])


def gather_tools(state: dict[str, Any]) -> dict[str, Any]:
    counters = increment_gather(state)
    merged = {**state, **counters}
    citations = list(state.get("citations") or [])
    quotes = list(state.get("untrusted_quotes") or [])
    lake_ids = list(state.get("lake_item_ids") or [])
    tool_count = int(counters.get("tool_call_count") or state.get("tool_call_count") or 0)
    budget_exhausted = bool(counters.get("budget_exhausted"))
    planned = _planned_tools(state)
    if int(state.get("gather_visits") or 0) >= 1:
        planned = [("search_items", {"q": str(state.get("case_id") or scenario_query(state))})]
    for name, kwargs in planned:
        if tool_count >= MAX_TOOL_INVOCATIONS or budget_exhausted:
            budget_exhausted = True
            break
        result = call_tool(name, **kwargs)
        tool_bump = increment_tool({**merged, "tool_call_count": tool_count})
        tool_count = int(tool_bump["tool_call_count"])
        budget_exhausted = bool(tool_bump.get("budget_exhausted") or budget_exhausted)
        for item_id in result.get("citations") or []:
            if item_id not in citations:
                citations.append(item_id)
            if item_id not in lake_ids:
                lake_ids.append(item_id)
        for quote in result.get("untrusted_quotes") or []:
            if quote not in quotes:
                quotes.append(quote)
        if result.get("block"):
            merged["block"] = True
        append_from_state(
            {**merged, "citations": citations, "lake_item_ids": lake_ids, "untrusted_quotes": quotes},
            row_kind="agent_step",
            event_type="EV-08",
            step_name="gather_tools",
            tool_name=name,
        )
    update = {
        **counters,
        "tool_call_count": tool_count,
        "budget_exhausted": budget_exhausted,
        "citations": citations,
        "lake_item_ids": lake_ids,
        "untrusted_quotes": quotes,
        "block": bool(merged.get("block") or state.get("block")),
    }
    return update


def scenario_query(state: dict[str, Any]) -> str:
    return str(state.get("proposed_action") or state.get("scenario") or "case")


def assemble_evidence(state: dict[str, Any]) -> dict[str, Any]:
    lake_ids = list(state.get("lake_item_ids") or [])
    for item_id in state.get("citations") or []:
        if item_id not in lake_ids:
            lake_ids.append(item_id)
    counters = increment_step(state)
    update = {**counters, "lake_item_ids": lake_ids, "untrusted_quotes": list(state.get("untrusted_quotes") or [])}
    append_from_state({**state, **update}, row_kind="agent_step", event_type="EV-08", step_name="assemble_evidence")
    return update


def ground_and_cite(state: dict[str, Any]) -> dict[str, Any]:
    citations = list(state.get("citations") or [])
    retrieved = list(state.get("lake_item_ids") or citations)
    model_body = {
        "sentence": state.get("sentence") or "",
        "citations": citations,
        "verdict": state.get("verdict") or "ANSWER",
        "block": bool(state.get("block")),
        "untrusted_quotes": list(state.get("untrusted_quotes") or []),
        "draft_plan": state.get("draft_plan"),
    }
    if not citations and not state.get("block"):
        grounded = ground(empty_abstain(), retrieved_item_ids=retrieved, untrusted_quotes=list(state.get("untrusted_quotes") or []), block=False)
        grounded["draft_plan"] = None
    else:
        grounded = ground(
            model_body,
            retrieved_item_ids=retrieved,
            untrusted_quotes=list(state.get("untrusted_quotes") or []),
            block=bool(state.get("block")),
        )
    counters = increment_step(state)
    update = {
        **counters,
        "sentence": grounded.get("sentence") or "",
        "citations": list(grounded.get("citations") or citations),
        "verdict": grounded.get("verdict") or "ABSTAIN",
        "block": bool(grounded.get("block") or state.get("block")),
        "draft_plan": grounded.get("draft_plan") if grounded.get("verdict") != "ABSTAIN" else (state.get("draft_plan") if state.get("record_change") else ""),
        "untrusted_quotes": list(grounded.get("untrusted_quotes") or []),
    }
    if not citations and not state.get("block"):
        update["verdict"] = "ABSTAIN"
        update["draft_plan"] = "" if not state.get("record_change") else state.get("draft_plan") or ""
        update["sentence"] = ""
    if str(state.get("scenario") or "") == "SP-08" and not recipe_sentence_complete(str(update.get("sentence") or "")):
        update["sentence"] = recipe_disagreement_sentence()
        update["citations"] = [item for item in RECIPE_CITES]
        update["verdict"] = "ANSWER"
        update["draft_plan"] = ""
    append_from_state({**state, **update}, row_kind="agent_step", event_type="EV-08", step_name="ground_and_cite")
    return update


def opa_gate(state: dict[str, Any]) -> dict[str, Any]:
    payload = build_opa_input(state)
    result = evaluate(payload)
    verdict = result["verdict"]
    update = {"opa_verdict": verdict}
    append_from_state({**state, **update}, row_kind="control", event_type="EV-07", step_name="opa_gate")
    return update


def route_verdict(state: dict[str, Any]) -> dict[str, Any]:
    verdict = str(state.get("opa_verdict") or "")
    case_id = str(state.get("case_id") or "")
    update: dict[str, Any] = {}
    if verdict == "BLOCK":
        if case_id:
            mark_blocked(case_id)
        update["error_class"] = "blocked"
        append_from_state({**state, **update}, row_kind="control", event_type="EV-12", step_name="route_verdict")
        return update
    if verdict == "HOLD_FOR_REVIEW" or (verdict == "EXECUTE" and state.get("record_change")):
        append_from_state(state, row_kind="control", event_type="EV-08", step_name="interrupt_wait", notes="paused")
    return update


def interrupt_wait(state: dict[str, Any]) -> dict[str, Any]:
    payload = interrupt(
        {
            "case_id": state.get("case_id"),
            "proposed_action": state.get("proposed_action"),
            "waiting_role": state.get("waiting_role"),
            "draft_plan": state.get("draft_plan"),
            "citations": list(state.get("citations") or []),
            "correlation_id": state.get("correlation_id"),
        }
    )
    body = payload if isinstance(payload, dict) else {}
    update = {
        "human_decision": str(body.get("decision") or ""),
        "human_action_type": str(body.get("action_type") or ""),
        "human_actor_id": str(body.get("actor_id") or ""),
        "human_actor_role": str(body.get("actor_role") or ""),
        "proposed_by": str(body.get("proposed_by") or state.get("proposed_by") or "model_draft"),
        "resume_owner_id": body.get("owner_id"),
        "resume_policy_id": body.get("policy_id"),
        "resume_hold_value": body.get("hold_value") or body.get("decision"),
    }
    append_from_state({**state, **update}, row_kind="control", event_type="EV-08", step_name="interrupt_wait", notes="resumed")
    return update


def apply_human_decision(state: dict[str, Any]) -> dict[str, Any]:
    actor_id = str(state.get("human_actor_id") or "")
    actor_role = str(state.get("human_actor_role") or "")
    action_type = str(state.get("human_action_type") or "")
    proposed_by = str(state.get("proposed_by") or "model_draft")
    case_id = str(state.get("case_id") or "")
    correlation_id = str(state.get("correlation_id") or "")
    denied = check_write_action(
        role=actor_role,
        action_type=action_type,
        actor_id=actor_id,
        proposed_by=proposed_by,
        correlation_id=correlation_id,
    )
    if denied:
        update = {"error_class": "forbidden_role"}
        append_from_state({**state, **update}, row_kind="control", event_type="EV-08", step_name="apply_human_decision")
        return update
    recorded = {
        "case_id": case_id,
        "action_type": action_type,
        "decision": state.get("human_decision"),
        "actor_id": actor_id,
        "actor_role": actor_role,
        "proposed_by": proposed_by,
        "correlation_id": correlation_id,
        "owner_id": state.get("resume_owner_id"),
        "policy_id": state.get("resume_policy_id"),
        "hold_value": state.get("resume_hold_value") or state.get("human_decision"),
    }
    if case_id:
        record_approval(case_id, recorded)
    event_type = "EV-10" if action_type == "assign_owner" else "EV-09"
    append_from_state(
        state,
        row_kind="human_approval",
        event_type=event_type,
        step_name="apply_human_decision",
        action_type=action_type,
        decision=str(state.get("human_decision") or ""),
    )
    return {"error_class": ""}


def write_audit(state: dict[str, Any]) -> dict[str, Any]:
    append_from_state(state, row_kind="control", event_type="EV-08", step_name="write_audit")
    return {}


def after_load(state: dict[str, Any]) -> str:
    if state.get("error_class") == "not_found":
        return "write_audit"
    return "plan_draft"


def after_gather(state: dict[str, Any]) -> str:
    if may_gather_again(state):
        return "gather_tools"
    return "assemble_evidence"


def after_route(state: dict[str, Any]) -> str:
    verdict = str(state.get("opa_verdict") or "")
    if verdict == "BLOCK":
        return "write_audit"
    if verdict == "EXECUTE" and not state.get("record_change"):
        return "write_audit"
    return "interrupt_wait"
