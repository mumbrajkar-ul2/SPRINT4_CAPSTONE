"""Read-only feature lists. The scenario case route stays the SCH-06 body."""
from __future__ import annotations

from fastapi.testclient import TestClient

from apps.app_a.server import app as app_a
from apps.app_b.server import app as app_b
from apps.shared.oidc_session import bearer_headers


def test_case_list_shows_site_code_and_sales_region(api_headers) -> None:
    response = TestClient(app_a).get("/api/cases?limit=5", headers=api_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["total"] >= 1
    row = body["items"][0]
    assert row["site_code"]
    assert row["sales_region"] in {"APAC", "AMER", "EMEA"}


def test_fab_02_does_not_see_a_germany_site() -> None:
    headers = bearer_headers("RT-01", sites=["FAB-02"])
    response = TestClient(app_a).get("/api/cases?limit=200", headers=headers)
    sites = {row["site_code"] for row in response.json()["items"]}
    assert "DE-BY" not in sites
    assert "US-TX" in sites or "BR-SP" in sites or "GB-ENG" in sites


def test_scenario_case_route_stays() -> None:
    headers = bearer_headers("RT-03")
    response = TestClient(app_a).get("/api/cases/PS000000016", headers=headers)
    assert response.status_code == 200
    assert response.json()["case"]["recipe_version"] == "R02"


def test_detail_refuses_the_other_site() -> None:
    headers = bearer_headers("RT-01", sites=["FAB-02"])
    listed = TestClient(app_a).get("/api/cases?site=DE-BY&limit=1", headers=bearer_headers("RT-01", sites=["FAB-01"]))
    case_id = listed.json()["items"][0]["id"]
    refused = TestClient(app_a).get(f"/api/cases/{case_id}/detail", headers=headers)
    assert refused.status_code == 403
    assert refused.json()["error_class"] == "site_forbidden"


def test_audit_search_is_not_a_correlation_id(api_headers) -> None:
    response = TestClient(app_a).get("/api/audit/search", headers=api_headers)
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert "items" in response.json()


def test_scrap_stays_an_estimate_and_unknown_cells_stay_empty(api_headers) -> None:
    client = TestClient(app_a)
    dashboard = client.get("/api/dashboard", headers=api_headers).json()
    assert dashboard["scrap"]["label"] == "estimate"
    assert dashboard["scrap"]["usd_per_defect"] == 1500
    assert dashboard["mtta"]["value"] is None
    assert dashboard["mtta"]["note"] == "Unknown"
    compare = client.get("/api/kpi/compare", headers=api_headers).json()
    assert all(cell["value"] is None and cell["note"] == "Unknown" for cell in compare["cells"])
    assert compare["scrap_rate"]["label"] == "estimate"


def test_i18n_covers_navigation_labels(api_headers) -> None:
    client = TestClient(app_b)
    english = client.get("/api/i18n/en", headers=api_headers).json()["strings"]
    chinese = client.get("/api/i18n/zh-TW", headers=api_headers).json()["strings"]
    assert english["nav.scenarios"] == "Scenarios"
    assert chinese["nav.scenarios"]
    assert "R02" not in chinese["nav.scenarios"]


def test_flags_and_genealogy_flag(api_headers) -> None:
    client = TestClient(app_a)
    flags = client.get("/api/flags", headers=api_headers)
    assert flags.status_code == 200
    assert flags.json()["flags"]["scenario_tabs"] is True
    genealogy = client.get("/api/lots/L00000000/genealogy", headers=api_headers)
    assert genealogy.status_code == 200
    steps = genealogy.json()["steps"]
    assert steps
    mismatched = [step for step in steps if step["recipe_mismatch"]]
    if mismatched:
        assert "differ" in mismatched[0]["flag"]


def test_graph_keeps_maps_to_inside_the_node_set(api_headers) -> None:
    body = TestClient(app_a).get("/api/graph/term.open_operational", headers=api_headers).json()
    nodes = body["nodes"]
    ids = {node["id"] for node in nodes}
    assert body["item_id"] == "term.open_operational"
    assert any(node["hop"] == 0 and node["kind"] for node in nodes)
    assert any(edge["type"] == "maps_to" and edge["from_id"] in ids and edge["to_id"] in ids for edge in body["edges"])
    assert len(nodes) <= 60


def test_fab_query_only_removes_sites(api_headers) -> None:
    client = TestClient(app_a)
    headers = bearer_headers("RT-01", sites=["FAB-02"])
    empty = client.get("/api/dashboard?fab=FAB-01", headers=headers).json()
    assert empty["open_cases"]["by_site"] == []
    narrowed = client.get("/api/dashboard?fab=FAB-02", headers=headers).json()
    sites = {row["site"] for row in narrowed["open_cases"]["by_site"]}
    assert "DE-BY" not in sites
    plain = client.get("/api/dashboard", headers=api_headers).json()
    assert plain["lot_scope"] == "all_lots"
    assert plain["scrap"]["label"] == "estimate"
    chamber_defects = sum(row["defect_count"] for row in plain["scrap_by_chamber"])
    assert chamber_defects == plain["scrap"]["defect_count"]


def test_partner_status_is_only_for_feeds(api_headers) -> None:
    client = TestClient(app_a)
    feeds = client.get("/api/partners/partner_feeds?status=REPLAY&limit=1", headers=api_headers)
    assert feeds.status_code == 200
    body = feeds.json()
    assert body["items"]
    assert all(row["processing_status"] == "REPLAY" for row in body["items"])
    assert body["total"] >= len(body["items"])
    full = client.get("/api/partners/partner_feeds?status=REPLAY&limit=200", headers=api_headers).json()
    assert full["total"] == body["total"]
    assert full["total"] == len(full["items"]) or full["total"] > 200
    refused = client.get("/api/partners/batch_runs?status=REPLAY", headers=api_headers)
    assert refused.status_code == 400
    assert refused.json()["error_class"] == "bad_request"


def test_audit_order_desc_puts_a_later_seq_first(api_headers) -> None:
    client = TestClient(app_a)
    ascending = client.get("/api/audit/search?limit=2", headers=api_headers)
    descending = client.get("/api/audit/search?order=desc&limit=2", headers=api_headers)
    assert ascending.status_code == 200
    assert descending.status_code == 200
    up = ascending.json()["items"]
    down = descending.json()["items"]
    if len(up) >= 2:
        assert up[0]["seq"] <= up[1]["seq"]
    if len(down) >= 2:
        assert down[0]["seq"] >= down[1]["seq"]
    bad = client.get("/api/audit/search?order=drop", headers=api_headers)
    assert bad.status_code == 400
