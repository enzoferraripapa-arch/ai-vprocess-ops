from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "001_core.sql"
DEFAULT_DB = ROOT / "runtime" / "engineering_memory.db"
DEFAULT_PROFILE = ROOT / "runtime" / "project_profile.local.json"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def apply_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def upsert_node(
    conn: sqlite3.Connection,
    node_id: str,
    node_type: str,
    title: str,
    body: str,
    status: str = "candidate",
    source_path: str | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO nodes (id, node_type, title, body, status, source_path)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            node_type=excluded.node_type,
            title=excluded.title,
            body=excluded.body,
            status=excluded.status,
            source_path=excluded.source_path,
            updated_at=CURRENT_TIMESTAMP
        """,
        (node_id, node_type, title, body, status, source_path),
    )


def write_profile(path: Path, project_name: str, target_project: str) -> None:
    profile = {
        "project_name": project_name,
        "target_project": str(Path(target_project)),
        "graph_db": str(DEFAULT_DB),
        "authority_model": {
            "llm": "decision_support_only",
            "graph_db": "engineering_memory",
            "formal_alm": "approval_authority",
            "execution_queue": "optional_task_tracker",
        },
        "required_outputs": [
            "artifact_inventory",
            "graph_importer",
            "trace_candidates",
            "v_process_recommendations",
            "human_review_report",
            "open_issue_list",
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")


def seed_empty_environment(
    conn: sqlite3.Connection,
    project_name: str,
    target_project: str,
) -> None:
    upsert_node(
        conn,
        "PROJECT-001",
        "project",
        project_name,
        "Target project registered for local engineering-memory pipeline setup.",
        "active",
        target_project,
    )
    upsert_node(
        conn,
        "OI-001",
        "open_issue",
        "Confirm target project boundary",
        (
            "Confirm which files, generated artifacts, external systems, and "
            "private inputs are in scope before import or analysis."
        ),
        "open",
        target_project,
    )
    upsert_node(
        conn,
        "ACT-001",
        "activity",
        "Build artifact inventory",
        (
            "Create a sanitized inventory of source files, documents, tests, "
            "logs, schemas, and configuration relevant to engineering memory."
        ),
        "candidate",
        target_project,
    )
    conn.execute(
        """
        INSERT OR IGNORE INTO edges
            (source_id, target_id, edge_type, rationale, confidence)
        VALUES
            ('OI-001', 'ACT-001', 'blocks',
             'Scope must be confirmed before importing project artifacts.', 1.0)
        """
    )
    conn.execute(
        """
        INSERT INTO run_log (run_type, summary)
        VALUES ('bootstrap', ?)
        """,
        (f"Initialized empty environment for {project_name}",),
    )


def check_environment(db_path: Path) -> int:
    if not db_path.exists():
        print(f"missing db: {db_path}")
        return 1
    with connect(db_path) as conn:
        result = conn.execute("PRAGMA integrity_check").fetchone()[0]
        nodes = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        edges = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    print(f"db: {db_path}")
    print(f"integrity_check: {result}")
    print(f"nodes: {nodes}")
    print(f"edges: {edges}")
    return 0 if result == "ok" else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--target-project")
    parser.add_argument("--project-name", default="target-project")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    db_path = Path(args.db)
    if args.check:
        return check_environment(db_path)

    if not args.target_project:
        parser.error("--target-project is required unless --check is used")

    with connect(db_path) as conn:
        apply_schema(conn)
        seed_empty_environment(conn, args.project_name, args.target_project)
        conn.commit()

    write_profile(DEFAULT_PROFILE, args.project_name, args.target_project)
    print(f"initialized db: {db_path}")
    print(f"wrote profile: {DEFAULT_PROFILE}")
    return check_environment(db_path)


if __name__ == "__main__":
    raise SystemExit(main())
