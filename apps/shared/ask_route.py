"""POST /api/ask. Both apps call the same question builder. Each app supplies its own generate function."""
from __future__ import annotations

import sqlite3
import time
from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.shared.ask_text import build_question, hint_ids
from apps.shared.feature_api import LAKE_DB, _legacy, _sites, _visible_site
from apps.shared.identity import error_body

NEXT_STEP = "Plans are proposals. Changes go through Approvals with an e-signature."


def build_ask_router(*, app_code: str, generate: Callable[..., dict[str, Any]]) -> APIRouter:
    router = APIRouter()

    @router.post("/api/ask")
    def ask(request: Request, payload: dict) -> JSONResponse:
        subject = str(payload.get("subject") or "")
        mode = str(payload.get("mode") or "")
        subject_id = str(payload.get("id") or "")
        if subject not in {"case", "lot", "fault"} or mode not in {"explain", "plan"}:
            return JSONResponse(error_body("bad_request", "Subject must be case, lot, or fault. Mode must be explain or plan."), status_code=400)
        record = _load(subject, subject_id, _sites(request))
        if record is None:
            return JSONResponse(error_body("not_found", "That record is not in the legacy tables."), status_code=404)
        if record.get("forbidden"):
            return JSONResponse(error_body("site_forbidden", "This record is outside the sites on the sign-in token."), status_code=403)
        question, facts = build_question(subject, record, mode)
        hints = hint_ids(subject, subject_id if subject == "fault" else None)
        prompt_id = "P-EXPLAIN-CONFLICT" if mode == "explain" else "P-DRAFT-PLAN"
        started = time.perf_counter()
        result = generate(
            question,
            prompt_id=prompt_id,
            case_id=subject_id if subject == "case" else None,
            hint_item_ids=hints,
        )
        body = {
            "subject": subject,
            "subject_id": subject_id,
            "mode": mode,
            "question": question,
            "facts": facts,
            "sentence": result.get("sentence") or "",
            "draft_plan": result.get("draft_plan"),
            "verdict": result.get("verdict") or "ABSTAIN",
            "citations": result.get("citations") or [],
            "grounded": result.get("grounded"),
            "source_badge": result.get("source_badge"),
            "model": result.get("model") or "",
            "latency_ms": round((time.perf_counter() - started) * 1000, 3),
            "next_step": NEXT_STEP,
        }
        if app_code == "b":
            body.update(_rule_trace(result.get("citations") or [], hints))
        return JSONResponse(body)

    return router


def _load(subject: str, subject_id: str, sites: list[str]) -> dict[str, Any] | None:
    conn = _legacy()
    try:
        if subject == "case":
            row = conn.execute("SELECT * FROM cases WHERE id = ?", (subject_id,)).fetchone()
            if row is None:
                return None
            body = dict(row)
            body["site_code"] = body.get("site")
            if not _visible_site(sites, body.get("site"), subject_id):
                return {"forbidden": True}
            return body
        if subject == "lot":
            row = conn.execute("SELECT * FROM wafer_lots WHERE lot_id = ?", (subject_id,)).fetchone()
            if row is None:
                return None
            body = dict(row)
            step = conn.execute(
                """
                SELECT s.recipe_version, t.recipe_rev, t.chamber, e.ecn_id
                FROM process_steps s
                LEFT JOIN fab_tools t ON t.tool_id = s.tool_id
                LEFT JOIN engineering_changes e ON e.tool_family = t.tool_family AND e.effective_at <= s.started_at
                WHERE s.lot_id = ?
                ORDER BY s.started_at
                LIMIT 1
                """,
                (subject_id,),
            ).fetchone()
            if step:
                body["dispatch_recipe"] = step["recipe_version"]
                body["equipment_recipe"] = step["recipe_rev"]
                body["chamber"] = step["chamber"]
                body["effective_ecn"] = step["ecn_id"]
                body["recipe_mismatch"] = bool(step["recipe_version"] and step["recipe_rev"] and step["recipe_version"] != step["recipe_rev"])
            return body
        if subject == "fault":
            if subject_id not in {"tool_drift", "outlier_wafer", "unqualified_supplier", "lot_genealogy"}:
                return None
            return {"fault_id": subject_id, "required_role": "RT-03", "recommended_action": "Review the findings.", "findings": []}
    finally:
        conn.close()
    return None


def _rule_trace(citations: list[str], hints: list[str]) -> dict[str, Any]:
    if not LAKE_DB.is_file():
        return {"rule_trace": [], "rule_trace_basis": "subject_definitions"}
    conn = sqlite3.connect(f"file:{LAKE_DB.resolve().as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    ids = citations or hints
    basis = "citations" if citations else "subject_definitions"
    rows = []
    for item_id in ids:
        found = conn.execute("SELECT id, kind, statement, trust, item_status FROM items WHERE id = ?", (item_id,)).fetchone()
        if found:
            rows.append(dict(found))
    conn.close()
    return {"rule_trace": rows, "rule_trace_basis": basis}
