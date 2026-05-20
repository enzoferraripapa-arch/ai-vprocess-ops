# Validation Log

This file records manual validation evidence when the repository claims checks
beyond GitHub-hosted Ubuntu CI.

## 2026-05-20 - One-Way Handoff Export Adapter

Scope:

- `trace_reviews` schema extension.
- `prototype/alm_handoff_export.py`.
- deterministic `sample_alm_handoff.md`.
- sample regression update for reviewed trace handoff.

Windows local validation:

```bash
python -m compileall -q prototype tools tests templates/empty_environment/scripts benchmarks
python -m unittest discover -s tests
python tools/check_public_safety.py
python tools/check_sample_outputs.py
python -m ruff check .
python -m bandit -q -r prototype tools templates/empty_environment/scripts benchmarks
git diff --check
```

Result:

```text
27 tests OK.
Public safety gate passed.
Sample output check passed.
Ruff passed.
Bandit passed.
git diff --check passed.
```

Dell Ubuntu manual validation:

```bash
python -m compileall -q prototype tools tests templates/empty_environment/scripts benchmarks
python -m unittest discover -s tests
python tools/check_public_safety.py
python tools/check_sample_outputs.py
ruff check .
bandit -q -r prototype tools templates/empty_environment/scripts benchmarks
python prototype/vprocess_graph.py --db .demo/vprocess_demo.db --input examples/sample_project_input.json
python prototype/decision_lifecycle.py --db .demo/vprocess_demo.db decide --id DEC-001 --status accepted --selected-option bounded_delta_v_process --decided-by dell-reviewer --rationale "Dell Ubuntu review accepted the bounded delta path." --decided-at 2026-01-02T03:04:05Z
python prototype/alm_handoff_export.py --db .demo/vprocess_demo.db trace-review --source CR-001 --target REQ-001 --edge-type impacts --status accepted --reviewed-by dell-reviewer --rationale "Dell Ubuntu review accepted the impact link to REQ-001." --reviewed-at 2026-01-02T03:04:05Z
python prototype/alm_handoff_export.py --db .demo/vprocess_demo.db export --format markdown --output .demo/alm_handoff.md
python prototype/alm_handoff_export.py --db .demo/vprocess_demo.db export --format json --output .demo/alm_handoff.json
python prototype/import_reverse_engineering.py --db .demo/reverse_engineering.db --input examples/sample_reverse_engineering_input.json --format json
python prototype/impact_query.py --db .demo/vprocess_demo.db --start CR-001 --max-depth 2
python prototype/impact_query.py --db .demo/reverse_engineering.db --start SRC-FW-TIMEOUT --max-depth 3 --edge-types observed_in,implements_candidate,verified_by,blocked_by,requires_activity
python prototype/llm_recommend.py --db .demo/vprocess_demo.db --provider prompt
python prototype/export_review_report.py --db .demo/vprocess_demo.db --output .demo/review_report.md
python prototype/mcp_readonly_stub.py --db .demo/vprocess_demo.db --list-tools
python prototype/mcp_readonly_stub.py --db .demo/vprocess_demo.db --call impact_paths --arguments '{"start":"CR-001","max_depth":2}'
python benchmarks/run_sample_regression.py
```

Result:

```text
27 tests OK.
Public safety gate passed.
Sample output check passed.
Ruff passed.
Bandit passed.
DELL_FULL_TEST_OK.
```
