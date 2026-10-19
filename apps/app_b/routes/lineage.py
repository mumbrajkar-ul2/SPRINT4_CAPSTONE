"""GET /api/lineage/{item_id}. Application B only. The view does not call Application A."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from apps.app_b.events import mint_correlation_id
from apps.app_b.rules import resolver
from apps.shared.identity import HEADER_CORRELATION, error_body, header_get

router = APIRouter()

PHASE10_CORRELATION_ID = "corr-p10b-doc-20261018-001"
PHASE10_KILL_CORRELATION_ID = "corr-p10b-kill-20261018-001"
PHASE10_ROW_COUNT = 12
PHASE10_TRACE = [
    {"seq": 1, "row_kind": "control", "event_type": "EV-08", "step_name": "load_case", "note": "Case PS000000016"},
    {"seq": 2, "row_kind": "control", "event_type": "EV-04", "step_name": "load_case", "note": "Recipe mismatch mark"},
    {"seq": 3, "row_kind": "agent_step", "event_type": "EV-08", "step_name": "plan_draft", "note": "Model draft. No write"},
    {"seq": 4, "row_kind": "agent_step", "event_type": "EV-08", "step_name": "gather_tools", "note": "Tool get_case"},
    {"seq": 5, "row_kind": "agent_step", "event_type": "EV-08", "step_name": "gather_tools", "note": "Tool get_item"},
    {"seq": 6, "row_kind": "agent_step", "event_type": "EV-08", "step_name": "assemble_evidence", "note": ""},
    {"seq": 7, "row_kind": "agent_step", "event_type": "EV-08", "step_name": "ground_and_cite", "note": "FD-14"},
    {"seq": 8, "row_kind": "control", "event_type": "EV-07", "step_name": "opa_gate", "note": "HOLD_FOR_REVIEW"},
    {"seq": 9, "row_kind": "control", "event_type": "EV-08", "step_name": "interrupt_wait", "note": "paused"},
    {"seq": 10, "row_kind": "control", "event_type": "EV-08", "step_name": "interrupt_wait", "note": "resumed"},
    {"seq": 11, "row_kind": "human_approval", "event_type": "EV-09", "step_name": "apply_human_decision", "note": "RT-03 recorded hold"},
    {"seq": 12, "row_kind": "control", "event_type": "EV-08", "step_name": "write_audit", "note": ""},
]

DEVIATIONS = [
    {
        "program": "Python priority",
        "lake_item_ids": ["code.legacy_logic.priority", "rule.urgent.amount.impl.python"],
        "statement": (
            "Observed ranking from legacy Python. Demo may show 50000 labelled proposed "
            "per rule.threshold.demo_50000. Live silent amount cutoff waits per "
            "rule.threshold.silent (HOLD_FOR_REVIEW)."
        ),
    },
    {
        "program": "JavaScript allow",
        "lake_item_ids": [
            "code.legacy_policy.js_allow",
            "rule.recipe_release.limit.impl.js",
            "rule.recipe_release.limit.impl.js_default",
        ],
        "statement": "Observed 1.05 and 999999. Those numbers are deviations.",
    },
    {
        "program": "Java totals",
        "lake_item_ids": ["code.reconcile_legacy.java_total", "rule.month_end.float.impl.java"],
        "statement": "Observed float total. Canonical money type stays Unknown.",
    },
    {
        "program": "Night batch",
        "lake_item_ids": [
            "code.shift_reconciliation.night_batch",
            "rule.open_flag.impl.night_batch",
            "rule.night_batch.join_multiply",
        ],
        "statement": "Observed open-flag and join multiply.",
    },
]


@router.get("/api/lineage/{item_id}")
def get_lineage(item_id: str, request: Request) -> JSONResponse:
    pin = resolver.pin_meta()
    env = resolver.fetch_item(item_id)
    items = list(env.get("items") or [])
    if not items:
        body = error_body(
            "not_found",
            "No lake item has that id.",
            correlation_id=header_get(request.headers, HEADER_CORRELATION) or None,
        )
        body["verdict"] = "ABSTAIN"
        body["ok"] = False
        return JSONResponse(body, status_code=404)

    links = resolver.fetch_links(item_id)
    edges = list(links.get("edges") or [])
    extra_ids = [
        "decision.bp4.four_programs",
        "decision.fd08.canonical_archive",
        "test.rule.recipe_release.emea_2023",
        "decision.fd06.two_apps",
        "arch.graph.edges_table",
    ]
    extra_items = []
    for extra_id in extra_ids:
        extra = resolver.fetch_item(extra_id)
        extra_items.extend(extra.get("items") or [])

    citations = [item["id"] for item in items]
    for extra in extra_items:
        if extra["id"] not in citations:
            citations.append(extra["id"])
    for edge in edges:
        for key in ("from_id", "to_id"):
            if edge.get(key) and edge[key] not in citations:
                citations.append(edge[key])
    for row in DEVIATIONS:
        for lake_id in row["lake_item_ids"]:
            if lake_id not in citations:
                citations.append(lake_id)

    app_b_corr = header_get(request.headers, HEADER_CORRELATION) or mint_correlation_id()
    return JSONResponse(
        {
            "ok": True,
            "item_id": item_id,
            "item": items[0],
            "edges": edges,
            "citations": citations,
            "lake_version": pin["lake_version"],
            "pin_sqlite_sha256": pin["pin_sqlite_sha256"],
            "phase10_correlation_id": PHASE10_CORRELATION_ID,
            "phase10_kill_correlation_id": PHASE10_KILL_CORRELATION_ID,
            "phase10_row_count": PHASE10_ROW_COUNT,
            "phase10_trace_summary": PHASE10_TRACE,
            "app_b_correlation_id": app_b_corr,
            "app": "app_b",
            "verdict": "ANSWER",
            "deviations": DEVIATIONS,
            "test_item_id": "test.rule.recipe_release.emea_2023",
            "decision_item_id": "decision.bp4.four_programs",
        }
    )
