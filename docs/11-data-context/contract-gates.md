# Contract gates

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Specifies the five FD-07 gates. Awaits HALF_A_ACCEPTED. |
| Evidence sources | Phase 5 playbook required analysis item 2; `knowledge-model.md`; `data-contracts.md`; `docs/10-architecture/adrs/adr-opa-gates.md`; `docs/10-architecture/adrs/adr-app-b-reads-only-the-lake.md`; catalogue BP7 |
| Assumptions | Half B implements write-time and build-time as tests and as checks inside `build.py`. Model-output and read-time expose a lookup helper Half B ships with the lake. App-B-build is a contract artifact Half B produces; Phase 11 runs it against Application B. OPA rule bodies stay Phase 10. The lake still returns `block: true` on injection locators so Phase 5 injection tests can yield BLOCK. |
| Unresolved issues | Pre-commit hook install on this laptop is Unknown. Identity on read-time is later (FD-13, FD-18). |
| Residual risks | A gate that only pretty-prints YAML would let `wafer_lots.parent_lot_id` through. A gate that uses the model as the checker would let untrusted text grade itself. |

This file names five gates. Each gate has a when, a checker, and a reject list. Half B must not add a sixth gate silently. Half B must not drop one of these five.

---

## Finding

**Finding.** Five gates, at write, build, model output, read, and Application B build, are enough to keep an invented field out of the lake and out of Application B.
**Evidence.** Phase 5 prompt required analysis item 2. Locked `additionalProperties: false`. Catalogue BP7 untrusted text. Phase 4 App-B-reads-only-the-lake ADR.
**Impact.** Half B writes tests that fail when a reject condition appears. Application B later pins the build artifact.
**Risk.** Implementing only build-time would let a draft item be read as accepted.
**Confidence.** High on the five names and the reject lists. Unknown on hook install.
**Open questions.** Whether a Git pre-commit hook runs on this laptop. pytest in CI and `build.py` are the required checkers even if the hook is absent.

---

## Gate 1 — Write-time

When it runs: each time a person or a harvest script adds or changes a YAML item, term, or rule card, before that file is treated as `accepted`.

Checker in Half B: JSON Schema validation in pytest. `build.py` also runs the same check. A Git pre-commit hook is optional.

### What write-time rejects

| Reject | Worked example |
|---|---|
| Extra property | Field `parent_lot_id` on an item file |
| Missing required field | Item with no `source.sha256` |
| `kind` outside the seven | `kind: conflict` |
| Link type outside the eight | `type: relates_to` |
| `claim`, `trust`, `authority`, `item_status`, `policy_status`, or `honesty` outside its enum | `trust: maybe` |
| `business_rule` without `authority` | Archive limit item missing `authority: policy_archive` |
| `trust: trusted_code` on a feed note or email body | Partner note stored as trusted |
| `policy_status: decided` on 50,000 or 999,999 | Python cutoff marked decided |
| `item_status: accepted` while the file still sits in `items/_drafts/` | Draft published early |
| Model-drafted `statement` with no `reviewer` when moving to accepted | Doc summary accepted unsigned |
| Statement that copies a full operational row | Pasting lot `L00000012` yield columns into YAML |
| Statement that orders a model to approve, ignore, or release | Instruction text in an accepted item outside `untrusted_text` quotes |
| File stem that does not match `id` | File `foo.yaml` with `id: rule.recipe_release.limit` |

Result of a reject: the file stays out of the accepted tree. `build.py` does not copy it into SQLite.

---

## Gate 2 — Build-time

When it runs: every `build.py` run and the Half B test job.

Checker: `build.py` plus pytest.

### What build-time rejects

| Reject | Worked example |
|---|---|
| Duplicate `id` | Two files with `rule.recipe_release.limit` |
| Link `to` that is not an item | Edge to `rule.missing` |
| `source.path` missing on disk | Path `legacy_js/nope.js` |
| `source.sha256` disagrees with `sources/register.yaml` for an inherited file | Archive JSON edited after the freeze |
| Enum value absent from `enums.generated.json` | Status word `DONE` |
| Table or column named in `source.locator` but absent from `PRAGMA table_info` | `wafer_lots.parent_lot_id` |
| Any of the seven kinds missing an `accepted` item | No `dependency` item |
| Any of BP1 to BP8 missing a `decision` item | No BP7 untrusted-text item |
| Any rule card in `rule-card-design.md` missing | No silent-threshold card |
| Any mapping term in `mapping-design.md` missing | No `map.site.IN-BLR` |
| Canonical `decision_table` that uses 999,999 | JS default copied as archive limit |
| Removal of an accepted `id` without a version raise | Silent delete after 1.0.0. First Half B build has no previous lake; this check starts at the next version. |
| Empty FTS5 index when `items` is not empty | Search table not built |
| Generated SQLite written somewhere other than `context-lake/generated/context-lake.sqlite3` | Path drift |

Result of a reject: `build.py` exits non-zero. No new `manifest.json` pin.

---

## Gate 3 — Model-output

When it runs: each harvest draft that a model writes, and each later agent answer that claims a table, column, id, status word, or rule.

Checker in Half B: a lookup helper, name `check_claim`, shipped with the lake. Input is a list of `{ table, column, item_id, status_word, rule_id }`. Output is `ok` or `reject` with the unknown names. Harvest must call it on a draft. Phase 9 and Phase 10 agents call the same helper. Half B also has a fixture test that feeds the genealogy sentence below and expects reject.

### What model-output rejects

| Reject | Worked example |
|---|---|
| Unknown table | `lot_family` |
| Unknown column | `wafer_lots.parent_lot_id` |
| Unknown item id | `rule.recipe_release.limit.v2099.moon` |
| Unknown status word | `DONE` |
| Unknown site, country, or sales region | Site `IN-DEL` |
| Answer with no citation when a fact was claimed | "The limit is 18600" with empty `citations` |
| Untrusted quote used as an instruction | Feed note used to set `verdict: ANSWER` that the hold is released |
| Invented threshold | "Use 40,000 because that is safer" |
| Output that fails `read-envelope.schema.json` | Extra field `guess` |

Worked example. An agent says lot L00000012 inherits a hold from parent lot L00000003 through `wafer_lots.parent_lot_id`. `check_claim` looks up the column list. The column is absent. The answer is rejected. The helper returns that the lake has no lot genealogy data. The case routes to a person. The rejection is counted. Honesty: the missing column is REAL.

Result of a reject: the draft stays in `_drafts/`, or the agent envelope has `verdict: ABSTAIN` and does not write a record.

---

## Gate 4 — Read-time

When it runs: each REST call on port 8091 and each MCP call on port 8092, once those listeners exist. Half B ships the envelope validator even if the listeners are wired later.

Checker: envelope schema with extra properties forbidden. Untrusted text only in `untrusted_quotes`.

### What read-time rejects

| Reject | Worked example |
|---|---|
| Unknown query parameter | `?parent_lot_id=L3` |
| Extra property on the request body | `{ "rewrite": true }` |
| Write method on the lake API | PUT or POST that would change items |
| Returning `item_status: draft` as current without a draft flag | Draft limit served as 1.0.0 |
| Returning a superseded item as current without `superseded` marked | 2022 APAC limit served for 2026-06-01 |
| Putting `untrusted_text` into `statement` of the envelope without also listing it in `untrusted_quotes` | Injection sentence in the answer body as an order |
| Serving SQLite opened writable | Runtime write handle |
| `rule_at` with no site, no country, and no sales region | Empty lookup |

`rule_at` that hits silence, overlap, invalid interval, or site/region disagreement returns `verdict: HOLD_FOR_REVIEW`. That is a valid read. It is not a reject.

Injection locator plus proposed action approve, release, ignore-validation, or close-from-text returns `block: true`. That is a valid read that yields BLOCK. See `injection-corpus-design.md`.

OPA role checks are Phase 10. This gate still enforces the envelope and the untrusted-quote rule.

---

## Gate 5 — App-B-build

When it runs: before each Application B release (Phase 11). Half B produces the pin and the enum file this gate consumes.

Checker: contract tests. Pin file records `lake_version` 1.0.0 and `sqlite_sha256`.

### What App-B-build rejects

| Reject | Worked example |
|---|---|
| Application B names a table, column, status word, site, or rule id absent from the pinned `enums.generated.json` | Code references `parent_lot_id` |
| Application B imports `legacy_logic.py`, `legacy_policy.js`, `ReconcileLegacy.java`, or `shift_reconciliation.py` | Hidden second rule source |
| Application B reads the inherited repo at build time | Phase 11 exclude |
| Application B built against a lake hash that is not the pin | Stale file |
| Application B fails a canonical rule-card test | 2023 EMEA amount 18,000 expected within limit, app says fail |
| Application B uses 999,999 as a live policy number | JS default compiled in |
| Application B uses 50,000 as `policy_status: decided` | Demo cutoff compiled as signed |
| Application B merges operational, finance, and audit closed into one flag | BO-06b unsigned |

Half B writes `context-lake/generated/app-b-pin.json` with `lake_version`, `sqlite_sha256`, `enum_sha256`, and the list of canonical rule-card ids. Phase 11 fails if Application B disagrees with that pin.

---

## What every gate shares

Harvested text is data. It is never an instruction.

A silent governed source routes to `HOLD_FOR_REVIEW`. It does not guess.

Test output that a gate produced is REAL. Say so in the Half B evidence.

---

## What this file does not do

This file does not write pytest. It does not write OPA. It does not write Application B. It does not start Half B.
