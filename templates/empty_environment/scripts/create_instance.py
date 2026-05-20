from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import shutil
import sys
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ".git",
    ".beads",
    ".demo",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "runtime",
}
EXCLUDED_FILE_PATTERNS = ("*.pyc", "*.db", "*.sqlite", "*.sqlite3", "*.log")


def is_excluded_file(path: Path) -> bool:
    return any(fnmatch.fnmatch(path.name, pattern) for pattern in EXCLUDED_FILE_PATTERNS)


def validate_destination(destination: Path) -> Path:
    destination = destination.expanduser().resolve()
    source = SOURCE_ROOT.resolve()
    if destination == source or source in destination.parents:
        raise ValueError(f"Destination must not be inside the template directory: {destination}")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"Destination exists and is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def copy_template(destination: Path) -> None:
    for item in SOURCE_ROOT.iterdir():
        if item.name in EXCLUDED_DIRS:
            continue
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(
                item,
                target,
                ignore=shutil.ignore_patterns(*EXCLUDED_DIRS, *EXCLUDED_FILE_PATTERNS),
            )
        elif not is_excluded_file(item):
            shutil.copy2(item, target)


def run_bootstrap(destination: Path, target_project: str, project_name: str) -> int:
    bootstrap_path = destination / "scripts" / "bootstrap_graph.py"
    spec = importlib.util.spec_from_file_location("empty_environment_bootstrap", bootstrap_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load bootstrap script: {bootstrap_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    old_argv = sys.argv[:]
    try:
        sys.argv = [
            str(bootstrap_path),
            "--target-project",
            target_project,
            "--project-name",
            project_name,
        ]
        return int(module.main())
    finally:
        sys.argv = old_argv


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy the empty engineering-memory environment and initialize its graph DB."
    )
    parser.add_argument("--destination", required=True)
    parser.add_argument("--target-project", required=True)
    parser.add_argument("--project-name", required=True)
    args = parser.parse_args()

    destination = validate_destination(Path(args.destination))
    copy_template(destination)
    result = run_bootstrap(destination, args.target_project, args.project_name)
    if result == 0:
        print(f"created instance: {destination}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
