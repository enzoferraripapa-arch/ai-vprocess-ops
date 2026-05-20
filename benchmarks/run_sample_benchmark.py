#!/usr/bin/env python3
"""Backward-compatible wrapper for the sample regression check."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_regression_module():
    module_path = ROOT / "benchmarks" / "run_sample_regression.py"
    spec = importlib.util.spec_from_file_location("run_sample_regression", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "benchmarks"))
    spec.loader.exec_module(module)
    return module


run_sample_regression = load_regression_module()

run_benchmark = run_sample_regression.run_regression_check


def main() -> int:
    return run_sample_regression.main()


if __name__ == "__main__":
    raise SystemExit(main())
