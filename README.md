# AI-Native V-Process Operations

[![CI](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/ci.yml)
[![Security](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/security.yml/badge.svg)](https://github.com/enzoferraripapa-arch/ai-vprocess-ops/actions/workflows/security.yml)

LLM + graph database + standards knowledge for engineering decision support.

This project is a public, sanitized reference architecture for using modern AI
to support V-process operation without training a custom model and without
replacing formal ALM systems.

It is also useful for vibe coding: move fast with an LLM, but keep the
engineering memory that lets you review, test, explain, and safely change the
result later.

```text
Vibe code fast. Keep the engineering memory.
```

AI coding needs engineering memory, not just better autocomplete.

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

## Repository Layout

```text
AGENTS.md
  Operating instructions for AI coding agents.

docs/
  Concept, operating model, promotion notes, and related-work positioning.

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
```

## Share This

If this resonates, see [docs/07_promotion_kit.md](docs/07_promotion_kit.md)
for short posts, longer announcements, and audience notes.

For nearby projects and positioning, see
[docs/08_related_work_and_positioning.md](docs/08_related_work_and_positioning.md).

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
python -m compileall -q prototype tools tests
python -m unittest discover -s tests
python tools/check_public_safety.py
python -m ruff check .
python -m bandit -q -r prototype tools
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json
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
