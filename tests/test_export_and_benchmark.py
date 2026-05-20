from __future__ import annotations

import importlib.util
import sqlite3
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


vprocess_graph = load_module(ROOT / "prototype" / "vprocess_graph.py", "vprocess_graph_for_export_test")
llm_recommend = load_module(ROOT / "prototype" / "llm_recommend.py", "llm_recommend_for_export_test")
export_review_report = load_module(ROOT / "prototype" / "export_review_report.py", "export_review_report")
run_sample_benchmark = load_module(ROOT / "benchmarks" / "run_sample_benchmark.py", "run_sample_benchmark")


class ExportAndBenchmarkTests(unittest.TestCase):
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

    def test_exports_markdown_report_with_boundary(self) -> None:
        conn = self.build_demo_graph()

        context = llm_recommend.collect_context(conn)
        report = export_review_report.render_report(context)

        self.assertIn("# V-Process Graph Review Report", report)
        self.assertIn("change_type=behavior-changing software update AND risk_level=high", report)
        self.assertIn("ACT-IMPACT", report)
        self.assertIn("Do not export candidate trace links as approved links", report)

    def test_sample_benchmark_passes_expected_scenario(self) -> None:
        result = run_sample_benchmark.run_benchmark()

        self.assertIn("Result: PASS", result)
        self.assertIn("ACT-IMPACT", result)
        self.assertIn("Export boundary present | `yes`", result)


if __name__ == "__main__":
    unittest.main()
