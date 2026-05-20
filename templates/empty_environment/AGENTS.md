# Agent Instructions

Use this directory as a per-project engineering-memory environment.

## Core Rule

The LLM is not the source of truth.

```text
Engineering state lives in the graph DB and reviewed artifacts.
The LLM reads structured context and proposes bounded actions.
Humans and formal tools keep final authority.
```

## Read Order

1. `README.md`
2. `runtime/project_profile.local.json`
3. `schema/001_core.sql`
4. `docs/01_self_use_playbook.md`
5. `docs/02_execution_queue_pattern.md`
6. `templates/agent_request.md`

If this template is still inside the `ai-vprocess-ops` repository, also read
the repository-root `AGENTS.md` and `docs/10_ai_agent_build_spec.md`. If the
template has been copied elsewhere, ask the user for the path or URL to the
`ai-vprocess-ops` reference repository when needed.

## Expected Work

For the configured target project:

- Build an artifact inventory.
- Create or extend graph importers.
- Store requirements, decisions, tests, evidence, and open issues as graph nodes.
- Store trace candidates as graph edges.
- Produce a human review report.
- Keep unresolved work visible as open issues.

## Execution Queue Boundary

If a task queue such as Beads is available, use it only for execution tracking:

- ready work
- blocked work
- claimed work
- completed implementation tasks

Do not use the execution queue as the authority for engineering facts, trace
rationale, approval state, SOP text, or formal ALM records.

## Do Not Claim

Do not claim:

- automatic compliance
- production readiness
- formal approval
- replacement of Polarion, DOORS, Jama, Codebeamer, or another ALM system
- that an LLM output is authoritative

