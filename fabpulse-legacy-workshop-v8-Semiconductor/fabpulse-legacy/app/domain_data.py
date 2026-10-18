import json,random,datetime
from .store import connect,setup

def generate_domain(count=6000,seed=4100):
    r=random.Random(seed+9211)
    sites=['IN-BLR','US-TX','DE-BY','JP-KN','GB-ENG','BR-SP']
    with connect() as c:
        c.execute('CREATE TABLE IF NOT EXISTS fab_tools(tool_id TEXT PRIMARY KEY, tool_family TEXT NOT NULL, chamber TEXT NOT NULL, recipe_rev TEXT NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS wafer_lots(lot_id TEXT PRIMARY KEY, tool_id TEXT NOT NULL REFERENCES fab_tools(tool_id), wafer_count INTEGER NOT NULL, defect_count INTEGER NOT NULL, measured_yield REAL, engineering_hold INTEGER NOT NULL)')
        c.execute('DELETE FROM wafer_lots')
        c.execute('DELETE FROM fab_tools')
        n=max(30,count//8)
        parents=[]
        for i in range(n):
            row=(f'T{i:07d}',r.choice(['etch','deposition','lithography','CMP']),r.choice(sites),r.choice(['R01','R02','R03']))
            c.execute('INSERT INTO fab_tools VALUES ({})'.format(','.join('?'*len(row))),row)
            parents.append(row[0])
        for i in range(count):
            tool_id=r.choice(parents)
            day=(datetime.date(2023,1,1)+datetime.timedelta(days=r.randint(0,1090))).isoformat()
            row=(f'L{i:08d}',tool_id,r.choice([12,25,50]),r.randint(0,11),round(r.uniform(80,99.9),3),1 if r.random()<.07 else 0)
            c.execute('INSERT INTO wafer_lots VALUES ({})'.format(','.join('?'*len(row))),row)
    return {'entity':'fab_tools','entity_count':n,'detail':'wafer_lots','detail_count':count}

if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser(); a.add_argument('--count',type=int,default=6000); a.add_argument('--seed',type=int,default=4100); args=a.parse_args()
 print(json.dumps(generate_domain(args.count,args.seed)))
