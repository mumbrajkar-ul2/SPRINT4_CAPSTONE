"""Reconciliation characterization. Tests call reconcile. New names are tested after they exist."""
import inspect
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import partner_feeds

from .harness import (
    PACKAGED_LEGACY,
    TempLegacyMixin,
    copy_packaged_legacy,
    expected_reconcile_outcome,
    feed_status_map,
    point_store,
    readonly_connect,
    restore_store,
)


class TestReconciliationReadOnly(unittest.TestCase):
    def test_untrusted_feed_note_count(self):
        """CT-30."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute(
            "SELECT COUNT(*) FROM partner_feeds "
            "WHERE raw_json LIKE '%auto approve%' OR raw_json LIKE '%disregard validation%'"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 86)

    def test_reconcile_default_limit_is_1000(self):
        sig = inspect.signature(partner_feeds.reconcile)
        self.assertEqual(sig.parameters["limit"].default, 1000)


class TestReconciliationWrites(TempLegacyMixin, unittest.TestCase):
    def _counts(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = {r[0]: r[1] for r in conn.execute("SELECT processing_status, COUNT(*) FROM partner_feeds GROUP BY 1")}
        conn.close()
        return rows

    def test_packaged_replay_count_before_reconcile(self):
        """CT-06."""
        self.assertEqual(self._counts().get("REPLAY", 0), 67)

    def test_packaged_new_and_retry_counts(self):
        counts = self._counts()
        self.assertEqual(counts.get("NEW", 0), 8000)
        self.assertEqual(counts.get("RETRY", 0), 500)

    def test_reconcile_replay_becomes_duplicate(self):
        """CT-07. Default limit 1000. Record the actual flipped count."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        before_rows = list(
            conn.execute(
                "SELECT feed_id, schema_rev, processing_status, raw_json FROM partner_feeds "
                "WHERE processing_status='REPLAY' ORDER BY feed_id"
            )
        )
        replay_ids = [r["feed_id"] for r in before_rows]
        conn.close()
        self.assertEqual(len(replay_ids), 67)
        result = partner_feeds.reconcile()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        flipped = []
        remaining = []
        for feed_id in replay_ids:
            row = conn.execute(
                "SELECT processing_status, error_reason FROM partner_feeds WHERE feed_id=?",
                (feed_id,),
            ).fetchone()
            if row["processing_status"] == "REPLAY":
                remaining.append(feed_id)
            else:
                flipped.append((feed_id, row["processing_status"], row["error_reason"]))
        conn.close()
        self.assertEqual(len(flipped) + len(remaining), 67)
        # Current reconcile() tests schema/key before REPLAY. A replay with no
        # business_key or schema_rev unsupported becomes REJECTED first.
        before_map = {row["feed_id"]: row for row in before_rows}
        duplicate = 0
        for feed_id, status, reason in flipped:
            expected_status, expected_reason = expected_reconcile_outcome(before_map[feed_id])
            self.assertEqual(status, expected_status, feed_id)
            self.assertEqual(reason, expected_reason, feed_id)
            if status == "DUPLICATE":
                self.assertEqual(reason, "replayed source message", feed_id)
                duplicate += 1
        self.assertEqual(result["duplicate"], duplicate)

    def test_reconcile_unsupported_schema_rejected(self):
        """CT-08."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO partner_feeds VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                "CHAR-UNSUP-1",
                "north",
                "unsupported",
                "2025-01-01T00:00:00+00:00",
                "2025-01-01T00:00:00+00:00",
                "C00000001",
                "lot",
                json.dumps({"business_key": "C00000001", "quantity": 1}),
                "NEW",
                None,
            ),
        )
        conn.commit()
        conn.close()
        partner_feeds.reconcile(limit=20000)
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT processing_status, error_reason FROM partner_feeds WHERE feed_id='CHAR-UNSUP-1'"
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "REJECTED")
        self.assertEqual(row[1], "schema/key validation")

    def test_reconcile_missing_business_key_rejected(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO partner_feeds VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                "CHAR-NOKEY-1",
                "north",
                "1.0",
                "2025-01-01T00:00:00+00:00",
                "2025-01-01T00:00:00+00:00",
                "C00000001",
                "lot",
                json.dumps({"quantity": 1}),
                "NEW",
                None,
            ),
        )
        conn.commit()
        conn.close()
        partner_feeds.reconcile(limit=20000)
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT processing_status, error_reason FROM partner_feeds WHERE feed_id='CHAR-NOKEY-1'"
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "REJECTED")
        self.assertEqual(row[1], "schema/key validation")

    def test_reconcile_negative_quantity_rejected(self):
        """CT-09."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO partner_feeds VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                "CHAR-NEG-1",
                "north",
                "1.0",
                "2025-01-01T00:00:00+00:00",
                "2025-01-01T00:00:00+00:00",
                "C00000001",
                "lot",
                json.dumps({"business_key": "C00000001", "quantity": -3}),
                "NEW",
                None,
            ),
        )
        conn.commit()
        conn.close()
        partner_feeds.reconcile(limit=20000)
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT processing_status, error_reason FROM partner_feeds WHERE feed_id='CHAR-NEG-1'"
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "REJECTED")
        self.assertEqual(row[1], "quantity out of range")

    def test_reconcile_valid_new_accepted(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO partner_feeds VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                "CHAR-OK-1",
                "north",
                "1.0",
                "2025-01-01T00:00:00+00:00",
                "2025-01-01T00:00:00+00:00",
                "C00000001",
                "lot",
                json.dumps({"business_key": "C00000001", "quantity": 0}),
                "NEW",
                None,
            ),
        )
        conn.commit()
        conn.close()
        partner_feeds.reconcile(limit=20000)
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT processing_status, error_reason FROM partner_feeds WHERE feed_id='CHAR-OK-1'"
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "ACCEPTED")
        self.assertIsNone(row[1])

    def test_reconcile_does_not_use_untrusted_note(self):
        """CT-31. Note text stays data. Status follows the four rules only."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        before = list(
            conn.execute(
                "SELECT feed_id, schema_rev, processing_status, raw_json FROM partner_feeds "
                "WHERE raw_json LIKE '%auto approve%' OR raw_json LIKE '%disregard validation%'"
            )
        )
        conn.close()
        self.assertEqual(len(before), 86)
        partner_feeds.reconcile(limit=20000)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        for row in before:
            after = conn.execute(
                "SELECT processing_status, error_reason, raw_json FROM partner_feeds WHERE feed_id=?",
                (row["feed_id"],),
            ).fetchone()
            expected_status, expected_reason = expected_reconcile_outcome(row)
            self.assertEqual(after["processing_status"], expected_status, row["feed_id"])
            self.assertEqual(after["error_reason"], expected_reason, row["feed_id"])
            self.assertEqual(after["raw_json"], row["raw_json"])
            self.assertTrue(
                "auto approve" in after["raw_json"] or "disregard validation" in after["raw_json"]
            )
        conn.close()

    def test_reconcile_does_not_delete_rows(self):
        conn = sqlite3.connect(self.db_path)
        before = conn.execute("SELECT COUNT(*) FROM partner_feeds").fetchone()[0]
        conn.close()
        partner_feeds.reconcile(limit=20000)
        conn = sqlite3.connect(self.db_path)
        after = conn.execute("SELECT COUNT(*) FROM partner_feeds").fetchone()[0]
        conn.close()
        self.assertEqual(before, after)

    def test_shadow_reconcile_feeds_matches_reconcile(self):
        """SH-RC. Two copies. Same limit 1000. Exact match on counts and per-feed_id status."""
        if not hasattr(partner_feeds, "reconcile_feeds"):
            self.skipTest("reconcile_feeds is added in slice 2 after these reconcile tests exist")
        tmp_a = tempfile.TemporaryDirectory(prefix="sh-rc-a-")
        tmp_b = tempfile.TemporaryDirectory(prefix="sh-rc-b-")
        path_a = copy_packaged_legacy(Path(tmp_a.name))
        path_b = copy_packaged_legacy(Path(tmp_b.name))
        prev = point_store(path_a)
        try:
            old_result = partner_feeds.reconcile(limit=1000)
        finally:
            restore_store(prev)
        prev = point_store(path_b)
        try:
            new_result = partner_feeds.reconcile_feeds(limit=1000)
        finally:
            restore_store(prev)
        self.assertEqual(old_result, new_result)
        map_a, count_a = feed_status_map(path_a)
        map_b, count_b = feed_status_map(path_b)
        self.assertEqual(count_a, count_b)
        self.assertEqual(map_a, map_b)
        tmp_a.cleanup()
        tmp_b.cleanup()


if __name__ == "__main__":
    unittest.main()
