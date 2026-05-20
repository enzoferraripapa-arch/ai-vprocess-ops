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

import policy_match

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "001_core.sql"
DEFAULT_TRACE = ROOT / "examples" / "sample_trace_graph.json"
DEFAULT_DECISIONS = ROOT / "examples" / "sample_v_process_decisions.json"
FINAL_DECISION_STATUSES = {"accepted", "rejected"}


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
        status = decision.get("status", "draft")
        decided_by = decision.get("decided_by")
        decided_at = decision.get("decided_at")
        if status in FINAL_DECISION_STATUSES and (not decided_by or not decided_at):
            raise ValueError(f"final decision {decision['id']} requires decided_by and decided_at")
        current = conn.execute(
            "SELECT status FROM decisions WHERE id = ?",
            (decision["id"],),
        ).fetchone()
        preserve_final = current is not None and current["status"] in FINAL_DECISION_STATUSES
        conn.execute(
            """
            INSERT INTO decisions(id, question, selected_option, rationale, status, decided_by, decided_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                question=excluded.question,
                selected_option=CASE
                    WHEN decisions.status IN ('accepted', 'rejected') THEN decisions.selected_option
                    ELSE excluded.selected_option
                END,
                rationale=CASE
                    WHEN decisions.status IN ('accepted', 'rejected') THEN decisions.rationale
                    ELSE excluded.rationale
                END,
                status=CASE
                    WHEN decisions.status IN ('accepted', 'rejected') THEN decisions.status
                    ELSE excluded.status
                END,
                decided_by=CASE
                    WHEN decisions.status IN ('accepted', 'rejected') THEN decisions.decided_by
                    ELSE excluded.decided_by
                END,
                decided_at=CASE
                    WHEN decisions.status IN ('accepted', 'rejected') THEN decisions.decided_at
                    ELSE excluded.decided_at
                END
            """,
            (
                decision["id"],
                decision["question"],
                decision.get("selected_option"),
                decision.get("rationale"),
                status,
                decided_by,
                decided_at,
            ),
        )
        if not preserve_final:
            conn.execute("DELETE FROM decision_options WHERE decision_id = ?", (decision["id"],))
            conn.executemany(
                """
                INSERT INTO decision_options(decision_id, option_key, description, pros, cons)
                VALUES(?, ?, ?, ?, ?)
                """,
                [
                    (
                        decision["id"],
                        option["option_key"],
                        option["description"],
                        option.get("pros"),
                        option.get("cons"),
                    )
                    for option in decision.get("options", [])
                ],
            )


def upsert_activity_policy(
    conn: sqlite3.Connection,
    policy_id: str,
    activity_id: str,
    conditions: list[tuple[str, str]],
    recommendation: str,
    rationale: str,
    severity: str = "normal",
) -> None:
    if not conditions:
        raise ValueError("activity policy must have at least one condition")
    trigger_key, trigger_value = conditions[0]
    conn.execute(
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
        (policy_id, activity_id, trigger_key, trigger_value, recommendation, rationale, severity),
    )
    conn.execute("DELETE FROM policy_conditions WHERE policy_id = ?", (policy_id,))
    conn.executemany(
        """
        INSERT INTO policy_conditions(policy_id, condition_key, condition_value)
        VALUES(?, ?, ?)
        """,
        [(policy_id, key, value) for key, value in conditions],
    )


def seed_activity_policies(conn: sqlite3.Connection) -> None:
    policies = [
        (
            "POL-HIGH-RISK-IMPACT",
            "ACT-IMPACT",
            [("risk_level", "high")],
            "Run change impact analysis before implementation.",
            "High-risk changes need affected requirements, tests, and controls identified.",
            "high",
        ),
        (
            "POL-BEHAVIOR-TRACE",
            "ACT-TRACE",
            [("change_type", "behavior-changing software update")],
            "Review trace candidates before ALM export.",
            "Behavior-changing software updates can invalidate existing requirement-test traces.",
            "high",
        ),
        (
            "POL-PARTIAL-REUSE-REGRESSION",
            "ACT-REGRESSION",
            [("reuse_level", "partial")],
            "Select regression tests for reused and modified behavior.",
            "Partial reuse requires confirmation that unchanged behavior remains covered.",
            "normal",
        ),
        (
            "POL-HIGH-BEHAVIOR-GATE",
            "ACT-GATE",
            [("risk_level", "high"), ("change_type", "behavior-changing software update")],
            "Prepare approval gate review before formal ALM export.",
            "High-risk behavior changes need explicit gate evidence before candidate traces are promoted.",
            "high",
        ),
    ]
    for policy_id, activity_id, conditions, recommendation, rationale, severity in policies:
        upsert_activity_policy(conn, policy_id, activity_id, conditions, recommendation, rationale, severity)


def recommend_activities(conn: sqlite3.Connection, project_data: dict) -> list[dict]:
    profile = project_data["project_profile"]
    return policy_match.matching_activity_policies(conn, profile)


def print_context(conn: sqlite3.Connection, recommendations: list[dict]) -> None:
    print("Recommended V-process activities")
    print("--------------------------------")
    for row in recommendations:
        print(f"- {row['activity_id']} {row['activity_title']} [{row['severity']}]")
        print(f"  conditions: {row['conditions_summary']}")
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
