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
- Formal ALM export should wait until trace candidates are reviewed.
- An open issue should be raised if configuration authority is unclear.

## Pass Criteria

The method passes the first benchmark if it identifies the three mandatory
activities, links them to project facts, and produces reviewable rationale.

Run:

```bash
python benchmarks/run_sample_benchmark.py
```

Current deterministic sample result:

```text
Result: PASS
Expected mandatory activities: ACT-IMPACT, ACT-REGRESSION, ACT-TRACE
Required open issue: OI-001
Export boundary: present
```

## Fail Criteria

The method fails if it:

- Treats the change as documentation-only.
- Exports trace candidates as approved records.
- Omits regression selection.
- Copies proprietary standards text into the output.
