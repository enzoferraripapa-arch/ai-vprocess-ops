# Concept

## Problem

V-process work is often treated as a static checklist. Real engineering work is
not static. Activities change based on product risk, change type, reuse level,
available evidence, standards obligations, open issues, and review findings.

Formal ALM tools are good at storing approved records. They are usually less
convenient for early reasoning: comparing process options, finding missing
evidence, drafting trace candidates, and deciding where review effort should go.

This architecture separates those responsibilities.

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
5. Let engineers approve, reject, or revise the recommendation.
6. Export accepted records into the formal ALM system when needed.
```

## Design Rules

- Store decisions with rationale, alternatives, and status.
- Distinguish approved records from candidates.
- Link every recommendation to evidence or an unresolved question.
- Keep copyrighted standards text out of the public DB; store clause references
  and short summaries instead.
- Prefer explicit typed edges over free-form conversation history.
- Make skipped activities explainable, not invisible.

