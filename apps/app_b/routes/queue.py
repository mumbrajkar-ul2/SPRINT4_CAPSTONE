"""GET /api/queue. Rank from lake cards. No model."""
from __future__ import annotations

from fastapi import APIRouter, Request

from apps.app_b.events import record_event
from apps.app_b.rules import resolver
from apps.app_b.store import queue_items
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get

router = APIRouter()


@router.get("/api/queue")
def get_queue(request: Request) -> dict[str, object]:
    items = queue_items()
    pin = resolver.pin_meta()
    replay = resolver.replay_count()
    cutoff = resolver.amount_cutoff_display()
    correlation_id = header_get(request.headers, HEADER_CORRELATION) or None
    actor_id = header_get(request.headers, HEADER_ACTOR_ID)
    actor_role = header_get(request.headers, HEADER_ACTOR_ROLE)
    for row in items:
        if row.get("duplicate_candidate"):
            record_event(
                "EV-02",
                correlation_id=correlation_id,
                actor_id=actor_id,
                actor_role=actor_role,
                case_id=row["case_id"],
                lake_item_ids=["rule.feed.replay_duplicate", "data.feed.replay"],
            )
            break
    return {
        "ok": True,
        "items": items,
        "model_used": False,
        "replay_candidate_count": replay["replay_candidate_count"],
        "replay_candidate_count_citations": replay["citations"],
        "amount_cutoff_label": cutoff["amount_cutoff_label"],
        "demo_amount_cutoff": cutoff["demo_amount_cutoff"],
        "live_amount_cutoff": cutoff["live_amount_cutoff"],
        "amount_cutoff_citations": cutoff["citations"],
        "lake_version": pin["lake_version"],
        "pin_sqlite_sha256": pin["pin_sqlite_sha256"],
    }
