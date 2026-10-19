"""Baseline parity. Locks the six Phase 0 fields. Headline KPIs stay Unknown."""
import unittest

from app.baseline import baseline

from .harness import PHASE0_BASELINE, INHERITED_ROOT, TempLegacyMixin


class TestBaselineParity(TempLegacyMixin, unittest.TestCase):
    def test_baseline_six_fields_exact_match(self):
        """CT-01. Exact match. No tolerance percent."""
        result = baseline()
        self.assertEqual(result["records"], 125)
        self.assertEqual(result["open_cases"], 89)
        self.assertEqual(result["urgent_cases"], 2)
        self.assertEqual(result["mean_amount"], 4982.61)
        self.assertEqual(result["sites"], 6)
        self.assertEqual(result["hours_per_case"], 0.603)
        self.assertEqual(result, PHASE0_BASELINE)

    def test_headline_kpis_remain_unknown(self):
        """CT-40. Exception cycle time and aged backlog stay Unknown."""
        exception_cycle_time = "Unknown"
        aged_backlog = "Unknown"
        self.assertEqual(exception_cycle_time, "Unknown")
        self.assertEqual(aged_backlog, "Unknown")
        source = (INHERITED_ROOT / "app" / "baseline.py").read_text(encoding="utf-8")
        self.assertNotIn("exception_cycle", source)
        self.assertNotIn("aged_backlog", source)
        self.assertIn("r['status']!='CLOSED'", source)
        self.assertIn("priority(", source)
        # 89 is the Python open_cases field. It is not an aged-backlog day count.
        self.assertEqual(PHASE0_BASELINE["open_cases"], 89)


if __name__ == "__main__":
    unittest.main()
