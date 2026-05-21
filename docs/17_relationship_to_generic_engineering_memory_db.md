# Relationship To A Generic Engineering-Memory DB

`ai-vprocess-ops` is the V-process review and handoff method layer. It sits
between project memory, if any, and the formal ALM / SOP / QMS system, and it
can be used with or without a separate generic engineering-memory DB.

This repository contains one V-process / pre-ALM reference method. It does not
contain two products or two required databases. A generic engineering-memory
DB, if used, is an external upstream project-memory layer.

Use the generic DB to preserve project state. Use this repository to define the
review, traceability, decision, and handoff rules that become important when
the project needs engineering evidence.

## Layer Relationship

```text
Generic engineering-memory DB
  Stores per-project memory:
  requirements, decisions, evidence, tests, open issues, traces, rationale,
  source references, session notes, and next actions.

ai-vprocess-ops
  Defines the V-process / pre-ALM method:
  candidate boundaries, No-X rules, decision lifecycle, trace review,
  impact query, review report, and one-way ALM handoff package.

Formal ALM / SOP / QMS system
  Keeps final authority:
  baselines, workflow state, signatures, formal approvals, audit records,
  customer-controlled records, and regulated evidence.
```

The relationship is directional:

```text
generic DB state -> ai-vprocess-ops review method -> formal handoff candidate
```

The generic DB can exist without `ai-vprocess-ops`, and `ai-vprocess-ops` can
be used without a generic DB by loading project facts directly into its local
SQLite graph. Use both only when the project actually needs both memory and
V-process review structure.

It is not:

```text
generic DB state -> automatic approval
ai-vprocess-ops output -> formal ALM record
ai-vprocess-ops repository -> bundled generic DB product
```

## What Each Layer Owns

| Layer | Owns | Does not own |
| --- | --- | --- |
| Generic engineering-memory DB | Project-local memory, facts, decisions, evidence pointers, open issues, traces, rationale, and next-session context. | Formal approval, compliance, baseline authority, or customer/QMS record status. |
| `ai-vprocess-ops` | How to structure candidates, review decisions, trace candidates, impact paths, No-X boundaries, and pre-formal handoff packages. | The target project's real data, final engineering judgement, production connector authority, or legal/regulatory acceptance. |
| Formal ALM / SOP / QMS | Official records, workflow states, signatures, baselines, approvals, release evidence, and audit trail. | AI-generated inference unless it has been reviewed and entered through the formal process. |

## When To Use The Generic DB Alone

Use only the generic DB when the work is lightweight:

- short-lived coding tasks;
- exploratory prototypes;
- personal project memory;
- issue tracking across AI sessions;
- local design notes and evidence pointers;
- non-regulated utilities where formal traceability is not needed yet.

Even then, keep the core boundary: memory is not approval.

## When To Add `ai-vprocess-ops`

Add this repository's method when the project needs more structure:

- requirements need source/rationale tracking;
- generated output must become reviewable candidates;
- tests, evidence, and defects need trace links;
- decisions need accepted/rejected/needs-review state;
- impact analysis must be explainable;
- ALM, SOP, QMS, safety, cybersecurity, or regulated handoff may appear later;
- AI agents need clear rules for what they may infer and what humans must
  decide.

## Practical Integration Pattern

1. Start with the generic DB for project-local memory.
2. Add or map these record families:
   - `Requirement`
   - `Decision`
   - `Evidence`
   - `Test`
   - `OpenIssue`
   - `TraceCandidate`
   - `ActivityRecommendation`
   - `ReviewRecord`
3. Apply the No-X rules from
   [docs/15_no_x_rule_pattern.md](15_no_x_rule_pattern.md).
4. Generate review reports and handoff packages from reviewed local records
   only.
5. Enter or import formal records through the target organization's approved
   ALM/SOP/QMS process.

## Responsibility Boundary

The generic DB and `ai-vprocess-ops` can make project reasoning more durable and
reviewable. They do not make the project safe, compliant, approved, released, or
market-ready.

If a derived workflow is used for real product development, the user of that
workflow is responsible for deciding the applicable standards, evidence,
reviewers, tests, approvals, connectors, release process, and operational
controls.

See also
[docs/16_application_examples_and_responsibility.md](16_application_examples_and_responsibility.md).
