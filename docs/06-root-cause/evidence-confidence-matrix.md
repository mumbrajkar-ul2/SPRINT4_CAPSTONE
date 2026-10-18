# Evidence and confidence matrix

| Field | Value |
|---|---|
| Stage | Phase 1 / 6 Root cause |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | All BP queries in `docs/05-current-state/conflict-catalogue.md`; file reads listed per row |
| Assumptions | High confidence means the count or the file text was observed in this unit. Medium means a reading of more than one file. Low means a single historic sentence. |
| Unresolved issues | Rows marked Unknown stay Unknown. |
| Residual risks | Raising an Inference to Verified Fact would hide a gap. |

This matrix scores each contributing condition. Correlation is marked where two facts sit together and the write path is not proven.

## Matrix

| ID | Condition | Evidence | Kind | Confidence | Causation note |
|---|---|---|---|---|---|
| C-BP1-count | 91 recipe mismatches | SQL join count 91 of 125 | Verified Fact | High | Direct count. |
| C-BP1-gen | Two generators pick different revision lists | `app/enterprise_data.py` R01-R04. `app/domain_data.py` R01-R03 | Verified Fact of the lists. Inference that they produced the packaged 91 | High on the lists. Medium on the production claim | Correlation of generator code with packaged rows. Seeded generate was not re-run. |
| C-BP2-count | 67 REPLAY rows | SQL count 67 | Verified Fact | High | Direct count. |
| C-BP2-code | Generator inserts REPLAY copies | `app/partner_feeds.py` `i%127==0` | Verified Fact | High | Direct write path in code. |
| C-BP2-hist | 2025 rollback after replay | `docs/historic-decisions.md` | Verified Fact of the sentence | High on the sentence. Low as a cause of the current 67 | Correlation only. |
| C-BP3-ev | 11,985 arrival != event | SQL count 11,985 of 12,500 | Verified Fact | High | Direct count. |
| C-BP3-pf | 7,471 ingest != source | SQL count 7,471 of 8,567 | Verified Fact | High | Direct count. |
| C-BP3-ref | 45 overlapping version pairs | SQL count 45 | Verified Fact | High | Direct count. |
| C-BP4-py | Python 50,000 cutoff | `app/legacy_logic.py`. Amount > 50000 count 0 | Verified Fact | High | Direct file and count. |
| C-BP4-js | JS limit * 1.05 and 999,999 | `legacy_js/legacy_policy.js` | Verified Fact | High | Direct file. JS was not executed. |
| C-BP4-java | Java drops blanks | `ReconcileLegacy.java`. Blank amount_text 10 | Verified Fact | High | Direct file and count. Java was not executed. |
| C-BP4-batch | Night batch flags REVIEW | Code plus SQL 2,090 | Verified Fact | High | Direct file and count. |
| C-BP5-89 | 89 cases not CLOSED | SQL count 89 | Verified Fact | High | Direct count. Python test, not SME aged backlog. |
| C-BP5-lists | Five status word lists | Distinct values and `domain-profile.json` | Verified Fact | High | Direct lists. |
| C-BP5-sme | REVIEW and HOLD are open | BO-06a DECIDED | Verified Fact of the decision | High | Policy fact. Not a data cause. |
| C-BP5-fin | Finance and audit closure | BO-06b PROPOSED | Unknown as signed policy | High that the row is unsigned | Do not treat as signed. |
| C-BP6-34 | 34 active policies | SQL count 34. 4 or 5 per region | Verified Fact | High | Direct count. Matches plan range. |
| C-BP6-vocab | Three region vocabularies | Distinct 3 / 8 / 6 | Verified Fact | High | Direct counts. |
| C-BP6-join | Night batch join multiplies rows | Code plus 23,168 joined flags vs 6,279 distinct objects | Verified Fact | High | Direct code and counts. |
| C-BP7-86 | 86 untrusted feeds | SQL count 86 | Verified Fact | High | Direct count. Matches plan. |
| C-BP7-150 | 150 untrusted lake events | File scan of bundled JSONL | Verified Fact | High | Direct count. Matches plan. Not the `events` table (0). |
| C-BP7-3 | 3 untrusted emails | File scan of `.eml` | Verified Fact | High | Direct count. Matches plan. |
| C-BP7-22 | 22 untrusted source documents | File scan of JSONL | Verified Fact | High | Direct count. Matches plan. |
| C-BP8-auth | No API auth | `app/server.py` | Verified Fact | High | Direct file. |
| C-BP8-695 | 695 unassigned tasks | SQL count 695 | Verified Fact | High | Direct count. |
| C-BP8-inc | INC-2025-014 owner | Incident file | Unknown person | High that the file says unknown | Do not invent a name. |
| C-KPI-cyc | Exception cycle time | Columns checked; no close time on `cases` | Unknown | High that the value is Unknown | No number written. |
| C-KPI-age | Aged backlog | No cutoff in archive or `policy_register` | Unknown | High that the value is Unknown | 89 is not aged. |

## How confidence was set

High: this unit ran the query or read the file.

Medium: this unit read two sources and joined them by inference.

Low: a single historic sentence used as a cause.

No row uses Low as the only support for a confirmed cause in `confirmed-root-causes.md`.

## What this file does not do

This file does not raise an Unknown to a number. It does not label correlation as causation.
