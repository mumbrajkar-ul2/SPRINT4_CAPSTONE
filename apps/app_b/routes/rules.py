"""GET /api/rules/at. Application B dated limit from the lake."""
from __future__ import annotations

from fastapi import APIRouter, Request

from apps.app_b.rules import resolver

router = APIRouter()


@router.get("/api/rules/at")
def get_rule_at(
    request: Request,
    rule_id: str,
    on_date: str,
    site_code: str | None = None,
    country_code: str | None = None,
    sales_region: str | None = None,
) -> dict[str, object]:
    del request
    if rule_id in {"rule.recipe_release.limit", "recipe_release"}:
        result = resolver.dated_limit(
            on_date=on_date,
            sales_region=sales_region,
            site_code=site_code,
            country_code=country_code,
        )
        pin = resolver.pin_meta()
        result["lake_version"] = pin["lake_version"]
        result["pin_sqlite_sha256"] = pin["pin_sqlite_sha256"]
        return result
    env = resolver.rule_at(
        rule_id,
        on_date,
        site_code=site_code,
        country_code=country_code,
        sales_region=sales_region,
    )
    pin = resolver.pin_meta()
    return {
        "ok": True,
        "verdict": env.get("verdict"),
        "limit_value": None,
        "citations": [item["id"] for item in env.get("items") or []],
        "items": env.get("items") or [],
        "lake_version": pin["lake_version"],
        "pin_sqlite_sha256": pin["pin_sqlite_sha256"],
    }
