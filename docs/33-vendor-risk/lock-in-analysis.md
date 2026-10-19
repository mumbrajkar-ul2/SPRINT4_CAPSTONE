# Lock-in analysis

| Field | Value |
|---|---|
| Stage | Phase 13 / 33 Vendor and concentration risk. Half B measured results. SC-33-01 / HB-33-01. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p13-33b-doc-20261018-001 |
| Status | MEASURED. HB-33-01 records that Application B source has no `azure_client` and no `complete_azure`. LK-33-01 and LK-33-02 stay out of Application B. BO-11 stays PROPOSED. Unit price stays Unknown. Hours to replace a supplier stay Unknown. |
| Evidence sources | FD-19; FD-13; FD-06; FD-15; BO-11; `apps/app_a/intelligence/azure_client.py`; `apps/app_a/intelligence/generate.py`; `apps/app_a/agent/graph.py`; `apps/app_a/rules/adapter.py`; `apps/app_b/rules/resolver.py`; `apps/app_b/opa.py`; `operations/replay_lookup.py`; `docs/19-intelligence/model-configuration.md`; `docs/10-architecture/adrs/adr-langgraph-interrupt-approval.md`; `docs/11-data-context/contract-gates.md`; `tests/platform/test_phase13_vendor_risk.py`; `vendor-inventory.md` |
| Assumptions | `MODEL_MODE=replay`. Azure stays NEEDS_HUMAN. Half B ran HB-33-01 only. BO-11 stays PROPOSED. Company titles and the signer stay Unknown. |
| Unresolved issues | Hours to replace LangGraph, Azure, or Compose stay Unknown. A replacement supplier name stays Unknown. Numeric floors stay Unknown. A vendor contract stays Unknown. A unit price stays Unknown. |
| Residual risks | Copying the Azure URL shape into a second client without a later design would hide the single live path. Rewriting Application A adapters in this half would add a feature. |

This file names the code and file shapes a later supplier change would edit. Lock-in here means that edit list. A contract cancellation step is absent because no contract is on file.

Engineering decision ED-P13-33A-06, authority: team-force. Exit effort stays a file list. Hours and dollars stay Unknown.

---

## Finding

**Finding.** Five shapes would need an edit if a later author changed a supplier. HB-33-01 measured that Application B source has no `azure_client` and no `complete_azure`. LK-33-01 and LK-33-02 stay out of Application B. Application B compose `PYTHONPATH` has no `fabpulse-legacy`, so LK-33-04 stays out of Application B imports. Application A still holds the Azure client and the inherited adapters. Hours to replace any shape stay Unknown. BO-11 stays PROPOSED.
**Evidence.** `tests/platform/test_phase13_vendor_risk.py`. `azure_client.py`. `generate.py` `elif mode == "azure"`. Honesty: REAL for the pytest greps. Unknown for replacement hours.
**Impact.** Half B did not rewrite those shapes. Half B recorded that Application B already avoids the Azure and inherited-tree shapes.
**Risk.** Changing the Azure URL in this half would be a live-path edit while Azure stays NEEDS_HUMAN.
**Confidence.** High on the five shapes and the Application B greps. Unknown on hours to replace any one of them.
**Open questions.** Reviewer grades HB-33-01. Named replacement supplier, if a later phase wants one.

---

## Locked facts this design applies

**Verified Fact.** FD-19. Replay is the path when the live model is off. This half invents no dollar exit cost.

**Verified Fact.** FD-13. Replay files live under `operations/model-replay/`. There is no third offline mode.

**Verified Fact.** FD-06. Application B reads only the lake for rules.

**Verified Fact** of BO-11. No monetary benefit. The row stays PROPOSED.

---

## Shapes a later supplier change would edit

| Id | Shape | File or field | What a later change edits | Label |
|---|---|---|---|---|
| LK-33-01 | Azure chat-completions URL | `apps/app_a/intelligence/azure_client.py` | Endpoint join, `api-key` header, `temperature` 0, `max_tokens` 800 | Verified Fact of the file. 800 is an engineering cap, not a cost floor |
| LK-33-02 | Mode branch | `apps/app_a/intelligence/generate.py` | The `elif mode == "azure"` arm | Verified Fact |
| LK-33-03 | Agent pause | `apps/app_a/agent/graph.py` and checkpoint SQLite | LangGraph `interrupt` and `SqliteSaver` | Verified Fact of FD-15 |
| LK-33-04 | Inherited imports | `apps/app_a/rules/adapter.py` | `LEGACY_ROOT` and the four function names | Verified Fact |
| LK-33-05 | Lake pin | `context-lake/generated/app-b-pin.json` and Application B `resolver.py` | Pin hashes and `get_item` calls | Verified Fact |

Worked example for LK-33-01. The client joins `AZURE_OPENAI_ENDPOINT`, `/openai/deployments/`, `AZURE_OPENAI_DEPLOYMENT`, `/chat/completions?api-version=`, and `AZURE_OPENAI_API_VERSION`. Those four values stay Unknown. This half does not invent them. A later different model host would need a new client module and a new mode name. That new mode is unnamed here.

Worked example for LK-33-05. Application B already left LK-33-04. The pin lists 25 canonical rule-card ids. Application B resolves each id from the lake. Honesty of the pin hashes: REAL.

---

## Shapes that already move without a supplier

| Shape | Why it moves | Label |
|---|---|---|
| Replay file | The file name is a SHA-256 hex digest of the canonical prompt. The file is local | Verified Fact |
| Lake card | YAML in this repo builds SQLite 1.0.0 | Verified Fact |
| Open Policy Agent verdict | Application B `local_evaluate()` returns EXECUTE, HOLD_FOR_REVIEW, or BLOCK when the binary is absent | Verified Fact of `apps/app_b/opa.py` |
| Deterministic ranking and intake | Those jobs are code. They do not call Azure | Verified Fact. FD-04 |

Application B already uses the lake shape and the local OPA fallback. Application B does not use the Azure URL shape and does not use the inherited import shape.

---

## Failure modes and recovery

| Id | Failure | What the person sees | Recovery |
|---|---|---|---|
| FM-33-09 | Live mode is set and the four Azure variables are missing | `error_class: missing_model_config` and an abstain | Set `MODEL_MODE=replay` |
| FM-33-10 | Live mode is set and the URL fails | `error_class: azure_call_failed` and an abstain | Leave replay as the laptop path. Do not invent a sentence |
| FM-33-11 | Checkpoint file is missing for an Application A pause | Agent restart loses that `thread_id` | Restore `apps/app_a/runtime/checkpoints.sqlite3`. Minutes stay Unknown |
| FM-33-12 | Pin hash disagrees | Application B refuses to start | Restore the pinned SQLite file |

---

## Dead-letter queue and replay

A failed Azure call abstains. It is not written to the intake dead-letter file.

A saved replay file is the recovery for a later repeat of the same canonical prompt. Honesty of a file a test authored by hand: PRECOMPUTED. Honesty of a file a person saved from a later Azure call: REAL for that rehearsal. That later save stays NEEDS_HUMAN.

---

## Runbook — list the edit before a supplier change

1. Name the row in `vendor-inventory.md`.
2. Open the file in the shape table above.
3. Keep `MODEL_MODE=replay` until a person supplies a new live path.
4. Leave unit price Unknown.
5. Do not start that edit in this half.

---

## SLOs and observability

Time to finish a supplier change stays Unknown. That time is not an SLO.

Proof that the Azure shape stayed unused is the replay branch plus HB-33-01. The boom-patch did not raise on the miss or the cited hit. Proof that the inherited shape stayed out of Application B is the Compose `PYTHONPATH` `/opt/platform:/opt/platform/context-lake` and the source grep with zero hits. Honesty: REAL.

---

## Cost and the 0C envelope

`max_tokens` 800 is the Azure request cap in `azure_client.py`. It is not measured spend. Phase 32 already said that. Bucket 1 on the shown replay path is 0 and 0. Honesty: REAL. A dollar cost to leave Azure stays Unknown because no contract exists. BO-11 stays PROPOSED.

---

## Exact Half B check HB-33-01

The same check as `vendor-inventory.md`. Half B asserted Application B source has no `azure_client` and no `complete_azure`. That is the record that LK-33-01 and LK-33-02 stay out of Application B. Half B did not edit `azure_client.py`.

| Cell | Expected after | Measured after | Honesty |
|---|---|---|---|
| Application B source `azure_client` | absent | absent | REAL |
| Application B source `complete_azure` | absent | absent | REAL |
| Application B compose `PYTHONPATH` | no `fabpulse-legacy` | `/opt/platform:/opt/platform/context-lake` | REAL |
| Azure client file | unchanged | `apps/app_a/intelligence/azure_client.py` still present. unused on replay | REAL |
| Hours to replace Azure | Unknown | Unknown | Unknown |
| Unit price | Unknown | Unknown | Unknown |
| BO-11 | PROPOSED | PROPOSED | PROPOSED |

---

## What this file does not do

This file does not replace Azure, LangGraph, Compose, or the inherited adapters. It does not invent a replacement name. It does not invent hours or dollars. It does not call Azure. It does not invent a contract, a unit price, or a dollar benefit. It does not sign BO-11. It does not start Phase 14. It does not update a tracker.
