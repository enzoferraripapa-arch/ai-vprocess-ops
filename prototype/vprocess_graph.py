#!/usr/bin/env python3
"""Minimal AI-native V-process graph demo.

This prototype intentionally uses only Python's standard library. It creates a
SQLite graph from fictional JSON input and prints activity recommendations that
an LLM or engineer could use as bounded context.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "001_core.sql"
DEFAULT_TRACE = ROOT / "examples" / "sample_trace_graph.json"
DEFAULT_DECISIONS = ROOT / "examples" / "sample_v_process_decisions.json"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    return conn


def upsert_node(
    conn: sqlite3.Connection,
    node_id: str,
    node_type: str,
    title: str,
    body: str | None = None,
    status: str = "candidate",
    confidence: float | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO nodes(id, node_type, title, body, status, confidence, updated_at)
        VALUES(?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(id) DO UPDATE SET
            node_type=excluded.node_type,
            title=excluded.title,
            body=excluded.body,
            status=excluded.status,
            confidence=excluded.confidence,
            updated_at=CURRENT_TIMESTAMP
        """,
        (node_id, node_type, title, body, status, confidence),
    )


def upsert_edge(
    conn: sqlite3.Connection,
    source_id: str,
    target_id: str,
    edge_type: str,
    rationale: str,
    confidence: float | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO edges(source_id, target_id, edge_type, rationale, confidence)
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(source_id, target_id, edge_type) DO UPDATE SET
            rationale=excluded.rationale,
            confidence=excluded.confidence
        """,
        (source_id, target_id, edge_type, rationale, confidence),
    )


def load_project(conn: sqlite3.Connection, input_path: Path) -> dict:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    profile = data["project_profile"]
    upsert_node(
        conn,
        profile["id"],
        "ProjectProfile",
        profile["title"],
        json.dumps(profile, indent=2),
        "active",
        1.0,
    )

    for req in data.get("requirements", []):
        upsert_node(conn, req["id"], "Requirement", req["title"], req.get("body"), req.get("status", "candidate"), 0.8)
        upsert_edge(conn, profile["id"], req["id"], "contains", "Project profile contains this requirement candidate.", 0.8)

    change = data["change_request"]
    upsert_node(conn, change["id"], "ChangeRequest", change["title"], change.get("body"), change.get("status", "candidate"), 0.8)
    upsert_edge(conn, profile["id"], change["id"], "contains", "Project profile contains this change request.", 0.8)

    for std in data.get("standards", []):
        upsert_node(conn, std["id"], "StandardClause", std["title"], std.get("summary"), "reference", 1.0)
        for req in data.get("requirements", []):
            upsert_edge(conn, req["id"], std["id"], "references_standard", "Requirement should be checked against this summarized standard reference.", 0.6)

    for sop in data.get("sops", []):
        upsert_node(conn, sop["id"], "SOP", sop["title"], sop.get("summary"), "reference", 1.0)
        upsert_edge(conn, change["id"], sop["id"], "uses_sop", "Change handling should follow this operating procedure.", 0.7)

    return data


def load_trace_fixture(conn: sqlite3.Connection, trace_path: Path = DEFAULT_TRACE) -> None:
    data = json.loads(trace_path.read_text(encoding="utf-8"))
    for node in data.get("nodes", []):
        upsert_node(
            conn,
            node["id"],
            node["node_type"],
            node["title"],
            node.get("body"),
            node.get("status", "candidate"),
            node.get("confidence"),
        )
    for edge in data.get("edges", []):
        upsert_edge(
            conn,
            edge["source_id"],
            edge["target_id"],
            edge["edge_type"],
            edge.get("rationale", ""),
            edge.get("confidence"),
        )


def load_decisions(conn: sqlite3.Connection, decisions_path: Path = DEFAULT_DECISIONS) -> None:
    decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
    for decision in decisions:
        conn.execute(
            """
            INSERT INTO decisions(id, question, selected_option, rationale, status)
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                question=excluded.question,
                selected_option=excluded.selected_option,
                rationale=excluded.rationale,
                status=excluded.status
            """,
            (
                decision["id"],
                decision["question"],
                decision.get("selected_option"),
                decision.get("rationale"),
                decision.get("status", "draft"),
            ),
        )


def seed_activity_policies(conn: sqlite3.Connection) -> None:
    policies = [
        (
            "POL-HIGH-RISK-IMPACT",
            "ACT-IMPACT",
            "risk_level",
            "high",
            "Run change impact analysis before implementation.",
            "High-risk changes need affected requirements, tests, and controls identified.",
            "high",
        ),
        (
            "POL-BEHAVIOR-TRACE",
            "ACT-TRACE",
            "change_type",
            "behavior-changing software update",
            "Review trace candidates before ALM export.",
            "Behavior-changing software updates can invalidate existing requirement-test traces.",
            "high",
        ),
        (
            "POL-PARTIAL-REUSE-REGRESSION",
            "ACT-REGRESSION",
            "reuse_level",
            "partial",
            "Select regression tests for reused and modified behavior.",
            "Partial reuse requires confirmation that unchanged behavior remains covered.",
            "normal",
        ),
    ]
    conn.executemany(
        """
        INSERT INTO activity_policies(
            id, activity_id, trigger_key, trigger_value, recommendation, rationale, severity
        )
        VALUES(?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            activity_id=excluded.activity_id,
            trigger_key=excluded.trigger_key,
            trigger_value=excluded.trigger_value,
            recommendation=excluded.recommendation,
            rationale=excluded.rationale,
            severity=excluded.severity
        """,
        policies,
    )


def recommend_activities(conn: sqlite3.Connection, project_data: dict) -> list[sqlite3.Row]:
    profile = project_data["project_profile"]
    matches: list[sqlite3.Row] = []
    for key, value in profile.items():
        rows = conn.execute(
            """
            SELECT p.*, n.title AS activity_title
            FROM activity_policies p
            JOIN nodes n ON n.id = p.activity_id
            WHERE p.trigger_key = ? AND p.trigger_value = ?
            ORDER BY CASE p.severity WHEN 'high' THEN 0 ELSE 1 END, p.id
            """,
            (key, str(value)),
        ).fetchall()
        matches.extend(rows)
    return matches


def print_context(conn: sqlite3.Connection, recommendations: list[sqlite3.Row]) -> None:
    print("Recommended V-process activities")
    print("--------------------------------")
    for row in recommendations:
        print(f"- {row['activity_id']} {row['activity_title']} [{row['severity']}]")
        print(f"  trigger: {row['trigger_key']} = {row['trigger_value']}")
        print(f"  action: {row['recommendation']}")
        print(f"  rationale: {row['rationale']}")

    print()
    print("Open issues")
    print("-----------")
    for row in conn.execute("SELECT id, title FROM nodes WHERE node_type='OpenIssue' ORDER BY id"):
        print(f"- {row['id']} {row['title']}")

    print()
    print("Trace candidates")
    print("----------------")
    for row in conn.execute(
        """
        SELECT e.source_id, s.title AS source_title, e.edge_type, e.target_id, t.title AS target_title, e.rationale
        FROM edges e
        JOIN nodes s ON s.id = e.source_id
        JOIN nodes t ON t.id = e.target_id
        WHERE e.edge_type IN ('requires_activity', 'references_standard', 'uses_sop', 'blocked_by')
        ORDER BY e.edge_type, e.source_id, e.target_id
        """
    ):
        print(f"- {row['source_id']} --{row['edge_type']}--> {row['target_id']}")
        print(f"  {row['rationale']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and query a minimal V-process graph.")
    parser.add_argument("--db", required=True, type=Path, help="SQLite DB path to create or update.")
    parser.add_argument("--input", required=True, type=Path, help="Fictional project input JSON.")
    args = parser.parse_args()

    conn = connect(args.db)
    with conn:
        project_data = load_project(conn, args.input)
        load_trace_fixture(conn)
        load_decisions(conn)
        seed_activity_policies(conn)
    recommendations = recommend_activities(conn, project_data)
    print_context(conn, recommendations)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

