# Terms and metric fields

| Field | Value |
|---|---|
| Stage | Phase 18 / DEV-017. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p18b-doc-20261019-001 |
| Status | CLOSED for the nine terms. |
| Evidence sources | `context-lake/generated/context-lake.sqlite3` table `terms`, lake version 1.0.0 |
| Assumptions | The nine terms were already in version 1.0.0. A version raise is not required. |
| Unresolved issues | The signed owner of each metric cell stays Unknown. |
| Residual risks | A reader who expects a 1.0.2 pin will not find one. Phase 17's pin stays the live pin. |

The nine terms already have one definition each in the `terms` table.

| Term id | Definition in the table |
|---|---|
| `term.lot` | A production lot. domain.json names the object as production lot. |
| `term.wafer` | A wafer is a unit listed in domain-profile.json. |
| `term.tool` | A fab tool stored in fab_tools. |
| `term.chamber` | chamber on fab_tools holds a site code in the packaged data. |
| `term.recipe_revision_dispatch` | Value in process_steps.recipe_version. |
| `term.metrology_sample` | One metrology row joined to lots on lot_id. |
| `term.engineering_change` | One engineering_changes row. |
| `term.replay` | partner_feeds.processing_status REPLAY. Duplicate candidate. |
| `term.approval` | A person action. The lake does not approve from untrusted text. |

Metric fields for a demo count. The signed owner is Unknown. The field names stay visible.

| Field | Value |
|---|---|
| Population | Packaged rows named on the scenario page. |
| Event time | The event time on that page. |
| Ingestion time | The arrival or ingest time on that page. |
| Window | The date the page names, such as `2024-06-01`. |
| Exclusions | Rows the page says have no clock, or policies outside the window. |
| Status | The status word on the page, such as `REPLAY` or `APPROVED`. |
| Unit | One row, one policy, or one event. |
| Owner | Unknown |
