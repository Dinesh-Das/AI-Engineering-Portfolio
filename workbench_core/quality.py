"""Objective CPU metrics and training checks; never manufacture model observations."""

import hashlib
import json
import math
import random
import statistics
import unicodedata

from .validation import validate_schema


def edit_distance(left, right):
    if len(left) * len(right) > 4_000_000:
        raise ValueError("Alignment budget exceeded; compare document pages/segments separately")
    if len(right) > len(left):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]


def text_quality(reference, prediction):
    if (
        not isinstance(reference, str)
        or not isinstance(prediction, str)
        or max(len(reference), len(prediction)) > 20000
    ):
        raise ValueError("Text metrics require strings below 20000 characters")
    reference = unicodedata.normalize("NFC", reference.replace("\r\n", "\n"))
    prediction = unicodedata.normalize("NFC", prediction.replace("\r\n", "\n"))
    words, predicted_words = reference.split(), prediction.split()
    characters = edit_distance(reference, prediction)
    word_errors = edit_distance(words, predicted_words)
    return {
        "exact_match": reference == prediction,
        "character_edits": characters,
        "word_edits": word_errors,
        "reference_characters": len(reference),
        "reference_words": len(words),
        "cer": characters / len(reference) if reference else 0.0 if not prediction else None,
        "wer": word_errors / len(words) if words else 0.0 if not predicted_words else None,
        "normalization": "NFC and CRLF-to-LF; WER splits Unicode whitespace",
        "empty_reference": not reference,
    }


def _box(box):
    if (
        not isinstance(box, list)
        or len(box) != 4
        or any(type(v) not in {int, float} or not 0 <= v <= 1e9 for v in box)
    ):
        raise ValueError("Boxes require four finite coordinates")
    if min(box) < 0 or box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError("Boxes require nonnegative coordinates and positive area")
    return box


def iou(left, right):
    a, b = _box(left), _box(right)
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0, min(a[3], b[3]) - max(a[1], b[1])
    )
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - intersection
    return intersection / union


def region_quality(reference, prediction, threshold=0.5, require_text=True):
    if (
        not isinstance(reference, list)
        or not isinstance(prediction, list)
        or max(len(reference), len(prediction)) > 200
    ):
        raise ValueError("Region lists may contain at most 200 entries")
    if type(threshold) not in {int, float} or not 0 < threshold <= 1:
        raise ValueError("IoU threshold must be between 0 and 1")
    for record in reference + prediction:
        if not isinstance(record, dict):
            raise ValueError("Region must be an object")
        _box(record.get("box"))
        if require_text and not isinstance(record.get("text"), str):
            raise ValueError("Region requires text")
    edges = [
        [
            j
            for j, candidate in enumerate(prediction)
            if iou(gold["box"], candidate["box"]) >= threshold
            and gold.get("label") == candidate.get("label")
            and (
                not require_text
                or unicodedata.normalize("NFC", gold["text"])
                == unicodedata.normalize("NFC", candidate["text"])
            )
        ]
        for gold in reference
    ]
    matches = {}

    def augment(index, visited):
        for target in edges[index]:
            if target in visited:
                continue
            visited.add(target)
            if target not in matches or augment(matches[target], visited):
                matches[target] = index
                return True
        return False

    for index in range(len(reference)):
        augment(index, set())
    true = len(matches)
    precision = true / len(prediction) if prediction else 1.0 if not reference else 0.0
    recall = true / len(reference) if reference else 1.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
        "matched": true,
        "false_positive": len(prediction) - true,
        "false_negative": len(reference) - true,
        "iou_threshold": threshold,
        "matching": "maximum-cardinality one-to-one; exact NFC text when enabled",
    }


def paired_comparison(rows, samples=500, seed=42):
    if (
        not isinstance(rows, list)
        or not 1 <= len(rows) <= 10000
        or type(samples) is not int
        or not 1 <= samples <= 2000
    ):
        raise ValueError("Invalid paired-evaluation size or sample budget")
    seen, differences = set(), []
    for row in rows:
        if (
            not isinstance(row, dict)
            or not isinstance(row.get("id"), str)
            or not row["id"]
            or row["id"] in seen
        ):
            raise ValueError("Paired cases require unique nonempty IDs")
        seen.add(row["id"])
        for key in ("baseline", "candidate"):
            if type(row.get(key)) not in {int, float} or not 0 <= row[key] <= 1:
                raise ValueError("Each paired score must be a finite number between 0 and 1")
        differences.append(row["candidate"] - row["baseline"])
    randomizer = random.Random(seed)
    bootstraps = sorted(
        statistics.mean(randomizer.choices(differences, k=len(differences))) for _ in range(samples)
    )
    return {
        "cases": len(rows),
        "mean_difference": statistics.mean(differences),
        "wins": sum(d > 0 for d in differences),
        "ties": differences.count(0),
        "losses": sum(d < 0 for d in differences),
        "bootstrap_95_interval": [
            bootstraps[int(0.025 * (samples - 1))],
            bootstraps[int(0.975 * (samples - 1))],
        ],
        "seed": seed,
        "resamples": samples,
        "scope": "paired supplied labels; no model or semantic judge was run",
    }


def _log_probabilities(logits, temperature):
    if (
        not isinstance(logits, list)
        or not 1 <= len(logits) <= 1000
        or any(type(v) not in {int, float} or not -1e6 <= v <= 1e6 for v in logits)
    ):
        raise ValueError("Logits must be bounded finite numeric lists")
    scaled = [value / temperature for value in logits]
    offset = max(scaled)
    normalizer = offset + math.log(sum(math.exp(value - offset) for value in scaled))
    return [value - normalizer for value in scaled]


def distillation_loss(teacher, student, target, temperature=2.0, alpha=0.5):
    if (
        type(temperature) not in {int, float}
        or not 0.01 <= temperature <= 100
        or type(alpha) not in {int, float}
        or not 0 <= alpha <= 1
    ):
        raise ValueError("Invalid temperature or loss weight")
    left, right = _log_probabilities(teacher, temperature), _log_probabilities(student, temperature)
    if len(left) != len(right) or type(target) is not int or not 0 <= target < len(left):
        raise ValueError("Teacher/student classes and target must agree")
    divergence = max(0.0, sum(math.exp(p) * (p - q) for p, q in zip(left, right))) * temperature**2
    hard_loss = -_log_probabilities(student, 1)[target]
    return {
        "kl_scaled": divergence,
        "hard_cross_entropy": hard_loss,
        "loss": alpha * divergence + (1 - alpha) * hard_loss,
    }


def data_leakage(splits):
    if not isinstance(splits, dict) or len(splits) < 2:
        raise ValueError("Supply at least two named dataset splits")
    hashes, groups, collisions = {}, {}, []
    for name, rows in splits.items():
        if not isinstance(rows, list) or len(rows) > 10000:
            raise ValueError("Dataset splits must be bounded lists")
        for row in rows:
            if not isinstance(row, dict) or "input" not in row:
                raise ValueError("Each dataset row needs an input field")
            digest = hashlib.sha256(
                json.dumps(
                    row["input"], sort_keys=True, ensure_ascii=False, allow_nan=False
                ).encode()
            ).hexdigest()
            if digest in hashes and hashes[digest] != name:
                collisions.append(
                    {"kind": "exact-input", "splits": [hashes[digest], name], "hash": digest}
                )
            hashes[digest] = name
            if "group" in row:
                group = hashlib.sha256(
                    json.dumps(row["group"], sort_keys=True, allow_nan=False).encode()
                ).hexdigest()
                if group in groups and groups[group] != name:
                    collisions.append(
                        {"kind": "source-group", "splits": [groups[group], name], "hash": group}
                    )
                groups[group] = name
    return {
        "leaks": collisions,
        "passed": not collisions,
        "scope": "exact input and supplied group identity; not semantic near-duplicate detection",
    }


def extraction_reward(prediction, expected, schema):
    if not isinstance(expected, dict):
        raise ValueError("Expected extraction must be an object")
    errors = validate_schema(prediction, schema)
    if errors or not isinstance(prediction, dict):
        return {"schema_valid": False, "field_accuracy": 0.0, "reward": 0.0, "errors": errors}
    correct = sum(
        key in prediction and type(prediction[key]) is type(value) and prediction[key] == value
        for key, value in expected.items()
    )
    accuracy = correct / len(expected) if expected else float(prediction == expected)
    return {"schema_valid": True, "field_accuracy": accuracy, "reward": accuracy, "errors": []}
