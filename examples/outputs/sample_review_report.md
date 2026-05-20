# V-Process Graph Review Report

This report is generated from the local engineering-memory graph. It is decision support, not approval.

## Project Context

- Project: `PROJECT-DEMO-001` Fictional motor controller firmware update
- Risk level: `high`
- Reuse level: `partial`
- Change type: `behavior-changing software update`
- Formal ALM: `external`

## Recommended V-Process Activities

- `ACT-TRACE` Trace candidate review [high]
  - Conditions: `change_type=behavior-changing software update`
  - Recommendation: Review trace candidates before ALM export.
  - Rationale: Behavior-changing software updates can invalidate existing requirement-test traces.
- `ACT-GATE` Approval gate preparation [high]
  - Conditions: `change_type=behavior-changing software update AND risk_level=high`
  - Recommendation: Prepare approval gate review before formal ALM export.
  - Rationale: High-risk behavior changes need explicit gate evidence before candidate traces are promoted.
- `ACT-IMPACT` Change impact analysis [high]
  - Conditions: `risk_level=high`
  - Recommendation: Run change impact analysis before implementation.
  - Rationale: High-risk changes need affected requirements, tests, and controls identified.
- `ACT-REGRESSION` Regression test selection [normal]
  - Conditions: `reuse_level=partial`
  - Recommendation: Select regression tests for reused and modified behavior.
  - Rationale: Partial reuse requires confirmation that unchanged behavior remains covered.

## Evidence And Trace Links

- `CR-001` --`blocked_by`--> `OI-001`
  - The owner of product-profile timeout values must be decided before formal approval.
- `PROJECT-DEMO-001` --`contains`--> `CR-001`
  - Project profile contains this change request.
- `PROJECT-DEMO-001` --`contains`--> `REQ-001`
  - Project profile contains this requirement candidate.
- `PROJECT-DEMO-001` --`contains`--> `REQ-002`
  - Project profile contains this requirement candidate.
- `CR-001` --`impacts`--> `REQ-001`
  - Configurable timeout handling can affect the safe-state transition requirement.
- `CR-001` --`impacts`--> `REQ-002`
  - Configurable timeout handling can affect diagnostic-event recording.
- `REQ-001` --`references_standard`--> `STD-SW-IMPACT-01`
  - Requirement should be checked against this summarized standard reference.
- `REQ-001` --`references_standard`--> `STD-SW-TRACE-01`
  - The requirement is safety-relevant and requires verification trace.
- `REQ-002` --`references_standard`--> `STD-SW-IMPACT-01`
  - Requirement should be checked against this summarized standard reference.
- `REQ-002` --`references_standard`--> `STD-SW-TRACE-01`
  - Requirement should be checked against this summarized standard reference.
- `CR-001` --`requires_activity`--> `ACT-IMPACT`
  - The change modifies runtime behavior.
- `CR-001` --`uses_sop`--> `SOP-DEMO-IMPACT-01`
  - Change handling should follow this operating procedure.

## Open Issues Blocking Approval Or ALM Export

- `OI-001`: Timeout configuration authority is not defined

## Human Decisions Needed

- `DEC-001` Should this change run a full V-process or a bounded delta V-process?
  - Current option: `bounded_delta_v_process`
  - Status: `draft`
  - Rationale: The change affects existing behavior but does not introduce a new subsystem. Impact analysis and regression selection are mandatory.
- `DEC-002` Should trace links be exported to the formal ALM immediately?
  - Current option: `export_after_review`
  - Status: `draft`
  - Rationale: Trace links are candidates until the engineering review confirms affected requirements and test coverage.

## Export Boundary

- Export only reviewed candidates to a formal ALM or SOP system.
- Do not export candidate trace links as approved links.
- Do not claim automatic compliance, production readiness, approval, baseline status, signature status, or audit closure.
- Keep formal workflow state, baselines, signatures, and audit records in the formal system.
