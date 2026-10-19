# Failure semantics

| Field | Value |
|---|---|
| Stage | Phase 10 / 21 Enterprise integration. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p10a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. |
| Evidence sources | `docs/12-specs/error-handling-spec.md`; `apps/app_a/routes/recovery.py`; `docs/19-intelligence/model-configuration.md`; `docs/10-architecture/adrs/adr-langgraph-interrupt-approval.md` |
| Assumptions | Numeric retry count and backoff stay Unknown (FD-19). Recovery shows a retry control. It does not claim a time target. |
| Unresolved issues | FD-19. Measured probe latency. Whether the OPA binary is installed. |
| Residual risks | Mapping HOLD_FOR_REVIEW to HTTP 200 without a wait flag would look like a finished write. Catching `GraphRecursionError` and auto-running the draft would skip the person. |

This file names what Application A does when an adapter fails, when the graph hits a bound, and when a restart happens mid-wait.

---

## Finding

**Finding.** Failures fall into six families: identity, upstream probe, lake miss, replay miss, graph bound, and checkpoint restart. None of those families writes a record from the model.
**Evidence.** EH-01 to the recovery classes in `error-handling-spec.md`. `GraphRecursionError` in LangGraph 1.0.3 when `recursion_limit` is reached. SqliteSaver is the locked restart store.
**Impact.** Half B can map each family to one `error_class` and one next step.
**Risk.** Inventing a retry-count number would invent an SLO.
**Confidence.** High on the class names. Unknown on measured timings.
**Open questions.** FD-19 retry count. Cut-off owner for late clocks.

---

## Family table

| Family | Trigger | `error_class` | HTTP on the route | Next step | Label |
|---|---|---|---|---|---|
| Identity missing | Missing `X-Api-Key`, `X-Actor-Id`, or `X-Actor-Role` | `missing_identity` | 401 | Graph does not start | Verified Fact. EH-01 |
| Role mismatch | Role is not the mapped RT role, or actor equals proposer | `forbidden_role` | 403 | Pending wait stays | Verified Fact. EH-02. BO-09 |
| Upstream timeout | Gateway mode `timeout` or a 3-second client timeout | `upstream_timeout` | 503 on the probe. Recovery GET stays 200 with the status text | Retry control is visible. Owner stays empty until RT-06 | Verified Fact of recovery.py |
| Upstream schema | Gateway mode `schema` or body missing expected fields | `upstream_schema` | 503 on the probe | Same visible retry. No record write | Verified Fact |
| Upstream throttle | Gateway mode `rate_limit` or HTTP 429 | `upstream_rate_limit` | 503 on the probe | Same visible retry | Verified Fact |
| Lake unread | Lake REST down or empty accepted set | `abstain` when the question is a read | 200 with `verdict: ABSTAIN` | FD-14. No write | Verified Fact |
| Replay miss | `MODEL_MODE=replay` and no file for the prompt hash | `replay_miss` | 200 with abstain on the query path | Do not call Azure | Verified Fact of generate.py |
| Injection | Corpus row IC-01 to IC-06 plus approve, release, ignore-validation, or close-from-text | `blocked` | 409 | OPA-R-01. Case unchanged | Verified Fact |
| Archive silence | `evaluate_live_policy` or `rule_at` finds no row | `wait_for_person` | 409 | OPA-R-02. HOLD_FOR_REVIEW | Verified Fact. BR-05 |
| Graph recursion | LangGraph raises `GraphRecursionError` at 12 supersteps | `wait_for_person` | 409 on the agent route | Catch the error. Write an audit row. Route HOLD_FOR_REVIEW. Do not apply the draft | Engineering decision ED-P10A-01 |
| Step budget | Application counter reaches 8 model-or-tool nodes | `wait_for_person` | 409 | OPA-R-10. HOLD_FOR_REVIEW with evidence so far | Engineering decision ED-P10A-02 |
| Checkpoint restart | Process dies during `interrupt()` | none. The wait continues | After restart, GET case still shows `waiting_role` | SqliteSaver reloads the thread. Person resumes with `Command(resume=...)` | Verified Fact of the lock |
| Checkpoint file missing | File was deleted | `not_found` on the thread | 404 | Case overlay from audit rows if any. Do not invent a decision | Engineering decision |

Worked example. Minutes 36 to 39 start a recipe-mismatch wait on `PS000000016`. The process stops. Half B starts the process again. SqliteSaver still has `thread_id` equal to the correlation id. RT-03 posts `recipe_hold_or_release`. The graph resumes. The packaged step row is still unread-write until that person acts.

Worked example. A gather loop calls tools until `tool_call_count` is 8. The next planned call is skipped. `budget_exhausted` is true. OPA returns HOLD_FOR_REVIEW. The draft stays a draft.

---

## Restart contract

**Verified Fact.** Phase 10 Done test. FD-15 checkpoint store is SqliteSaver.

1. `interrupt()` runs in node `interrupt_wait`.
2. SqliteSaver writes `apps/app_a/runtime/checkpoints.sqlite3`.
3. Half B must create `apps/app_a/runtime/` if it is missing.
4. On boot, Application A opens the same file with `check_same_thread=False`.
5. `POST /api/approvals` looks up `thread_id` = `correlation_id`. If a checkpoint is waiting, it sends `Command(resume=...)`.
6. Today's in-memory `_APPROVALS` dict in `store.py` is lost on process stop. Half B rebuilds waiting state from the checkpoint and from `audit_chain` rows. That rebuild is required for the Done test.

---

## What this file does not do

This file does not set a retry count. It does not set a recovery-time target. It does not write the catch blocks.
