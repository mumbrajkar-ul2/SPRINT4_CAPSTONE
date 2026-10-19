"""Recursive edge walks GQ-G01 through GQ-G12. Output is REAL."""
from __future__ import annotations

from lake_runtime import get_links


def _ids(env: dict) -> set[str]:
    return {item["id"] for item in env["items"]}


def test_gqg01_four_programs_and_test() -> None:
    env = get_links(
        "rule.recipe_release.limit",
        types=["implements", "tested_by", "conflicts_with"],
    )
    ids = _ids(env)
    assert "code.legacy_logic.priority" in ids
    assert "code.legacy_policy.js_allow" in ids
    assert "code.reconcile_legacy.java_total" in ids
    assert "code.shift_reconciliation.night_batch" in ids
    assert "test.rule.recipe_release.emea_2023" in ids


def test_gqg02_canonical_decisions() -> None:
    env = get_links("rule.recipe_release.limit", types=["governs"])
    ids = _ids(env)
    assert "decision.fd08.canonical_archive" in ids
    assert "decision.bo05.recipe_authority" in ids


def test_gqg03_recipe_mismatch() -> None:
    env = get_links("data.join.recipe_mismatch", types=["conflicts_with", "evidenced_by"])
    ids = _ids(env)
    assert "term.recipe_revision_dispatch" in ids
    assert "term.recipe_revision_equipment" in ids
    assert "decision.bp1.recipe_mismatch" in ids


def test_gqg04_apac_supersedes() -> None:
    env = get_links("rule.recipe_release.limit.v2026.apac", types=["supersedes"], direction="outgoing")
    ids = _ids(env)
    assert "rule.recipe_release.limit.v2025.apac" in ids
    assert "rule.recipe_release.limit.v2024.apac" in ids
    assert "rule.recipe_release.limit.v2023.apac" in ids
    assert "rule.recipe_release.limit.v2022.apac" in ids


def test_gqg05_js_depends_on_archive() -> None:
    env = get_links("data.contract.decision_policies_archive", types=["depends_on"])
    assert "code.legacy_policy.js_allow" in _ids(env)


def test_gqg06_open_words() -> None:
    env = get_links("term.open_operational", types=["maps_to"])
    ids = _ids(env)
    for word in (
        "term.local.review",
        "term.local.hold",
        "term.local.under_review",
        "term.local.open",
        "term.local.escalated",
        "term.local.reopened",
        "term.local.queued",
        "term.local.processing",
        "term.local.engineering_review",
    ):
        assert word in ids
    night = get_links("term.open_operational", types=["implements", "maps_to"])
    assert "rule.open_flag.impl.night_batch" in _ids(night)


def test_gqg07_impact_2026_apac() -> None:
    env = get_links(
        "rule.recipe_release.limit.v2026.apac",
        types=["implements", "tested_by", "depends_on", "governs", "maps_to"],
        depth=3,
    )
    ids = _ids(env)
    assert "code.legacy_policy.js_allow" in ids
    assert "test.rule.recipe_release.apac_2026" in ids
    assert "decision.fd08.canonical_archive" in ids
    assert "term.sales_region" in ids


def test_gqg08_site_to_archive_family() -> None:
    env = get_links("map.site.IN-BLR", types=["maps_to"])
    ids = _ids(env)
    assert "term.country_code" in ids
    assert "term.sales_region" in ids
    assert "rule.recipe_release.limit" in ids


def test_gqg09_injection_evidence() -> None:
    env = get_links("rule.untrusted_text.block", types=["evidenced_by"])
    ids = _ids(env)
    for locator in (
        "data.injection.partner_feeds",
        "data.injection.bundled_events",
        "data.injection.emails",
        "data.injection.source_documents",
        "data.injection.html",
        "data.injection.evidence_payloads",
    ):
        assert locator in ids


def test_gqg10_no_parent_lot_edge() -> None:
    env = get_links("term.lot_genealogy", types=["conflicts_with", "evidenced_by"])
    ids = _ids(env)
    assert "data.missing.lot_genealogy" in ids
    assert not any("parent" in item_id for item_id in ids)


def test_gqg11_incident_owner_unknown() -> None:
    env = get_links("decision.inc_2025_014", types=["evidenced_by"])
    ids = _ids(env)
    assert "data.incident.inc_2025_014" in ids
    owners = {item["owner"] for item in env["items"] if item["id"] == "decision.inc_2025_014"}
    assert owners == {"unknown"}


def test_gqg12_join_conflicts_overlap_not_open() -> None:
    env = get_links("rule.night_batch.join_multiply", types=["conflicts_with", "implements"])
    ids = _ids(env)
    assert "rule.policy.overlap_or_invalid" in ids
    conflict_edges = [e for e in env["edges"] if e["type"] == "conflicts_with"]
    assert not any(
        {e["from_id"], e["to_id"]} == {"rule.open_flag.impl.night_batch", "rule.open_closed.operational"}
        for e in conflict_edges
    )
