import datetime, json, random
from .store import connect
TABLES = [('process_steps', 'step_id TEXT PRIMARY KEY, lot_id TEXT NOT NULL REFERENCES wafer_lots(lot_id), tool_id TEXT NOT NULL REFERENCES fab_tools(tool_id), recipe_version TEXT NOT NULL, step_name TEXT NOT NULL, started_at TEXT NOT NULL, ended_at TEXT'), ('metrology', 'sample_id TEXT PRIMARY KEY, lot_id TEXT NOT NULL REFERENCES wafer_lots(lot_id), parameter TEXT NOT NULL, measured REAL NOT NULL, unit TEXT NOT NULL, spec_low REAL NOT NULL, spec_high REAL NOT NULL'), ('engineering_changes', 'ecn_id TEXT PRIMARY KEY, tool_family TEXT NOT NULL, from_rev TEXT NOT NULL, to_rev TEXT NOT NULL, effective_at TEXT NOT NULL, approval_state TEXT NOT NULL'), ('supplier_parts', 'part_id TEXT PRIMARY KEY, vendor TEXT NOT NULL, tool_family TEXT NOT NULL, lead_days INTEGER NOT NULL, qualification_state TEXT NOT NULL')]
DOMAIN = 'Semiconductor'
PHRASES = ['recipe revision differs from effective ECN', 'metrology excursion follows chamber maintenance', 'wafer hold created during incomplete reroute']

def expand(seed=4100):
    rng = random.Random(seed + 77019)
    with connect() as c:
        for name,ddl in TABLES:
            c.execute('CREATE TABLE IF NOT EXISTS '+name+'('+ddl+')')
        for name,_ in reversed(TABLES):
            c.execute('DELETE FROM '+name)
        parents = [x[0] for x in c.execute('SELECT tool_id FROM fab_tools')]
        n=len(parents)
        if not n: raise RuntimeError('Domain data missing: generate base data first')
        date0=datetime.datetime(2023,1,1,tzinfo=datetime.timezone.utc)
        def ts(i):return (date0+datetime.timedelta(hours=i*7)).isoformat()
        lots=[dict(x) for x in c.execute('SELECT lot_id,tool_id FROM wafer_lots ORDER BY lot_id')]
        tools=[dict(x) for x in c.execute('SELECT tool_id,tool_family FROM fab_tools ORDER BY tool_id')]
        for i,lot in enumerate(lots):
            c.execute('INSERT INTO process_steps VALUES (?,?,?,?,?,?,?)',(f'PS{i:09d}',lot['lot_id'],lot['tool_id'],rng.choice(['R01','R02','R03','R04']),rng.choice(['etch','litho','CMP','implant']),ts(i),ts(i+1) if i%7 else None))
            c.execute('INSERT INTO metrology VALUES (?,?,?,?,?,?,?)',(f'MET{i:09d}',lot['lot_id'],rng.choice(['CD','overlay','thickness']),round(rng.gauss(52,9),3),rng.choice(['nm','angstrom']),40,60))
        for i,tool in enumerate(tools):
            c.execute('INSERT INTO engineering_changes VALUES (?,?,?,?,?,?)',(f'ECN{i:07d}',tool['tool_family'],'R01','R02',ts(i),rng.choice(['DRAFT','APPROVED','REJECTED'])))
            c.execute('INSERT INTO supplier_parts VALUES (?,?,?,?,?)',(f'SP{i:07d}',rng.choice(['Vendor-A','Vendor-B','Vendor-C']),tool['tool_family'],rng.randint(7,180),rng.choice(['QUALIFIED','PENDING','EXPIRED'])))
        return {t:c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t,_ in TABLES}
