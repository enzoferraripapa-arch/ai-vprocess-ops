from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "prototype" / "vprocess_graph.py"

spec = importlib.util.spec_from_file_location("vprocess_graph", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load module from {MODULE_PATH}")
vprocess_graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vprocess_graph)


class VProcessGraphTests(unittest.TestCase):
    def build_demo_graph(self) -> tuple[sqlite3.Connection, dict]:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        conn = vprocess_graph.connect(Path(temp_dir.name) / "demo.db")
        with conn:
            project_data = vprocess_graph.load_project(conn, ROOT / "examples" / "sample_project_input.json")
            vprocess_graph.load_trace_fixture(conn)
            vprocess_graph.load_decisions(conn)
            vprocess_graph.seed_activity_policies(conn)
        self.addCleanup(conn.close)
        return conn, project_data

    def test_recommends_expected_v_process_activities(self) -> None:
        conn, project_data = self.build_demo_graph()

        recommendations = vprocess_graph.recommend_activities(conn, project_data)
        activity_ids = {row["activity_id"] for row in recommendations}

        self.assertEqual({"ACT-IMPACT", "ACT-TRACE", "ACT-REGRESSION"}, activity_ids)

    def test_keeps_open_issue_and_blocking_trace(self) -> None:
        conn, _project_data = self.build_demo_graph()

        open_issue = conn.execute(
            "SELECT id, title FROM nodes WHERE node_type = 'OpenIssue' AND id = 'OI-001'"
        ).fetchone()
        blocking_edge = conn.execute(
            """
            SELECT 1
            FROM edges
            WHERE source_id = 'CR-001'
              AND target_id = 'OI-001'
              AND edge_type = 'blocked_by'
            """
        ).fetchone()

        self.assertIsNotNone(open_issue)
        self.assertIsNotNone(blocking_edge)


if __name__ == "__main__":
    unittest.main()
