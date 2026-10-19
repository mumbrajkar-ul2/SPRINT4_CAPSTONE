# Portability assessment

| Field | Value |
|---|---|
| Stage | Phase 13 / 33 Vendor and concentration risk. Half B measured results. SC-33-01 / HB-33-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-33b-doc-20261018-001 |
| Status | MEASURED. HB-33-01 records Application B isolation and unused Azure on replay. BO-11 stays PROPOSED. Unit price stays Unknown. A live Compose-up on a blocked sandbox stays NEEDS_HUMAN. |
| Evidence sources | FD-06; FD-13; FD-17; FD-19; BO-11; `compose.yaml`; `apps/app_b/`; `context-lake/generated/app-b-pin.json`; `docs/10-architecture/adrs/adr-app-b-reads-only-the-lake.md`; `docs/model-comparison/app-b-from-lake.md`; `docs/model-comparison/parity-harness.md`; `tests/platform/test_freeze_and_bounds.py`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `tests/platform/test_phase13_vendor_risk.py`; `vendor-inventory.md` |
| Assumptions | Lake 1.0.0 and the pin hash hold. `MODEL_MODE=replay`. Half B ran HB-33-01 only. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Application A still needs the inherited tree. Shared image still copies that tree. Numeric floors stay Unknown. A vendor contract stays Unknown. A unit price stays Unknown. |
| Residual risks | Opening `legacy.sqlite3` from Application B would put the inherited path back. Importing `apps.app_a.rules` would hide a missing lake item. |

This file names what already runs after a supplier or a sibling application is left out. Portability here means Application B still answers from the lake when Application A is down, and the laptop still answers when Azure is unset. This half cites that evidence. This half does not add a third application.

Engineering decision ED-P13-33A-05, authority: team-force. Half B is a record of the existing Application B isolation. Half B adds no product feature.

---

## Finding

**Finding.** Application B already runs from the Context Lake without Application A. HB-33-01 measured Compose Application B `PYTHONPATH` as `/opt/platform:/opt/platform/context-lake`. Application B source has no `fabpulse-legacy-workshop`, no `apps.app_a.rules`, no `8100`, no `complete_azure`, and no `azure_client`. Application A query under replay returned `ABSTAIN` on a miss and `ANSWER` on a cited hit. The Azure boom-patch stayed unused. A live Compose-up on a blocked sandbox stays NEEDS_HUMAN. The file checks still run in pytest. BO-11 stays PROPOSED.
**Evidence.** `tests/platform/test_phase13_vendor_risk.py`. `compose.yaml` service `app-b`. FD-06. Honesty: REAL for the pytest. Unknown for a live 8110 health call in this half.
**Impact.** Half B added one pytest that reads the Compose `PYTHONPATH` strings and repeats the Azure boom-patch. The product stayed as built.
**Risk.** Changing Application B to import Application A would erase this evidence.
**Confidence.** High on the isolation already on disk and the pytest greps. Unknown on a later Application A move off the inherited tree.
**Open questions.** Reviewer grades HB-33-01. Whether a later live Compose-up records 8110 health again.

---

## Locked facts this design applies

**Verified Fact.** FD-06. Application B decides pass, fail, or wait by reading the Context Lake. Application B does not import the transformed rule code. Application B does not call Application A at run time.

**Verified Fact.** FD-17. The parity harness may start Application A for two-app rows. The stopped-A check is a separate test. The harness prints matched row count 12 and differing row count 2. It does not publish a match percent. Honesty: REAL.

**Verified Fact.** FD-13. Application B host port is 8110. Application A host port is 8100. Compose default `MODEL_MODE=replay`.

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric floors stay Unknown.

**Verified Fact** of BO-11. No monetary benefit. The row stays PROPOSED.

---

## What already moves

| Job | Where it runs without the unused supplier | Label |
|---|---|---|
| Application B pass, fail, or wait | Lake cards through `get_item`, `get_links`, `search_items`, `rule_at` | Verified Fact |
| Application B health | `GET /health` on 8110 with Application A down | Verified Fact of the stopped-A check design |
| Application B lineage | `GET /api/lineage/{item_id}` on 8110. Application A has no lineage route | Verified Fact |
| GenAI sentence on the laptop | Replay file or abstain. Azure unset | Verified Fact |
| Ranking, intake, reconciliation on Application A | Deterministic code. Live model off | Verified Fact. FD-04 |
| OPA verdict on Application B | `local_evaluate()` when the `opa` binary is absent | Verified Fact |

Worked example. Pin `lake_version` `1.0.0`. Pin `sqlite_sha256` `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Application B opens that file or calls lake REST on 8091. Application A on 8100 stays down. `GET /health` on 8110 is HTTP 200. Scenario 8 still shows dispatch `R02` and equipment `R01`. Honesty: REAL in the Phase 11 harness write-up.

Worked example. `MODEL_MODE=replay`. Azure variables unset. Application A query on a missing hash returns `replay_miss` and abstains. Application B query uses a replay file or builds a cited sentence from retrieved lake statements. Neither path calls `complete_azure`.

---

## What still sits on one path

| Job | Path that still holds it | Label |
|---|---|---|
| Application A rule functions | Inherited workshop `PYTHONPATH` and `adapter.py` | Verified Fact |
| Application A agent pause | LangGraph checkpoint file | Verified Fact |
| Later live model sentence | Azure OpenAI client | Verified Fact of the unused client |
| Shared image contents | `Dockerfile.platform` still copies the inherited tree into the image Application B uses | Verified Fact. Application B does not import those copied files |

This half does not move Application A off the inherited tree. That move would be a new build.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery |
|---|---|---|---|
| FM-33-13 | Application B calls port 8100 | Isolation check fails | Remove that call. `test_no_app_b_feature_handlers` already forbids the string `8100` in Application B source |
| FM-33-14 | Application B opens packaged `legacy.sqlite3` | Inherited path returns | Keep fixtures in `apps/app_b/fixtures/scenarios.yaml` |
| FM-33-15 | Pin hash miss | Application B start fails | Restore the pinned file |
| FM-33-16 | Replay file missing | `replay_miss` and abstain, or Application B lake-statement fallback | Accept the abstain or the cited lake sentence. Do not call Azure |

---

## Dead-letter queue and replay

Application B compose volumes omit `dlq.sqlite3`, `checkpoints.sqlite3`, and `audit_chain.sqlite3`. **Verified Fact** of `tests/platform/test_phase13_release.py`.

Portability for a bad Application A intake stays the Application A dead-letter file. Portability for a missing model file stays replay or abstain. Application B does not take over the Application A dead-letter file.

---

## Runbook — prove Application B still runs alone

1. Leave Application A stopped.
2. Start lake REST on 8091, or use in-process `lake_runtime` against the pin.
3. Start Application B on 8110.
4. Call `GET /health`. Expect HTTP 200.
5. Open scenario 8 case `PS000000016`. Expect `recipe_version=R02` and `recipe_rev=R01`.
6. Grep `apps/app_b` for `fabpulse-legacy-workshop`, `apps.app_a.rules`, `8100`, `azure_client`, and `complete_azure`. Expect zero hits.

Half B automates steps that read Compose and grep. A live Compose-up on a blocked sandbox stays NEEDS_HUMAN. The file checks still run in pytest.

---

## SLOs and observability

No portability percent is set. The harness already refused a match percent. This half does the same.

Observability is the Compose `PYTHONPATH` strings, the source grep, `GET /health` on 8110, and stdout `model_mode=replay`.

---

## Cost and the 0C envelope

Moving Application B off Application A added no measured Azure tokens. Application B query still has no Phase 32 meter write. That Application B token line stays Unknown. Application A replay bucket 1 on the shown path is 0 and 0. Honesty: REAL. This half claims no dollar benefit from the isolation. BO-11 stays PROPOSED.

---

## Exact Half B check HB-33-01

The same check as `vendor-inventory.md`.

| Probe | Expected after | Measured after | Honesty |
|---|---|---|---|
| `tests/platform/test_phase13_vendor_risk.py` | File present and passing | File present. 9 passed | REAL |
| Application B `PYTHONPATH` | no `fabpulse-legacy` substring | `/opt/platform:/opt/platform/context-lake` | REAL |
| Application A `PYTHONPATH` | inherited third part remains | `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` | REAL |
| Application B Azure strings | `complete_azure` and `azure_client` absent | both absent | REAL |
| Application B source `apps.app_a.rules` | absent | absent | REAL |
| Application B source `fabpulse-legacy-workshop` | absent | absent | REAL |
| Application B source `8100` | absent | absent | REAL |
| Application A replay query | boom-patch unused. query finishes | miss `ABSTAIN` `replay_miss`. cite `ANSWER`. boom-patch unused | REAL |
| Live Compose-up 8110 | NEEDS_HUMAN | NEEDS_HUMAN. file checks ran in pytest | Unknown for a live 8110 socket in this half |
| Unit price | Unknown | Unknown | Unknown |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |

Honesty of the pytest cells: REAL. Unknown cells stay Unknown.

---

## What this file does not do

This file does not add a third application. It does not move Application A off the inherited tree. It does not split `Dockerfile.platform`. It does not add a product screen or a new HTTP route. It does not call Azure. It does not invent a contract, a unit price, or a dollar benefit. It does not sign BO-11. It does not start Phase 14. It does not update a tracker.
