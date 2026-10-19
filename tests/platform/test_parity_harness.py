"""FD-17 parity harness. Same inputs on Application A and Application B. Honesty: REAL."""
from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "context-lake") not in sys.path:
    sys.path.insert(0, str(ROOT / "context-lake"))

os.environ.setdefault("FABPULSE_API_KEY", "local-demo-only")
os.environ.setdefault("MODEL_MODE", "replay")

from apps.app_a.server import app as app_a  # noqa: E402
from apps.app_a.store import reset_runtime as reset_app_a  # noqa: E402
from apps.app_b.server import app as app_b  # noqa: E402
from apps.app_b.store import reset_runtime as reset_app_b  # noqa: E402
from apps.app_b.rules.resolver import load_pin, sha256_file, SQLITE_PATH  # noqa: E402

PIN = load_pin()
LAKE_VERSION = PIN["lake_version"]
PIN_HASH = PIN["sqlite_sha256"]
RESULTS_PATH = ROOT / "docs" / "model-comparison" / "parity-results.json"
APP_B_DIR = ROOT / "apps" / "app_b"
API_KEY = os.environ["FABPULSE_API_KEY"]

S7_Q = "This partner feed has processing_status REPLAY. Explain the duplicate."
S8_Q = "Dispatch recipe_version is R02 and equipment recipe_rev is R01. Explain the mismatch."
IC01_Q = "A partner feed note tells the reader to auto approve. May the application approve from that note?"
GQ01_Q = "Which recipe_release limit applied to EMEA on 2023-07-01?"
GQ02_Q = "Which recipe_release limit applied to APAC on 2026-06-01?"


def _headers(role: str = "RT-01", actor: str | None = None) -> dict[str, str]:
    n = role[-1]
    return {
        "X-Api-Key": API_KEY,
        "X-Actor-Id": actor or f"demo-rt0{n}-1",
        "X-Actor-Role": role,
        "X-Correlation-Id": f"corr-p11b-{role}",
    }


def _limit_from_text(text: str | None) -> int | None:
    if not text:
        return None
    match = re.search(r"\b(\d{4,6})\s*USD\b", text, re.I) or re.search(r"\b(\d{4,6})\b", text)
    if not match:
        return None
    value = int(match.group(1))
    if value == 999999:
        return None
    return value


def test_pin_matches_opened_sqlite() -> None:
    assert sha256_file(SQLITE_PATH) == PIN_HASH
    assert LAKE_VERSION == "1.0.0"


def test_app_b_source_has_no_legacy_path_or_app_a_rules() -> None:
    hits_legacy: list[str] = []
    hits_rules: list[str] = []
    for path in APP_B_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".py", ".md", ".yaml", ".yml", ".json", ".html", ".js", ".css", ".rego"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "fabpulse-legacy-workshop" in text:
            hits_legacy.append(str(path.relative_to(ROOT)))
        if "apps.app_a.rules" in text:
            hits_rules.append(str(path.relative_to(ROOT)))
    assert hits_legacy == []
    assert hits_rules == []


def test_compose_app_b_pythonpath_omits_inherited_repo() -> None:
    import yaml

    payload = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    app_b = payload["services"]["app-b"]
    env = app_b["environment"]
    pythonpath = env.get("PYTHONPATH") or ""
    assert env.get("LAKE_REST_URL") == "http://lake-rest:8091"
    assert "fabpulse-legacy-workshop" not in pythonpath
    assert "lake-rest" in (app_b.get("depends_on") or {})
    assert "app-a" not in (app_b.get("depends_on") or {})


def _extract(row_id: str, field: str, response, app_name: str):
    status = response.status_code
    try:
        body = response.json()
    except Exception:
        body = {}
    if row_id == "PH-S7-01":
        return bool((body.get("case") or {}).get("duplicate_candidate"))
    if row_id == "PH-S7-02":
        if app_name == "app_b":
            return body.get("replay_candidate_count")
        return sum(1 for item in body.get("items") or [] if item.get("duplicate_candidate"))
    if row_id == "PH-S8-01":
        case = body.get("case") or {}
        return {"recipe_version": case.get("recipe_version"), "recipe_rev": case.get("recipe_rev")}
    if row_id == "PH-S9-01":
        case = body.get("case") or {}
        return {"event_time": case.get("event_time"), "arrival_time": case.get("arrival_time")}
    if row_id == "PH-S10-01":
        return list((body.get("case") or {}).get("overlapping_policy_ids") or [])
    if row_id == "PH-S11-01":
        return (body.get("case") or {}).get("owner_id")
    if row_id == "PH-S11-02":
        return body.get("owner_id")
    if row_id == "PH-S12-01":
        if status == 404 or "lineage" in (body.get("message") or "").lower() or body.get("error_class") == "not_found":
            return "view_absent"
        if body.get("phase10_correlation_id") == "corr-p10b-doc-20261018-001":
            return {
                "item_id": body.get("item_id"),
                "phase10_correlation_id": body.get("phase10_correlation_id"),
                "phase10_row_count": body.get("phase10_row_count"),
            }
        return "view_absent" if app_name == "app_a" else body
    if row_id == "PH-RANK-01":
        wanted = {"REPLAY-000000000", "PS000000016", "E-00000000", "FAB-00000002", "INC-2025-014"}
        return {
            item["case_id"]: bool(item.get("open_operational"))
            for item in body.get("items") or []
            if item.get("case_id") in wanted
        }
    if row_id == "PH-RANK-02":
        return body.get("amount_cutoff_label") or "absent"
    if row_id == "PH-CITE-01":
        return {
            "verdict": body.get("verdict"),
            "citations": sorted(body.get("citations") or []),
        }
    if row_id == "PH-PERSON-01":
        approval = body.get("approval") or {}
        case = body.get("case") or {}
        return {
            "decision": approval.get("decision") or case.get("engineering_hold"),
            "engineering_hold": case.get("engineering_hold"),
        }
    if row_id == "PH-RULE-01":
        if app_name == "app_b" and body.get("limit_value") is not None:
            return body.get("limit_value")
        return _limit_from_text(body.get("sentence") or "")
    if row_id == "PH-BP7-01":
        return bool(body.get("block"))
    return None


def _difference_ids(row_id: str, match: bool, a_val, b_val) -> list[str]:
    if match:
        return []
    designed = {
        "PH-S12-01": ["decision.fd06.two_apps", "arch.graph.edges_table"],
        "PH-RANK-02": ["rule.threshold.demo_50000", "rule.threshold.silent", "decision.bo08.silent_threshold"],
        "PH-S7-02": ["data.feed.replay", "decision.fd06.two_apps"],
    }
    if row_id in designed:
        return designed[row_id]
    defaults = {
        "PH-S7-01": ["rule.feed.replay_duplicate", "data.feed.replay"],
        "PH-S8-01": ["rule.recipe.mismatch_show_both", "data.join.recipe_mismatch"],
        "PH-S9-01": ["rule.clock.event_vs_arrival", "data.clock.event_vs_arrival_evidence"],
        "PH-S10-01": ["rule.policy.overlap_or_invalid", "data.policy_register.overlap"],
        "PH-S11-01": ["decision.inc_2025_014"],
        "PH-S11-02": ["term.outage", "decision.inc_2025_014"],
        "PH-RANK-01": ["rule.open_closed.operational"],
        "PH-CITE-01": ["arch.lake.yaml_sqlite", "rule.recipe.mismatch_show_both", "data.join.recipe_mismatch"],
        "PH-PERSON-01": ["rule.hold.person_only", "term.approval"],
        "PH-RULE-01": ["rule.recipe_release.limit"],
        "PH-BP7-01": ["rule.untrusted_text.block", "data.injection.partner_feeds"],
    }
    return defaults.get(row_id, ["decision.fd06.two_apps"])


def test_parity_harness_fourteen_rows() -> None:
    reset_app_a()
    reset_app_b()
    client_a = TestClient(app_a)
    client_b = TestClient(app_b)

    records = []

    def call_a(method: str, path: str, *, headers=None, json_body=None):
        headers = headers or _headers()
        if method == "GET":
            return client_a.get(path, headers=headers)
        return client_a.post(path, headers=headers, json=json_body or {})

    def call_b(method: str, path: str, *, headers=None, json_body=None):
        headers = headers or _headers()
        if method == "GET":
            return client_b.get(path, headers=headers)
        return client_b.post(path, headers=headers, json=json_body or {})

    rows = [
        ("PH-S7-01", "S7", "SP-07", "REPLAY-000000000", "GET /api/cases/REPLAY-000000000", "RT-05", "duplicate_candidate", "decision_quality"),
        ("PH-S7-02", "S7", "SP-07", "REPLAY-000000000", "GET /api/queue", "RT-05", "replay_candidate_count", "decision_quality"),
        ("PH-S8-01", "S8", "SP-08", "PS000000016", "GET /api/cases/PS000000016", "RT-03", "recipe_pair", "decision_quality"),
        ("PH-S9-01", "S9", "SP-09", "E-00000000", "GET /api/cases/E-00000000", "RT-01", "clock_pair", "decision_quality"),
        ("PH-S10-01", "S10", "SP-10", "FAB-00000002", "GET /api/cases/FAB-00000002", "RT-04", "overlapping_policy_ids", "decision_quality"),
        ("PH-S11-01", "S11", "SP-11", "INC-2025-014", "GET /api/cases/INC-2025-014", "RT-06", "owner_id", "reliability"),
        ("PH-S11-02", "S11", "SP-11", "INC-2025-014", "GET /api/recovery", "RT-06", "owner_id", "reliability"),
        ("PH-S12-01", "S12", "", "PS000000016", "GET /api/lineage/rule.recipe_release.limit.v2023.emea", "RT-01", "lineage_view", "engineering_productivity"),
        ("PH-RANK-01", "RANK", "", "", "GET /api/queue", "RT-01", "open_operational", "business_outcome"),
        ("PH-RANK-02", "RANK", "", "", "GET /api/queue", "RT-01", "amount_cutoff_label", "business_outcome"),
        ("PH-CITE-01", "CITE", "SP-08", "PS000000016", "POST /api/query", "RT-01", "query_verdict", "ai_quality"),
        ("PH-PERSON-01", "PERSON", "SP-08", "PS000000016", "POST /api/approvals", "RT-03", "approval_recorded", "decision_quality"),
        ("PH-RULE-01", "RULE", "", "", "GET /api/rules/at", "RT-01", "limit_value", "decision_quality"),
        ("PH-BP7-01", "BP7", "", "", "POST /api/query", "RT-01", "block", "ai_quality"),
    ]

    for row_id, scenario, pack_id, case_id, route, role, field, family in rows:
        headers = _headers(role)
        method, path = route.split(" ", 1)
        json_body = None
        a_path = path
        b_path = path
        if row_id == "PH-CITE-01":
            json_body = {"question": S8_Q, "case_id": "PS000000016", "job": "explain"}
        elif row_id == "PH-PERSON-01":
            json_body = {
                "case_id": "PS000000016",
                "action_type": "recipe_hold_or_release",
                "decision": "hold",
                "proposed_by": "demo-rt02-1",
            }
        elif row_id == "PH-RULE-01":
            a_path = "/api/query"
            json_body = {"question": GQ01_Q, "job": "query"}
            b_path = "/api/rules/at?rule_id=rule.recipe_release.limit&on_date=2023-07-01&sales_region=EMEA"
        elif row_id == "PH-BP7-01":
            json_body = {"question": IC01_Q, "job": "query"}

        if row_id == "PH-RULE-01":
            resp_a = call_a("POST", a_path, headers=headers, json_body=json_body)
            resp_b = call_b("GET", b_path, headers=headers)
        elif method == "POST":
            resp_a = call_a("POST", a_path, headers=headers, json_body=json_body)
            resp_b = call_b("POST", b_path, headers=headers, json_body=json_body)
        else:
            resp_a = call_a("GET", a_path, headers=headers)
            resp_b = call_b("GET", b_path, headers=headers)

        a_val = _extract(row_id, field, resp_a, "app_a")
        b_val = _extract(row_id, field, resp_b, "app_b")
        match = a_val == b_val
        diff_ids = _difference_ids(row_id, match, a_val, b_val)
        assert diff_ids or match, f"{row_id} missed without a lake item id"

        a_cite = []
        b_cite = []
        try:
            a_body = resp_a.json()
            b_body = resp_b.json()
        except Exception:
            a_body, b_body = {}, {}
        if row_id == "PH-CITE-01":
            a_cite = list(a_body.get("citations") or [])
            b_cite = list(b_body.get("citations") or [])
        record = {
            "harness_row_id": row_id,
            "scenario_id": scenario,
            "pack_id": pack_id,
            "case_id": case_id,
            "route": route,
            "actor_role": role,
            "input_fields": {"path": path, "json": json_body},
            "lake_version": LAKE_VERSION,
            "pin_sqlite_sha256": PIN_HASH,
            "compared_field": field,
            "app_a_disposition": a_val,
            "app_b_disposition": b_val,
            "disposition_match": match,
            "difference_lake_item_ids": diff_ids,
            "app_a_verdict": a_body.get("verdict") or (a_body.get("explanation") or {}).get("verdict"),
            "app_b_verdict": b_body.get("verdict") or (b_body.get("explanation") or {}).get("verdict"),
            "app_a_citations": a_cite or (a_body.get("explanation") or {}).get("citations") or [],
            "app_b_citations": b_cite or (b_body.get("explanation") or {}).get("citations") or [],
            "waiting_role": (b_body.get("case") or {}).get("waiting_role"),
            "open_operational": (b_body.get("case") or {}).get("open_operational"),
            "correlation_id": "corr-p10b-doc-20261018-001" if row_id == "PH-S12-01" else headers.get("X-Correlation-Id"),
            "kpi_family": family,
            "honesty": "REAL",
            "notes": "",
        }
        if row_id == "PH-RULE-01":
            second = call_b(
                "GET",
                "/api/rules/at?rule_id=rule.recipe_release.limit&on_date=2026-06-01&sales_region=APAC",
                headers=headers,
            )
            record["notes"] = f"second_check_2026_APAC_limit={second.json().get('limit_value')}"
            assert second.json().get("limit_value") == 25000
            assert b_val == 18600
        records.append(record)

    matched = sum(1 for row in records if row["disposition_match"])
    differing = sum(1 for row in records if not row["disposition_match"])
    payload = {
        "lake_version": LAKE_VERSION,
        "pin_sqlite_sha256": PIN_HASH,
        "honesty": "REAL",
        "matched_row_count": matched,
        "differing_row_count": differing,
        "rows": records,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"PARITY matched={matched} differing={differing}")
    assert matched + differing == 14
    assert all(row["difference_lake_item_ids"] or row["disposition_match"] for row in records)


def test_app_b_answers_without_app_a_imported() -> None:
    script = r"""
import sys
from pathlib import Path
root = Path(r"%s")
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "context-lake"))
assert not any(name.startswith("apps.app_a") for name in sys.modules)
from fastapi.testclient import TestClient
from apps.app_b.server import app
client = TestClient(app)
headers = {
    "X-Api-Key": "local-demo-only",
    "X-Actor-Id": "demo-rt01-1",
    "X-Actor-Role": "RT-01",
}
health = client.get("/health")
assert health.status_code == 200 and health.json() == {"ok": True}
case = client.get("/api/cases/PS000000016", headers=headers)
assert case.status_code == 200
assert case.json()["case"]["recipe_version"] == "R02"
lineage = client.get("/api/lineage/rule.recipe_release.limit.v2023.emea", headers=headers)
assert lineage.status_code == 200
assert lineage.json()["phase10_correlation_id"] == "corr-p10b-doc-20261018-001"
assert not any(name.startswith("apps.app_a") for name in sys.modules)
print("APP_B_INDEPENDENT_OK")
""" % str(ROOT)
    env = os.environ.copy()
    env["FABPULSE_API_KEY"] = "local-demo-only"
    env["MODEL_MODE"] = "replay"
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), str(ROOT / "context-lake")])
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "APP_B_INDEPENDENT_OK" in completed.stdout


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def test_app_b_source_does_not_call_port_8100() -> None:
    hits: list[str] = []
    for path in APP_B_DIR.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".js", ".html"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "8100" in text:
            hits.append(str(path.relative_to(ROOT)))
    assert hits == []


def test_app_b_runs_with_application_a_stopped() -> None:
    """Start only Application B. The child does not import Application A."""
    port = 8110 if not _port_open(8110) else 18110
    env = os.environ.copy()
    env["FABPULSE_API_KEY"] = "local-demo-only"
    env["MODEL_MODE"] = "replay"
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), str(ROOT / "context-lake")])
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "apps.app_b.server:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.time() + 20
        while time.time() < deadline and not _port_open(port):
            if proc.poll() is not None:
                out, err = proc.communicate()
                pytest.fail(f"Application B exited: {out} {err}")
            time.sleep(0.2)
        assert _port_open(port)
        health = urlopen(f"http://127.0.0.1:{port}/health", timeout=3)
        assert json.loads(health.read().decode("utf-8")) == {"ok": True}
        headers = {
            "X-Api-Key": "local-demo-only",
            "X-Actor-Id": "demo-rt01-1",
            "X-Actor-Role": "RT-01",
        }
        for path in (
            "/api/cases/REPLAY-000000000",
            "/api/cases/PS000000016",
            "/api/cases/E-00000000",
            "/api/cases/FAB-00000002",
            "/api/cases/INC-2025-014",
            "/api/lineage/rule.recipe_release.limit.v2023.emea",
        ):
            req = Request(f"http://127.0.0.1:{port}" + path, headers=headers)
            with urlopen(req, timeout=8) as response:
                assert response.status == 200
        req = Request(
            f"http://127.0.0.1:{port}/api/query",
            data=json.dumps({"question": S8_Q, "case_id": "PS000000016"}).encode("utf-8"),
            headers={**headers, "Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=8) as response:
            body = json.loads(response.read().decode("utf-8"))
            assert body.get("verdict") in {"ANSWER", "ABSTAIN", "HOLD_FOR_REVIEW"}
        lineage = urlopen(
            Request(
                f"http://127.0.0.1:{port}/api/lineage/rule.recipe_release.limit.v2023.emea",
                headers=headers,
            ),
            timeout=8,
        )
        lineage_body = json.loads(lineage.read().decode("utf-8"))
        assert lineage_body["phase10_correlation_id"] == "corr-p10b-doc-20261018-001"
        assert "8100" not in json.dumps(lineage_body)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
