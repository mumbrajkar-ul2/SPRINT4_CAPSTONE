"""Write PRECOMPUTED replay files for the freeze set. Does not call Azure."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "context-lake") not in sys.path:
    sys.path.insert(0, str(ROOT / "context-lake"))

from operations.replay_lookup import prompt_hash  # noqa: E402

from apps.app_a.eval.sentences import (  # noqa: E402
    INJECTION_LOCATORS,
    INJECTION_QUESTIONS,
    RECOVERY_QUESTION,
    RECOVERY_SENTENCE,
    SENTENCES,
)
from apps.app_a.intelligence.canonical import canonical_prompt_bytes  # noqa: E402
from apps.app_a.intelligence.prompts import CURRENT_SEMVER, load_prompt  # noqa: E402
from apps.app_a.intelligence.retrieve import retrieve  # noqa: E402

REPLAY_DIR = ROOT / "operations" / "model-replay"
GOLDEN = ROOT / "context-lake" / "eval" / "golden-questions.yaml"
FREEZE = ROOT / "apps" / "app_a" / "eval" / "freeze-set.yaml"


def sch09(sentence: str, citations: list[str], verdict: str, block: bool = False, extra: dict | None = None) -> str:
    body = {
        "sentence": sentence,
        "citations": citations,
        "verdict": verdict,
        "block": block,
        "untrusted_quotes": [],
    }
    if extra:
        body.update(extra)
    return json.dumps(body, ensure_ascii=False)


def write_one(prompt_id: str, question: str, case_id: str, sentence: str, verdict: str, expected_ids: list[str], hints: list[str] | None = None, block: bool = False, extra: dict | None = None) -> str:
    retrieved = retrieve(question, hint_item_ids=hints or expected_ids)
    retrieved_ids = list(retrieved.get("retrieved_item_ids") or [])
    citations = [item_id for item_id in expected_ids if item_id in retrieved_ids]
    if verdict == "ABSTAIN":
        citations = [item_id for item_id in expected_ids if item_id in retrieved_ids]
    if block and "rule.untrusted_text.block" in retrieved_ids and "rule.untrusted_text.block" not in citations:
        citations.append("rule.untrusted_text.block")
    if verdict == "ABSTAIN" and not citations:
        sentence = ""
    prompt = load_prompt(prompt_id, CURRENT_SEMVER)
    canonical = canonical_prompt_bytes(
        prompt_id=prompt_id,
        semver=CURRENT_SEMVER,
        system=prompt["system"],
        retrieved_item_ids=retrieved_ids,
        question=question,
        case_id=case_id,
    )
    digest = prompt_hash(canonical)
    REPLAY_DIR.mkdir(parents=True, exist_ok=True)
    (REPLAY_DIR / digest).write_text(sch09(sentence, citations, verdict, block=block, extra=extra), encoding="utf-8")
    return digest


def main() -> None:
    golden = yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))["questions"]
    freeze = yaml.safe_load(FREEZE.read_text(encoding="utf-8"))
    written: list[str] = []
    for row in golden:
        qid = row["id"]
        verdict = row["expected_verdict"]
        block = verdict == "BLOCK"
        model_verdict = "HOLD_FOR_REVIEW" if block else verdict
        digest = write_one(
            "P-NL-QUERY",
            row["question"],
            "",
            SENTENCES[qid],
            model_verdict,
            list(row.get("expected_item_ids") or []),
            block=block,
        )
        written.append(f"{qid} {digest}")
    for row in freeze["scenario_packs"]:
        digest = write_one(
            row["prompt_id"],
            row["question"],
            row["case_id"],
            SENTENCES[row["id"]],
            row["expected_verdict"],
            list(row["expected_item_ids"]),
        )
        written.append(f"{row['id']} {digest}")
    for row in freeze["ungrounded_controls"]:
        digest = write_one(
            "P-NL-QUERY",
            row["question"],
            "",
            SENTENCES[row["id"]],
            row["expected_verdict"],
            list(row.get("expected_item_ids") or []),
        )
        written.append(f"{row['id']} {digest}")
    for row in freeze["draft_plan"]:
        digest = write_one(
            row["prompt_id"],
            row["question"],
            row["case_id"],
            SENTENCES[row["id"]],
            row["expected_verdict"],
            list(row["expected_item_ids"]),
            extra={"draft_plan": SENTENCES[row["id"]]},
        )
        written.append(f"{row['id']} {digest}")
    for ic_id, question in INJECTION_QUESTIONS.items():
        locator = INJECTION_LOCATORS[ic_id]
        digest = write_one(
            "P-NL-QUERY",
            question,
            "",
            SENTENCES[ic_id],
            "HOLD_FOR_REVIEW",
            [locator, "rule.untrusted_text.block", "decision.bp7.untrusted_text"],
            hints=[locator, "rule.untrusted_text.block", "decision.bp7.untrusted_text"],
            block=True,
        )
        written.append(f"{ic_id} {digest}")
    digest = write_one(
        "P-NL-QUERY",
        RECOVERY_QUESTION,
        "INC-2025-014",
        RECOVERY_SENTENCE,
        "ANSWER",
        ["term.outage", "decision.inc_2025_014"],
        hints=["term.outage", "decision.inc_2025_014"],
    )
    written.append(f"RECOVERY {digest}")
    print("\n".join(written))
    print(f"wrote {len(written)} replay files")


if __name__ == "__main__":
    main()
