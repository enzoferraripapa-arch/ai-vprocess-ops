# Distribution Plan

This repo will not spread just because it is public. The target audience is
high-context: people already using AI coding agents on real projects and feeling
context loss, traceability loss, or review-preparation cost.

## Message

Lead with the problem, not with V-process terminology.

```text
AI coding agents can build fast, but the engineering reason behind the work
disappears across sessions.
```

Then position the repo:

```text
ai-vprocess-ops is a graph-backed build specification and copyable starter
environment for preserving engineering memory: requirements, decisions,
evidence, trace candidates, tests, open issues, and ALM handoff reasoning.
```

## Audience Order

| Priority | Audience | Lead With | Avoid |
| --- | --- | --- | --- |
| 1 | Claude Code / Codex / Cursor power users | Cross-session context loss and copyable empty environment | Compliance claims |
| 2 | Agent-memory and MCP builders | Engineering memory vs general agent memory | V-process jargon first |
| 3 | Vibe coding communities | Why generated code exists and what tests/evidence support it | Enterprise process language |
| 4 | Requirements / systems engineers | Trace candidates, evidence, review gates, ALM handoff | Replacing Polarion/DOORS/Jama |
| 5 | Hacker News / devtools | Small auditable prototype and local-first design | Grand claims |

## First Week

1. Publish or update a GitHub release note for the empty-environment template.
2. Post one short community note focused on AI coding context loss.
3. Wait for feedback before posting elsewhere.
4. If no response, improve the README title/first paragraph rather than posting
   the same message repeatedly.
5. Track stars, forks, views, clones, issues, and referrers after each post.

## Metrics

Use GitHub traffic as a weak signal only.

| Metric | Meaning |
| --- | --- |
| Unique views | Humans are at least opening the repo. |
| Stars | The message is understandable enough to save. |
| Forks | Someone may try the template or adapt it. |
| Issues/discussions | The audience has enough context to engage. |
| Clone spikes without views | Often bots, CI, dependency tools, or automated indexing. |

## Posting Rule

Do not post as a sales pitch.

Ask for feedback from people with the actual pain:

```text
I am interested in feedback from people using AI agents on long-running
projects, especially where context loss, traceability, or review preparation
becomes the bottleneck.
```
