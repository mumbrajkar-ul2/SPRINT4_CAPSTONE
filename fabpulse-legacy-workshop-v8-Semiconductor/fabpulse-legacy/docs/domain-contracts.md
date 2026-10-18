# Domain records and local endpoints

- `GET /api/domain/process_steps?limit=20&offset=0` — relational record with schema `step_id TEXT PRIMARY KEY, lot_id TEXT NOT NULL REFERENCES wafer_lots(lot_id), tool_id TEXT NOT NULL REFERENCES fab_tools(tool_id), recipe_version TEXT NOT NULL, step_name TEXT NOT NULL, started_at TEXT NOT NULL, ended_at TEXT`
- `GET /api/domain/metrology?limit=20&offset=0` — relational record with schema `sample_id TEXT PRIMARY KEY, lot_id TEXT NOT NULL REFERENCES wafer_lots(lot_id), parameter TEXT NOT NULL, measured REAL NOT NULL, unit TEXT NOT NULL, spec_low REAL NOT NULL, spec_high REAL NOT NULL`
- `GET /api/domain/engineering_changes?limit=20&offset=0` — relational record with schema `ecn_id TEXT PRIMARY KEY, tool_family TEXT NOT NULL, from_rev TEXT NOT NULL, to_rev TEXT NOT NULL, effective_at TEXT NOT NULL, approval_state TEXT NOT NULL`
- `GET /api/domain/supplier_parts?limit=20&offset=0` — relational record with schema `part_id TEXT PRIMARY KEY, vendor TEXT NOT NULL, tool_family TEXT NOT NULL, lead_days INTEGER NOT NULL, qualification_state TEXT NOT NULL`

All records are synthetic. Resource endpoints expose legacy read models and should not be assumed to be complete domain APIs.
