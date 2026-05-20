from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vprocess_graph = load_module(ROOT / "prototype" / "vprocess_graph.py", "vprocess_graph_for_impact_test")
impact_query = load_module(ROOT / "prototype" / "impact_query.py", "impact_query")


class ImpactQueryTests(unittest.TestCase):
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

    def test_recursive_impact_paths_reach_requirements_and_standards(self) -> None:
        conn = self.build_demo_graph()

        paths = impact_query.query_impact_paths(conn, "CR-001", max_depth=2)
        reached = {row["node_id"] for row in paths}

        self.assertIn("REQ-001", reached)
        self.assertIn("REQ-002", reached)
        self.assertIn("STD-SW-TRACE-01", reached)
        self.assertIn("OI-001", reached)

    def test_render_markdown_includes_boundary(self) -> None:
        conn = self.build_demo_graph()

        paths = impact_query.query_impact_paths(conn, "CR-001", max_depth=1)
        report = impact_query.render_markdown(paths, "CR-001")

        self.assertIn("# Impact Query", report)
        self.assertIn("recursive SQLite CTE", report)
        self.assertIn("Do not treat recursive reachability as compliance", report)


if __name__ == "__main__":
    unittest.main()
