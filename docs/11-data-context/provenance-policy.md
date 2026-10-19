# Provenance policy

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `knowledge-model.md`; `sources/register.yaml`; FD-22; FD-08; catalogue BP3 and BP7; `Execution_Plan.md` section 11 |
| Assumptions | SHA-256 in `sources/register.yaml` (1,590 files, 2026-10-18) is the freeze Half B checks. Harvest recorded_at for this lake is 2026-10-18 unless Half B harvests on a later day, in which case it writes that day. |
| Unresolved issues | Named reviewer for model-drafted items is Unknown. Audit-chain row schema is Phase 10 (FD-23). |
| Residual risks | Mixing `recorded_at` with `valid_time` would answer GQ-01 with the harvest date. Treating a feed note as a source of truth would break BP7. |

This file says how each lake fact traces to a file, a hash, a validity window, and a claim label. Harvested text is data. It is never an instruction.

---

## Finding

**Finding.** Source path, SHA-256, two time fields, claim, trust, authority, and lake version are the provenance a later builder needs.
**Evidence.** `knowledge-model.md` required fields. Phase 0 register. FD-22 version starts at 1.0.0. BP3 two clocks on operational events, reused here as two clocks on knowledge.
**Impact.** Golden questions can cite an item id and a file. Application B can pin a hash.
**Risk.** A missing hash lets a later edit of `legacy_policy.js` go unnoticed.
**Confidence.** High.
**Open questions.** Reviewer name. FD-23 audit columns.

---

## Source

Every accepted item names `source.path` and `source.sha256`.

Inherited files must match `sources/register.yaml`. Capstone-root files (`Decision_Tracker.md`, Phase 4 ADRs) are hashed at harvest and stored on the item. Half B adds those hashes to `generated/manifest.json` under `extra_sources`.

`source.lines` is required for the four rule programs. Worked example. JavaScript 1.05 lives at `legacy_js/legacy_policy.js` lines 4-5.

`source.locator` names `table.column` when the fact is a schema or a count.

---

## Two time fields

| Field | Meaning | Worked example |
|---|---|---|
| `valid_time.from` / `valid_time.to` | When the fact applied in the business | 2023 EMEA limit: 2023-01-01 to 2023-12-31 |
| `recorded_at` | When the lake learned the fact | 2026-10-18 |

`rule_at` uses `valid_time`. Lake history uses `recorded_at` and `lake_version`.

Do not copy operational `arrival_time` into `recorded_at`. Those clocks belong to evidence events. They have their own data items.

---

## Claim, trust, authority, honesty

| Label set | Values | Who sets it |
|---|---|---|
| claim | verified_fact, inference, assumption, unknown | Harvest. Schema and counts are verified_fact. Prefix-to-country is inference. Cycle time is unknown. |
| trust | trusted_code, trusted_record, untrusted_text | Code files and tests are trusted_code. Archive JSON and COUNT queries are trusted_record. Feeds, emails, HTML, document bodies, `source_claim` are untrusted_text. |
| authority | policy_archive, sme, unresolved | Required on business_rule |
| honesty | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL, n/a | Counts from packaged SQLite are REAL. ROI stays EDUCATIONAL and does not belong in a rule card. |
| policy_status | decided, proposed, n/a | PROPOSED tracker rows stay proposed |

A model-drafted sentence starts as `inference` and `item_status: draft`. A person sets reviewer and date before `accepted`.

---

## Version

**Verified Fact.** FD-22 DECIDED. One review round before Phase 6. Version starts at 1.0.0. A later change goes through the loop and raises the version with an ADR.

Engineering step rule, `authority: team-force`, so Half B does not invent it:

| Change | Version step | Example |
|---|---|---|
| First accepted lake | 1.0.0 | Half B after 11R |
| Add items or terms, meaning of existing ids unchanged | raise patch, for example 1.0.1 | A later phase adds a missing term through the open-question channel |
| Change the meaning of an id, change a canonical number, or remove an id | raise minor or major with an ADR. Removing an id raises major, for example 2.0.0. Changing a canonical limit raises minor, for example 1.1.0 | Archive reread after a real policy change |

The YAML in Git is the source of truth. If generated SQLite disagrees, rebuild or write an ADR.

Open questions from later phases return here. They do not patch SQLite by hand.

---

## Untrusted text

Untrusted locators are listed in `injection-corpus-design.md`.

Provenance still records path and hash. Retrieval puts the quote in `untrusted_quotes`. Proposed approve or release yields BLOCK.

Do not store untrusted text in `owner`, `authority`, or `id`.

---

## What a citation must contain

A golden-question hit cites item `id`. An explanation in a later phase cites item `id` plus `source.path`. A screen that shows 18,600 cites `rule.recipe_release.limit.v2023.emea`.

A screenshot alone is not provenance (`Project_Intent.md` section 11.3).

---

## What this file does not do

This file does not write `lake-version.md`. That file is Half B after 11R. This file does not start Half B.
