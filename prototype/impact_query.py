#!/usr/bin/env python3
"""Query impact paths from the SQLite engineering-memory graph."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

DEFAULT_EDGE_TYPES = (
    "blocked_by",
    "impacts",
    "references_standard",
    "requires_activity",
    "uses_sop",
)
MAX_DEPTH = 8
MAX_EDGE_FILTERS = 12


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"missing graph DB: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query_impact_paths(
    conn: sqlite3.Connection,
    start_id: str,
    max_depth: int = 3,
    edge_types: tuple[str, ...] = DEFAULT_EDGE_TYPES,
) -> list[dict]:
    if max_depth < 0:
        raise ValueError("max_depth must be 0 or greater")
    if max_depth > MAX_DEPTH:
        raise ValueError(f"max_depth must be {MAX_DEPTH} or less")
    if not edge_types:
        raise ValueError("edge_types must include at least one edge type")
    if len(edge_types) > MAX_EDGE_FILTERS:
        raise ValueError(f"edge_types must include {MAX_EDGE_FILTERS} or fewer edge types")
    padded_edge_types = (*edge_types, *("__never_match_edge_type__" for _ in range(MAX_EDGE_FILTERS - len(edge_types))))
    rows = conn.execute(
        """
        WITH RECURSIVE impact(
            depth,
            node_id,
            node_type,
            title,
            path_ids,
            display_path,
            edge_path,
            from_node_id,
            via_edge_type,
            via_rationale
        ) AS (
            SELECT
                0,
                n.id,
                n.node_type,
                n.title,
                '|' || n.id || '|',
                n.id,
                '',
                NULL,
                NULL,
                NULL
            FROM nodes n
            WHERE n.id = ?

            UNION ALL

            SELECT
                impact.depth + 1,
                target.id,
                target.node_type,
                target.title,
                impact.path_ids || target.id || '|',
                impact.display_path || ' -> ' || target.id,
                CASE
                    WHEN impact.edge_path = '' THEN edge.edge_type
                    ELSE impact.edge_path || ' -> ' || edge.edge_type
                END,
                edge.source_id,
                edge.edge_type,
                edge.rationale
            FROM impact
            JOIN edges edge ON edge.source_id = impact.node_id
            JOIN nodes target ON target.id = edge.target_id
            WHERE impact.depth < ?
              AND instr(impact.path_ids, '|' || target.id || '|') = 0
              AND edge.edge_type IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        )
        SELECT
            depth,
            node_id,
            node_type,
            title,
            display_path,
            edge_path,
            from_node_id,
            via_edge_type,
            via_rationale
        FROM impact
        ORDER BY depth, display_path
        """,
        (start_id, max_depth, *padded_edge_types),
    ).fetchall()
    return [dict(row) for row in rows]


def render_markdown(paths: list[dict], start_id: str) -> str:
    lines = [
        "# Impact Query",
        "",
        f"Start node: `{start_id}`",
        "",
        "This is a recursive SQLite CTE over the local `nodes` and `edges` tables. It is impact discovery, not approval.",
        "",
        "## Reachable Paths",
        "",
    ]
    if not paths:
        lines.append("- No reachable paths found.")
        return "\n".join(lines)

    for row in paths:
        lines.append(f"- depth {row['depth']}: `{row['node_id']}` ({row['node_type']}) {row['title']}")
        lines.append(f"  - Path: `{row['display_path']}`")
        if row["via_edge_type"]:
            lines.append(f"  - Via: `{row['from_node_id']}` --`{row['via_edge_type']}`--> `{row['node_id']}`")
        if row["via_rationale"]:
            lines.append(f"  - Rationale: {row['via_rationale']}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- These paths identify candidate impact and review scope.",
            "- A human reviewer must decide which paths become formal ALM trace links.",
            "- Do not treat recursive reachability as compliance, approval, or baseline status.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_edge_types(value: str | None) -> tuple[str, ...]:
    if not value:
        return DEFAULT_EDGE_TYPES
    edge_types = tuple(part.strip() for part in value.split(",") if part.strip())
    if not edge_types:
        raise ValueError("--edge-types must include at least one edge type")
    return edge_types


def main() -> int:
    parser = argparse.ArgumentParser(description="Query recursive impact paths from the V-process graph.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--start", required=True, help="Start node ID, such as CR-001.")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--edge-types", help="Comma-separated edge types. Defaults to review-relevant impact edges.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    edge_types = parse_edge_types(args.edge_types)
    with connect(args.db) as conn:
        paths = query_impact_paths(conn, args.start, max_depth=args.max_depth, edge_types=edge_types)

    if args.format == "json":
        print(json.dumps(paths, indent=2))
    else:
        print(render_markdown(paths, args.start))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
