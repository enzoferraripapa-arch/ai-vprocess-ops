#!/usr/bin/env python3
"""Record human review decisions in the local engineering-memory graph."""

from __future__ import annotations

import argparse
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

FINAL_STATUSES = {"accepted", "rejected"}
OPEN_STATUSES = {"draft", "needs_review"}
VALID_STATUSES = FINAL_STATUSES | OPEN_STATUSES


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


def get_decision(conn: sqlite3.Connection, decision_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown decision: {decision_id}")
    return row


def decision_option_keys(conn: sqlite3.Connection, decision_id: str) -> set[str]:
    rows = conn.execute(
        "SELECT option_key FROM decision_options WHERE decision_id = ? ORDER BY option_key",
        (decision_id,),
    ).fetchall()
    return {row["option_key"] for row in rows}


def validate_status(status: str) -> str:
    if status not in VALID_STATUSES:
        allowed = ", ".join(sorted(VALID_STATUSES))
        raise ValueError(f"status must be one of: {allowed}")
    return status


def validate_selected_option(conn: sqlite3.Connection, decision_id: str, selected_option: str | None) -> None:
    if selected_option is None:
        return
    known_options = decision_option_keys(conn, decision_id)
    if known_options and selected_option not in known_options:
        allowed = ", ".join(sorted(known_options))
        raise ValueError(f"selected_option for {decision_id} must be one of: {allowed}")


def update_decision(
    conn: sqlite3.Connection,
    *,
    decision_id: str,
    status: str,
    decided_by: str | None = None,
    selected_option: str | None = None,
    rationale: str | None = None,
    decided_at: str | None = None,
) -> dict[str, Any]:
    status = validate_status(status)
    current = get_decision(conn, decision_id)
    validate_selected_option(conn, decision_id, selected_option)

    if status == "accepted" and not has_text(selected_option):
        raise ValueError("accepted decisions require --selected-option")
    if status in FINAL_STATUSES:
        if not has_text(decided_by):
            raise ValueError(f"{status} decisions require --decided-by")
        if not has_text(rationale):
            raise ValueError(f"{status} decisions require --rationale")
        decided_at = decided_at or utc_now()
    else:
        decided_by = None
        decided_at = None
        if selected_option is None:
            selected_option = current["selected_option"]
        if rationale is None:
            rationale = current["rationale"]

    conn.execute(
        """
        UPDATE decisions
        SET
            selected_option = ?,
            rationale = ?,
            status = ?,
            decided_by = ?,
            decided_at = ?
        WHERE id = ?
        """,
        (
            selected_option,
            rationale,
            status,
            decided_by,
            decided_at,
            decision_id,
        ),
    )
    updated = get_decision(conn, decision_id)
    return dict(updated)


def list_decisions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT
            d.id,
            d.question,
            d.selected_option,
            d.rationale,
            d.status,
            d.decided_by,
            d.decided_at,
            COUNT(o.option_key) AS option_count
        FROM decisions d
        LEFT JOIN decision_options o ON o.decision_id = d.id
        GROUP BY d.id
        ORDER BY d.id
        """
    ).fetchall()
    return [dict(row) for row in rows]


def render_decisions(decisions: list[dict[str, Any]]) -> str:
    lines = ["Decision lifecycle", "------------------"]
    if not decisions:
        lines.append("- No decision records found.")
        return "\n".join(lines)
    for decision in decisions:
        lines.append(f"- {decision['id']} [{decision['status']}] {decision['question']}")
        lines.append(f"  selected_option: {decision.get('selected_option') or 'undecided'}")
        lines.append(f"  decided_by: {decision.get('decided_by') or 'unset'}")
        lines.append(f"  decided_at: {decision.get('decided_at') or 'unset'}")
        lines.append(f"  options: {decision.get('option_count', 0)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Record or list human decision lifecycle state.")
    parser.add_argument("--db", required=True, type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List decision records and current lifecycle state.")

    decide_parser = subparsers.add_parser("decide", help="Accept, reject, or reopen a decision.")
    decide_parser.add_argument("--id", required=True, help="Decision id, for example DEC-001.")
    decide_parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))
    decide_parser.add_argument("--selected-option")
    decide_parser.add_argument("--decided-by")
    decide_parser.add_argument("--rationale")
    decide_parser.add_argument("--decided-at", help="Deterministic ISO timestamp for tests or imports.")

    args = parser.parse_args()

    with connect(args.db) as conn:
        if args.command == "list":
            print(render_decisions(list_decisions(conn)))
            return 0

        with conn:
            updated = update_decision(
                conn,
                decision_id=args.id,
                status=args.status,
                decided_by=args.decided_by,
                selected_option=args.selected_option,
                rationale=args.rationale,
                decided_at=args.decided_at,
            )
        print(render_decisions([updated | {"option_count": len(decision_option_keys(conn, args.id))}]))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
