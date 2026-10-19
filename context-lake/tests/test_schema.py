"""Write-time schema tests. Output is REAL."""
from __future__ import annotations

from pathlib import Path

import yaml

from build import item_validator, load_yaml, term_validator

LAKE = Path(__file__).resolve().parents[1]


def _sample_item() -> dict:
    path = LAKE / "items" / "rules" / "rule.recipe_release.limit.yaml"
    return load_yaml(path)


def test_accepted_items_match_schema() -> None:
    validator = item_validator()
    errors = []
    for path in (LAKE / "items").rglob("*.yaml"):
        if path.name.endswith(".card.yaml"):
            continue
        item = load_yaml(path)
        errors.extend(f"{path.name}: {e.message}" for e in validator.iter_errors(item))
    assert errors == []


def test_extra_property_rejected() -> None:
    item = _sample_item()
    item["parent_lot_id"] = "L00000003"
    validator = item_validator()
    assert list(validator.iter_errors(item))


def test_missing_sha256_rejected() -> None:
    item = _sample_item()
    del item["source"]["sha256"]
    validator = item_validator()
    assert list(validator.iter_errors(item))


def test_kind_conflict_rejected() -> None:
    item = _sample_item()
    item["kind"] = "conflict"
    validator = item_validator()
    assert list(validator.iter_errors(item))


def test_relates_to_link_rejected() -> None:
    item = _sample_item()
    item["links"] = [{"type": "relates_to", "to": "rule.recipe_release.limit"}]
    validator = item_validator()
    assert list(validator.iter_errors(item))


def test_business_rule_requires_authority() -> None:
    item = _sample_item()
    del item["authority"]
    validator = item_validator()
    assert list(validator.iter_errors(item))


def test_terms_match_schema() -> None:
    validator = term_validator()
    errors = []
    for path in (LAKE / "semantic-layer").glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        docs = payload if isinstance(payload, list) else [payload]
        for term in docs:
            errors.extend(f"{path.name}: {e.message}" for e in validator.iter_errors(term))
    assert errors == []


def test_file_stem_matches_id() -> None:
    mismatches = []
    for path in (LAKE / "items").rglob("*.yaml"):
        if path.name.endswith(".card.yaml"):
            continue
        item = load_yaml(path)
        if path.stem != item["id"]:
            mismatches.append((path.name, item["id"]))
    assert mismatches == []
