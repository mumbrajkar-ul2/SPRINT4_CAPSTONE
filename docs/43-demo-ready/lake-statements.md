# Lake statements for the live demo

| Field | Value |
|---|---|
| Stage | Phase 17 / Live demo and React screens. Half A. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p17a-doc-20261019-001 |
| Status | The YAML files are in `docs/43-demo-ready/lake-yaml/`. The pinned sqlite stays version 1.0.0. |
| Evidence sources | Packaged columns named below. Existing items `data.feed.replay`, `data.join.recipe_mismatch`, `data.clock.event_vs_arrival_evidence`, `data.policy_register.overlap`, `data.contract.decision_policies_archive`. |
| Assumptions | Application B reads the lake items. Application A may also read the packaged columns. The values must match. |
| Unresolved issues | Historical phase docs keep the pin they measured. That pin is still the live pin. |
| Residual risks | Copying a raw data row into the lake would fail the Phase 5 exclude rule. |

Each new item is a statement with a locator. It is not a copy of a raw row.

## Replay pair

Item `data.demo.replay_pair`. Ref `C00001646`. `FEED-000000000` ingested `2022-04-25T19:09`. `REPLAY-000000000` ingested `2022-04-25T20:09`. Same source time `2022-04-25T19:39`. Locator: `partner_feeds` for that ref. The packaged store stays at 67 `REPLAY` rows. That count is already in `data.feed.replay`.

## Recipe rows

Item `data.demo.recipe_times`.

- Step `PS000000016`. Etch. `2023-01-05T16:00` to `2023-01-05T23:00`. Dispatch recipe R02. Tool `T0000013` recipe R01. The tool row has no effective date.
- Change `ECN0000001`. Etch. R01 to R02. Effective `2023-01-01T07:00`. Status `APPROVED`.

Locator: the process-step row and the engineering-change row. The existing item `data.join.recipe_mismatch` stays the mismatch statement.

## Clocks

Item `data.demo.backfill_clock`. Event `E-00000000`. Kind `tool_alarm`. Event time `2020-12-30`. Arrival time `2021-01-01`. The page says metrology samples have no clock. Locator: the evidence event row. The existing item `data.clock.event_vs_arrival_evidence` stays the two-clock statement.

## Policy date

Item `data.demo.policy_windows`. Five US policies with `valid_from` and `valid_to`. On `2024-06-01`, four of them are in force. `POL-0018` runs `2024-01-01` through `2024-12-31`. `POL-0034` starts `2025-01-01`, so it is not in force on that date. Locator: `policy_register` for site `FAB-00000002`. The existing item `data.policy_register.overlap` stays the overlap statement.

## Implements link

Item `code.transformed.evaluate_live_policy`. It names the transformed function `evaluate_live_policy` that Application A calls from `apps/app_a/rules/adapter.py`. Half B adds an `implements` link from `rule.recipe_release.limit.v2023.emea` to that code item.

The rule trace on Application B shows five ordered steps:

1. Historical decision `decision.bp4.four_programs`.
2. Earlier code `code.legacy_policy.js_allow`.
3. Specification `data.contract.decision_policies_archive`.
4. Test `test.rule.recipe_release.emea_2023`.
5. Transformed implementation `code.transformed.evaluate_live_policy`.

## Version

The YAML files are statements. They are not compiled into the pinned sqlite. A build that adds them changes the item ids search returns, and the saved replies miss. The live pin stays version 1.0.0, hash `f5be2b320a898756b6730edb539fcaeac422ded8f7e37b942c49ea65b01c12b8`. The ADR is `docs/10-architecture/adrs/adr-lake-demo-statements-1.0.1.md`.
