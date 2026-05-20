# AI Agent Build Specification

This repository is not only a reference prototype.

It is also a build specification for AI coding agents.

Give this repository to Codex, Claude Code, Cursor, or another coding agent
together with an authorized target project. Ask the agent to build a
project-specific engineering-memory pipeline that extracts evidence, creates
graph records, and produces reviewable V-process outputs.

```text
This repository defines the operating model.
The target project provides the artifacts.
The AI coding agent builds the local pipeline.
Humans review and promote candidates.
```

## What The Agent Should Build

A project-specific implementation can include:

- A source/test/config/document inventory scanner.
- A parser or importer for authorized artifacts.
- A mapper from source facts into graph nodes and edges.
- A reverse-engineering pass that creates `ObservedBehavior`,
  `RequirementCandidate`, `TraceCandidate`, `Evidence`, and `OpenIssue` records.
- A V-process activity recommendation pass.
- A SQLite exporter compatible with `schema/001_core.sql`.
- A review report for humans.
- Optional adapters for GitHub Issues, Markdown specs, Polarion, DOORS, Jama,
  Codebeamer, or another formal ALM system.

The exact implementation should follow the target project's language, build
system, repository layout, and authorization boundary.

This repository includes a minimal local demo:

```text
prototype/vprocess_graph.py
  Loads fictional project data into SQLite graph tables and prints policy-based
  V-process activity recommendations, including AND-condition policies.

prototype/llm_recommend.py
  Reads the SQLite graph, builds bounded LLM context, and can call a local
  Ollama model for review recommendations.

prototype/impact_query.py
  Uses a recursive SQLite CTE to query review-relevant impact paths from a
  change request or another start node.

prototype/export_review_report.py
  Exports a deterministic Markdown review report from the same graph context.

benchmarks/run_sample_benchmark.py
  Runs the fictional sample scenario and checks that the expected activities,
  open issue, trace context, and export boundary are present.
```

The demo is deliberately small. It proves the read path from graph DB to LLM
context, recursive SQLite impact query, and Markdown report export, but it is
not a production trace engine, MCP server, or formal ALM adapter.

## Per-Project Empty Environment

For repeated use, create a separate empty engineering-memory environment beside
the target project instead of mixing generated state into this repository.

Use [templates/empty_environment](../templates/empty_environment) as the
starting point. It gives the agent:

- a small `AGENTS.md` for the per-project runtime;
- a SQLite schema compatible with this repository's graph model;
- a bootstrap script that creates an empty graph DB;
- a project profile file for the target project path and authority model;
- a reusable prompt template for the first agent request;
- an optional boundary for task queues such as Beads.

Recommended separation:

```text
This repository
  Defines the build specification and public operating model.

Per-project empty environment
  Holds local graph DB, project profile, generated reports, and importer code.

Target project
  Provides authorized source, tests, documents, logs, and configuration.

Execution queue, if used
  Tracks ready, blocked, claimed, and completed implementation work.
```

Do not commit generated databases, private project profiles, customer reports,
or target-project artifacts back to this public reference repository.

Cross-platform copy command:

```bash
python templates/empty_environment/scripts/create_instance.py \
  --destination ../my-project-memory \
  --target-project ../my-project \
  --project-name my-project
```

Windows PowerShell users can also use:

```powershell
.\templates\empty_environment\scripts\create_instance.ps1 `
  -Destination "..\my-project-memory" `
  -TargetProject "..\my-project" `
  -ProjectName "my-project"
```

If an execution queue such as Beads is available, connect it after the graph DB
is initialized. Do not make the queue the source of engineering facts; use it
only for ready, blocked, claimed, and completed work.

## Prompt: Build A Local Engineering-Memory Pipeline

```text
Read this repository as a build specification for AI-assisted engineering
memory.

Then inspect the authorized target project and create a local
engineering-memory pipeline that:

1. inventories source files, tests, configuration, logs, and documentation;
2. extracts observed behavior and evidence;
3. creates RequirementCandidate, TraceCandidate, Evidence, OpenIssue, and
   Decision records;
4. stores the records as graph nodes and edges compatible with
   schema/001_core.sql;
5. recommends V-process activities such as impact analysis, trace review,
   regression test selection, approval gate preparation, and open issue triage;
6. writes a human-readable review report;
7. keeps all inferred requirements and traces as candidates until human review;
8. does not ingest secrets, customer data, proprietary standards text, or
   unauthorized third-party artifacts.

Before coding, summarize the target project's artifact types and propose the
node/edge mapping. After coding, run tests and the public safety gate.
```

## Prompt: Review The Demo Graph With A Local LLM

First build the demo graph:

```bash
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json
```

Then either inspect the prompt:

```bash
python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider prompt
```

Or call a local Ollama model:

```bash
python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider ollama \
  --model llama3.1
```

The expected behavior is not an authoritative approval. The model should return
a bounded review: recommended activities, supporting evidence, blocking open
issues, trace links that need human review, and claims that must not be made
yet.

## Prompt: Query Recursive Impact Paths

```bash
python prototype/impact_query.py \
  --db .demo/vprocess_demo.db \
  --start CR-001 \
  --max-depth 2
```

This query uses SQLite recursive CTEs over the local `edges` table. It identifies
candidate impact paths such as change request to requirement to standard
reference. It is not a formal impact-analysis approval.

## Prompt: Export A Markdown Review Report

```bash
python prototype/export_review_report.py \
  --db .demo/vprocess_demo.db \
  --output .demo/review_report.md
```

The report is a one-way review artifact. It does not write to Polarion, DOORS,
Jama, Codebeamer, or another formal ALM system. Use it to review candidates
before deciding what should be promoted into the formal tool.

## Prompt: Reverse Engineer Requirements From Authorized Code

```text
Use docs/09_reverse_engineering_workflow.md as the operating procedure.

Analyze only the authorized source, test, configuration, log, and documentation
files in the target project.

For each recovered behavior, produce:

- ObservedBehavior
- Evidence
- RequirementCandidate
- TraceCandidate edges
- OpenIssue records for ambiguity
- Recommended V-process activity
- Human decision needed

Do not present inferred requirements as authoritative. Mark them as
needs_review until a human reviewer promotes them.
```

## Prompt: Build A Review Report

```text
Read the generated engineering-memory graph and create a review report with:

1. recommended V-process activities;
2. the trigger for each recommendation;
3. the evidence and node IDs supporting it;
4. candidate trace links;
5. open issues that block approval or ALM export;
6. decisions that require human review;
7. suggested next actions.

Do not claim automatic compliance. Keep the report as decision support.
```

## Prompt: Add A Formal ALM Export Adapter

```text
Add an export adapter from the engineering-memory graph to the target team's
formal ALM workflow.

Before implementation:

- identify which graph nodes can be exported;
- identify which records must remain candidates;
- identify required human approval points;
- identify fields that map to the ALM system;
- identify fields that must not be exported.

The adapter must not make the graph authoritative. Formal ALM remains the
authority for workflow state, baselines, signatures, approvals, and audit
records.
```

## Expected Deliverables

For a target project, the agent should normally create:

```text
tools/
  project-specific scanner/importer/exporter scripts

schema/
  optional project-specific schema extensions

examples/
  sanitized sample input and output

reports/
  generated review report examples, if safe to publish

tests/
  focused tests for the importer, mapper, and report generator
```

Generated databases, private reports, customer artifacts, logs, and caches
should stay out of public commits unless explicitly sanitized.

## Acceptance Criteria

A project-specific pipeline is useful when it can answer:

- Which existing artifacts were analyzed?
- Which behaviors were observed?
- Which requirements were inferred?
- Which evidence supports each inference?
- Which trace links are candidates?
- Which open issues block confidence or approval?
- Which V-process activities are recommended?
- Which decisions require a human reviewer?

It is not useful if it only summarizes files without preserving traceable
evidence, uncertainty, and review decisions.

## Boundary

This specification is for authorized engineering work only.

Do not use it for unauthorized third-party reverse engineering, DRM bypass,
credential extraction, secret discovery, malware development, evasion workflows,
or publication of private operational details.
