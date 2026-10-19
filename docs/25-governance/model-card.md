# Model card

| Field | Value |
|---|---|
| Stage | Phase 12 / 25 Governance and assurance. Half B evidence. |
| Date / version | 2026-10-18, v1.1 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p12-25b-doc-20261018-001 |
| Status | MEASURED. HB-25-01, HB-25-02, and HB-25-03 recorded. Replay sentences stay PRECOMPUTED. Live Azure stays NEEDS_HUMAN. |
| Evidence sources | FD-13; FD-14; FD-18; `docs/19-intelligence/model-configuration.md`; `docs/19-intelligence/prompt-registry.md`; `docs/19-intelligence/rag-evaluation-results.md`; `docs/19-intelligence/grounding-results.md`; `operations/model-replay/README.md`; `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7`; `compose.yaml`; `.env.example`; `Execution_Plan.md` section 10 and 11 |
| Assumptions | Compose default `MODEL_MODE=replay` stays. Replay file bodies are PRECOMPUTED. A Done test that needs a live model pauses as NEEDS_HUMAN. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown. Token cost stays Unknown. Retrieval p95 stays Unknown. Percent floors stay Unknown. |
| Residual risks | Treating a PRECOMPUTED sentence as a live Azure pass would skip FD-13. Writing 90 or 95 as a floor would skip FD-18. |

This card describes the language path Application A and Application B use today. `MODEL_MODE=replay` reads a saved file named by the SHA-256 hash of the prompt. Replay sentences are PRECOMPUTED. Live Azure stays NEEDS_HUMAN. This card issues no compliance certificate.

Engineering decision ED-P12-25A-05, authority: team-force. Model card id `MC-25-01`. It covers SYS-AI-01, SYS-AI-02, and SYS-AI-05. Half B recorded the replay and Azure cells. Half B did not call Azure.

---

## Finding

**Finding.** The in-use language path is replay. File bodies are PRECOMPUTED. Pipeline scores against those files are REAL. Live Azure stays NEEDS_HUMAN. A hallucination is an AI answer that does not cite a lake item. Percent floors stay Unknown. Half B confirmed `compose.yaml` still defaults `MODEL_MODE` to `replay`, named one replay file path, and left Azure endpoint, deployment name, and API version Unknown.
**Evidence.** FD-13. FD-14. FD-18. Freeze run 42 of 42 on 2026-10-18. `operations/model-replay/README.md`. Half B Recorded sentences under this card.
**Impact.** The reviewer can match this card to Compose, the replay folder, and the unset Azure names without a network call.
**Risk.** A later Azure rehearsal under the same hash would replace a PRECOMPUTED body. That replacement stays NEEDS_HUMAN until a person runs it.
**Confidence.** High on replay. Unknown on Azure deployment name.
**Open questions.** Azure key holder. Azure endpoint. Azure deployment name. Azure API version.

---

## Card identity

| Field | Value | Label |
|---|---|---|
| Card id | MC-25-01 | Engineering decision |
| System ids | SYS-AI-01, SYS-AI-02, SYS-AI-05 | Engineering decision |
| Name | Fabpulse replay language path | Engineering decision |
| Version of prompts | 1.0.0 | Verified Fact |
| Lake version cited | 1.0.0 | Verified Fact |
| `MODEL_MODE` now | `replay` | Verified Fact of Compose default. HB-25-01 REAL |
| Replay sentence honesty | PRECOMPUTED | PRECOMPUTED |
| Live Azure | NEEDS_HUMAN | Verified Fact of Execution Plan section 11. HB-25-03 REAL |

---

## Intended use

**Verified Fact.** FD-04. Prompt registry.

The path drafts a cited sentence for three jobs:

1. Conflict explanation, prompt `P-EXPLAIN-CONFLICT`.
2. Natural-language query, prompt `P-NL-QUERY`.
3. Read-only draft plan, prompt `P-DRAFT-PLAN`.

Intended callers are people or tests that send `X-Api-Key`, `X-Actor-Id`, and `X-Actor-Role` as one of RT-01 to RT-06.

Worked example. Scenario 8 asks why recipe `R02` and `R01` differ on lot `L00000016`. Honesty of those ids: REAL. The path returns a sentence plus lake item `rule.recipe.mismatch_show_both`. RT-03 records hold.

---

## Out of scope

**Verified Fact.** FD-04. FD-05. FD-02. BO-03 working answer.

The path does not rank the queue. The path does not mark a duplicate. The path does not return the governed pass or fail. The path does not write `engineering_hold`. The path does not drop a replay. The path does not pick a policy. The path does not assign INC-2025-014 an owner. The path does not invent `parent_lot_id`.

SYS-AI-04, the hold predictor, stays rejected. This card does not describe a shipped ML model.

---

## How a sentence is obtained

**Verified Fact.** `model-configuration.md`. `operations/replay_lookup.py`.

| Mode | What the process does | Honesty of the sentence |
|---|---|---|
| `replay` | Hash the canonical prompt bytes. Read `operations/model-replay/{sha256}`. On a miss, return `error_class: replay_miss` and abstain. Open no public-network socket. Invent no sentence | PRECOMPUTED when the file exists |
| `azure` | Send the same prompt to Azure OpenAI after a person sets the mode and supplies a key. Save the response under the hash | REAL for that rehearsal. Until then NEEDS_HUMAN |

There is no third offline mode.

Worked example. Changing prompt semver from `1.0.0` to `1.0.1` changes the digest. The old file is not reused.

---

## Training data and the live model

**Unknown.** This repository stores PRECOMPUTED replay files. It does not record a training set. It does not record a fine-tune. Azure deployment name, endpoint, and API version stay Unknown.

**Assumption.** A later Azure rehearsal uses the person-supplied deployment. That row stays NEEDS_HUMAN until the person runs it.

Do not invent a model family name for the live path.

---

## Inputs, outputs, and checks

**Verified Fact.** Gate 3. FD-14. FD-18.

| Item | Value |
|---|---|
| Input to the model | Versioned prompt plus retrieved lake items plus case fields as data |
| Output schema | SCH-09: `sentence`, `citations`, `verdict`, `block`, `untrusted_quotes` |
| Allowed tools | Empty list on the three prompt files. Agent write-tool list is empty |
| After-return check | `check_claim` in code. Empty ANSWER citations become ABSTAIN |
| Hallucination | An AI answer that does not cite a lake item |
| Forced ungrounded | UQ-01, UQ-02, UQ-03 abstain |

Harvested feed, email, HTML, and document text stay data. Approve-or-ignore language is copied into `untrusted_quotes`. That text is not an order.

---

## Measured numbers already on disk

Honesty of counts: REAL. Honesty of replay wording: PRECOMPUTED. Floors stay Unknown.

| Measure | Value | Floor | Label |
|---|---|---|---|
| Freeze rows scored 2026-10-18 | 42 | Unknown | REAL |
| Grounded pass | 42 of 42 | Unknown | REAL |
| Citation precision that run | 79 of 79 | Unknown | REAL |
| Citation recall that run | 40 of 41 | Unknown | REAL |
| Abstention correctness that run | 6 of 6 | Unknown | REAL |
| Rejected schema claims that run | 0 | Unknown | REAL |
| UQ-01 parent lot | ABSTAIN | Behaviour required | REAL |
| UQ-02 INC-2025-014 owner | ABSTAIN. Owner stays Unknown | Behaviour required | REAL |
| UQ-03 MOON 2099 limit | ABSTAIN | Behaviour required | REAL |

Do not read 42 of 42 as a 90 or 95 decided target. Sub-stage 26 records the next eval numbers.

Engineering defaults for a later live call: temperature 0, maximum completion tokens 800. Those numbers are repeatability settings. They are not quality floors. Authority: team-force, ED-P9A-02.

---

## Limits and residual risks

| Limit | What the reader should picture |
|---|---|
| Replay miss | The process abstains. It does not guess |
| Live Azure | NEEDS_HUMAN. Unmeasured on this laptop |
| Confidential process data | Recipe, hold, and policy fields may appear in a retrieved envelope. They stay on this laptop under BO-10 |
| Port 8080 | Baseline listener. This card does not cover it |
| Retention days | Unknown |

---

## Half B evidence this file names

| Check | What Half B records | Honesty when recorded |
|---|---|---|
| HB-25-01 | Compose still sets `MODEL_MODE: replay` | REAL |
| HB-25-02 | This card still says replay sentences are PRECOMPUTED. One replay file path is listed | REAL path. PRECOMPUTED body |
| HB-25-03 | This card still says live Azure is NEEDS_HUMAN. Endpoint, deployment, and API version stay Unknown | REAL |

### Recorded

Recorded 2026-10-18 under `corr-p12-25b-doc-20261018-001`. Half B did not call Azure. Half B did not replace a PRECOMPUTED label with REAL.

HB-25-01. `compose.yaml` service `app-a` line 122 sets `MODEL_MODE: ${MODEL_MODE:-replay}`. Service `app-b` line 152 sets the same default. Honesty: REAL.

HB-25-02. This card still says replay sentence honesty is PRECOMPUTED. Named path: `operations/model-replay/adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7`. That file exists. Size 63 bytes. `operations/model-replay/README.md` still labels fixture bodies PRECOMPUTED. Honesty of the path: REAL. Honesty of the body: PRECOMPUTED.

HB-25-03. This card still says live Azure is NEEDS_HUMAN. Process environment has no `AZURE_OPENAI_ENDPOINT`, no `AZURE_OPENAI_DEPLOYMENT`, and no `AZURE_OPENAI_API_VERSION`. `compose.yaml` has no `AZURE_` key. `.env` is absent. Endpoint, deployment name, and API version stay Unknown. Honesty: REAL.

---

## What this file does not do

This file describes the replay language path. Replay sentences are PRECOMPUTED. Live Azure stays NEEDS_HUMAN. It issues no compliance certificate. It does not write sub-stage 26.

STOP. Do not start sub-stage 26.
