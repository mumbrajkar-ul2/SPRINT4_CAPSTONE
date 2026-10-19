"""Run every harvest writer. Does not copy operational rows."""
from __future__ import annotations

from .generate_cards import generate_cards
from .generate_eval import generate_eval
from .generate_items import generate_items
from .generate_terms import generate_terms


def main() -> None:
    items = generate_items()
    cards = generate_cards()
    terms = generate_terms()
    generate_eval()
    print(f"harvest items={len(items)} cards={len(cards)} terms={len(terms)}")


if __name__ == "__main__":
    main()
