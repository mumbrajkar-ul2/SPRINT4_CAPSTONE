"""GET /api/queue. Order from transformed priority(). No model."""
from __future__ import annotations

from fastapi import APIRouter, Request

from apps.app_a.events import record_event
from apps.app_a.store import queue_items
from apps.shared.identity import HEADER_ACTOR_ID, HEADER_ACTOR_ROLE, HEADER_CORRELATION, header_get

router = APIRouter()


@router.get("/api/queue")
def get_queue(request: Request) -> dict[str, object]:
    items = queue_items()
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
                lake_item_ids=["rule.feed.replay_duplicate"],
            )
            break
    return {"ok": True, "items": items, "model_used": False}
