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
   regression test selection, and open issue triage;
6. writes a human-readable review report;
7. keeps all inferred requirements and traces as candidates until human review;
8. does not ingest secrets, customer data, proprietary standards text, or
   unauthorized third-party artifacts.

Before coding, summarize the target project's artifact types and propose the
node/edge mapping. After coding, run tests and the public safety gate.
```

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

