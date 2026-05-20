# AI-Native V-Process Operations

[![CI](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/ci.yml)
[![Security](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/security.yml/badge.svg)](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/security.yml)

LLM + graph database + standards knowledge for engineering decision support.

This project is a public, sanitized reference architecture for using modern AI
to support V-process operation without training a custom model and without
replacing formal ALM systems.

Use it with Codex, Claude Code, Cursor, GitHub Copilot, or another AI coding
agent when the real problem is not code generation speed, but loss of
engineering context: requirements, traceability, decisions, evidence, tests,
open issues, and ALM handoff reasoning.

It is also useful for vibe coding: move fast with an LLM, but keep the
engineering memory that lets you review, test, explain, and safely change the
result later.

```text
Vibe code fast. Keep the engineering memory.
```

AI coding needs engineering memory, not just better autocomplete or agent
memory.

Not another prompt template.

This repository is a graph-backed build specification for AI agents that need to
create project-specific engineering memory: requirements, decisions, trace
candidates, evidence, open issues, V-process recommendations, and authorized
reverse-engineering reports.

Most agent-memory tools help an agent remember conversations, tasks, or codebase
structure. This project uses a narrower boundary: preserve engineering meaning
that must survive the chat session, then let humans or formal tools decide what
becomes authoritative.

Shareable one-liner:

```text
AI-Native V-Process Operations is a lightweight graph memory for AI-assisted
engineering, built to preserve requirements, decisions, tests, evidence, and
open issues before they disappear into chat history.
```

## For AI Agents

If you are using Codex, Claude Code, Cursor, or another coding agent, start with
[AGENTS.md](AGENTS.md). It defines the read order, operating boundary, expected
recommendation format, and publication safety rules for this repository.

This repository is also a build specification for AI coding agents. Give it to
an agent together with an authorized target project and ask it to build a local
engineering-memory pipeline: artifact inventory, graph importer, reverse
engineering pass, V-process recommendations, and human review report.

See [docs/10_ai_agent_build_spec.md](docs/10_ai_agent_build_spec.md) for prompt
examples.

For a ready-to-copy per-project starter workspace, see
[templates/empty_environment](templates/empty_environment). It gives an AI
agent a local graph DB, project profile, schema, bootstrap scripts, and first
request template without mixing private project state into this public
reference repository.

## Core Thesis

The LLM is not the source of truth.

The model is not trained or fine-tuned by this workflow. Project state,
decisions, rationale, traces, unresolved issues, and external references are
stored in a structured graph database. The LLM reads the relevant graph context
and helps engineers plan, review, compare, and explain V-process activities.

In short:

```text
Model weights stay fixed.
Engineering state lives in the database.
The LLM reads the database and proposes the next engineering action.
Humans and formal tools keep final authority.
```

## What This Is

- A pre-ALM engineering intelligence layer.
- A graph model for V-process activity planning and trace reasoning.
- A way to connect requirements, design, implementation, tests, decisions,
  risks, standards references, and unresolved issues.
- A low-cost architecture for review preparation, trace candidate generation,
  activity recommendation, and decision explainability.
- A copyable build specification for AI coding agents that need durable
  engineering memory across sessions.

## Current Prototype Scope

The prototype is intentionally small. Today it demonstrates three concrete
things:

1. loading fictional project/change data into SQLite graph tables;
2. matching simple V-process activity policies against a project profile;
3. building an LLM review prompt from the graph, with optional local Ollama
   execution.

It is not yet a production trace engine, recursive impact-analysis engine,
MCP server, GraphRAG system, or ALM export adapter. Those are project-specific
extensions that should be built and tested against authorized target artifacts.
The current graph layer is a small SQLite `nodes`/`edges` schema, not a
Neo4j-style path-query engine.

## Who This Is For

- Engineers using AI coding agents for real projects, not only demos.
- Vibe coders who need to recover the reason behind generated code.
- Reviewers of AI-generated pull requests.
- Teams preparing requirements, tests, trace candidates, and evidence before
  formal ALM entry.
- Builders of local-first agent memory, MCP, context engineering, requirements
  as code, and traceability tooling.

## For Vibe Coders

Vibe coding is fast, but the engineering context can disappear quickly.

If you have never lost the reason behind AI-generated code, you may not need
this yet. If you have, this project is for you.

This project gives AI-assisted coding sessions a lightweight graph memory:
requirements, decisions, tests, unresolved issues, and external references are
stored as nodes and edges instead of being buried in chat history.

Use it when you want to move fast with an LLM while still keeping enough
engineering structure to answer practical questions later:

- Why was this feature built?
- Which requirement or user need does it serve?
- Which test should cover it?
- Which decision changed the design?
- What is still unresolved?
- What could break if this changes again?

## What This Is Not

- It is not model training.
- It is not a replacement for human engineering judgement.
- It is not a replacement for formal ALM records, baselines, signatures, or
  regulated approval workflows.
- It is not a copy of any commercial ALM product.
- It does not include proprietary standards text or confidential project data.
- It is not a tool for unauthorized third-party reverse engineering, DRM
  bypass, credential extraction, or secret discovery.

## Intended Boundary

```text
Graph DB
  Stores engineering state, trace candidates, decisions, rationale, and issues.

LLM
  Reads structured context and drafts recommendations, questions, and review
  checklists.

Formal ALM
  Remains the authority for approved work items, workflow state, baselines,
  signatures, and audit records.

Standards/SOP Knowledge
  Provides external constraints and review criteria through references or
  summaries, not copied copyrighted source text.
```

## Minimal Use Cases

1. Decide which V-process activities are required for a project or change.
2. Generate trace candidates between requirements, design, tests, and evidence.
3. Build a review checklist from project risk, lifecycle phase, and standards
   references.
4. Track unresolved process or compliance questions before formal ALM entry.
5. Explain why a process activity was selected, skipped, or escalated.
6. Preserve engineering context during AI-assisted or vibe-coded development.
7. Recover requirement and trace candidates from authorized legacy artifacts.

## Use The Right Weight

This pattern is useful for many AI-assisted projects, not because every project
is regulated or safety-critical, but because AI work often loses the context
that engineers need later:

```text
Why was this built?
Which assumptions were used?
What is still unresolved?
Which decision changed the direction?
Which test, source, or evidence supports the result?
What should the next session read first?
```

Scale the workflow to the risk and expected lifetime of the work:

| Project shape | Recommended use |
| --- | --- |
| Small one-off task | Keep a short agent instruction file, project profile, and open issues. |
| Normal app or tool | Add artifact inventory, decisions, tests, evidence, and trace candidates. |
| Long-lived project | Add importers, review reports, and optional execution-task tracking. |
| Regulated, SOP, ALM, or safety-related work | Use the full graph and keep formal approval outside this environment. |

The default boundary is:

```text
Execution queue carries the work.
The graph DB preserves why the work exists.
Formal ALM or SOP systems keep final authority.
```

Task queues such as Beads are useful, but optional. They track execution state:
ready, blocked, claimed, and completed. The graph DB is different: it records
requirements, decisions, evidence, uncertainty, and rationale so the next
engineer or AI session can understand why the work exists.

For a copyable starter workspace, see
[templates/empty_environment](templates/empty_environment).

## Repository Layout

```text
AGENTS.md
  Operating instructions for AI coding agents.

docs/
  Concept, operating model, prompt examples, promotion notes, and positioning.

schema/
  Minimal SQLite schema for the graph and decision layer.

examples/
  Sanitized, fictional input data.

prototype/
  Dependency-free Python demo using SQLite.

tests/
  Standard-library unit tests for the Python prototype.

tools/
  Public safety checks for secrets, internal markers, JSON, Python, schema, and workflows.

benchmarks/
  Templates for measuring output quality and cost reduction.

templates/empty_environment/
  Copyable per-project workspace for local engineering-memory runs.
```

## Share This

If this resonates, see [docs/07_promotion_kit.md](docs/07_promotion_kit.md)
for short posts, longer announcements, and audience notes.

For launch order, target audiences, and traffic metrics, see
[docs/11_distribution_plan.md](docs/11_distribution_plan.md).

For nearby projects and positioning, see
[docs/08_related_work_and_positioning.md](docs/08_related_work_and_positioning.md).

For authorized legacy-system recovery, see
[docs/09_reverse_engineering_workflow.md](docs/09_reverse_engineering_workflow.md)
and [examples/sample_reverse_engineering_input.json](examples/sample_reverse_engineering_input.json).

For AI agent prompt examples, see
[docs/10_ai_agent_build_spec.md](docs/10_ai_agent_build_spec.md).

## Quick Start

From the repository root:

```bash
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json
```

The demo creates a local SQLite DB, loads fictional requirements and standards
references, creates trace candidates, and prints recommended V-process
activities.

Then build the LLM review prompt from the graph:

```bash
python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider prompt
```

If you run a local Ollama server, you can ask a model to review the graph:

```bash
python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider ollama \
  --model llama3.1
```

The LLM output is still only decision support. Requirements, trace links, and
activity recommendations remain candidates until human review.

## Quality And Safety Gates

This repository intentionally keeps the first safety layer simple and auditable.
The core local gate uses only the Python standard library:

```bash
python -m unittest discover -s tests
python tools/check_public_safety.py
```

GitHub Actions also runs:

- Python compile and unit tests on Python 3.11, 3.12, and 3.13.
- The public safety gate for secret-like strings, internal project markers,
  generated DB artifacts, JSON validity, SQL schema loading, and workflow
  permissions.
- Ruff and Bandit for Python quality and static security checks.
- CodeQL and Dependency Review as GitHub-native security checks.
- Dependabot for GitHub Actions and pinned Python development-tool updates.

Current baseline:

- `CI` verifies that the Python prototype compiles, the unit tests pass, the
  public safety gate passes, and the demo can build/query the sample graph.
- `Ruff and Bandit` provide a small static quality/security layer for Python
  without changing the prototype's dependency-free runtime.
- `Security` runs CodeQL on the Python code and Dependency Review on pull
  requests that change dependencies.
- `Dependabot` keeps GitHub Actions and pinned development tools visible as
  reviewable update pull requests.
- The public safety gate rejects common publication accidents: committed SQLite
  databases, bytecode caches, private-key-like material, token-like strings,
  internal project markers, invalid JSON, broken SQL schema loading, broad
  workflow permissions, `pull_request_target`, and workflows that require
  repository secrets.

Useful local checks:

```bash
python -m compileall -q prototype tools tests templates/empty_environment/scripts
python -m unittest discover -s tests
python tools/check_public_safety.py
python -m ruff check .
python -m bandit -q -r prototype tools templates/empty_environment/scripts
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json
python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider prompt
```

The goal is not to claim that automation proves engineering quality. The goal
is to make low-cost mistakes visible before they reach users: broken examples,
lost trace behavior, leaked private context, unsafe workflow permissions, and
unreviewed dependency/tooling drift.

## Public Release Rules

- Use fictional or sanitized examples only.
- Do not publish real customer requirements, proprietary SOPs, tokens, server
  names, or confidential standards text.
- Keep standards references as clause IDs and short original summaries.
- Choose a license before publishing as a standalone GitHub repository.
- Treat the architecture as decision support, not as an autonomous compliance
  authority.
