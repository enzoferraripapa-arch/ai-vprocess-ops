# AI V-Process Empty Environment

This is a reusable empty runtime template for applying the `ai-vprocess-ops`
pattern to a real target project.

Use it as a copyable starting point when you want an AI agent to build a local
engineering-memory pipeline for a specific project.

## Roles

```text
ai-vprocess-ops reference repo
  Defines the operating model and public build specification.

This empty environment
  Holds the per-project graph DB, profile, prompts, reports, and optional task
  queue integration.

Target project
  The real code, documents, tests, logs, and configuration to analyze.

Execution queue, if available
  Tracks execution tasks: ready, blocked, claimed, done. Beads is one option,
  but this template does not require it.

Graph DB
  Tracks engineering memory: requirements, decisions, evidence, tests,
  open issues, traces, and rationale.
```

## When To Use This

Use this template when an AI agent will help create, modify, analyze, or
maintain a project across more than a trivial one-off task.

The useful part is not project type. It is preserving the engineering context
that usually disappears during AI-assisted work:

```text
Why was this built?
Which assumptions were used?
What is still unresolved?
Which decision changed the direction?
Which test, source, or evidence supports the result?
What should the next session read first?
```

This makes the template useful for many kinds of work:

- web apps, CLIs, desktop tools, and local utilities
- long-lived AI-generated or AI-assisted codebases
- documentation, SOP, and knowledge-base projects
- existing-code analysis and redesign
- projects with requirements, tests, evidence, and open issues
- multi-session Codex, Claude Code, Cursor, or agent workflows

## Use The Right Weight

Do not force the full workflow onto every task. Scale the environment to the
risk and expected lifetime of the work.

| Project shape | Recommended use |
| --- | --- |
| Small one-off task | Use only `AGENTS.md`, project profile, and open issues. |
| Normal app or tool | Add artifact inventory, decisions, tests, evidence, and trace candidates. |
| Long-lived project | Add importers, review reports, and optional execution-task tracking. |
| Regulated, SOP, ALM, or safety-related work | Use the full graph and keep formal approval outside this environment. |

The default rule:

```text
Execution queue carries the work.
The graph DB preserves why the work exists.
Formal ALM or SOP systems keep final authority.
```

## Quick Start

From this template directory:

```bash
python scripts/bootstrap_graph.py \
  --target-project /path/to/target-project \
  --project-name target-project
```

On Windows, the Python launcher works too:

```powershell
py -3 .\scripts\bootstrap_graph.py `
  --target-project "C:\path\to\target-project" `
  --project-name "target-project"
```

Then give an AI agent:

```text
Read AGENTS.md in this empty environment.
Read templates/agent_request.md.
Use the target project path from runtime/project_profile.local.json.
Build the engineering-memory pipeline and keep formal approval out of scope.
```

## Copy For A New Project

Use the cross-platform helper:

```bash
python scripts/create_instance.py \
  --destination /path/to/my-project-memory \
  --target-project /path/to/my-project \
  --project-name my-project
```

On Windows, you can also use the PowerShell helper:

```powershell
.\scripts\create_instance.ps1 `
  -Destination "C:\path\to\my-project-memory" `
  -TargetProject "C:\path\to\my-project" `
  -ProjectName "my-project"
```

The destination must be empty or absent. The script copies this template and
initializes a local graph DB.

## Checks

Cross-platform:

```bash
python scripts/bootstrap_graph.py --check
```

Windows helper:

```powershell
.\scripts\check_environment.ps1
py -3 .\scripts\bootstrap_graph.py --check
```
