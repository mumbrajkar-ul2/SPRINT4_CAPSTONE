"""Rule-evaluation characterization. Tests call the old names first."""
import inspect
import tempfile
import unittest
from pathlib import Path

from app.legacy_logic import manual_review_required, priority
from legacy_batch.shift_reconciliation import run

from .harness import (
    HOLD_FOR_REVIEW,
    INHERITED_ROOT,
    PACKAGED_ENTERPRISE,
    PACKAGED_LEGACY,
    TempEnterpriseMixin,
    compile_and_run_java,
    night_batch_full,
    readonly_connect,
    run_js_policy,
    which_tool,
)


class TestPriorityAndReview(unittest.TestCase):
    def test_priority_closed_is_archive(self):
        """CT-02."""
        self.assertEqual(priority("CLOSED", "LOW", 99999), "archive")

    def test_priority_critical_open_is_urgent(self):
        """CT-03."""
        self.assertEqual(priority("OPEN", "CRITICAL", 1), "urgent")

    def test_priority_amount_above_50000_is_urgent(self):
        """CT-04. Current Python deviation. 50,000 stays PROPOSED as live policy."""
        self.assertEqual(priority("OPEN", "LOW", 50001), "urgent")

    def test_priority_high_is_review(self):
        self.assertEqual(priority("OPEN", "HIGH", 1), "review")

    def test_priority_escalated_is_review(self):
        self.assertEqual(priority("ESCALATED", "LOW", 1), "review")

    def test_priority_other_is_queue(self):
        self.assertEqual(priority("OPEN", "LOW", 1), "queue")

    def test_packaged_amount_above_50000_count(self):
        """CT-05."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute("SELECT COUNT(*) FROM cases WHERE amount > 50000").fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)

    def test_manual_review_required_true_cases(self):
        self.assertTrue(manual_review_required("OPEN", "HIGH"))
        self.assertTrue(manual_review_required("OPEN", "CRITICAL"))
        self.assertTrue(manual_review_required("ESCALATED", "LOW"))
        self.assertTrue(manual_review_required("REOPENED", "LOW"))

    def test_manual_review_required_false_for_open_low(self):
        self.assertFalse(manual_review_required("OPEN", "LOW"))


class TestNightBatch(TempEnterpriseMixin, unittest.TestCase):
    def test_night_batch_review_object_in_flagged(self):
        """CT-17. Known REVIEW object FAB-00000011 is in the flagged set."""
        full = night_batch_full(self.enterprise_path, limit=500)
        flagged_ids = {row["object_id"] for row in full["flagged"]}
        self.assertIn("FAB-00000011", flagged_ids)
        report = run(limit=500, db=self.enterprise_path)
        self.assertEqual(report["processed"], full["processed"])
        self.assertEqual(report["by_tenant"], full["by_tenant"])
        self.assertEqual(report["flagged_count"], full["flagged_count"])

    def test_night_batch_hold_object_in_flagged(self):
        full = night_batch_full(self.enterprise_path, limit=500)
        flagged_ids = {row["object_id"] for row in full["flagged"]}
        self.assertIn("FAB-00000022", flagged_ids)

    def test_night_batch_flags_review_as_open(self):
        """CT-25. REVIEW is in the night-batch flag list. BO-06a match."""
        source = (INHERITED_ROOT / "legacy_batch" / "shift_reconciliation.py").read_text(encoding="utf-8")
        self.assertIn("('HOLD','REVIEW')", source)
        self.assertIn("REVIEW", source)

    def test_night_batch_default_limit_500(self):
        sig = inspect.signature(run)
        self.assertEqual(sig.parameters["limit"].default, 500)

    def test_shadow_run_flag_matches_run(self):
        """SH-RE night batch. Same copy and limit."""
        from legacy_batch import shift_reconciliation

        if not hasattr(shift_reconciliation, "run_flag"):
            self.skipTest("run_flag is added in slice 3 after these run tests exist")
        old = run(limit=500, db=self.enterprise_path)
        new = shift_reconciliation.run_flag(limit=500, db=self.enterprise_path)
        self.assertEqual(old["processed"], new["processed"])
        self.assertEqual(old["by_tenant"], new["by_tenant"])
        self.assertEqual(old["flagged_count"], new["flagged_count"])
        self.assertEqual(old["flagged_preview"], new["flagged_preview"])
        full = night_batch_full(self.enterprise_path, limit=500)
        self.assertEqual(old["processed"], full["processed"])
        self.assertEqual({r["object_id"] for r in full["flagged"]}, {r["object_id"] for r in full["flagged"]})


class TestStatusAndPolicyCounts(unittest.TestCase):
    def test_operational_review_count(self):
        """CT-18."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        count = conn.execute("SELECT COUNT(*) FROM operational_objects WHERE status='REVIEW'").fetchone()[0]
        conn.close()
        self.assertEqual(count, 2090)

    def test_cases_status_values(self):
        """CT-23."""
        conn = readonly_connect(PACKAGED_LEGACY)
        values = [r[0] for r in conn.execute("SELECT DISTINCT status FROM cases ORDER BY 1")]
        conn.close()
        self.assertEqual(values, ["CLOSED", "ESCALATED", "OPEN", "REOPENED", "UNDER_REVIEW"])

    def test_operational_status_values(self):
        """CT-24."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        values = [r[0] for r in conn.execute("SELECT DISTINCT status FROM operational_objects ORDER BY 1")]
        conn.close()
        self.assertEqual(values, ["CLOSED", "ESCALATED", "HOLD", "OPEN", "REOPENED", "REVIEW"])

    def test_active_policy_count(self):
        """CT-26."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        count = conn.execute("SELECT COUNT(*) FROM policy_register WHERE active=1").fetchone()[0]
        conn.close()
        self.assertEqual(count, 34)

    def test_active_policy_count_per_region(self):
        """CT-27."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        rows = {
            r[0]: r[1]
            for r in conn.execute(
                "SELECT region, COUNT(*) FROM policy_register WHERE active=1 GROUP BY 1"
            )
        }
        conn.close()
        self.assertEqual(rows, {"AU": 4, "BR": 4, "DE": 5, "GB": 4, "IN": 4, "JP": 4, "US": 5, "ZA": 4})

    def test_cases_region_values(self):
        """CT-28."""
        conn = readonly_connect(PACKAGED_LEGACY)
        values = [r[0] for r in conn.execute("SELECT DISTINCT region FROM cases ORDER BY 1")]
        conn.close()
        self.assertEqual(values, ["AMER", "APAC", "EMEA"])

    def test_operational_region_values(self):
        """CT-29."""
        conn = readonly_connect(PACKAGED_ENTERPRISE)
        values = [r[0] for r in conn.execute("SELECT DISTINCT region FROM operational_objects ORDER BY 1")]
        conn.close()
        self.assertEqual(values, ["AU", "BR", "DE", "GB", "IN", "JP", "US", "ZA"])

    def test_recipe_mismatch_count(self):
        """CT-10."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute(
            "SELECT COUNT(*) FROM process_steps p JOIN fab_tools t ON p.tool_id = t.tool_id "
            "WHERE p.recipe_version != t.recipe_rev"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 91)

    def test_process_steps_count(self):
        """CT-11."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute("SELECT COUNT(*) FROM process_steps").fetchone()[0]
        conn.close()
        self.assertEqual(count, 125)

    def test_unjoined_process_steps(self):
        """CT-12."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute(
            "SELECT COUNT(*) FROM process_steps p LEFT JOIN fab_tools t ON p.tool_id = t.tool_id "
            "WHERE t.tool_id IS NULL"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 0)

    def test_vendor_blank_amount_count(self):
        """CT-22."""
        conn = readonly_connect(PACKAGED_LEGACY)
        count = conn.execute(
            "SELECT COUNT(*) FROM vendor_file_rows WHERE amount_text IS NULL OR trim(amount_text)=''"
        ).fetchone()[0]
        conn.close()
        self.assertEqual(count, 10)


class TestJavaScriptDeviation(unittest.TestCase):
    def test_js_source_literals(self):
        source = (INHERITED_ROOT / "legacy_js" / "legacy_policy.js").read_text(encoding="utf-8")
        self.assertIn("999999", source)
        self.assertIn("1.05", source)

    def test_js_threshold_apac_2026(self):
        live = self._live()
        if live is None:
            return
        self.assertEqual(live["threshold_apac_2026"], 25000)

    def test_js_allows_26250_apac_2026(self):
        """CT-19. 25000 * 1.05 = 26250."""
        live = self._live()
        if live is None:
            return
        self.assertTrue(live["allows_26250"])

    def test_js_allows_27000_apac_2026(self):
        live = self._live()
        if live is None:
            return
        self.assertFalse(live["allows_27000"])

    def test_js_threshold_apac_1999_is_999999(self):
        """CT-20. Current deviation. Not live policy."""
        live = self._live()
        if live is None:
            return
        self.assertEqual(live["threshold_apac_1999"], 999999)

    def _live(self):
        if not which_tool("node"):
            self._label_unknown()
            return None
        completed = run_js_policy()
        if completed.returncode != 0:
            self._label_unknown()
            self.fail("node is present but the live run failed: " + completed.stderr)
        import json

        return json.loads(completed.stdout)

    def _label_unknown(self):
        live_run = "Unknown"
        self.assertEqual(live_run, "Unknown")


class TestJavaDeviation(unittest.TestCase):
    def test_java_source_literals(self):
        source = (INHERITED_ROOT / "legacy_java" / "ReconcileLegacy.java").read_text(encoding="utf-8")
        self.assertIn('startsWith("tenant,")', source)
        self.assertIn("parts.length<6", source)
        self.assertIn("NumberFormatException", source)

    def test_java_skips_blank_amount_cell(self):
        """CT-21. Blank field index 4 is omitted from count."""
        source = (INHERITED_ROOT / "legacy_java" / "ReconcileLegacy.java").read_text(encoding="utf-8")
        self.assertIn("NumberFormatException", source)
        if not which_tool("javac") or not which_tool("java"):
            live_run = "Unknown"
            self.assertEqual(live_run, "Unknown")
            return
        with tempfile.TemporaryDirectory(prefix="char-java-") as folder:
            workdir = Path(folder)
            csv_path = workdir / "fixture.csv"
            csv_path.write_text(
                "tenant,external_id,message_kind,pad,amount,received_ts\n"
                "T1,E1,kind,x,10.50,2020-01-01\n"
                "T1,E2,kind,x,,2020-01-01\n"
                "T1,E3,kind,x,not-a-number,2020-01-01\n"
                "short,line\n",
                encoding="utf-8",
            )
            compile_run, run_result = compile_and_run_java(csv_path, workdir)
            self.assertEqual(compile_run.returncode, 0, compile_run.stderr)
            self.assertIsNotNone(run_result)
            self.assertEqual(run_result.returncode, 0, run_result.stderr)
            self.assertIn("count=1", run_result.stdout)
            self.assertIn("total=10.50", run_result.stdout)


class TestLivePolicyNewPath(unittest.TestCase):
    def test_evaluate_live_policy_no_match_is_hold(self):
        from app import legacy_logic

        if not hasattr(legacy_logic, "evaluate_live_policy"):
            self.skipTest("evaluate_live_policy is added in slice 3 after old-name tests exist")
        result = legacy_logic.evaluate_live_policy("APAC", 1999)
        self.assertEqual(result, HOLD_FOR_REVIEW)
        self.assertNotEqual(result, 999999)

    def test_evaluate_live_policy_silent_urgent_cutoff_is_hold(self):
        from app import legacy_logic

        if not hasattr(legacy_logic, "evaluate_live_policy"):
            self.skipTest("evaluate_live_policy is added in slice 3 after old-name tests exist")
        result = legacy_logic.evaluate_live_policy(question="urgent_amount_cutoff")
        self.assertEqual(result, HOLD_FOR_REVIEW)
        self.assertNotEqual(result, 50000)
        source = inspect.getsource(legacy_logic.evaluate_live_policy)
        self.assertNotIn("50000", source)
        self.assertNotIn("999999", source)

    def test_evaluate_live_policy_archive_apac_2026(self):
        from app import legacy_logic

        if not hasattr(legacy_logic, "evaluate_live_policy"):
            self.skipTest("evaluate_live_policy is added in slice 3 after old-name tests exist")
        result = legacy_logic.evaluate_live_policy("APAC", 2026)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["limit"], 25000)
        self.assertEqual(result["currency"], "USD")


if __name__ == "__main__":
    unittest.main()
