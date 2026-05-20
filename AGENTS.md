# Agent Instructions

Use this repository as an engineering-memory reference architecture for
AI-assisted V-process decision support.

## Core Rule

The LLM is not the source of truth.

```text
Model weights stay fixed.
Engineering state lives in the database.
The LLM reads structured graph context and proposes bounded engineering actions.
Humans and formal tools keep final authority.
```

Do not describe this workflow as model training or fine-tuning. It is external
memory: requirements, decisions, trace candidates, evidence, open issues, SOP
references, and standards references are stored outside the model.

## Read Order

Before changing or extending the project, read these files in order:

1. `README.md`
2. `docs/02_learning_vs_external_memory.md`
3. `docs/03_v_process_decision_graph.md`
4. `schema/001_core.sql`
5. `examples/sample_project_input.json`
6. `examples/sample_trace_graph.json`
7. `prototype/vprocess_graph.py`
8. `prototype/decision_lifecycle.py`
9. `docs/12_architecture.md`

Use `docs/10_ai_agent_build_spec.md` when a user wants an AI coding agent to
build a project-specific scanner, graph importer, reverse-engineering pipeline,
ALM export adapter, or human review report from this specification.

Use `docs/08_related_work_and_positioning.md` when explaining how this differs
from agent-memory, requirements-as-code, code-context graph, or GraphRAG tools.

Use `docs/09_reverse_engineering_workflow.md` for authorized legacy-system
recovery tasks where existing code, tests, logs, configuration, or partial
documentation are converted into observed behavior, requirement candidates,
trace candidates, open issues, and V-process activity recommendations.

## Intended Work

When asked to use or extend this repository, preserve this operating model:

- Store engineering context as graph nodes and edges.
- Keep examples fictional and sanitized.
- Preserve rationale, not only final output.
- Connect each recommendation to the requirement, change, issue, SOP, standard
  reference, or policy that triggered it.
- Treat trace links as candidates until reviewed.
- Treat reverse-engineered requirements as candidates until reviewed and
  formally promoted.
- Record accepted or rejected decisions with reviewer, rationale, and timestamp;
  do not treat those records as formal ALM approval.
- Treat V-process activity recommendations as decision support, not approval.
- Keep formal ALM systems authoritative for baselines, workflow state,
  signatures, approvals, and audit records.

## Expected Agent Output

When producing analysis or recommendations from this repository, prefer this
shape:

```text
Recommendation:
  The V-process activity or review action being proposed.

Trigger:
  The requirement, change request, project attribute, policy, open issue, SOP,
  or standard reference that caused the recommendation.

Rationale:
  Why the action is needed.

Trace:
  Relevant node IDs and edge types.

Open Issues:
  Anything that blocks approval or export to a formal ALM system.

Human Decision Needed:
  The explicit decision that cannot be delegated to the LLM.
```

## Safety And Publication Rules

Never add real customer data, proprietary SOP text, copyrighted standards text,
server names, tokens, passwords, private keys, internal hostnames, or private DB
files.

Do not use this repository to support unauthorized third-party reverse
engineering, DRM or license-enforcement bypass, credential extraction, secret
discovery, malware development, or evasion workflows.

Do not commit generated SQLite databases, bytecode caches, local demo output, or
temporary scan artifacts. Curated Markdown sample outputs under
`examples/outputs/` and `benchmarks/sample_result.md` are allowed when they are
fictional, deterministic, and reviewed.

Before committing changes, run the relevant local checks:

```bash
python -m compileall -q prototype tools tests templates/empty_environment/scripts benchmarks
python -m unittest discover -s tests
python tools/check_public_safety.py
python tools/check_sample_outputs.py
python -m ruff check .
python -m bandit -q -r prototype tools templates/empty_environment/scripts benchmarks
```

If the prototype behavior changes, also run:

```bash
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json
python prototype/import_reverse_engineering.py \
  --db .demo/reverse_engineering.db \
  --input examples/sample_reverse_engineering_input.json
python prototype/impact_query.py \
  --db .demo/vprocess_demo.db \
  --start CR-001 \
  --max-depth 2
python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider prompt
python prototype/decision_lifecycle.py \
  --db .demo/vprocess_demo.db \
  list
python prototype/decision_lifecycle.py \
  --db .demo/vprocess_demo.db \
  decide \
  --id DEC-001 \
  --status accepted \
  --selected-option bounded_delta_v_process \
  --decided-by local-reviewer \
  --rationale "Local review accepted the bounded delta path."
python prototype/export_review_report.py \
  --db .demo/vprocess_demo.db \
  --output .demo/review_report.md
python prototype/mcp_readonly_stub.py \
  --db .demo/vprocess_demo.db \
  --list-tools
python benchmarks/run_sample_regression.py
```

Remove `.demo/`, `.ruff_cache/`, and `__pycache__/` directories after local
verification.

## Do Not Claim

Do not claim:

- Automatic compliance.
- Replacement of human engineering judgement.
- Replacement of formal ALM systems.
- Replacement of agent-memory tools.
- Production readiness.
- That generated code is safe because it passed this repository's checks.

The narrow, useful claim is:

```text
AI-assisted engineering needs a durable graph of why, not only faster generation
of what.
```
