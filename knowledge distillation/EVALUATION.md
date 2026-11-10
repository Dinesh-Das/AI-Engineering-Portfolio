# Evaluation protocol: knowledge distillation

## Hypothesis

Sweep temperature and teacher-loss weight with a fixed data split; report accuracy, parameter count and CPU inference time.

## Dataset and cases

Create a small versioned development set and a separate holdout. Include successful inputs, unanswerable/unsupported requests, malformed inputs, conflicting evidence, cross-user boundaries where relevant, and a simulated dependency timeout. Keep original documents, media timestamps, graph facts or executable expected results as ground truth.

## Metrics

Held-out task accuracy; schema/format validity separately from semantic correctness; per-class metrics where relevant; training cost; peak memory; exported-model latency and regression rates.

The collection's `tools.evaluate` helper computes exact answer match, retrieval recall/MRR, abstention accuracy and latency/cost summaries from observations you supply. It does not call a model, grade prose semantically or manufacture results. Use task-specific metrics in addition: executable tests for code, field-level matching for extraction, WER/diarization for audio, and held-out accuracy/AP for training.

## Run record

For every case record: case ID, dataset version, source revision, model/provider revision, prompt/tool settings, expected evidence/outcome, actual evidence/outcome, elapsed milliseconds and cost if known. Keep missing metrics missing; never treat absent labels as a perfect score.

Use `python -m tools.evaluate --input observations.jsonl` from the collection root. See [metric format](../docs/EVALUATION_FORMAT.md).

## Passing decision

Choose quality and cost/latency limits before observing the candidate results. Compare with a frozen baseline, inspect the worst failures and test repeated runs for nondeterministic output. Judge-based grading should be blinded and calibrated on an independently reviewed anchor set. Syntax/integrity checks establish source health only; they do not pass this quality evaluation.

Status at import: no live model observations, no GPU training result and no production benchmark reproduced.
