# Promotion Kit

Use these snippets when sharing the project.

## Project URL

https://github.com/enzoferraripapa-arch/ai-vprocess-ops

## One-Liner

AI coding needs engineering memory, not just better autocomplete.

## Discovery Keywords

Use these naturally in posts and README text. Do not stuff them mechanically.

```text
AI coding agents
engineering memory
agent memory
context engineering
Claude Code
Codex
Cursor
requirements traceability
V-process
ALM handoff
evidence graph
decision traceability
vibe coding
```

## High-Context One-Liner

Not another prompt template: a graph-backed build spec for AI agents that need
to create project-specific engineering memory.

## Short Pitch

AI-Native V-Process Operations is a lightweight graph memory for AI-assisted
engineering. It stores requirements, decisions, tests, evidence, unresolved
issues, and external references as nodes and edges so the reason behind
AI-generated work does not disappear into chat history.

## High-Context Pitch

This is for people who already know that prompt patterns are not enough.

`ai-vprocess-ops` is a graph-backed build specification for AI coding agents.
Give it to Codex, Claude Code, Cursor, or another agent together with an
authorized target project, then ask it to build a local engineering-memory
pipeline: artifact inventory, graph importer, reverse-engineering pass,
V-process recommendations, and human review report.

The point is not to write better prompts. The point is to make the agent build a
project-specific system that preserves requirements, decisions, trace
candidates, evidence, open issues, and review gates.

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

## Launch Order

Use a small sequence instead of posting everywhere at once.

1. GitHub release or pinned repository note: explain what the repo is and who
   should use it.
2. `r/ClaudeCode` or a Claude Code community: lead with cross-session context
   loss and the copyable empty environment.
3. `r/AI_Agents` or local-first agent-memory communities: lead with the
   boundary between task queue, graph DB, and formal authority.
4. Hacker News `Show HN`: lead with the small auditable prototype and ask for
   feedback from people building agent-memory and developer-tooling systems.
5. One direct reply/comment in a relevant thread about Beads, MCP memory,
   context engineering, requirements-as-code, or traceability. Do not spam
   unrelated threads.

## GitHub Release Note

Title:

```text
v0.2.0: Copyable engineering-memory environment for AI coding agents
```

Body:

```text
This release turns ai-vprocess-ops from a reference repo into a copyable starter
workspace for AI-assisted engineering memory.

Highlights:

- templates/empty_environment: per-project starter environment
- local SQLite graph DB bootstrap
- project profile for target-project boundaries
- first-request prompt for Codex, Claude Code, Cursor, or other coding agents
- optional Beads/task-queue boundary
- clearer distinction between execution queue, graph DB, and formal ALM/SOP authority

The goal is not automatic compliance. The goal is to preserve requirements,
decisions, evidence, trace candidates, tests, and open issues before they
disappear into chat history.
```

## Hacker News / Reddit Style Post

Title:

```text
Show HN: A graph-backed build spec for AI coding agents
```

Body:

```text
I built a small public reference repo for something I think AI coding tools are
missing: engineering memory.

Not another prompt template.
Not model training.
Not a replacement for ALM.

It is a graph-backed build specification that an AI coding agent can use to
create a project-specific engineering-memory pipeline: requirements, decisions,
trace candidates, evidence, open issues, V-process recommendations, authorized
reverse-engineering reports, and human review gates.

The LLM is not the source of truth. The graph is the durable engineering memory.
Humans and formal tools keep final authority.

Repo:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops
```

## Claude Code / Codex Community Post

Title:

```text
I made a copyable engineering-memory template for AI coding agents
```

Body:

```text
I published a small repo for a problem I keep hitting with AI coding agents:
the agent can build fast, but the engineering reason behind the work disappears
across sessions.

This is not another prompt template and not model training.

The repo defines a lightweight graph-backed engineering-memory pattern. The new
empty-environment template can be copied beside a target project and initialized
with a local SQLite graph DB. Then Codex, Claude Code, Cursor, or another agent
can build project-specific importers and reports around it.

The split is deliberate:

- task queue: ready / blocked / claimed / done work
- graph DB: requirements, decisions, evidence, trace candidates, open issues
- formal ALM/SOP system: approvals, baselines, signatures, audit records

Repo:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops

I am interested in feedback from people using agents on long-running projects,
especially where context loss, traceability, or review preparation becomes the
actual bottleneck.
```

## AI Agents / Context Engineering Post

Title:

```text
Engineering memory layer for AI agents: task queue != source of truth
```

Body:

```text
I published a small local-first reference repo around engineering memory for AI
agents.

The main idea: an execution queue is good for work state, but it should not be
the source of engineering facts. Requirements, decisions, evidence, tests,
trace candidates, open issues, and rationale need a durable structure that can
be reviewed by humans and later promoted into formal systems.

This repo uses a lightweight SQLite graph model and a copyable empty
environment that an AI coding agent can turn into a project-specific pipeline.
It is intentionally pre-ALM: the LLM is not authority, and formal tools keep
approval/baseline/signature state.

Repo:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops
```

## X / Short Thread

```text
AI coding does not need another prompt template.

It needs engineering memory.
```

```text
I published `ai-vprocess-ops`:
a graph-backed build spec for AI agents that need to create project-specific
engineering memory.

Requirements.
Decisions.
Trace candidates.
Evidence.
Open issues.
Review gates.
```

```text
The idea is simple:

Do not train the model.
Do not make the LLM the source of truth.
Store engineering state in a graph.
Let the agent read it and build project-specific pipelines around it.
```

```text
Useful for:

- AI coding sessions that lose rationale
- V-process decision support
- trace candidate generation
- authorized reverse engineering
- pre-ALM review preparation
```

```text
Repo:
https://github.com/enzoferraripapa-arch/ai-vprocess-ops
```

## GitHub Related-Project Comment

Use this only when it is directly relevant to a discussion about agent memory,
MCP, context engineering, requirements-as-code, traceability, or AI coding
guardrails.

```text
This is related, but from a slightly different angle.

Most agent-memory work focuses on helping the assistant remember facts,
preferences, patterns, or prior tasks.

I am exploring engineering memory instead: requirements, decisions, trace
candidates, evidence, open issues, V-process activity recommendations, and
human review gates stored as graph context.

The repo is not a finished platform. It is a build specification an AI coding
agent can read to create a project-specific pipeline.

https://github.com/enzoferraripapa-arch/ai-vprocess-ops
```

## Where Not To Lead

Do not lead with generic "Vibe Coding best practices" or "how to write better
prompts." That framing attracts readers who expect tutorials, prompt templates,
or beginner workflow advice.

Lead with this instead:

```text
Not another prompt template.
A graph-backed build spec for AI agents that need engineering memory.
```

The best audience already understands AGENTS.md, MCP, repo-local memory,
context engineering, CI gates, and the limits of chat history.

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
- GitHub issues/discussions in adjacent tools: lead with graph-backed
  engineering memory, not with generic AI coding advice.

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
