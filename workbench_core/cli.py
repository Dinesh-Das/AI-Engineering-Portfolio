"""Per-project executable enhancement commands. Model-free unless using original apps."""

import argparse
import json
import sys
from pathlib import Path

from .artifacts import manifest
from .contracts import stream_state
from .doctor import inspect
from .evidence import EvidenceIndex
from .io import read_json, write_json
from .quality import (
    data_leakage,
    distillation_loss,
    extraction_reward,
    paired_comparison,
    region_quality,
    text_quality,
)
from .scenarios import checks
from .state import StateStore
from .validation import readonly_query, validate_schema


def main(project_root=None, argv=None):
    root = Path(project_root or Path.cwd()).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command")
    for name in ("check", "doctor"):
        command = commands.add_parser(name)
        command.add_argument("--output", type=Path)
    search = commands.add_parser(
        "search", help="Search an actual local JSON document corpus or saved CPU index"
    )
    source = search.add_mutually_exclusive_group(required=True)
    source.add_argument("--documents", type=Path)
    source.add_argument("--index", type=Path)
    search.add_argument("--save-index", type=Path)
    search.add_argument("--query", required=True)
    search.add_argument("--tenant", required=True)
    search.add_argument("--k", type=int, default=5)
    search.add_argument("--context-chars", type=int, default=4000)
    for name in ("quality", "compare", "schema", "reward", "dataset", "distill", "stream-check"):
        command = commands.add_parser(name)
        command.add_argument("--input", type=Path, required=True)
        command.add_argument("--output", type=Path)
    sql = commands.add_parser("query-sql")
    sql.add_argument("--database", type=Path, required=True)
    sql.add_argument("--sql", required=True)
    sql.add_argument("--parameters", default="[]")
    sql.add_argument("--max-rows", type=int, default=100)
    artifact = commands.add_parser("artifacts")
    artifact.add_argument("--directory", type=Path, required=True)
    artifact.add_argument(
        "--input",
        type=Path,
        required=True,
        help="JSON list of expected artifact IDs/paths/checksums",
    )
    job = commands.add_parser("job")
    job.add_argument("--state", type=Path, required=True)
    job.add_argument("--owner", required=True)
    job.add_argument("--id", required=True)
    job.add_argument(
        "--operation",
        choices=("create", "show", "running", "failed", "completed", "cancelled"),
        required=True,
    )
    job.add_argument("--input", type=Path)
    memory = commands.add_parser("memory")
    memory.add_argument("--state", type=Path, required=True)
    memory.add_argument("--owner", required=True)
    memory.add_argument("--key", required=True)
    memory.add_argument("--operation", choices=("remember", "recall", "forget"), required=True)
    memory.add_argument("--input", type=Path)
    memory.add_argument("--ttl", type=float)
    args = parser.parse_args(argv)
    command = args.command or "check"
    try:
        if command == "check":
            result = checks(read_json(root / "enhancement/profile.json"))
        elif command == "doctor":
            result = inspect(root)
        elif command == "search":
            index = (
                EvidenceIndex(read_json(args.documents))
                if args.documents
                else EvidenceIndex.load(args.index)
            )
            result = {
                "evidence": index.search(args.query, args.tenant, args.k, args.context_chars),
                "retrieval": "lexical-bm25-reference",
                "model_executed": False,
            }
            result["abstain"] = not result["evidence"]
            if args.save_index:
                index.save(args.save_index)
        elif command == "quality":
            data = read_json(args.input)
            result = text_quality(data["reference"], data["prediction"])
            if "reference_regions" in data or "prediction_regions" in data:
                result["regions"] = region_quality(
                    data["reference_regions"], data["prediction_regions"]
                )
        elif command == "compare":
            result = paired_comparison(read_json(args.input))
        elif command == "schema":
            data = read_json(args.input)
            errors = validate_schema(data["value"], data["schema"])
            result = {
                "valid": not errors,
                "errors": errors,
                "scope": "explicit supported schema subset",
            }
        elif command == "reward":
            data = read_json(args.input)
            result = extraction_reward(data["prediction"], data["expected"], data["schema"])
        elif command == "dataset":
            result = data_leakage(read_json(args.input))
        elif command == "distill":
            data = read_json(args.input)
            result = distillation_loss(
                data["teacher"],
                data["student"],
                data["target"],
                data.get("temperature", 2),
                data.get("alpha", 0.5),
            )
        elif command == "stream-check":
            result = stream_state(read_json(args.input))
        elif command == "query-sql":
            result = readonly_query(
                args.database, args.sql, json.loads(args.parameters), args.max_rows
            )
        elif command == "artifacts":
            result = manifest(args.directory, read_json(args.input))
        elif command == "job":
            with StateStore(args.state) as store:
                if args.operation == "create":
                    if not args.input:
                        raise ValueError("--input is required to create a job")
                    created = store.create_job(args.id, args.owner, read_json(args.input))
                    result = {"created": created, "job": store.job(args.id, args.owner)}
                elif args.operation == "show":
                    result = store.job(args.id, args.owner)
                else:
                    result = store.transition(args.id, args.owner, args.operation)
        elif command == "memory":
            with StateStore(args.state) as store:
                if args.operation == "remember":
                    if not args.input:
                        raise ValueError("--input is required to remember a value")
                    store.remember(args.owner, args.key, read_json(args.input), ttl=args.ttl)
                    result = store.recall(args.owner, args.key)
                elif args.operation == "recall":
                    result = store.recall(args.owner, args.key)
                else:
                    store.forget(args.owner, args.key)
                    result = {"deleted": True}
        else:
            raise ValueError("Unknown command")
        if getattr(args, "output", None):
            write_json(args.output, result)
        print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
        if command == "check" and not result["passed"]:
            return 1
        if command == "schema" and not result["valid"]:
            return 1
        if command == "dataset" and not result["passed"]:
            return 1
        return 0
    except (ValueError, TypeError, KeyError, OSError, PermissionError, RecursionError) as error:
        print(json.dumps({"error": str(error), "command": command}), file=sys.stderr)
        return 2
