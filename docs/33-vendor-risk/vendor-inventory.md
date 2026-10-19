# Vendor inventory

| Field | Value |
|---|---|
| Stage | Phase 13 / 33 Vendor and concentration risk. Half B measured results. SC-33-01 / HB-33-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-33b-doc-20261018-001 |
| Status | MEASURED. HB-33-01 records existing Compose and Application B facts. Application A query under replay abstains or cites without calling Azure. BO-11 stays PROPOSED. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. Those two figures are not vendor spend. Unit price stays Unknown. |
| Evidence sources | FD-19; FD-13; FD-06; FD-04; BO-11; `compose.yaml`; `Dockerfile.platform`; `requirements-platform.txt`; `apps/app_a/intelligence/azure_client.py`; `apps/app_a/intelligence/generate.py`; `apps/app_b/intelligence/generate.py`; `docs/19-intelligence/model-configuration.md`; `docs/21-integration/integration-inventory.md`; `docs/27-hardening/dependency-hardening.md`; `docs/32-finops/finops-model.md`; `docs/00-preflight/ai-economics/quality-latency-cost-envelope.md`; `docs/model-comparison/app-b-from-lake.md`; `tests/platform/test_freeze_and_bounds.py`; `tests/platform/test_phase13_vendor_risk.py` |
| Assumptions | `MODEL_MODE=replay`. Azure OpenAI stays the later live path and stays NEEDS_HUMAN. Half B ran HB-33-01 only. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown. A vendor contract stays Unknown. A unit price stays Unknown. Numeric floors stay Unknown. |
| Residual risks | Writing a dollar benefit would skip BO-11. Calling Azure from a later half would leave replay. Treating the inherited workshop tree as a signed supplier contract would invent a party that is not on an invoice. |

This file names every supplier this laptop stack uses or names for a later live path. A supplier here is a product, an image, a CI host, a package, or a later cloud model this repo already points at. The one Half B check is SC-33-01. This half adds no product screen. This half invents no contract.

Engineering decision ED-P13-33A-01, authority: team-force. Control id `SC-33-01`. Check id `HB-33-01`. Half B writes `tests/platform/test_phase13_vendor_risk.py`. Half B adds no HTTP route.

Engineering decision ED-P13-33A-02, authority: team-force. Supplier ids `V-33-01` to `V-33-10`. Concentration ids live in `concentration-risk-analysis.md`.

Engineering decision ED-P13-33A-04, authority: team-force. The inventory includes Azure OpenAI even though the laptop path does not call it. The inventory includes first-party lake files and the inherited workshop tree so a later reader can see which jobs stay inside this repo.

---

## Finding

**Finding.** Ten named rows cover the suppliers and the first-party stores this stack already uses. Azure OpenAI is row `V-33-01`. Compose default `MODEL_MODE` is `${MODEL_MODE:-replay}` on Application A and Application B. Application A imports `complete_azure` and calls it only when mode is `azure`. Application B source has no `azure_client` and no `complete_azure`. Application B `PYTHONPATH` is `/opt/platform:/opt/platform/context-lake`. Application A `PYTHONPATH` keeps the inherited third part `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. Application A `POST /api/query` under replay returned `verdict` `ABSTAIN` on a miss and `verdict` `ANSWER` on a cited hit. The Azure boom-patch stayed unused. No invoice, contract, or unit price sits in this repo. BO-11 stays PROPOSED. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. They are not vendor spend.
**Evidence.** `compose.yaml`. `tests/platform/test_phase13_vendor_risk.py`. Correlation id `corr-p13-33b-doc-20261018-001`. FD-13. FD-19. BO-11. Honesty of those pytest facts: REAL.
**Impact.** Half B recorded those rows in one pytest file. Half B added no vendor page in the product.
**Risk.** Filling a price cell from a public list would invent a unit price.
**Confidence.** High on the ten rows, the replay default, and the pytest output. Unknown on a later Azure invoice.
**Open questions.** Reviewer grades HB-33-01. Who later records an Azure invoice.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. Numeric latency, availability, recovery-time, recovery-point, retry-count, and cost floors stay Unknown. This half invents no percent and no dollar benefit.

**Verified Fact.** FD-13. Compose default `MODEL_MODE=replay`. Modes are `replay` and `azure`. There is no third offline mode.

**Verified Fact.** FD-06. Application B takes pass, fail, or wait from the Context Lake. Application B does not import Application A rule functions. Application B does not call Application A at run time.

**Verified Fact.** FD-04. Ranking, rule evaluation, reconciliation, and intake de-duplication are deterministic code. Conflict explanation, natural-language query, and agentic planning are the GenAI paths.

**Verified Fact** of BO-11 working answer. Label every ROI number EDUCATIONAL. State each assumption. Claim no monetary benefit. The row stays PROPOSED. Company titles and the signer stay Unknown.

**Verified Fact.** A Done test that needs Azure pauses as NEEDS_HUMAN.

---

## Supplier rows

**Verified Fact** of the files named in the Evidence column. Contract and unit price stay **Unknown**.

| Id | Name | What it does on this laptop | Later live path | Contract | Unit price | Honesty |
|---|---|---|---|---|---|---|
| V-33-01 | Azure OpenAI | Unused. `azure_client.py` exists. Replay reads a local file | Yes. Person sets `MODEL_MODE=azure` and four variables | Unknown. None invented | Unknown | REAL that the client exists. Unknown on a call |
| V-33-02 | Docker Compose | Starts the seven named containers from `compose.yaml` | Same | Unknown | Unknown | REAL |
| V-33-03 | `python:3.12-slim` image | Base of `Dockerfile.platform` and the inherited workshop image | Same | Unknown | Unknown | REAL of the tag. Digest Unknown |
| V-33-04 | GitHub Actions | `.github/workflows/verify.yml` runs characterization, lake, platform, and `docker compose config` | Same | Unknown | Unknown | REAL |
| V-33-05 | LangGraph 1.0.3 plus the two checkpoint pins | Application A agent graph, pause, and SQLite checkpoint | Same | Unknown | Unknown | REAL of the pins |
| V-33-06 | Open Policy Agent binary | Optional. Python `evaluate()` runs when the binary is absent | Same | Unknown | Unknown | REAL that the fallback exists. Binary hash Unknown |
| V-33-07 | FastAPI, Uvicorn, httpx, PyYAML, jsonschema, pytest | Declared lines in `requirements-platform.txt` | Same | Unknown | Unknown | REAL of the file |
| V-33-08 | SQLite | Holds the lake, packaged stores, checkpoints, audit, and dead-letter rows | Same | Unknown. No commercial contract invented | Unknown | REAL that the files exist |
| V-33-09 | Inherited workshop tree | Application A imports transformed functions and opens packaged SQLite | Laptop only | Not a commercial supplier | Unknown | REAL of the path |
| V-33-10 | Context Lake 1.0.0 | Application B reads cards from the pinned SQLite or lake REST on 8091 | Same | First-party in this repo | Unknown | REAL of the pin |

Worked example. `V-33-01` on this laptop. `MODEL_MODE=replay`. The four Azure variables stay unset. Application A `POST /api/query` reads `operations/model-replay/{sha256}` or returns `replay_miss`. Phase 32 wrote `prompt_tokens=0` and `completion_tokens=0` on the shown replay query. Honesty of those two zeros: REAL. Dollar spend for that query stays Unknown.

Worked example. `V-33-10`. Pin `lake_version` is `1.0.0`. Pin `sqlite_sha256` is `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. Honesty: REAL. Application B start fails when the opened file hash disagrees with that pin.

Cursor coordinator, executor, and reviewer tokens stay off this inventory as a case supplier. Phase 32 named those tokens bucket 3. Count stays Unknown. **Assumption** A-W1 from `docs/32-finops/finops-model.md`.

---

## What is first-party and what is a later live path

| Piece | Kind | Label |
|---|---|---|
| Context Lake YAML, pin, and `context-lake.sqlite3` | First-party store in this repo | Verified Fact |
| Replay files under `operations/model-replay/` | First-party saved prompts | Verified Fact. Honesty of a hand-written file: PRECOMPUTED |
| Application A transformed rules | First-party code that still imports the inherited tree | Verified Fact |
| Application B lake resolver | First-party code with no inherited import | Verified Fact |
| Azure OpenAI chat completions | Later live path. NEEDS_HUMAN | Verified Fact of the client. Unknown of a live call |

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery |
|---|---|---|---|
| FM-33-01 | `MODEL_MODE=azure` on the laptop | A public-network call, or `missing_model_config` if the four variables are unset | Set `MODEL_MODE=replay`. Leave the four Azure variables unset |
| FM-33-02 | A public list price is written into this pack | A dollar cell | Leave unit price Unknown |
| FM-33-03 | A benefit sentence is written from 0 tokens | A signed saving | Write the zeros. Leave BO-11 PROPOSED |
| FM-33-04 | Application B compose `PYTHONPATH` gains the inherited tree | Application B can import Application A’s rule path | Restore `PYTHONPATH: /opt/platform:/opt/platform/context-lake` |

A supplier outage on Azure does not park an intake row. Ranking, intake, lake reads, and health stay up under replay. **Verified Fact.** FD-19.

---

## Dead-letter queue and replay

Invalid intake stays in `apps/app_a/runtime/dlq.sqlite3`. Model replay stays in `operations/model-replay/`. Those two stores stay separate.

A missing replay file returns `error_class: replay_miss` and `verdict: ABSTAIN`. That miss is not a dead-letter row. **Verified Fact** of Application A `generate.py`.

---

## Runbook — read this inventory

1. Confirm `MODEL_MODE=replay` in `compose.yaml` on `app-a`, `app-b`, `lake-rest`, and `lake-mcp`.
2. Confirm Azure variables are unset on the laptop.
3. Confirm Application B source has no `complete_azure` string.
4. Confirm Application B compose `PYTHONPATH` has two parts: `/opt/platform` and `/opt/platform/context-lake`.
5. If a later author wants a dollar cell, stop. Unit price stays Unknown. BO-11 stays PROPOSED.

---

## SLOs and observability

This inventory sets no availability percent. Phase 31 left API p95 and error budget Unknown. This half leaves those cells Unknown.

Proof that the laptop path is replay is the Compose default `${MODEL_MODE:-replay}` on Application A and Application B. Proof that Azure stayed uncalled is HB-33-01. That pytest replaces `complete_azure` with a function that raises. The Application A miss and cite queries finished without that raise. Honesty: REAL.

---

## Cost and the 0C envelope

The 0C envelope left inference cost Unknown. Phase 32 measured bucket 1 as 0 and 0 on the shown Application A replay query. Honesty: REAL for that path. Lines B2 to B7 stay Unknown. `mean_amount` 4982.61 and `hours_per_case` 0.603 stay SIMULATED. Those two figures are not vendor spend.

This half writes no unit price. This half writes no dollar benefit. BO-11 stays PROPOSED.

---

## Exact Half B check HB-33-01

Control id **SC-33-01**. Name: record Application B isolation and unused Azure on replay.

File Half B added: `tests/platform/test_phase13_vendor_risk.py`.

Half B added no product route. Half B did not split `Dockerfile.platform`. Half B did not call Azure. Half B did not copy an extra runbook into `operations/`.

### HB-33-01 before

The vendor-risk pytest file was absent. Compose already held the replay default and the `PYTHONPATH` split. Those file facts were unasserted by this pack.

Measured before

| Field | Expected before | Measured before | Honesty |
|---|---|---|---|
| `tests/platform/test_phase13_vendor_risk.py` | absent | absent on the Half A tree | REAL of the Half A tree |
| Compose Application A `MODEL_MODE` | `${MODEL_MODE:-replay}` | `${MODEL_MODE:-replay}` | REAL of the file. Unasserted by this pack |
| Compose Application B `MODEL_MODE` | `${MODEL_MODE:-replay}` | `${MODEL_MODE:-replay}` | REAL of the file. Unasserted by this pack |
| Compose Application B `PYTHONPATH` | `/opt/platform:/opt/platform/context-lake` | `/opt/platform:/opt/platform/context-lake` | REAL of the file. Unasserted by this pack |
| Compose Application A `PYTHONPATH` third part | inherited tree | `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` | REAL of the file. Unasserted by this pack |
| Application B source `apps.app_a.rules` | absent | absent | REAL of the files. Unasserted by this pack |
| Application B source `fabpulse-legacy-workshop` | absent | absent | REAL of the files. Unasserted by this pack |
| Application B source `8100` | absent | absent | REAL of the files. Unasserted by this pack |
| Application B source `complete_azure` | absent | absent | REAL of the files. Unasserted by this pack |
| Application B source `azure_client` | absent | absent | REAL of the files. Unasserted by this pack |
| Unit price | Unknown | Unknown | Unknown |
| Contract | Unknown | Unknown | Unknown |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |
| `mean_amount` 4982.61 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |
| `hours_per_case` 0.603 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |

### HB-33-01 after

Command: `python -m pytest tests/platform/test_phase13_vendor_risk.py -v --tb=short`. In-process `TestClient`. `MODEL_MODE=replay`. `complete_azure` patched to fail. `socket.create_connection` patched to fail. `socket.socket` forbidden only inside `generate()` so TestClient could open its event loop. Correlation id `corr-p13-33b-doc-20261018-001` on the cited hit. Correlation id `corr-p13-33b-miss-001` on the miss.

Measured after

| Field | Expected after | Measured after | Honesty |
|---|---|---|---|
| pytest file | present and passing | `tests/platform/test_phase13_vendor_risk.py` present. 9 passed | REAL |
| Compose Application A `MODEL_MODE` | `${MODEL_MODE:-replay}` | `${MODEL_MODE:-replay}` | REAL |
| Compose Application B `MODEL_MODE` | `${MODEL_MODE:-replay}` | `${MODEL_MODE:-replay}` | REAL |
| Compose Application B `PYTHONPATH` | two parts. no `fabpulse-legacy` | `/opt/platform:/opt/platform/context-lake` | REAL |
| Compose Application A `PYTHONPATH` third part | inherited tree remains | `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy` | REAL |
| Application B source `apps.app_a.rules` | absent | absent | REAL |
| Application B source `fabpulse-legacy-workshop` | absent | absent | REAL |
| Application B source `8100` | absent | absent | REAL |
| Application B source `complete_azure` | absent | absent | REAL |
| Application B source `azure_client` | absent | absent | REAL |
| Application A miss HTTP status | 200 | 200 | REAL |
| Application A miss `verdict` | `ABSTAIN` | `ABSTAIN` | REAL |
| Application A miss `error_class` | `replay_miss` | `replay_miss` | REAL |
| Application A cite HTTP status | 200 | 200 | REAL |
| Application A cite `verdict` | `ANSWER` | `ANSWER` | REAL |
| Application A cite citations | `arch.listener.lake_rest_8091` | `arch.listener.lake_rest_8091` | REAL |
| Azure boom-patch | unused | unused. process finished | REAL |
| Socket during `generate()` | none | none | REAL |
| `GET /health` | 200 `{"ok": true}` | 200 `{"ok": true}` | REAL |
| New HTTP route | none | none | REAL |
| Extra `operations/` runbook | none | none | REAL |
| Unit price | Unknown | Unknown | Unknown |
| Contract | Unknown | Unknown | Unknown |
| Dollars | Unknown | Unknown | Unknown |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |
| `mean_amount` 4982.61 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |
| `hours_per_case` 0.603 | SIMULATED. Not vendor spend | SIMULATED. Not vendor spend | SIMULATED |

Worked example of the measured after. Application B compose `PYTHONPATH` is `/opt/platform:/opt/platform/context-lake`. That string has no `fabpulse-legacy`. Application A compose `PYTHONPATH` still ends with `/opt/platform/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy`. Application B source under `apps/app_b/` has zero hits for `apps.app_a.rules`, `fabpulse-legacy-workshop`, `8100`, `complete_azure`, and `azure_client`. Miss question `What does arch.listener.lake_rest_8091 say? zz-p13-31-no-replay-file` returned HTTP 200, `verdict` `ABSTAIN`, `error_class` `replay_miss`. Cite question `Which port does the Context Lake REST listener use?` returned HTTP 200, `verdict` `ANSWER`, citation `arch.listener.lake_rest_8091`. The Azure boom-patch did not raise. Honesty: REAL.

Unknown cells stay Unknown. BO-11 stays PROPOSED.

---

## What this file does not do

This file does not add a product screen. It does not add an HTTP route. It does not call Azure. It does not invent a contract, a unit price, or a dollar benefit. It does not sign BO-11. It does not start Phase 14. It does not update a tracker.
