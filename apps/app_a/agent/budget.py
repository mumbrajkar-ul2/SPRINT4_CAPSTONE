"""FD-15 numeric bounds. Engineering defaults. Not quality floors."""
from __future__ import annotations

from typing import Any

RECURSION_LIMIT = 12
STEP_BUDGET = 8
MAX_TOOL_INVOCATIONS = 8
MAX_GATHER_VISITS = 3


def increment_step(state: dict[str, Any]) -> dict[str, Any]:
    step_count = int(state.get("step_count") or 0) + 1
    exhausted = step_count >= STEP_BUDGET or bool(state.get("budget_exhausted"))
    if int(state.get("tool_call_count") or 0) >= MAX_TOOL_INVOCATIONS:
        exhausted = True
    return {"step_count": step_count, "budget_exhausted": exhausted}


def increment_tool(state: dict[str, Any]) -> dict[str, Any]:
    tool_call_count = int(state.get("tool_call_count") or 0) + 1
    exhausted = tool_call_count >= MAX_TOOL_INVOCATIONS or bool(state.get("budget_exhausted"))
    if int(state.get("step_count") or 0) >= STEP_BUDGET:
        exhausted = True
    return {"tool_call_count": tool_call_count, "budget_exhausted": exhausted}


def increment_gather(state: dict[str, Any]) -> dict[str, Any]:
    gather_visits = int(state.get("gather_visits") or 0) + 1
    step_update = increment_step(state)
    exhausted = gather_visits >= MAX_GATHER_VISITS or bool(step_update.get("budget_exhausted"))
    return {
        "gather_visits": gather_visits,
        "step_count": step_update["step_count"],
        "budget_exhausted": exhausted,
    }


def may_gather_again(state: dict[str, Any]) -> bool:
    citations = list(state.get("citations") or [])
    if citations:
        return False
    if state.get("block"):
        return False
    if state.get("budget_exhausted"):
        return False
    if int(state.get("gather_visits") or 0) >= MAX_GATHER_VISITS:
        return False
    if int(state.get("tool_call_count") or 0) >= MAX_TOOL_INVOCATIONS:
        return False
    if int(state.get("step_count") or 0) >= STEP_BUDGET:
        return False
    return True
