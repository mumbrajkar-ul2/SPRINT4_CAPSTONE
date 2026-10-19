# Lake fixes — round 1

| Field | Value |
|---|---|
| Stage | Phase 5 / 11R Review, fix, and revision loop. Half B. |
| Date / version | 2026-10-18, v1.0.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5b-doc-20261018-001 |
| Status | FIXES APPLIED. One numbered round. |
| Evidence sources | First `build.py` failure log; first pytest run; read-only count of `evidence_events.payload`; jsonschema 4.26 deprecation warning |
| Assumptions | Changing the id pattern to accept the locked site-map ids does not add a field. It implements the locked ids. |
| Unresolved issues | Named reviewer for draft items is still Unknown. |
| Residual risks | A later hand edit of `enums.generated.json` would skip `build.py`. |

Each fix has a number, the before text, and the after text.

---

## Fix 1 — id pattern accepts locked site codes

**Finding.** Schema pattern `^[a-z][a-z0-9._-]+$` rejected `map.site.IN-BLR`. Half A locked that id.

**Before.** `build.py` exited with six errors of the form `'map.site.IN-BLR' does not match '^[a-z][a-z0-9._-]+$'`.

**After.** Pattern is `^[a-z][A-Za-z0-9._-]+$` on item, link, term, and rule-card schemas. The six site-map ids validate. Authority: team-force. Evidence: required ids in `knowledge-model.md`.

---

## Fix 2 — write-time checker keeps BLOCK sentences

**Finding.** The first checker treated any trusted statement that contained "approve" as an order.

**Before.** `BUILD FAIL: decision.bp7.untrusted_text.yaml: instruction language in trusted statement`. The sentence says a proposed approve yields BLOCK. A later run also failed `term.approval.yaml`, which says the lake does not approve from untrusted text.

**After.** The checker still rejects an order to approve, ignore validation, or release. It allows the sentence when the same text also says block, never, does not, data, or person.

---

## Fix 3 — unresolved demo card states HOLD_FOR_REVIEW

**Finding.** `data-contracts.md` requires a HOLD_FOR_REVIEW row on an unresolved card. `rule.threshold.demo_50000` had only the demo-display row.

**Before.** `BUILD FAIL: rule.threshold.demo_50000: unresolved card missing HOLD_FOR_REVIEW`.

**After.** The card keeps the demo row: show 50000 with policy_status proposed. It adds a live-policy row: archive silent, route HOLD_FOR_REVIEW.

---

## Fix 4 — IC-06 count is 9, honesty REAL

**Finding.** Half A left the evidence-payload count Unknown. Harvest counted 9 rows whose payload note contains ignore-controls-and-release language. Query: `mode=ro` on `enterprise_legacy.sqlite3`.

**Before.** IC-06 had `count_honesty: REAL` and no number.

**After.** IC-06 has `catalogue_count: 9` and `count_honesty: REAL`. The item `data.injection.evidence_payloads` already stated that count.

---

## Fix 5 — drop deprecated schema resolver

**Finding.** `jsonschema.RefResolver` is deprecated in this install. The first pytest run printed that warning twice.

**Before.** `build.py` imported `RefResolver` and resolved `link.schema.json` by URL.

**After.** `item.schema.json` holds the link object inline. `link.schema.json` stays as its own file for card-free link checks. `build.py` no longer imports `RefResolver`. The second pytest run printed no warning.

---

## Fix 6 — remove harvest probe scripts

**Finding.** `_probe.py` and `_probe_injection.py` were one-shot read-only counters. They are not harvest outputs.

**Before.** Those two files sat under `context-lake/harvest/`.

**After.** Both files are deleted. Harvest writers remain `generate_items.py`, `generate_cards.py`, `generate_terms.py`, `generate_eval.py`, and `run_harvest.py`.

---

## Rebuild after the fixes

`python build.py` wrote 148 items, 180 edges, 267 term rows.

`python -m pytest tests -q` returned `46 passed in 4.16s`.

No injection test leaked. Honesty: REAL.
