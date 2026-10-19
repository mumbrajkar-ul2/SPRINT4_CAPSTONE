# Containment procedures

| Field | Value |
|---|---|
| Stage | Phase 13 / 29 Incident and BCDR. Half B operations copy. SC-29-01. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-29b-doc-20261018-001 |
| Status | OPERATIONS COPY. This file is the accepted design copied into `operations/`. No new stop route. No new BLOCK rule. |
| Evidence sources | FD-19; FD-13; FD-18; FD-10; `docs/29-incident-bcdr/containment-procedures.md`; `docs/28-resilience/fallback-matrix.md`; `docs/28-resilience/ai-disabled-mode.md`; `docs/24-security-privacy/prompt-injection-controls.md`; `docs/27-hardening/secrets-hardening.md`; `apps/app_a/agent/tools.py`; `apps/app_a/runtime/dlq.py`; `compose.yaml` |
| Assumptions | `MODEL_MODE=replay`. Azure variables stay unset for this walk. BO rows that are PROPOSED stay PROPOSED. Harvested strings stay data. |
| Unresolved issues | Live Azure containment behaviour stays Unknown. Named owner for INC-2025-014 stays Unknown. Numeric recovery-time and recovery-point floors stay Unknown. |
| Residual risks | Setting `MODEL_MODE=azure` because a hash has no file would open a public-network socket. Retrying BLOCK would run a write. Deleting a parked row would hide the failure. |

This file names how the person stops an AI incident from going further. Each step uses a path that already exists. This file adds no new stop route. This file adds no new BLOCK rule. Recovery time stays Unknown. Recovery point stays Unknown.

Engineering decision ED-P13-29A-05, authority: team-force. Containment default `CON-29-01`. Keep `MODEL_MODE=replay`. Do not set `azure` on the laptop demo. Do not delete a parked intake row. Do not retry an injection BLOCK. Those four limits are engineering defaults. They are not Business Owner policy. They are not a recovery-time floor.

---

## Finding

**Finding.** Four stops already exist. Replay mode keeps the live model off the network. A replay miss abstains. OPA BLOCK returns HTTP 409 on the same request. The dead-letter file keeps an invalid intake listed after replay. Containment for this sub-stage is those four stops, written as a walk a person can follow. This copy adds no fifth stop in application code.
**Evidence.** FD-19. FD-13. `WRITE_TOOLS = []`. HB-28-01 REAL. Phase 12 HTTP 409 `blocked`. `dlq.py` never deletes a row.
**Impact.** The tabletop records that the four stops still hold during TT-29-01.
**Risk.** Parking an injection approve as a later EXECUTE would skip FD-10.
**Confidence.** High on the four current stops. Unknown on a live Azure duration.
**Open questions.** Azure variable values. INC-2025-014 owner.

---

## Locked facts this copy applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. A failed intake stays visible. The parked intake from sub-stage 28 stays listed.

**Verified Fact.** FD-13. Modes `replay` and `azure`. No third offline mode. Ollama is not a product mode.

**Verified Fact.** Injection still BLOCKS. The model has no write tool.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. BO-03 working answer still sends every record-changing write through a person.

---

## Containment default CON-29-01

| Limit | What the person does | Evidence |
|---|---|---|
| Keep replay | Leave `MODEL_MODE=replay` in Compose and in the process | FD-13. FD-19 |
| Do not set `azure` on the laptop | A missing replay file stays `replay_miss` | `ai-disabled-mode.md` |
| Do not delete a parked row | `GET /api/recovery` still lists `DLQ-28-BAD` after replay | HB-28-01 REAL |
| Do not retry BLOCK | One HTTP 409. Case unchanged | Phase 12. `WRITE_TOOLS` is `[]` |

Worked example. Partner note says auto approve. `proposed_action=approve`. OPA returns BLOCK. HTTP 409. The next step is stop. There is no replay of that action as EXECUTE.

Worked example. Intake `{"message_id": "DLQ-28-BAD"}` is `PARKED`. Containment is to leave that row in `parked_intakes`. Replay of the same body stays `PARKED`. The original failure stays visible.

---

## Procedure by incident type

| Incident | Containment steps | What stays up |
|---|---|---|
| AI-INC-29-01 Live Azure off | Confirm `MODEL_MODE=replay`. Confirm Azure variables unset. `GET /health` 200 | Ranking, intake, rules, park, OPA, identity, lake reads |
| AI-INC-29-02 Replay miss | Leave `error_class: replay_miss`. Do not import `complete_azure` onto the network path | Same as the row above. Query abstains |
| AI-INC-29-03 Injection | Leave HTTP 409. Do not open `interrupt()`. Do not call `record_approval`. Do not park the payload as EXECUTE | Case row unchanged. Packaged `engineering_hold` unchanged |
| AI-INC-29-04 Invalid intake | Leave the dead-letter row. Replay only when fields are complete. Packaged `legacy.sqlite3` stays unread-write | Recovery GET HTTP 200. Health 200 |
| AI-INC-29-05 Container exit | Start that named service. Do not rewrite packaged sqlite to "fix" health | Other healthy listeners |
| AI-INC-29-06 Identity | Missing headers: send `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role`. Missing process key: set `FABPULSE_API_KEY` and restart the four gated listeners. `/health` stays 200 | Health GET. Port 8080 and 8090 stay ungated |
| AI-INC-29-07 No lake cite | Leave `verdict: ABSTAIN`. Do not invent a lake item id | Query path HTTP 200 with abstain |
| AI-INC-29-08 Key on stdout | Follow `docs/27-hardening/secrets-hardening.md`. Rotate the process key. This file adds no vault product | Gated `/api` uses the new key after restart |

---

## What containment does not change

Port 8080 still serves case reads with no identity check. Port 8090 still serves the fixture feed with no identity check. Those stay for characterization CT-35 and the source fixture. Wrapping those ports, if release work needs it, is named for sub-stage 30. This file does not add a login server.

`WRITE_TOOLS` stays `[]`. Recursion limit stays 12. Step budget stays 8.

---

## Dead-letter queue and replay

Park is containment for invalid intake only. Language-model replay stays `MODEL_MODE=replay`. Those two stores are different folders.

Do not mix them. Do not copy a parked JSON body into `operations/model-replay/`. Do not copy a PRECOMPUTED model file into `dlq.sqlite3`.

This file is the operations copy of that procedure.

---

## Runbook — stop the incident from going further

1. Read `error_class` on the HTTP body and `event` on stdout.
2. `replay_miss` → keep replay. Do not set `azure` on the laptop.
3. `blocked` → stop. Do not replay as a write.
4. Parked `PARKED` → leave the row listed. Replay the `parked_id` only when the body should be retried.
5. `missing_identity` or `missing_server_key` → send headers or set the process key. Health stays 200.
6. `/health` not 200 → open `dr-plan.md`. Start that service. Do not claim a recovery-time floor.
7. `wait_for_person` → mapped RT role posts approval. Company title stays Unknown.

---

## SLOs and observability

Each stop is proven by HTTP status, `error_class`, parked `status`, and `/health`. Those cells do not prove availability percent, recovery time, or recovery point. **Verified Fact.** FD-19.

Recovery time stays Unknown. Recovery point stays Unknown.

---

## Cost and the 0C envelope

Containment under replay adds 0 live tokens. Token line B1 stays 0 and 0. Lines B2 to B7 stay Unknown. This file claims no dollar benefit.

---

## Exact Half B check

HB-29-01 in `docs/29-incident-bcdr/tabletop-results.md`. The tabletop records `MODEL_MODE=replay`, no Azure socket, `WRITE_TOOLS` `[]`, and the parked intake still listed. This file does not add a second check.

---

## What this file does not do

This file does not add a kill-switch route. It does not start sub-stage 30. It does not call Azure. It does not delete a parked intake. It does not retry BLOCK. It does not sign a Business Owner row. It does not invent a recovery-time floor. It does not invent a recovery-point floor.
