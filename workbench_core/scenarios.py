"""Executable, deterministic experiments bound to each project's actual learning goal.

These exercise CPU reference behavior; they are not canned model completions.
"""

import sqlite3
import tempfile
import time
from contextlib import closing
from pathlib import Path

from .artifacts import manifest
from .contracts import ToolRegistry, stream_state
from .evidence import EvidenceIndex
from .quality import (
    data_leakage,
    distillation_loss,
    extraction_reward,
    paired_comparison,
    region_quality,
    text_quality,
)
from .safety import arithmetic
from .state import StateStore
from .validation import readonly_query, validate_schema


def require(condition, message="Observed behavior differs from the expected contract"):
    if not condition:
        raise AssertionError(message)


def rejected(function, exception=ValueError):
    try:
        function()
    except exception:
        return
    raise AssertionError("Invalid operation was accepted")


def checks(profile):
    family = profile["family"]
    fixture = profile["fixture"]
    results = []

    def case(name, function):
        started = time.perf_counter()
        try:
            function()
            results.append(
                {
                    "name": name,
                    "passed": True,
                    "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
                }
            )
        except (ValueError, PermissionError, OSError, AssertionError, KeyError, TypeError) as error:
            results.append({"name": name, "passed": False, "error": str(error)})

    with tempfile.TemporaryDirectory(prefix="ai-project-lab-") as directory:
        root = Path(directory)
        if family == "retrieval":
            index = EvidenceIndex(fixture["documents"])
            case(
                "supporting-evidence-retains-source",
                lambda: require(index.search(fixture["query"], "learner")[0]["id"] == "support"),
            )
            case(
                "cross-tenant-evidence-is-excluded",
                lambda: require(index.search("confidential", "learner") == []),
            )
            case(
                "missing-evidence-abstains",
                lambda: require(index.search("zxqvnotincorpus", "learner") == []),
            )
            case(
                "context-budget-is-enforced",
                lambda: require(
                    sum(
                        len(d["text"])
                        for d in index.search(fixture["query"], "learner", context_chars=25)
                    )
                    <= 25
                ),
            )
            index.save(root / "index.json")
            case(
                "index-persists-content-hashes-and-source",
                lambda: require(
                    EvidenceIndex.load(root / "index.json").search(fixture["query"], "learner")[0][
                        "source"
                    ]
                    == fixture["documents"][0]["source"]
                ),
            )
            case(
                "invalid-retrieval-limit-is-rejected",
                lambda: rejected(lambda: index.search("x", "learner", k=0)),
            )
        elif family in {"workflow", "memory"}:
            path = root / "state.sqlite"
            if family == "workflow":
                with StateStore(path) as store:
                    case(
                        "run-created-once",
                        lambda: require(
                            store.create_job("experiment", "learner", fixture["payload"])
                        ),
                    )
                    case(
                        "duplicate-delivery-is-idempotent",
                        lambda: require(
                            not store.create_job("experiment", "learner", fixture["payload"])
                        ),
                    )
                    case(
                        "conflicting-idempotency-payload-is-rejected",
                        lambda: rejected(
                            lambda: store.create_job("experiment", "learner", {"changed": True})
                        ),
                    )
                    case(
                        "another-owner-cannot-read-run",
                        lambda: rejected(lambda: store.job("experiment", "other"), PermissionError),
                    )
                    store.transition("experiment", "learner", "running")
                with StateStore(path) as resumed:
                    case(
                        "restart-retains-running-state",
                        lambda: require(
                            resumed.job("experiment", "learner")["status"] == "running"
                        ),
                    )
                    resumed.transition("experiment", "learner", "failed")
                    resumed.transition("experiment", "learner", "running")
                    resumed.transition("experiment", "learner", "completed")
                    case(
                        "completed-job-cannot-reexecute",
                        lambda: rejected(
                            lambda: resumed.transition("experiment", "learner", "running")
                        ),
                    )
            else:
                with StateStore(path) as store:
                    store.remember("learner", fixture["key"], fixture["old_value"], now=10, ttl=10)
                    store.remember("learner", fixture["key"], fixture["new_value"], now=11, ttl=10)
                    case(
                        "correction-replaces-old-fact",
                        lambda: require(
                            store.recall("learner", fixture["key"], now=12)["value"]
                            == fixture["new_value"]
                        ),
                    )
                    case(
                        "another-user-cannot-recall-fact",
                        lambda: require(store.recall("other", fixture["key"], now=12) is None),
                    )
                    case(
                        "expired-fact-is-not-returned",
                        lambda: require(store.recall("learner", fixture["key"], now=22) is None),
                    )
                with StateStore(path) as resumed:
                    case(
                        "memory-version-survives-restart",
                        lambda: require(
                            resumed.recall("learner", fixture["key"], now=12)["version"] == 2
                        ),
                    )
                    resumed.forget("learner", fixture["key"])
                    case(
                        "deletion-removes-fact",
                        lambda: require(resumed.recall("learner", fixture["key"], now=12) is None),
                    )
        elif family == "tools":
            registry = ToolRegistry()
            schema = {
                "type": "object",
                "properties": {"expression": {"type": "string", "maxLength": 500}},
                "required": ["expression"],
                "additionalProperties": False,
            }
            registry.register(fixture["tool_name"], schema, arithmetic)
            case(
                "typed-tool-call-executes-allowed-operation",
                lambda: require(
                    registry.call(fixture["tool_name"], {"expression": "37*3+19*2"}) == 149
                ),
            )
            case(
                "extra-tool-arguments-rejected",
                lambda: rejected(
                    lambda: registry.call(fixture["tool_name"], {"expression": "1", "shell": True})
                ),
            )
            case(
                "python-execution-is-not-a-calculator-operation",
                lambda: rejected(
                    lambda: registry.call(
                        fixture["tool_name"], {"expression": "__import__('os').getcwd()"}
                    )
                ),
            )
            registry.register(
                "write_artifact",
                {"type": "object", "additionalProperties": False},
                lambda: "written",
                write=True,
            )
            case(
                "unauthorized-write-is-rejected",
                lambda: rejected(lambda: registry.call("write_artifact", {}), PermissionError),
            )
            case("unknown-tool-is-rejected", lambda: rejected(lambda: registry.call("unknown", {})))
        elif family == "sql":
            path = root / "fixture.sqlite"
            with closing(sqlite3.connect(path)) as connection:
                connection.execute("CREATE TABLE evidence (name TEXT, value INTEGER)")
                connection.executemany(
                    "INSERT INTO evidence VALUES (?,?)",
                    [(fixture["row_name"], 375), ("other", 900)],
                )
                connection.commit()
            case(
                "parameterized-read-returns-ground-truth",
                lambda: require(
                    readonly_query(
                        path, "SELECT value FROM evidence WHERE name=?", [fixture["row_name"]]
                    )["rows"]
                    == [[375]]
                ),
            )
            case(
                "write-statement-is-rejected",
                lambda: rejected(lambda: readonly_query(path, "DELETE FROM evidence")),
            )
            case(
                "attachment-is-rejected",
                lambda: rejected(
                    lambda: readonly_query(path, "ATTACH DATABASE ':memory:' AS injected")
                ),
            )
            case(
                "result-limit-is-explicit",
                lambda: require(
                    readonly_query(path, "SELECT * FROM evidence", max_rows=1)["truncated"]
                ),
            )
            case(
                "query-values-do-not-become-sql",
                lambda: require(
                    readonly_query(
                        path, "SELECT value FROM evidence WHERE name=?", ["' OR 1=1 --"]
                    )["rows"]
                    == []
                ),
            )
        elif family in {"ocr", "transcript"}:
            gold = fixture["reference"]
            case(
                "exact-text-has-zero-edit-errors",
                lambda: require(text_quality(gold, gold)["cer"] == 0),
            )
            case(
                "corrupted-text-has-observable-error",
                lambda: require(text_quality(gold, fixture["prediction"])["character_edits"] > 0),
            )
            case(
                "unicode-canonical-equivalence-is-controlled",
                lambda: require(text_quality("café", "cafe\u0301")["cer"] == 0),
            )
            case(
                "empty-reference-does-not-create-perfect-score",
                lambda: require(text_quality("", "invented")["cer"] is None),
            )
            regions = [{"box": [0, 0, 100, 20], "text": fixture["region_text"]}]
            case(
                "duplicate-regions-cannot-inflate-recall",
                lambda: require(region_quality(regions, regions + regions)["precision"] == 0.5),
            )
            case(
                "invalid-region-is-rejected",
                lambda: rejected(
                    lambda: region_quality(regions, [{"box": [10, 10, 0, 0], "text": "x"}])
                ),
            )
        elif family in {"extraction", "training"}:
            schema, expected = fixture["schema"], fixture["expected"]
            case(
                "correct-extraction-meets-schema-and-ground-truth",
                lambda: require(extraction_reward(expected, expected, schema)["reward"] == 1),
            )
            wrong = {**expected, fixture["target_field"]: fixture["wrong_value"]}
            case(
                "schema-valid-wrong-answer-is-not-full-reward",
                lambda: require(extraction_reward(wrong, expected, schema)["reward"] < 1),
            )
            case(
                "unknown-fields-are-rejected",
                lambda: require(bool(validate_schema({**expected, "unexpected": 1}, schema))),
            )
            case(
                "missing-required-field-is-rejected",
                lambda: require(bool(validate_schema({}, schema))),
            )
            case(
                "cross-split-source-leakage-is-detected",
                lambda: require(
                    not data_leakage(
                        {
                            "train": [{"input": "a", "group": "source-1"}],
                            "test": [{"input": "b", "group": "source-1"}],
                        }
                    )["passed"]
                ),
            )
            if profile.get("variant") == "distillation":
                case(
                    "identical-teacher-student-has-zero-kl",
                    lambda: require(
                        abs(distillation_loss([1000, 999], [1000, 999], 0, alpha=1)["kl_scaled"])
                        < 1e-10
                    ),
                )
            if profile.get("variant") == "detection":
                reference = [{"box": [0, 0, 20, 20], "label": "invoice"}]
                case(
                    "wrong-class-is-not-a-detection-match",
                    lambda: require(
                        region_quality(
                            reference,
                            [{"box": [0, 0, 20, 20], "label": "other"}],
                            require_text=False,
                        )["matched"]
                        == 0
                    ),
                )
        elif family == "evaluation":
            case(
                "paired-effect-uses-the-same-cases",
                lambda: require(paired_comparison(fixture["pairs"])["mean_difference"] == 0.5),
            )
            case(
                "missing-candidate-label-is-rejected",
                lambda: rejected(lambda: paired_comparison([{"id": "a", "baseline": 1}])),
            )
            case(
                "duplicate-case-ids-are-rejected",
                lambda: rejected(lambda: paired_comparison([fixture["pairs"][0]] * 2)),
            )
            case(
                "nonfinite-scores-are-rejected",
                lambda: rejected(
                    lambda: paired_comparison(
                        [{"id": "a", "baseline": 0, "candidate": float("nan")}]
                    )
                ),
            )
            case(
                "bootstrap-is-reproducible",
                lambda: require(
                    paired_comparison(fixture["pairs"]) == paired_comparison(fixture["pairs"])
                ),
            )
        elif family == "streaming":
            start = {"type": "start", "fixture": True}
            delta = {"type": "delta", "channel": "answer", "text": fixture["answer"]}
            case(
                "complete-answer-can-enter-history",
                lambda: require(
                    stream_state([start, delta, {"type": "done"}])["can_commit_history"]
                ),
            )
            case(
                "interrupted-answer-cannot-enter-history",
                lambda: require(not stream_state([start, delta])["can_commit_history"]),
            )
            case(
                "failed-answer-cannot-enter-history",
                lambda: require(
                    not stream_state([start, delta, {"type": "error"}])["can_commit_history"]
                ),
            )
            case(
                "empty-final-answer-cannot-enter-history",
                lambda: require(not stream_state([start, {"type": "done"}])["can_commit_history"]),
            )
            case(
                "post-completion-delta-is-rejected",
                lambda: rejected(lambda: stream_state([start, {"type": "done"}, delta])),
            )
            case(
                "trace-is-not-final-answer",
                lambda: require(
                    not stream_state(
                        [
                            start,
                            {"type": "delta", "channel": "thinking", "text": "trace"},
                            {"type": "done"},
                        ]
                    )["can_commit_history"]
                ),
            )
        elif family == "artifacts":
            (root / "segment.txt").write_text(fixture["content"], encoding="utf-8")
            records = [{"id": fixture["artifact_id"], "path": "segment.txt"}]
            case(
                "complete-artifact-has-content-hash",
                lambda: require(len(manifest(root, records)["artifacts"][0]["sha256"]) == 64),
            )
            case(
                "duplicate-artifact-id-is-rejected",
                lambda: rejected(lambda: manifest(root, records * 2)),
            )
            case(
                "path-traversal-is-rejected",
                lambda: rejected(lambda: manifest(root, [{"id": "x", "path": "../outside"}])),
            )
            case(
                "wrong-content-hash-is-rejected",
                lambda: rejected(lambda: manifest(root, [{**records[0], "sha256": "0" * 64}])),
            )
            (root / "empty.txt").touch()
            case(
                "empty-artifact-is-rejected",
                lambda: rejected(lambda: manifest(root, [{"id": "empty", "path": "empty.txt"}])),
            )
        else:
            raise ValueError("Unknown enhancement family: " + str(family))
    return {
        "project": profile["project_id"],
        "family": family,
        "objective": profile["purpose"],
        "passed": bool(results) and all(r["passed"] for r in results),
        "checks": results,
        "evidence_scope": "executable CPU reference/contract checks on declared synthetic fixtures",
        "live_model_executed": False,
        "original_application_verified": False,
    }
