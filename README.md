# AI-Native V-Process Operations

LLM + graph database + standards knowledge for engineering decision support.

This project is a public, sanitized reference architecture for using modern AI
to support V-process operation without training a custom model and without
replacing formal ALM systems.

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

## Repository Layout

```text
docs/
  Concept and operating model.

schema/
  Minimal SQLite schema for the graph and decision layer.

examples/
  Sanitized, fictional input data.

prototype/
  Dependency-free Python demo using SQLite.

benchmarks/
  Templates for measuring output quality and cost reduction.
```

## Quick Start

From the repository root:

```bash
python public/ai-vprocess-ops/prototype/vprocess_graph.py \
  --db public/ai-vprocess-ops/.demo/vprocess_demo.db \
  --input public/ai-vprocess-ops/examples/sample_project_input.json
```

The demo creates a local SQLite DB, loads fictional requirements and standards
references, creates trace candidates, and prints recommended V-process
activities.

## Public Release Rules

- Use fictional or sanitized examples only.
- Do not publish real customer requirements, proprietary SOPs, tokens, server
  names, or confidential standards text.
- Keep standards references as clause IDs and short original summaries.
- Choose a license before publishing as a standalone GitHub repository.
- Treat the architecture as decision support, not as an autonomous compliance
  authority.

