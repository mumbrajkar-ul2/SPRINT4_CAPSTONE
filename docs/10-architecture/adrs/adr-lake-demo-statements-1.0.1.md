# ADR: Demo statements stay beside the pinned lake

| Field | Value |
|---|---|
| Stage | Phase 17 lake edit. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p17b-doc-20261019-001 |
| Status | ACCEPTED for this edit. Authority: team-force. |
| Evidence sources | FD-22; `docs/43-demo-ready/lake-statements.md` |
| Assumptions | The five statements are YAML with a locator. They are not compiled into the pinned sqlite. |
| Unresolved issues | The nine terms were already in version 1.0.0. Phase 18 does not raise the version. |
| Residual risks | Compiling the new YAML changes which item ids search returns. The saved replies then miss and the freeze set abstains. |

The pinned lake stays version 1.0.0. The sqlite hash stays `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8` in `context-lake/generated/app-b-pin.json`.

The statement files are `data.demo.replay_pair`, `data.demo.recipe_times`, `data.demo.backfill_clock`, `data.demo.policy_windows`, and `code.transformed.evaluate_live_policy`. They live in `docs/43-demo-ready/lake-yaml/`. Each one is a statement with a locator. None of them copies a raw data row. The demo session shows those same facts.

`rule.recipe_release.limit.v2023.emea` does not gain a new `implements` link inside the pinned sqlite. The edges that already exist stay the answers for the relationship questions.

The Phase 5 file `context-lake/review/lake-version.md` stays the record of version 1.0.0. This ADR is the record that Phase 17 did not change that pin.
