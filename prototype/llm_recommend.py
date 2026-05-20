#!/usr/bin/env python3
"""Read the demo graph and ask an LLM for bounded V-process recommendations.

The default mode prints the exact prompt/context that would be sent to an LLM.
The optional Ollama mode calls a local Ollama server using only the Python
standard library.
"""

from __future__ import annotations

import argparse
import http.client
import json
import sqlite3
from pathlib import Path
from urllib.parse import urlparse

EDGE_TYPES_FOR_REVIEW = (
    "requires_activity",
    "references_standard",
    "impacts",
    "uses_sop",
    "blocked_by",
    "contains",
    "observed_in",
    "reads_config",
    "implements_candidate",
    "verified_by",
)
MAX_REVIEW_EDGE_TYPES = 12
MAX_EDGE_LIMIT = 200


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"missing graph DB: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def rows_as_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    return [dict(row) for row in rows]


def decode_json_object(text: str | None) -> dict:
    if not text:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def validate_edge_limit(edge_limit: int) -> int:
    if isinstance(edge_limit, bool):
        raise ValueError("edge_limit must be an integer")
    edge_limit = int(edge_limit)
    if edge_limit < 1:
        raise ValueError("edge_limit must be 1 or greater")
    if edge_limit > MAX_EDGE_LIMIT:
        raise ValueError(f"edge_limit must be {MAX_EDGE_LIMIT} or less")
    return edge_limit


def fetch_project_profiles(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        """
        SELECT id, node_type, title, body, status
        FROM nodes
        WHERE node_type IN ('ProjectProfile', 'ReverseEngineeringProfile')
        ORDER BY id
        """
    ).fetchall()
    profiles = []
    for row in rows:
        profile = decode_json_object(row["body"])
        profile["_node_id"] = row["id"]
        profile["_node_type"] = row["node_type"]
        profile["_title"] = row["title"]
        profile["_status"] = row["status"]
        profiles.append(profile)
    return profiles


def fetch_activity_matches(conn: sqlite3.Connection, profiles: list[dict]) -> list[dict]:
    matches: list[dict] = []
    seen: set[str] = set()
    rows = conn.execute(
        """
        SELECT
            p.id,
            p.activity_id,
            n.title AS activity_title,
            p.recommendation,
            p.rationale,
            p.severity
        FROM activity_policies p
        JOIN nodes n ON n.id = p.activity_id
        ORDER BY CASE p.severity WHEN 'high' THEN 0 ELSE 1 END, p.id
        """
    ).fetchall()
    for profile in profiles:
        for row in rows:
            conditions = [
                {"key": condition["condition_key"], "value": condition["condition_value"]}
                for condition in conn.execute(
                    """
                    SELECT condition_key, condition_value
                    FROM policy_conditions
                    WHERE policy_id = ?
                    ORDER BY condition_key, condition_value
                    """,
                    (row["id"],),
                )
            ]
            if not all(str(profile.get(condition["key"])) == condition["value"] for condition in conditions):
                continue
            if row["id"] in seen:
                continue
            seen.add(row["id"])
            result = dict(row)
            result["conditions"] = conditions
            result["conditions_summary"] = " AND ".join(
                f"{condition['key']}={condition['value']}" for condition in conditions
            )
            matches.append(result)
    return matches


def collect_context(conn: sqlite3.Connection, edge_limit: int = 40) -> dict:
    edge_limit = validate_edge_limit(edge_limit)
    padded_edge_types = (
        *EDGE_TYPES_FOR_REVIEW,
        *("__never_match_edge_type__" for _ in range(MAX_REVIEW_EDGE_TYPES - len(EDGE_TYPES_FOR_REVIEW))),
    )
    profiles = fetch_project_profiles(conn)
    trace_edges = rows_as_dicts(
        conn.execute(
            """
            SELECT
                e.source_id,
                s.node_type AS source_type,
                s.title AS source_title,
                e.edge_type,
                e.target_id,
                t.node_type AS target_type,
                t.title AS target_title,
                e.rationale,
                e.confidence
            FROM edges e
            JOIN nodes s ON s.id = e.source_id
            JOIN nodes t ON t.id = e.target_id
            WHERE e.edge_type IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ORDER BY e.edge_type, e.source_id, e.target_id
            LIMIT ?
            """,
            (*padded_edge_types, edge_limit),
        ).fetchall()
    )
    return {
        "project_profiles": profiles,
        "matched_activity_policies": fetch_activity_matches(conn, profiles),
        "open_issues": rows_as_dicts(
            conn.execute(
                """
                SELECT id, title, body, status, confidence
                FROM nodes
                WHERE node_type = 'OpenIssue'
                ORDER BY id
                """
            ).fetchall()
        ),
        "decisions": rows_as_dicts(
            conn.execute(
                """
                SELECT id, question, selected_option, rationale, status
                FROM decisions
                ORDER BY id
                """
            ).fetchall()
        ),
        "trace_edges": trace_edges,
    }


def build_prompt(context: dict) -> str:
    context_json = json.dumps(context, indent=2, ensure_ascii=False)
    instructions = """You are reviewing a small engineering-memory graph for AI-assisted V-process work.

Use only the graph context below. Treat requirements, traces, and decisions as candidates unless the graph says otherwise.

Return a concise Markdown review with these sections:

1. Recommended V-process activities
2. Evidence and trace links used
3. Open issues that block approval or ALM export
4. Human decisions needed next
5. What must not be claimed yet

Rules:

- Do not claim automatic compliance.
- Do not claim production readiness.
- Do not treat the LLM output as authority.
- Keep formal ALM approval, baselines, signatures, and audit state outside this graph.
- Mention uncertainty when the graph only provides candidates.

Graph context:

```json
"""
    return f"{instructions}{context_json}\n```"


def call_ollama(prompt: str, model: str, base_url: str, timeout: int) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Ollama URL must be an http(s) URL with a host")
    connection_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    path_prefix = parsed.path.rstrip("/")
    path = f"{path_prefix}/api/chat" if path_prefix else "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": "You are a careful engineering review assistant. Use only the provided graph context.",
            },
            {"role": "user", "content": prompt},
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    conn = connection_class(parsed.hostname, parsed.port, timeout=timeout)
    try:
        conn.request("POST", path, body=body, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        response_body = response.read().decode("utf-8", errors="replace")
    finally:
        conn.close()
    if response.status >= 400:
        raise RuntimeError(f"Ollama request failed: HTTP {response.status}: {response_body}")
    data = json.loads(response_body)
    message = data.get("message", {})
    content = message.get("content")
    if not isinstance(content, str):
        raise RuntimeError("Ollama response did not contain message.content")
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an LLM prompt from the V-process graph.")
    parser.add_argument("--db", required=True, type=Path, help="SQLite graph DB created by prototype/vprocess_graph.py.")
    parser.add_argument("--provider", choices=("prompt", "ollama"), default="prompt")
    parser.add_argument("--model", default="llama3.1", help="Ollama model name when --provider ollama is used.")
    parser.add_argument("--ollama-url", default="http://localhost:11434", help="Local Ollama base URL.")
    parser.add_argument("--timeout", type=int, default=60, help="LLM request timeout in seconds.")
    parser.add_argument("--edge-limit", type=int, default=40, help="Maximum trace edges to include in context.")
    args = parser.parse_args()

    with connect(args.db) as conn:
        context = collect_context(conn, edge_limit=args.edge_limit)
    prompt = build_prompt(context)

    if args.provider == "prompt":
        print(prompt)
        return 0

    print(call_ollama(prompt, args.model, args.ollama_url, args.timeout))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
