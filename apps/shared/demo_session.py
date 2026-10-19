"""Session overlay for the live demo. The packaged sqlite files stay unread by this module."""
from __future__ import annotations

from typing import Any

PROPOSED_BY = "model_draft"
PHASE10_CORRELATION_ID = "corr-p10b-doc-20261018-001"
PACKAGED_REPLAY_ROWS = 67

REPLAY = {
    "ref": "C00001646",
    "feed_id": "FEED-000000000",
    "replay_id": "REPLAY-000000000",
    "feed_ingested": "2022-04-25T19:09",
    "replay_ingested": "2022-04-25T20:09",
    "source_time": "2022-04-25T19:39",
    "lake_item_id": "data.demo.replay_pair",
}

RECIPE = {
    "step_id": "PS000000016",
    "family": "etch",
    "started": "2023-01-05T16:00",
    "ended": "2023-01-05T23:00",
    "dispatch_recipe": "R02",
    "tool_id": "T0000013",
    "tool_recipe": "R01",
    "tool_effective_date": None,
    "change_id": "ECN0000001",
    "change_from": "R01",
    "change_to": "R02",
    "change_effective": "2023-01-01T07:00",
    "change_status": "APPROVED",
    "lake_item_id": "data.demo.recipe_times",
}

CLOCK = {
    "event_id": "E-00000000",
    "kind": "tool_alarm",
    "event_time": "2020-12-30",
    "arrival_time": "2021-01-01",
    "metrology_clock": "Metrology samples have no clock.",
    "lake_item_id": "data.demo.backfill_clock",
}

POLICIES = [
    {"policy_id": "POL-0002", "valid_from": "2023-01-01", "valid_to": None},
    {"policy_id": "POL-0010", "valid_from": "2021-01-01", "valid_to": None},
    {"policy_id": "POL-0018", "valid_from": "2024-01-01", "valid_to": "2024-12-31"},
    {"policy_id": "POL-0026", "valid_from": "2022-01-01", "valid_to": None},
    {"policy_id": "POL-0034", "valid_from": "2025-01-01", "valid_to": None},
]
POLICY_ON_DATE = "2024-06-01"
POLICY_LAKE_ITEM = "data.demo.policy_windows"

RULE_TRACE = [
    {"step": 1, "role": "historical decision", "item_id": "decision.bp4.four_programs"},
    {"step": 2, "role": "earlier code", "item_id": "code.legacy_policy.js_allow"},
    {"step": 3, "role": "specification", "item_id": "data.contract.decision_policies_archive"},
    {"step": 4, "role": "test", "item_id": "test.rule.recipe_release.emea_2023"},
    {"step": 5, "role": "transformed implementation", "item_id": "code.transformed.evaluate_live_policy"},
]


def policies_in_force(on_date: str = POLICY_ON_DATE) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    for row in POLICIES:
        start = row["valid_from"]
        end = row["valid_to"]
        if start <= on_date and (end is None or on_date <= end):
            chosen.append(row)
    return chosen


class DemoSession:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.replay_open = False
        self.backfill_applied = False
        self.policy_checked = False
        self.policy_choice: str | None = None
        self.parked: list[dict[str, Any]] = []
        self.last_probe: dict[str, Any] | None = None
        self.gateway_message: dict[str, Any] | None = None
        self.owner_typed: str | None = None
        self.correlation_id: str | None = None

    def queue_extra(self) -> int:
        extra = 1 if self.replay_open else 0
        if self.gateway_message is not None:
            extra += 1
        return extra

    def receive_replay(self) -> None:
        self.replay_open = True

    def confirm_drop(self, *, actor_role: str) -> str | None:
        if actor_role != "RT-05":
            return "Confirm drop waits for RT-05."
        self.replay_open = False
        return None

    def apply_backfill(self) -> None:
        self.backfill_applied = True

    def check_policy(self) -> dict[str, Any]:
        self.policy_checked = True
        in_force = policies_in_force()
        return {
            "on_date": POLICY_ON_DATE,
            "in_force_count": len(in_force),
            "in_force": in_force,
            "verdict": "ABSTAIN",
            "sentence": "Four policies are in force. The app abstains and waits for RT-04.",
        }

    def decide_policy(self, choice: str, *, actor_role: str) -> str | None:
        if actor_role != "RT-04":
            return "A policy decision waits for RT-04."
        self.policy_choice = choice
        return None

    def park(self, message_id: str = "DLQ-DEMO-BAD") -> dict[str, Any]:
        row = {
            "parked_id": message_id,
            "message_id": message_id,
            "status": "PARKED",
        }
        self.parked = [item for item in self.parked if item["message_id"] != message_id]
        self.parked.append(row)
        return row

    def replay_parked(self, message_id: str = "DLQ-DEMO-BAD") -> dict[str, Any] | None:
        for row in self.parked:
            if row["message_id"] == message_id:
                row["status"] = "REPLAYED"
                return row
        return None

    def receive_gateway(self, message_id: str, body: dict[str, Any]) -> None:
        self.gateway_message = {"message_id": message_id, "body": body}

    def snapshot(self, *, base_queue: int, app_name: str, lineage: bool) -> dict[str, Any]:
        policy = self.check_policy() if self.policy_checked else {
            "on_date": POLICY_ON_DATE,
            "in_force_count": len(policies_in_force()),
            "in_force": policies_in_force(),
            "verdict": None,
            "sentence": "Check the overlap has not run.",
        }
        if self.policy_checked:
            policy["verdict"] = "ABSTAIN"
        return {
            "ok": True,
            "app_name": app_name,
            "lineage": lineage,
            "proposed_by": PROPOSED_BY,
            "packaged_replay_rows": PACKAGED_REPLAY_ROWS,
            "queue_count": base_queue + self.queue_extra(),
            "base_queue": base_queue,
            "replay_open": self.replay_open,
            "replay": REPLAY,
            "recipe": RECIPE,
            "clock": CLOCK,
            "backfill_applied": self.backfill_applied,
            "policy": policy,
            "policy_choice": self.policy_choice,
            "parked_intakes": list(self.parked),
            "last_probe": self.last_probe,
            "gateway_message": self.gateway_message,
            "owner_id": self.owner_typed or "",
            "phase10_correlation_id": PHASE10_CORRELATION_ID,
            "correlation_id": self.correlation_id,
            "rule_trace": RULE_TRACE if lineage else [],
            "known_differences": [
                "Application A has no lineage route.",
                "The 50,000 label is proposed on Application B only.",
            ],
        }
