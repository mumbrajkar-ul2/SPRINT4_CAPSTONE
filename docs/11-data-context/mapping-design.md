# Mapping design

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Specifies FD-09. Awaits HALF_A_ACCEPTED. |
| Evidence sources | BO-07 DECIDED; catalogue BP5 and BP6; `app/generate.py` site and region lists; `app/enterprise_legacy.py` tenant and country lists; read-only SQLite on 2026-10-18; `domain-profile.json`; `contracts/decision-policies-archive.json`; `policy_register` rows |
| Assumptions | Site-to-country derivation uses the ISO-style prefix already present in the six site codes. That derivation is an engineering map, `authority: team-force`, because BO-07 says country is derived and does not publish a table. AU and ZA have no site code. Those cases stay `HOLD_FOR_REVIEW`. |
| Unresolved issues | Sales-region for ZA is Unknown. `TENANT-SOUTH` is a fourth tenant name. The archive has only APAC, EMEA, AMER. BO-06b stays PROPOSED, so finance-closed and audit-closed stay separate terms. |
| Residual risks | Using `cases.region` as the archive key would ignore the site. Using `organizations.tenant` as a region would put Brazil under `TENANT-APAC`. Treating 999,999 as a region default would hide a no-match. |

This file is the cross-system map for region, status, and recipe. Site code is the canonical location key (BO-07). Country and sales region are derived. The most specific scope wins. Two scopes that disagree route to `HOLD_FOR_REVIEW`.

---

## Finding

**Finding.** Packaged `cases` assign `site` and `region` independently. 84 of 125 cases have a stored sales region that disagrees with the region derived from the site. The map must use the site, then compare, then wait on disagreement.
**Evidence.** Read-only `SELECT site, region, COUNT(*) FROM cases GROUP BY site, region` on 2026-10-18. `app/generate.py` lines 9-11 and 30: `rng.choice(sites)` and `rng.choice(regions)` are separate calls. BO-07.
**Impact.** `rule_at` keyed only on `cases.region` would pick the wrong archive row for most packaged cases. `rule_at` keyed on site, with a disagreement check, matches BO-07.
**Risk.** Skipping the disagreement check would hide BP6 on the demo data.
**Confidence.** High on the 84 count and on the generator. The prefix-to-country table is Inference.
**Open questions.** ZA sales region. AU has no site. Company names for the six sites are Unknown.

Honesty on the 84 count: REAL.

---

## Region map

### Three vocabularies already stored

| Vocabulary | Values | Where | Count |
|---|---|---|---:|
| Six site codes | BR-SP, DE-BY, GB-ENG, IN-BLR, JP-KN, US-TX | `cases.site`, `fab_tools.chamber` | 6 |
| Eight country codes | AU, BR, DE, GB, IN, JP, US, ZA | `operational_objects.region`, `organizations.region`, `policy_register.region` | 8 |
| Three sales regions | APAC, EMEA, AMER | `cases.region`, archive JSON `region` | 3 |

**Verified Fact.** Catalogue BP6. No stored map joins APAC to IN or JP.

**Verified Fact.** A fourth tenant name `TENANT-SOUTH` exists on `organizations`. The archive has no SOUTH region.

**Verified Fact.** `organizations` pairing on 2026-10-18: `TENANT-APAC` holds IN and BR. `TENANT-EMEA` holds DE and GB. `TENANT-AMER` holds US and ZA. `TENANT-SOUTH` holds AU and JP. Brazil under `TENANT-APAC` shows the tenant name is not a country map. Do not harvest tenant as canonical region.

### Canonical key

**Verified Fact.** BO-07. The site code is the canonical key. Country and sales region are derived from the site. A policy binds at the most specific scope and inherits upward. Where two scopes disagree, the case routes to review.

Specificity order, most specific first:

1. Site code
2. Country code
3. Sales region (APAC, EMEA, AMER)

`recipe_release` in the archive binds at sales region. `policy_register` binds at country code. A site-level policy row does not exist in either governed source. Inheritance means: start at the site, derive country, derive sales region, then read the row at the finest governed scope that source has.

### Derived table Half B must write as terms

`authority: team-force` on the derivation. Claim: Inference. `policy_status: decided` for the six site rows because BO-07 requires a derived country. `policy_status: proposed` is wrong here: this is an engineering map, not a Business Owner number.

| Site | Derived country | Derived sales region | Why the prefix |
|---|---|---|---|
| IN-BLR | IN | APAC | Site string starts with IN |
| JP-KN | JP | APAC | Site string starts with JP |
| US-TX | US | AMER | Site string starts with US |
| BR-SP | BR | AMER | Site string starts with BR |
| DE-BY | DE | EMEA | Site string starts with DE |
| GB-ENG | GB | EMEA | Site string starts with GB |

Term ids: `map.site.IN-BLR`, and one per site.

### Country with no site

| Country | Site | Sales region | Route |
|---|---|---|---|
| AU | none in packaged data | Unknown as a signed value. Archive has APAC as a possible bucket | `HOLD_FOR_REVIEW` |
| ZA | none in packaged data | Unknown. Tenant pairing puts ZA under `TENANT-AMER`. That pairing is a generator artifact. | `HOLD_FOR_REVIEW` |

Do not invent a site for AU or ZA.

### Disagreement on packaged cases

Stored `cases.region` versus derived sales region, 2026-10-18, honesty REAL:

| Site | Derived region | Cases | Stored match | Stored disagree |
|---|---|---:|---:|---:|
| BR-SP | AMER | 25 | 9 | 16 |
| DE-BY | EMEA | 30 | 10 | 20 |
| GB-ENG | EMEA | 25 | 9 | 16 |
| IN-BLR | APAC | 13 | 4 | 9 |
| JP-KN | APAC | 16 | 6 | 10 |
| US-TX | AMER | 16 | 3 | 13 |
| Total |  | 125 | 41 | 84 |

Worked example. Site IN-BLR, stored region AMER, date 2026-06-01. Canonical site derives APAC. Archive 2026 APAC limit is 25,000. Stored AMER would have pointed at 27,200. The two scopes disagree. `rule_at` returns `HOLD_FOR_REVIEW`. It does not pick 25,000 or 27,200.

When the caller supplies only a site, and no stored sales region is in the lookup, use the derived region. That path is how Application B evaluates a rule when the input is a site code.

When the caller supplies site and a sales region, and they disagree, wait.

When the caller supplies only a country code with no site, derive sales region from the six-row table if the country is on that table. AU and ZA wait.

When the caller supplies only a sales region, use the archive at that region, and record that site was absent. Application B still shows the missing site as a gap. A later owner may require site on every lookup. That tighter rule is not signed here. Open question.

### Register versus archive

`recipe_release` limits and `FAB-RULE-*` thresholds are different families. Do not map 25,000 onto `FAB-RULE-0`.

If both families match one object and their numbers disagree, `HOLD_FOR_REVIEW`.

If two active `policy_register` rows match one country on the lookup date, `HOLD_FOR_REVIEW`. Catalogue BP6: 4 or 5 active rows per country. Worked example: US has five active rows. One US object in the night batch becomes five joined rows.

If `valid_from` is after `valid_to`, `HOLD_FOR_REVIEW`. Worked example: `POL-0039` AU `FAB-RULE-4`, `valid_from` 2025-01-01, `valid_to` 2024-12-31, `active` 1. Honesty: REAL.

---

## Status map

### Five local word lists

**Verified Fact.** Catalogue BP5.

| List | Words | Source |
|---|---|---|
| 1. Cases | OPEN, UNDER_REVIEW, CLOSED, ESCALATED, REOPENED | `cases.status` |
| 2. Policy exceptions | OPEN, WAIVED, BLOCKED, REVIEW | `policy_exceptions.outcome` |
| 3. Enterprise objects | OPEN, REVIEW, HOLD, CLOSED, REOPENED, ESCALATED | `operational_objects.status` |
| 4. Domain profile queues | QUEUED, PROCESSING, HOLD, ENGINEERING_REVIEW, RELEASED | `domain-profile.json` `states` |
| 5. Archive notes | not reviewed, provisionally cleared, escalated, reopened | `app/archived_documents.py` |

Packaged exception outcomes on 2026-10-18, honesty REAL: OPEN 59, REVIEW 57, BLOCKED 54, WAIVED 54.

Packaged object status, honesty REAL: OPEN 2090, REVIEW 2090, HOLD 2083, CLOSED 2079, REOPENED 2079, ESCALATED 2079.

### Canonical operational meaning

**Verified Fact.** BO-06a DECIDED.

A case is **open** while any disposition or engineering action is still pending, including REVIEW and HOLD.

A case is **closed** only when a final disposition is recorded and no engineering action is pending.

`legacy_batch/shift_reconciliation.py` flags HOLD and REVIEW. Its comment treats REVIEW as open. That matches BO-06a.

### Map each local word to an operational bucket

Canonical term ids: `term.open_operational`, `term.closed_operational`.

| Local word | System | Operational bucket | Authority | Notes |
|---|---|---|---|---|
| OPEN | cases, exceptions, objects | open | sme | Pending work |
| UNDER_REVIEW | cases | open | sme | Same meaning as REVIEW |
| REVIEW | exceptions, objects | open | sme | BO-06a |
| HOLD | objects, domain profile | open | sme | BO-06a |
| ESCALATED | cases, objects, archive notes | open | sme | Pending |
| REOPENED | cases, objects, archive notes | open | sme | Pending |
| QUEUED | domain profile | open | sme | Pending |
| PROCESSING | domain profile | open | sme | Pending |
| ENGINEERING_REVIEW | domain profile | open | sme | Pending |
| not reviewed | archive notes | open | sme | Pending |
| CLOSED | cases, objects | closed only if a final disposition is recorded and no engineering action is pending | sme | `cases` has no engineering-action column and no `lot_id`. A cases.CLOSED word is a local disposition word. Confirming BO-06a closed needs an explicit engineering-action-clear field. When that field is absent, the operational closed flag is Unknown and the case routes to `HOLD_FOR_REVIEW` for closure claims. Queue counts that only need the SME open set still treat REVIEW and HOLD as open. |
| RELEASED | domain profile | closed-candidate for the queue | unresolved | Domain queue released is not signed as finance-closed or audit-closed. |
| WAIVED | exceptions | disposition recorded; operational closed only if no engineering action is pending | unresolved | No engineering-action field on `policy_exceptions`. |
| BLOCKED | exceptions | open | inference | A blocked exception is still pending a later action. If a later owner says BLOCKED is a final refusal, change the term through the lake loop. |
| provisionally cleared | archive notes | open | sme | Not a final disposition |

Python `open_cases` uses `status != 'CLOSED'` on `cases` only. That count is 89. Honesty: REAL. It is a local test. It is not the SME aged-backlog number. Aged-backlog cutoff stays Unknown.

### Three closure states (BO-06b)

BO-06b is PROPOSED, not signed. Half B writes three terms and does not merge them.

| Term id | Meaning | Source | policy_status |
|---|---|---|---|
| `term.closed_operational` | BO-06a closed | sme | decided |
| `term.closed_finance` | A finance action is recorded, for example a `financial_adjustments` row with `booked_at` | unresolved | proposed |
| `term.closed_audit` | An audit close is recorded | unresolved | proposed |

Operational closure does not book finance and does not close audit. A row that is operationally closed and missing a finance or audit mark routes to `HOLD_FOR_REVIEW` when the question is finance or audit. Do not write that routing as signed policy. Label it PROPOSED.

---

## Recipe map

### Local fields

| Field | System | What it holds |
|---|---|---|
| `process_steps.recipe_version` | Dispatch / MESDispatch path | Revision the step ran |
| `fab_tools.recipe_rev` | Equipment | Revision listed on the tool |
| `engineering_changes.from_rev`, `to_rev`, `effective_at`, `approval_state` | Change record | Intended revision change |

**Verified Fact.** 91 of 125 steps have `recipe_version` different from the joined `recipe_rev`. Honesty: REAL.

**Verified Fact.** BO-05. The governed archive is canonical for the `recipe_release` **limit**. The four programs are deviations.

BO-05 does not pick `recipe_version` over `recipe_rev`. When the two revision strings differ, both are shown. A Process Engineer at RT-03 approves a hold or a release. The lake records the mismatch as a `data_relationship` and a `decision` item. The lake does not pick a winning string.

Canonical terms:

| Term id | Definition |
|---|---|
| `term.recipe_revision_dispatch` | Value in `process_steps.recipe_version` |
| `term.recipe_revision_equipment` | Value in `fab_tools.recipe_rev` |
| `term.recipe_revision_change` | Pair `from_rev` / `to_rev` on `engineering_changes` |
| `term.recipe_release_limit` | Archive `limit` for `recipe_release` at a sales region and date |
| `term.recipe_mismatch` | Dispatch revision and equipment revision differ on the same `tool_id` |

`domain-profile.json` names policy `lot_genealogy`. `wafer_lots` has no `parent_lot_id`. Term `term.lot_genealogy` exists with claim `unknown` and statement that the column is absent. A model that cites `wafer_lots.parent_lot_id` fails the model-output gate.

---

## Semantic-layer files Half B must write

Under `context-lake/semantic-layer/`:

- `region.md` and `region.yaml`
- `status.md` and `status.yaml`
- `recipe.md` and `recipe.yaml`
- plus one YAML file per Intent 9.2 term listed in `data-contracts.md`

Each YAML `local_names` list names Python, JavaScript, Java, night batch, MESDispatch, and PLM-Metrology when that system has a word for the term. If a system is silent, the local name is `absent` and claim is `verified_fact` of the absence.

---

## What this file does not do

This file does not write the YAML maps. It does not invent a ZA sales region. It does not sign BO-06b. It does not start Half B.
