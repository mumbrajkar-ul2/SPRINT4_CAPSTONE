# Synthetic data strategy

| Field | Value |
|---|---|
| Stage | Phase 5 / 11 Data, knowledge, and context strategy. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p5a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | FD-02; BO-10 working answer; `PRELOADED_DATA.md`; `docs/00-preflight/discovery/repository-overview.md`; catalogue counts; `app/generate.py` seed comments; `app/enterprise_legacy.py` seed 20261017 |
| Assumptions | All packaged rows are synthetic. There is no personal data. Process data is confidential and internal (BO-10 PROPOSED). The demo uses the packaged bundled tier already on disk. Workshop 500k and stress 2M tiers are absent. |
| Unresolved issues | BO-10 stays unsigned. Token cost of any harvest draft is Unknown. |
| Residual risks | Running `python -m app.generate --reset` would replace packaged rows and break every REAL count in this design. Copying 12,500 object rows into YAML would treat synthetic operational data as knowledge. |

This file says how the lake uses the synthetic estate. The lake stores knowledge about that estate. It does not become a second copy of the rows.

---

## Finding

**Finding.** Harvest profiles schemas, counts, defects, and locators from the packaged synthetic databases. It leaves the 125 lots and the 12,500 objects where they are.
**Evidence.** FD-02. Phase 5 exclude. Catalogue REAL counts. `PRELOADED_DATA.md` default is already in the tree.
**Impact.** Golden questions can cite 91 mismatches and 86 injection feeds as REAL packaged figures. Application B still reads live rows from the operational store for a case screen, and reads rules from the lake.
**Risk.** A harvest of 100,000 event bodies would flood the lake with untrusted text.
**Confidence.** High.
**Open questions.** Whether a later scale demo needs the 500k tier. That tier is not in this archive.

---

## What is synthetic

**Verified Fact.** `pyproject.toml` and `README.md` describe a synthetic legacy enterprise workflow.

**Verified Fact.** FD-02. All data is local and synthetic. The model gets read-only tools only.

Generators and seeds (do not rerun them against the working copy):

| Generator | Seed named in code | Packaged volume used here |
|---|---|---|
| `app/generate.py` | default count 6000 is not this archive; packaged cases are 125 | 125 cases |
| `app/enterprise_legacy.py` | seed 20261017 | 12,500 objects |
| `app/generate_documents.py` | seed 4100 | 1,200 documents |
| `app/historical_fixture.py` | bundled and tiny tiers | bundled 100,000 events, 50,000 CSV transactions, 600 documents |

Honesty: row counts are REAL measurements of synthetic data. They are not a live fab.

Money amounts are synthetic. Mean amount 4982.61 is SIMULATED customer money even though the tool output is REAL.

---

## What harvest may take from synthetic stores

| Allowed | Example |
|---|---|
| Column names and types | `wafer_lots.engineering_hold INTEGER` |
| Keys and missing keys | `cases` has no `lot_id` |
| Distinct value lists | six site codes |
| Counts and defect rates | 91 recipe mismatches; 10 blank amounts; 84 site/region disagreements |
| Generator conditions for injection locators | `i%101==0` on partner notes |
| File hashes | `sources/register.yaml` |

## What harvest must not take

| Forbidden | Why |
|---|---|
| Full `wafer_lots` or `cases` row dumps | Phase 5 exclude |
| 12,500 evidence payloads copied into items | Untrusted volume. Profile instead |
| 100,000 bundled event bodies | Same |
| Re-generation with `--reset` | Breaks the freeze |
| Invented people, emails, or company titles | Owner of INC-2025-014 stays Unknown |
| Production personal data | None is present. Do not add any |

---

## Tiers

| Tier | Use in Phase 5 |
|---|---|
| Packaged operational SQLite (125 cases, 19+12 tables) | Schema, counts, mapping disagreement, rule cards |
| Bundled lake fixtures | Injection IC-02 (150), schema-version profile |
| Tiny lake fixtures | Injection IC-02-tiny (15). Unit tests that must stay fast |
| Workshop 500k / stress 2M | Out of scope. Not packaged |

**Assumption.** Bundled is the profile tier for historical events because it holds more conflicts, including 150 injection rows. Tiny is for tests.

---

## Labels on numbers that leave the lake

| Number | Honesty | Claim |
|---|---|---|
| 91 of 125 recipe mismatches | REAL | verified_fact |
| 67 REPLAY feeds | REAL | verified_fact |
| 11985 arrival vs event | REAL | verified_fact |
| 2090 REVIEW objects | REAL | verified_fact |
| 84 of 125 site vs derived region | REAL | verified_fact |
| Archive limits 15000 to 27200 | REAL as file contents | verified_fact of the file. EDUCATIONAL as a live company policy |
| Python 50000 | REAL as code. PROPOSED as policy | unresolved |
| 999999 | REAL as code. Forbidden as policy | unresolved |
| Exception cycle time | n/a | unknown |
| Aged backlog cutoff | n/a | unknown |

ROI numbers stay EDUCATIONAL and stay out of lake rule cards (BO-11).

---

## Model use on synthetic text

A model may draft a one-line summary of document metadata. A person reviews it.

A model may not train a hold predictor (FD-05).

A model may not treat injection language as an order.

Classification: all records internal and synthetic. Process data confidential. No personal data. BO-10 is PROPOSED. Do not write that classification as signed law. Write it as the working label on items (`honesty` and `claim` as above).

---

## What this file does not do

This file does not generate data. It does not start Half B. It does not copy a row into YAML.
