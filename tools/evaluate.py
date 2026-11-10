"""Compute deterministic metrics from labeled JSONL observations; never calls a model."""

import argparse
import json
import math
import statistics
from pathlib import Path


def summarize(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError('At least one observation is required')
    seen = set()
    exact, recall, reciprocal, abstention, latency, costs = [], [], [], [], [], []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Each observation must be an object')
        identifier = row.get('id')
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise ValueError('Every observation needs a unique nonempty string id')
        seen.add(identifier)
        for left, right in (('expected', 'actual'), ('relevant_ids', 'retrieved_ids'), ('should_abstain', 'abstained')):
            if (left in row) != (right in row):
                raise ValueError(f'{identifier}: supply both {left} and {right}')
        if 'expected' in row:
            exact.append(float(row['expected'] == row['actual']))
        if 'relevant_ids' in row:
            relevant, retrieved = row['relevant_ids'], row['retrieved_ids']
            if not isinstance(relevant, list) or not isinstance(retrieved, list) or not relevant:
                raise ValueError(f'{identifier}: retrieval labels need a nonempty relevant_ids list')
            if any(not isinstance(v, str) or not v for v in relevant + retrieved):
                raise ValueError(f'{identifier}: evidence IDs must be nonempty strings')
            gold = set(relevant)
            recall.append(len(gold & set(retrieved)) / len(gold))
            reciprocal.append(next((1 / rank for rank, value in enumerate(retrieved, 1) if value in gold), 0.0))
        if 'should_abstain' in row:
            if type(row['should_abstain']) is not bool or type(row['abstained']) is not bool:
                raise ValueError(f'{identifier}: abstention labels must be booleans')
            abstention.append(float(row['should_abstain'] == row['abstained']))
        for field, values in (('latency_ms', latency), ('cost_usd', costs)):
            if field in row:
                value = row[field]
                if type(value) not in {int, float} or not math.isfinite(value) or value < 0:
                    raise ValueError(f'{identifier}: {field} must be finite and nonnegative')
                values.append(value)

    def mean(values):
        return statistics.mean(values) if values else None

    return {'observations': len(rows), 'exact_match': mean(exact), 'recall_at_k': mean(recall),
            'mrr': mean(reciprocal), 'abstention_accuracy': mean(abstention),
            'latency_p50_ms': statistics.median(latency) if latency else None,
            'latency_p95_ms': sorted(latency)[math.ceil(0.95 * len(latency)) - 1] if latency else None,
            'reported_cost_usd': sum(costs) if costs else None,
            'coverage': {'exact_match': len(exact), 'retrieval': len(recall),
                         'abstention': len(abstention), 'latency': len(latency), 'cost': len(costs)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text(encoding='utf-8').splitlines() if line.strip()]
    report = json.dumps(summarize(rows), indent=2, allow_nan=False) + '\n'
    if args.output:
        args.output.write_text(report, encoding='utf-8')
    print(report, end='')


if __name__ == '__main__':
    main()
