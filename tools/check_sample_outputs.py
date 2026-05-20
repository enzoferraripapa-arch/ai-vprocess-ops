#!/usr/bin/env python3
"""Verify committed sample outputs match the executable demo."""

from __future__ import annotations

import difflib
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_command(args: list[str]) -> str:
    # The argv is built from fixed repo-local commands and shell=False is preserved.
    result = subprocess.run(  # nosec B603
        [sys.executable, *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"


def compare(name: str, expected_path: Path, actual: str) -> list[str]:
    expected = normalize(expected_path.read_text(encoding="utf-8"))
    actual = normalize(actual)
    if expected == actual:
        return []
    return list(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=expected_path.as_posix(),
            tofile=f"generated/{name}",
        )
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "vprocess_demo.db"
        report_path = Path(temp_dir) / "sample_review_report.md"

        run_command(
            [
                "prototype/vprocess_graph.py",
                "--db",
                str(db_path),
                "--input",
                "examples/sample_project_input.json",
            ]
        )
        impact_output = run_command(
            [
                "prototype/impact_query.py",
                "--db",
                str(db_path),
                "--start",
                "CR-001",
                "--max-depth",
                "2",
            ]
        )
        run_command(
            [
                "prototype/decision_lifecycle.py",
                "--db",
                str(db_path),
                "decide",
                "--id",
                "DEC-001",
                "--status",
                "accepted",
                "--selected-option",
                "bounded_delta_v_process",
                "--decided-by",
                "sample-reviewer",
                "--rationale",
                "Sample review accepted the bounded delta V-process path.",
                "--decided-at",
                "2026-01-02T03:04:05Z",
            ]
        )
        run_command(
            [
                "prototype/export_review_report.py",
                "--db",
                str(db_path),
                "--output",
                str(report_path),
            ]
        )
        handoff_output = run_command(
            [
                "prototype/alm_handoff_export.py",
                "--db",
                str(db_path),
                "trace-review",
                "--source",
                "CR-001",
                "--target",
                "REQ-001",
                "--edge-type",
                "impacts",
                "--status",
                "accepted",
                "--reviewed-by",
                "sample-reviewer",
                "--rationale",
                "Sample trace review accepted the impact link to REQ-001.",
                "--reviewed-at",
                "2026-01-02T03:04:05Z",
            ]
        )
        if "accepted" not in handoff_output:
            raise RuntimeError("trace review command did not record an accepted review")
        handoff_markdown = run_command(
            [
                "prototype/alm_handoff_export.py",
                "--db",
                str(db_path),
                "export",
                "--format",
                "markdown",
            ]
        )
        report_output = report_path.read_text(encoding="utf-8")
        regression_output = run_command(["benchmarks/run_sample_regression.py"])

    diffs: list[str] = []
    diffs.extend(compare("sample_impact_query.md", ROOT / "examples/outputs/sample_impact_query.md", impact_output))
    diffs.extend(compare("sample_review_report.md", ROOT / "examples/outputs/sample_review_report.md", report_output))
    diffs.extend(compare("sample_alm_handoff.md", ROOT / "examples/outputs/sample_alm_handoff.md", handoff_markdown))
    diffs.extend(compare("sample_result.md", ROOT / "benchmarks/sample_result.md", regression_output))

    if diffs:
        print("Sample output check failed. Regenerate or update the committed samples:")
        print("".join(diffs))
        return 1

    print("Sample output check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
