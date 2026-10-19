"""Read the full audit trace for one correlation id, ordered by seq."""
from __future__ import annotations

import json
from typing import Any

from apps.app_a.audit.store import COLUMNS, get_connection


def _decode(row: Any) -> dict[str, Any]:
    body = {name: row[name] for name in COLUMNS}
    raw_ids = body.get("lake_item_ids") or "[]"
    try:
        body["lake_item_ids"] = json.loads(raw_ids)
    except json.JSONDecodeError:
        body["lake_item_ids"] = []
    return body


def read_trace(correlation_id: str) -> list[dict[str, Any]]:
    if not correlation_id:
        return []
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM audit_chain WHERE correlation_id = ? ORDER BY seq ASC",
        (correlation_id,),
    ).fetchall()
    return [_decode(row) for row in rows]
