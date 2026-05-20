# ALM Handoff Export Package

This package contains only graph records that have local human review metadata.
It is a one-way handoff artifact, not a formal ALM write or approval.

## Accepted Decisions

- `DEC-001` Should this change run a full V-process or a bounded delta V-process?
  - Selected option: `bounded_delta_v_process`
  - Rationale: Sample review accepted the bounded delta V-process path.
  - Decided by: `sample-reviewer`
  - Decided at: `2026-01-02T03:04:05Z`

## Reviewed Trace Candidates

- `CR-001` --`impacts`--> `REQ-001`
  - Source: ChangeRequest / Change timeout handling from fixed threshold to configurable threshold
  - Target: Requirement / Control loop shall enter a safe state on sensor timeout
  - Edge rationale: Configurable timeout handling can affect the safe-state transition requirement.
  - Review rationale: Sample trace review accepted the impact link to REQ-001.
  - Reviewed by: `sample-reviewer`
  - Reviewed at: `2026-01-02T03:04:05Z`

## Excluded From Export

- Non-accepted decisions: `1`
- Non-accepted trace candidates: `5`

## Boundary

- This export is preparation for a human-controlled ALM/SOP handoff.
- It does not write to Polarion, DOORS, Jama, Codebeamer, or another formal system.
- It does not create approvals, signatures, baselines, or audit closure.
- Formal ALM remains the authority for workflow state.
