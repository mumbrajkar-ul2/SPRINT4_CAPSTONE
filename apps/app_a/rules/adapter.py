"""Import Phase 7 functions from the inherited tree. Do not treat lake YAML as live policy."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LEGACY_ROOT = ROOT / "fabpulse-legacy-workshop-v8-Semiconductor" / "fabpulse-legacy"
if str(LEGACY_ROOT) not in sys.path:
    sys.path.insert(0, str(LEGACY_ROOT))

from app.gateway_bridge import intake_apply  # noqa: E402
from app.legacy_logic import evaluate_live_policy, priority  # noqa: E402
from app.partner_feeds import reconcile_feeds  # noqa: E402

HOLD_FOR_REVIEW = "HOLD_FOR_REVIEW"
REQUIRED_INTAKE_FIELDS = ("message_id", "business_key", "system", "event_type", "occurred_at")


def rank(status: str, severity: str, amount: float) -> str:
    """Queue order from transformed priority(). No model."""
    return priority(status, severity, amount)


def live_policy(region: str | None = None, year: int | None = None, question: str | None = None) -> Any:
    """Archive match or HOLD_FOR_REVIEW from evaluate_live_policy."""
    return evaluate_live_policy(region=region, year=year, question=question)


def replay_is_duplicate_candidate(processing_status: str) -> bool:
    """Same REPLAY rule as reconcile_feeds, without writing the packaged store."""
    return processing_status == "REPLAY"


def invalid_intake_reason(event: Any) -> str:
    if not isinstance(event, dict) or not all(event.get(key) for key in REQUIRED_INTAKE_FIELDS):
        return "missing_required_fields"
    return "unknown_lot"


def intake_dedupe(
    events: list[dict[str, Any]],
    stream: str = "primary",
    *,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """Call transformed intake_apply. Park each invalid event. Tests must point LEGACY_DB at a temp file."""
    from apps.app_a.runtime.dlq import park_invalid_intake

    totals: dict[str, Any] = {"accepted": 0, "duplicates": 0, "invalid": 0, "received": len(events)}
    for event in events:
        one = intake_apply([event], stream=stream)
        totals["accepted"] += one["accepted"]
        totals["duplicates"] += one["duplicates"]
        totals["invalid"] += one["invalid"]
        if one["invalid"]:
            park_invalid_intake(
                event if isinstance(event, dict) else {"value": event},
                reason=invalid_intake_reason(event),
                correlation_id=correlation_id,
            )
    return totals


def imported_reconcile_feeds():
    """Expose the write path for tests that use a temp store. Queue GET does not call this."""
    return reconcile_feeds
