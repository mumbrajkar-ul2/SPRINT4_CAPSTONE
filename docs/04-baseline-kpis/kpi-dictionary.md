# KPI dictionary

| Field | Value |
|---|---|
| Stage | Phase 0 / 4 Before-AI KPIs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p0-doc-20261018-001 |
| Status | FROZEN families. No targets invented |
| Evidence sources | FD-03; `Execution_Plan.md` section 9; `Project_Intent.md` section 14; BO-02; `app/baseline.py`; `app/workshop_check.py` |
| Assumptions | Headline pair follows the BO-02 working answer. The row is still PROPOSED |
| Unresolved issues | Exception cycle time and aged backlog have no tool field. Their baseline values are Unknown |
| Residual risks | Freezing `Project_Intent.md` section 9 (Context Lake) as the KPI set would be the old wrong default. FD-03 forbids that |

This dictionary freezes definitions. It does not set a target percent, a dollar benefit, or a success threshold.

## Frozen set

**Verified Fact.** FD-03 DECIDED 2026-10-18, authority team-force. The eight families are the families in `Execution_Plan.md` section 9. They match `Project_Intent.md` section 14. They are not the Context Lake list in `Project_Intent.md` section 9.

**Verified Fact.** BO-02 working answer. Exception cycle time and aged backlog are the two headline business KPIs. The other six families are supporting measures.

## Family table

| Family | Headline? | Measures in the plan | Honesty label | Baseline source today |
|---|---|---|---|---|
| Business outcome | Yes. The two headlines sit here | Exception cycle time. Aged backlog. The plan also names first-pass resolution, rework, and release delay as candidates | SIMULATED | Cycle time: Unknown. Aged backlog: Unknown. Related counts from `app/baseline.py`: records, open_cases, urgent_cases |
| Decision quality | Supporting | Correct disposition versus expert labels | PRECOMPUTED | Unknown. No expert-label run in this unit |
| Engineering productivity | Supporting | Discovery time. Tests accepted | REAL | Unknown. This unit did not time discovery or run unittest |
| Performance | Supporting | API p95. Retrieval p95. Agent time | REAL | Unknown. Server not started |
| Reliability | Supporting | Recovery. Duplicate rate. Replay correctness | REAL | Row counts exist (outages 72, partner feeds 8,567). Rates Unknown |
| AI quality | Supporting | Groundedness. Citation. Abstention. Rejected schema claims | REAL | Unknown. No model call |
| Cost | Supporting | Tokens. Cost per resolved scenario | REAL | Tokens Unknown. Synthetic hours_per_case 0.603 and mean_amount 4982.61 from the tool |
| ROI | Supporting | Avoided effort minus cost | EDUCATIONAL | Unknown. BO-11 forbids a monetary benefit claim |

## Headline definitions

### Exception cycle time

**What it is.** The time from the case's event or created time to a final operational disposition.

**Population.** Packaged cases in `data/legacy.sqlite3`.

**Clock.** Unknown until Phase 1 names the start field and the end field. `app/baseline.py` does not emit this number.

**Exclusions.** Unknown.

**Owner of the definition.** Business Owner for success use (BO-02). Team-Force for the query once the fields are named.

**Baseline value.** Unknown.

**Target.** Not set.

**Honesty.** SIMULATED when a number is later modelled on this synthetic set.

### Aged backlog

**What it is.** The count of cases that are still open and older than an agreed age.

**Population.** Cases that `app/baseline.py` would count in `open_cases` (`status != CLOSED`). That tool count is 89. That is not the aged subset.

**Age threshold.** Unknown. Not invented.

**Owner of the definition.** Business Owner for success use. SME for the operational meaning of open (BO-06a DECIDED).

**Baseline value.** Unknown.

**Related measured count.** open_cases = 89 on both tool runs. Honesty: REAL for the Python `status != CLOSED` test. That test is not the SME operational meaning of open.

**Target.** Not set.

**Honesty.** SIMULATED when a later aged count is modelled.

## Supporting measures the current tools do emit

These are frozen as observed baseline fields. They are not headline KPIs.

| Field | Meaning in `app/baseline.py` | Honesty |
|---|---|---|
| records | Count of rows in `cases` | REAL |
| open_cases | Count where `status != CLOSED` | REAL for that test |
| urgent_cases | Count where `priority()` returns urgent | REAL for the Python rule |
| mean_amount | Mean of `cases.amount`, rounded to 2 decimals | SIMULATED money |
| sites | Distinct `cases.site` values | REAL |
| hours_per_case | Sum of `operating_costs.labor_hours` divided by sum of `operating_costs.total_cases`, rounded to 3 decimals | SIMULATED labor |

## What is not in this dictionary

`Project_Intent.md` section 9 (Context Lake, semantic layer, knowledge graph) is not a KPI family.

No first-pass resolution rate is invented. No rework rate is invented. No ROI dollar is invented.
