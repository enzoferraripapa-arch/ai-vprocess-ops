# Sample Assessment

This is a fictional example of how to judge the approach.

## Scenario

A behavior-changing software update modifies timeout handling in a high-risk
embedded controller. The team must decide whether to run a full V-process or a
bounded delta process.

## Expected Useful Output

- Change impact analysis is required.
- Trace candidate review is required.
- Regression test selection is required.
- Approval gate preparation is required when high risk and behavior-changing
  software update conditions are both true.
- Formal ALM export should wait until trace candidates are reviewed.
- An open issue should be raised if configuration authority is unclear.

## Pass Criteria

The sample regression check passes if it identifies the mandatory activities,
links them to project facts, and produces reviewable rationale.

Run:

```bash
python benchmarks/run_sample_regression.py
```

Current deterministic sample result:

```text
Result: PASS
Expected mandatory activities: ACT-GATE, ACT-IMPACT, ACT-REGRESSION, ACT-TRACE
Required open issue: OI-001
Recursive impact path: CR-001 reaches affected requirements and standards
Export boundary: present
```

## Fail Criteria

The method fails if it:

- Treats the change as documentation-only.
- Exports trace candidates as approved records.
- Omits approval gate preparation for the high-risk behavior change.
- Omits regression selection.
- Copies proprietary standards text into the output.
