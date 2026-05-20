#!/usr/bin/env python3
"""Read-only JSON-RPC-style stub for the demo graph.

This is intentionally a small local prototype, not a complete MCP server. It
exposes read-only graph context, impact paths, and review-report generation
through `tools/list` and `tools/call` style JSON-RPC messages.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
from typing import Any

import export_review_report
import impact_query
import llm_recommend

MAX_MCP_EDGE_LIMIT = 80
MAX_MCP_DEPTH = 4

TOOLS = [
    {
        "name": "graph_context",
        "description": "Return bounded graph context for LLM review.",
        "inputSchema": {
            "type": "object",
            "properties": {"edge_limit": {"type": "integer", "default": 40, "minimum": 1, "maximum": 80}},
            "additionalProperties": False,
        },
    },
    {
        "name": "impact_paths",
        "description": "Return recursive impact paths from a start node.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start": {"type": "string"},
                "max_depth": {"type": "integer", "default": 3, "minimum": 0, "maximum": 4},
                "format": {"type": "string", "enum": ["json", "markdown"], "default": "json"},
            },
            "required": ["start"],
            "additionalProperties": False,
        },
    },
    {
        "name": "review_report",
        "description": "Return a deterministic Markdown review report from the graph.",
        "inputSchema": {
            "type": "object",
            "properties": {"edge_limit": {"type": "integer", "default": 40, "minimum": 1, "maximum": 80}},
            "additionalProperties": False,
        },
    },
]


def jsonrpc_result(request_id: Any, result: Any) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def jsonrpc_error(request_id: Any, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def as_int(value: Any, default: int, *, name: str, minimum: int, maximum: int) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    result = int(value)
    if result < minimum:
        raise ValueError(f"{name} must be {minimum} or greater")
    if result > maximum:
        raise ValueError(f"{name} must be {maximum} or less")
    return result


def open_readonly(db_path: Path):
    if not db_path.exists():
        raise FileNotFoundError(f"missing graph DB: {db_path}")
    uri = db_path.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA query_only = ON")
    return conn


def call_tool(db_path: Path, name: str, arguments: dict[str, Any] | None = None) -> Any:
    arguments = arguments or {}
    if name == "graph_context":
        edge_limit = as_int(
            arguments.get("edge_limit"), 40, name="edge_limit", minimum=1, maximum=MAX_MCP_EDGE_LIMIT
        )
        with closing(open_readonly(db_path)) as conn:
            return llm_recommend.collect_context(conn, edge_limit=edge_limit)

    if name == "impact_paths":
        start = arguments.get("start")
        if not isinstance(start, str) or not start:
            raise ValueError("impact_paths requires non-empty string argument: start")
        max_depth = as_int(arguments.get("max_depth"), 3, name="max_depth", minimum=0, maximum=MAX_MCP_DEPTH)
        output_format = arguments.get("format", "json")
        if output_format not in {"json", "markdown"}:
            raise ValueError("impact_paths format must be 'json' or 'markdown'")
        with closing(open_readonly(db_path)) as conn:
            paths = impact_query.query_impact_paths(conn, start, max_depth=max_depth)
        if output_format == "markdown":
            return impact_query.render_markdown(paths, start)
        return paths

    if name == "review_report":
        edge_limit = as_int(
            arguments.get("edge_limit"), 40, name="edge_limit", minimum=1, maximum=MAX_MCP_EDGE_LIMIT
        )
        with closing(open_readonly(db_path)) as conn:
            context = llm_recommend.collect_context(conn, edge_limit=edge_limit)
        return export_review_report.render_report(context)

    raise ValueError(f"unknown tool: {name}")


def handle_request(db_path: Path, request: dict[str, Any]) -> dict:
    request_id = request.get("id")
    method = request.get("method")
    try:
        if method == "tools/list":
            return jsonrpc_result(request_id, {"tools": TOOLS})
        if method == "tools/call":
            params = request.get("params") or {}
            if not isinstance(params, dict):
                raise ValueError("tools/call params must be an object")
            name = params.get("name")
            if not isinstance(name, str):
                raise ValueError("tools/call params.name must be a string")
            arguments = params.get("arguments") or {}
            if not isinstance(arguments, dict):
                raise ValueError("tools/call params.arguments must be an object")
            return jsonrpc_result(
                request_id,
                {"content": [{"type": "text", "text": json.dumps(call_tool(db_path, name, arguments), indent=2)}]},
            )
        return jsonrpc_error(request_id, -32601, f"method not found: {method}")
    except (FileNotFoundError, ValueError, TypeError) as exc:
        return jsonrpc_error(request_id, -32602, str(exc))


def serve_json_lines(db_path: Path) -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError("request must be a JSON object")
            response = handle_request(db_path, request)
        except (json.JSONDecodeError, ValueError) as exc:
            response = jsonrpc_error(None, -32700, str(exc))
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run read-only JSON-RPC-style graph tools over the demo DB.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--serve", action="store_true", help="Read JSON-RPC requests as JSON lines from stdin.")
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--call", choices=[tool["name"] for tool in TOOLS])
    parser.add_argument("--arguments", default="{}", help="JSON object for --call arguments.")
    args = parser.parse_args()

    if args.serve:
        return serve_json_lines(args.db)

    if args.list_tools:
        print(json.dumps({"tools": TOOLS}, indent=2))
        return 0

    if args.call:
        arguments = json.loads(args.arguments)
        if not isinstance(arguments, dict):
            raise ValueError("--arguments must decode to a JSON object")
        print(json.dumps(call_tool(args.db, args.call, arguments), indent=2))
        return 0

    parser.error("use --serve, --list-tools, or --call")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
