# Vibe Coding With Engineering Memory

Vibe coding works because an LLM can turn intent into working software quickly.
The risk is that the engineering thread can disappear just as quickly.

This project is a small structure for preserving that thread.

## The Problem

An AI-assisted coding session often produces useful code before the project has
clear requirements, decisions, trace links, tests, and review notes.

That is fine for exploration. It becomes expensive later when the team needs to
answer basic engineering questions.

```text
Why does this exist?
What requirement does it satisfy?
Which test proves it?
Which decision changed it?
What should not be changed casually?
What is still unresolved?
```

Chat history is not a durable answer to those questions.

## The Pattern

Use the graph as lightweight engineering memory.

```text
Requirement -> Decision -> Implementation -> Test -> Evidence
Requirement -> TraceCandidate -> TraceReview
Decision -> ALMHandoffPackage
          \-> OpenIssue
          \-> ExternalReference
```

The LLM can still draft code, tests, and explanations. The graph stores the
state that should survive beyond one chat window.

## Minimal Vibe Coding Workflow

1. Capture the user intent as a `Requirement` node.
2. Capture important tradeoffs as `Decision` nodes.
3. Link changed files or modules as implementation references.
4. Link tests or manual checks as `Evidence`.
5. Store unresolved assumptions as `OpenIssue`.
6. Record accepted or rejected human decisions with rationale and timestamp.
7. Record trace review state before treating a candidate link as handoff-ready.
8. Ask the LLM for the next action using only the relevant graph slice.

## Useful Edge Types

```text
implements
verified_by
depends_on
blocked_by
included_in_alm_handoff
supersedes
conflicts_with
explained_by
```

## Why This Is Not Heavy Process

The goal is not to slow down exploration.

The goal is to keep just enough structure so that fast AI-assisted work does
not become unreviewable code. A small graph can preserve the important context
without forcing a full enterprise ALM workflow at the start.

For higher-risk work, the same structure can produce a one-way handoff package
from accepted local review records. That package is still pre-formal: it helps a
human enter or import records into an ALM system, but it is not an ALM approval.

## Rule of Thumb

If a future engineer would ask "why is this here?", store the answer as a node
or edge while the context is still fresh.
