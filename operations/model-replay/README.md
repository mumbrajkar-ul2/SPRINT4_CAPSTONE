# Model replay file rule

| Field | Value |
|---|---|
| Stage | Phase 8 / 18 Delivery foundations. Half B platform. |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p8b-doc-20261018-001 |
| Status | IMPLEMENTATION. FD-13 DECIDED. Replay wiring only. |
| Evidence sources | `Execution_Plan.md` section 10; `docs/17-implementation-prd/implementation-prd.md` ED-P8A-08; `Decision_Tracker.md` FD-13 |
| Assumptions | Phase 9 writes rehearsal files when a person runs a live prompt. This folder starts with one unit-test file. |
| Unresolved issues | How many rehearsal files Phase 9 will add stays Unknown. |
| Residual risks | Inventing a sentence for a missing hash would hide a cache miss. |

Replay reads a file from this folder. The file name is the SHA-256 hex digest of the exact prompt bytes. The file body is the saved rehearsal response. If the file is missing, `operations/replay_lookup.py` returns `error_class: replay_miss`. It does not open a public-network socket. It does not invent a model sentence.

`MODEL_MODE=replay` is the Compose default. There is no third offline mode.

Worked example. Prompt bytes `phase8-replay-fixture-prompt` hash to `adeac7ef972529e9ea945d0403abcd627b195c222b8c296f5f76e6a7ef7d3ef7`. That file holds a PRECOMPUTED unit-test body. It is not a live model answer.

Phase 9 Half B added PRECOMPUTED freeze-set files for P-EXPLAIN-CONFLICT, P-NL-QUERY, and P-DRAFT-PLAN at semver 1.0.0. `apps/app_a/eval/write_replay_fixtures.py` writes them. Pipeline scores against those files are REAL. The file bodies are not live Azure answers. A later Azure rehearsal, when a person sets `MODEL_MODE=azure` and supplies a key, can replace a file under the same hash. Until then those rows stay PRECOMPUTED. They are not a live pass.
