# V-Process Decision Graph

## Node Types

The minimal graph uses these node families.

```text
ProjectProfile
Requirement
ChangeRequest
Risk
StandardClause
SOP
Activity
Decision
ReviewQuestion
TraceCandidate
Evidence
OpenIssue
```

Teams can add domain-specific nodes such as Hazard, SafetyGoal, FSR, TSR,
SoftwareRequirement, TestCase, TestResult, WorkItem, Baseline, or Release.

## Edge Types

```text
requires_activity
derived_from
traces_to
verified_by
mitigated_by
blocked_by
explained_by
references_standard
uses_sop
exported_to_alm
supersedes
conflicts_with
```

## Activity Decision Pattern

Each activity recommendation should answer four questions.

```text
Why is this activity needed?
Which evidence triggered it?
Which standard/SOP reference applies?
What happens if it is skipped?
```

## Example

```text
ChangeRequest: CR-001
  -> affects Requirement: REQ-001
  -> references StandardClause: STD-SW-TRACE-01
  -> requires_activity Activity: ImpactAnalysis
  -> requires_activity Activity: RegressionTestSelection
  -> blocked_by OpenIssue: OI-001
```

This is not just a checklist. It is a traceable decision structure.

