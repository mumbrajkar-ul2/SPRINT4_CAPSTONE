# Recovery time and recovery point

| Field | Value |
|---|---|
| Stage | Phase 13 / 29 Incident and BCDR. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-29a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. Numeric cells stay Unknown. |
| Evidence sources | FD-19; FD-11; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/12-specs/system-spec.md`; `docs/17-implementation-prd/finalized-nfrs.md`; `fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy/docs/operations-service-levels.md`; `compose.yaml`; `docs/28-resilience/failure-injection-results.md` |
| Assumptions | Historical notes in the inherited service-levels file stay historical. BO rows that are PROPOSED stay PROPOSED. `MODEL_MODE=replay`. |
| Unresolved issues | Recovery-time floor stays Unknown. Recovery-point floor stays Unknown. Availability percent stays Unknown. API p95 stays Unknown. Measured restore seconds stay Unknown. |
| Residual risks | Copying 8 hours or 24 hours from the inherited file into a floor cell would skip FD-19. Inventing a percent would skip FD-19. |

This file names what recovery time and recovery point mean on this product, which cells are still empty, and which inherited notes stay unused as floors. Recovery time is how many seconds until `GET /health` returns HTTP 200 after a stop. Recovery point is how much already-written data can be missing after a stop.

Engineering decision ED-P13-29A-04 continued, authority: team-force. The restore catalogue in `dr-plan.md` is the evidence source for what exists on disk. It is not a numeric floor.

---

## Finding

**Finding.** FD-19 leaves numeric recovery-time and recovery-point floors Unknown until a measured run. The 0C envelope left those cells Unknown. `system-spec.md` and `finalized-nfrs.md` already marked the inherited 8-hour recovery note and the inherited 24-hour recovery-point note as not adopted. The inherited file `operations-service-levels.md` still records those older planning assumptions. This half leaves every numeric floor cell Unknown. This half copies neither 8 hours nor 24 hours into a floor. Compose health retries 5 times at a 10-second interval after a 15-second start period. Those integers are probe settings. They are not a recovery-time floor.
**Evidence.** FD-19 DECIDED 2026-10-18. Envelope latency table. `operations-service-levels.md` sentence on 8 hours and 24 hours. `compose.yaml` healthcheck keys. HB-28-01 did not measure restart seconds.
**Impact.** Half B tabletop records health 200. That one GET does not fill a recovery-time floor. Measured cells in `tabletop-results.md` stay a walk result, not an SLO.
**Risk.** A later reader treating 5 Compose retries as "recovery in 50 seconds" would invent a floor this phase has not measured.
**Confidence.** High on the Unknown cells and on the inherited notes remaining unused. Unknown on any future measured seconds.
**Open questions.** HALF_A_ACCEPTED. A measured restart, if a later check records one.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Numeric latency, availability, recovery-time, recovery-point, retry-count, and cost floors stay Unknown until a measured run. Do not invent a percent or a dollar benefit.

**Verified Fact.** FD-11. Specs already left recovery time and recovery point Unknown. Inherited 99.5 percent availability is not adopted.

**Verified Fact.** Envelope file. `docs/operations-service-levels.md` records older planning notes: 99.5% scheduled-hour availability, recovery time 8 hours, recovery point 24 hours. That file says these are historical working targets, not measured guarantees.

**Verified Fact** of BO rows that are PROPOSED. Those rows stay PROPOSED. This half invents no signer.

---

## What the two numbers would mean here

| Name | Meaning on this laptop product | Floor in force now | Label |
|---|---|---|---|
| Recovery time | Seconds from process stop until `GET /health` on that listener returns HTTP 200 | Unknown | Unknown |
| Recovery point | Already-written rows that are missing after the process starts again: parked intake rows, checkpoint waits, audit rows, in-memory `_LAST` | Unknown | Unknown |

Worked example. Application A exits. The person runs `docker compose up` for `app-a`. The next `GET /health` on 8100 returns 200. The number of seconds between exit and that 200 is the measured recovery time for that one run. This half has not measured that number. The cell stays Unknown.

Worked example. The process opened `apps/app_a/runtime/dlq.sqlite3` and held `DLQ-28-BAD` as `PARKED`. After a Compose recreate with no host bind for that file, the new process opens an empty default file. The parked row is missing. How many rows may go missing is the recovery point. This half has not set a maximum. The cell stays Unknown.

---

## Envelope and inherited notes

| Axis | Inherited note | Adopted as this product's floor | Cell in this file |
|---|---|---|---|
| Availability | 99.5 percent scheduled-hour | No | Unknown |
| Recovery time | 8 hours | No | Unknown |
| Recovery point | 24 hours | No | Unknown |
| Partner feed accepted | 4 hours | No | Unknown |
| Overnight reconciliation | Before 06:00 | No | Unknown |

The inherited file is evidence that those notes exist as older planning assumptions. Honesty of that file's text: REAL as a quote of the file. This project leaves the floor cells Unknown.

Do not copy 8 hours into a Half B measured cell as a target. Do not copy 24 hours into a Half B measured cell as a target. Do not invent a percent.

---

## What a later measured run may write

A later measured run may write seconds next to one named stop and one named start. That write is a REAL observation of that run. A floor still needs a later Business Owner or SME row. FD-19 says Team-Force names engineering defaults. This half names no default second count. The floor cell stays Unknown.

Compose probe settings already in `compose.yaml`:

| Setting | Value | What it is |
|---|---|---|
| `interval` | 10s | Time between health probes |
| `timeout` | 4s | Time one probe waits |
| `retries` | 5 | Failed probes before unhealthy |
| `start_period` | 15s | Time after start before failures count |

Those values are the current Compose file. Honesty: REAL of the file. They are not a recovery-time floor.

Client timeouts already in code (3s gateway, 5s lake, 15s OPA, 30s Azure) stay client timeouts. They are not SLOs. **Verified Fact** of `timeout-retry-policy.md`.

---

## Restore catalogue versus a floor

`dr-plan.md` lists RS-29-01 to RS-29-06. Replay files sit on a host bind mount. Packaged sqlite stays read-only. Dead-letter, checkpoint, and audit sqlite are process files. `_LAST` is memory. That catalogue tells the person what to expect after a stop. It does not fill the Unknown cells in the table above.

---

## Dead-letter queue and replay

Parked rows are one kind of already-written data in the recovery-point question. Model replay files are another kind. They live in different folders. A measured recovery point, when one exists, must name which folder was measured. This half measures neither.

The parked intake from sub-stage 28 stays listed while the process still opens the same dead-letter file. That visibility is FD-19. It is not a recovery-point number.

---

## SLOs and observability

HB-29-01 will record `/health` HTTP 200 and a parked-list result. Those cells prove the tabletop walk. They do not prove a recovery-time floor or a recovery-point floor. **Verified Fact.** FD-19.

Sub-stage 31 writes SLO files. This sub-stage does not fill those files.

---

## Cost and the 0C envelope

Empty numeric recovery cells add no token line. Token line B1 stays 0 and 0 under replay. Lines B2 to B7 stay Unknown. This half claims no dollar benefit for an unmeasured restore.

Labor hours per case 0.603 and mean case amount 4982.61 stay SIMULATED legacy fields. BO-11 working answer stays PROPOSED.

---

## Exact Half B check

`tabletop-results.md` HB-29-01. Measured recovery-time seconds stay Unknown. Measured recovery-point row counts stay Unknown unless the walk records that the same dead-letter file still lists `DLQ-28-BAD`. Listing that row proves visibility. It does not prove a maximum loss number.

---

## What this file does not do

This file does not adopt 8 hours. It does not adopt 24 hours. It does not invent a percent. It does not start Half B. It does not sign a Business Owner row.

STOP. Wait for HALF_A_ACCEPTED. Do not write Half B.
