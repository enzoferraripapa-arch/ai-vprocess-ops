from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype"))


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vprocess_graph = load_module(ROOT / "prototype" / "vprocess_graph.py", "vprocess_graph_for_re_import_test")
llm_recommend = load_module(ROOT / "prototype" / "llm_recommend.py", "llm_recommend_for_re_import_test")
import_reverse_engineering = load_module(
    ROOT / "prototype" / "import_reverse_engineering.py",
    "import_reverse_engineering",
)


class ImportReverseEngineeringTests(unittest.TestCase):
    def build_empty_graph(self) -> sqlite3.Connection:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        conn = vprocess_graph.connect(Path(temp_dir.name) / "demo.db")
        self.addCleanup(conn.close)
        return conn

    def test_imports_authorized_reverse_engineering_records(self) -> None:
        conn = self.build_empty_graph()

        with conn:
            summary = import_reverse_engineering.load_reverse_engineering(
                conn,
                ROOT / "examples" / "sample_reverse_engineering_input.json",
            )

        self.assertEqual("RE-DEMO-001", summary["profile_id"])
        self.assertEqual(["ACT-IMPACT", "ACT-TRACE"], summary["recommended_activities"])

        requirement = conn.execute(
            "SELECT id, status FROM nodes WHERE id = 'RC-SAFE-STATE-TIMEOUT'"
        ).fetchone()
        source = conn.execute("SELECT source_path FROM nodes WHERE id = 'SRC-FW-TIMEOUT'").fetchone()
        blocking_edge = conn.execute(
            """
            SELECT 1
            FROM edges
            WHERE source_id = 'RC-SAFE-STATE-TIMEOUT'
              AND target_id = 'OI-TIMEOUT-OWNER'
              AND edge_type = 'blocked_by'
            """
        ).fetchone()
        activity_edge = conn.execute(
            """
            SELECT 1
            FROM edges
            WHERE source_id = 'RE-DEMO-001'
              AND target_id = 'ACT-IMPACT'
              AND edge_type = 'requires_activity'
            """
        ).fetchone()

        self.assertEqual("needs_review", requirement["status"])
        self.assertEqual("firmware/control/timeout_monitor.c", source["source_path"])
        self.assertIsNotNone(blocking_edge)
        self.assertIsNotNone(activity_edge)

        context = llm_recommend.collect_context(conn)
        edge_types = {edge["edge_type"] for edge in context["trace_edges"]}
        self.assertIn("observed_in", edge_types)
        self.assertIn("implements_candidate", edge_types)
        self.assertIn("verified_by", edge_types)

    def test_cli_import_outputs_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "reverse.db"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "prototype" / "import_reverse_engineering.py"),
                    "--db",
                    str(db_path),
                    "--input",
                    str(ROOT / "examples" / "sample_reverse_engineering_input.json"),
                    "--format",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        summary = json.loads(result.stdout)
        self.assertEqual("RE-DEMO-001", summary["profile_id"])
        self.assertEqual(7, summary["trace_candidate_edges"])


if __name__ == "__main__":
    unittest.main()
