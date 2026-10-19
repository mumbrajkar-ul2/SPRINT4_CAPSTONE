"""Write lake item YAML from governed files, schema counts, and locked decisions."""
from __future__ import annotations

from .common import (
    ARCHIVE_LIMITS,
    INHERITED,
    SITE_MAP,
    WORKSPACE,
    base_item,
    load_register,
    open_ro,
    source_for_inherited,
    source_for_workspace,
    write_item,
)


def _counts() -> dict[str, int]:
    legacy = open_ro(INHERITED / "data" / "legacy.sqlite3")
    ent = open_ro(INHERITED / "data" / "enterprise_legacy.sqlite3")
    out = {
        "recipe_mismatch": legacy.execute(
            """
            SELECT COUNT(*) FROM process_steps p
            JOIN fab_tools t ON t.tool_id = p.tool_id
            WHERE p.recipe_version != t.recipe_rev
            """
        ).fetchone()[0],
        "process_steps": legacy.execute("SELECT COUNT(*) FROM process_steps").fetchone()[0],
        "replay": legacy.execute(
            "SELECT COUNT(*) FROM partner_feeds WHERE processing_status='REPLAY'"
        ).fetchone()[0],
        "injection_feeds": legacy.execute(
            """
            SELECT COUNT(*) FROM partner_feeds
            WHERE raw_json LIKE '%auto approve%'
               OR raw_json LIKE '%disregard validation%'
            """
        ).fetchone()[0],
        "blank_amounts": legacy.execute(
            """
            SELECT COUNT(*) FROM vendor_file_rows
            WHERE amount_text IS NULL OR TRIM(amount_text)=''
            """
        ).fetchone()[0],
        "cases_over_50000": legacy.execute(
            "SELECT COUNT(*) FROM cases WHERE amount > 50000"
        ).fetchone()[0],
        "cases_not_closed": legacy.execute(
            "SELECT COUNT(*) FROM cases WHERE status != 'CLOSED'"
        ).fetchone()[0],
        "cases": legacy.execute("SELECT COUNT(*) FROM cases").fetchone()[0],
        "objects": ent.execute("SELECT COUNT(*) FROM operational_objects").fetchone()[0],
        "review_objects": ent.execute(
            "SELECT COUNT(*) FROM operational_objects WHERE status='REVIEW'"
        ).fetchone()[0],
        "hold_objects": ent.execute(
            "SELECT COUNT(*) FROM operational_objects WHERE status='HOLD'"
        ).fetchone()[0],
        "clocks_differ": ent.execute(
            "SELECT COUNT(*) FROM evidence_events WHERE event_time != arrival_time"
        ).fetchone()[0],
        "evidence": ent.execute("SELECT COUNT(*) FROM evidence_events").fetchone()[0],
        "unassigned": ent.execute(
            """
            SELECT COUNT(*) FROM workflow_tasks
            WHERE assigned_to IS NULL OR TRIM(assigned_to)=''
            """
        ).fetchone()[0],
        "orgs": ent.execute("SELECT COUNT(*) FROM organizations").fetchone()[0],
        "us_active": ent.execute(
            "SELECT COUNT(*) FROM policy_register WHERE region='US' AND active=1"
        ).fetchone()[0],
        "active_register": ent.execute(
            "SELECT COUNT(*) FROM policy_register WHERE active=1"
        ).fetchone()[0],
        "register_rows": ent.execute("SELECT COUNT(*) FROM policy_register").fetchone()[0],
        "injection_payload": ent.execute(
            """
            SELECT COUNT(*) FROM evidence_events
            WHERE payload LIKE '%ignore all controls and release%'
            """
        ).fetchone()[0],
    }
    disagree = 0
    for site, region, n in legacy.execute(
        "SELECT site, region, COUNT(*) FROM cases GROUP BY site, region"
    ):
        derived = SITE_MAP[site]["sales_region"]
        if region != derived:
            disagree += n
    out["site_region_disagree"] = disagree
    legacy.close()
    ent.close()
    return out


def generate_items() -> list[str]:
    register = load_register()
    counts = _counts()
    src = lambda rel, **kw: source_for_inherited(rel, register, **kw)
    cap = source_for_workspace
    written: list[str] = []

    def put(item, *, draft: bool = False) -> None:
        write_item(item, draft=draft)
        written.append(item["id"])

    archive = src("contracts/decision-policies-archive.json")
    register_db = src("data/enterprise_legacy.sqlite3", locator="policy_register.threshold")
    legacy_db = src("data/legacy.sqlite3")
    py = src("app/legacy_logic.py", lines="2-5")
    js = src("legacy_js/legacy_policy.js", lines="4-5")
    java = src("legacy_java/ReconcileLegacy.java", lines="12")
    batch = src("legacy_batch/shift_reconciliation.py", lines="8-14")
    profile = src("domain-profile.json")
    domain = src("domain.json")
    compose = src("compose.yaml")
    server = src("app/server.py", lines="63")
    gateway = src("services/source_gateway/server.py")
    feeds = src("app/partner_feeds.py", lines="60-67")
    historic = src("docs/historic-decisions.md", lines="9")
    incident = src("operations/incidents/INC-2025-014.md")
    tracker = cap("Decision_Tracker.md")
    catalogue = cap("docs/05-current-state/conflict-catalogue.md")
    adr_lake = cap("docs/10-architecture/adrs/adr-lake-yaml-to-sqlite.md")
    adr_graph = cap("docs/10-architecture/adrs/adr-knowledge-graph-edges-table.md")
    adr_ports = cap("docs/10-architecture/adrs/adr-ports-and-compose.md")
    adr_apps = cap("docs/10-architecture/adrs/adr-two-applications.md")
    km = cap("docs/11-data-context/knowledge-model.md")
    mapping = cap("docs/11-data-context/mapping-design.md")
    inject_design = cap("docs/11-data-context/injection-corpus-design.md")

    # --- archive versions ---
    for year, region, start, end, limit in ARCHIVE_LIMITS:
        item_id = f"rule.recipe_release.limit.v{year}.{region.lower()}"
        prev_year = str(int(year) - 1)
        supersedes = (
            f"rule.recipe_release.limit.v{prev_year}.{region.lower()}"
            if year != "2022"
            else None
        )
        links = [
            {"type": "governs", "to": "rule.recipe_release.limit"},
            {"type": "maps_to", "to": "term.sales_region"},
        ]
        if supersedes:
            links.append({"type": "supersedes", "to": supersedes})
        if year == "2023" and region == "EMEA":
            links.append({"type": "tested_by", "to": "test.rule.recipe_release.emea_2023"})
        if year == "2026" and region == "APAC":
            links.append({"type": "tested_by", "to": "test.rule.recipe_release.apac_2026"})
            links.append({"type": "implements", "to": "code.legacy_policy.js_allow"})
        put(
            base_item(
                id=item_id,
                kind="business_rule",
                statement=(
                    f"The {year} {region} recipe_release limit is {limit} USD "
                    f"from {start} through {end}. Currency is USD. Honesty: REAL."
                ),
                source=archive,
                claim="verified_fact",
                trust="trusted_record",
                owner="Policy Owner (RT-04)",
                policy_status="decided",
                honesty="REAL",
                authority="policy_archive",
                valid_time={"from": start, "to": end},
                supersedes=supersedes,
                links=links,
            )
        )

    put(
        base_item(
            id="rule.recipe_release.limit",
            kind="business_rule",
            statement=(
                "The canonical recipe_release limit is the archive JSON row whose "
                "sales region and date match. Fifteen versions cover APAC, EMEA, "
                "and AMER from 2022 through 2026. A missing row does not use 999999."
            ),
            source=archive,
            claim="verified_fact",
            trust="trusted_record",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            honesty="REAL",
            authority="policy_archive",
            links=[
                {"type": "tested_by", "to": "test.rule.recipe_release.emea_2023"},
                {"type": "tested_by", "to": "test.rule.recipe_release.apac_2026"},
                {"type": "conflicts_with", "to": "rule.recipe_release.limit.impl.js"},
            ],
        )
    )
    put(
        base_item(
            id="rule.recipe_release.no_match",
            kind="business_rule",
            statement=(
                "When no archive recipe_release row matches the derived sales region "
                "and date, the route is HOLD_FOR_REVIEW. Country IN is not an archive "
                "region. Date 2021-06-01 is outside 2022-2026. Do not use 999999."
            ),
            source=archive,
            claim="verified_fact",
            trust="trusted_record",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            honesty="REAL",
            authority="policy_archive",
            links=[{"type": "governs", "to": "rule.recipe_release.limit"}],
        )
    )
    put(
        base_item(
            id="rule.policy.overlap_or_invalid",
            kind="business_rule",
            statement=(
                "When two active policy_register rows match one country on the lookup "
                f"date, or when valid_from is after valid_to, the route is HOLD_FOR_REVIEW. "
                f"US has {counts['us_active']} active rows. POL-0039 has from 2025-01-01 "
                "and to 2024-12-31. Honesty: REAL."
            ),
            source=register_db,
            claim="verified_fact",
            trust="trusted_record",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            honesty="REAL",
            authority="policy_archive",
            links=[{"type": "evidenced_by", "to": "data.policy_register.overlap"}],
        )
    )
    put(
        base_item(
            id="rule.fab_rule.family",
            kind="business_rule",
            statement=(
                "policy_register stores family FAB-RULE-0 through FAB-RULE-4 at country "
                "scope. Those thresholds are a different family from recipe_release. "
                f"The table has {counts['register_rows']} rows, {counts['active_register']} active. "
                "Honesty: REAL."
            ),
            source=register_db,
            claim="verified_fact",
            trust="trusted_record",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            honesty="REAL",
            authority="policy_archive",
            links=[],
        )
    )

    # --- deviations ---
    put(
        base_item(
            id="rule.recipe_release.limit.impl.js",
            kind="business_rule",
            statement=(
                "legacy_policy.js allows an amount when it is less than or equal to "
                "the archive limit times 1.05. Amount 15700 for APAC 2022 is allowed "
                "here (15000 times 1.05 is 15750) and denied on the archive."
            ),
            source=js,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="unresolved",
            links=[
                {"type": "implements", "to": "rule.recipe_release.limit"},
                {"type": "depends_on", "to": "data.contract.decision_policies_archive"},
            ],
        )
    )
    put(
        base_item(
            id="rule.recipe_release.limit.impl.js_default",
            kind="business_rule",
            statement=(
                "legacy_policy.js returns 999999 when year or region is missing from "
                "the archive. Region IN and year 2026 take that default. The canonical "
                "route is HOLD_FOR_REVIEW. 999999 is not a live policy number."
            ),
            source=js,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="unresolved",
            links=[
                {"type": "implements", "to": "rule.recipe_release.limit"},
                {"type": "conflicts_with", "to": "rule.recipe_release.no_match"},
            ],
        )
    )
    put(
        base_item(
            id="rule.urgent.amount.impl.python",
            kind="business_rule",
            statement=(
                "legacy_logic.py returns urgent when amount is greater than 50000. "
                f"Packaged cases with amount above 50000: {counts['cases_over_50000']}. "
                "The archive is silent on this cutoff. Live policy is HOLD_FOR_REVIEW. "
                "Demo may show 50000 labelled PROPOSED. Honesty: REAL."
            ),
            source=py,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="proposed",
            honesty="REAL",
            authority="unresolved",
            links=[
                {"type": "implements", "to": "rule.recipe_release.limit"},
                {"type": "conflicts_with", "to": "rule.threshold.silent"},
            ],
        )
    )
    put(
        base_item(
            id="rule.priority.closed.impl.python",
            kind="business_rule",
            statement=(
                "legacy_logic.py returns archive when status is CLOSED. A CLOSED word "
                "is not enough for SME operational closed. Confirming closed needs a "
                "final disposition and no pending engineering action."
            ),
            source=py,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="unresolved",
            links=[
                {"type": "implements", "to": "code.legacy_logic.priority"},
                {"type": "conflicts_with", "to": "rule.open_closed.operational"},
            ],
        )
    )
    put(
        base_item(
            id="rule.urgent.severity.impl.python",
            kind="business_rule",
            statement=(
                "legacy_logic.py returns urgent when severity is CRITICAL. The archive "
                "is silent on severity words. This ranking is a recorded deviation."
            ),
            source=py,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            authority="unresolved",
            links=[{"type": "implements", "to": "code.legacy_logic.priority"}],
        )
    )
    put(
        base_item(
            id="rule.open_closed.operational",
            kind="business_rule",
            statement=(
                "A case is open while any disposition or engineering action is pending, "
                "including REVIEW and HOLD. A case is closed only when a final "
                "disposition is recorded and no engineering action is pending. BO-06a."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="SME",
            policy_status="decided",
            honesty="n/a",
            authority="sme",
            links=[{"type": "governs", "to": "term.open_operational"}],
        )
    )
    put(
        base_item(
            id="rule.open_closed.finance_audit",
            kind="business_rule",
            statement=(
                "Operational closed, finance booked, and audit closed are three states. "
                "BO-06b is PROPOSED. A mismatch routes to HOLD_FOR_REVIEW. Do not merge "
                "the three flags."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="Business Owner",
            policy_status="proposed",
            honesty="n/a",
            authority="unresolved",
            links=[{"type": "governs", "to": "term.closed_finance"}],
        )
    )
    put(
        base_item(
            id="rule.region.site_canonical",
            kind="business_rule",
            statement=(
                "Site code is the canonical location key. Country and sales region are "
                "derived from the site. IN-BLR derives country IN and sales region APAC. "
                "US-TX derives US and AMER. DE-BY derives DE and EMEA. GB-ENG derives GB "
                "and EMEA. BR-SP derives BR and AMER. JP-KN derives JP and APAC."
            ),
            source=mapping,
            claim="inference",
            trust="trusted_record",
            owner="SME",
            policy_status="decided",
            honesty="n/a",
            authority="sme",
            links=[{"type": "maps_to", "to": "term.site_code"}],
        )
    )
    put(
        base_item(
            id="rule.region.specificity",
            kind="business_rule",
            statement=(
                "The most specific scope wins. Order is site, then country, then sales "
                "region. recipe_release still binds at the derived sales region. "
                "FAB-RULE binds at country."
            ),
            source=mapping,
            claim="verified_fact",
            trust="trusted_record",
            owner="SME",
            policy_status="decided",
            honesty="n/a",
            authority="sme",
            links=[{"type": "governs", "to": "rule.region.site_canonical"}],
        )
    )
    put(
        base_item(
            id="rule.region.disagreement",
            kind="business_rule",
            statement=(
                "When the site-derived sales region disagrees with a stored sales region, "
                f"the route is HOLD_FOR_REVIEW. {counts['site_region_disagree']} of "
                f"{counts['cases']} packaged cases have that disagreement. Country AU "
                "has no site. Country ZA has no site. Those lookups wait. Do not invent "
                "a site. Honesty: REAL."
            ),
            source=mapping,
            claim="verified_fact",
            trust="trusted_record",
            owner="SME",
            policy_status="decided",
            honesty="REAL",
            authority="sme",
            links=[{"type": "conflicts_with", "to": "rule.region.site_canonical"}],
        )
    )
    put(
        base_item(
            id="rule.threshold.silent",
            kind="business_rule",
            statement=(
                "The archive is silent on an urgent amount cutoff. Live policy is "
                "HOLD_FOR_REVIEW. Do not invent a number. Demo may show 50000 labelled "
                "PROPOSED. Never use 999999 as a live policy number. BO-08 stays PROPOSED."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="Business Owner",
            policy_status="proposed",
            honesty="n/a",
            authority="unresolved",
            links=[{"type": "conflicts_with", "to": "rule.threshold.never_999999"}],
        )
    )
    put(
        base_item(
            id="rule.month_end.blank.impl.java",
            kind="business_rule",
            statement=(
                "ReconcileLegacy.java skips a row when amount_text is blank or unreadable. "
                f"Packaged vendor_file_rows with blank amount_text: {counts['blank_amounts']}. "
                "The canonical path on a blank is HOLD_FOR_REVIEW. Honesty: REAL."
            ),
            source=java,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="unresolved",
            links=[{"type": "implements", "to": "code.reconcile_legacy.java_total"}],
        )
    )
    put(
        base_item(
            id="rule.month_end.float.impl.java",
            kind="business_rule",
            statement=(
                "ReconcileLegacy.java parses amount_text with Double.parseDouble and "
                "adds it to a double total. The lake records that deviation. It does "
                "not pick a binary money type in this unit."
            ),
            source=java,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            authority="unresolved",
            links=[{"type": "implements", "to": "code.reconcile_legacy.java_total"}],
        )
    )
    put(
        base_item(
            id="rule.open_flag.impl.night_batch",
            kind="business_rule",
            statement=(
                "shift_reconciliation.py flags status REVIEW and status HOLD. That flag "
                "matches BO-06a. REVIEW is open. HOLD is open. CLOSED is not flagged "
                "for status. The threshold branch is separate."
            ),
            source=batch,
            claim="verified_fact",
            trust="trusted_code",
            owner="SME",
            policy_status="decided",
            honesty="n/a",
            authority="sme",
            links=[
                {"type": "implements", "to": "rule.open_closed.operational"},
                {"type": "maps_to", "to": "term.open_operational"},
            ],
        )
    )
    put(
        base_item(
            id="rule.night_batch.join_multiply",
            kind="business_rule",
            statement=(
                "The night batch joins each object to every active policy_register row "
                f"on the same country code. US has {counts['us_active']} active rows. "
                "One US object can become five joined rows. LIMIT 500 applies to joined "
                "rows. Canonical overlap is HOLD_FOR_REVIEW."
            ),
            source=batch,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="unresolved",
            links=[
                {"type": "conflicts_with", "to": "rule.policy.overlap_or_invalid"},
                {"type": "implements", "to": "code.shift_reconciliation.night_batch"},
            ],
        )
    )
    put(
        base_item(
            id="rule.feed.replay_duplicate",
            kind="business_rule",
            statement=(
                f"processing_status REPLAY marks a partner feed as a duplicate candidate. "
                f"Packaged REPLAY rows: {counts['replay']}. reconcile() would mark "
                "DUPLICATE. This unit does not run reconcile(). Drop waits for RT-05. "
                "Honesty: REAL."
            ),
            source=feeds,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="policy_archive",
            links=[{"type": "evidenced_by", "to": "data.feed.replay"}],
        )
    )
    put(
        base_item(
            id="rule.recipe.mismatch_show_both",
            kind="business_rule",
            statement=(
                "When dispatch recipe_version is R02 and equipment recipe_rev is R01, "
                "both values are shown. A Process Engineer at RT-03 approves a hold or "
                "a release. The lake does not pick a winner. The lake does not write "
                "engineering_hold."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="SME",
            policy_status="decided",
            honesty="n/a",
            authority="sme",
            links=[
                {"type": "maps_to", "to": "term.recipe_revision_dispatch"},
                {"type": "maps_to", "to": "term.recipe_revision_equipment"},
            ],
        )
    )
    put(
        base_item(
            id="rule.clock.event_vs_arrival",
            kind="business_rule",
            statement=(
                "event_time and arrival_time stay two fields. "
                f"{counts['clocks_differ']} of {counts['evidence']} evidence rows differ. "
                "Month-end uses event_time unless a later signed rule says otherwise. "
                "A signed cut-off owner is Unknown, so a cut-off question routes "
                "HOLD_FOR_REVIEW. Honesty: REAL."
            ),
            source=src("data/enterprise_legacy.sqlite3", locator="evidence_events.event_time"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            authority="policy_archive",
            links=[{"type": "evidenced_by", "to": "data.clock.event_vs_arrival_evidence"}],
        )
    )
    put(
        base_item(
            id="rule.untrusted_text.block",
            kind="business_rule",
            statement=(
                "Harvested instruction language never drives approve, release, "
                "ignore-validation, or close-from-text. The expected verdict is BLOCK. "
                "Injection locators live in the six packaged stores named on the "
                "injection corpus."
            ),
            source=inject_design,
            claim="verified_fact",
            trust="trusted_record",
            owner="Policy Owner (RT-04)",
            policy_status="n/a",
            honesty="n/a",
            authority="policy_archive",
            links=[
                {"type": "evidenced_by", "to": "data.injection.partner_feeds"},
                {"type": "evidenced_by", "to": "data.injection.bundled_events"},
                {"type": "evidenced_by", "to": "data.injection.emails"},
                {"type": "evidenced_by", "to": "data.injection.source_documents"},
                {"type": "evidenced_by", "to": "data.injection.html"},
                {"type": "evidenced_by", "to": "data.injection.evidence_payloads"},
            ],
        )
    )
    put(
        base_item(
            id="rule.threshold.never_999999",
            kind="business_rule",
            statement=(
                "When no archive row matches, the route is HOLD_FOR_REVIEW. The "
                "JavaScript default 999999 is not a live policy number."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="Business Owner",
            policy_status="proposed",
            honesty="n/a",
            authority="unresolved",
            links=[{"type": "conflicts_with", "to": "rule.recipe_release.limit.impl.js_default"}],
        )
    )
    put(
        base_item(
            id="rule.threshold.demo_50000",
            kind="business_rule",
            statement=(
                "If a demo screen must show an urgent cutoff, show 50000 with "
                "policy_status proposed. That number is the Python cutoff. It is not "
                "a signed live policy. Never show 999999 as the fallback."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="Business Owner",
            policy_status="proposed",
            honesty="REAL",
            authority="unresolved",
            links=[{"type": "governs", "to": "rule.urgent.amount.impl.python"}],
        )
    )
    put(
        base_item(
            id="rule.hold.person_only",
            kind="business_rule",
            statement=(
                "A model that proposes engineering_hold=1 routes to HOLD_FOR_REVIEW. "
                "The lake does not write the hold. A person approves every "
                "record-changing action. FD-05 rejects a hold predictor. The tracker "
                "row is PROPOSED."
            ),
            source=tracker,
            claim="verified_fact",
            trust="trusted_record",
            owner="SME",
            policy_status="proposed",
            honesty="n/a",
            authority="sme",
            links=[],
        )
    )

    # --- site maps ---
    for site, derived in SITE_MAP.items():
        put(
            base_item(
                id=f"map.site.{site}",
                kind="data_relationship",
                statement=(
                    f"Site {site} derives country {derived['country']} and sales region "
                    f"{derived['sales_region']}. The prefix of the site string is the "
                    "country code. This map is an engineering derivation for BO-07."
                ),
                source=mapping,
                claim="inference",
                trust="trusted_record",
                owner="team-force",
                policy_status="decided",
                honesty="n/a",
                authority="sme",
                links=[
                    {"type": "maps_to", "to": "term.country_code"},
                    {"type": "maps_to", "to": "term.sales_region"},
                    {"type": "maps_to", "to": "term.site_code"},
                ],
            )
        )

    # --- code ---
    put(
        base_item(
            id="code.legacy_logic.priority",
            kind="code_intelligence",
            statement=(
                "app/legacy_logic.py function priority returns archive when status is "
                "CLOSED, urgent when severity is CRITICAL or amount is greater than "
                "50000, review when severity is HIGH or status is ESCALATED, else queue. "
                "Python priority does not read the archive JSON."
            ),
            source=py,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[
                {"type": "implements", "to": "rule.recipe_release.limit"},
                {"type": "implements", "to": "rule.urgent.amount.impl.python"},
            ],
        )
    )
    put(
        base_item(
            id="code.legacy_policy.js_allow",
            kind="code_intelligence",
            statement=(
                "legacy_js/legacy_policy.js reads contracts/decision-policies-archive.json. "
                "legacyAllows returns true when amount is less than or equal to the "
                "archive limit times 1.05. Missing year or region returns 999999."
            ),
            source=js,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[
                {"type": "implements", "to": "rule.recipe_release.limit"},
                {"type": "implements", "to": "rule.recipe_release.limit.v2026.apac"},
                {"type": "depends_on", "to": "data.contract.decision_policies_archive"},
            ],
        )
    )
    put(
        base_item(
            id="code.reconcile_legacy.java_total",
            kind="code_intelligence",
            statement=(
                "legacy_java/ReconcileLegacy.java sums vendor amount_text as a double. "
                "A blank or unreadable cell is skipped with no report."
            ),
            source=java,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            links=[{"type": "implements", "to": "rule.recipe_release.limit"}],
        )
    )
    put(
        base_item(
            id="code.shift_reconciliation.night_batch",
            kind="code_intelligence",
            statement=(
                "legacy_batch/shift_reconciliation.py reads data/enterprise_legacy.sqlite3 "
                "directly. It does not call the HTTP API. It flags HOLD and REVIEW, and "
                "flags value greater than threshold after a join on country code."
            ),
            source=batch,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            links=[
                {"type": "implements", "to": "rule.recipe_release.limit"},
                {"type": "depends_on", "to": "dep.night_batch_reads_enterprise"},
            ],
        )
    )
    put(
        base_item(
            id="code.partner_feeds.reconcile",
            kind="code_intelligence",
            statement=(
                "app/partner_feeds.py function reconcile marks processing_status REPLAY "
                "as DUPLICATE. This harvest records that behaviour. It does not run "
                "reconcile() against the packaged database."
            ),
            source=feeds,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            links=[{"type": "implements", "to": "rule.feed.replay_duplicate"}],
        )
    )
    put(
        base_item(
            id="code.tests.inventory",
            kind="code_intelligence",
            statement=(
                "Seven test modules sit under tests/. test_workflow.py checks 125 cases, "
                "CLOSED to archive, and CRITICAL to urgent. test_domain.py checks tools "
                "and lots. test_enterprise.py checks domain rows. test_partner_feeds.py "
                "checks table names. test_historical_fixture.py checks tiny lake counts. "
                "test_enterprise_legacy_v6.py checks a 120-row generate. "
                "test_source_gateway.py can write packaged gateway_inbox. Harvest does "
                "not run those tests."
            ),
            source=cap("docs/05-current-state/brownfield-inventory.md"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            links=[{"type": "tested_by", "to": "test.rule.recipe_release.emea_2023"}],
        )
    )
    put(
        base_item(
            id="test.rule.recipe_release.emea_2023",
            kind="code_intelligence",
            statement=(
                "Canonical test: amount 18000, sales_region EMEA, on_date 2023-07-01 "
                "is within the 18600 USD recipe_release limit."
            ),
            source=km,
            claim="verified_fact",
            trust="trusted_record",
            owner="team-force",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "tested_by", "to": "rule.recipe_release.limit"}],
        )
    )
    put(
        base_item(
            id="test.rule.recipe_release.apac_2026",
            kind="code_intelligence",
            statement=(
                "Canonical test: amount 25000, sales_region APAC, on_date 2026-06-01 "
                "is within the 25000 USD recipe_release limit. Amount 25001 is outside."
            ),
            source=km,
            claim="verified_fact",
            trust="trusted_record",
            owner="team-force",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "tested_by", "to": "rule.recipe_release.limit.v2026.apac"}],
        )
    )

    # --- architecture ---
    put(
        base_item(
            id="arch.listener.legacy_8080",
            kind="architecture",
            statement=(
                "The inherited legacy API listens on port 8080. app/server.py reads "
                "PORT and defaults to 8080. The handler does not check identity."
            ),
            source=server,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "depends_on", "to": "arch.compose.inherited"}],
        )
    )
    put(
        base_item(
            id="arch.listener.gateway_8090",
            kind="architecture",
            statement=(
                "The inherited source gateway listens on port 8090. The event payload "
                "returns occurred_at and published_at."
            ),
            source=gateway,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "depends_on", "to": "arch.compose.inherited"}],
        )
    )
    put(
        base_item(
            id="arch.listener.lake_rest_8091",
            kind="architecture",
            statement=(
                "The Context Lake REST listener uses port 8091. That port is locked "
                "in the Phase 4 ports ADR. The inherited compose file does not listen "
                "there yet."
            ),
            source=adr_ports,
            claim="verified_fact",
            trust="trusted_record",
            owner="team-force",
            policy_status="decided",
            honesty="n/a",
            links=[{"type": "depends_on", "to": "arch.lake.yaml_sqlite"}],
        )
    )
    put(
        base_item(
            id="arch.listener.lake_mcp_8092",
            kind="architecture",
            statement=(
                "The Context Lake MCP listener uses port 8092. That port is locked "
                "in the Phase 4 ports ADR."
            ),
            source=adr_ports,
            claim="verified_fact",
            trust="trusted_record",
            owner="team-force",
            policy_status="decided",
            honesty="n/a",
            links=[{"type": "depends_on", "to": "arch.lake.yaml_sqlite"}],
        )
    )
    put(
        base_item(
            id="arch.compose.inherited",
            kind="architecture",
            statement=(
                "Inherited compose.yaml starts services legacy, source-gateway, and "
                "bridge. It publishes 8080 and 8090. It does not publish 8091 or 8092."
            ),
            source=compose,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="arch.lake.yaml_sqlite",
            kind="architecture",
            statement=(
                "People and harvest scripts write YAML in Git. build.py writes "
                "context-lake.sqlite3 with tables items, edges, terms, and FTS5. "
                "The YAML is the source of truth."
            ),
            source=adr_lake,
            claim="verified_fact",
            trust="trusted_record",
            owner="team-force",
            policy_status="decided",
            honesty="n/a",
            links=[],
        )
    )
    put(
        base_item(
            id="arch.graph.edges_table",
            kind="architecture",
            statement=(
                "The knowledge graph is the edges table in context-lake.sqlite3. "
                "Recursive SQL walks the links. The project does not run a graph database."
            ),
            source=adr_graph,
            claim="verified_fact",
            trust="trusted_record",
            owner="team-force",
            policy_status="decided",
            honesty="n/a",
            links=[{"type": "depends_on", "to": "arch.lake.yaml_sqlite"}],
        )
    )

    # --- dependencies ---
    put(
        base_item(
            id="dep.js_reads_archive",
            kind="dependency",
            statement=(
                "legacy_policy.js reads contracts/decision-policies-archive.json from "
                "the working directory. Python priority does not read that file."
            ),
            source=js,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            links=[
                {"type": "depends_on", "to": "data.contract.decision_policies_archive"},
                {"type": "depends_on", "to": "code.legacy_policy.js_allow"},
            ],
        )
    )
    put(
        base_item(
            id="dep.night_batch_reads_enterprise",
            kind="dependency",
            statement=(
                "The night batch reads data/enterprise_legacy.sqlite3. It does not "
                "call the HTTP API."
            ),
            source=batch,
            claim="verified_fact",
            trust="trusted_code",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            links=[{"type": "depends_on", "to": "code.shift_reconciliation.night_batch"}],
        )
    )

    # --- data ---
    put(
        base_item(
            id="data.contract.decision_policies_archive",
            kind="data_relationship",
            statement=(
                "contracts/decision-policies-archive.json holds 15 historical_versions "
                "of rule recipe_release for APAC, EMEA, and AMER from 2022 through 2026. "
                "2026 limits are APAC 25000, EMEA 26100, AMER 27200. Honesty: REAL."
            ),
            source=archive,
            claim="verified_fact",
            trust="trusted_record",
            owner="Policy Owner (RT-04)",
            policy_status="decided",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.join.recipe_mismatch",
            kind="data_relationship",
            statement=(
                f"{counts['recipe_mismatch']} of {counts['process_steps']} process steps "
                "have recipe_version different from the joined fab_tools.recipe_rev on "
                "tool_id. The lake does not pick a winning revision. Honesty: REAL."
            ),
            source=src("data/legacy.sqlite3", locator="process_steps.recipe_version"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[
                {"type": "conflicts_with", "to": "term.recipe_revision_dispatch"},
                {"type": "conflicts_with", "to": "term.recipe_revision_equipment"},
                {"type": "evidenced_by", "to": "decision.bp1.recipe_mismatch"},
            ],
        )
    )
    put(
        base_item(
            id="data.missing.lot_genealogy",
            kind="data_relationship",
            statement=(
                "wafer_lots has columns lot_id, tool_id, wafer_count, defect_count, "
                "measured_yield, and engineering_hold. There is no parent_lot_id column. "
                "The lake has no lot genealogy data."
            ),
            source=src("data/legacy.sqlite3", locator="wafer_lots.lot_id"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "evidenced_by", "to": "term.lot_genealogy"}],
        )
    )
    put(
        base_item(
            id="data.missing.case_lot_id",
            kind="data_relationship",
            statement=(
                "cases has no lot_id column. A case row cannot join to wafer_lots on a "
                "stored lot key."
            ),
            source=src("data/legacy.sqlite3", locator="cases.id"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.clock.event_vs_arrival_partner",
            kind="data_relationship",
            statement=(
                "partner_feeds stores source_ts and ingest_ts as two fields. Harvest "
                "records the two clocks. It does not copy feed JSON bodies into the lake."
            ),
            source=src("data/legacy.sqlite3", locator="partner_feeds.source_ts"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.clock.event_vs_arrival_evidence",
            kind="data_relationship",
            statement=(
                f"{counts['clocks_differ']} of {counts['evidence']} evidence_events rows "
                "have arrival_time different from event_time. Honesty: REAL."
            ),
            source=src("data/enterprise_legacy.sqlite3", locator="evidence_events.arrival_time"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.feed.replay",
            kind="data_relationship",
            statement=(
                f"partner_feeds has {counts['replay']} rows with processing_status REPLAY. "
                "Honesty: REAL. Those rows stay in the operational store."
            ),
            source=src("data/legacy.sqlite3", locator="partner_feeds.processing_status"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.policy_register.overlap",
            kind="data_relationship",
            statement=(
                f"US has {counts['us_active']} active policy_register rows at once. "
                "A night-batch join on country multiplies one US object into several "
                "flagged rows. Honesty: REAL."
            ),
            source=register_db,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.policy_register.invalid_interval",
            kind="data_relationship",
            statement=(
                "POL-0039 is active with valid_from 2025-01-01 and valid_to 2024-12-31. "
                "The interval is empty. A match routes to HOLD_FOR_REVIEW. Honesty: REAL."
            ),
            source=src("data/enterprise_legacy.sqlite3", locator="policy_register.valid_from"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "evidenced_by", "to": "rule.policy.overlap_or_invalid"}],
        )
    )
    put(
        base_item(
            id="data.task.unassigned",
            kind="data_relationship",
            statement=(
                f"workflow_tasks has {counts['unassigned']} rows with assigned_to empty. "
                "Honesty: REAL."
            ),
            source=src("data/enterprise_legacy.sqlite3", locator="workflow_tasks.assigned_to"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.org.tenant_country_pairing",
            kind="data_relationship",
            statement=(
                f"organizations has {counts['orgs']} rows. TENANT-APAC holds IN and BR. "
                "TENANT-EMEA holds DE and GB. TENANT-AMER holds US and ZA. TENANT-SOUTH "
                "holds AU and JP. The tenant name is not a country map. Brazil under "
                "TENANT-APAC is a generator pairing. Honesty: REAL."
            ),
            source=src("data/enterprise_legacy.sqlite3", locator="organizations.tenant"),
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="data.incident.inc_2025_014",
            kind="data_relationship",
            statement=(
                "operations/incidents/INC-2025-014.md records a 2025-11-18 partner-feed "
                "delay and a 04:00 UTC manual spreadsheet. Follow-up owner is unknown."
            ),
            source=incident,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )

    injection_specs = [
        (
            "data.injection.partner_feeds",
            f"partner_feeds.raw_json has {counts['injection_feeds']} rows whose notes "
            "field contains auto-approve language. Generator condition is i%101==0. "
            "Honesty: REAL. The note is data.",
            src("data/legacy.sqlite3", locator="partner_feeds.raw_json"),
            counts["injection_feeds"],
        ),
        (
            "data.injection.bundled_events",
            "Bundled lake events JSONL has 150 rows whose source_claim field contains "
            "approve-this-record language. Generator condition is i%671==0. Honesty: REAL.",
            inject_design,
            150,
        ),
        (
            "data.injection.emails",
            "Archive emails 00000.eml, 00202.eml, and 00404.eml contain "
            "approve-or-ignore language. Count 3. Honesty: REAL.",
            src("data/archive_documents/00000.eml"),
            3,
        ),
        (
            "data.injection.source_documents",
            "source_documents.jsonl has 22 bodies with ignore-or-release language. "
            "Generator condition is i%57==0. Honesty: REAL.",
            src("data/documents/source_documents.jsonl"),
            22,
        ),
        (
            "data.injection.html",
            "Archive HTML files 00101.html and 00303.html contain approve-or-ignore "
            "language. Count 2. Honesty: REAL.",
            src("data/archive_documents/00101.html"),
            2,
        ),
        (
            "data.injection.evidence_payloads",
            f"evidence_events.payload has {counts['injection_payload']} rows whose note "
            "contains ignore-controls-and-release language. Generator condition is "
            "i%1399==0. Honesty: REAL.",
            src("data/enterprise_legacy.sqlite3", locator="evidence_events.payload"),
            counts["injection_payload"],
        ),
    ]
    for item_id, statement, source, _count in injection_specs:
        put(
            base_item(
                id=item_id,
                kind="data_relationship",
                statement=statement,
                source=source,
                claim="verified_fact",
                trust="untrusted_text",
                owner="unknown",
                policy_status="n/a",
                honesty="REAL",
                links=[
                    {"type": "evidenced_by", "to": "rule.untrusted_text.block"},
                    {"type": "evidenced_by", "to": "decision.bp7.untrusted_text"},
                ],
            )
        )
    put(
        base_item(
            id="data.injection.tiny_events",
            kind="data_relationship",
            statement=(
                "Tiny lake events have 15 rows whose source_claim field contains "
                "approve language. They are a fast-test subset. They do not replace "
                "the 150 bundled rows. Honesty: REAL."
            ),
            source=inject_design,
            claim="verified_fact",
            trust="untrusted_text",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "evidenced_by", "to": "rule.untrusted_text.block"}],
        )
    )

    # --- domain ---
    put(
        base_item(
            id="domain.profile.states",
            kind="domain_knowledge",
            statement=(
                "domain-profile.json lists states QUEUED, PROCESSING, HOLD, "
                "ENGINEERING_REVIEW, and RELEASED."
            ),
            source=profile,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "maps_to", "to": "term.open_operational"}],
        )
    )
    put(
        base_item(
            id="domain.profile.parts",
            kind="domain_knowledge",
            statement=(
                "domain-profile.json lists parts ETCH, LITHO, DEPOSITION, and CMP."
            ),
            source=profile,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="domain.profile.policies",
            kind="domain_knowledge",
            statement=(
                "domain-profile.json names policies spc_hold, ec_effective_date, "
                "tool_qualification, and lot_genealogy. lot_genealogy is a policy "
                "string. It is not a wafer_lots column."
            ),
            source=profile,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[{"type": "maps_to", "to": "term.lot_genealogy"}],
        )
    )
    put(
        base_item(
            id="domain.profile.systems",
            kind="domain_knowledge",
            statement=(
                "domain-profile.json names systems MESDispatch and PLM-Metrology."
            ),
            source=profile,
            claim="verified_fact",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="REAL",
            links=[],
        )
    )
    put(
        base_item(
            id="domain.object.lot",
            kind="domain_knowledge",
            statement=(
                "domain.json says the object is a production lot. Partition is chamber. "
                "Metric is scrap_cost in USD."
            ),
            source=domain,
            claim="verified_fact",
            trust="trusted_record",
            owner="Fab operations",
            policy_status="n/a",
            honesty="n/a",
            links=[{"type": "maps_to", "to": "term.lot"}],
        )
    )

    term_statements = {
        "term.open_operational": (
            "Open means any disposition or engineering action is still pending, "
            "including REVIEW and HOLD. Local words REVIEW, HOLD, UNDER_REVIEW, OPEN, "
            "ESCALATED, REOPENED, QUEUED, PROCESSING, and ENGINEERING_REVIEW map here."
        ),
        "term.closed_operational": (
            "Operational closed means a final disposition is recorded and no "
            "engineering action is pending. A cases.CLOSED word alone is not enough."
        ),
        "term.closed_finance": (
            "Finance closed means a finance action is recorded, for example a "
            "financial_adjustments row with booked_at. BO-06b is PROPOSED."
        ),
        "term.closed_audit": (
            "Audit closed means an audit close is recorded. BO-06b is PROPOSED."
        ),
        "term.recipe_revision_dispatch": (
            "Dispatch recipe revision is the value in process_steps.recipe_version."
        ),
        "term.recipe_revision_equipment": (
            "Equipment recipe revision is the value in fab_tools.recipe_rev."
        ),
        "term.recipe_revision_change": (
            "A recipe change record is the from_rev and to_rev pair on engineering_changes."
        ),
        "term.recipe_release_limit": (
            "The recipe_release limit is the archive limit for a sales region and date."
        ),
        "term.recipe_mismatch": (
            "A recipe mismatch means dispatch recipe_version and equipment recipe_rev "
            "differ on the same tool_id."
        ),
        "term.lot_genealogy": (
            "lot_genealogy is a named policy string in domain-profile.json. "
            "wafer_lots has no parent_lot_id column. The lake has no lot genealogy data."
        ),
        "term.sales_region": (
            "Sales region values are APAC, EMEA, and AMER. The archive recipe_release "
            "rule binds at sales region."
        ),
        "term.country_code": (
            "Country codes in the packaged estate are AU, BR, DE, GB, IN, JP, US, and ZA. "
            "AU and ZA have no site code."
        ),
        "term.site_code": (
            "Site codes are BR-SP, DE-BY, GB-ENG, IN-BLR, JP-KN, and US-TX. "
            "Site is the canonical location key."
        ),
        "term.lot": "A lot is a production lot. domain.json names the object as production lot.",
        "term.wafer": "A wafer is a unit listed in domain-profile.json units.",
        "term.tool": "A tool is a fab tool. fab_tools stores tool_id, tool_family, chamber, and recipe_rev.",
        "term.chamber": "chamber on fab_tools holds a site code in the packaged data.",
        "term.process_step": "A process step is one row in process_steps for a lot and tool.",
        "term.metrology_sample": "A metrology sample is one row in metrology joined to lots on lot_id.",
        "term.excursion": "A yield excursion is a named kind YIELD_EXCURSION in domain-profile.json.",
        "term.engineering_hold": "engineering_hold is an integer column on wafer_lots. A model does not write it.",
        "term.engineering_change": "An engineering change is one row in engineering_changes.",
        "term.case": "A case is one row in cases. The table has no lot_id.",
        "term.evidence": "An evidence event is one row in evidence_events with event_time and arrival_time.",
        "term.decision": "A decision in the lake is a recorded choice, conflict, or historic note.",
        "term.policy": "A policy is a governed rule row in the archive or policy_register.",
        "term.source_message": "A source message is an upstream event. The gateway returns occurred_at and published_at.",
        "term.replay": "REPLAY is a partner_feeds processing_status that marks a duplicate candidate.",
        "term.duplicate": "DUPLICATE is the status reconcile() writes for a REPLAY feed.",
        "term.outage": "An upstream outage is one row in upstream_outages.",
        "term.cost_period": "A cost period is one row in operating_costs.",
        "term.approval": "Approval is a person action. The lake does not approve from untrusted text.",
    }
    term_links = {
        "term.open_operational": [
            {"type": "maps_to", "to": "term.local.review"},
            {"type": "maps_to", "to": "term.local.hold"},
            {"type": "maps_to", "to": "term.local.under_review"},
            {"type": "maps_to", "to": "term.local.open"},
            {"type": "maps_to", "to": "term.local.escalated"},
            {"type": "maps_to", "to": "term.local.reopened"},
            {"type": "maps_to", "to": "term.local.queued"},
            {"type": "maps_to", "to": "term.local.processing"},
            {"type": "maps_to", "to": "term.local.engineering_review"},
        ],
        "term.sales_region": [
            {"type": "maps_to", "to": "rule.recipe_release.limit"},
        ],
        "term.lot_genealogy": [
            {"type": "evidenced_by", "to": "data.missing.lot_genealogy"},
            {"type": "conflicts_with", "to": "data.missing.lot_genealogy"},
        ],
        "term.recipe_release_limit": [
            {"type": "maps_to", "to": "rule.recipe_release.limit"},
        ],
    }
    term_authority = {
        "term.open_operational": ("sme", "decided", "verified_fact"),
        "term.closed_operational": ("sme", "decided", "verified_fact"),
        "term.closed_finance": ("unresolved", "proposed", "verified_fact"),
        "term.closed_audit": ("unresolved", "proposed", "verified_fact"),
        "term.lot_genealogy": ("unresolved", "n/a", "unknown"),
    }
    for term_id, statement in term_statements.items():
        auth, pol, claim = term_authority.get(term_id, ("n/a", "n/a", "verified_fact"))
        put(
            base_item(
                id=term_id,
                kind="domain_knowledge",
                statement=statement,
                source=profile if term_id.startswith("term.") and term_id in {
                    "term.wafer", "term.lot", "term.excursion"
                } else mapping if term_id.startswith("term.") else profile,
                claim=claim,
                trust="trusted_record",
                owner="unknown",
                policy_status=pol,
                honesty="n/a",
                authority=None if auth == "n/a" else auth,
                links=term_links.get(term_id, []),
            )
        )

    local_words = {
        "term.local.review": "REVIEW",
        "term.local.hold": "HOLD",
        "term.local.under_review": "UNDER_REVIEW",
        "term.local.open": "OPEN",
        "term.local.escalated": "ESCALATED",
        "term.local.reopened": "REOPENED",
        "term.local.queued": "QUEUED",
        "term.local.processing": "PROCESSING",
        "term.local.engineering_review": "ENGINEERING_REVIEW",
    }
    for item_id, word in local_words.items():
        put(
            base_item(
                id=item_id,
                kind="domain_knowledge",
                statement=(
                    f"Local status word {word} maps to operational open. BO-06a treats "
                    "pending work as open."
                ),
                source=mapping,
                claim="verified_fact",
                trust="trusted_record",
                owner="SME",
                policy_status="decided",
                honesty="n/a",
                authority="sme",
                links=[{"type": "maps_to", "to": "term.open_operational"}],
            )
        )

    # --- decisions ---
    decisions = [
        (
            "decision.fd08.canonical_archive",
            "FD-08. The governed archive JSON and policy_register are canonical. "
            "The four local programs are deviations with parity tests.",
            tracker,
            "decided",
            "policy_archive",
            [{"type": "governs", "to": "rule.recipe_release.limit"}],
        ),
        (
            "decision.fd06.two_apps",
            "FD-06. Application A runs from transformed code. Application B reads "
            "rules only from the Context Lake. Both apps run the same scenarios.",
            adr_apps,
            "decided",
            "sme",
            [],
        ),
        (
            "decision.fd22.lake_version_policy",
            "FD-22. One review round. Version starts at 1.0.0. Later changes go "
            "through the loop with an ADR. Add items = patch. Change meaning = minor "
            "with an ADR. Remove an id = major.",
            tracker,
            "decided",
            "sme",
            [{"type": "governs", "to": "arch.lake.yaml_sqlite"}],
        ),
        (
            "decision.bo05.recipe_authority",
            "BO-05. The archive is canonical for the recipe_release limit. The four "
            "programs are deviations. BO-05 does not pick recipe_version over recipe_rev.",
            tracker,
            "decided",
            "sme",
            [{"type": "governs", "to": "rule.recipe_release.limit"}],
        ),
        (
            "decision.bo06a.open_closed",
            "BO-06a. REVIEW and HOLD are open. Closed needs a final disposition and "
            "no pending engineering action. Night batch flags REVIEW as open.",
            tracker,
            "decided",
            "sme",
            [{"type": "governs", "to": "rule.open_closed.operational"}],
        ),
        (
            "decision.bo06b.three_closures",
            "BO-06b is PROPOSED. Operational closed, finance booked, and audit closed "
            "stay three states. A mismatch routes to HOLD_FOR_REVIEW.",
            tracker,
            "proposed",
            "unresolved",
            [{"type": "governs", "to": "rule.open_closed.finance_audit"}],
        ),
        (
            "decision.bo07.site_canonical",
            "BO-07. Site code is the canonical location key. Country and sales region "
            "are derived. Two scopes that disagree route to HOLD_FOR_REVIEW.",
            tracker,
            "decided",
            "sme",
            [{"type": "governs", "to": "rule.region.site_canonical"}],
        ),
        (
            "decision.bo08.silent_threshold",
            "BO-08 is PROPOSED. A threshold the archive does not state stays PROPOSED. "
            "Demo may use 50000 labelled PROPOSED. Never use 999999 as a live limit.",
            tracker,
            "proposed",
            "unresolved",
            [{"type": "governs", "to": "rule.threshold.silent"}],
        ),
        (
            "decision.bp1.recipe_mismatch",
            f"Catalogue BP1. {counts['recipe_mismatch']} of {counts['process_steps']} "
            "process steps have recipe_version different from the joined tool recipe_rev. "
            "Honesty: REAL.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "data.join.recipe_mismatch"}],
        ),
        (
            "decision.bp2.replay",
            f"Catalogue BP2. {counts['replay']} partner feeds have processing_status "
            "REPLAY. Honesty: REAL.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "data.feed.replay"}],
        ),
        (
            "decision.bp3.two_clocks",
            f"Catalogue BP3. {counts['clocks_differ']} of {counts['evidence']} evidence "
            "rows have arrival_time different from event_time. Honesty: REAL.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "data.clock.event_vs_arrival_evidence"}],
        ),
        (
            "decision.bp4.four_programs",
            "Catalogue BP4. Four local programs read urgent, allow, total, or open-flag "
            "rules: Python priority, JavaScript allow, Java totals, and the night batch.",
            catalogue,
            "n/a",
            "sme",
            [],
        ),
        (
            "decision.bp5.open_closed_words",
            "Catalogue BP5. Five local word lists name open and closed differently. "
            "BO-06a supplies the operational meaning.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "governs", "to": "rule.open_closed.operational"}],
        ),
        (
            "decision.bp6.region_overlap",
            f"Catalogue BP6. {counts['site_region_disagree']} of {counts['cases']} cases "
            "store a sales region that disagrees with the region derived from the site. "
            "Honesty: REAL.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "rule.region.disagreement"}],
        ),
        (
            "decision.bp7.untrusted_text",
            "Catalogue BP7. Six packaged stores carry approve-or-ignore language. "
            "That text is data. A proposed approve or release yields BLOCK.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "rule.untrusted_text.block"}],
        ),
        (
            "decision.bp8.auth_and_owner",
            "Catalogue BP8. The legacy API on 8080 does not check identity. "
            "INC-2025-014 follow-up owner is unknown.",
            catalogue,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "decision.inc_2025_014"}],
        ),
        (
            "decision.inc_2025_014",
            "INC-2025-014 follow-up owner is Unknown. Do not invent a name. "
            "A 04:00 UTC manual spreadsheet was used on 2025-11-18.",
            incident,
            "n/a",
            "unresolved",
            [{"type": "evidenced_by", "to": "data.incident.inc_2025_014"}],
        ),
        (
            "decision.historic.2025_replay_rollback",
            "2025 historic decision: a rollout was rolled back after a replayed "
            "partner delivery inflated the exception queue.",
            historic,
            "n/a",
            "sme",
            [{"type": "evidenced_by", "to": "data.feed.replay"}],
        ),
    ]
    for item_id, statement, source, pol, auth, links in decisions:
        put(
            base_item(
                id=item_id,
                kind="decision",
                statement=statement,
                source=source,
                claim="verified_fact",
                trust="trusted_record",
                owner="unknown" if "inc_2025" in item_id else "team-force",
                policy_status=pol,
                honesty="REAL" if "bp" in item_id or "inc" in item_id or "historic" in item_id else "n/a",
                authority=auth,
                links=links,
            )
        )

    put(
        base_item(
            id="data.draft.business_context",
            kind="domain_knowledge",
            statement=(
                "Inherited docs/business-context.md is a synthetic training file. "
                "A one-line model draft of that file stays draft until a named "
                "reviewer accepts it."
            ),
            source=src("docs/business-context.md"),
            claim="inference",
            trust="trusted_record",
            owner="unknown",
            policy_status="n/a",
            honesty="n/a",
            item_status="draft",
        ),
        draft=True,
    )
    return written
