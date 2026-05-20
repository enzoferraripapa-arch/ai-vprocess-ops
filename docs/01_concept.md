# Concept

## Problem

V-process work is often treated as a static checklist. Real engineering work is
not static. Activities change based on product risk, change type, reuse level,
available evidence, standards obligations, open issues, and review findings.

Formal ALM tools are good at storing approved records. They are usually less
convenient for early reasoning: comparing process options, finding missing
evidence, drafting trace candidates, and deciding where review effort should go.

This architecture separates those responsibilities.

The public prototype now covers the pre-formal path end to end: graph import,
activity policy matching, recursive impact discovery, human decision recording,
trace review recording, review-report export, and one-way ALM handoff package
generation.

## Principle

Use a graph database as the working memory for engineering reasoning. Use the
LLM as a reader, analyst, and drafting assistant over that working memory. Keep
formal approval and baseline authority outside the LLM.

## Basic Flow

```text
1. Ingest project facts, requirements, changes, standards references, and SOPs.
2. Store them as nodes and typed edges.
3. Ask the LLM to reason over a bounded graph slice.
4. Generate activity recommendations, trace candidates, and review questions.
5. Let engineers accept, reject, or revise decisions and trace candidates.
6. Export accepted local review records into a one-way handoff package.
7. Let humans or project-specific adapters enter approved records into the
   formal ALM system when needed.
```

## Design Rules

- Store decisions with rationale, alternatives, and status.
- Store trace reviews separately from trace edges so candidate links do not
  become authoritative by accident.
- Distinguish formal ALM approval from local accepted review state.
- Link every recommendation to evidence or an unresolved question.
- Keep copyrighted standards text out of the public DB; store clause references
  and short summaries instead.
- Prefer explicit typed edges over free-form conversation history.
- Make skipped activities explainable, not invisible.
- Keep handoff exports one-way unless a target project explicitly implements a
  controlled formal adapter.
