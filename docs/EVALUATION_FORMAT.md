# Offline observation metrics

`python -m tools.evaluate --input observations.jsonl` accepts one JSON object per line. It computes metrics only for supplied labels and reports coverage, so unlabeled observations cannot create a perfect score.

| Field | Meaning |
| --- | --- |
| `id` | Required unique nonempty case ID |
| `expected`, `actual` | Optional pair; exact JSON/Python-value equality, without semantic grading |
| `relevant_ids`, `retrieved_ids` | Optional pair of string lists; relevant IDs must be nonempty; recall uses unique IDs, MRR uses the first relevant result's position |
| `should_abstain`, `abstained` | Optional pair of actual JSON booleans |
| `latency_ms` | Optional finite nonnegative observed duration |
| `cost_usd` | Optional finite nonnegative observed cost |

Missing pairs, duplicate IDs, invalid types, NaN and negative duration/cost values fail validation. Empty datasets are rejected. Retrieval metrics average over labeled cases; if result-list lengths differ, report those lengths and do not imply one common k. P50 uses the median; p95 uses the nearest-rank definition. Reported cost sums only observations with a cost field.

```json
{"id":"case-1","expected":"42","actual":"42","relevant_ids":["doc-a"],"retrieved_ids":["doc-b","doc-a"],"should_abstain":false,"abstained":false,"latency_ms":120,"cost_usd":0.001}
```

The helper does not compute factuality, WER, AP, code pass rates or statistical confidence intervals. Use the project-specific protocol for those. An exact textual match is useful for deterministic labels; it is not an appropriate sole metric for open-ended prose.
