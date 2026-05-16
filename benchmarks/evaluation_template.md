# Evaluation Template

Use this template to compare manual work, enterprise-tool-assisted work, and
AI + graph assisted work on the same input.

## Input Set

```text
Project profile:
Change request:
Requirements:
Standards references:
Existing tests:
Known open issues:
```

## Output Set

```text
V-process activities recommended:
Activities intentionally skipped:
Trace candidates:
Review questions:
Open issues:
Export candidates for formal ALM:
```

## Scoring

| Metric | Manual | Enterprise Tool | AI + Graph | Notes |
|---|---:|---:|---:|---|
| Correct activity selection |  |  |  |  |
| Missed mandatory items |  |  |  | Lower is better |
| False positives |  |  |  | Lower is better |
| Trace candidate usefulness |  |  |  |  |
| Explanation quality |  |  |  |  |
| Human review time |  |  |  | Lower is better |
| Setup time |  |  |  | Lower is better |
| Total cost |  |  |  | Lower is better |

## Acceptance Rule

The AI + graph approach is useful when it reduces preparation time while keeping
human review burden and missed mandatory items within an agreed tolerance.

The output should be accepted as candidate engineering context, not as an
automatic approval.

