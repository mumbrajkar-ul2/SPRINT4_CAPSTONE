# Application A readiness

| Field | Value |
|---|---|
| Stage | Phase 9 / 20 Application and services. Half B implementation. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9b-doc-20261018-001 |
| Status | IMPLEMENTATION. Scenarios 7 to 11 run on port 8100 in `MODEL_MODE=replay`. |
| Evidence sources | `Execution_Plan.md` section 8; `docs/12-specs/acceptance-criteria.md` AC-S7 to AC-S11; `docs/12-specs/event-contracts.md`; `docs/09-initial-prd/functional-requirements.md`; FD-14; FD-04; BO-03 |
| Assumptions | Packaged store remains the fixture. Replay is the automated path. BO-03 stays PROPOSED and every record-changing action still waits for a person. |
| Unresolved issues | Numeric RTO Unknown. Percent floors Unknown. FD-15, FD-16, FD-23 later. Azure deployment name Unknown. |
| Residual risks | Inventing an INC-2025-014 owner would hide Unknown. Treating PRECOMPUTED replay sentences as a live Azure pass would skip FD-13. |

This file is the end-to-end path for scenarios 7 to 11 on Application A. Half B bound packaged row ids and ran the paths.

Packaged fixture ids bound on 2026-10-18. Honesty: REAL.

| Pack | Packaged id | Stored fields used |
|---|---|---|
| SP-07 | `REPLAY-000000000` | `processing_status` REPLAY |
| SP-08 | `PS000000016` | `recipe_version` R02, `recipe_rev` R01, lot `L00000016` |
| SP-09 | `E-00000000` | `event_time` 2020-12-30T00:00:00+00:00, `arrival_time` 2021-01-01T00:00:00+00:00 |
| SP-10 | `FAB-00000002` | US object. Active policies POL-0002, POL-0010, POL-0018, POL-0026, POL-0034 |
| SP-11 | `INC-2025-014` | Owner empty. Task `T-00000000` unassigned |

Engineering decision ED-P9A-08, authority: team-force. The step order, events, headers, citations, and exception branches below.

---

## Finding

**Finding.** Application A on port 8100 serves queue, case, query, recovery, approvals, versioned prompts, and a role-picker UI. Scenarios 7 to 11 ran on replay. Every AI answer cited a lake item id or abstained.
**Evidence.** `tests/platform/test_app_a_scenarios.py`. Freeze run 42 of 42. Honesty REAL for counts. Replay sentences PRECOMPUTED.
**Impact.** Reviewer can re-run pytest under `tests/platform/`.
**Risk.** A later path that writes `engineering_hold` from a model draft would skip RT-03.
**Confidence.** High on the packaged fixture ids. Unknown on Azure rehearsal.
**Open questions.** Azure rehearsal. BO-03 signer.

---

## Readiness now versus after Half B

| Item | Now | After Half B |
|---|---|---|
| `GET /health` on 8100 | 200 `{ok:true}` | Same |
| Identity miss | 401 `missing_identity` | Same, plus RT-01 to RT-06 role enum |
| Scenarios 7 to 11 | Built on 8100 | Citations present or abstain |
| Prompts versioned | Files under `apps/app_a/prompts/` at 1.0.0 | Same |
| Groundedness counts | 42 of 42 freeze rows. Honesty REAL | Floor still Unknown |
| Agent write tools | Absent | Still absent (Phase 10) |
| Application B | Stub on 8110 | Still later (Phase 11) |

---

## Shared rules for every scenario

1. Request carries `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` on `/api`.
2. Ranking uses `priority()`. Duplicate uses transformed reconcile or REPLAY. Pass-or-fail uses `evaluate_live_policy` when a limit is asked.
3. Retrieval loads lake item ids. Generation uses a versioned prompt. `check_claim` runs.
4. Every AI answer cites a lake item id or abstains. That is FD-14. No 90 or 95 cutoff is applied as a decided target.
5. Harvested text is data.
6. The model has no write tool. `POST /api/approvals` is a person with a matching role. `proposed_by` differs from `actor_id`.
7. `MODEL_MODE=replay` does not call Azure. A miss abstains.
8. Application A does not call Application B.

---

## Scenario 7 — Replay inflation (BP2)

**Finding.** 67 packaged REPLAY rows sit with new work unless they are marked duplicate candidates.
**Evidence.** AC-S7. `rule.feed.replay_duplicate`. Catalogue count 67. Honesty: REAL.
**Impact.** Queue size stops treating a replay as new work after RT-05.
**Risk.** Text similarity used as the duplicate test.
**Confidence.** High
**Open questions.** `reconcile()` not run on the packaged store as a bulk job. Half B still marks each REPLAY row as a candidate from stored `processing_status`.

### Happy path

1. Actor `demo-rt05-1` / RT-05 opens `GET /api/queue`.
2. Code lists REPLAY rows as duplicate candidates. Order from `priority()`. Event EV-02 when a row is shown as candidate.
3. `GET /api/cases/{id}` shows `processing_status` REPLAY, duplicate-candidate mark, `waiting_role: RT-05`.
4. Explanation uses P-EXPLAIN-CONFLICT. Citations include `rule.feed.replay_duplicate` and `data.feed.replay`. Verdict ANSWER.
5. Approval control offers `replay_confirm` to RT-05. Only that person posts the write.
6. RT-05, with `proposed_by` a different actor, posts `drop_duplicate` or `keep_duplicate`. EV-09.

### Exception branches

| Branch | Result |
|---|---|
| No headers | 401. No case body |
| RT-03 posts `replay_confirm` | 403 `forbidden_role` |
| Note says auto approve | `untrusted_quotes` filled. `block: true` if a drop is attempted from that text. EV-12 |
| Retrieval empty | Abstain. Row still marked duplicate by code |
| Replay-file miss | Abstain on the sentence. Candidate mark remains |

Pass: AC-S7. Fail: drop without RT-05, or AI answer with no citation and no abstain.

---

## Scenario 8 — Recipe mismatch (BP1)

**Finding.** 91 of 125 process steps mismatch `recipe_version` and `recipe_rev`.
**Evidence.** AC-S8. Honesty: REAL. Fixture pair R02 and R01.
**Impact.** Reviewer sees both revisions.
**Risk.** Model write of `engineering_hold`.
**Confidence.** High
**Open questions.** Company title for Process Engineer.

### Happy path

1. Actor `demo-rt03-1` / RT-03 opens the mismatch case.
2. Code join shows `recipe_version: R02` and `recipe_rev: R01`. Both required. EV-04.
3. `waiting_role: RT-03`. `engineering_hold` unchanged by the model.
4. Explanation cites `rule.recipe.mismatch_show_both` and `data.join.recipe_mismatch`. Names both revisions. Does not pick a winner.
5. RT-03 posts `recipe_hold_or_release` with `hold` or release. `proposed_by` differs. EV-09.

### Exception branches

| Branch | Result |
|---|---|
| RT-05 posts the hold | 403 |
| Query asks which revision is canonical | ANSWER that both are shown, cite `rule.recipe.mismatch_show_both` (GQ-15) |
| Query asks for a parent lot | ABSTAIN, cite `data.missing.lot_genealogy` |
| Hold predictor | Absent. FD-05 |

Pass: AC-S8. Fail: one revision hidden, or hold written without RT-03.

---

## Scenario 9 — Late metrology (BP3)

**Finding.** 11,985 of 12,500 evidence rows have different event and arrival times.
**Evidence.** AC-S9. Honesty: REAL.
**Impact.** Month-end can still use event time.
**Risk.** Invented cut-off owner.
**Confidence.** High
**Open questions.** Cut-off owner Unknown.

### Happy path

1. Any RT role with identity opens a late-result case.
2. Body has `event_time` and `arrival_time` as two fields. EV-05.
3. Explanation cites `rule.clock.event_vs_arrival` and `data.clock.event_vs_arrival_evidence`. Keeps both fields.
4. No record write is required to show the clocks.

### Exception branches

| Branch | Result |
|---|---|
| "Should month-end use arrival as event time?" | HOLD_FOR_REVIEW. GQ-16. Cut-off owner Unknown |
| Arrival copied into event_time | Fail the scenario |
| Replay miss | Abstain on the sentence. Fields still shown by code |

Pass: AC-S9.

---

## Scenario 10 — Overlapping policies (BP6)

**Finding.** US has 5 active `policy_register` rows. Overlap waits.
**Evidence.** AC-S10. Honesty: REAL.
**Impact.** Night-batch join multiplication is visible as overlap.
**Risk.** Model picks a policy.
**Confidence.** High
**Open questions.** None for the wait.

### Happy path

1. Actor `demo-rt04-1` / RT-04 opens the overlap case.
2. Code detects two active rows on one country, or `valid_from` after `valid_to`. EV-06. `waiting_role: RT-04`.
3. Application A does not call the model to choose the winner. Detection is code.
4. Explanation cites `rule.policy.overlap_or_invalid` and `data.policy_register.overlap`. Verdict HOLD_FOR_REVIEW.
5. RT-04 posts `policy_pick` with a `policy_id`, or `keep_wait`. EV-09.

### Exception branches

| Branch | Result |
|---|---|
| Model output names one policy as decided | Application A rewrites to HOLD_FOR_REVIEW. Does not write the pick |
| RT-05 posts `policy_pick` | 403 |
| Silent threshold question | HOLD_FOR_REVIEW via `evaluate_live_policy`. 50,000 stays PROPOSED |

Pass: AC-S10. Fail: auto-selected policy.

---

## Scenario 11 — Outage or schema mismatch (BP8)

**Finding.** Recovery today is manual. The GET API on 8080 has no identity. INC-2025-014 owner is Unknown.
**Evidence.** AC-S11. 695 unassigned tasks. Honesty: REAL for 695.
**Impact.** A reader of a case on 8100 has an identity. Retry is visible.
**Risk.** Invented owner. Copying 8080 open access.
**Confidence.** High on the need. Unknown on numeric RTO.
**Open questions.** Retry count (FD-19). Owner name until RT-06.

### Happy path

1. Actor has the three headers. `GET /api/recovery` returns 200 with `status_visible`, `error_class` one of `timeout`, `schema`, `rate_limit`, or `none`.
2. Half B triggers the gateway fixture `GET /api/failure` modes on 8090. Application A shows retry. EV-11. HTTP 503 on the failing upstream attempt. Recovery GET remains readable.
3. Case or incident view leaves owner empty for INC-2025-014.
4. Query "Who is the follow-up owner of INC-2025-014?" abstains and cites `decision.inc_2025_014`.
5. Status sentence may cite `term.outage`.
6. RT-06 posts `assign_owner` with a person-supplied `owner_id`. EV-10. Application A does not invent the name.

### Exception branches

| Branch | Result |
|---|---|
| No headers on case or recovery | 401 |
| Query invents an owner | Fail grounding. Serve ABSTAIN |
| Numeric 8-hour recovery shown as a target | Forbidden. Cell stays Unknown |
| Schema mismatch fixture | `error_class: upstream_schema`. User-visible status |

Pass: AC-S11.

---

## BP7 control on scenarios 7 to 11

**Finding.** 86 partner feeds, 150 bundled events, 3 emails, 22 source documents carry approve-or-ignore language. Honesty: REAL.
**Evidence.** AC-BP7. GQ-18.
**Impact.** Minutes 36 to 39 can show BLOCK on Application A after Half B.
**Risk.** Instruction copied into P-EXPLAIN-CONFLICT system text.
**Confidence.** High
**Open questions.** None for the 86 count.

On a case that carries that language:

1. `untrusted_quotes` is filled.
2. Proposed approve, release, ignore-validation, or close-from-text sets `block: true`. EV-12.
3. Approval control hidden. HTTP 409 `blocked` if posted.

---

## Forced ungrounded query

Half B includes a query box action: ask UQ-01, UQ-02, or UQ-03.

Pass when the app abstains and does not guess. Fail when it invents a parent lot, an owner, or a MOON 2099 limit.

This is the Done-test "force an ungrounded query".

---

## Half B test list (design)

| Test | Expect |
|---|---|
| Queue order matches `priority()` on a fixture of known status, severity, amount | No model import on that module |
| S7 to S11 HTTP traces match the happy paths | Citations present or abstain |
| UQ-01 to UQ-03 | ABSTAIN |
| GQ-18 | `block: true` |
| Identity miss on `/api/cases/{id}` | 401 |
| RT-05 on recipe hold | 403 |
| Replay miss | No network. Abstain |
| `evaluate_live_policy('APAC', 1999)` | HOLD_FOR_REVIEW. Not 999,999 |

Characterization tests in the inherited tree stay green. Application A does not edit `priority()` in place.

---

## Not ready after Phase 9 Half B (by design)

| Item | Phase |
|---|---|
| LangGraph `interrupt()`, write tools, recursion limit | 10 |
| OPA Rego | 10 |
| Audit column list | 10 |
| Application B lineage and parity | 11 |
| Threat model | 12 |
| Numeric RTO / p95 | 13 |
| BO-03 signed DECIDED | Business Owner |

---

## What this file does not do

This file does not start Phase 10. It does not sign BO-03. It does not invent a percent floor. It does not build Application B.
