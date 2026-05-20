#!/usr/bin/env python3
"""Export a deterministic Markdown review report from the demo graph."""

from __future__ import annotations

import argparse
from pathlib import Path

import llm_recommend


def render_list_item(identifier: str, title: str, detail: str | None = None) -> list[str]:
    lines = [f"- `{identifier}`: {title}"]
    if detail:
        lines.append(f"  - {detail}")
    return lines


def render_report(context: dict) -> str:
    lines = [
        "# V-Process Graph Review Report",
        "",
        "This report is generated from the local engineering-memory graph. It is decision support, not approval.",
        "",
        "## Project Context",
        "",
    ]

    for profile in context["project_profiles"]:
        lines.extend(
            [
                f"- Project: `{profile.get('_node_id', 'unknown')}` {profile.get('_title', 'Untitled')}",
                f"- Risk level: `{profile.get('risk_level', 'unknown')}`",
                f"- Reuse level: `{profile.get('reuse_level', 'unknown')}`",
                f"- Change type: `{profile.get('change_type', 'unknown')}`",
                f"- Formal ALM: `{profile.get('formal_alm', 'unknown')}`",
                "",
            ]
        )

    lines.extend(["## Recommended V-Process Activities", ""])
    for policy in context["matched_activity_policies"]:
        lines.extend(
            [
                f"- `{policy['activity_id']}` {policy['activity_title']} [{policy['severity']}]",
                f"  - Conditions: `{policy['conditions_summary']}`",
                f"  - Recommendation: {policy['recommendation']}",
                f"  - Rationale: {policy['rationale']}",
            ]
        )
    if not context["matched_activity_policies"]:
        lines.append("- No activity policy matched the current project profile.")

    lines.extend(["", "## Evidence And Trace Links", ""])
    for edge in context["trace_edges"]:
        lines.extend(
            [
                f"- `{edge['source_id']}` --`{edge['edge_type']}`--> `{edge['target_id']}`",
                f"  - {edge['rationale'] or 'No rationale recorded.'}",
            ]
        )
    if not context["trace_edges"]:
        lines.append("- No trace edges were selected for this report.")

    lines.extend(["", "## Open Issues Blocking Approval Or ALM Export", ""])
    for issue in context["open_issues"]:
        lines.extend(render_list_item(issue["id"], issue["title"], issue.get("body")))
    if not context["open_issues"]:
        lines.append("- No open issues recorded in the graph.")

    lines.extend(["", "## Human Decisions Needed", ""])
    for decision in context["decisions"]:
        lines.extend(
            [
                f"- `{decision['id']}` {decision['question']}",
                f"  - Current option: `{decision.get('selected_option') or 'undecided'}`",
                f"  - Status: `{decision['status']}`",
                f"  - Rationale: {decision.get('rationale') or 'No rationale recorded.'}",
            ]
        )
    if not context["decisions"]:
        lines.append("- No decision records found.")

    lines.extend(
        [
            "",
            "## Export Boundary",
            "",
            "- Export only reviewed candidates to a formal ALM or SOP system.",
            "- Do not export candidate trace links as approved links.",
            "- Do not claim automatic compliance, production readiness, approval, baseline status, signature status, or audit closure.",
            "- Keep formal workflow state, baselines, signatures, and audit records in the formal system.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a Markdown review report from the V-process graph.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Write the report to this Markdown file. Prints to stdout if omitted.")
    parser.add_argument("--edge-limit", type=int, default=40)
    args = parser.parse_args()

    with llm_recommend.connect(args.db) as conn:
        context = llm_recommend.collect_context(conn, edge_limit=args.edge_limit)
    report = render_report(context)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
