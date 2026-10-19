# Model configuration

| Field | Value |
|---|---|
| Stage | Phase 9 / 19 Intelligence core. Half A design. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p9a-doc-20261018-001 |
| Status | DESIGN. Awaits HALF_A_ACCEPTED. No live model call in this half. |
| Evidence sources | `Decision_Tracker.md` FD-13, FD-14; `Execution_Plan.md` section 10; `operations/model-replay/README.md`; `operations/replay_lookup.py`; `.env.example`; `docs/17-implementation-prd/implementation-prd.md` ED-P8A-08 |
| Assumptions | Compose default `MODEL_MODE=replay` stays. A Done test that needs a live model pauses as NEEDS_HUMAN. The human supplies the Azure key. |
| Unresolved issues | Azure endpoint, deployment name, and API version stay Unknown until a person supplies them. Token cost stays Unknown. Retrieval p95 stays Unknown. |
| Residual risks | Calling Azure while `MODEL_MODE=replay` would break the offline demo. Inventing a sentence on a replay miss would hide a cache miss. |

This file names how Application A obtains a model response. Replay is the path this half designs for Half B to build. Azure OpenAI is the later live path. This half does not call Azure.

Engineering decision ED-P9A-02, authority: team-force. Modes, hash input, and engineering defaults below.

---

## Finding

**Finding.** Application A has two model modes: `replay` and `azure`. Half B implements both. Half B tests run in `replay`. A live Azure call waits for a person and a key.
**Evidence.** FD-13. `Execution_Plan.md` section 10. `operations/replay_lookup.py` today returns `replay_required` when the mode is not `replay`.
**Impact.** Half B must extend the lookup so `azure` can run when a person sets that mode. Replay still must not open a public-network socket.
**Risk.** Leaving `azure` as a silent fall-through from a missing replay file would call the network during the laptop demo.
**Confidence.** High on the two mode names. Unknown on Azure deployment name.
**Open questions.** Deployment name. API version. Token prices.

---

## Modes

| `MODEL_MODE` | What Application A does | When |
|---|---|---|
| `replay` | Reads `operations/model-replay/{sha256}`. On a miss, returns `error_class: replay_miss`. Does not open a public-network socket. Does not invent a sentence. | Compose default. Half B tests. Laptop demo |
| `azure` | Sends the same canonical prompt to Azure OpenAI. Saves the response under the hash so a later replay can play it back. | Rehearsal when a person sets the mode and supplies the key |

There is no third offline mode. Ollama is not a product mode. **Verified Fact.** FD-13. ED-P8A-08.

Worked example. Half B runs `POST /api/query` with `MODEL_MODE=replay` and a prompt whose hash has no file. The body is `error_class: replay_miss`. The process does not call Azure.

---

## Replay hash input

Engineering decision ED-P9A-02 continued, authority: team-force.

`operations/replay_lookup.py` hashes the exact prompt bytes. Application A must build those bytes the same way every time.

Canonical JSON, UTF-8, keys in this order, no extra whitespace beyond one space after `:` and `,` in a compact dump that Half B pins in a test:

| Key | What it holds |
|---|---|
| `prompt_id` | `P-EXPLAIN-CONFLICT`, `P-NL-QUERY`, or `P-DRAFT-PLAN` |
| `semver` | For example `1.0.0` |
| `system` | The system text from the versioned prompt file |
| `retrieved_item_ids` | Sorted list of lake item ids from this retrieval |
| `question` | The user question or the case-explanation job string |
| `case_id` | The case id, or empty string |

The SHA-256 hex digest of those bytes is the replay file name.

Worked example. Changing `semver` from `1.0.0` to `1.0.1` changes the digest. The old file is not reused. Half B writes a new rehearsal file after a person runs Azure, or a test fixture labelled PRECOMPUTED.

Honesty of a fixture that a unit test authors by hand: PRECOMPUTED. Honesty of a file saved from a live Azure call: REAL for that rehearsal. The audience is told when replay is on. **Verified Fact.** `Execution_Plan.md` section 10.

---

## Azure OpenAI later live path

These environment names are the live path. Values stay out of source. Values stay Unknown in this design.

| Variable | What it holds |
|---|---|
| `MODEL_MODE` | `azure` when a person wants a live call |
| `AZURE_OPENAI_ENDPOINT` | Resource URL. Unknown until supplied |
| `AZURE_OPENAI_API_KEY` | Secret. Human supplies it. Not committed |
| `AZURE_OPENAI_DEPLOYMENT` | Deployment name. Unknown until supplied |
| `AZURE_OPENAI_API_VERSION` | API version string. Unknown until supplied |

Half B may write a client module that reads these variables. Half B must not call that client when `MODEL_MODE=replay`. Half B must not write a key into a prompt file, a test, or a log line.

A Done test that needs Azure pauses as NEEDS_HUMAN. **Verified Fact.** `Execution_Plan.md` section 11.

---

## Engineering defaults (not quality floors)

These numbers are engineering defaults so replay is repeatable. They are not groundedness floors. They are not citation floors. They are not abstention floors. FD-14 leaves those percent floors Unknown.

| Setting | Default | Authority | What it is not |
|---|---|---|---|
| Temperature | 0 | team-force, ED-P9A-02 | Not a quality percent |
| Maximum completion tokens | 800 | team-force, ED-P9A-02 | Not a business threshold. Raise in a later ADR if a freeze answer is truncated |
| Timeout milliseconds | Unknown | Not set here | FD-11 and FD-19 leave latency Unknown |

Worked example. Temperature 0 means the live path asks Azure for the most likely next token at each step. It does not mean 90 percent of answers are grounded. Groundedness is measured later and recorded as Unknown until that run.

---

## What the model may call

**Verified Fact.** FD-02. Phase 9 locked fact: no write tools.

| Call | Phase 9 |
|---|---|
| Lake REST `search_items`, `get_item`, `get_links`, `rule_at` | Application A retrieval code calls these. The model does not hold a write tool to the lake |
| `POST /api/approvals` | Forbidden for the model |
| Case, hold, feed, or owner write | Forbidden for the model |
| LangGraph write tools | Phase 10. Out of this configuration |

Retrieval runs in Application A code. The retrieved envelope is passed into the prompt as data. See `retrieval-pipeline.md`.

---

## Failure behaviour

| Event | Application A returns | Label |
|---|---|---|
| Replay file missing | HTTP 200 query body with `verdict: ABSTAIN`, `error_class: replay_miss` on the log, empty sentence, citations empty or the missing-data item if retrieval already found one | Inference of the HTTP mapping, authority: team-force. Replay miss is not a crash |
| Azure variables missing in `azure` mode | `error_class: missing_model_config`. No invented sentence | Inference |
| Azure call fails | `verdict: ABSTAIN`. Log the error class. Do not guess | Inference |
| `check_claim` rejects the model output | `verdict: ABSTAIN`. Citations may name the reject reason item such as `data.missing.lot_genealogy` | Verified Fact of Gate 3 |

---

## What this file does not do

This file does not call Azure. It does not invent a deployment name. It does not set a groundedness percent. It does not start Half B.
