"""Read-only lists for both apps. Numbers come from the legacy database or stay Unknown.

Scrap of 1,500 USD per defect is an estimate. It does not fill a cell the demo calls Unknown.
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sqlite3
import statistics
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

from apps.shared.identity import error_body, header_get
from apps.shared.site_scope import EXEMPT_IDS, fab_label, site_visible

ROOT = Path(__file__).resolve().parents[2]
LEGACY_DB = ROOT / "fabpulse-legacy-workshop-v8-Semiconductor" / "fabpulse-legacy" / "data" / "legacy.sqlite3"
LAKE_DB = ROOT / "context-lake" / "generated" / "context-lake.sqlite3"
SCRAP_USD = 1500
SALES_REGION = {
    "IN-BLR": "APAC",
    "JP-KN": "APAC",
    "US-TX": "AMER",
    "BR-SP": "AMER",
    "DE-BY": "EMEA",
    "GB-ENG": "EMEA",
}
ROLE_ACTION = {
    "RT-01": "dispose",
    "RT-02": "approve_agent",
    "RT-03": "recipe_hold_or_release",
    "RT-04": "policy_pick",
    "RT-05": "replay_confirm",
    "RT-06": "assign_owner",
}
FAB_CODES = {
    "FAB-01": ["JP-KN", "IN-BLR", "DE-BY"],
    "FAB-02": ["US-TX", "BR-SP", "GB-ENG"],
}
DOMAIN_TABLES = (
    "process_steps",
    "metrology",
    "engineering_changes",
    "supplier_parts",
)
PARTNER_TABLES = (
    "partner_feeds",
    "batch_runs",
    "reference_versions",
    "upstream_outages",
    "policy_exceptions",
)
_LINK_WORDS = {
    "en": {
        "link.maps_to": "maps to",
        "link.implements": "implements",
        "link.conflicts_with": "conflicts with",
        "link.supersedes": "supersedes",
        "link.governs": "governs",
        "link.evidenced_by": "evidenced by",
        "link.depends_on": "depends on",
        "link.tested_by": "tested by",
        "link.all": "All links",
    },
    "zh-TW": {
        "link.maps_to": "對應",
        "link.implements": "實作",
        "link.conflicts_with": "相衝突",
        "link.supersedes": "取代",
        "link.governs": "管轄",
        "link.evidenced_by": "由證據支持",
        "link.depends_on": "依賴",
        "link.tested_by": "由測試鎖定",
        "link.all": "全部連結",
    },
}
NAV = {
    "en": {
        "nav.home": "Home",
        "nav.dashboard": "Dashboard",
        "nav.cases": "Cases",
        "nav.approvals": "Approvals",
        "nav.scenarios": "Scenarios",
        "nav.lots": "Lot genealogy & SPC",
        "nav.partners": "Partner feeds",
        "nav.graph": "Knowledge graph",
        "nav.glossary": "Glossary",
        "nav.audit": "Audit",
        "nav.kpis": "A-vs-B KPIs",
        "nav.faults": "Fault scenarios",
        "nav.queue": "Queue",
        "nav.ask": "Ask",
        "nav.compare": "Compare",
        "header.sites": "All my sites",
        "header.language": "Language",
        "header.signout": "Logout",
        "btn.apply": "Apply",
        "btn.show_graph": "Show graph",
        "btn.show_lot": "Show lot",
        "btn.search": "Search",
        "btn.sign": "Sign",
        "btn.back": "Back",
        "btn.clear": "Clear",
        "page.home.title": "Home",
        "page.home.sentence": "See what is waiting on this shift, then open that page.",
        "page.dashboard.title": "Dashboard",
        "page.dashboard.sentence": "Open cases, holds, and yield for the sites on this sign-in.",
        "page.cases.title": "Cases",
        "page.cases.sentence": "Find a case on your sites and read its timeline.",
        "page.approvals.title": "Approvals",
        "page.approvals.sentence": "Read the waiting item, then sign it.",
        "page.scenarios.title": "Scenarios",
        "page.scenarios.sentence": "The seven demo cases: replay, recipe, clocks, policy, outage, rule trace, and compare.",
        "page.lots.title": "Lot genealogy and SPC",
        "page.lots.sentence": "Follow a lot through its steps, then read the control chart for one measurement.",
        "page.partners.title": "Partner feeds",
        "page.partners.sentence": "Partner deliveries, batch runs, reference versions, outages, and policy exceptions.",
        "page.graph.title": "Knowledge graph",
        "page.graph.sentence": "Item relationships derived from the legacy data.",
        "page.glossary.title": "Glossary",
        "page.glossary.sentence": "One name for each term, and the local words that map to it.",
        "page.audit.title": "Audit",
        "page.audit.sentence": "The recorded writes, in the order they were stored.",
        "page.kpis.title": "A-vs-B KPIs",
        "page.kpis.sentence": "Measured figures, and the cells this demo has not measured.",
        "page.faults.title": "Fault scenarios",
        "page.faults.sentence": "Four checks over lots, tools, wafers, and supplier parts.",
        "app.a": "This app drafts an answer with the model, then a person signs any change.",
        "app.b": "This app answers from the Context Lake and does not call the model.",
        **_LINK_WORDS["en"],
    },
    "zh-TW": {
        "nav.home": "首頁",
        "nav.dashboard": "儀表板",
        "nav.cases": "案件",
        "nav.approvals": "核准",
        "nav.scenarios": "情境",
        "nav.lots": "批次譜系與管制圖",
        "nav.partners": "夥伴資料",
        "nav.graph": "知識圖",
        "nav.glossary": "詞彙",
        "nav.audit": "稽核",
        "nav.kpis": "A 與 B 指標",
        "nav.faults": "異常情境",
        "nav.queue": "佇列",
        "nav.ask": "詢問",
        "nav.compare": "比較",
        "header.sites": "我的全部廠區",
        "header.language": "語言",
        "header.signout": "登出",
        "btn.apply": "套用",
        "btn.show_graph": "顯示圖",
        "btn.show_lot": "顯示批次",
        "btn.search": "搜尋",
        "btn.sign": "簽署",
        "btn.back": "返回",
        "btn.clear": "清除",
        "page.home.title": "首頁",
        "page.home.sentence": "先看這一班在等什麼，再打開那個頁面。",
        "page.dashboard.title": "儀表板",
        "page.dashboard.sentence": "這個登入可以看到的未結案件、暫停與良率。",
        "page.cases.title": "案件",
        "page.cases.sentence": "在你的廠區找出一筆案件，並讀它的時間線。",
        "page.approvals.title": "核准",
        "page.approvals.sentence": "先讀等待中的項目，再簽署。",
        "page.scenarios.title": "情境",
        "page.scenarios.sentence": "七個示範：重送、配方、時鐘、政策、中斷、規則路徑、比較。",
        "page.lots.title": "批次譜系與管制圖",
        "page.lots.sentence": "沿著批次的步驟走，再看一項量測的管制圖。",
        "page.partners.title": "夥伴資料",
        "page.partners.sentence": "夥伴交貨、批次、參考版本、中斷與政策例外。",
        "page.graph.title": "知識圖",
        "page.graph.sentence": "由舊資料導出的項目關係。",
        "page.glossary.title": "詞彙",
        "page.glossary.sentence": "每個詞一個名稱，以及對應到它的本地用詞。",
        "page.audit.title": "稽核",
        "page.audit.sentence": "已記錄的寫入，依存放順序排列。",
        "page.kpis.title": "A 與 B 指標",
        "page.kpis.sentence": "已量到的數字，以及這次示範尚未量到的格子。",
        "page.faults.title": "異常情境",
        "page.faults.sentence": "對批次、機台、晶圓與供應零件的四項檢查。",
        "app.a": "這個應用程式用模型起草答案，變更要由人簽署。",
        "app.b": "這個應用程式從情境湖回答，不呼叫模型。",
        **_LINK_WORDS["zh-TW"],
    },
}
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_LOT_ID = re.compile(r"^L\d+$")


def _legacy() -> sqlite3.Connection:
    path = Path(os.environ.get("LEGACY_DB") or LEGACY_DB)
    conn = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _lake() -> sqlite3.Connection | None:
    if not LAKE_DB.is_file():
        return None
    conn = sqlite3.connect(f"file:{LAKE_DB.resolve().as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _page(request: Request) -> tuple[int, int]:
    try:
        limit = int(request.query_params.get("limit") or 50)
    except ValueError:
        limit = 50
    try:
        offset = int(request.query_params.get("offset") or 0)
    except ValueError:
        offset = 0
    return max(1, min(limit, 200)), max(0, offset)


def _sites(request: Request) -> list[str]:
    claims = getattr(request.state, "claims", None) or {}
    sites = claims.get("sites")
    if sites:
        return [str(item) for item in sites]
    return ["FAB-01", "FAB-02"]


def _role(request: Request) -> str:
    claims = getattr(request.state, "claims", None) or {}
    roles = [str(item) for item in (claims.get("roles") or [])]
    for role in roles:
        if role.startswith("RT-"):
            return role
    return header_get(request.headers, "X-Actor-Role")


def _codes(sites: list[str]) -> list[str]:
    codes: list[str] = []
    for label in sites:
        codes.extend(FAB_CODES.get(label, []))
    return codes


def _scoped_codes(request: Request) -> tuple[list[str], list[str], bool]:
    """Token sites, legacy codes, and whether a fab query narrowed them.

    A fab value can only remove codes. It never adds a site the token lacks.
    """
    sites = _sites(request)
    codes = _codes(sites)
    fab = (request.query_params.get("fab") or "").strip()
    if not fab:
        return sites, codes, False
    if fab not in sites:
        return sites, [], True
    allowed = set(FAB_CODES.get(fab, []))
    return sites, [code for code in codes if code in allowed], True


def _case_clause(codes: list[str], narrowed: bool) -> tuple[str, tuple[Any, ...]]:
    if narrowed and not codes:
        return "0", ()
    if not codes:
        return "site IS NULL OR site IN ('')", ()
    marks = ",".join("?" for _ in codes)
    return f"site IS NULL OR site IN ({marks})", tuple(codes)


def _select_filtered(conn: sqlite3.Connection, table: str, request: Request, status: str = "") -> list[dict[str, Any]]:
    query = (request.query_params.get("q") or "").strip()
    filters: list[str] = []
    args: list[Any] = []
    if status:
        filters.append("processing_status = ?")
        args.append(status)
    if table == "metrology" and _LOT_ID.match(query):
        filters.append("lot_id = ?")
        args.append(query)
    elif query:
        columns = _text_columns(conn, table)
        if columns:
            filters.append("(" + " OR ".join(f"{name} LIKE ?" for name in columns) + ")")
            args.extend([f"%{query}%"] * len(columns))
        else:
            filters.append("0")
    where = (" WHERE " + " AND ".join(filters)) if filters else ""
    return _rows(conn, f"SELECT * FROM {table}{where} ORDER BY 1", tuple(args))


def _text_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    names: list[str] = []
    for row in conn.execute(f"PRAGMA table_info({table})"):
        name = str(row[1])
        if not _IDENT.match(name):
            continue
        kind = str(row[2] or "").upper()
        if any(bit in kind for bit in ("INT", "REAL", "FLOA", "DOUB", "NUM", "BOOL")):
            continue
        names.append(name)
    return names


def _visible_site(sites: list[str], site: str | None, record_id: str | None = None) -> bool:
    return site_visible(sites, site, record_id)


def _list(items: list[dict[str, Any]], limit: int, offset: int) -> dict[str, Any]:
    window = items[offset : offset + limit]
    return {"ok": True, "items": window, "total": len(items), "limit": limit, "offset": offset}


def _rows(conn: sqlite3.Connection, sql: str, args: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql, args).fetchall()]


def _case_row(row: dict[str, Any]) -> dict[str, Any]:
    site = row.get("site")
    row["site_code"] = site
    row["sales_region"] = SALES_REGION.get(site or "")
    row["fab_label"] = fab_label(site)
    return row


def _csv_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    if text[:1] in "=+-@":
        return "'" + text
    return text


def _scrap(defect_count: int) -> dict[str, Any]:
    return {
        "defect_count": defect_count,
        "usd_per_defect": SCRAP_USD,
        "amount_usd": defect_count * SCRAP_USD,
        "label": "estimate",
        "measured": False,
        "source": "assumption",
        "note": "1,500 USD per defect is an estimate.",
    }


def _unknown(name: str) -> dict[str, Any]:
    return {"name": name, "value": None, "source": None, "measured": False, "note": "Unknown"}


def build_feature_router(
    *,
    app_code: str,
    queue_items: Callable[[], list[dict[str, Any]]],
    audit_path: Callable[[], Path],
    lake_detail: bool,
) -> APIRouter:
    router = APIRouter()

    @router.get("/api/dashboard")
    def dashboard(request: Request) -> JSONResponse:
        _sites_on, codes, narrowed = _scoped_codes(request)
        where, where_args = _case_clause(codes, narrowed)
        conn = _legacy()
        try:
            by_status = _rows(conn, f"SELECT status, count(*) AS n FROM cases WHERE {where} GROUP BY status", where_args)
            by_severity = _rows(conn, f"SELECT severity, count(*) AS n FROM cases WHERE {where} GROUP BY severity", where_args)
            by_site = _rows(conn, f"SELECT site, count(*) AS n FROM cases WHERE {where} GROUP BY site", where_args)
            for row in by_site:
                row["site_code"] = row.get("site")
                row["sales_region"] = SALES_REGION.get(row.get("site") or "")
            now = conn.execute("SELECT max(started_at) FROM process_steps").fetchone()[0]
            holds = _rows(
                conn,
                """
                SELECT lot_id, tool_id, defect_count, engineering_hold
                FROM wafer_lots WHERE engineering_hold = 1
                """,
            )
            for hold in holds:
                latest = conn.execute(
                    "SELECT max(started_at) FROM process_steps WHERE lot_id = ?",
                    (hold["lot_id"],),
                ).fetchone()[0]
                hold["latest_step"] = latest
                hold["now"] = now
                hold["sla_hours"] = 24
                hold["sla_breached"] = bool(latest and now and latest < now)
            defects = conn.execute("SELECT coalesce(sum(defect_count), 0) FROM wafer_lots").fetchone()[0]
            chambers = _rows(
                conn,
                """
                SELECT coalesce(t.chamber, 'unknown') AS chamber,
                       coalesce(sum(w.defect_count), 0) AS defect_count
                FROM wafer_lots w
                LEFT JOIN fab_tools t ON t.tool_id = w.tool_id
                GROUP BY coalesce(t.chamber, 'unknown')
                ORDER BY defect_count DESC
                """,
            )
            yield_row = conn.execute("SELECT avg(measured_yield) FROM wafer_lots").fetchone()[0]
        finally:
            conn.close()
        scrap_by_chamber = []
        for chamber in chambers:
            row = _scrap(int(chamber["defect_count"]))
            row["chamber"] = chamber["chamber"]
            scrap_by_chamber.append(row)
        return JSONResponse(
            {
                "ok": True,
                "open_cases": {"by_status": by_status, "by_severity": by_severity, "by_site": by_site},
                "engineering_holds": holds,
                "scrap": _scrap(int(defects)),
                "scrap_by_chamber": scrap_by_chamber,
                "lot_scope": "all_lots",
                "yield": {"value": yield_row, "measured": True, "source": "wafer_lots.measured_yield"},
                "mtta": _unknown("mtta"),
                "mttr": _unknown("mttr"),
                "now": now,
                "link_note": "Cases link to lots by sequence number, not by a foreign key.",
                "clock_note": "Now is the latest process step time. The legacy rows end in February 2023.",
            }
        )

    @router.get("/api/cases")
    def case_list(request: Request) -> JSONResponse:
        sites, codes, narrowed = _scoped_codes(request)
        limit, offset = _page(request)
        if narrowed and not codes:
            filters = ["0"]
            args = []
        elif codes:
            filters = ["(site IS NULL OR site IN (" + ",".join("?" for _ in codes) + "))"]
            args = list(codes)
        else:
            filters = ["site IS NULL"]
            args = []
        for key in ("status", "severity", "segment", "site"):
            value = request.query_params.get(key)
            if value:
                filters.append(f"{key} = ?")
                args.append(value)
        query = request.query_params.get("q")
        if query:
            filters.append("(id LIKE ? OR note LIKE ?)")
            args.extend([f"%{query}%", f"%{query}%"])
        sql = "SELECT * FROM cases WHERE " + " AND ".join(filters) + " ORDER BY id"
        conn = _legacy()
        try:
            rows = [_case_row(row) for row in _rows(conn, sql, tuple(args))]
        finally:
            conn.close()
        rows = [row for row in rows if _visible_site(sites, row.get("site"), row.get("id"))]
        return JSONResponse(_list(rows, limit, offset))

    @router.get("/api/cases/{case_id}/detail")
    def case_detail(case_id: str, request: Request) -> JSONResponse:
        sites = _sites(request)
        conn = _legacy()
        try:
            found = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
            if found is None:
                return JSONResponse(error_body("not_found", "No legacy case has that id."), status_code=404)
            body = _case_row(dict(found))
            if case_id not in EXEMPT_IDS and not _visible_site(sites, body.get("site"), case_id):
                return JSONResponse(error_body("site_forbidden", "This record is outside the sites on the sign-in token."), status_code=403)
            timeline = _rows(conn, "SELECT * FROM events WHERE case_id = ? ORDER BY recorded_at", (case_id,))
            policies = _rows(conn, "SELECT * FROM policy_exceptions ORDER BY recorded_at DESC LIMIT 20")
        finally:
            conn.close()
        detail = {
            "ok": True,
            "case": body,
            "timeline": timeline,
            "policies": policies,
            "link_note": "Cases link to lots by sequence number, not by a foreign key.",
        }
        if lake_detail:
            lake = _lake()
            if lake is not None:
                detail["lake_item_ids"] = [row[0] for row in lake.execute("SELECT id FROM items ORDER BY id LIMIT 20")]
                lake.close()
        return JSONResponse(detail)

    @router.get("/api/approvals/pending")
    def pending(request: Request) -> JSONResponse:
        role = _role(request)
        sites = _sites(request)
        items = []
        for row in queue_items():
            if row.get("waiting_role") != role:
                continue
            if not _visible_site(sites, row.get("site"), row.get("case_id")):
                continue
            item = dict(row)
            item["action_type"] = ROLE_ACTION.get(role, "")
            item["proposed_by"] = item.get("proposed_by") or "model_draft"
            items.append(item)
        limit, offset = _page(request)
        return JSONResponse(_list(items, limit, offset))

    @router.get("/api/domain/{table}")
    def domain(table: str, request: Request) -> JSONResponse:
        if table not in DOMAIN_TABLES:
            return JSONResponse(error_body("not_found", "That domain table is not on this list."), status_code=404)
        limit, offset = _page(request)
        conn = _legacy()
        try:
            rows = _select_filtered(conn, table, request)
        finally:
            conn.close()
        return JSONResponse(_list(rows, limit, offset))

    @router.get("/api/lots/{lot_id}/genealogy")
    def genealogy(lot_id: str) -> JSONResponse:
        conn = _legacy()
        try:
            lot = conn.execute("SELECT * FROM wafer_lots WHERE lot_id = ?", (lot_id,)).fetchone()
            if lot is None:
                return JSONResponse(error_body("not_found", "No lot has that id."), status_code=404)
            steps = _rows(
                conn,
                """
                SELECT s.step_id, s.step_name, s.started_at, s.recipe_version, s.tool_id,
                       t.recipe_rev, t.chamber, t.tool_family
                FROM process_steps s
                LEFT JOIN fab_tools t ON t.tool_id = s.tool_id
                WHERE s.lot_id = ?
                ORDER BY s.started_at
                """,
                (lot_id,),
            )
            for step in steps:
                step["recipe_mismatch"] = bool(step.get("recipe_version") and step.get("recipe_rev") and step["recipe_version"] != step["recipe_rev"])
                ecn = conn.execute(
                    """
                    SELECT ecn_id, to_rev, effective_at FROM engineering_changes
                    WHERE tool_family = ? AND effective_at <= ?
                    ORDER BY effective_at DESC LIMIT 1
                    """,
                    (step.get("tool_family"), step.get("started_at") or ""),
                ).fetchone()
                step["effective_ecn"] = dict(ecn) if ecn else None
                step["ecn_conflict"] = bool(ecn and step.get("recipe_version") and ecn["to_rev"] != step["recipe_version"])
                if step["recipe_mismatch"]:
                    step["flag"] = f"Dispatch recipe {step['recipe_version']} and tool recipe {step['recipe_rev']} differ."
        finally:
            conn.close()
        return JSONResponse(
            {
                "ok": True,
                "lot": dict(lot),
                "steps": steps,
                "link_note": "Cases link to lots by sequence number, not by a foreign key.",
            }
        )

    @router.get("/api/spc/{parameter}")
    def spc(parameter: str) -> JSONResponse:
        conn = _legacy()
        try:
            rows = _rows(conn, "SELECT * FROM metrology WHERE parameter = ? ORDER BY sample_id", (parameter,))
        finally:
            conn.close()
        if not rows:
            return JSONResponse(error_body("not_found", "No metrology rows use that parameter."), status_code=404)
        values = [float(row["measured"]) for row in rows]
        mean = statistics.fmean(values)
        sigma = statistics.pstdev(values) if len(values) > 1 else 0.0
        units = sorted({row.get("unit") for row in rows if row.get("unit")})
        flags = _western(values, mean, sigma)
        return JSONResponse(
            {
                "ok": True,
                "parameter": parameter,
                "items": rows,
                "mean": mean,
                "sigma": sigma,
                "limits": {"1": sigma, "2": 2 * sigma, "3": 3 * sigma},
                "spec_low": rows[0].get("spec_low"),
                "spec_high": rows[0].get("spec_high"),
                "rules": flags,
                "unit_warning": "This parameter mixes units." if len(units) > 1 else None,
                "units": units,
                "measured": True,
                "source": "metrology",
            }
        )

    @router.get("/api/partners/{table}")
    def partners(table: str, request: Request) -> JSONResponse:
        if table not in PARTNER_TABLES:
            return JSONResponse(error_body("not_found", "That partner table is not on this list."), status_code=404)
        status = (request.query_params.get("status") or "").strip()
        if status and table != "partner_feeds":
            return JSONResponse(error_body("bad_request", "Status applies only to partner feeds."), status_code=400)
        limit, offset = _page(request)
        conn = _legacy()
        try:
            rows = _select_filtered(conn, table, request, status=status if table == "partner_feeds" else "")
            rejected, inputs = conn.execute(
                "SELECT coalesce(sum(rejected_count), 0), coalesce(sum(input_count), 0) FROM batch_runs"
            ).fetchone()
            drift = conn.execute(
                """
                SELECT count(*) FROM (
                    SELECT ref_key FROM reference_versions GROUP BY ref_key HAVING count(*) > 1
                )
                """
            ).fetchone()[0]
        finally:
            conn.close()
        body = _list(rows, limit, offset)
        body["rejection_rate"] = {
            "value": (rejected / inputs) if inputs else None,
            "measured": bool(inputs),
            "source": "batch_runs",
        }
        body["retry_rate"] = _unknown("retry_rate")
        body["reference_version_drift"] = {"value": drift, "measured": True, "source": "reference_versions"}
        return JSONResponse(body)

    @router.get("/api/audit/search")
    def audit_search(request: Request) -> Response:
        limit, offset = _page(request)
        path = audit_path()
        if not path.is_file():
            rows: list[dict[str, Any]] = []
        else:
            conn = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            filters = ["1=1"]
            args: list[Any] = []
            if request.query_params.get("actor"):
                filters.append("actor_id = ?")
                args.append(request.query_params["actor"])
            if request.query_params.get("case"):
                filters.append("case_id = ?")
                args.append(request.query_params["case"])
            if request.query_params.get("from"):
                filters.append("occurred_at >= ?")
                args.append(request.query_params["from"])
            if request.query_params.get("to"):
                filters.append("occurred_at <= ?")
                args.append(request.query_params["to"])
            order = (request.query_params.get("order") or "asc").lower()
            if order not in {"asc", "desc"}:
                conn.close()
                return JSONResponse(error_body("bad_request", "Order must be asc or desc."), status_code=400)
            sql = "SELECT * FROM audit_chain WHERE " + " AND ".join(filters) + f" ORDER BY seq {order}"
            try:
                rows = [dict(row) for row in conn.execute(sql, tuple(args))]
            except sqlite3.Error:
                rows = []
            finally:
                conn.close()
        if request.query_params.get("format") == "csv":
            handle = io.StringIO()
            writer = csv.writer(handle)
            fields = list(rows[0].keys()) if rows else ["audit_id"]
            writer.writerow(fields)
            for row in rows[offset : offset + limit]:
                writer.writerow([_csv_cell(row.get(field)) for field in fields])
            return Response(handle.getvalue(), media_type="text/csv")
        return JSONResponse(_list(rows, limit, offset))

    @router.get("/api/semantic/terms")
    def terms(request: Request) -> JSONResponse:
        query = (request.query_params.get("q") or "").strip()
        lake = _lake()
        if lake is None:
            return JSONResponse(_list([], *_page(request)))
        if query:
            rows = _rows(
                lake,
                "SELECT * FROM terms WHERE canonical_name LIKE ? OR definition LIKE ? OR term_id LIKE ? ORDER BY term_id",
                (f"%{query}%", f"%{query}%", f"%{query}%"),
            )
        else:
            rows = _rows(lake, "SELECT * FROM terms ORDER BY term_id")
        lake.close()
        return JSONResponse(_list(rows, *_page(request)))

    @router.get("/api/graph")
    def graph() -> JSONResponse:
        lake = _lake()
        if lake is None:
            return JSONResponse({"ok": True, "items": []})
        rows = _rows(
            lake,
            """
            SELECT id, kind, statement FROM items
            WHERE id IN (
                SELECT from_id FROM edges GROUP BY from_id ORDER BY count(*) DESC LIMIT 12
            )
            """,
        )
        lake.close()
        return JSONResponse({"ok": True, "items": rows[:12]})

    @router.get("/api/graph/{item_id}")
    def graph_item(item_id: str) -> JSONResponse:
        lake = _lake()
        if lake is None:
            return JSONResponse(error_body("not_found", "The lake file is not on this machine."), status_code=404)
        seed = lake.execute("SELECT id, kind, statement FROM items WHERE id = ?", (item_id,)).fetchone()
        if seed is None:
            lake.close()
            return JSONResponse(error_body("not_found", "That id is not a lake item."), status_code=404)
        nodes: dict[str, dict[str, Any]] = {item_id: {**dict(seed), "hop": 0}}
        frontier = [item_id]
        for hop in (1, 2):
            nxt: list[str] = []
            for node in frontier:
                for edge in lake.execute(
                    "SELECT from_id, to_id, type FROM edges WHERE from_id = ? OR to_id = ?",
                    (node, node),
                ):
                    other = edge["to_id"] if edge["from_id"] == node else edge["from_id"]
                    if other not in nodes and len(nodes) < 60:
                        found = lake.execute("SELECT id, kind, statement FROM items WHERE id = ?", (other,)).fetchone()
                        if found:
                            nodes[other] = {**dict(found), "hop": hop}
                            nxt.append(other)
            frontier = nxt
        id_list = list(nodes)
        marks = ",".join("?" for _ in id_list)
        edges = _rows(
            lake,
            f"SELECT from_id, to_id, type FROM edges WHERE from_id IN ({marks}) AND to_id IN ({marks})",
            tuple(id_list) + tuple(id_list),
        )
        lake.close()
        return JSONResponse({"ok": True, "item_id": item_id, "nodes": list(nodes.values()), "edges": edges})

    @router.get("/api/kpi/compare")
    def kpi() -> JSONResponse:
        return JSONResponse(
            {
                "ok": True,
                "cells": [
                    _unknown("mtta"),
                    _unknown("mttr"),
                    _unknown("api_p95_ms"),
                    _unknown("groundedness_percent"),
                ],
                "scrap_rate": {
                    "usd_per_defect": SCRAP_USD,
                    "label": "estimate",
                    "measured": False,
                    "source": "assumption",
                    "note": "1,500 USD per defect is an estimate. It does not fill an Unknown cell.",
                },
            }
        )

    @router.get("/api/costs")
    def costs() -> JSONResponse:
        conn = _legacy()
        try:
            rows = _rows(conn, "SELECT * FROM operating_costs ORDER BY period")
            defects = int(conn.execute("SELECT coalesce(sum(defect_count), 0) FROM wafer_lots").fetchone()[0])
        finally:
            conn.close()
        return JSONResponse({"ok": True, "periods": rows, "scrap": _scrap(defects), "measured_cost": True, "source": "operating_costs"})

    @router.get("/api/scenarios/faults")
    def faults() -> JSONResponse:
        conn = _legacy()
        try:
            drift = _rows(
                conn,
                """
                SELECT t.chamber, sum(w.defect_count) AS defects
                FROM wafer_lots w JOIN fab_tools t ON t.tool_id = w.tool_id
                GROUP BY t.chamber
                ORDER BY defects DESC
                """,
            )
            outlier = _rows(
                conn,
                """
                SELECT sample_id, lot_id, parameter, measured, unit, spec_low, spec_high
                FROM metrology
                WHERE measured < spec_low OR measured > spec_high
                """,
            )
            supplier = _rows(
                conn,
                """
                SELECT part_id, vendor, tool_family, qualification_state
                FROM supplier_parts
                WHERE qualification_state != 'QUALIFIED'
                """,
            )
            genealogy_hits = _rows(
                conn,
                """
                SELECT s.step_id, s.lot_id, s.recipe_version, t.recipe_rev
                FROM process_steps s
                JOIN fab_tools t ON t.tool_id = s.tool_id
                WHERE s.recipe_version != t.recipe_rev
                """,
            )
        finally:
            conn.close()
        return JSONResponse(
            {
                "ok": True,
                "detectors": [
                    {"id": "tool_drift", "findings": drift, "recommended_action": "Review the chamber with the highest defect count.", "required_role": "RT-03"},
                    {"id": "outlier_wafer", "findings": outlier, "recommended_action": "Hold a wafer that sits outside its spec.", "required_role": "RT-03"},
                    {"id": "unqualified_supplier", "findings": supplier, "recommended_action": "Do not treat an expired or pending part as qualified.", "required_role": "RT-04"},
                    {
                        "id": "lot_genealogy",
                        "findings": genealogy_hits,
                        "recommended_action": "Show both recipe ids when they differ.",
                        "required_role": "RT-03",
                        "flag": "A step recipe and the tool recipe differ.",
                    },
                ],
            }
        )

    @router.get("/api/flags")
    def flags() -> JSONResponse:
        path = Path(__file__).resolve().parent / f"flags-{app_code}.json"
        if not path.is_file():
            return JSONResponse({"ok": True, "flags": {}})
        return JSONResponse({"ok": True, "flags": json.loads(path.read_text(encoding="utf-8"))})

    @router.get("/api/notifications")
    def notifications() -> JSONResponse:
        conn = _legacy()
        try:
            now = conn.execute("SELECT max(started_at) FROM process_steps").fetchone()[0]
            holds = _rows(conn, "SELECT lot_id FROM wafer_lots WHERE engineering_hold = 1")
        finally:
            conn.close()
        items = [
            {"kind": "sla_breach", "lot_id": row["lot_id"], "sla_hours": 24, "now": now}
            for row in holds
        ]
        webhook = os.environ.get("FF_TEAMS_WEBHOOK")
        posted = False
        if webhook and items:
            posted = _post_webhook(webhook, {"items": len(items)})
        return JSONResponse({"ok": True, "items": items, "teams_posted": posted})

    @router.get("/api/i18n/{locale}")
    def i18n(locale: str) -> JSONResponse:
        strings = NAV.get(locale)
        if strings is None:
            return JSONResponse(error_body("not_found", "That locale is not on this list."), status_code=404)
        return JSONResponse({"ok": True, "locale": locale, "strings": strings})

    return router


def _western(values: list[float], mean: float, sigma: float) -> dict[str, list[int]]:
    if sigma == 0:
        return {"rule_1": [], "rule_2": [], "rule_3": [], "rule_4": []}
    zed = [(value - mean) / sigma for value in values]

    def side(index: int, band: float) -> int:
        if zed[index] > band:
            return 1
        if zed[index] < -band:
            return -1
        return 0

    rule_1 = [index for index, score in enumerate(zed) if abs(score) > 3]
    rule_2: list[int] = []
    rule_3: list[int] = []
    rule_4: list[int] = []
    for start in range(len(zed)):
        window3 = [side(index, 2) for index in range(start, min(start + 3, len(zed)))]
        if len(window3) == 3 and (window3.count(1) >= 2 or window3.count(-1) >= 2):
            rule_2.append(start)
        window5 = [side(index, 1) for index in range(start, min(start + 5, len(zed)))]
        if len(window5) == 5 and (window5.count(1) >= 4 or window5.count(-1) >= 4):
            rule_3.append(start)
        window8 = [1 if zed[index] > 0 else -1 if zed[index] < 0 else 0 for index in range(start, min(start + 8, len(zed)))]
        if len(window8) == 8 and (window8.count(1) == 8 or window8.count(-1) == 8):
            rule_4.append(start)
    return {"rule_1": rule_1, "rule_2": rule_2, "rule_3": rule_3, "rule_4": rule_4}


def _post_webhook(url: str, payload: dict[str, Any]) -> bool:
    from urllib.request import Request, urlopen

    try:
        request = Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=1) as response:
            return 200 <= int(response.status) < 300
    except OSError:
        return False
