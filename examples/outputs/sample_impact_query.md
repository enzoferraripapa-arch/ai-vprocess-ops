# Impact Query

Start node: `CR-001`

This is a recursive SQLite CTE over the local `nodes` and `edges` tables. It is impact discovery, not approval.

## Reachable Paths

- depth 0: `CR-001` (ChangeRequest) Change timeout handling from fixed threshold to configurable threshold
  - Path: `CR-001`
- depth 1: `ACT-IMPACT` (Activity) Change impact analysis
  - Path: `CR-001 -> ACT-IMPACT`
  - Via: `CR-001` --`requires_activity`--> `ACT-IMPACT`
  - Rationale: The change modifies runtime behavior.
- depth 1: `OI-001` (OpenIssue) Timeout configuration authority is not defined
  - Path: `CR-001 -> OI-001`
  - Via: `CR-001` --`blocked_by`--> `OI-001`
  - Rationale: The owner of product-profile timeout values must be decided before formal approval.
- depth 1: `REQ-001` (Requirement) Control loop shall enter a safe state on sensor timeout
  - Path: `CR-001 -> REQ-001`
  - Via: `CR-001` --`impacts`--> `REQ-001`
  - Rationale: Configurable timeout handling can affect the safe-state transition requirement.
- depth 1: `REQ-002` (Requirement) Diagnostic event shall be recorded for timeout transition
  - Path: `CR-001 -> REQ-002`
  - Via: `CR-001` --`impacts`--> `REQ-002`
  - Rationale: Configurable timeout handling can affect diagnostic-event recording.
- depth 1: `SOP-DEMO-IMPACT-01` (SOP) Fictional SOP: software change impact review
  - Path: `CR-001 -> SOP-DEMO-IMPACT-01`
  - Via: `CR-001` --`uses_sop`--> `SOP-DEMO-IMPACT-01`
  - Rationale: Change handling should follow this operating procedure.
- depth 2: `STD-SW-IMPACT-01` (StandardClause) Fictional standard clause: change impact analysis
  - Path: `CR-001 -> REQ-001 -> STD-SW-IMPACT-01`
  - Via: `REQ-001` --`references_standard`--> `STD-SW-IMPACT-01`
  - Rationale: Requirement should be checked against this summarized standard reference.
- depth 2: `STD-SW-TRACE-01` (StandardClause) Fictional standard clause: bidirectional traceability
  - Path: `CR-001 -> REQ-001 -> STD-SW-TRACE-01`
  - Via: `REQ-001` --`references_standard`--> `STD-SW-TRACE-01`
  - Rationale: The requirement is safety-relevant and requires verification trace.
- depth 2: `STD-SW-IMPACT-01` (StandardClause) Fictional standard clause: change impact analysis
  - Path: `CR-001 -> REQ-002 -> STD-SW-IMPACT-01`
  - Via: `REQ-002` --`references_standard`--> `STD-SW-IMPACT-01`
  - Rationale: Requirement should be checked against this summarized standard reference.
- depth 2: `STD-SW-TRACE-01` (StandardClause) Fictional standard clause: bidirectional traceability
  - Path: `CR-001 -> REQ-002 -> STD-SW-TRACE-01`
  - Via: `REQ-002` --`references_standard`--> `STD-SW-TRACE-01`
  - Rationale: Requirement should be checked against this summarized standard reference.

## Boundary

- These paths identify candidate impact and review scope.
- A human reviewer must decide which paths become formal ALM trace links.
- Do not treat recursive reachability as compliance, approval, or baseline status.
