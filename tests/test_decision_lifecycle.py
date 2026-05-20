from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "prototype"
sys.path.insert(0, str(PROTOTYPE))

import decision_lifecycle  # noqa: E402
import export_review_report  # noqa: E402
import llm_recommend  # noqa: E402
import vprocess_graph  # noqa: E402


class DecisionLifecycleTests(unittest.TestCase):
    def build_demo_db(self) -> tuple[Path, object]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        db_path = Path(temp_dir.name) / "demo.db"
        conn = vprocess_graph.connect(db_path)
        with conn:
            vprocess_graph.load_project(conn, ROOT / "examples" / "sample_project_input.json")
            vprocess_graph.load_trace_fixture(conn)
            vprocess_graph.load_decisions(conn)
            vprocess_graph.seed_activity_policies(conn)
        self.addCleanup(conn.close)
        return db_path, conn

    def test_records_accepted_decision_and_preserves_it_after_seed_reload(self) -> None:
        _db_path, conn = self.build_demo_db()

        with conn:
            updated = decision_lifecycle.update_decision(
                conn,
                decision_id="DEC-001",
                status="accepted",
                selected_option="bounded_delta_v_process",
                decided_by="sample_reviewer",
                rationale="Impact analysis shows the change is bounded to existing behavior.",
                decided_at="2026-01-02T03:04:05Z",
            )

        self.assertEqual("accepted", updated["status"])
        self.assertEqual("sample_reviewer", updated["decided_by"])
        self.assertEqual("2026-01-02T03:04:05Z", updated["decided_at"])

        with conn:
            vprocess_graph.load_decisions(conn)
        reloaded = decision_lifecycle.get_decision(conn, "DEC-001")

        self.assertEqual("accepted", reloaded["status"])
        self.assertEqual("sample_reviewer", reloaded["decided_by"])
        self.assertEqual("2026-01-02T03:04:05Z", reloaded["decided_at"])

    def test_preserves_decision_options_after_final_review(self) -> None:
        _db_path, conn = self.build_demo_db()
        replacement_seed = [
            {
                "id": "DEC-001",
                "question": "Should this change run a full V-process or a bounded delta V-process?",
                "selected_option": "full_v_process",
                "rationale": "Replacement seed should not rewrite final review state.",
                "status": "draft",
                "options": [
                    {
                        "option_key": "full_v_process",
                        "description": "Replacement option set.",
                    }
                ],
            }
        ]
        with conn:
            decision_lifecycle.update_decision(
                conn,
                decision_id="DEC-001",
                status="accepted",
                selected_option="bounded_delta_v_process",
                decided_by="sample_reviewer",
                rationale="Impact analysis shows the change is bounded to existing behavior.",
                decided_at="2026-01-02T03:04:05Z",
            )

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        seed_path = Path(temp_dir.name) / "decisions.json"
        seed_path.write_text(json.dumps(replacement_seed), encoding="utf-8", newline="\n")
        with conn:
            vprocess_graph.load_decisions(conn, seed_path)

        option_keys = decision_lifecycle.decision_option_keys(conn, "DEC-001")
        reloaded = decision_lifecycle.get_decision(conn, "DEC-001")

        self.assertEqual("accepted", reloaded["status"])
        self.assertEqual("bounded_delta_v_process", reloaded["selected_option"])
        self.assertIn("bounded_delta_v_process", option_keys)

    def test_rejects_final_seed_decision_without_review_metadata(self) -> None:
        _db_path, conn = self.build_demo_db()
        bad_seed = [
            {
                "id": "DEC-SEED-FINAL",
                "question": "Should this invalid seed be accepted?",
                "selected_option": "yes",
                "rationale": "Missing reviewer metadata.",
                "status": "accepted",
            }
        ]
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        seed_path = Path(temp_dir.name) / "bad_decisions.json"
        seed_path.write_text(json.dumps(bad_seed), encoding="utf-8", newline="\n")

        with self.assertRaisesRegex(ValueError, "requires decided_by and decided_at"):
            vprocess_graph.load_decisions(conn, seed_path)

    def test_rejects_unknown_option_when_decision_options_are_defined(self) -> None:
        _db_path, conn = self.build_demo_db()

        with self.assertRaisesRegex(ValueError, "selected_option for DEC-001"):
            decision_lifecycle.update_decision(
                conn,
                decision_id="DEC-001",
                status="accepted",
                selected_option="undefined_option",
                decided_by="sample_reviewer",
                rationale="This should fail before updating the decision.",
                decided_at="2026-01-02T03:04:05Z",
            )

    def test_review_metadata_reaches_llm_context_and_report(self) -> None:
        db_path, conn = self.build_demo_db()

        with conn:
            decision_lifecycle.update_decision(
                conn,
                decision_id="DEC-002",
                status="accepted",
                selected_option="export_after_review",
                decided_by="sample_reviewer",
                rationale="Trace candidates should be reviewed before formal ALM export.",
                decided_at="2026-01-02T03:04:05Z",
            )

        with closing(llm_recommend.connect(db_path)) as llm_conn:
            context = llm_recommend.collect_context(llm_conn)
        decision = next(item for item in context["decisions"] if item["id"] == "DEC-002")
        report = export_review_report.render_report(context)

        self.assertEqual("sample_reviewer", decision["decided_by"])
        self.assertEqual("2026-01-02T03:04:05Z", decision["decided_at"])
        self.assertIn("Decided by: `sample_reviewer`", report)
        self.assertIn("Decided at: `2026-01-02T03:04:05Z`", report)


if __name__ == "__main__":
    unittest.main()
