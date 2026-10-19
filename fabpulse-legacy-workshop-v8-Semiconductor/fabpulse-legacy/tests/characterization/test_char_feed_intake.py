"""Feed-intake characterization. Tests call apply. New names are tested after they exist."""
import json
import sqlite3
import unittest

from app import gateway_bridge
from app.integration import consume_source_messages

from .harness import (
    INHERITED_ROOT,
    PACKAGED_ENTERPRISE,
    PACKAGED_LEGACY,
    TempLegacyMixin,
    inbox_comparable_rows,
    readonly_connect,
)


class TestFeedIntakeReadOnly(unittest.TestCase):
    def test_packaged_inbox_one_received(self):
        conn = readonly_connect(PACKAGED_LEGACY)
        rows = list(conn.execute("SELECT message_id, status FROM gateway_inbox"))
        conn.close()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["message_id"], "CHECK-semiconductor_lot")
        self.assertEqual(rows[0]["status"], "RECEIVED")

    def test_evidence_clock_mismatch_count(self):
        """CT-13."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        count = conn.execute(
            "SELECT COUNT(*) FROM evidence_events WHERE arrival_time != event_time"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 11985)

    def test_partner_feed_clock_mismatch_count(self):
        """CT-14."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute(
            "SELECT COUNT(*) FROM partner_feeds WHERE ingest_ts != source_ts"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 7471)

    def test_reference_version_overlap_count(self):
        """CT-15."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute(
            """
            SELECT COUNT(*) FROM reference_versions a
            JOIN reference_versions b
              ON a.ref_key = b.ref_key
             AND a.version < b.version
             AND a.valid_from < COALESCE(b.valid_to, '9999-12-31')
             AND b.valid_from < COALESCE(a.valid_to, '9999-12-31')
            """
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 45)

    def test_packaged_source_messages_count(self):
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute("SELECT COUNT(*) FROM source_messages").fetchone()[0]
        conn.close()
        self.assertEqual(count, 15)

    def test_gateway_event_json_has_both_clocks(self):
        """CT-16. Event object the gateway builds has occurred_at and published_at."""
        source = (INHERITED_ROOT / "services" / "source_gateway" / "server.py").read_text(encoding="utf-8")
        self.assertIn("'occurred_at'", source)
        self.assertIn("'published_at'", source)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "source_gateway_server",
            INHERITED_ROOT / "services" / "source_gateway" / "server.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        event = module.build_event_record("L00000000", "mes", "lot_started", 0, 0)
        self.assertIn("occurred_at", event)
        self.assertIn("published_at", event)
        self.assertTrue(event["occurred_at"])
        self.assertTrue(event["published_at"])


class TestFeedIntakeWrites(TempLegacyMixin, unittest.TestCase):
    def _lot_id(self):
        conn = sqlite3.connect(self.db_path)
        lot = conn.execute("SELECT lot_id FROM wafer_lots ORDER BY lot_id LIMIT 1").fetchone()[0]
        conn.close()
        return lot

    def test_apply_rejects_missing_required_fields(self):
        result = gateway_bridge.apply([{"message_id": "bad"}])
        self.assertEqual(result["invalid"], 1)
        self.assertEqual(result["accepted"], 0)

    def test_apply_rejects_missing_occurred_at(self):
        payload = {
            "message_id": "NO-CLOCK-1",
            "business_key": self._lot_id(),
            "system": "mes",
            "event_type": "lot_started",
        }
        result = gateway_bridge.apply([payload])
        self.assertEqual(result["invalid"], 1)
        self.assertEqual(result["accepted"], 0)

    def test_apply_rejects_unknown_lot(self):
        payload = {
            "message_id": "UNKNOWN-LOT-1",
            "business_key": "NOT-A-LOT",
            "system": "mes",
            "event_type": "lot_started",
            "occurred_at": "2025-01-01T00:00:00Z",
        }
        result = gateway_bridge.apply([payload])
        self.assertEqual(result["invalid"], 1)

    def test_apply_accepts_new_valid_event(self):
        occurred = "2025-02-02T03:00:00Z"
        payload = {
            "message_id": "NEW-VALID-1",
            "business_key": self._lot_id(),
            "system": "mes",
            "event_type": "lot_started",
            "occurred_at": occurred,
        }
        result = gateway_bridge.apply([payload])
        self.assertEqual(result["accepted"], 1)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT status, event_time FROM gateway_inbox WHERE message_id=?",
            ("NEW-VALID-1",),
        ).fetchone()
        conn.close()
        self.assertEqual(row["status"], "RECEIVED")
        self.assertEqual(row["event_time"], occurred)

    def test_apply_duplicate_message_id(self):
        payload = {
            "message_id": "DUP-1",
            "business_key": self._lot_id(),
            "system": "mes",
            "event_type": "lot_started",
            "occurred_at": "2025-01-01T00:00:00Z",
        }
        first = gateway_bridge.apply([payload])
        second = gateway_bridge.apply([payload])
        self.assertEqual(first["accepted"], 1)
        self.assertEqual(second["duplicates"], 1)

    def test_consume_source_messages_returns_list(self):
        batch = consume_source_messages(3)
        self.assertIsInstance(batch, list)
        self.assertLessEqual(len(batch), 3)
        if batch:
            self.assertIn("message_id", batch[0])
            self.assertIn("payload", batch[0])

    def test_shadow_intake_apply_matches_apply(self):
        """SH-FI. Same events on two copies. received_at is omitted. PROPOSED, owner Team-Force."""
        if not hasattr(gateway_bridge, "intake_apply"):
            self.skipTest("intake_apply is added in slice 1 after these apply tests exist")
        from .harness import copy_packaged_legacy, point_store, restore_store, TempLegacyMixin as _
        import tempfile
        from pathlib import Path

        events = [
            {"message_id": "bad"},
            {
                "message_id": "UNKNOWN-LOT-SH",
                "business_key": "NOT-A-LOT",
                "system": "mes",
                "event_type": "lot_started",
                "occurred_at": "2025-01-01T00:00:00Z",
            },
            {
                "message_id": "VALID-SH-1",
                "business_key": self._lot_id(),
                "system": "mes",
                "event_type": "lot_started",
                "occurred_at": "2025-03-01T00:00:00Z",
            },
            {
                "message_id": "VALID-SH-1",
                "business_key": self._lot_id(),
                "system": "mes",
                "event_type": "lot_started",
                "occurred_at": "2025-03-01T00:00:00Z",
            },
        ]
        tmp_a = tempfile.TemporaryDirectory(prefix="sh-fi-a-")
        tmp_b = tempfile.TemporaryDirectory(prefix="sh-fi-b-")
        path_a = copy_packaged_legacy(Path(tmp_a.name))
        path_b = copy_packaged_legacy(Path(tmp_b.name))
        prev = point_store(path_a)
        try:
            old_result = gateway_bridge.apply(events)
        finally:
            restore_store(prev)
        prev = point_store(path_b)
        try:
            new_result = gateway_bridge.intake_apply(events)
        finally:
            restore_store(prev)
        self.assertEqual(old_result["accepted"], new_result["accepted"])
        self.assertEqual(old_result["duplicates"], new_result["duplicates"])
        self.assertEqual(old_result["invalid"], new_result["invalid"])
        self.assertEqual(old_result["received"], new_result["received"])
        self.assertEqual(inbox_comparable_rows(path_a), inbox_comparable_rows(path_b))
        tmp_a.cleanup()
        tmp_b.cleanup()


if __name__ == "__main__":
    unittest.main()
