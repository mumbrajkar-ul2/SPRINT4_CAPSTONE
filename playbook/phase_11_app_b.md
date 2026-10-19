# Phase 11 — Application B, built only from the lake

> Spine unit: 20 ported | Guidelines 3, 4, 14 | Decision gate: FD-17

Build phase. Two halves. Half A is the App B and parity-harness design. Half B builds App B from the lake and the parity harness. The coordinator spawns an executor for Half A, then for Half B after the reviewer returns HALF_A_ACCEPTED.

## Inputs

- Phase 5 lake `context-lake/` and `context-lake.sqlite3`
- Phase 6 specs `docs/12-specs/`
- Phase 9 App A `apps/app_a/` (for the comparison, not for rules)
- `Decision_Tracker.md` (section 6 row for Phase 11)

## Prompt

```text
# Phase 11 — Application B, built only from the lake

## Objective
Build Application B. It runs the same workflow as App A, takes its rules only from the Context Lake, and adds a context and lineage view. Build the parity harness that compares the two apps on identical scenarios and KPIs.

## Scope
Analyse and build across the App B UI and services, the lineage view, and the parity harness. Exclude: reading the legacy repo at build time; taking any rule from App A's code.

## Sub-stages
- 20p Application B from the lake. `apps/app_b/` plus `docs/model-comparison/`: `parity-harness.md`, `app-b-lineage.md`.

## Required analysis (Half A)
1. The portability design: App B builds from the lake alone, with no legacy-repo path.
2. The rule-resolution path: every rule App B uses cites a lake item id.
3. The parity-harness design: same scenarios, same dispositions, or each difference traced to a lake item.
4. The lineage view: it shows the correlation id from the Phase 10 audit chain.
For every element: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response for Half A. Wait for HALF_A_ACCEPTED.

## Required work (Half B, after acceptance)
1. Build `apps/app_b/` using only the lake for rules.
2. Build the lineage view that shows the correlation id.
3. Build the parity harness and run it on identical scenarios; trace each A-versus-B difference to a lake item.
4. Confirm App B runs with App A stopped, and that no build input points at the legacy repo.

## Evidence rules
Every rule App B uses cites a lake item id. Each A-versus-B difference traces to a lake item. Classify claims as Verified Fact, Inference, Assumption, or Unknown. Harness output is REAL.

## Constraints and guardrails
Do not read the legacy repo when building App B. Do not copy a rule from App A's code. Keep the comparison honest: B's only source is the lake. Plain speech.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| App B rule source | Only the Context Lake; never the legacy repo or App A's code |
| Parity rule | Same scenarios and dispositions, or each difference traced to a lake item |
| Lineage | The view shows the correlation id from the Phase 10 audit chain |
| Independence | App B runs with App A stopped |
| Screen library | The same React library as Application A. FastAPI on port 8110 serves the built files. The lineage view is a React view. Rules still come only from the lake. |

## Decision gate (before you start)
FD-17 parity-harness design — Team-Force; the SME advises. No Business Owner decision required.

## Required artifacts
`apps/app_b/` and `docs/model-comparison/`. Standard header on the docs.

## Completion gate
Half A PASS when the portability design, the rule-resolution path, and the parity-harness design are specified. Half B PASS when App B runs without App A, uses only lake rules, and every A-versus-B difference traces to a lake item. BLOCKED otherwise.

## Required final response (after each half)
Return the seven items.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/model-comparison/parity-harness.md` (Half A design, Half B results) | Header. The harness design. Each A-versus-B difference traced to a lake item. |
| `apps/app_b/` (Half B) | App B built only from the lake. `apps/app_b/ui/` is a React app. The lineage view is a React view and shows the correlation id. FastAPI on port 8110 serves the built files. No legacy-repo path in the build inputs. Sharing the React pattern does not share rule code. |
| `docs/model-comparison/app-b-lineage.md` (Half B) | Header. The lineage view showing the correlation id from the audit chain. |

## Done test

Run App B with App A stopped; it works. Run the parity harness; each difference traces to a lake item. Grep App B's build inputs for any legacy-repo path; there is none.

Screen library check for Application B, same three steps as Application A, against `apps/app_b/ui/`. Fail the stage when that folder is only `index.html`, `assets/app.js`, and `assets/styles.css`. The Phase 11 PASS row stays the record of the first run. The files that satisfy this check are built in Phase 17. The presenter layout is built in Phase 17.
