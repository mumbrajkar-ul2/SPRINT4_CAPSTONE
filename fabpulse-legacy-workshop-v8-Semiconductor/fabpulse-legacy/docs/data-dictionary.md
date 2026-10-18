# Domain data dictionary

The legacy application includes shared intake tables (`cases`, `events`, `source_messages`, `operating_costs`) and these additional domain tables:

- `fab_tools`: tool_id TEXT PRIMARY KEY, tool_family TEXT NOT NULL, chamber TEXT NOT NULL, recipe_rev TEXT NOT NULL
- `wafer_lots`: lot_id TEXT PRIMARY KEY, tool_id TEXT NOT NULL REFERENCES fab_tools(tool_id), wafer_count INTEGER NOT NULL, defect_count INTEGER NOT NULL, measured_yield REAL, engineering_hold INTEGER NOT NULL

Rows use synthetic identifiers, local site aliases, valid foreign-key relationships and generated historical values. The site, currency, revision and unit choices reflect multiple inherited operational practices rather than a canonical enterprise data model.

Inspect the joins and semantics before deriving KPIs.
