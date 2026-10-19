# AI incident playbook

| Field | Value |
|---|---|
| Stage | Phase 13 / 29 Incident and BCDR. Half B operations copy. SC-29-01. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-29b-doc-20261018-001 |
| Status | OPERATIONS COPY. This file is the accepted design copied into `operations/`. Application code stays as built in sub-stage 28. |
| Evidence sources | FD-19; FD-13; FD-15; FD-18; Group C; `docs/29-incident-bcdr/ai-incident-playbook.md`; `docs/28-resilience/failure-injection-results.md`; `docs/28-resilience/ai-disabled-mode.md`; `apps/app_a/routes/recovery.py`; `apps/app_a/runtime/dlq.py`; `apps/app_a/agent/tools.py`; `compose.yaml`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md` |
| Assumptions | `MODEL_MODE=replay`. One `docker compose up` still starts the seven named containers. Host ports stay 8080, 8090, 8091, 8092, 8100, 8110. BO rows that are PROPOSED stay PROPOSED. Packaged sqlite files stay `mode=ro`. |
| Unresolved issues | Numeric recovery-time and recovery-point floors stay Unknown. Availability percent stays Unknown. Dollar benefits stay Unknown. Company job titles stay Unknown. INC-2025-014 owner stays Unknown. |
| Residual risks | Deleting a parked intake row would hide the failure. Calling Azure after a replay miss would open a public-network socket. Retrying an injection BLOCK would run a write. Copying an inherited recovery-time note or recovery-point note would present an unmeasured number as a floor. |

This file names how a person walks an AI incident on this laptop product. Continuity is how work keeps going while a piece is down. Disaster recovery is how the person starts the process again after a stop. The Half B check is tabletop TT-29-01. Measured cells live in `docs/29-incident-bcdr/tabletop-results.md`. This file adds no product screen. This file adds no new HTTP route. This file adds no new sqlite table.

Engineering decision ED-P13-29A-01, authority: team-force. Control id `SC-29-01`. Check id `HB-29-01`. Tabletop id `TT-29-01`. This file is one of the four runbooks SC-29-01 copies into `operations/`.

Engineering decision ED-P13-29A-02, authority: team-force. Incident type ids `AI-INC-29-01` to `AI-INC-29-08`. Failure ids `FM-29-01` to `FM-29-08`.

Engineering decision ED-P13-29A-06, authority: team-force. The four operations copies are `ai-incident-playbook.md`, `containment-procedures.md`, `bc-plan.md`, and `dr-plan.md`. `rto-rpo.md` and `tabletop-results.md` stay in `docs/29-incident-bcdr/`.

---

## Finding

**Finding.** Application A already keeps running when the live model is off. Compose default `MODEL_MODE=replay` reads `operations/model-replay/{sha256}`. A miss returns `replay_miss` and abstains. Injection still returns HTTP 409 `blocked`. `WRITE_TOOLS` is `[]`. Sub-stage 28 already parks an invalid intake in `apps/app_a/runtime/dlq.sqlite3` and lists it on `GET /api/recovery`. Replay of that row leaves it listed. Recovery GET sets `owner_id` to `None` for case `INC-2025-014`. This file is the operations copy of that walk. Numeric recovery-time and recovery-point floors stay Unknown.
**Evidence.** FD-19. `compose.yaml` `MODEL_MODE: ${MODEL_MODE:-replay}`. `failure-injection-results.md` HB-28-01 REAL rows for `DLQ-28-BAD` `PARKED`. `recovery.py` `"owner_id": None` and `case_id="INC-2025-014"`.
**Impact.** A person follows this file, `containment-procedures.md`, `bc-plan.md`, and `dr-plan.md`. The tabletop walks the existing park list, health GET, and replay mode. No application feature is added.
**Risk.** Filling `owner_id` with a demo actor would invent a person. Writing an inherited recovery note as a floor would skip FD-19.
**Confidence.** High on the current park, replay, BLOCK, and replay-mode paths. Measured tabletop cells live in `tabletop-results.md`.
**Open questions.** INC-2025-014 owner. Company job titles. Numeric recovery-time and recovery-point floors.

---

## Locked facts this copy applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible to the person. The parked intake from sub-stage 28 stays listed. Numeric recovery-time and recovery-point floors stay Unknown until a measured run. This file invents no percent and no dollar benefit.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. Replay files live under `operations/model-replay/`. There is no third offline mode.

**Verified Fact.** FD-18. Injection returns BLOCK and drives no action. A scored AI answer cites a lake item or abstains. Numeric percent floors stay Unknown.

**Verified Fact.** FD-15. `WRITE_TOOLS` is `[]`. Recursion limit 12. Step budget 8. Checkpoint file `apps/app_a/runtime/checkpoints.sqlite3`.

**Verified Fact** of BO-01 through BO-13 that are PROPOSED. Those rows stay PROPOSED. This file invents no signer name. BO-03 working answer still sends every record-changing write through a person.

**Verified Fact.** Group C. RT-06 assigns the follow-up owner for INC-2025-014 at run time. The person's name stays Unknown. Company job titles stay Unknown.

**Verified Fact.** Injection still BLOCKS. HTTP 409. `error_class: blocked`. The model has no write tool.

---

## What is already running

**Verified Fact.**

| Piece | What it does today | Label |
|---|---|---|
| `GET /health` on 8100 | HTTP 200 `{"ok": true}` when the process is up | Verified Fact |
| `GET /api/recovery` | HTTP 200. Lists `parked_intakes`. `owner_id` is `None`. Identity required | Verified Fact of `recovery.py` |
| `POST /api/recovery/dlq/replay` | Re-runs `intake_apply` on a parked row. The row stays in the list | Verified Fact of HB-28-01 |
| Dead-letter file | `apps/app_a/runtime/dlq.sqlite3`. Tests may use `APP_A_DLQ_PATH` | Verified Fact |
| Model replay | Reads `operations/model-replay/{sha256}`. Miss abstains. Opens no Azure socket | Verified Fact |
| Agent tools | Six read names. `WRITE_TOOLS` is `[]` | Verified Fact |
| Injection | HTTP 409 `blocked`. Case unchanged | Verified Fact of Phase 12 |
| Compose `app-a` volume | Only `./operations/model-replay` mounted read-only | Verified Fact of `compose.yaml` |

Worked example. HB-28-01 parked `{"message_id": "DLQ-28-BAD"}`. `GET /api/recovery` listed `status` `PARKED`. Replay of that same body stayed `PARKED`. The row stayed in `parked_intakes`. Honesty: REAL in `failure-injection-results.md`.

Worked example. `GET /api/recovery` cites case `INC-2025-014` and returns `owner_id` `None`. This file does not put a demo actor in that field.

---

## Incident types

Engineering decision ED-P13-29A-02 continued, authority: team-force.

| Id | What failed | What the person sees | First action | Numeric floor |
|---|---|---|---|---|
| AI-INC-29-01 | Live Azure is off | Replay file or `replay_miss` abstain. Process stays up | Keep `MODEL_MODE=replay`. See `containment-procedures.md` | None invented |
| AI-INC-29-02 | Replay file missing | `error_class: replay_miss`. `verdict: ABSTAIN` | Leave the miss visible. Do not set `azure` on the laptop | None invented |
| AI-INC-29-03 | Injection write-from-text | HTTP 409 `blocked`. Case unchanged | Stop. Do not retry. Do not park as EXECUTE | None invented |
| AI-INC-29-04 | Invalid intake | `parked_intakes` lists the row. `invalid` 1 | Leave the row listed. Replay when the body is complete | None invented |
| AI-INC-29-05 | Named container exits | Compose marks unhealthy after five failed probes | `docker compose up` for that service. Seconds until health 200 stay Unknown | Restart seconds Unknown |
| AI-INC-29-06 | Missing headers or missing process key | HTTP 401 `missing_identity` or HTTP 503 `missing_server_key`. `/health` stays 200 | Send the three headers. Or set `FABPULSE_API_KEY` | None invented |
| AI-INC-29-07 | AI answer with no lake item id | `check_claim` abstains or the body is `ABSTAIN` | Leave the abstain visible | Citation percent stays Unknown |
| AI-INC-29-08 | Shared key printed on stdout | JSON log must already redact the key per sub-stage 27 | Rotate `FABPULSE_API_KEY` using the 27 secrets runbook. This file adds no vault | None invented |

Worked example for AI-INC-29-01. `MODEL_MODE=replay`. Azure variables unset. `POST /api/query` with a saved hash returns the PRECOMPUTED sentence after `check_claim`. Honesty of that sentence: PRECOMPUTED. Honesty of HTTP: REAL when the test runs. Ranking, intake, rules, park, and OPA still run.

Worked example for AI-INC-29-04. Payload `{"message_id": "DLQ-28-BAD"}` is one parked row. The person opens `GET /api/recovery` and still sees it after a same-body replay. That is the parked intake from sub-stage 28. It stays listed.

---

## Who acts

Engineering decision ED-P13-29A-07, authority: team-force. Duties use the closed role list RT-01 to RT-06. Company job titles stay Unknown. Named people stay Unknown.

| Duty on this walk | Role code | Group C duty text | Limit |
|---|---|---|---|
| Read recovery GET and the parked list | Any of RT-01 to RT-06 with identity headers | Read | No signer name is invented |
| Confirm a duplicate intake before it is dropped | RT-05 | Confirm a replay duplicate | Packaged sqlite stays unread-write |
| Assign a follow-up owner for INC-2025-014 | RT-06 at run time | Assign the follow-up owner | Owner name stays Unknown in this file |
| Approve a record-changing action | Mapped RT role for that `action_type` | Person approves | BO-03 stays PROPOSED |
| Dispose HOLD_FOR_REVIEW | RT-01 | Dispose a case that routed to wait | Proposer is never the approver |

`owner_id` on recovery GET stays `None` until RT-06 supplies a real owner at run time. This file does not write `demo-rt06-1` into that field as the incident owner.

---

## Walk — detect, contain, recover, leave the failure visible

1. Read `GET /health` on 8100. HTTP 200 means the process is up.
2. Read process `MODEL_MODE`. The Compose default is `replay`.
3. `GET /api/recovery` with `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role`. Read `error_class`, `retry_shown`, `parked_intakes`, and `owner_id`.
4. Match the body to one row in the incident-type table. Open `containment-procedures.md` for that row.
5. If `parked_intakes` has a `PARKED` row, leave it listed. Replay with `POST /api/recovery/dlq/replay` only when the body should be retried. Same body that is still invalid stays `PARKED`.
6. If `error_class` is `blocked`, stop. Do not replay that action as a write.
7. If `error_class` is `replay_miss`, keep `MODEL_MODE=replay`. Do not set `azure` on the laptop demo.
8. If `/health` fails, open `dr-plan.md` and start that named service with Compose. Seconds until the next 200 stay Unknown.
9. Leave the original failure in the parked list, in `error_class`, and in stdout `event`. Do not delete the dead-letter row.

This file is the operations copy of that walk. Recovery time stays Unknown. Recovery point stays Unknown.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery | Numeric floor |
|---|---|---|---|---|
| FM-29-01 | Live model off | Replay or abstain. Health 200 | Keep replay | Token line B1 stays 0 and 0 in the envelope |
| FM-29-02 | Replay miss | `replay_miss` abstain | Keep replay. Add a saved file only in a later rehearsal | None invented |
| FM-29-03 | Injection approve, release, ignore-validation, or close-from-text | HTTP 409 `blocked` | Leave the record. Do not retry | None invented |
| FM-29-04 | Invalid intake | Parked row on recovery GET | Replay. Row stays listed | None invented |
| FM-29-05 | Named container exits | Compose unhealthy after five failed probes | `docker compose up` for that service | Restart seconds Unknown |
| FM-29-06 | Identity miss | 401 or 503 on `/api`. Health 200 | Send headers or set the process key | None invented |
| FM-29-07 | Answer with no lake id | Abstain | Leave the abstain | Percent floor Unknown |
| FM-29-08 | Process restart during an approval wait | Checkpoint file keeps `waiting_role` | Person at the mapped RT role resumes | None invented |

---

## Dead-letter queue and replay

Language-model replay and intake park are different stores.

| Store | Path | What a miss or invalid does |
|---|---|---|
| Model replay | `operations/model-replay/{sha256}` | `replay_miss`. Abstain. No Azure |
| Intake dead-letter | `apps/app_a/runtime/dlq.sqlite3` | Row stays visible. Replay re-runs `intake_apply` |

The model does not write either store. Application A code writes the dead-letter file. A parked row is not deleted after `REPLAYED`. **Verified Fact.** FD-19. HB-28-01 REAL.

Identity misses, OPA BLOCK rows, and replay misses are not parked in the dead-letter file. Those results return on the same request.

---

## SLOs and observability

| Signal | Where it lives | What it proves | What it does not prove |
|---|---|---|---|
| `/health` HTTP 200 | Application A | The process accepted a GET | An availability percent |
| `parked_intakes` on recovery GET | `/api/recovery` | The failed intake is still listed | A recovery-time floor |
| JSON `event=intake_parked` | stdout | SC-28-01 wrote a row | A cost saving |
| JSON `model_mode=replay` | stdout | This request used replay | API p95 |
| `error_class: blocked` | HTTP 409 body | Injection stopped | A citation percent |
| `owner_id` | Recovery body | The field is present | A named owner. Value stays `None` here |

Availability, API p95, retrieval p95, recovery time, and recovery point stay Unknown. **Verified Fact.** FD-19. The 0C envelope left those cells Unknown. This file leaves them Unknown.

Do not copy an inherited availability note as a floor. Do not copy an inherited recovery-time note as a floor. Do not copy an inherited recovery-point note as a floor.

---

## Cost and the 0C envelope

SC-29-01 adds no live model call. Token line B1 in `docs/00-preflight/ai-economics/provisional-token-budget.md` stays 0 prompt tokens and 0 completion tokens when `MODEL_MODE=replay`. Lines B2 to B7 stay Unknown.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. This file claims no dollar benefit. **Verified Fact.** FD-19. BO-11 working answer stays PROPOSED.

---

## What this file does not do

This file does not add an incident HTTP route. It does not start sub-stage 30. It does not call Azure. It does not invent an availability percent. It does not invent a recovery-time floor. It does not invent a recovery-point floor. It does not invent a dollar benefit. It does not sign a Business Owner row. It does not invent a company title. It does not fill INC-2025-014 `owner_id`.
