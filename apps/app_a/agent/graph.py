"""Compile graph app_a_investigate with SqliteSaver and recursion_limit 12."""
from __future__ import annotations

import os
from typing import Any

from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from apps.app_a.agent.budget import RECURSION_LIMIT
from apps.app_a.agent.checkpointer import get_saver
from apps.app_a.agent.nodes import (
    after_gather,
    after_load,
    after_route,
    apply_human_decision,
    assemble_evidence,
    gather_tools,
    ground_and_cite,
    interrupt_wait,
    load_case,
    opa_gate,
    plan_draft,
    route_verdict,
    write_audit,
)
from apps.app_a.agent.state import AgentState
from apps.app_a.audit.writer import append_from_state

GRAPH_NAME = "app_a_investigate"

os.environ.setdefault("MODEL_MODE", "replay")


def build_graph(checkpointer: Any = None):
    builder = StateGraph(AgentState)
    builder.add_node("load_case", load_case)
    builder.add_node("plan_draft", plan_draft)
    builder.add_node("gather_tools", gather_tools)
    builder.add_node("assemble_evidence", assemble_evidence)
    builder.add_node("ground_and_cite", ground_and_cite)
    builder.add_node("opa_gate", opa_gate)
    builder.add_node("route_verdict", route_verdict)
    builder.add_node("interrupt_wait", interrupt_wait)
    builder.add_node("apply_human_decision", apply_human_decision)
    builder.add_node("write_audit", write_audit)
    builder.add_edge(START, "load_case")
    builder.add_conditional_edges("load_case", after_load, {"plan_draft": "plan_draft", "write_audit": "write_audit"})
    builder.add_edge("plan_draft", "gather_tools")
    builder.add_conditional_edges(
        "gather_tools",
        after_gather,
        {"gather_tools": "gather_tools", "assemble_evidence": "assemble_evidence"},
    )
    builder.add_edge("assemble_evidence", "ground_and_cite")
    builder.add_edge("ground_and_cite", "opa_gate")
    builder.add_edge("opa_gate", "route_verdict")
    builder.add_conditional_edges(
        "route_verdict",
        after_route,
        {"write_audit": "write_audit", "interrupt_wait": "interrupt_wait"},
    )
    builder.add_edge("interrupt_wait", "apply_human_decision")
    builder.add_edge("apply_human_decision", "write_audit")
    builder.add_edge("write_audit", END)
    saver = checkpointer if checkpointer is not None else get_saver()
    return builder.compile(checkpointer=saver, name=GRAPH_NAME)


_GRAPH = None


def get_graph(checkpointer: Any = None):
    global _GRAPH
    if checkpointer is not None:
        return build_graph(checkpointer)
    if _GRAPH is None:
        _GRAPH = build_graph()
    return _GRAPH


def reset_graph() -> None:
    global _GRAPH
    _GRAPH = None


def invoke_config(correlation_id: str) -> dict[str, Any]:
    return {
        "recursion_limit": RECURSION_LIMIT,
        "configurable": {"thread_id": correlation_id},
    }


def run_agent(payload: dict[str, Any], *, checkpointer: Any = None) -> dict[str, Any]:
    graph = get_graph(checkpointer)
    correlation_id = str(payload.get("correlation_id") or "")
    config = invoke_config(correlation_id)
    try:
        result = graph.invoke(payload, config)
        return {"ok": True, "state": result, "waiting": is_waiting(graph, correlation_id)}
    except GraphRecursionError:
        hold = {
            **payload,
            "opa_verdict": "HOLD_FOR_REVIEW",
            "budget_exhausted": True,
            "error_class": "wait_for_person",
        }
        append_from_state(hold, row_kind="control", event_type="EV-07", step_name="recursion_limit", notes="GraphRecursionError")
        return {"ok": False, "state": hold, "waiting": False, "error_class": "wait_for_person"}


def resume_agent(correlation_id: str, resume_payload: dict[str, Any], *, checkpointer: Any = None) -> dict[str, Any]:
    graph = get_graph(checkpointer)
    config = invoke_config(correlation_id)
    result = graph.invoke(Command(resume=resume_payload), config)
    return {"ok": True, "state": result, "waiting": is_waiting(graph, correlation_id)}


def is_waiting(graph: Any, correlation_id: str) -> bool:
    snapshot = graph.get_state(invoke_config(correlation_id))
    if snapshot is None:
        return False
    if getattr(snapshot, "interrupts", None):
        return True
    nxt = tuple(getattr(snapshot, "next", ()) or ())
    return "interrupt_wait" in nxt


def snapshot_for(correlation_id: str, *, checkpointer: Any = None) -> Any:
    graph = get_graph(checkpointer)
    return graph.get_state(invoke_config(correlation_id))
