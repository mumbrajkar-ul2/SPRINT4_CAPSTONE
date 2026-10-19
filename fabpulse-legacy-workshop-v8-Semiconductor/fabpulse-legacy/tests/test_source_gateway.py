import json,unittest,os,tempfile,shutil
from pathlib import Path
from app import gateway_bridge,operational_report,store
CFG=json.loads((Path(__file__).resolve().parents[1]/'integration'/'source-gateway.json').read_text())
ROOT=Path(__file__).resolve().parents[1]
class TestGatewayAndDomain(unittest.TestCase):
    def setUp(self):
        self._tmp=tempfile.TemporaryDirectory(prefix='gw-legacy-')
        self._db=Path(self._tmp.name)/'legacy.sqlite3'
        shutil.copy2(ROOT/'data'/'legacy.sqlite3',self._db)
        self._old=store.DB
        store.DB=self._db
        os.environ['LEGACY_DB']=str(self._db)
    def tearDown(self):
        store.DB=self._old
        os.environ.pop('LEGACY_DB',None)
        try:
            self._tmp.cleanup()
        except PermissionError:
            pass
    def test_relations(self):
        report=operational_report.run()
        self.assertGreater(report['parent_records'],0)
        self.assertGreater(report['detail_records'],0)
        self.assertGreaterEqual(report['parents_with_detail'],1)
    def test_idempotent_ingestion(self):
        from app.store import connect
        with connect() as c: key=c.execute('SELECT '+CFG['parent_key']+' FROM '+CFG['parent_table']+' LIMIT 1').fetchone()[0]
        e={'message_id':'CHECK-'+CFG['event_kind'],'business_key':key,'system':CFG['sources'][0],'event_type':CFG['event_types'][0],'occurred_at':'2025-01-01T00:00:00Z'}
        one=gateway_bridge.apply([e]);two=gateway_bridge.apply([e]);self.assertIn(one['accepted'],(0,1));self.assertEqual(two['duplicates'],1)
    def test_invalid_rejected(self):
        self.assertEqual(gateway_bridge.apply([{'message_id':'bad'}])['invalid'],1)
if __name__=='__main__':unittest.main()
