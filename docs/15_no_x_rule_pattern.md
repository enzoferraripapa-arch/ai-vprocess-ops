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

## Reuse And Delta Rules

Reuse and delta development are high-risk because the project already has
documents, components, tests, and approvals that look familiar. Familiarity is
not applicability.

| Rule | Prohibited assumption | Required evidence | Fallback |
| --- | --- | --- | --- |
| `NO-LEGACY-AS-CURRENT` | A legacy artifact, existing design, or previous document is current project truth. | Current scope, current baseline, applicability review, changed assumptions, and owner disposition. | Use it only as reference input until accepted for this project. |
| `NO-PAST-PASS-AS-CURRENT-PASS` | A previous pass, approval, review, or release result still passes the current project. | Current criteria, current evidence snapshot, delta impact review, reviewer, and revalidation result. | Reopen the gate or mark the old result as historical evidence only. |
| `NO-SMALL-DELTA-AS-LOW-RISK` | A small-looking change is automatically low risk. | Affected interfaces, timing, safety/security impact, regression scope, and hidden dependency check. | Route through delta impact review before lowering review depth. |
| `NO-REUSE-AS-TRACE-CLOSURE` | Reusing a component, document, template, or test closes traceability. | Current source requirement, target artifact, link rationale, applicability status, and accepted trace review. | Keep trace links as candidates until reviewed. |
| `NO-EXISTING-TEST-AS-REVALIDATION` | Existing tests prove the reused or changed item is validated now. | Current configuration, test environment, acceptance criteria, regression rationale, and re-run or justified reuse result. | Plan revalidation or record why the existing test is not sufficient. |

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
