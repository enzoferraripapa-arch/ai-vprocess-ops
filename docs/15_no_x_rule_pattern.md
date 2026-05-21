# No-X Rule Pattern

AI-assisted engineering fails when a useful intermediate artifact is mistaken
for authority. A No-X rule names that mistake explicitly.

This pattern keeps AI-agent output useful without letting it impersonate a
controlled engineering record, a formal approval, a passed gate, or accepted
traceability.

## Rule Shape

Use one row per boundary:

| Field | Meaning |
| --- | --- |
| Rule code | Stable identifier, such as `NO-CANDIDATE-AS-RECORD`. |
| Name | Short negative boundary. |
| Applies to | The artifact, event, route, trace, connector, or report section where the confusion appears. |
| Prohibited assumption | The false conclusion the project must not make. |
| Required evidence | What would have to exist before the stronger claim is allowed. |
| No-go signal | Observable condition that blocks promotion or handoff. |
| Fallback action | What the agent or reviewer should do instead. |

The negative wording is intentional. It prevents polite labels such as
"draft", "candidate", "planned", or "local accepted" from drifting into formal
authority.

## Core Rules

| Rule | Prohibited assumption | Required evidence | Fallback |
| --- | --- | --- | --- |
| `NO-ROUTING-AS-APPROVAL` | A route or recommendation means the project approved that activity. | Trigger source, affected activity, candidate status, reviewer, and approval record when authority is needed. | Keep it as a planning candidate until reviewed. |
| `NO-CANDIDATE-AS-RECORD` | A generated artifact is already a controlled record. | Draft status, source evidence, reviewer, storage target, baseline/reference id, and acceptance disposition. | Label it as candidate/draft and route it through review or handoff. |
| `NO-GATE-CANDIDATE-AS-PASS` | A gate candidate means the gate passed. | Entry rule, pass/fail condition, approver role, evidence snapshot, and final gate disposition. | Keep the activity blocked or under review. |
| `NO-TRACE-CANDIDATE-AS-TRACEABILITY` | A suggested trace link is accepted traceability. | Accepted link role, source/target ids, rationale, missing-link disposition, review result, and formal reference when required. | Keep it as candidate evidence until accepted/imported. |
| `NO-HANDOFF-AS-IMPORT` | A handoff package means the formal system was updated. | Package checksum, reviewer, import result, target ids, verification result, and residual issues. | Keep package status open until import/manual entry is verified. |
| `NO-LOCAL-ACCEPTED-AS-FORMAL-APPROVAL` | A local accepted decision is a formal ALM/QMS approval. | Formal system id, approver authority, workflow state, signature/approval evidence, and audit record when applicable. | Export only as a handoff candidate. |
| `NO-STATE-SKIP` | State can advance because the next state is convenient or implied. | From-state, to-state, actor, rationale, evidence snapshot, review disposition, and unresolved issue check. | Return to the last evidence-backed state and record the missing evidence. |
| `NO-CEREMONY-AS-ENGINEERING` | Completing a form, checklist, or workflow step means the engineering decision is sound. | Rationale, alternatives, constraints, affected interfaces, risk impact, and owner disposition. | Keep the engineering gate open until evidence is reviewed. |

## Empty Sections

An empty evidence section is not a promise that evidence exists elsewhere. It
should be marked as an absence marker:

```text
Not implemented / no event rows recorded yet.
Boundary: this is an explicit absence marker only; it is not execution evidence,
not a state transition, and not approval.
Pending checks: state evidence and audit path.
```

This avoids placeholder theater: a report can show the future evidence slot
without pretending the slot is populated.

## Agent Instructions

When an AI agent writes or updates project artifacts:

- attach the relevant No-X rule near the candidate output;
- do not hide the boundary in a separate policy document only;
- mark empty record sections as absence markers;
- require human review before promotion, import, baseline, approval, or closure;
- export candidate packages in one direction unless an approved connector
  authority package exists.

The goal is not more ceremony. The goal is to stop useful intermediate output
from silently becoming false authority.
