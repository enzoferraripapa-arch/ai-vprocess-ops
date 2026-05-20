from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_MODULE_PATH = ROOT / "prototype" / "vprocess_graph.py"
LLM_MODULE_PATH = ROOT / "prototype" / "llm_recommend.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vprocess_graph = load_module(GRAPH_MODULE_PATH, "vprocess_graph_for_llm_test")
llm_recommend = load_module(LLM_MODULE_PATH, "llm_recommend")


class LlmRecommendTests(unittest.TestCase):
    def build_demo_graph(self) -> sqlite3.Connection:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        conn = vprocess_graph.connect(Path(temp_dir.name) / "demo.db")
        with conn:
            project_data = vprocess_graph.load_project(conn, ROOT / "examples" / "sample_project_input.json")
            vprocess_graph.load_trace_fixture(conn)
            vprocess_graph.load_decisions(conn)
            vprocess_graph.seed_activity_policies(conn)
        self.addCleanup(conn.close)
        self.assertIsNotNone(project_data)
        return conn

    def test_builds_prompt_from_graph_context(self) -> None:
        conn = self.build_demo_graph()

        context = llm_recommend.collect_context(conn)
        prompt = llm_recommend.build_prompt(context)

        self.assertIn("ACT-IMPACT", prompt)
        self.assertIn("CR-001", prompt)
        self.assertIn("Do not claim automatic compliance", prompt)
        self.assertIn("Human decisions needed next", prompt)

    def test_reference_and_template_schemas_match(self) -> None:
        reference = (ROOT / "schema" / "001_core.sql").read_text(encoding="utf-8")
        template = (ROOT / "templates" / "empty_environment" / "schema" / "001_core.sql").read_text(encoding="utf-8")

        self.assertEqual(reference, template)


if __name__ == "__main__":
    unittest.main()
