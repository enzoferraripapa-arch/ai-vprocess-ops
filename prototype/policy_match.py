"""Activity policy loading and profile matching helpers."""

from __future__ import annotations

import re
import sqlite3
from typing import Any

INTEGER_RE = re.compile(r"^-?\d+$")


def normalize_policy_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else str(value)
    if isinstance(value, str):
        stripped = value.strip()
        lowered = stripped.lower()
        if lowered in {"true", "false"}:
            return lowered
        if INTEGER_RE.fullmatch(stripped):
            return str(int(stripped))
        return stripped
    return str(value)


def load_activity_policies(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        """
        SELECT
            p.id,
            p.activity_id,
            n.title AS activity_title,
            p.trigger_key,
            p.trigger_value,
            p.recommendation,
            p.rationale,
            p.severity,
            pc.condition_key,
            pc.condition_value
        FROM activity_policies p
        JOIN nodes n ON n.id = p.activity_id
        LEFT JOIN policy_conditions pc ON pc.policy_id = p.id
        ORDER BY
            CASE p.severity WHEN 'high' THEN 0 ELSE 1 END,
            p.id,
            pc.condition_key,
            pc.condition_value
        """
    ).fetchall()

    policies: dict[str, dict] = {}
    for row in rows:
        policy_id = row["id"]
        if policy_id not in policies:
            policies[policy_id] = {
                "id": policy_id,
                "activity_id": row["activity_id"],
                "activity_title": row["activity_title"],
                "trigger_key": row["trigger_key"],
                "trigger_value": row["trigger_value"],
                "recommendation": row["recommendation"],
                "rationale": row["rationale"],
                "severity": row["severity"],
                "conditions": [],
            }
        if row["condition_key"] is not None:
            policies[policy_id]["conditions"].append(
                {"key": row["condition_key"], "value": row["condition_value"]}
            )

    for policy in policies.values():
        if not policy["conditions"]:
            policy["conditions"].append({"key": policy["trigger_key"], "value": policy["trigger_value"]})
        policy["conditions_summary"] = " AND ".join(
            f"{condition['key']}={condition['value']}" for condition in policy["conditions"]
        )

    return list(policies.values())


def policy_matches_profile(conditions: list[dict], profile: dict) -> bool:
    for condition in conditions:
        expected = normalize_policy_value(condition["value"])
        actual = normalize_policy_value(profile.get(condition["key"]))
        if actual is None or actual != expected:
            return False
    return True


def matching_activity_policies(conn: sqlite3.Connection, profile: dict) -> list[dict]:
    return [policy for policy in load_activity_policies(conn) if policy_matches_profile(policy["conditions"], profile)]
