"""Write sibling rule-card YAML for RC-01 through RC-25."""
from __future__ import annotations

from .common import (
    ARCHIVE_LIMITS,
    LAKE_ROOT,
    dump_yaml,
    load_register,
    source_for_inherited,
    source_for_workspace,
)

CARDS_DIR = LAKE_ROOT / "items" / "rules"


def _card(
    *,
    id: str,
    statement: str,
    source: dict,
    authority: str,
    owner: str,
    policy_status: str,
    claim: str,
    trust: str,
    honesty: str,
    inputs: list,
    decision_table: list,
    tests: list,
    observed_implementations: list,
) -> dict:
    return {
        "id": id,
        "kind": "business_rule",
        "statement": statement,
        "inputs": inputs,
        "decision_table": decision_table,
        "authority": authority,
        "owner": owner,
        "policy_status": policy_status,
        "tests": tests,
        "observed_implementations": observed_implementations,
        "source": source,
        "claim": claim,
        "trust": trust,
        "lake_version": "1.0.0",
        "item_status": "accepted",
        "honesty": honesty,
    }


def generate_cards() -> list[str]:
    register = load_register()
    archive = source_for_inherited("contracts/decision-policies-archive.json", register)
    js = source_for_inherited("legacy_js/legacy_policy.js", register, lines="4-5")
    py = source_for_inherited("app/legacy_logic.py", register, lines="2-5")
    java = source_for_inherited("legacy_java/ReconcileLegacy.java", register, lines="12")
    batch = source_for_inherited("legacy_batch/shift_reconciliation.py", register, lines="8-14")
    tracker = source_for_workspace("Decision_Tracker.md")
    mapping = source_for_workspace("docs/11-data-context/mapping-design.md")
    inject = source_for_workspace("docs/11-data-context/injection-corpus-design.md")
    ent = source_for_inherited(
        "data/enterprise_legacy.sqlite3", register, locator="policy_register.threshold"
    )

    ids: list[str] = []

    def put(card: dict) -> None:
        dump_yaml(CARDS_DIR / f"{card['id']}.card.yaml", card)
        ids.append(card["id"])

    version_rows = []
    for year, region, start, end, limit in ARCHIVE_LIMITS:
        version_rows.append(
            {
                "when": {
                    "sales_region": region,
                    "on_date_from": start,
                    "on_date_to": end,
                },
                "then": {"limit": limit, "currency": "USD"},
            }
        )
    rc01_tests = [
        {"given": {"amount": 18000, "sales_region": "EMEA", "on_date": "2023-07-01"}, "expect": {"within_limit": True, "limit": 18600}},
        {"given": {"amount": 19000, "sales_region": "EMEA", "on_date": "2023-07-01"}, "expect": {"within_limit": False, "limit": 18600}},
        {"given": {"amount": 25000, "sales_region": "APAC", "on_date": "2026-06-01"}, "expect": {"within_limit": True, "limit": 25000}},
        {"given": {"amount": 25001, "sales_region": "APAC", "on_date": "2026-06-01"}, "expect": {"within_limit": False, "limit": 25000}},
        {"given": {"amount": 27200, "sales_region": "AMER", "on_date": "2026-06-01"}, "expect": {"within_limit": True, "limit": 27200}},
    ]
    for year, region, start, end, limit in ARCHIVE_LIMITS:
        mid = f"{year}-06-01"
        rc01_tests.append(
            {
                "given": {"amount": limit, "sales_region": region, "on_date": mid},
                "expect": {"within_limit": True, "limit": limit},
            }
        )
        rc01_tests.append(
            {
                "given": {"amount": limit + 1, "sales_region": region, "on_date": mid},
                "expect": {"within_limit": False, "limit": limit},
            }
        )

    put(
        _card(
            id="rule.recipe_release.limit",
            statement="Canonical recipe_release limit from the archive JSON.",
            source=archive,
            authority="policy_archive",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="REAL",
            inputs=[
                {"name": "amount", "term": "term.recipe_release_limit"},
                {"name": "sales_region", "term": "term.sales_region"},
                {"name": "on_date", "term": "term.policy"},
            ],
            decision_table=version_rows,
            tests=rc01_tests,
            observed_implementations=[{"id": "rule.recipe_release.limit.impl.js"}],
        )
    )
    put(
        _card(
            id="rule.recipe_release.no_match",
            statement="No archive row routes to HOLD_FOR_REVIEW.",
            source=archive,
            authority="policy_archive",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="REAL",
            inputs=[{"name": "sales_region", "term": "term.sales_region"}, {"name": "on_date", "term": "term.policy"}],
            decision_table=[{"when": {"archive_match": False}, "then": {"route": "HOLD_FOR_REVIEW"}}],
            tests=[
                {"given": {"amount": 100, "country": "IN", "on_date": "2026-01-01", "derived_sales_region": None}, "expect": {"route": "HOLD_FOR_REVIEW"}},
                {"given": {"amount": 100, "sales_region": "APAC", "on_date": "2021-06-01"}, "expect": {"route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[{"id": "rule.recipe_release.limit.impl.js_default"}],
        )
    )
    put(
        _card(
            id="rule.policy.overlap_or_invalid",
            statement="Overlap or invalid interval routes to HOLD_FOR_REVIEW.",
            source=ent,
            authority="policy_archive",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="REAL",
            inputs=[{"name": "country", "term": "term.country_code"}, {"name": "on_date", "term": "term.policy"}],
            decision_table=[
                {"when": {"overlap": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
                {"when": {"invalid_interval": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[
                {"given": {"country": "US", "on_date": "2026-06-01", "family": "FAB-RULE"}, "expect": {"route": "HOLD_FOR_REVIEW"}},
                {"given": {"policy_id": "POL-0039"}, "expect": {"route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.recipe_release.limit.impl.js",
            statement="JavaScript allows archive limit times 1.05.",
            source=js,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="REAL",
            inputs=[{"name": "amount", "term": "term.recipe_release_limit"}, {"name": "sales_region", "term": "term.sales_region"}],
            decision_table=[
                {"when": {"implementation": "js"}, "then": {"within_limit": "amount <= limit * 1.05"}},
                {"when": {"archive_match": False}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[
                {"given": {"amount": 15700, "region": "APAC", "year": 2022}, "expect": {"implementation_within_limit": True, "canonical_within_limit": False}},
                {"given": {"amount": 27000, "region": "APAC", "year": 2026}, "expect": {"implementation_within_limit": False, "canonical_within_limit": False}},
            ],
            observed_implementations=[{"path": "legacy_js/legacy_policy.js", "lines": "4-5"}],
        )
    )
    put(
        _card(
            id="rule.recipe_release.limit.impl.js_default",
            statement="JavaScript missing year or region returns 999999 on this implementation only.",
            source=js,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="REAL",
            inputs=[{"name": "region", "term": "term.country_code"}],
            decision_table=[
                {"when": {"implementation": "js_default"}, "then": {"implementation_limit": 999999}},
                {"when": {"canonical": True, "archive_match": False}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[
                {"given": {"amount": 100, "region": "IN", "year": 2026}, "expect": {"implementation_within_limit": True, "canonical_route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[{"path": "legacy_js/legacy_policy.js", "lines": "4"}],
        )
    )
    put(
        _card(
            id="rule.urgent.amount.impl.python",
            statement="Python urgent cutoff is 50000. Live policy is HOLD_FOR_REVIEW.",
            source=py,
            authority="unresolved",
            owner="unknown",
            policy_status="proposed",
            claim="verified_fact",
            trust="trusted_code",
            honesty="REAL",
            inputs=[{"name": "amount", "term": "term.recipe_release_limit"}],
            decision_table=[
                {"when": {"implementation": "python", "amount_gt": 50000}, "then": {"route": "URGENT"}},
                {"when": {"canonical": True, "archive_silent": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[
                {"given": {"status": "OPEN", "severity": "LOW", "amount": 50001}, "expect": {"implementation_route": "URGENT", "canonical_route": "HOLD_FOR_REVIEW"}},
                {"given": {"status": "OPEN", "severity": "LOW", "amount": 49999}, "expect": {"implementation_route": "QUEUE", "canonical_route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[{"path": "app/legacy_logic.py", "lines": "4"}],
        )
    )
    put(
        _card(
            id="rule.priority.closed.impl.python",
            statement="Python CLOSED returns archive. SME closed needs more.",
            source=py,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="n/a",
            inputs=[{"name": "status", "term": "term.closed_operational"}],
            decision_table=[
                {"when": {"implementation": "python", "status": "CLOSED"}, "then": {"route": "ARCHIVE"}},
                {"when": {"canonical": True, "engineering_action_unknown": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[
                {"given": {"status": "CLOSED"}, "expect": {"implementation_route": "ARCHIVE", "canonical_route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[{"path": "app/legacy_logic.py", "lines": "3"}],
        )
    )
    put(
        _card(
            id="rule.urgent.severity.impl.python",
            statement="Python CRITICAL returns urgent.",
            source=py,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="n/a",
            inputs=[{"name": "severity", "term": "term.case"}],
            decision_table=[
                {"when": {"implementation": "python", "severity": "CRITICAL"}, "then": {"route": "URGENT"}},
                {"when": {"canonical": True, "archive_silent": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[{"given": {"status": "OPEN", "severity": "CRITICAL", "amount": 1}, "expect": {"implementation_route": "URGENT"}}],
            observed_implementations=[{"path": "app/legacy_logic.py", "lines": "4"}],
        )
    )
    put(
        _card(
            id="rule.open_closed.operational",
            statement="REVIEW and HOLD are open. BO-06a.",
            source=tracker,
            authority="sme",
            owner="SME",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "status", "term": "term.open_operational"}],
            decision_table=[
                {"when": {"status": "REVIEW"}, "then": {"route": "OPEN"}},
                {"when": {"status": "HOLD"}, "then": {"route": "OPEN"}},
                {"when": {"status": "CLOSED", "engineering_action": "none", "final_disposition": True}, "then": {"route": "CLOSED_OPERATIONAL"}},
            ],
            tests=[
                {"given": {"status": "REVIEW"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "HOLD"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "UNDER_REVIEW"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "ESCALATED"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "REOPENED"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "OPEN"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "CLOSED", "engineering_action": "pending"}, "expect": {"route": "OPEN"}},
                {"given": {"status": "CLOSED", "final_disposition": True, "engineering_action": "none"}, "expect": {"route": "CLOSED_OPERATIONAL"}},
            ],
            observed_implementations=[{"id": "rule.open_flag.impl.night_batch"}],
        )
    )
    put(
        _card(
            id="rule.open_closed.finance_audit",
            statement="Three closure states. BO-06b unsigned.",
            source=tracker,
            authority="unresolved",
            owner="Business Owner",
            policy_status="proposed",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "question", "term": "term.closed_finance"}],
            decision_table=[{"when": {"mismatch": True}, "then": {"route": "HOLD_FOR_REVIEW"}}],
            tests=[
                {"given": {"operational_closed": True, "finance_booked_at": None, "question": "finance-closed"}, "expect": {"route": "HOLD_FOR_REVIEW"}},
                {"given": {"operational_closed": True, "audit_mark": None, "question": "audit-closed"}, "expect": {"route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.region.site_canonical",
            statement="Site is canonical. Country and sales region are derived.",
            source=mapping,
            authority="sme",
            owner="SME",
            policy_status="decided",
            claim="inference",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "site", "term": "term.site_code"}],
            decision_table=[
                {"when": {"site": "IN-BLR"}, "then": {"country": "IN", "sales_region": "APAC"}},
                {"when": {"site": "US-TX"}, "then": {"country": "US", "sales_region": "AMER"}},
                {"when": {"site": "DE-BY"}, "then": {"country": "DE", "sales_region": "EMEA"}},
                {"when": {"site": "GB-ENG"}, "then": {"country": "GB", "sales_region": "EMEA"}},
                {"when": {"site": "BR-SP"}, "then": {"country": "BR", "sales_region": "AMER"}},
                {"when": {"site": "JP-KN"}, "then": {"country": "JP", "sales_region": "APAC"}},
            ],
            tests=[
                {"given": {"site": "IN-BLR"}, "expect": {"country": "IN", "sales_region": "APAC"}},
                {"given": {"site": "US-TX"}, "expect": {"country": "US", "sales_region": "AMER"}},
                {"given": {"site": "DE-BY"}, "expect": {"country": "DE", "sales_region": "EMEA"}},
                {"given": {"site": "GB-ENG"}, "expect": {"country": "GB", "sales_region": "EMEA"}},
                {"given": {"site": "BR-SP"}, "expect": {"country": "BR", "sales_region": "AMER"}},
                {"given": {"site": "JP-KN"}, "expect": {"country": "JP", "sales_region": "APAC"}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.region.specificity",
            statement="Most specific scope wins: site, country, sales region.",
            source=mapping,
            authority="sme",
            owner="SME",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "site", "term": "term.site_code"}],
            decision_table=[{"when": {"site": "IN-BLR", "family": "FAB-RULE"}, "then": {"bind": "country IN"}}],
            tests=[{"given": {"site": "IN-BLR", "family": "FAB-RULE"}, "expect": {"bind_scope": "country", "archive_family": "APAC"}}],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.region.disagreement",
            statement="Site and stored region disagreement waits. AU and ZA wait.",
            source=mapping,
            authority="sme",
            owner="SME",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="REAL",
            inputs=[{"name": "site", "term": "term.site_code"}, {"name": "sales_region", "term": "term.sales_region"}],
            decision_table=[{"when": {"disagree": True}, "then": {"route": "HOLD_FOR_REVIEW"}}],
            tests=[
                {"given": {"site": "IN-BLR", "stored_sales_region": "AMER"}, "expect": {"route": "HOLD_FOR_REVIEW"}},
                {"given": {"country": "AU", "site": None}, "expect": {"route": "HOLD_FOR_REVIEW"}},
                {"given": {"country": "ZA", "site": None}, "expect": {"route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.threshold.silent",
            statement="Silent threshold routes to HOLD_FOR_REVIEW.",
            source=tracker,
            authority="unresolved",
            owner="Business Owner",
            policy_status="proposed",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "amount", "term": "term.recipe_release_limit"}],
            decision_table=[{"when": {"archive_silent": True}, "then": {"route": "HOLD_FOR_REVIEW"}}],
            tests=[
                {"given": {"amount": 60000, "archive_silent": True}, "expect": {"route": "HOLD_FOR_REVIEW"}},
                {"given": {"demo_display": True}, "expect": {"cutoff": 50000, "policy_status": "proposed"}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.month_end.blank.impl.java",
            statement="Java skips blank amount_text. Canonical path waits.",
            source=java,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="REAL",
            inputs=[{"name": "amount_text", "term": "term.cost_period"}],
            decision_table=[
                {"when": {"implementation": "java", "amount_text": ""}, "then": {"row": "omitted"}},
                {"when": {"canonical": True, "amount_text": ""}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[{"given": {"amount_text": ""}, "expect": {"implementation_row": "omitted", "canonical_route": "HOLD_FOR_REVIEW"}}],
            observed_implementations=[{"path": "legacy_java/ReconcileLegacy.java", "lines": "12"}],
        )
    )
    put(
        _card(
            id="rule.month_end.float.impl.java",
            statement="Java totals use double. The lake records the deviation.",
            source=java,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="n/a",
            inputs=[{"name": "amount_text", "term": "term.cost_period"}],
            decision_table=[
                {"when": {"implementation": "java"}, "then": {"total_type": "double"}},
                {"when": {"canonical": True, "money_type_unsigned": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[{"given": {"implementation": "java"}, "expect": {"total_type": "double"}}],
            observed_implementations=[{"path": "legacy_java/ReconcileLegacy.java", "lines": "12"}],
        )
    )
    put(
        _card(
            id="rule.open_flag.impl.night_batch",
            statement="Night batch flags REVIEW and HOLD. That matches BO-06a.",
            source=batch,
            authority="sme",
            owner="SME",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_code",
            honesty="n/a",
            inputs=[{"name": "status", "term": "term.open_operational"}],
            decision_table=[
                {"when": {"status": "REVIEW"}, "then": {"flagged": True, "route": "OPEN"}},
                {"when": {"status": "HOLD"}, "then": {"flagged": True, "route": "OPEN"}},
                {"when": {"status": "CLOSED"}, "then": {"flagged": False}},
            ],
            tests=[
                {"given": {"status": "REVIEW"}, "expect": {"flagged": True, "route": "OPEN"}},
                {"given": {"status": "HOLD"}, "expect": {"flagged": True, "route": "OPEN"}},
                {"given": {"status": "CLOSED"}, "expect": {"flagged": False}},
            ],
            observed_implementations=[{"path": "legacy_batch/shift_reconciliation.py", "lines": "13"}],
        )
    )
    put(
        _card(
            id="rule.night_batch.join_multiply",
            statement="Night batch join multiplies one US object into five rows.",
            source=batch,
            authority="unresolved",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="REAL",
            inputs=[{"name": "country", "term": "term.country_code"}],
            decision_table=[
                {"when": {"implementation": "night_batch", "country": "US"}, "then": {"joined_rows": 5}},
                {"when": {"canonical": True, "overlap": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[{"given": {"us_objects": 1, "active_policies": 5}, "expect": {"implementation_joined_rows": 5, "canonical_route": "HOLD_FOR_REVIEW"}}],
            observed_implementations=[{"path": "legacy_batch/shift_reconciliation.py", "lines": "8"}],
        )
    )
    put(
        _card(
            id="rule.feed.replay_duplicate",
            statement="REPLAY is a duplicate candidate. No auto drop.",
            source=source_for_inherited("app/partner_feeds.py", register, lines="67"),
            authority="policy_archive",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_code",
            honesty="REAL",
            inputs=[{"name": "processing_status", "term": "term.replay"}],
            decision_table=[{"when": {"processing_status": "REPLAY"}, "then": {"route": "QUEUE", "duplicate_candidate": True}}],
            tests=[{"given": {"processing_status": "REPLAY"}, "expect": {"duplicate_candidate": True, "auto_drop": False}}],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.recipe.mismatch_show_both",
            statement="Show both recipe fields. Do not pick a winner.",
            source=tracker,
            authority="sme",
            owner="SME",
            policy_status="decided",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "recipe_version", "term": "term.recipe_revision_dispatch"}, {"name": "recipe_rev", "term": "term.recipe_revision_equipment"}],
            decision_table=[{"when": {"mismatch": True}, "then": {"show_both": True, "write_hold": False}}],
            tests=[{"given": {"recipe_version": "R02", "recipe_rev": "R01"}, "expect": {"show_both": True, "write_engineering_hold": False}}],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.clock.event_vs_arrival",
            statement="Keep two clocks. A cut-off question waits.",
            source=ent,
            authority="policy_archive",
            owner="unknown",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_record",
            honesty="REAL",
            inputs=[{"name": "event_time", "term": "term.evidence"}, {"name": "arrival_time", "term": "term.evidence"}],
            decision_table=[{"when": {"cutoff_owner": "unknown"}, "then": {"route": "HOLD_FOR_REVIEW"}}],
            tests=[{"given": {"event_time": "T1", "arrival_time": "T2", "question": "cutoff"}, "expect": {"show_both": True, "route": "HOLD_FOR_REVIEW"}}],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.untrusted_text.block",
            statement="Untrusted text never approves or releases.",
            source=inject,
            authority="policy_archive",
            owner="Policy Owner (RT-04)",
            policy_status="n/a",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "proposed_action", "term": "term.approval"}],
            decision_table=[{"when": {"injection_locator": True, "proposed_action": "approve"}, "then": {"route": "BLOCK"}}],
            tests=[
                {"given": {"store": "partner_feeds", "proposed_action": "approve"}, "expect": {"block": True}},
                {"given": {"store": "bundled_events", "proposed_action": "release"}, "expect": {"block": True}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.threshold.never_999999",
            statement="No archive match is HOLD_FOR_REVIEW, not 999999.",
            source=tracker,
            authority="unresolved",
            owner="Business Owner",
            policy_status="proposed",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "archive_match", "term": "term.recipe_release_limit"}],
            decision_table=[{"when": {"archive_match": False}, "then": {"route": "HOLD_FOR_REVIEW"}}],
            tests=[{"given": {"archive_match": False}, "expect": {"route": "HOLD_FOR_REVIEW", "limit_is_999999": False}}],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.threshold.demo_50000",
            statement="Demo cutoff 50000 stays PROPOSED.",
            source=tracker,
            authority="unresolved",
            owner="Business Owner",
            policy_status="proposed",
            claim="verified_fact",
            trust="trusted_record",
            honesty="REAL",
            inputs=[{"name": "demo_display", "term": "term.policy"}],
            decision_table=[
                {"when": {"demo_display": True}, "then": {"cutoff": 50000, "policy_status": "proposed"}},
                {"when": {"live_policy": True, "archive_silent": True}, "then": {"route": "HOLD_FOR_REVIEW"}},
            ],
            tests=[
                {"given": {"demo_display": True}, "expect": {"cutoff": 50000, "policy_status": "proposed"}},
                {"given": {"live_policy": True}, "expect": {"route": "HOLD_FOR_REVIEW"}},
            ],
            observed_implementations=[],
        )
    )
    put(
        _card(
            id="rule.hold.person_only",
            statement="A model hold proposal waits. A person writes the hold.",
            source=tracker,
            authority="sme",
            owner="SME",
            policy_status="proposed",
            claim="verified_fact",
            trust="trusted_record",
            honesty="n/a",
            inputs=[{"name": "proposed_hold", "term": "term.engineering_hold"}],
            decision_table=[{"when": {"model_proposes_hold": True}, "then": {"route": "HOLD_FOR_REVIEW", "write": False}}],
            tests=[{"given": {"model_proposes_engineering_hold": 1}, "expect": {"route": "HOLD_FOR_REVIEW", "write": False}}],
            observed_implementations=[],
        )
    )
    return ids
