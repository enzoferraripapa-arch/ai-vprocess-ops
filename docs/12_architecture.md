# Architecture

This repository is a local-first engineering-memory pattern for AI-assisted
development. The graph is a working memory for review and decision support; it
is not the approval authority.

```mermaid
flowchart LR
    target["Authorized target project<br/>source, tests, docs, logs"]
    importer["Project-specific scanner/importer<br/>built by an AI coding agent"]
    graph["SQLite engineering-memory graph<br/>nodes, edges, decisions, policies"]
    policy["Policy matcher<br/>single and AND conditions"]
    impact["Recursive impact query<br/>SQLite CTE paths"]
    prompt["LLM review context<br/>bounded prompt or local Ollama"]
    report["Markdown review report<br/>deterministic export"]
    tools["Read-only JSON-RPC tool stub<br/>graph context, impact paths, report text"]
    human["Human engineering review"]
    alm["Formal ALM / SOP system<br/>baselines, signatures, approvals"]
    queue["Optional execution queue<br/>ready, blocked, claimed, done"]

    target --> importer --> graph
    graph --> policy
    graph --> impact
    graph --> prompt
    graph --> report
    graph --> tools
    policy --> human
    impact --> human
    prompt --> human
    report --> human
    tools --> human
    human --> alm
    queue -. execution state only .-> importer
    queue -. does not own engineering facts .-> graph
```

## Responsibility Split

| Layer | Owns | Does Not Own |
| --- | --- | --- |
| Target project | Authorized source artifacts, tests, logs, documents, configuration | AI-generated engineering conclusions |
| Importer/scanner | Project-specific extraction and mapping into graph records | Formal approval or compliance claims |
| SQLite graph | Requirements, decisions, evidence, trace candidates, open issues, policy inputs | Final ALM workflow state |
| Policy and impact queries | Candidate recommendations and candidate impact paths | Human engineering judgement |
| LLM prompt/report | Review assistance, questions, summaries, next-action drafts | Authority, signatures, baselines |
| Formal ALM/SOP system | Approved work items, baselines, workflow state, signatures, audit records | Unreviewed inferred candidates |

## Current Executable Path

```bash
python prototype/vprocess_graph.py \
  --db .demo/vprocess_demo.db \
  --input examples/sample_project_input.json

python prototype/impact_query.py \
  --db .demo/vprocess_demo.db \
  --start CR-001 \
  --max-depth 2

python prototype/llm_recommend.py \
  --db .demo/vprocess_demo.db \
  --provider prompt

python prototype/export_review_report.py \
  --db .demo/vprocess_demo.db \
  --output .demo/review_report.md

python prototype/mcp_readonly_stub.py \
  --db .demo/vprocess_demo.db \
  --list-tools
```

## Boundary

The graph can preserve why work exists and what evidence supports candidate
recommendations. It must not be treated as automatic compliance, production
readiness, formal approval, or a replacement for Polarion, DOORS, Jama,
Codebeamer, or another ALM system.
