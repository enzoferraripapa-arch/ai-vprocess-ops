#!/usr/bin/env python3
"""One-way handoff export for reviewed graph records.

The export package is intentionally not an ALM writer. It serializes accepted
decisions and accepted trace reviews so a human can import or re-enter them in a
formal system.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

TRACE_REVIEW_STATUSES = {"accepted", "rejected", "needs_review"}
EXPORTABLE_TRACE_EDGE_TYPES = {"impacts", "references_standard", "verified_by", "implements_candidate"}


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"missing graph DB: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def has_text(value: str | None) -> bool:
    return bool(value and value.strip())


def get_trace_edge(conn: sqlite3.Connection, source_id: str, target_id: str, edge_type: str) -> sqlite3.Row:
    row = conn.execute(
        """
        SELECT source_id, target_id, edge_type, rationale, confidence
        FROM edges
        WHERE source_id = ? AND target_id = ? AND edge_type = ?
        """,
        (source_id, target_id, edge_type),
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown trace edge: {source_id} --{edge_type}--> {target_id}")
    return row


def validate_trace_review_status(status: str) -> str:
    if status not in TRACE_REVIEW_STATUSES:
        allowed = ", ".join(sorted(TRACE_REVIEW_STATUSES))
        raise ValueError(f"trace review status must be one of: {allowed}")
    return status


def record_trace_review(
    conn: sqlite3.Connection,
    *,
    source_id: str,
    target_id: str,
    edge_type: str,
    status: str,
    reviewed_by: str | None = None,
    rationale: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    status = validate_trace_review_status(status)
    get_trace_edge(conn, source_id, target_id, edge_type)

    if status in {"accepted", "rejected"}:
        if edge_type not in EXPORTABLE_TRACE_EDGE_TYPES:
            allowed = ", ".join(sorted(EXPORTABLE_TRACE_EDGE_TYPES))
            raise ValueError(f"trace edge type must be exportable for final review: {allowed}")
        if not has_text(reviewed_by):
            raise ValueError(f"{status} trace reviews require --reviewed-by")
        if not has_text(rationale):
            raise ValueError(f"{status} trace reviews require --rationale")
        reviewed_at = reviewed_at or utc_now()
    else:
        reviewed_by = None
        reviewed_at = None

    conn.execute(
        """
        INSERT INTO trace_reviews(
            source_id, target_id, edge_type, status, reviewed_by, reviewed_at, rationale, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(source_id, target_id, edge_type) DO UPDATE SET
            status=excluded.status,
            reviewed_by=excluded.reviewed_by,
            reviewed_at=excluded.reviewed_at,
            rationale=excluded.rationale,
            updated_at=CURRENT_TIMESTAMP
        """,
        (source_id, target_id, edge_type, status, reviewed_by, reviewed_at, rationale),
    )
    return dict(
        conn.execute(
            """
            SELECT source_id, target_id, edge_type, status, reviewed_by, reviewed_at, rationale
            FROM trace_reviews
            WHERE source_id = ? AND target_id = ? AND edge_type = ?
            """,
            (source_id, target_id, edge_type),
        ).fetchone()
    )


def accepted_decisions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT id, question, selected_option, rationale, decided_by, decided_at
        FROM decisions
        WHERE status = 'accepted'
          AND decided_by IS NOT NULL
          AND decided_at IS NOT NULL
          AND length(trim(coalesce(selected_option, ''))) > 0
          AND length(trim(coalesce(rationale, ''))) > 0
          AND length(trim(coalesce(decided_by, ''))) > 0
          AND length(trim(coalesce(decided_at, ''))) > 0
        ORDER BY id
        """
    ).fetchall()
    return [dict(row) for row in rows]


def reviewed_trace_candidates(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT
            e.source_id,
            s.node_type AS source_type,
            s.title AS source_title,
            e.edge_type,
            e.target_id,
            t.node_type AS target_type,
            t.title AS target_title,
            e.rationale AS edge_rationale,
            tr.reviewed_by,
            tr.reviewed_at,
            tr.rationale AS review_rationale
        FROM trace_reviews tr
        JOIN edges e
          ON e.source_id = tr.source_id
         AND e.target_id = tr.target_id
         AND e.edge_type = tr.edge_type
        JOIN nodes s ON s.id = e.source_id
        JOIN nodes t ON t.id = e.target_id
        WHERE tr.status = 'accepted'
          AND tr.reviewed_by IS NOT NULL
          AND tr.reviewed_at IS NOT NULL
          AND length(trim(coalesce(tr.reviewed_by, ''))) > 0
          AND length(trim(coalesce(tr.reviewed_at, ''))) > 0
          AND length(trim(coalesce(tr.rationale, ''))) > 0
          AND e.edge_type IN (?, ?, ?, ?)
        ORDER BY e.edge_type, e.source_id, e.target_id
        """,
        tuple(sorted(EXPORTABLE_TRACE_EDGE_TYPES)),
    ).fetchall()
    return [dict(row) for row in rows]


def excluded_counts(conn: sqlite3.Connection) -> dict[str, int]:
    accepted_decision_ids = {
        row["id"]
        for row in conn.execute(
            """
            SELECT id
            FROM decisions
            WHERE status = 'accepted'
              AND decided_by IS NOT NULL
              AND decided_at IS NOT NULL
              AND length(trim(coalesce(selected_option, ''))) > 0
              AND length(trim(coalesce(rationale, ''))) > 0
              AND length(trim(coalesce(decided_by, ''))) > 0
              AND length(trim(coalesce(decided_at, ''))) > 0
            """
        )
    }
    accepted_trace_keys = {
        (row["source_id"], row["target_id"], row["edge_type"])
        for row in conn.execute(
            """
            SELECT source_id, target_id, edge_type
            FROM trace_reviews
            WHERE status = 'accepted'
              AND reviewed_by IS NOT NULL
              AND reviewed_at IS NOT NULL
              AND length(trim(coalesce(reviewed_by, ''))) > 0
              AND length(trim(coalesce(reviewed_at, ''))) > 0
              AND length(trim(coalesce(rationale, ''))) > 0
            """
        )
    }
    trace_edge_rows = conn.execute(
        """
        SELECT source_id, target_id, edge_type
        FROM edges
        WHERE edge_type IN (?, ?, ?, ?)
        """,
        tuple(sorted(EXPORTABLE_TRACE_EDGE_TYPES)),
    ).fetchall()
    decision_total = conn.execute("SELECT COUNT(*) AS count FROM decisions").fetchone()["count"]
    return {
        "non_accepted_decisions": decision_total - len(accepted_decision_ids),
        "non_accepted_trace_candidates": len(
            [
                row
                for row in trace_edge_rows
                if (row["source_id"], row["target_id"], row["edge_type"]) not in accepted_trace_keys
            ]
        ),
    }


def collect_handoff(conn: sqlite3.Connection) -> dict[str, Any]:
    return {
        "export_type": "ai_vprocess_alm_handoff",
        "boundary": (
            "One-way handoff package. This is not a formal ALM write, approval, "
            "baseline, signature, or compliance claim."
        ),
        "accepted_decisions": accepted_decisions(conn),
        "reviewed_trace_candidates": reviewed_trace_candidates(conn),
        "excluded_counts": excluded_counts(conn),
    }


def render_markdown(handoff: dict[str, Any]) -> str:
    lines = [
        "# ALM Handoff Export Package",
        "",
        "This package contains only graph records that have local human review metadata.",
        "It is a one-way handoff artifact, not a formal ALM write or approval.",
        "",
        "## Accepted Decisions",
        "",
    ]
    for decision in handoff["accepted_decisions"]:
        lines.extend(
            [
                f"- `{decision['id']}` {decision['question']}",
                f"  - Selected option: `{decision.get('selected_option') or 'undecided'}`",
                f"  - Rationale: {decision.get('rationale') or 'No rationale recorded.'}",
                f"  - Decided by: `{decision['decided_by']}`",
                f"  - Decided at: `{decision['decided_at']}`",
            ]
        )
    if not handoff["accepted_decisions"]:
        lines.append("- No accepted decisions with reviewer metadata.")

    lines.extend(["", "## Reviewed Trace Candidates", ""])
    for trace in handoff["reviewed_trace_candidates"]:
        lines.extend(
            [
                f"- `{trace['source_id']}` --`{trace['edge_type']}`--> `{trace['target_id']}`",
                f"  - Source: {trace['source_type']} / {trace['source_title']}",
                f"  - Target: {trace['target_type']} / {trace['target_title']}",
                f"  - Edge rationale: {trace.get('edge_rationale') or 'No edge rationale recorded.'}",
                f"  - Review rationale: {trace.get('review_rationale') or 'No review rationale recorded.'}",
                f"  - Reviewed by: `{trace['reviewed_by']}`",
                f"  - Reviewed at: `{trace['reviewed_at']}`",
            ]
        )
    if not handoff["reviewed_trace_candidates"]:
        lines.append("- No accepted trace reviews with reviewer metadata.")

    excluded = handoff["excluded_counts"]
    lines.extend(
        [
            "",
            "## Excluded From Export",
            "",
            f"- Non-accepted decisions: `{excluded['non_accepted_decisions']}`",
            f"- Non-accepted trace candidates: `{excluded['non_accepted_trace_candidates']}`",
            "",
            "## Boundary",
            "",
            "- This export is preparation for a human-controlled ALM/SOP handoff.",
            "- It does not write to Polarion, DOORS, Jama, Codebeamer, or another formal system.",
            "- It does not create approvals, signatures, baselines, or audit closure.",
            "- Formal ALM remains the authority for workflow state.",
        ]
    )
    return "\n".join(lines)


def write_output(path: Path | None, text: str) -> None:
    if path is None:
        print(text)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export reviewed graph records as a one-way ALM handoff package.")
    parser.add_argument("--db", required=True, type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    review_parser = subparsers.add_parser("trace-review", help="Record review state for a trace candidate edge.")
    review_parser.add_argument("--source", required=True)
    review_parser.add_argument("--target", required=True)
    review_parser.add_argument("--edge-type", required=True)
    review_parser.add_argument("--status", required=True, choices=sorted(TRACE_REVIEW_STATUSES))
    review_parser.add_argument("--reviewed-by")
    review_parser.add_argument("--rationale")
    review_parser.add_argument("--reviewed-at")

    export_parser = subparsers.add_parser("export", help="Export accepted records to JSON or Markdown.")
    export_parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    export_parser.add_argument("--output", type=Path)

    args = parser.parse_args()

    with connect(args.db) as conn:
        if args.command == "trace-review":
            with conn:
                review = record_trace_review(
                    conn,
                    source_id=args.source,
                    target_id=args.target,
                    edge_type=args.edge_type,
                    status=args.status,
                    reviewed_by=args.reviewed_by,
                    rationale=args.rationale,
                    reviewed_at=args.reviewed_at,
                )
            print(json.dumps(review, indent=2))
            return 0

        handoff = collect_handoff(conn)
        if args.format == "json":
            write_output(args.output, json.dumps(handoff, indent=2))
        else:
            write_output(args.output, render_markdown(handoff))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
