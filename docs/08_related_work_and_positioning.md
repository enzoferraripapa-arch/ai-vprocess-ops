# Related Work And Positioning

This project sits near several active AI engineering movements, but it has a
different center of gravity.

```text
Others are building memory for agents.
This project explores engineering memory for AI-assisted V-process decisions.
```

## Nearby Work

| Area | Examples | What They Focus On | Relationship To This Project |
| --- | --- | --- | --- |
| Agent memory | [MemoryGraph](https://github.com/memory-graph/memory-graph), [Memento MCP](https://github.com/lfrmonteiro99/memento-mcp), [Engram](https://github.com/tstockham96/engram) | Persistent memory for coding agents, often through MCP, typed memories, graph recall, or cross-session context | Very close in memory architecture, but usually broader than engineering process control |
| Requirements as context | [ContextGit](https://github.com/Mohamedsaleh14/ContextGit), [RTMX](https://github.com/rtmx-ai/rtmx), [Reqvire](https://github.com/reqvire-org/reqvire) | Requirements traceability, requirements-as-code, AI-readable project intent, tests, and status | Very close in traceability intent; this project adds V-process activity selection and SOP/standard/open-issue context |
| Code context graphs | [Code Context Graph / narsil-mcp](https://github.com/postrv/narsil-mcp) | Machine-readable code intelligence: call graphs, symbols, security findings, dependency intelligence, and local code context | Complementary; code context graphs can become one input to the V-process decision graph |
| Execution queues | [Beads](https://steveyegge.github.io/beads/) and similar agent-first task trackers | Ready, blocked, claimed, and completed work for long-running coding agents | Complementary; the queue carries execution state, while this project's graph preserves engineering meaning and rationale |
| AI-augmented V-model | [Agile V](https://agile-v.org/) and the related [paper](https://arxiv.org/abs/2602.20684) | AI agents across requirements, design, build, test, compliance, and human approval gates | Closest at the lifecycle level; this repository is a smaller, local-first reference architecture rather than a full framework |
| GraphRAG and context engineering | Knowledge graph / GraphRAG projects and MCP-based context layers | Turning fragmented project knowledge into queryable graph context for agents | Shares the graph-context idea, but uses explicit engineering artifacts and decision boundaries |

## Differentiation

This repository is intentionally not trying to become a general agent memory
platform, a full ALM replacement, or a commercial lifecycle suite.

Its specific scope is smaller:

- Preserve the reason behind AI-assisted engineering work.
- Store requirements, decisions, trace candidates, tests, evidence, open issues,
  SOP references, and standards references as structured graph context.
- Recommend V-process activities from project/change attributes.
- Keep formal ALM systems as the authority for baselines, approvals, signatures,
  workflow state, and audit records.
- Make publication and AI-assisted workflow accidents visible through simple CI
  and safety gates.

## Practical Positioning

Use this project when the problem is not "the agent forgot my preference", but:

- Why was this engineering activity selected?
- Which requirement, test, issue, or standard reference drove the decision?
- What is still unresolved before formal approval?
- What context should an LLM read before proposing a review, test, or change?
- What should stay in a lightweight graph before entering a formal ALM tool?

## Plain-Language Comparison

```text
Agent memory:
  Helps an AI assistant remember facts, preferences, patterns, and mistakes.

Requirements-as-context:
  Helps AI coding tools understand what should be built and how it is traced.

Code context graph:
  Helps AI tools understand the actual codebase structure and blast radius.

Execution queue:
  Helps agents know what work is ready, blocked, claimed, or done.

AI-native V-process operations:
  Helps engineers decide what process activity, trace review, test selection,
  open issue, or escalation is needed before the work is treated as complete.
```

## Community Fit

The idea is most likely to resonate with:

- AI coding and vibe coding communities that have felt context loss.
- MCP and agent-memory builders working on persistent local context.
- Requirements engineering and systems engineering practitioners.
- Reviewers of AI-generated pull requests.
- Teams trying to reduce process cost without pretending that an LLM is the
  source of truth.

## What To Avoid

Do not position this as:

- A replacement for agent memory tools.
- A replacement for Polarion, DOORS, Jama, Codebeamer, or other formal ALM
  systems.
- Automatic compliance.
- Proof that AI-generated code is safe.
- A finished production platform.

The useful claim is narrower and stronger:

```text
AI-assisted engineering needs a durable graph of why, not only faster generation
of what.
```
