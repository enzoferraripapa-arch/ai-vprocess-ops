# Cost Reduction Model

The cost reduction target is not "replace everything."

The target is to avoid paying enterprise-tool prices for work that can be
handled as structured reasoning before formal record management.

## Good Targets for Low-Cost AI + Graph Support

- V-process activity selection.
- Standards/SOP lookup and summarization.
- Review checklist generation.
- Trace candidate generation.
- Requirement gap detection.
- Change impact pre-analysis.
- Open issue classification.
- Decision rationale drafting.
- Trace review preparation.
- One-way handoff package generation for ALM entry.

## Poor Targets for Initial Replacement

- Legal approval.
- Electronic signatures.
- Formal baseline authority.
- Regulated workflow state.
- Enterprise identity and permissions.
- Customer-mandated ALM records.
- Vendor-supported audit packages.

## Decision Rule

Use low-cost AI + graph where the output is a candidate, draft, checklist, or
analysis. Accepted local review records can also be exported as a handoff
package when they carry reviewer, timestamp, and rationale.

Use formal ALM where the output becomes the official record.

## Measurement

Compare methods by evidence, not brand.

```text
Inputs:
  Same requirements, same standards summaries, same project profile.

Outputs:
  Activity recommendations, trace candidates, trace reviews, decision records,
  review questions, open issues, and one-way handoff packages.

Metrics:
  Correctness, missing items, false positives, explanation quality,
  review time, setup time, and total cost.
```

The repository's sample regression check is not a cost benchmark. It only
guards deterministic behavior for the fictional sample: expected activities,
impact paths, decision review state, trace handoff state, and export boundary.
