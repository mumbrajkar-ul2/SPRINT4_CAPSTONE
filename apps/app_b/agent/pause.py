"""LangGraph interrupt pause for Application B. The checkpoint file survives a restart."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from apps.app_b.rules.resolver import fetch_item

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CHECKPOINT_PATH = ROOT / "apps" / "app_b" / "runtime" / "checkpoints.sqlite3"
PROPOSED_BY = "model_draft"
LAKE_TOOL_ITEM = "rule.hold.person_only"


class PauseState(TypedDict, total=False):
    correlation_id: str
    case_id: str
    proposed_by: str
    verdict: str
    human_actor_id: str
    tool_item_id: str

_SAVER: SqliteSaver | None = None
_CONN: sqlite3.Connection | None = None
_GRAPH: Any = None
_PATH: Path | None = None


def checkpoint_path() -> Path:
    env = (os.environ.get("APP_B_CHECKPOINT_PATH") or "").strip()
    return Path(env) if env else DEFAULT_CHECKPOINT_PATH


def close_pause() -> None:
    """Drop the in-memory graph. The checkpoint file stays on disk."""
    global _SAVER, _CONN, _GRAPH, _PATH
    _GRAPH = None
    _SAVER = None
    if _CONN is not None:
        try:
            _CONN.close()
        except sqlite3.Error:
            pass
    _CONN = None
    _PATH = None


def get_graph() -> Any:
    global _SAVER, _CONN, _GRAPH, _PATH
    target = checkpoint_path()
    if _GRAPH is not None and _PATH == target:
        return _GRAPH
    close_pause()
    target.parent.mkdir(parents=True, exist_ok=True)
    _CONN = sqlite3.connect(str(target), check_same_thread=False)
    _SAVER = SqliteSaver(_CONN)
    _PATH = target

    def read_lake(state: PauseState) -> dict[str, Any]:
        fetch_item(LAKE_TOOL_ITEM)
        return {
            "tool_item_id": LAKE_TOOL_ITEM,
            "verdict": "HOLD_FOR_REVIEW",
            "case_id": state.get("case_id") or "",
            "correlation_id": state.get("correlation_id") or "",
            "proposed_by": state.get("proposed_by") or PROPOSED_BY,
        }

    def wait_for_person(state: PauseState) -> dict[str, Any]:
        decision = interrupt(
            {
                "proposed_by": state.get("proposed_by") or PROPOSED_BY,
                "verdict": "HOLD_FOR_REVIEW",
                "correlation_id": state.get("correlation_id"),
            }
        )
        actor = ""
        if isinstance(decision, dict):
            actor = str(decision.get("actor_id") or "")
        return {"human_actor_id": actor, "verdict": "HOLD_FOR_REVIEW"}

    builder = StateGraph(PauseState)
    builder.add_node("read_lake", read_lake)
    builder.add_node("wait_for_person", wait_for_person)
    builder.add_edge(START, "read_lake")
    builder.add_edge("read_lake", "wait_for_person")
    builder.add_edge("wait_for_person", END)
    _GRAPH = builder.compile(checkpointer=_SAVER)
    return _GRAPH


def _config(correlation_id: str) -> dict[str, Any]:
    return {"configurable": {"thread_id": correlation_id}}


def start_pause(correlation_id: str, case_id: str = "PS000000016") -> dict[str, Any]:
    graph = get_graph()
    graph.invoke(
        {
            "correlation_id": correlation_id,
            "case_id": case_id,
            "proposed_by": PROPOSED_BY,
            "verdict": "",
            "human_actor_id": "",
            "tool_item_id": "",
        },
        _config(correlation_id),
    )
    return pause_status(correlation_id)


def pause_status(correlation_id: str) -> dict[str, Any]:
    graph = get_graph()
    snapshot = graph.get_state(_config(correlation_id))
    interrupts = tuple(getattr(snapshot, "interrupts", ()) or ())
    nxt = tuple(getattr(snapshot, "next", ()) or ())
    values = dict(getattr(snapshot, "values", {}) or {})
    return {
        "ok": True,
        "correlation_id": correlation_id,
        "case_id": values.get("case_id"),
        "proposed_by": values.get("proposed_by") or PROPOSED_BY,
        "waiting": bool(interrupts) or "wait_for_person" in nxt,
        "verdict": "HOLD_FOR_REVIEW" if interrupts or nxt else values.get("verdict"),
        "checkpoint_path": str(checkpoint_path()),
        "tool_item_id": values.get("tool_item_id"),
    }


def resume_pause(correlation_id: str, actor_id: str) -> dict[str, Any]:
    status = pause_status(correlation_id)
    if actor_id == status.get("proposed_by"):
        status["ok"] = False
        status["message"] = "Resume requires a different person from proposed_by."
        return status
    graph = get_graph()
    graph.invoke(Command(resume={"actor_id": actor_id}), _config(correlation_id))
    return pause_status(correlation_id)
