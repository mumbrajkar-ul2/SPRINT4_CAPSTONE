"""Write semantic-layer Markdown and YAML terms."""
from __future__ import annotations

from .common import LAKE_ROOT, SITE_MAP, dump_yaml

SL = LAKE_ROOT / "semantic-layer"

ABSENT = {"system": "all-silent", "field_or_word": "absent", "meaning": "This system has no local word for the term."}


def _term(
    term_id: str,
    name: str,
    definition: str,
    local_names: list,
    *,
    authority: str = "n/a",
    policy_status: str = "n/a",
    claim: str = "verified_fact",
    maps_to_term: str | None = None,
    source_path: str = "docs/11-data-context/mapping-design.md",
) -> dict:
    row = {
        "term_id": term_id,
        "canonical_name": name,
        "definition": definition,
        "local_names": local_names,
        "authority": authority,
        "policy_status": policy_status,
        "claim": claim,
        "source_path": source_path,
    }
    if maps_to_term:
        row["maps_to_term"] = maps_to_term
    return row


def _locals(*pairs: tuple[str, str, str]) -> list[dict]:
    return [{"system": s, "field_or_word": w, "meaning": m} for s, w, m in pairs]


def generate_terms() -> list[str]:
    SL.mkdir(parents=True, exist_ok=True)
    ids: list[str] = []

    region_terms = [
        _term(
            "term.site_code",
            "site code",
            "Site code is the canonical location key. The six codes are BR-SP, DE-BY, GB-ENG, IN-BLR, JP-KN, and US-TX.",
            _locals(
                ("cases", "site", "Stored site code"),
                ("fab_tools", "chamber", "Packaged chamber holds a site code"),
                ("Python", "absent", "legacy_logic.py has no site argument"),
                ("JavaScript", "absent", "legacy_policy.js keys on archive region"),
                ("Java", "absent", "ReconcileLegacy.java has no site field"),
                ("night batch", "absent", "The job joins on country, not site"),
                ("MESDispatch", "absent", "No site field in domain-profile.json"),
                ("PLM-Metrology", "absent", "No site field in domain-profile.json"),
            ),
            authority="sme",
            policy_status="decided",
        ),
        _term(
            "term.country_code",
            "country code",
            "Country is derived from the site prefix. Packaged country codes are AU, BR, DE, GB, IN, JP, US, and ZA. AU and ZA have no site.",
            _locals(
                ("policy_register", "region", "Country code"),
                ("operational_objects", "region", "Country code"),
                ("organizations", "region", "Country code"),
                ("Python", "absent", "No country argument"),
                ("JavaScript", "absent", "Uses APAC, EMEA, AMER"),
                ("Java", "absent", "No country field"),
                ("night batch", "operational_objects.region", "Join key"),
                ("MESDispatch", "absent", "No country list"),
                ("PLM-Metrology", "absent", "No country list"),
            ),
            authority="sme",
            policy_status="decided",
            maps_to_term="term.site_code",
        ),
        _term(
            "term.sales_region",
            "sales region",
            "Sales regions are APAC, EMEA, and AMER. recipe_release binds at this scope.",
            _locals(
                ("cases", "region", "Stored sales region, assigned independently of site"),
                ("archive", "region", "APAC, EMEA, AMER"),
                ("Python", "absent", "No region argument"),
                ("JavaScript", "region", "Archive region argument"),
                ("Java", "absent", "No region field"),
                ("night batch", "absent", "Joins on country"),
                ("MESDispatch", "absent", "No sales region"),
                ("PLM-Metrology", "absent", "No sales region"),
            ),
            authority="sme",
            policy_status="decided",
            maps_to_term="term.site_code",
        ),
    ]
    for site, derived in SITE_MAP.items():
        region_terms.append(
            _term(
                f"map.site.{site}",
                f"site {site}",
                f"Site {site} derives country {derived['country']} and sales region {derived['sales_region']}.",
                _locals(
                    ("cases", "site", site),
                    ("mapping", "derived_country", derived["country"]),
                    ("mapping", "derived_sales_region", derived["sales_region"]),
                    ("Python", "absent", "No site map in legacy_logic.py"),
                    ("JavaScript", "absent", "No site map in legacy_policy.js"),
                    ("Java", "absent", "No site map in ReconcileLegacy.java"),
                    ("night batch", "absent", "No site map in the night batch"),
                    ("MESDispatch", "absent", "No site map"),
                    ("PLM-Metrology", "absent", "No site map"),
                ),
                authority="sme",
                policy_status="decided",
                claim="inference",
                maps_to_term="term.site_code",
            )
        )
    dump_yaml(SL / "region.yaml", region_terms)
    (SL / "region.md").write_text(
        (
            "# Region terms\n\n"
            "Site code is the canonical location key. Country and sales region "
            "are derived from the site. Two scopes that disagree wait for a person.\n"
            "AU and ZA have no site. Those lookups wait. Do not invent a site.\n"
        ),
        encoding="utf-8",
    )
    ids.extend(t["term_id"] for t in region_terms)

    status_terms = [
        _term(
            "term.open_operational",
            "open operational",
            "A case is open while any disposition or engineering action is pending, including REVIEW and HOLD.",
            _locals(
                ("cases", "OPEN", "Pending work"),
                ("cases", "UNDER_REVIEW", "Same meaning as REVIEW"),
                ("operational_objects", "REVIEW", "Open"),
                ("operational_objects", "HOLD", "Open"),
                ("Python", "status != CLOSED", "Local open_cases count"),
                ("JavaScript", "absent", "No open flag"),
                ("Java", "absent", "No open flag"),
                ("night batch", "HOLD and REVIEW", "Flagged as outstanding"),
                ("MESDispatch", "QUEUED PROCESSING HOLD ENGINEERING_REVIEW", "Domain profile states"),
                ("PLM-Metrology", "absent", "No status list"),
            ),
            authority="sme",
            policy_status="decided",
        ),
        _term(
            "term.closed_operational",
            "closed operational",
            "A case is closed only when a final disposition is recorded and no engineering action is pending.",
            _locals(
                ("cases", "CLOSED", "Local disposition word. Engineering action is absent, so closure stays Unknown until confirmed."),
                ("operational_objects", "CLOSED", "Local status word"),
                ("Python", "CLOSED", "Returns archive"),
                ("JavaScript", "absent", "No closed flag"),
                ("Java", "absent", "No closed flag"),
                ("night batch", "CLOSED", "Not flagged for status"),
                ("MESDispatch", "RELEASED", "Domain queue released is not signed as operational closed"),
                ("PLM-Metrology", "absent", "No closed word"),
            ),
            authority="sme",
            policy_status="decided",
        ),
        _term(
            "term.closed_finance",
            "closed finance",
            "Finance closed means a finance action is recorded, for example booked_at on financial_adjustments. BO-06b is PROPOSED.",
            _locals(
                ("financial_adjustments", "booked_at", "Finance timestamp"),
                ("Python", "absent", "No finance flag"),
                ("JavaScript", "absent", "No finance flag"),
                ("Java", "absent", "No finance flag"),
                ("night batch", "absent", "No finance flag"),
                ("MESDispatch", "absent", "No finance flag"),
                ("PLM-Metrology", "absent", "No finance flag"),
            ),
            authority="unresolved",
            policy_status="proposed",
        ),
        _term(
            "term.closed_audit",
            "closed audit",
            "Audit closed means an audit close is recorded. BO-06b is PROPOSED.",
            _locals(
                ("Python", "absent", "No audit flag"),
                ("JavaScript", "absent", "No audit flag"),
                ("Java", "absent", "No audit flag"),
                ("night batch", "absent", "No audit flag"),
                ("MESDispatch", "absent", "No audit flag"),
                ("PLM-Metrology", "absent", "No audit flag"),
            ),
            authority="unresolved",
            policy_status="proposed",
        ),
    ]
    dump_yaml(SL / "status.yaml", status_terms)
    (SL / "status.md").write_text(
        (
            "# Status terms\n\n"
            "REVIEW is open. HOLD is open. Closed needs a final disposition and "
            "no pending engineering action. Finance closed and audit closed stay "
            "separate terms. BO-06b is still PROPOSED.\n"
        ),
        encoding="utf-8",
    )
    ids.extend(t["term_id"] for t in status_terms)

    recipe_terms = [
        _term(
            "term.recipe_revision_dispatch",
            "dispatch recipe revision",
            "Value in process_steps.recipe_version.",
            _locals(
                ("MESDispatch", "process_steps.recipe_version", "Dispatch revision"),
                ("Python", "absent", "No recipe field"),
                ("JavaScript", "absent", "No recipe field"),
                ("Java", "absent", "No recipe field"),
                ("night batch", "absent", "No recipe field"),
                ("PLM-Metrology", "absent", "Equipment uses recipe_rev"),
            ),
            authority="sme",
            policy_status="decided",
        ),
        _term(
            "term.recipe_revision_equipment",
            "equipment recipe revision",
            "Value in fab_tools.recipe_rev.",
            _locals(
                ("PLM-Metrology", "fab_tools.recipe_rev", "Equipment revision"),
                ("Python", "absent", "No recipe field"),
                ("JavaScript", "absent", "No recipe field"),
                ("Java", "absent", "No recipe field"),
                ("night batch", "absent", "No recipe field"),
                ("MESDispatch", "absent", "Dispatch uses recipe_version"),
            ),
            authority="sme",
            policy_status="decided",
        ),
        _term(
            "term.recipe_revision_change",
            "recipe revision change",
            "Pair from_rev and to_rev on engineering_changes.",
            _locals(
                ("engineering_changes", "from_rev", "Prior revision"),
                ("engineering_changes", "to_rev", "Intended revision"),
                ("Python", "absent", "No change pair"),
                ("JavaScript", "absent", "No change pair"),
                ("Java", "absent", "No change pair"),
                ("night batch", "absent", "No change pair"),
                ("MESDispatch", "absent", "No change pair"),
                ("PLM-Metrology", "absent", "No change pair"),
            ),
        ),
        _term(
            "term.recipe_release_limit",
            "recipe release limit",
            "Archive limit for recipe_release at a sales region and date.",
            _locals(
                ("archive", "limit", "USD limit"),
                ("JavaScript", "threshold(region,year)", "Reads the archive, then multiplies by 1.05"),
                ("Python", "amount > 50000", "Different cutoff, not this limit"),
                ("Java", "absent", "No recipe_release limit"),
                ("night batch", "policy_register.threshold", "Different family"),
                ("MESDispatch", "absent", "No limit field"),
                ("PLM-Metrology", "absent", "No limit field"),
            ),
            authority="policy_archive",
            policy_status="decided",
        ),
        _term(
            "term.recipe_mismatch",
            "recipe mismatch",
            "Dispatch revision and equipment revision differ on the same tool_id.",
            _locals(
                ("process_steps", "recipe_version", "Dispatch side"),
                ("fab_tools", "recipe_rev", "Equipment side"),
                ("Python", "absent", "No mismatch test"),
                ("JavaScript", "absent", "No mismatch test"),
                ("Java", "absent", "No mismatch test"),
                ("night batch", "absent", "No mismatch test"),
                ("MESDispatch", "legacy note", "domain-profile.json says a recipe revision field differs"),
                ("PLM-Metrology", "legacy note", "Same profile sentence"),
            ),
            authority="sme",
            policy_status="decided",
        ),
        _term(
            "term.lot_genealogy",
            "lot genealogy",
            "Named policy string in domain-profile.json. wafer_lots has no parent_lot_id. The lake has no lot genealogy data.",
            _locals(
                ("domain-profile", "lot_genealogy", "Policy name only"),
                ("wafer_lots", "absent", "No parent_lot_id column"),
                ("Python", "absent", "No parent lot"),
                ("JavaScript", "absent", "No parent lot"),
                ("Java", "absent", "No parent lot"),
                ("night batch", "absent", "No parent lot"),
                ("MESDispatch", "lot_genealogy", "Policy string"),
                ("PLM-Metrology", "absent", "No parent lot"),
            ),
            authority="unresolved",
            claim="unknown",
        ),
    ]
    dump_yaml(SL / "recipe.yaml", recipe_terms)
    (SL / "recipe.md").write_text(
        (
            "# Recipe terms\n\n"
            "Dispatch stores recipe_version. Equipment stores recipe_rev. "
            "When the two strings differ, both values are shown. "
            "The lake does not pick a winner.\n"
        ),
        encoding="utf-8",
    )
    ids.extend(t["term_id"] for t in recipe_terms)

    intent_terms = [
        ("term.lot", "lot", "A production lot. domain.json names the object as production lot."),
        ("term.wafer", "wafer", "A wafer is a unit listed in domain-profile.json."),
        ("term.tool", "tool", "A fab tool stored in fab_tools."),
        ("term.chamber", "chamber", "chamber on fab_tools holds a site code in the packaged data."),
        ("term.process_step", "process step", "One process_steps row for a lot and a tool."),
        ("term.metrology_sample", "metrology sample", "One metrology row joined to lots on lot_id."),
        ("term.excursion", "excursion", "Kind YIELD_EXCURSION in domain-profile.json."),
        ("term.engineering_hold", "engineering hold", "Integer column wafer_lots.engineering_hold. A model does not write it."),
        ("term.engineering_change", "engineering change", "One engineering_changes row."),
        ("term.case", "case", "One cases row. The table has no lot_id."),
        ("term.evidence", "evidence", "One evidence_events row with event_time and arrival_time."),
        ("term.decision", "decision", "A recorded choice, conflict, or historic note in the lake."),
        ("term.policy", "policy", "A governed rule row in the archive or policy_register."),
        ("term.source_message", "source message", "An upstream event. The gateway returns occurred_at and published_at."),
        ("term.replay", "replay", "partner_feeds.processing_status REPLAY. Duplicate candidate."),
        ("term.duplicate", "duplicate", "Status reconcile() writes for a REPLAY feed."),
        ("term.outage", "outage", "One upstream_outages row."),
        ("term.cost_period", "cost period", "One operating_costs row."),
        ("term.approval", "approval", "A person action. The lake does not approve from untrusted text."),
    ]
    for term_id, name, definition in intent_terms:
        payload = _term(
            term_id,
            name,
            definition,
            _locals(
                ("Python", "absent", "No dedicated local word in legacy_logic.py"),
                ("JavaScript", "absent", "No dedicated local word in legacy_policy.js"),
                ("Java", "absent", "No dedicated local word in ReconcileLegacy.java"),
                ("night batch", "absent", "No dedicated local word in the night batch"),
                ("MESDispatch", "domain-profile", definition),
                ("PLM-Metrology", "domain-profile", definition),
            ),
            source_path="Project_Intent.md",
        )
        dump_yaml(SL / f"{term_id}.yaml", payload)
        ids.append(term_id)
    return ids
