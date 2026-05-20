#!/usr/bin/env python3
"""Import an authorized reverse-engineering sample into the graph DB."""

from __future__ import annotations

import argparse
import json
import sqlite3
from contextlib import closing
from pathlib import Path

import vprocess_graph

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "examples" / "sample_reverse_engineering_input.json"


def readable_body(record: dict) -> str | None:
    body = record.get("body") or record.get("summary")
    review_question = record.get("review_question")
    if body and review_question:
        return f"{body}\n\nReview question: {review_question}"
    return body or review_question


def upsert_record_node(conn: sqlite3.Connection, record: dict, default_status: str = "candidate") -> None:
    vprocess_graph.upsert_node(
        conn,
        record["id"],
        record["node_type"],
        record["title"],
        readable_body(record),
        record.get("status", default_status),
        record.get("confidence"),
    )
    if record.get("path"):
        conn.execute("UPDATE nodes SET source_path = ? WHERE id = ?", (record["path"], record["id"]))


def load_reverse_engineering(conn: sqlite3.Connection, input_path: Path = DEFAULT_INPUT) -> dict:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    profile = data["reverse_engineering_profile"]
    profile_id = profile["id"]

    vprocess_graph.upsert_node(
        conn,
        profile_id,
        "ReverseEngineeringProfile",
        profile["title"],
        json.dumps(profile, indent=2),
        profile.get("status", "candidate"),
        1.0,
    )

    node_groups = (
        data.get("sources", []),
        data.get("observed_behaviors", []),
        data.get("requirement_candidates", []),
        data.get("open_issues", []),
    )
    imported_node_count = 1
    for group in node_groups:
        for record in group:
            upsert_record_node(conn, record)
            vprocess_graph.upsert_edge(
                conn,
                profile_id,
                record["id"],
                "contains",
                "Reverse-engineering profile contains this candidate artifact.",
                record.get("confidence"),
            )
            imported_node_count += 1

    for edge in data.get("trace_candidates", []):
        vprocess_graph.upsert_edge(
            conn,
            edge["source_id"],
            edge["target_id"],
            edge["edge_type"],
            edge.get("rationale", ""),
            edge.get("confidence"),
        )

    for activity in data.get("recommended_activities", []):
        body = f"Trigger: {activity['trigger']}\n\nRationale: {activity['rationale']}"
        vprocess_graph.upsert_node(conn, activity["activity_id"], "Activity", activity["title"], body, "candidate", None)
        vprocess_graph.upsert_edge(
            conn,
            profile_id,
            activity["activity_id"],
            "requires_activity",
            activity["rationale"],
            None,
        )

    summary = {
        "profile_id": profile_id,
        "imported_nodes": imported_node_count + len(data.get("recommended_activities", [])),
        "trace_candidate_edges": len(data.get("trace_candidates", [])),
        "recommended_activities": [activity["activity_id"] for activity in data.get("recommended_activities", [])],
    }
    conn.execute(
        "INSERT INTO run_log(run_type, summary) VALUES (?, ?)",
        ("reverse_engineering_import", json.dumps(summary, sort_keys=True)),
    )
    return summary


def render_summary(summary: dict) -> str:
    lines = [
        "Imported authorized reverse-engineering sample",
        "----------------------------------------------",
        f"- Profile: {summary['profile_id']}",
        f"- Nodes imported: {summary['imported_nodes']}",
        f"- Trace candidate edges: {summary['trace_candidate_edges']}",
        f"- Recommended activities: {', '.join(summary['recommended_activities']) or 'none'}",
        "",
        "Boundary: observed behaviors, recovered requirements, and traces remain candidates until human review.",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import authorized reverse-engineering sample records into the graph.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    with closing(vprocess_graph.connect(args.db)) as conn:
        with conn:
            summary = load_reverse_engineering(conn, args.input)

    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(render_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
