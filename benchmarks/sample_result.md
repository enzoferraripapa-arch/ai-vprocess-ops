# Sample Regression Check Result

Scenario: fictional behavior-changing timeout update in a high-risk embedded controller.

Result: PASS

| Check | Value |
| --- | --- |
| Expected mandatory activities | `ACT-GATE, ACT-IMPACT, ACT-REGRESSION, ACT-TRACE` |
| Actual activities | `ACT-GATE, ACT-IMPACT, ACT-REGRESSION, ACT-TRACE` |
| Missing activities | `none` |
| Extra activities | `none` |
| Required open issues | `OI-001` |
| Missing open issues | `none` |
| Trace edges in report context | `12` |
| Recursive impact path reaches requirements/standards | `yes` |
| Human decision review recorded | `yes` |
| One-way handoff includes reviewed trace | `yes` |
| Export boundary present | `yes` |

Interpretation: this regression check only verifies the deterministic sample output. It does not prove compliance,
production readiness, or general performance on real projects.
