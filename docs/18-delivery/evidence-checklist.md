# Evidence checklist

| Field | Value |
|---|---|
| Stage | Phase 8 / 18 Delivery foundations. Half B platform. |
| Date / version | 2026-10-18, v1.2 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8b-doc-20261018-001. Health rows EV-H8080 and EV-H8090 recorded by the coordinator from the Team-Force paste, correlation id corr-p8-human-20261018-001. |
| Status | IMPLEMENTATION. Ports 8080 and 8090 returned health bodies. |
| Evidence sources | Commands listed in each row. Team-Force paste on 2026-10-18 for `http://127.0.0.1:8080/health` and `http://127.0.0.1:8090/health`. |
| Assumptions | The pasted bodies are the documents those two URLs returned after Compose was started. |
| Unresolved issues | The paste did not include a separate HTTP status number. The bodies themselves say status ok. |
| Residual risks | A later reader can still confuse these two Compose health bodies with the earlier host-uvicorn checks on 8091, 8092, 8100, and 8110. |

This file records what Half B actually ran. Health-check output that came from a live HTTP call is REAL. A skipped Compose bring-up is marked NEEDS_HUMAN.

---

## Finding

**Finding.** Four new listeners answered on this machine. `docker compose config` published the six host ports. `docker compose up` was not started because the machine has `python:3.11-slim` and would have to pull `python:3.12-slim` and build two images.
**Evidence.** Command results below.
**Impact.** A person must run `docker compose up --build` from the capstone root to prove the seven containers together.
**Risk.** Pasting a guessed 200 for 8080 or 8090.
**Confidence.** High on the four host listeners and on `compose config`. Unknown on the seven-container run.
**Open questions.** None for these two health URLs. Team-Force pasted the bodies on 2026-10-18.

---

## How a row is filled

| Column | What this unit wrote |
|---|---|
| Result | Observed status, body snippet, or file fact |
| Honesty | REAL for a live check. PRECOMPUTED for the replay fixture body. Unknown if the check could not run |
| Note | `NEEDS_HUMAN` when Compose was not started, plus the command a person must run |

---

## Health per service

| ID | Listener | Command or route | Result | Honesty |
|---|---|---|---|---|
| EV-H8080 | Legacy API | `GET http://127.0.0.1:8080/health` | Team-Force paste 2026-10-18: `{"status": "ok", "service": "fabpulse-legacy"}` | REAL |
| EV-H8090 | Source gateway | `GET http://127.0.0.1:8090/health` | Team-Force paste 2026-10-18: `{"status": "ok", "service": "source-gateway", "domain": "High Tech"}` | REAL |
| EV-H8091 | Lake REST | `GET http://127.0.0.1:8091/health` | HTTP 200 `{"ok":true}` | REAL |
| EV-H8092 | Lake MCP | `GET http://127.0.0.1:8092/health` | HTTP 200 `{"ok":true,"tools":["search_items","get_item","get_links","rule_at"]}` | REAL |
| EV-H8100 | Application A | `GET http://127.0.0.1:8100/health` | HTTP 200 `{"ok":true}` | REAL |
| EV-H8110 | Application B | `GET http://127.0.0.1:8110/health` | HTTP 200 `{"ok":true}` | REAL |

Worked example. Host uvicorn served Application A. `GET http://127.0.0.1:8100/health` returned `{"ok":true}`. That is not the seven-container Compose run.

The command a person must run for the full stack:

```text
cd c:\MangeshStudy\FDE\Labs\SPRINT4_CAPSTONE
docker compose up --build
```

Then call `GET http://127.0.0.1:8080/health` and `GET http://127.0.0.1:8090/health`.

---

## Identity scaffolding

| ID | Check | Result | Honesty |
|---|---|---|---|
| EV-ID-A | 8100 identity probe, no headers | HTTP 401 `error_class: missing_identity`. No case body. | REAL |
| EV-ID-B | 8110 identity probe, no headers | HTTP 401 `error_class: missing_identity` | REAL |
| EV-ID-HIT | Both probes with `X-Api-Key`, `X-Actor-Id: demo-rt01-1`, `X-Actor-Role: RT-01` | HTTP 200 `{"ok":true,"actor_id":"demo-rt01-1","actor_role":"RT-01"}`. No case fields. | REAL |
| EV-ID-KEY | Wrong key | HTTP 401 `error_class: missing_identity` | REAL |
| EV-ID-SRC | Application source has no `local-demo-only` literal | `apps/` Python files have no that string. | REAL |
| EV-ID-CASE | `GET /api/cases/CASE-1` on 8100 with no headers | HTTP 401 `error_class: missing_identity` | REAL |

---

## Lake seams

| ID | Check | Result | Honesty |
|---|---|---|---|
| EV-L-RO | POST `http://127.0.0.1:8091/v1/items` with the API key | HTTP 405 `error_class: lake_write_rejected` | REAL |
| EV-L-KEY | GET `/v1/version` with no key | HTTP 401 `error_class: missing_identity` | REAL |
| EV-L-VER | GET `/v1/version` with key | HTTP 200 `lake_version` 1.0.0. `item_count` 148. `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` | REAL |

---

## Replay

| ID | Check | Result | Honesty |
|---|---|---|---|
| EV-R-HIT | Prompt bytes `phase8-replay-fixture-prompt` | Lookup returned the saved file. Body contains `phase8-replay-unit-body`. | REAL for the lookup. PRECOMPUTED for the file body |
| EV-R-MISS | Prompt `no-saved-file-for-this-prompt` | `error_class: replay_miss`. `socket.create_connection` was not called. | REAL |
| EV-R-ENV | Compose default `MODEL_MODE=replay` | `docker compose config` printed `MODEL_MODE: replay` on app-a, app-b, lake-rest, and lake-mcp. | REAL |

---

## Compose, CI, logs, freeze

| ID | Check | Result | Honesty |
|---|---|---|---|
| EV-C-UP | `docker compose up` from the capstone root | Team-Force reached `http://127.0.0.1:8080/health` and `http://127.0.0.1:8090/health` on 2026-10-18. Both bodies say status ok. See EV-H8080 and EV-H8090. | REAL |
| EV-C-CFG | `docker compose config` | Exit 0. Published host ports 8080, 8090, 8091, 8092, 8100, 8110. Container names `fabpulse-legacy`, `fabpulse-source-gateway`, `fabpulse-bridge`, `fabpulse-lake-rest`, `fabpulse-lake-mcp`, `fabpulse-app-a`, `fabpulse-app-b`. | REAL |
| EV-CI | Capstone workflow omissions | `.github/workflows/verify.yml` has no `generate --reset` and no live model call. | REAL |
| EV-LOG | JSON line on `identity_missing` for `app-a` | `{"service":"app-a","level":"warn","event":"identity_missing","path":"/api/identity-check","status":401}` The key is not in the line. | REAL |
| EV-FZ | Packaged hashes after tests | `data/legacy.sqlite3` still `2d9a3fae58af56daf524d16eb99dedf4ef82ade39d1ca68ad36e249fa0b99879`. `data/enterprise_legacy.sqlite3` still `f13ed709df16f3c6244282ff4efde7768dee9294f0533098de3d34f0657af913`. Characterization 70 tests OK. Lake tests 46 passed. Platform tests 24 passed. | REAL |
| EV-NF | No feature handlers in the stubs | `apps/app_a/` and `apps/app_b/` have no queue, approval, query, recovery, or lineage route. | REAL |

Ports 8080 and 8090 use the inherited workshop image. Those two services keep the current no-identity GET behaviour. That wrap is recorded in `compose.yaml`.

---

## Half A design evidence (kept)

| ID | Artifact | Result | Label |
|---|---|---|---|
| EV-D17 | Five files under `docs/17-implementation-prd/` | Still on disk | Verified Fact of the paths |
| EV-D18 | Five files under `docs/18-delivery/` | Still on disk. This file updated in Half B | Verified Fact |
| EV-D-SIG | `implementation-baseline-signoff.md` | UNSIGNED | Verified Fact |
| EV-D-FD13 | FD-13 | DECIDED in `Decision_Tracker.md` before this unit. This unit did not edit the tracker. | Verified Fact |

---

## What this file does not do

This file does not claim a healthy seven-container Compose stack. It does not start Phase 9.
