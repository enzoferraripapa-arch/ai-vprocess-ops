# Agent Request Template

Read this environment first:

```text
AGENTS.md
runtime/project_profile.local.json
docs/01_self_use_playbook.md
docs/02_execution_queue_pattern.md
```

If available, read the `ai-vprocess-ops` reference repository.

Target project is defined in:

```text
runtime/project_profile.local.json
```

Build a local engineering-memory pipeline for the target project.

Required outputs:

- artifact inventory
- graph importer
- requirement, decision, test, evidence, and open_issue nodes
- trace candidates
- V-process activity recommendations
- human review report
- remaining blocked items

Rules:

- LLM output is not authority.
- Do not claim compliance.
- Do not include private data in public artifacts.
- Formal ALM approval stays outside scope.
- If an execution queue is available, use it only for execution tasks.
- Store durable engineering meaning in the graph DB.

