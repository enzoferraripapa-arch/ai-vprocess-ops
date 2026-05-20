# Publication Checklist

Use this checklist before copying the package to a public GitHub repository.

## Content Safety

- [ ] No real customer names.
- [ ] No real server names, IP addresses, tokens, or credentials.
- [ ] No proprietary requirements.
- [ ] No copyrighted standards text.
- [ ] No internal SOP text unless explicitly approved for publication.
- [ ] No export-controlled technical detail.

## Repository Readiness

- [ ] README explains that this is not model training.
- [ ] README explains that this is not an ALM replacement.
- [ ] Early docs explain that local accepted decisions and trace reviews are
  not formal approvals.
- [ ] Examples are fictional.
- [ ] Prototype runs without paid services.
- [ ] Generated demo DB files are ignored.
- [ ] Handoff exports are one-way and do not call vendor ALM APIs.
- [ ] If claiming platform coverage beyond GitHub-hosted Ubuntu CI, record the
  manual Windows or Dell Ubuntu validation command set used for the release.
  See [14_validation_log.md](14_validation_log.md) for the current format.
- [ ] License is selected before public release.
- [ ] Contribution rules are defined if external patches are expected.

## Suggested First Public Scope

Expected public scope:

```text
README.md
AGENTS.md
.github/
docs/
schema/
examples/
prototype/
tests/
tools/
benchmarks/
templates/empty_environment/
```

Do not publish private reference documents or local DB snapshots.
