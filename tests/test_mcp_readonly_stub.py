from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
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


vprocess_graph = load_module(ROOT / "prototype" / "vprocess_graph.py", "vprocess_graph_for_mcp_test")
mcp_readonly_stub = load_module(ROOT / "prototype" / "mcp_readonly_stub.py", "mcp_readonly_stub")


class McpReadonlyStubTests(unittest.TestCase):
    def build_demo_db(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        db_path = Path(temp_dir.name) / "demo.db"
        conn = vprocess_graph.connect(db_path)
        with conn:
            vprocess_graph.load_project(conn, ROOT / "examples" / "sample_project_input.json")
            vprocess_graph.load_trace_fixture(conn)
            vprocess_graph.load_decisions(conn)
            vprocess_graph.seed_activity_policies(conn)
        conn.close()
        return db_path

    def test_tools_list_request(self) -> None:
        db_path = self.build_demo_db()

        response = mcp_readonly_stub.handle_request(db_path, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})

        self.assertEqual("2.0", response["jsonrpc"])
        tool_names = {tool["name"] for tool in response["result"]["tools"]}
        self.assertEqual({"graph_context", "impact_paths", "review_report"}, tool_names)

    def test_impact_paths_tool_call_is_read_only(self) -> None:
        db_path = self.build_demo_db()

        response = mcp_readonly_stub.handle_request(
            db_path,
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "impact_paths", "arguments": {"start": "CR-001", "max_depth": 2}},
            },
        )

        content = response["result"]["content"][0]["json"]
        reached = {row["node_id"] for row in content}
        self.assertIn("REQ-001", reached)
        self.assertIn("STD-SW-TRACE-01", reached)

        with closing(sqlite3.connect(db_path)) as conn:
            node_count = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        self.assertGreater(node_count, 0)

        with self.assertRaises(sqlite3.OperationalError), closing(mcp_readonly_stub.open_readonly(db_path)) as conn:
            conn.execute("INSERT INTO nodes(id, node_type, title) VALUES ('WRITE-FAIL', 'Test', 'should fail')")

    def test_graph_context_and_review_report_tools(self) -> None:
        db_path = self.build_demo_db()

        graph_context = mcp_readonly_stub.call_tool(db_path, "graph_context", {"edge_limit": 5})
        report = mcp_readonly_stub.call_tool(db_path, "review_report", {"edge_limit": 5})

        self.assertIn("matched_activity_policies", graph_context)
        self.assertIn("# V-Process Graph Review Report", report)

    def test_rejects_unbounded_arguments(self) -> None:
        db_path = self.build_demo_db()

        for arguments in ({"edge_limit": 0}, {"edge_limit": 999}):
            response = mcp_readonly_stub.handle_request(
                db_path,
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": "graph_context", "arguments": arguments},
                },
            )
            self.assertEqual(-32602, response["error"]["code"])

        response = mcp_readonly_stub.handle_request(
            db_path,
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "impact_paths", "arguments": {"start": "CR-001", "max_depth": 99}},
            },
        )
        self.assertEqual(-32602, response["error"]["code"])

    def test_cli_call_and_json_line_mode(self) -> None:
        db_path = self.build_demo_db()
        script = ROOT / "prototype" / "mcp_readonly_stub.py"

        call_result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--db",
                str(db_path),
                "--call",
                "impact_paths",
                "--arguments",
                '{"start":"CR-001","max_depth":2}',
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("STD-SW-TRACE-01", call_result.stdout)

        serve_result = subprocess.run(
            [sys.executable, str(script), "--db", str(db_path), "--serve"],
            input='{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"review_report","arguments":{}}}\n',
            check=True,
            capture_output=True,
            text=True,
        )
        response = json.loads(serve_result.stdout)
        content = response["result"]["content"][0]["json"]
        self.assertIn("# V-Process Graph Review Report", content)


if __name__ == "__main__":
    unittest.main()
