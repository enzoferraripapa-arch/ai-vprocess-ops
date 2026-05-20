#!/usr/bin/env python3
"""Public release safety gate for the sample repository.

The checks are intentionally dependency-free so they can run in local shells and
GitHub Actions before heavier third-party scanners.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".demo", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"}
TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".gitignore",
    ".gitattributes",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sql",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}
DISALLOWED_ARTIFACT_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pyc", ".pyo", ".pyd", ".pem", ".p12", ".key"}
DISALLOWED_FILENAMES = {".env", ".env.local"}

SECRET_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("openai-token", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "assigned-secret",
        re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"),
    ),
]

INTERNAL_MARKERS = [
    ("internal-project-name", re.compile(r"\bTORASAN\b", re.IGNORECASE)),
    ("internal-host-provider", re.compile(r"\bKAGOYA\b", re.IGNORECASE)),
    ("internal-vps-marker", re.compile(r"\bv133\b", re.IGNORECASE)),
    ("private-db-name", re.compile(r"polarion_(?:knowledge|manual_architecture)\.db", re.IGNORECASE)),
    ("source-corpus-path", re.compile(r"reference_docs[/\\]", re.IGNORECASE)),
    ("windows-user-path", re.compile(r"\b[A-Z]:\\Users\\[^\\\s]+")),
    ("unix-home-path", re.compile(r"(?<![A-Za-z0-9_.-])/home/[A-Za-z0-9_.-]+/")),
    ("codex-local-path", re.compile(r"(?:^|[/\\])\.codex(?:[/\\]|$)")),
    ("claude-local-path", re.compile(r"(?:^|[/\\])\.claude(?:[/\\]|$)")),
]


@dataclass(frozen=True)
class Finding:
    check: str
    path: Path
    message: str

    def format(self) -> str:
        return f"{self.check}: {self.path.as_posix()}: {self.message}"


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)


def iter_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and not is_excluded(path))


def read_text(path: Path) -> tuple[str | None, Finding | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError as exc:
        return None, Finding("utf8", relative(path), f"not UTF-8 text: {exc}")


def check_disallowed_artifacts(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        rel = relative(path)
        if path.name in DISALLOWED_FILENAMES or path.suffix.lower() in DISALLOWED_ARTIFACT_SUFFIXES:
            findings.append(Finding("artifact", rel, "generated, private, or credential-like file must not be committed"))
    return findings


def check_text_files(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE"}:
            continue

        text, error = read_text(path)
        if error is not None:
            findings.append(error)
            continue
        if text is None:
            continue

        rel = relative(path)
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(name, rel, "possible credential or private key material"))
        for name, pattern in INTERNAL_MARKERS:
            if pattern.search(text):
                findings.append(Finding(name, rel, "internal project marker should not be published"))
    return findings


def check_json_files(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if path.suffix.lower() != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(Finding("json", relative(path), f"invalid JSON: {exc}"))
    return findings


def check_python_files(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        if path.suffix.lower() != ".py":
            continue
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except SyntaxError as exc:
            findings.append(Finding("python", relative(path), str(exc)))
    return findings


def check_sql_schema() -> list[Finding]:
    schema_path = ROOT / "schema" / "001_core.sql"
    template_schema_path = ROOT / "templates" / "empty_environment" / "schema" / "001_core.sql"
    findings: list[Finding] = []
    try:
        schema = schema_path.read_text(encoding="utf-8")
        conn = sqlite3.connect(":memory:")
        with conn:
            conn.executescript(schema)
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
                )
            }
        conn.close()
    except sqlite3.Error as exc:
        return [Finding("schema", relative(schema_path), f"schema does not load: {exc}")]

    expected = {
        "activity_policies",
        "decision_options",
        "decisions",
        "edges",
        "external_refs",
        "nodes",
        "policy_conditions",
        "run_log",
        "trace_reviews",
    }
    missing = expected - tables
    if missing:
        findings.append(Finding("schema", relative(schema_path), f"missing expected tables: {sorted(missing)}"))
    if template_schema_path.exists() and template_schema_path.read_text(encoding="utf-8") != schema:
        findings.append(
            Finding(
                "schema-parity",
                relative(template_schema_path),
                "template schema must match schema/001_core.sql exactly",
            )
        )
    return findings


def check_workflows(files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    workflow_dir = ROOT / ".github" / "workflows"
    workflow_files = [
        path for path in files if path.parent == workflow_dir and path.suffix.lower() in {".yml", ".yaml"}
    ]
    for path in workflow_files:
        text = path.read_text(encoding="utf-8")
        rel = relative(path)
        if "permissions:" not in text:
            findings.append(Finding("workflow-permissions", rel, "workflow should declare explicit permissions"))
        if re.search(r"permissions:\s*(?:write-all|read-all)", text):
            findings.append(Finding("workflow-permissions", rel, "avoid broad workflow permissions"))
        if "pull_request_target:" in text:
            findings.append(Finding("workflow-trigger", rel, "pull_request_target is not allowed in this public sample"))
        if "secrets." in text:
            findings.append(Finding("workflow-secrets", rel, "public sample workflows should not require repository secrets"))
    return findings


def run_checks() -> list[Finding]:
    files = iter_files()
    findings: list[Finding] = []
    findings.extend(check_disallowed_artifacts(files))
    findings.extend(check_text_files(files))
    findings.extend(check_json_files(files))
    findings.extend(check_python_files(files))
    findings.extend(check_sql_schema())
    findings.extend(check_workflows(files))
    return findings


def main() -> int:
    findings = run_checks()
    if findings:
        print("Public safety gate failed:")
        for finding in findings:
            print(f"- {finding.format()}")
        return 1

    print("Public safety gate passed.")
    print("Checked: UTF-8 text, secret patterns, internal markers, JSON, Python compile, SQL schema/parity, workflows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
