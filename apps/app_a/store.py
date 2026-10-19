"""Read packaged rows. Overlay the five scenario fixtures. Approvals stay in memory so freeze hashes do not change."""
from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from pathlib import Path
from typing import Any

from apps.app_a.rules.adapter import rank, replay_is_duplicate_candidate

ROOT = Path(__file__).resolve().parents[2]
LEGACY_DB = ROOT / "fabpulse-legacy-workshop-v8-Semiconductor" / "fabpulse-legacy" / "data" / "legacy.sqlite3"
ENTERPRISE_DB = (
    ROOT / "fabpulse-legacy-workshop-v8-Semiconductor" / "fabpulse-legacy" / "data" / "enterprise_legacy.sqlite3"
)

OPEN_WORDS = {
    "OPEN",
    "UNDER_REVIEW",
    "REVIEW",
    "HOLD",
    "ESCALATED",
    "REOPENED",
    "QUEUED",
    "PROCESSING",
    "ENGINEERING_REVIEW",
    "REPLAY",
}

# Packaged row ids. Honesty: REAL. Bound on 2026-10-18 from the freeze sqlite files.
SCENARIO_BINDINGS = {
    "REPLAY-000000000": {
        "scenario": "SP-07",
        "feed_id": "REPLAY-000000000",
        "processing_status": "REPLAY",
        "waiting_role": "RT-05",
        "citation_targets": ["rule.feed.replay_duplicate", "data.feed.replay"],
        "explain_question": "This partner feed has processing_status REPLAY. Explain the duplicate.",
    },
    "PS000000016": {
        "scenario": "SP-08",
        "step_id": "PS000000016",
        "lot_id": "L00000016",
        "tool_id": "T0000013",
        "recipe_version": "R02",
        "recipe_rev": "R01",
        "waiting_role": "RT-03",
        "citation_targets": ["rule.recipe.mismatch_show_both", "data.join.recipe_mismatch"],
        "explain_question": "Dispatch recipe_version is R02 and equipment recipe_rev is R01. Explain the mismatch.",
    },
    "E-00000000": {
        "scenario": "SP-09",
        "event_id": "E-00000000",
        "event_time": "2020-12-30T00:00:00+00:00",
        "arrival_time": "2021-01-01T00:00:00+00:00",
        "citation_targets": ["rule.clock.event_vs_arrival", "data.clock.event_vs_arrival_evidence"],
        "explain_question": "This evidence row has event_time 2020-12-30T00:00:00+00:00 and arrival_time 2021-01-01T00:00:00+00:00. Explain the two clocks.",
    },
    "FAB-00000002": {
        "scenario": "SP-10",
        "object_id": "FAB-00000002",
        "region": "US",
        "overlapping_policy_ids": ["POL-0002", "POL-0010", "POL-0018", "POL-0026", "POL-0034"],
        "waiting_role": "RT-04",
        "citation_targets": ["rule.policy.overlap_or_invalid", "data.policy_register.overlap"],
        "explain_question": "US has five active policy_register rows. Explain the overlap. Do not pick a policy.",
    },
    "INC-2025-014": {
        "scenario": "SP-11",
        "incident_id": "INC-2025-014",
        "owner_id": None,
        "waiting_role": "RT-06",
        "citation_targets": ["term.outage", "decision.inc_2025_014"],
        "explain_question": "Show recovery status. Who is the follow-up owner of INC-2025-014?",
    },
}

_APPROVALS: dict[str, list[dict[str, Any]]] = {}
_MUTATIONS: dict[str, dict[str, Any]] = {}
_BLOCKED: set[str] = set()
_DRAFTS: dict[str, str] = {}
_CACHE: dict[str, Any] | None = None
PACKAGED_OPEN_URIS: list[str] = []


def _open(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.as_posix()}?mode=ro"
    PACKAGED_OPEN_URIS.append(uri)
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _open_operational(status: str) -> bool:
    return status in OPEN_WORDS and status != "CLOSED"


def reset_runtime() -> None:
    global _CACHE
    _APPROVALS.clear()
    _MUTATIONS.clear()
    _BLOCKED.clear()
    _DRAFTS.clear()
    PACKAGED_OPEN_URIS.clear()
    _CACHE = None
    from apps.app_a.audit.store import reset_audit_store
    from apps.app_a.agent.checkpointer import reset_checkpointer
    from apps.app_a.agent.graph import reset_graph

    reset_audit_store()
    reset_checkpointer()
    reset_graph()


def load_packaged() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    cases: dict[str, dict[str, Any]] = {}
    with _open(LEGACY_DB) as conn:
        for row in conn.execute("SELECT id, status, severity, amount, note, site, region FROM cases"):
            body = {
                "case_id": row["id"],
                "status": row["status"],
                "open_operational": _open_operational(row["status"]),
                "severity": row["severity"],
                "amount": row["amount"],
                "note": row["note"],
                "site": row["site"],
                "region": row["region"],
                "untrusted_quotes": [],
                "waiting_role": None,
                "owner_id": None,
                "finance_closed": False,
                "audit_closed": False,
                "duplicate_candidate": False,
                "rank": rank(row["status"], row["severity"], row["amount"]),
                "scenario": None,
                "citation_targets": [],
                "engineering_hold": None,
            }
            cases[row["id"]] = body
        for row in conn.execute(
            "SELECT feed_id, processing_status, ref_id, raw_json FROM partner_feeds WHERE processing_status = 'REPLAY'"
        ):
            payload = json.loads(row["raw_json"])
            notes = payload.get("notes") or ""
            body = {
                "case_id": row["feed_id"],
                "status": "REPLAY",
                "open_operational": True,
                "severity": "MEDIUM",
                "amount": 0,
                "processing_status": row["processing_status"],
                "ref_id": row["ref_id"],
                "duplicate_candidate": replay_is_duplicate_candidate(row["processing_status"]),
                "untrusted_quotes": [notes] if "auto approve" in notes.lower() or "disregard" in notes.lower() else [],
                "waiting_role": "RT-05",
                "owner_id": None,
                "rank": "queue",
                "scenario": "SP-07" if row["feed_id"] == "REPLAY-000000000" else "replay",
                "citation_targets": ["rule.feed.replay_duplicate", "data.feed.replay"],
                "explain_question": SCENARIO_BINDINGS["REPLAY-000000000"]["explain_question"],
                "engineering_hold": None,
            }
            cases[row["feed_id"]] = body
        step = conn.execute(
            """
            SELECT p.step_id, p.lot_id, p.tool_id, p.recipe_version, t.recipe_rev,
                   w.engineering_hold
            FROM process_steps p
            JOIN fab_tools t ON p.tool_id = t.tool_id
            LEFT JOIN wafer_lots w ON p.lot_id = w.lot_id
            WHERE p.step_id = 'PS000000016'
            """
        ).fetchone()
        if step:
            cases["PS000000016"] = {
                "case_id": "PS000000016",
                "status": "HOLD",
                "open_operational": True,
                "severity": "HIGH",
                "amount": 0,
                "recipe_version": step["recipe_version"],
                "recipe_rev": step["recipe_rev"],
                "lot_id": step["lot_id"],
                "tool_id": step["tool_id"],
                "engineering_hold": step["engineering_hold"],
                "untrusted_quotes": [],
                "waiting_role": "RT-03",
                "owner_id": None,
                "rank": "review",
                "scenario": "SP-08",
                "citation_targets": ["rule.recipe.mismatch_show_both", "data.join.recipe_mismatch"],
                "explain_question": SCENARIO_BINDINGS["PS000000016"]["explain_question"],
                "duplicate_candidate": False,
            }
    with _open(ENTERPRISE_DB) as conn:
        ev = conn.execute(
            "SELECT event_id, object_id, event_time, arrival_time FROM evidence_events WHERE event_id = 'E-00000000'"
        ).fetchone()
        if ev:
            cases["E-00000000"] = {
                "case_id": "E-00000000",
                "status": "OPEN",
                "open_operational": True,
                "severity": "MEDIUM",
                "amount": 0,
                "event_time": ev["event_time"],
                "arrival_time": ev["arrival_time"],
                "object_id": ev["object_id"],
                "untrusted_quotes": [],
                "waiting_role": None,
                "owner_id": None,
                "rank": "queue",
                "scenario": "SP-09",
                "citation_targets": ["rule.clock.event_vs_arrival", "data.clock.event_vs_arrival_evidence"],
                "explain_question": SCENARIO_BINDINGS["E-00000000"]["explain_question"],
                "duplicate_candidate": False,
                "engineering_hold": None,
            }
        policies = [
            dict(row)
            for row in conn.execute(
                "SELECT policy_id, region, policy_code, active, valid_from, valid_to "
                "FROM policy_register WHERE region = 'US' AND active = 1 ORDER BY policy_id"
            )
        ]
        obj = conn.execute(
            "SELECT object_id, region, status FROM operational_objects WHERE object_id = 'FAB-00000002'"
        ).fetchone()
        if obj:
            cases["FAB-00000002"] = {
                "case_id": "FAB-00000002",
                "status": obj["status"],
                "open_operational": _open_operational(obj["status"]),
                "severity": "HIGH",
                "amount": 0,
                "region": obj["region"],
                "overlapping_policy_ids": [row["policy_id"] for row in policies],
                "untrusted_quotes": [],
                "waiting_role": "RT-04",
                "owner_id": None,
                "rank": "review",
                "scenario": "SP-10",
                "citation_targets": ["rule.policy.overlap_or_invalid", "data.policy_register.overlap"],
                "explain_question": SCENARIO_BINDINGS["FAB-00000002"]["explain_question"],
                "duplicate_candidate": False,
                "engineering_hold": None,
            }
        task = conn.execute(
            "SELECT task_id, object_id, status, assigned_to FROM workflow_tasks WHERE task_id = 'T-00000000'"
        ).fetchone()
        cases["INC-2025-014"] = {
            "case_id": "INC-2025-014",
            "status": "OPEN",
            "open_operational": True,
            "severity": "HIGH",
            "amount": 0,
            "owner_id": None,
            "task_id": task["task_id"] if task else "T-00000000",
            "untrusted_quotes": [],
            "waiting_role": "RT-06",
            "rank": "review",
            "scenario": "SP-11",
            "citation_targets": ["term.outage", "decision.inc_2025_014"],
            "explain_question": SCENARIO_BINDINGS["INC-2025-014"]["explain_question"],
            "duplicate_candidate": False,
            "engineering_hold": None,
        }
    _CACHE = {"cases": cases, "us_policies": policies if "policies" in locals() else []}
    return _CACHE


def get_case(case_id: str) -> dict[str, Any] | None:
    packed = load_packaged()["cases"].get(case_id)
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
    packed = load_packaged()["cases"]
    rows = []
    for case_id in packed:
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
