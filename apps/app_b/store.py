"""Load the five scenario fixtures. Do not open the inherited sqlite files."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from apps.app_b.rules import resolver

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "scenarios.yaml"

_CASES: dict[str, dict[str, Any]] | None = None
_APPROVALS: dict[str, list[dict[str, Any]]] = {}
_MUTATIONS: dict[str, dict[str, Any]] = {}
_BLOCKED: set[str] = set()
_DRAFTS: dict[str, str] = {}


def _lake_untrusted_quotes(case_id: str) -> list[str]:
    """Copy lake locator statements onto the REPLAY case. Do not open inherited sqlite."""
    if case_id != "REPLAY-000000000":
        return []
    env = resolver.fetch_item("data.injection.partner_feeds")
    quotes: list[str] = []
    for item in env.get("items") or []:
        statement = item.get("statement")
        if item.get("trust") == "untrusted_text" and statement:
            quotes.append(str(statement))
    return quotes


def reset_runtime() -> None:
    global _CASES
    _APPROVALS.clear()
    _MUTATIONS.clear()
    _BLOCKED.clear()
    _DRAFTS.clear()
    _CASES = None
    from apps.app_b.audit.store import reset_audit_store

    reset_audit_store()
    resolver.verify_pin()


def _base_cases() -> dict[str, dict[str, Any]]:
    global _CASES
    if _CASES is not None:
        return _CASES
    resolver.verify_pin()
    payload = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
    cases: dict[str, dict[str, Any]] = {}
    for raw in payload.get("cases") or []:
        case_id = raw["case_id"]
        status = raw["status"]
        severity = raw.get("severity") or "MEDIUM"
        amount = float(raw.get("amount") or 0)
        waiting = raw.get("waiting_role")
        opened = resolver.open_operational(status)
        ranked = resolver.queue_rank(
            status=status,
            severity=severity,
            amount=amount,
            waiting_role=waiting,
        )
        flags = resolver.finance_audit_flags()
        body: dict[str, Any] = {
            "case_id": case_id,
            "status": status,
            "open_operational": opened["open_operational"],
            "severity": severity,
            "amount": amount,
            "waiting_role": waiting,
            "owner_id": raw.get("owner_id"),
            "finance_closed": flags["finance_closed"],
            "audit_closed": flags["audit_closed"],
            "duplicate_candidate": False,
            "rank": ranked["rank"],
            "scenario": raw.get("pack_id"),
            "citation_targets": list(raw.get("citation_targets") or []),
            "explain_question": raw.get("explain_question"),
            "untrusted_quotes": _lake_untrusted_quotes(case_id),
            "engineering_hold": raw.get("engineering_hold"),
            "lake_item_ids": list(raw.get("lake_items") or raw.get("citation_targets") or []),
        }
        if raw.get("processing_status"):
            replay = resolver.replay_duplicate(raw["processing_status"])
            body["processing_status"] = raw["processing_status"]
            body["duplicate_candidate"] = replay["duplicate_candidate"]
            body["citation_targets"] = list(
                dict.fromkeys(body["citation_targets"] + replay.get("citations", []))
            )
        if raw.get("recipe_version") is not None:
            pair = resolver.recipe_pair(raw["recipe_version"], raw["recipe_rev"])
            body["recipe_version"] = pair["recipe_version"]
            body["recipe_rev"] = pair["recipe_rev"]
            body["lot_id"] = raw.get("lot_id")
            body["tool_id"] = raw.get("tool_id")
        if raw.get("event_time") is not None:
            clocks = resolver.clock_pair(raw["event_time"], raw["arrival_time"])
            body["event_time"] = clocks["event_time"]
            body["arrival_time"] = clocks["arrival_time"]
        if raw.get("overlapping_policy_ids"):
            overlap = resolver.policy_overlap(list(raw["overlapping_policy_ids"]))
            body["overlapping_policy_ids"] = overlap["overlapping_policy_ids"]
            body["region"] = raw.get("region")
        if case_id == "INC-2025-014":
            owner = resolver.empty_owner()
            body["owner_id"] = owner["owner_id"]
            body["task_id"] = raw.get("task_id")
        cases[case_id] = body
    _CASES = cases
    return cases


def get_case(case_id: str) -> dict[str, Any] | None:
    packed = _base_cases().get(case_id)
    if packed is None:
        return None
    body = deepcopy(packed)
    body.update(_MUTATIONS.get(case_id, {}))
    if case_id in _DRAFTS:
        body["draft_plan"] = _DRAFTS[case_id]
    body["approvals"] = list(_APPROVALS.get(case_id, []))
    body["blocked"] = case_id in _BLOCKED
    return body


def queue_items() -> list[dict[str, Any]]:
    rows = []
    for case_id in _base_cases():
        body = get_case(case_id)
        if body is None:
            continue
        rows.append(
            {
                "case_id": body["case_id"],
                "open_operational": body["open_operational"],
                "status": body["status"],
                "severity": body["severity"],
                "amount": body["amount"],
                "waiting_role": body.get("waiting_role"),
                "rank": body.get("rank"),
                "duplicate_candidate": body.get("duplicate_candidate", False),
                "scenario": body.get("scenario"),
            }
        )
    order = {"urgent": 0, "review": 1, "queue": 2, "archive": 3}
    rows.sort(key=lambda row: (order.get(row.get("rank") or "queue", 9), row["case_id"]))
    return rows


def record_approval(case_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    _APPROVALS.setdefault(case_id, []).append(payload)
    action = payload.get("action_type")
    decision = payload.get("decision")
    mutation: dict[str, Any] = {}
    if action == "replay_confirm" and decision == "drop_duplicate":
        mutation["status"] = "DUPLICATE"
        mutation["duplicate_candidate"] = True
        mutation["waiting_role"] = None
    if action == "recipe_hold_or_release":
        mutation["engineering_hold"] = 1 if decision == "hold" else 0
        mutation["waiting_role"] = None
    if action == "policy_pick":
        mutation["chosen_policy_id"] = payload.get("policy_id")
        mutation["waiting_role"] = None
    if action == "keep_wait" or (action == "policy_pick" and decision == "keep_wait"):
        mutation["waiting_role"] = "RT-04"
        mutation.pop("chosen_policy_id", None)
    if action == "assign_owner":
        mutation["owner_id"] = payload.get("owner_id")
        mutation["waiting_role"] = None
    if action == "dispose":
        mutation["waiting_role"] = None
    _MUTATIONS.setdefault(case_id, {}).update(mutation)
    return get_case(case_id) or {}


def set_draft(case_id: str, draft_plan: str) -> None:
    _DRAFTS[case_id] = draft_plan


def mark_blocked(case_id: str) -> None:
    _BLOCKED.add(case_id)


def is_blocked(case_id: str) -> bool:
    return case_id in _BLOCKED
