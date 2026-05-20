# Self-Use Playbook

Use this playbook when applying the engineering-memory pattern to one of your
own projects.

## Recommended Flow

1. Copy this empty environment to a new per-project directory.
2. Initialize it with the target project path.
3. Give the AI agent this environment, the target project, and the reference
   `ai-vprocess-ops` repository.
4. Ask the AI agent to build a local pipeline, not a final compliance claim.
5. Review the report and promote only reviewed facts into formal systems.

## Minimum First Pass

The first useful pass should produce:

- artifact inventory
- initial graph importer
- requirement or intent candidates
- decision candidates
- test and evidence candidates
- open issues
- trace candidates
- human review report

## Authority Boundaries

```text
LLM output
  Draft recommendations and candidates.

Graph DB
  Durable engineering-memory working state.

Human review
  Converts candidates into accepted decisions or rejected notes.

Formal ALM or SOP system
  Owns baseline, workflow state, signatures, approvals, and audit records.
```

## First Agent Prompt

Use `templates/agent_request.md` and replace the target project if needed.

