#!/usr/bin/env python3
"""Run the fictional sample benchmark against the deterministic graph outputs."""

from __future__ import annotations

import argparse
import importlib.util
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ACTIVITIES = {"ACT-GATE", "ACT-IMPACT", "ACT-TRACE", "ACT-REGRESSION"}
REQUIRED_OPEN_ISSUES = {"OI-001"}

sys.path.insert(0, str(ROOT / "prototype"))


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vprocess_graph = load_module(ROOT / "prototype" / "vprocess_graph.py", "benchmark_vprocess_graph")
llm_recommend = load_module(ROOT / "prototype" / "llm_recommend.py", "benchmark_llm_recommend")
impact_query = load_module(ROOT / "prototype" / "impact_query.py", "benchmark_impact_query")
export_review_report = load_module(
    ROOT / "prototype" / "export_review_report.py",
    "benchmark_export_review_report",
)


def build_graph(db_path: Path) -> sqlite3.Connection:
    conn = vprocess_graph.connect(db_path)
    with conn:
        project_data = vprocess_graph.load_project(conn, ROOT / "examples" / "sample_project_input.json")
        vprocess_graph.load_trace_fixture(conn)
        vprocess_graph.load_decisions(conn)
        vprocess_graph.seed_activity_policies(conn)
    if not project_data:
        raise RuntimeError("sample project input did not load")
    return conn


def evaluate_context(context: dict) -> dict:
    actual_activities = {policy["activity_id"] for policy in context["matched_activity_policies"]}
    actual_open_issues = {issue["id"] for issue in context["open_issues"]}
    return {
        "expected_activities": sorted(EXPECTED_ACTIVITIES),
        "actual_activities": sorted(actual_activities),
        "missing_activities": sorted(EXPECTED_ACTIVITIES - actual_activities),
        "extra_activities": sorted(actual_activities - EXPECTED_ACTIVITIES),
        "required_open_issues": sorted(REQUIRED_OPEN_ISSUES),
        "actual_open_issues": sorted(actual_open_issues),
        "missing_open_issues": sorted(REQUIRED_OPEN_ISSUES - actual_open_issues),
        "trace_edge_count": len(context["trace_edges"]),
    }


def render_result(metrics: dict, report: str, impact_paths: list[dict]) -> str:
    passed = not metrics["missing_activities"] and not metrics["missing_open_issues"]
    boundary_present = "Do not claim automatic compliance" in report and "Do not export candidate trace links" in report
    impacted_nodes = {row["node_id"] for row in impact_paths}
    impact_path_present = {"REQ-001", "REQ-002", "STD-SW-TRACE-01"}.issubset(impacted_nodes)
    passed = passed and boundary_present and impact_path_present
    lines = [
        "# Sample Benchmark Result",
        "",
        "Scenario: fictional behavior-changing timeout update in a high-risk embedded controller.",
        "",
        f"Result: {'PASS' if passed else 'FAIL'}",
        "",
        "| Check | Value |",
        "| --- | --- |",
        f"| Expected mandatory activities | `{', '.join(metrics['expected_activities'])}` |",
        f"| Actual activities | `{', '.join(metrics['actual_activities'])}` |",
        f"| Missing activities | `{', '.join(metrics['missing_activities']) or 'none'}` |",
        f"| Extra activities | `{', '.join(metrics['extra_activities']) or 'none'}` |",
        f"| Required open issues | `{', '.join(metrics['required_open_issues'])}` |",
        f"| Missing open issues | `{', '.join(metrics['missing_open_issues']) or 'none'}` |",
        f"| Trace edges in report context | `{metrics['trace_edge_count']}` |",
        f"| Recursive impact path reaches requirements/standards | `{'yes' if impact_path_present else 'no'}` |",
        f"| Export boundary present | `{'yes' if boundary_present else 'no'}` |",
        "",
        "Interpretation: this benchmark only checks the deterministic sample output. It does not prove compliance,",
        "production readiness, or general performance on real projects.",
        "",
    ]
    return "\n".join(lines)


def run_benchmark() -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "benchmark.db"
        conn = build_graph(db_path)
        try:
            context = llm_recommend.collect_context(conn)
            report = export_review_report.render_report(context)
            metrics = evaluate_context(context)
            impact_paths = impact_query.query_impact_paths(conn, "CR-001", max_depth=2)
        finally:
            conn.close()
    return render_result(metrics, report, impact_paths)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the sample ai-vprocess-ops benchmark.")
    parser.add_argument("--output", type=Path, help="Write benchmark result Markdown to this file.")
    args = parser.parse_args()

    result = run_benchmark()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
