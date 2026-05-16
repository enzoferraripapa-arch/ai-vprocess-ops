# Promotion Kit

Use these snippets when sharing the project.

## Project URL

https://github.com/enzoferraripapa-arch/ai-vprocess-ops

## One-Liner

AI coding needs engineering memory, not just better autocomplete.

## Short Pitch

AI-Native V-Process Operations is a lightweight graph memory for AI-assisted
engineering. It stores requirements, decisions, tests, evidence, unresolved
issues, and external references as nodes and edges so the reason behind
AI-generated work does not disappear into chat history.

## For Vibe Coders

Vibe coding is fast. The problem is not speed. The problem is losing the reason
behind the code.

This project gives AI-assisted coding sessions a small graph memory:
requirements, decisions, tests, open issues, and evidence are stored as
structured context that can survive beyond one chat window.

## Longer Announcement

I published a small open-source reference architecture for AI-assisted
engineering:

https://github.com/enzoferraripapa-arch/ai-vprocess-ops

The idea is simple: LLMs should not only generate code. They should help
preserve engineering memory.

The model is not trained or fine-tuned. Instead, requirements, decisions,
trace candidates, test evidence, open issues, and external references are stored
in a lightweight graph database. The LLM reads that structured context and helps
engineers decide what to review, test, explain, or escalate next.

This is useful for V-process and regulated engineering, but it is also useful
for vibe coding. If you have ever looked at AI-generated code and asked, "Why
did we build it this way?", this project is for you.

## Social Post

AI coding needs engineering memory, not just better autocomplete.

I published `ai-vprocess-ops`, a lightweight graph memory for AI-assisted
engineering and vibe coding.

It stores requirements, decisions, tests, evidence, and open issues as nodes and
edges so the reason behind AI-generated work does not disappear into chat
history.

https://github.com/enzoferraripapa-arch/ai-vprocess-ops

## Hacker News / Reddit Style Post

Title:

```text
Show HN: A graph memory for AI-assisted engineering and vibe coding
```

Body:

```text
I built a small public reference architecture for preserving engineering memory
during AI-assisted development.

The goal is not to train an LLM or replace an ALM system. The goal is to keep
requirements, decisions, trace candidates, test evidence, and unresolved issues
as structured graph context so they do not vanish into chat history.

It started from V-process / regulated engineering thinking, but I think the same
problem appears in vibe coding: code gets generated quickly, but the reason
behind it is easy to lose.

Repo:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops
```

## AI Engineering Community Post

Title:

```text
Engineering memory for AI coding: V-process decisions as a small graph
```

Body:

```text
I published a small open-source prototype around a problem I keep seeing in
AI-assisted development:

The code can be generated quickly, but the engineering reason behind it is easy
to lose.

There are already strong projects around agent memory, MCP memory, requirements
as context, and code context graphs. This project is narrower: it explores
engineering memory for V-process decisions.

The prototype stores requirements, decisions, trace candidates, tests, evidence,
open issues, SOP references, and standards references as graph nodes and edges.
The LLM is not the source of truth and is not trained. It reads the graph and
helps propose what should be reviewed, tested, escalated, or traced next.

It is not a replacement for formal ALM tools. It is a lightweight pre-ALM /
decision-support layer for AI-assisted engineering and vibe coding.

Repo:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops

Related positioning:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops/blob/main/docs/08_related_work_and_positioning.md

I would be interested in feedback from people building agent memory, MCP tools,
requirements-as-code, or AI coding workflows.
```

## Short Community Reply

Use this when replying to a discussion about AI coding memory, context loss, or
requirements traceability:

```text
This is close to the problem I am exploring, but from a V-process / engineering
decision angle rather than general agent memory.

Others are building memory for agents. I am trying to preserve engineering
memory: requirements, decisions, trace candidates, tests, evidence, open issues,
SOP references, and standards references, so an LLM can help decide what should
be reviewed, tested, escalated, or traced next.

Prototype:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops
```

## Suggested Communities

- `r/vibecoding`: lead with lost context, design rationale, and safer vibe
  coding.
- `r/ClaudeCode`: lead with cross-session engineering memory and review
  preparation.
- `r/AI_Agents`: lead with graph memory as state management, not just recall.
- `r/mcp`: lead with future MCP integration potential and local-first context.
- `r/ContextEngineering`: lead with explicit graph context for engineering
  decisions.
- Hacker News `Show HN`: lead with the small, auditable prototype and the
  distinction from model training.

## Suggested Positioning Line

```text
Others are building memory for agents. This project explores engineering memory
for AI-assisted V-process decisions.
```

## Target Audience

- Engineers using LLMs for real code, not just demos.
- Vibe coders who have lost the reason behind AI-generated code.
- Reviewers dealing with AI-generated pull requests.
- Systems engineers who care about requirements, tests, and traceability.
- Teams that want lightweight structure before formal ALM entry.
- Tool builders thinking beyond autocomplete.

## What To Emphasize

- This is not model training.
- The LLM is not the source of truth.
- The database stores engineering memory.
- The graph preserves why, not only what.
- Human review and formal ALM still keep final authority.

## What Not To Claim

- Do not claim automatic compliance.
- Do not claim replacement of human judgement.
- Do not claim replacement of formal ALM workflows.
- Do not claim the prototype is production-ready.
- Do not publish proprietary standards text or confidential project data.
