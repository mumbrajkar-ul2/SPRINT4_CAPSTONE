"""Typed state fields for graph app_a_investigate. Names from Half A."""
from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict, total=False):
    correlation_id: str
    thread_id: str
    case_id: str
    actor_id: str
    actor_role: str
    proposed_by: str
    proposed_action: str
    record_change: bool
    draft_plan: str
    sentence: str
    citations: list[str]
    model_mode: str
    answer_source: str
    retrieved_item_ids: list[str]
    replay_save: str
    message: str
    untrusted_quotes: list[str]
    lake_item_ids: list[str]
    verdict: str
    block: bool
    opa_verdict: str
    waiting_role: str
    step_count: int
    tool_call_count: int
    gather_visits: int
    budget_exhausted: bool
    human_decision: str
    human_action_type: str
    human_actor_id: str
    human_actor_role: str
    error_class: str
    scenario: str
