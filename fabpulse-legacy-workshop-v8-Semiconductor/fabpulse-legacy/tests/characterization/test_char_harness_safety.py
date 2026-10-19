"""Harness safety. Packaged files stay unread for write. Current open GET is recorded."""
import ast
import unittest
from pathlib import Path

from .harness import (
    INHERITED_ROOT,
    PACKAGED_ENTERPRISE,
    PACKAGED_LEGACY,
    count_archive_eml_approve_or_ignore,
    count_bundled_source_claim,
    count_source_documents_untrusted,
    hashes_from_register,
    readonly_connect,
    sha256_file,
)

CHAR_DIR = Path(__file__).resolve().parent
WRITE_MODULE_FILES = (
    "test_char_feed_intake.py",
    "test_char_reconciliation.py",
    "test_char_baseline_parity.py",
)


class TestHarnessSafety(unittest.TestCase):
    def test_write_tests_set_temp_legacy_db(self):
        """CT-38. Write tests point store.DB at a temporary copy."""
        for name in WRITE_MODULE_FILES:
            text = (CHAR_DIR / name).read_text(encoding="utf-8")
            self.assertIn("TempLegacyMixin", text, name)
            tree = ast.parse(text)
            mixin_used = False
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    bases = [getattr(b, "id", "") for b in node.bases if isinstance(b, ast.Name)]
                    if "TempLegacyMixin" in bases:
                        mixin_used = True
            self.assertTrue(mixin_used, name)
        harness = (CHAR_DIR / "harness.py").read_text(encoding="utf-8")
        self.assertIn("copy_packaged_legacy", harness)
        self.assertIn("point_store", harness)

    def test_packaged_db_hashes_unchanged(self):
        """CT-39. Packaged hashes match the source register."""
        expected = hashes_from_register()
        self.assertEqual(sha256_file(PACKAGED_LEGACY), expected["data/legacy.sqlite3"])
        self.assertEqual(sha256_file(PACKAGED_ENTERPRISE), expected["data/enterprise_legacy.sqlite3"])

    def test_get_cases_without_identity_returns_200(self):
        """CT-35. Current server skips an identity header. Live HTTP is Unknown."""
        source = (INHERITED_ROOT / "app" / "server.py").read_text(encoding="utf-8")
        self.assertIn("if u.path=='/api/cases':", source)
        self.assertNotIn("Authorization", source)
        self.assertNotIn("X-User", source)
        self.assertNotIn("identity", source.lower())
        self.assertIn("return self.respond(200,{'items':items,'limit':limit,'offset':offset})", source)
        live_http = "Unknown"
        self.assertEqual(live_http, "Unknown")

    def test_unassigned_workflow_tasks(self):
        """CT-36. Read-only count."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        count = conn.execute("SELECT COUNT(*) FROM workflow_tasks WHERE assigned_to IS NULL").fetchone()[0]
        conn.close()
        self.assertEqual(count, 695)

    def test_incidents_body(self):
        """CT-37. Handler lists INC-2019-0082. INC-2025-014 has no owner. Live HTTP is Unknown."""
        source = (INHERITED_ROOT / "app" / "server.py").read_text(encoding="utf-8")
        self.assertIn("INC-2019-0082", source)
        self.assertNotIn("INC-2025-014", source)
        incident = (INHERITED_ROOT / "operations" / "incidents" / "INC-2025-014.md").read_text(encoding="utf-8")
        self.assertIn("Follow-up owner unknown", incident)
        self.assertNotIn("owner:", incident.lower().replace("follow-up owner unknown", ""))
        live_http = "Unknown"
        self.assertEqual(live_http, "Unknown")

    def test_untrusted_bundled_lake_events(self):
        """CT-32. Bundled lake events with source_claim."""
        self.assertEqual(count_bundled_source_claim(), 150)

    def test_untrusted_archive_eml(self):
        """CT-33. Archive .eml files containing approve or ignore."""
        self.assertEqual(count_archive_eml_approve_or_ignore(), 3)

    def test_untrusted_source_documents(self):
        """CT-34. Source documents whose body contains approve, ignore, or release all holds."""
        self.assertEqual(count_source_documents_untrusted(), 22)


if __name__ == "__main__":
    unittest.main()
