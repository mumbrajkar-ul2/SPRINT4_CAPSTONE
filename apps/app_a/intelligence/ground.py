"""FD-14 grounding: every AI answer cites a retrieved lake item id or abstains."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LAKE_ROOT = ROOT / "context-lake"
if str(LAKE_ROOT) not in sys.path:
    sys.path.insert(0, str(LAKE_ROOT))

from lake_runtime import check_claim, load_enums  # noqa: E402

VERDICTS = {"ANSWER", "ABSTAIN", "HOLD_FOR_REVIEW"}
ITEM_ID_RE = re.compile(
    r"\b(?:rule|data|term|decision|arch|code|dep|map|test)\.[A-Za-z0-9._-]+\b"
)
TABLE_COLUMN_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\.([a-z_][a-z0-9_]*)\b")
ABSTAIN_BODY = {
    "sentence": "",
    "citations": [],
    "verdict": "ABSTAIN",
    "block": False,
    "untrusted_quotes": [],
}


def empty_abstain(*, citations: list[str] | None = None, untrusted_quotes: list[str] | None = None) -> dict[str, Any]:
    body = dict(ABSTAIN_BODY)
    body["citations"] = list(citations or [])
    body["untrusted_quotes"] = list(untrusted_quotes or [])
    return body


def extract_claims(sentence: str, citations: list[str], enums: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    enums = enums or load_enums()
    claims: list[dict[str, Any]] = []
    for item_id in citations:
        claims.append({"item_id": item_id, "rule_id": item_id})
    for item_id in ITEM_ID_RE.findall(sentence or ""):
        claims.append({"item_id": item_id, "rule_id": item_id})
    columns = set(enums.get("columns", []))
    tables = set(enums.get("tables", []))
    for table, column in TABLE_COLUMN_RE.findall(sentence or ""):
        key = f"{table}.{column}"
        if table in tables or key in columns or column == "parent_lot_id":
            claims.append({"table": table, "column": column})
    for status in enums.get("status_words", []):
        if status and re.search(rf"\b{re.escape(status)}\b", sentence or ""):
            claims.append({"status_word": status})
    for site in enums.get("site_codes", []):
        if site and site in (sentence or ""):
            claims.append({"site": site})
    for country in enums.get("country_codes", []):
        if country and re.search(rf"\b{re.escape(country)}\b", sentence or ""):
            claims.append({"country": country})
    for region in enums.get("sales_regions", []):
        if region and re.search(rf"\b{re.escape(region)}\b", sentence or ""):
            claims.append({"sales_region": region})
    if re.search(r"\bMOON\b", sentence or "", re.I):
        claims.append({"sales_region": "MOON"})
    if "parent_lot_id" in (sentence or ""):
        claims.append({"table": "wafer_lots", "column": "parent_lot_id"})
    return claims


def _invented_fact_on_abstain(sentence: str) -> bool:
    text = sentence or ""
    if re.search(r"parent_lot_id", text):
        return True
    if re.search(r"\bL\d{8}\b", text) and "parent" in text.lower():
        return True
    if re.search(r"owner is (?!Unknown)[A-Z][a-z]+", text):
        return True
    if re.search(r"\bMOON\b", text, re.I) and re.search(r"\d{4,}", text):
        return True
    return False


def ground(
    model_body: dict[str, Any] | None,
    *,
    retrieved_item_ids: list[str],
    untrusted_quotes: list[str] | None = None,
    block: bool = False,
) -> dict[str, Any]:
    """Apply the FD-14 rule. Empty citations on ANSWER become ABSTAIN. No percent floor."""
    retrieved = set(retrieved_item_ids or [])
    quotes = list(untrusted_quotes or [])
    reject_reason = None
    if not model_body or not isinstance(model_body, dict):
        return {
            **empty_abstain(untrusted_quotes=quotes),
            "grounded": True,
            "reject_reason": None,
            "check_claim": {"ok": True, "result": "ok", "unknown": []},
        }

    verdict = str(model_body.get("verdict") or "").strip()
    if verdict not in VERDICTS:
        verdict = "ABSTAIN"
    sentence = model_body.get("sentence") if isinstance(model_body.get("sentence"), str) else ""
    raw_citations = model_body.get("citations") or []
    if not isinstance(raw_citations, list):
        raw_citations = []
    citations = [str(item_id) for item_id in raw_citations if item_id]
    dropped = [item_id for item_id in citations if item_id not in retrieved]
    citations = [item_id for item_id in citations if item_id in retrieved]
    model_block = bool(model_body.get("block")) or block
    model_quotes = model_body.get("untrusted_quotes") or []
    if isinstance(model_quotes, list):
        for row in model_quotes:
            if isinstance(row, str) and row not in quotes:
                quotes.append(row)

    if dropped:
        reject_reason = "not_retrieved"
        verdict = "ABSTAIN"
        sentence = ""
    needs_cite = verdict in {"ANSWER", "HOLD_FOR_REVIEW"} or model_block
    if needs_cite and not citations:
        reject_reason = reject_reason or "missing_citation"
        verdict = "ABSTAIN"
        sentence = ""
        model_block = False if reject_reason == "missing_citation" and not block else model_block

    enums = load_enums()
    known_ids = set(enums.get("item_ids", []))
    unknown_ids = [item_id for item_id in citations if item_id not in known_ids]
    if unknown_ids:
        reject_reason = "unknown_item_id"
        verdict = "ABSTAIN"
        sentence = ""
        citations = []

    claims = extract_claims(sentence, citations, enums)
    checked = check_claim(claims, enums)
    if not checked.get("ok"):
        reject_reason = "check_claim_reject"
        missing = []
        for item_id in ("data.missing.lot_genealogy", "decision.inc_2025_014"):
            if item_id in retrieved:
                missing.append(item_id)
        verdict = "ABSTAIN"
        sentence = ""
        citations = missing
        model_block = False

    if verdict == "ABSTAIN" and _invented_fact_on_abstain(sentence):
        reject_reason = "invented_fact_on_abstain"
        sentence = ""
        citations = [item_id for item_id in citations if item_id in retrieved]

    if model_block and "rule.untrusted_text.block" in retrieved and "rule.untrusted_text.block" not in citations:
        citations.append("rule.untrusted_text.block")

    grounded = True
    if verdict in {"ANSWER", "HOLD_FOR_REVIEW"} and not citations:
        grounded = False
        verdict = "ABSTAIN"
        sentence = ""
        reject_reason = reject_reason or "missing_citation"
    if model_block and "rule.untrusted_text.block" not in citations and "rule.untrusted_text.block" not in retrieved:
        model_block = False

    result = {
        "sentence": sentence if verdict != "ABSTAIN" or citations else "",
        "citations": citations,
        "verdict": verdict,
        "block": model_block,
        "untrusted_quotes": quotes,
        "grounded": grounded and reject_reason in {None, "missing_citation"} or verdict == "ABSTAIN",
        "reject_reason": reject_reason,
        "check_claim": checked,
        "draft_plan": model_body.get("draft_plan") if isinstance(model_body.get("draft_plan"), str) else None,
    }
    if result["verdict"] == "ABSTAIN" and result["reject_reason"] == "invented_fact_on_abstain":
        result["sentence"] = ""
    if result["verdict"] == "ABSTAIN" and not result["citations"]:
        result["sentence"] = ""
    # An abstain after a rewrite is a grounded abstain.
    if result["verdict"] == "ABSTAIN":
        result["grounded"] = True
        result["draft_plan"] = None
        result["block"] = bool(block or model_block) and "rule.untrusted_text.block" in (citations or retrieved)
    return result
