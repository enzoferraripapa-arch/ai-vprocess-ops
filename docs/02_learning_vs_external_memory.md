# Learning vs External Memory

This workflow is often misunderstood as "training the LLM."

That is not correct.

## Model Training

Model training changes model weights. It changes the behavior of the model
itself. It requires a training pipeline, training data, evaluation, deployment,
and lifecycle management for model versions.

## External Memory

External memory keeps model weights unchanged. The engineering data is stored in
a database. At runtime, the system retrieves relevant records and gives them to
the LLM as context.

## Practical Difference

```text
Training:
  The model remembers because its weights changed.

External memory:
  The database remembers. The model reads the database.
```

## Engineering Analogy

Training is closer to rebuilding a binary.

External memory is closer to running the same binary with structured config,
database state, logs, and documentation.

## Why This Matters

For regulated engineering work, external memory is easier to inspect, correct,
version, export, and audit than model weights. If a recommendation is wrong,
engineers can inspect the graph, the evidence, and the decision record. They do
not need to guess what the model learned internally.

