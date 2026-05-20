# Authorized Reverse Engineering Workflow

This workflow uses the same engineering-memory graph for authorized reverse
engineering of existing software, configuration, tests, logs, and partial
documentation.

The goal is not to bypass protections, extract secrets, or analyze third-party
systems without permission. The goal is to recover engineering intent from
systems that are already owned, maintained, inherited, or explicitly authorized
for analysis.

```text
Existing artifacts
  -> observed behavior
  -> inferred requirement candidates
  -> trace candidates
  -> open issues
  -> reviewed engineering memory
```

## Core Rule

Every reverse-engineered statement starts as a candidate.

```text
Observed behavior is evidence.
Inferred intent is a hypothesis.
Trace links are candidates.
Requirements become authoritative only after human review and formal promotion.
```

## Input Sources

Use only authorized and sanitized material:

- Source files.
- Configuration files.
- Test cases and test results.
- Logs and runtime observations.
- Build scripts.
- API examples.
- Existing design notes.
- Issue tickets or review comments.
- Formal ALM exports when available.

Do not ingest secrets, credentials, customer data, proprietary standards text,
or private operational details into a public graph.

## Suggested Node Types

These node types can be represented using the generic `nodes` table in
`schema/001_core.sql`.

```text
SourceFile
Function
Interface
ConfigItem
ObservedBehavior
InferredRequirement
RequirementCandidate
TestCandidate
Evidence
OpenIssue
Risk
Decision
Activity
StandardClause
SOP
```

## Suggested Edge Types

```text
contains
calls
reads_config
emits_event
observed_in
inferred_from
implements_candidate
verified_by
blocked_by
needs_review
requires_activity
references_standard
uses_sop
promoted_to_requirement
```

## Analysis Passes

## Executable Sample Import

The repository includes a fictional authorized reverse-engineering sample and a
small importer that projects it into the same SQLite graph schema:

```bash
python prototype/import_reverse_engineering.py \
  --db .demo/reverse_engineering.db \
  --input examples/sample_reverse_engineering_input.json
```

Then inspect candidate paths from an authorized source artifact:

```bash
python prototype/impact_query.py \
  --db .demo/reverse_engineering.db \
  --start SRC-FW-TIMEOUT \
  --max-depth 3 \
  --edge-types observed_in,implements_candidate,verified_by,blocked_by,requires_activity
```

This import is still candidate-state only. It does not promote inferred
requirements, close open issues, or export approved links to a formal ALM
system.

### 1. Inventory Pass

Identify the authorized artifacts and create source/evidence nodes.

Expected output:

```text
SourceFile nodes
ConfigItem nodes
Test/Evidence nodes
OpenIssue nodes for unreadable or ambiguous areas
```

### 2. Behavior Pass

Extract what the system actually appears to do.

Use `ObservedBehavior` for behavior that is directly supported by code, tests,
logs, or configuration. Attach evidence with `observed_in` or `inferred_from`
edges.

Do not turn observed behavior directly into a formal requirement.

### 3. Requirement Candidate Pass

Translate observed behavior into `RequirementCandidate` or
`InferredRequirement` nodes.

Each candidate should include:

- The observed behavior that supports it.
- The evidence source.
- Confidence.
- Known assumptions.
- Review questions.

### 4. Trace Candidate Pass

Create candidate edges between behavior, requirement candidates, tests, risks,
SOP references, standard references, and open issues.

Useful trace questions:

- Which behavior appears to implement this candidate requirement?
- Which test currently verifies it?
- Which config item changes it?
- Which open issue blocks confidence?
- Which V-process activity is now required?

### 5. V-Process Gap Pass

Recommend missing or incomplete engineering activities.

Examples:

```text
Impact analysis:
  Needed when a recovered behavior changes externally visible behavior or risk.

Trace review:
  Needed when inferred requirements are not connected to tests or evidence.

Regression test selection:
  Needed when reused behavior is partially modified.

Open issue triage:
  Needed when ownership, intended behavior, or acceptance criteria are unclear.
```

### 6. Human Promotion Gate

A human reviewer decides whether a candidate becomes a formal artifact.

Possible outcomes:

```text
promote_to_requirement
keep_as_candidate
split_candidate
merge_candidate
reject_as_implementation_detail
open_issue
export_to_alm_after_review
```

## Expected Agent Output

When an AI agent analyzes existing artifacts, prefer this output shape:

```text
Observed Behavior:
  What the artifact appears to do.

Evidence:
  Source IDs, file paths, test names, log snippets, or configuration keys.

Inferred Requirement Candidate:
  A candidate requirement written in requirement language.

Confidence:
  high / medium / low, with a reason.

Trace Candidates:
  Candidate node IDs and edge types.

Open Issues:
  Ambiguities, missing ownership, missing tests, conflicting behavior, or
  anything that blocks formal promotion.

Recommended V-Process Activity:
  Impact analysis, trace review, regression selection, review question, or
  another bounded activity.

Human Decision Needed:
  The decision that must not be delegated to the LLM.
```

## Example Graph Fragment

```text
SourceFile: SRC-FW-TIMEOUT
  -> contains Function: FN-TIMEOUT-CHECK

Function: FN-TIMEOUT-CHECK
  -> reads_config ConfigItem: CFG-SENSOR-TIMEOUT-MS
  -> emits_event ObservedBehavior: BEH-SAFE-STATE-ON-TIMEOUT

ObservedBehavior: BEH-SAFE-STATE-ON-TIMEOUT
  -> inferred_from SourceFile: SRC-FW-TIMEOUT
  -> inferred_from Evidence: TEST-TIMEOUT-SAFE-STATE
  -> implements_candidate RequirementCandidate: RC-SAFE-STATE-TIMEOUT
  -> blocked_by OpenIssue: OI-TIMEOUT-OWNER

RequirementCandidate: RC-SAFE-STATE-TIMEOUT
  -> requires_activity Activity: ACT-TRACE
  -> requires_activity Activity: ACT-IMPACT
```

## What To Avoid

Do not use this workflow for:

- Unauthorized third-party system analysis.
- DRM or license enforcement bypass.
- Credential extraction.
- Secret discovery.
- Malware development or evasion.
- Publishing private source code, customer data, server names, or confidential
  operational details.

The useful scope is narrower and practical:

```text
Recover engineering intent from authorized artifacts, keep uncertainty visible,
and turn legacy behavior into reviewable V-process candidates.
```
