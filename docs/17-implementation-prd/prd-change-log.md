# PRD change log

| Field | Value |
|---|---|
| Stage | Phase 8 / 17 Implementation PRD. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. BO rows that are PROPOSED stay PROPOSED. |
| Evidence sources | `docs/09-initial-prd/`; `docs/17-implementation-prd/implementation-prd.md`; `docs/12-specs/`; `docs/10-architecture/adrs/adr-ports-and-compose.md`; `Decision_Tracker.md` |
| Assumptions | The Initial PRD text on disk stays the Phase 3 record. This log records how the implementation PRD differs. It does not rewrite the Phase 3 files. |
| Unresolved issues | Signer names stay Unknown. Numeric SLO cells stay Unknown. FD-13 stays DEFERRED until HALF_A_ACCEPTED. |
| Residual risks | Editing a Phase 3 file in place would hide the original unsigned Initial PRD. |

This file lists every change from the Initial PRD to the implementation PRD. A row that says Unchanged keeps the Phase 3 requirement.

---

## Finding

**Finding.** Product scope is unchanged. The implementation PRD adds platform facts the Initial PRD left later: six host ports, three identity headers, replay wiring, CI steps, and log fields.
**Evidence.** `initial-prd.md` BO-04 working answer. `implementation-prd.md` IA-01 to IA-12.
**Impact.** A reviewer can see what moved from Unknown to a team-force decision.
**Risk.** Treating a platform row as a new business problem would grow past BO-04.
**Confidence.** High
**Open questions.** Reviewer verdict.

---

## How to read a row

| Change type | Meaning |
|---|---|
| Unchanged | The Phase 3 statement still binds the product |
| Invalidated | A Phase 3 assumption is no longer true. See IA-* in `implementation-prd.md` |
| Named now | A Phase 3 Unknown is given a team-force value |
| Still Unknown | The cell stays empty. No number is invented |
| Still PROPOSED | A Business Owner row stays unsigned |

---

## Product scope

| Item | Phase 3 | Implementation PRD | Change type |
|---|---|---|---|
| Two applications | Application A from rebuilt program. Application B from the lake | Same | Unchanged |
| Eight business problems | BP1 to BP8 | Same | Unchanged |
| Demo scenarios | S7 to S13 | Same | Unchanged |
| AI limits | FD-04 and BO-03 working answer | Same. BO-03 still PROPOSED | Unchanged. Still PROPOSED |
| Hold predictor | Rejected. 117/125 versus 117/125 | Same | Unchanged |
| Ninth business problem | Out of scope | Still out of scope | Unchanged |
| 40-minute path | Execution_Plan section 10 | Same working path. FD-21 still later | Unchanged |
| Headline KPIs | Exception cycle time. Aged backlog. Both Unknown | Same | Still Unknown. Still PROPOSED |
| Dollar benefit | Forbidden (BO-11) | Still forbidden | Still PROPOSED |

---

## Assumptions invalidated

These rows copy IA-01 to IA-12. The full wording lives in `implementation-prd.md`.

| ID | Phase 3 assumption | Implementation fact | Change type |
|---|---|---|---|
| IA-01 | Ports 8080, 8090, 8091, 8092 stay later-phase facts | Those four ports are locked | Invalidated |
| IA-02 | Identity design stays later | Scaffolding is named. FD-18 still later | Invalidated for scaffolding |
| IA-03 | Application host ports stay Unknown | 8100 and 8110 | Named now |
| IA-04 | Identity header format stays Unknown | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` | Named now |
| IA-05 | FD-07 later | FD-07 DECIDED | Invalidated |
| IA-06 | FD-09 later | FD-09 DECIDED | Invalidated |
| IA-07 | FD-10 later | FD-10 DECIDED | Invalidated |
| IA-08 | FD-11 pending | FD-11 DECIDED. Percents still Unknown | Invalidated for contracts. Still Unknown for percents |
| IA-09 | FD-22 later | FD-22 DECIDED. Lake 1.0.0 | Invalidated |
| IA-10 | Lake item schema later | Schema exists | Invalidated |
| IA-11 | Replay stays an assumption until Phase 15 | Phase 8 wires replay. FD-21 still later | Named now for wiring |
| IA-12 | No lake listener in the current picture | Half B adds 8091 and 8092 | Named now |

Worked example. Phase 3 said Application A host port is Unknown. The implementation PRD says 8100. The browser opens `http://127.0.0.1:8100`.

---

## Platform rows added

These rows are new in the implementation PRD. They serve BP8 and the laptop demo. They do not add a ninth problem.

| Row | Value | Authority |
|---|---|---|
| Application A host port | 8100. FastAPI serves `/api` and React | team-force. ED-P8A-01 |
| Application B host port | 8110. FastAPI serves `/api` and React | team-force. ED-P8A-01 |
| Shared key variable | `FABPULSE_API_KEY` | team-force. ED-P8A-02 |
| Documented local default | `local-demo-only` in `.env.example` | team-force. ED-P8A-02 |
| Identity headers | `X-Api-Key`, `X-Actor-Id`, `X-Actor-Role` | team-force. ED-P8A-02 |
| Missing identity | HTTP 401, `error_class: missing_identity` | Already in EH-01. Format now named |
| 8080 and 8090 identity | None. Baseline and fixture | team-force. ED-P8A-03 |
| Lake key | `X-Api-Key` except health | team-force. ED-P8A-04 |
| Container names | `fabpulse-legacy`, `fabpulse-source-gateway`, `fabpulse-bridge`, `fabpulse-lake-rest`, `fabpulse-lake-mcp`, `fabpulse-app-a`, `fabpulse-app-b` | team-force. ED-P8A-05 |
| CI path | Capstone `.github/workflows/verify.yml`. No `generate --reset` | team-force. ED-P8A-06 |
| Logs | JSON lines on stdout | team-force. ED-P8A-07 |
| Replay | `MODEL_MODE=replay`. Files in `operations/model-replay/` named by SHA-256 of the prompt | team-force. ED-P8A-08. Design already in section 10 |

---

## Numeric cells

| Cell | Phase 3 | Implementation PRD | Change type |
|---|---|---|---|
| Exception cycle time | Unknown | Unknown | Still Unknown |
| Aged backlog cutoff | Unknown | Unknown | Still Unknown |
| API p95 | Unknown | Unknown | Still Unknown |
| Retrieval p95 | Unknown | Unknown | Still Unknown |
| Availability percent | Inherited 99.5 not adopted | Still not adopted | Still Unknown |
| Recovery time | Inherited 8 hours not adopted | Still not adopted | Still Unknown |
| Recovery point | Inherited 24 hours not adopted | Still not adopted | Still Unknown |
| Groundedness percent | Unknown | Unknown | Still Unknown |
| Citation percent | Unknown | Unknown | Still Unknown |
| Abstention percent | Unknown | Unknown | Still Unknown |
| Token cost | Unknown | Unknown | Still Unknown |

No percent was filled in.

---

## Business Owner rows

| ID | Phase 3 status | Implementation status | Change type |
|---|---|---|---|
| BO-02 | PROPOSED | PROPOSED | Still PROPOSED |
| BO-03 | PROPOSED | PROPOSED | Still PROPOSED |
| BO-04 | PROPOSED. Initial PRD UNSIGNED | PROPOSED. Implementation PRD UNSIGNED | Still PROPOSED |
| BO-06b | PROPOSED | PROPOSED | Still PROPOSED |
| BO-08 | PROPOSED | PROPOSED | Still PROPOSED |
| BO-10 | PROPOSED | PROPOSED | Still PROPOSED |
| BO-11 | PROPOSED | PROPOSED | Still PROPOSED |
| BO-12 | PROPOSED | PROPOSED | Still PROPOSED |
| BO-13 | PROPOSED | PROPOSED | Still PROPOSED |

This log does not mark any of those rows DECIDED.

---

## What this file does not do

This file does not edit `docs/09-initial-prd/`. It does not write code. It does not sign a Business Owner row.
