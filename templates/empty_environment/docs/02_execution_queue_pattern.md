# Execution Queue Pattern

An execution queue is useful when an AI agent needs stable task tracking while
building or extending this environment. Beads is one possible queue, but the
pattern is not tied to a specific tool.

## Division Of Responsibility

```text
Execution queue
  Tracks agent work: ready, blocked, claimed, completed.

Graph DB
  Tracks engineering meaning: why the task exists, what it affects, what is
  unresolved, and what evidence supports it.
```

## Good Queue Tasks

- Implement artifact inventory scanner.
- Add importer for Markdown documents.
- Add importer for test results.
- Generate trace candidate report.
- Add public-safety check for private markers.
- Fix failing unit tests.

## Bad Queue Tasks

- Approve a requirement.
- Declare compliance.
- Mark a formal ALM workflow state as approved.
- Store private customer data.
- Replace the graph DB as engineering memory.

## Suggested Mapping

| Queue concept | Graph DB concept |
| --- | --- |
| issue or task | task or open_issue node |
| blocked_by | `blocks` edge |
| claim | run_log entry or task owner |
| close | task status update after verification |
| compact memory | compact project profile and next action summary |

## Operating Rule

If the execution queue and the graph disagree, stop and reconcile. The queue can
say what the agent is doing next, but the graph should explain why the work
exists.

