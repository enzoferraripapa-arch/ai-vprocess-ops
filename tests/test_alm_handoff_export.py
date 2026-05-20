from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype"))

import alm_handoff_export  # noqa: E402
import decision_lifecycle  # noqa: E402
import vprocess_graph  # noqa: E402


class AlmHandoffExportTests(unittest.TestCase):
    def build_demo_graph(self) -> sqlite3.Connection:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        conn = vprocess_graph.connect(Path(temp_dir.name) / "demo.db")
        with conn:
            vprocess_graph.load_project(conn, ROOT / "examples" / "sample_project_input.json")
            vprocess_graph.load_trace_fixture(conn)
            vprocess_graph.load_decisions(conn)
            vprocess_graph.seed_activity_policies(conn)
        self.addCleanup(conn.close)
        return conn

    def test_exports_only_accepted_decisions_and_accepted_trace_reviews(self) -> None:
        conn = self.build_demo_graph()

        with conn:
            decision_lifecycle.update_decision(
                conn,
                decision_id="DEC-001",
                status="accepted",
                selected_option="bounded_delta_v_process",
                decided_by="sample_reviewer",
                rationale="The delta path is accepted for this sample.",
                decided_at="2026-01-02T03:04:05Z",
            )
            alm_handoff_export.record_trace_review(
                conn,
                source_id="CR-001",
                target_id="REQ-001",
                edge_type="impacts",
                status="accepted",
                reviewed_by="sample_reviewer",
                rationale="The change impact on REQ-001 was reviewed.",
                reviewed_at="2026-01-02T03:04:05Z",
            )
            alm_handoff_export.record_trace_review(
                conn,
                source_id="CR-001",
                target_id="REQ-002",
                edge_type="impacts",
                status="rejected",
                reviewed_by="sample_reviewer",
                rationale="REQ-002 is not exported in this sample handoff.",
                reviewed_at="2026-01-02T03:04:05Z",
            )

        handoff = alm_handoff_export.collect_handoff(conn)
        exported_decision_ids = {decision["id"] for decision in handoff["accepted_decisions"]}
        exported_trace_keys = {
            (trace["source_id"], trace["target_id"], trace["edge_type"])
            for trace in handoff["reviewed_trace_candidates"]
        }
        markdown = alm_handoff_export.render_markdown(handoff)

        self.assertEqual({"DEC-001"}, exported_decision_ids)
        self.assertEqual({("CR-001", "REQ-001", "impacts")}, exported_trace_keys)
        self.assertIn("# ALM Handoff Export Package", markdown)
        self.assertIn("one-way handoff artifact", markdown)
        self.assertIn("Non-accepted decisions: `1`", markdown)
        self.assertIn("Non-accepted trace candidates: `5`", markdown)

    def test_final_trace_review_requires_reviewer_and_rationale(self) -> None:
        conn = self.build_demo_graph()

        with self.assertRaisesRegex(ValueError, "accepted trace reviews require --reviewed-by"):
            alm_handoff_export.record_trace_review(
                conn,
                source_id="CR-001",
                target_id="REQ-001",
                edge_type="impacts",
                status="accepted",
                rationale="Missing reviewer.",
                reviewed_at="2026-01-02T03:04:05Z",
            )

    def test_schema_rejects_malformed_final_trace_review(self) -> None:
        conn = self.build_demo_graph()

        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO trace_reviews(source_id, target_id, edge_type, status, reviewed_by, reviewed_at)
                VALUES('CR-001', 'REQ-001', 'impacts', 'accepted', 'sample_reviewer', '2026-01-02T03:04:05Z')
                """
            )

    def test_schema_rejects_malformed_accepted_decision(self) -> None:
        conn = self.build_demo_graph()

        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                """
                UPDATE decisions
                SET status = 'accepted',
                    selected_option = NULL,
                    rationale = 'Missing selected option.',
                    decided_by = 'sample_reviewer',
                    decided_at = '2026-01-02T03:04:05Z'
                WHERE id = 'DEC-001'
                """
            )

    def test_final_trace_review_rejects_non_trace_edge_types(self) -> None:
        conn = self.build_demo_graph()

        with self.assertRaisesRegex(ValueError, "trace edge type must be exportable"):
            alm_handoff_export.record_trace_review(
                conn,
                source_id="CR-001",
                target_id="ACT-IMPACT",
                edge_type="requires_activity",
                status="accepted",
                reviewed_by="sample_reviewer",
                rationale="Activities are not exported as trace links.",
                reviewed_at="2026-01-02T03:04:05Z",
            )

    def test_unknown_trace_edge_is_rejected(self) -> None:
        conn = self.build_demo_graph()

        with self.assertRaisesRegex(ValueError, "unknown trace edge"):
            alm_handoff_export.record_trace_review(
                conn,
                source_id="CR-001",
                target_id="REQ-404",
                edge_type="impacts",
                status="needs_review",
            )


if __name__ == "__main__":
    unittest.main()
