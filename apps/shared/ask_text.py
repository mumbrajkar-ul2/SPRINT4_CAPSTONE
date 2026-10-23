"""The Ask question is the same on both apps.

The sentence lists facts from the record. It leaves out the user name, the fab access label, and the clock.
"""
from __future__ import annotations

HINTS = {
    "case": [
        "term.case",
        "term.lot",
        "term.tool",
        "term.source_message",
        "term.engineering_hold",
    ],
    "lot": [
        "term.lot",
        "term.lot_genealogy",
        "term.process_step",
        "term.engineering_change",
        "term.recipe_revision_dispatch",
        "term.recipe_revision_equipment",
        "term.recipe_mismatch",
        "data.join.recipe_mismatch",
        "decision.bp1.recipe_mismatch",
        "data.missing.lot_genealogy",
    ],
    "tool_drift": ["term.tool", "term.chamber", "term.excursion", "domain.profile.policies"],
    "outlier_wafer": ["term.metrology_sample", "term.wafer", "term.excursion", "domain.profile.policies"],
    "unqualified_supplier": ["domain.profile.parts", "term.tool", "domain.profile.policies"],
    "lot_genealogy": [
        "term.lot_genealogy",
        "term.engineering_change",
        "term.recipe_revision_change",
        "data.missing.lot_genealogy",
        "decision.bp1.recipe_mismatch",
    ],
}


def hint_ids(subject: str, fault_id: str | None = None) -> list[str]:
    if subject == "fault":
        return list(HINTS.get(fault_id or "", []))
    return list(HINTS.get(subject, []))


def build_question(subject: str, record: dict, mode: str) -> tuple[str, list[str]]:
    facts: list[str] = []
    if subject == "case":
        for label, key in (("status", "status"), ("severity", "severity"), ("site", "site_code")):
            if record.get(key):
                facts.append(f"{label} {record[key]}")
    elif subject == "lot":
        if record.get("measured_yield") is not None:
            facts.append(f"yield {record['measured_yield']}")
        facts.append(f"hold {record.get('engineering_hold')}")
        if record.get("tool_id"):
            facts.append(f"tool {record['tool_id']}")
        if record.get("chamber"):
            facts.append(f"chamber {record['chamber']}")
        if record.get("dispatch_recipe"):
            facts.append(f"dispatch recipe {record['dispatch_recipe']}")
        if record.get("equipment_recipe"):
            facts.append(f"equipment recipe {record['equipment_recipe']}")
        if record.get("effective_ecn"):
            facts.append(f"effective ecn {record['effective_ecn']}")
        if record.get("recipe_mismatch"):
            facts.append("recipe ids differ")
    elif subject == "fault":
        if record.get("fault_id"):
            facts.append(f"fault {record['fault_id']}")
        if record.get("count") is not None:
            facts.append(f"count {record['count']}")
        if record.get("required_role"):
            facts.append(f"role {record['required_role']}")
        if record.get("recommended_action"):
            facts.append(record["recommended_action"])
        for finding in (record.get("findings") or [])[:3]:
            facts.append(str(finding)[:80])
    facts = facts[:8]
    verb = "Explain" if mode == "explain" else "Draft a plan for"
    question = f"{verb} these facts. " + " ".join(facts)
    return question, facts
