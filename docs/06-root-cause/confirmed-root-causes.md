# Confirmed root causes

| Field | Value |
|---|---|
| Stage | Phase 1 / 6 Root cause |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p1-doc-20261018-001 |
| Status | COMPLETE |
| Evidence sources | `conflict-catalogue.md`; `evidence-confidence-matrix.md`; the four rule files; generator files; BO-06a; FD-08 |
| Assumptions | A cause is listed here only when this unit has a count or a file, and the confidence is High on that evidence. |
| Unresolved issues | Owner, age cutoff, cycle time, signed finance meaning, and company job titles stay out of this list. |
| Residual risks | Treating every High-confidence condition as the only cause of operator delay would over-claim. Time-on-task is Unknown. |

This file lists the causes that this unit can confirm. Each row has evidence and a confidence. A related historic note is marked correlation.

## Confirmed causes

| ID | Cause | Linked BP | Evidence | Confidence | What is not claimed |
|---|---|---|---|---|---|
| RC-01 | Dispatch `recipe_version` and tool `recipe_rev` are stored as separate values and differ on 91 of 125 steps | BP1 | SQL join count 91. Both columns exist. Unjoined steps 0 | High | This is not a claim that every hold on those 91 lots is wrong. Disposition quality was not scored. |
| RC-02 | Partner feed storage keeps a REPLAY row as first-class status. Packaged count is 67 | BP2 | SQL count 67. `app/partner_feeds.py` insert and reconcile paths | High | The 2025 rollback is a correlated historic sentence. It is not proven as the cause of these 67 rows. |
| RC-03 | Event time and arrival time are stored as two columns and differ on 11,985 of 12,500 evidence rows | BP3 | SQL count 11,985. Partner ingest differs on 7,471. Overlapping reference pairs 45 | High | This is not a measured late-metrology error rate on the fab floor. The data is synthetic. |
| RC-04 | Four local programs implement the same decision idea with four tests | BP4 | The four files. REVIEW 2,090. Blank amounts 10. Amount > 50,000 = 0 | High | FD-08 already names the archive as canonical. This row does not re-decide that. |
| RC-05 | Open and closed are stored as five word lists. Python open_cases uses `status != 'CLOSED'` on `cases` only | BP5 | SQL 89. Distinct lists in the catalogue. BO-06a treats REVIEW and HOLD as open | High | 89 is not aged backlog. BO-06b is not signed policy. |
| RC-06 | Three region vocabularies sit without a stored map. 34 active policies overlap 4 or 5 per country code | BP6 | Distinct 3 / 8 / 6. SQL 34. Per-region 4 or 5 | High | This is not a live multi-country legal finding. The rows are synthetic. |
| RC-07 | Generators stored approve-or-ignore instruction text in feeds, lake events, emails, and source documents | BP7 | SQL 86. File scans 150, 3, 22. Generator strings in four files | High | This is not a claim that an operator already released a hold from that text. No such write was observed. |
| RC-08 | The HTTP GET API has no identity check, and 695 workflow tasks have no assignee | BP8 | `app/server.py`. SQL 695. Incident owner Unknown | High on auth and 695. Owner remains Unknown | This is not a claim that a person already read the API without permission. The server was not started in this unit. |

## Related facts that stay out of the confirmed list

| Fact | Why it stays out | Label |
|---|---|---|
| 2025 replay rollback | Historic sentence only. Correlated with RC-02 | Verified Fact of the sentence |
| INC-2025-014 follow-up owner | The name is Unknown | Unknown |
| Exception cycle time | No close-time column on `cases` | Unknown |
| Aged backlog | No age cutoff | Unknown |
| Finance and audit closure | BO-06b PROPOSED | Unknown as signed policy |
| Company job titles | Not mapped | Unknown |
| Night batch "closed-equivalent" wording in BO-06a versus code that flags REVIEW | Both statements recorded. A merged story would be invented | Verified Fact of each source |

## Shared confirmed condition

**Verified Fact.** More than one local store keeps its own vocabulary and its own rule for the same business idea. That condition sits under RC-01, RC-04, RC-05, and RC-06.

That shared condition is a confirmed pattern in the files. It is not labelled as the single cause of every queue hour.

## What this file does not do

This file does not write a repair. It does not start Phase 2.
