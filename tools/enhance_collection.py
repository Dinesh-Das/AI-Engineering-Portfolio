"""Build source-specific executable learning extensions without touching user journals."""

import csv
import hashlib
import json
import re
import tomllib
from pathlib import Path

from .analysis import analyze_project

ROOT = Path(__file__).resolve().parents[1]
OCR = ("Latex-OCR-Lama", "gemma3-ocr", "llama-ocr", "qwen-2.5VL-ocr")
OCR_NOTES = {
    "Latex-OCR-Lama": {
        "category": "ocr",
        "purpose": "Measure faithful equation transcription from the preserved LaTeX OCR demo.",
        "mechanism": "The original Streamlit app sends equation image bytes to local Ollama llama3.2-vision, retains the LaTeX in session state and renders it. Its existing characterization tests preserve upstream behavior, including known state limitations.",
        "experiment": "Compare an independently transcribed equation against model LaTeX. Test spacing, missing subscripts and changed signs separately; text edit distance cannot decide mathematical equivalence.",
        "production": "Validate and normalize image uploads before an isolated inference job; bind source hash and model/prompt version to each result. Invalidate results on source changes, limit image/pixel/token budgets and render untrusted LaTeX with a restricted renderer. Preserve source and normalized scoring separately.",
    },
    "gemma3-ocr": {
        "category": "ocr",
        "purpose": "Evaluate Gemma faithful transcription separately from prompted Markdown formatting.",
        "mechanism": "The redesigned Streamlit workspace validates images in ocr.py, checks an installed local Ollama Gemma model and binds session output to source/model/mode. No cloud backend or automatic model download is part of the app flow.",
        "experiment": "Hold the page and Gemma revision fixed; compare faithful mode against structured Markdown using separate text references. Measure digit/name errors, service failures and stale-result invalidation independently.",
        "production": "Keep uploaded content in session memory, preserve local-only inference policy and disable telemetry. Move bounded image inference behind authenticated per-user jobs only if sharing the app; protect source/model identity, queue limits and explicit service failure recovery.",
    },
    "llama-ocr": {
        "category": "ocr",
        "purpose": "Measure page-level OCR quality across the local batch/PDF vision workbench.",
        "mechanism": "The rebuilt app normalizes image/PDF inputs in workbench/documents.py, chooses task-specific prompts and uses an installed local Ollama vision model through its bounded client. Batch/page results can be exported.",
        "experiment": "Label individual PDF pages before batching; compare the same pages across installed vision models. Aggregate character edit counts over reference characters rather than averaging page CER, and retain failed/empty pages.",
        "production": "Isolate PDF rendering and inference workers, cap pages/pixels/bytes and GPU concurrency, and track per-page terminal state. Encrypt retained documents and exports, reconcile interrupted batches by page identity and evaluate failed pages explicitly instead of silently dropping them.",
    },
    "qwen-2.5VL-ocr": {
        "category": "ocr",
        "purpose": "Evaluate Qwen page transcription and grounded text-region detection independently.",
        "mechanism": "qwen_ocr/core.py normalizes image and grounding output; backends.py selects local Transformers or explicitly configured DashScope inference. The app can extract a page or locate lines; the CPU extension loads neither backend.",
        "experiment": "Pair each human text region with a box in the same normalized pixel coordinate space. Compare local and opted-in cloud outputs on held-out pages; vary IoU and text equality separately and include duplicate/missed lines.",
        "production": "Separate CPU image normalization from model workers, pin model/processor revisions and preserve coordinate transforms. Require explicit cloud processing authorization, keep provider credentials outside source, bound image/token/concurrency costs and monitor text plus region recall per document type.",
    },
}
FAMILIES = {
    "rag": "retrieval",
    "retrieval": "retrieval",
    "agents": "workflow",
    "memory": "memory",
    "mcp": "tools",
    "training": "training",
    "structured": "extraction",
    "evaluation": "evaluation",
    "voice": "transcript",
    "interfaces": "streaming",
    "media": "artifacts",
    "operations": "artifacts",
    "recipe": "artifacts",
    "ocr": "ocr",
}
OVERRIDES = {
    "graphiti-mcp": "memory",
    "mindsdb-mcp": "sql",
    "sales-analytics-agent": "sql",
    "llamaindex-mcp": "sql",
    "art_mcp_rl": "sql",
}
FEATURES = {
    "retrieval": (
        "Persistent evidence retrieval",
        "A bounded lexical BM25 reference ranks only documents in the requested tenant, retains source IDs and SHA-256 content hashes, persists a versioned index, and returns no evidence for unmatched terms.",
        "Token overlap cannot establish semantic answerability. This is a CPU baseline beside the original embedding/reranking pipeline; it does not replace its provider or synthesize answers.",
        "Compare lexical and original retrieval on the same labeled questions. Record supporting-source recall, ranking changes and abstention errors before comparing answer fluency.",
    ),
    "workflow": (
        "Durable workflow state",
        "SQLite transactions persist a run ID, owner, payload hash, state and version. Duplicate creation is idempotent, conflicting payloads are rejected, restarts retain state, and completed runs cannot transition back to running.",
        "This protects local state transitions. Exactly-once external side effects require provider idempotency or an outbox, worker leases and reconciliation; this is not a distributed job scheduler.",
        "Kill a worker between tool completion and state update. Explain which external effect could repeat and design its idempotency key before retrying.",
    ),
    "memory": (
        "Scoped, correctable memory",
        "SQLite stores values under an owner/key pair with versions, optional expiry, correction, explicit deletion and restart persistence.",
        "Owner strings supplied on a CLI are trusted local inputs, not authentication. Production identity must come from verified sessions. Expired values are hidden from reads but require a retention/purge job for physical deletion.",
        "Correct one fact, restart, read as a second owner, then delete it. Explain how expiry, backup retention and deletion of vector/graph copies differ.",
    ),
    "tools": (
        "Typed and authorized tool boundary",
        "An allowlisted registry validates a strict documented JSON-schema subset before calling a tool. Arithmetic uses a bounded AST interpreter; write tools require explicit application authorization.",
        "The registry is a local adapter, not a full MCP server or a sandbox. A registered network/shell tool still needs its own destination, credential, timeout and resource policy.",
        "Send extra arguments, a Python expression and an unauthorized write. Trace which boundary rejects each and why model instructions cannot grant permissions.",
    ),
    "sql": (
        "Bounded read-only SQL",
        "SQLite opens an existing database in read-only URI mode, applies an authorizer that denies writes and attachment, binds parameters, limits rows and interrupts excessive work.",
        "This is a SQLite reference adapter. It is not an authorization layer for the original remote database, nor a guarantee against inference from permitted data. Views and credentials must enforce tenant access.",
        "Try a write, database attachment and an injection string passed as a value. Then use a database view that exposes only one tenant and explain why read-only alone is insufficient.",
    ),
    "ocr": (
        "Objective OCR quality",
        "NFC-normalized character and word edit distance expose transcription errors. Optional region scoring uses IoU and maximum-cardinality one-to-one matching with exact text, so duplicate boxes cannot inflate recall.",
        "No image or model is loaded. CER/WER require independently transcribed references; Markdown/LaTeX syntax differences can dominate the score. Formula equivalence, layout quality and hallucination need separate labels.",
        "Transcribe a held-out page by hand; compare raw transcription and formatted output separately. Introduce one digit error and one duplicate region; retain counts as well as rates.",
    ),
    "transcript": (
        "Objective transcript comparison",
        "NFC-normalized character and whitespace-token word edit distance compare supplied reference and predicted transcripts, with explicit empty-reference handling and optional region matching.",
        "No speech model, diarization or audio decoder is executed. These metrics do not measure timing, speaker identity, synthesis naturalness or word alignment.",
        "Use a human transcript with names and numbers. Compare WER with task-critical token errors; assess speaker/timestamp and synthesized-audio quality independently.",
    ),
    "extraction": (
        "Schema and semantic accuracy",
        "A strict schema subset validates output shape, while independently supplied expected fields determine exact field accuracy. Valid JSON with incorrect facts cannot earn full reward. Split audits flag identical inputs and shared source groups.",
        "Exact field equality is intentionally strict. It is not a semantic judge, a general JSON Schema engine or proof that the expected labels are correct.",
        "Create a schema-valid wrong amount and a correct value with an extra key. Explain why format rewards alone can train the wrong behavior.",
    ),
    "training": (
        "Training data and reward checks",
        "Deterministic schema/field rewards and exact-input/source-group split checks expose reward shortcuts and leakage before expensive training. Distillation profiles also include stable temperature-scaled KL and cross-entropy; detection profiles check class-aware region matches.",
        "No optimizer, gradient, GPU training or convergence claim is made. Source-group checks depend on trustworthy group labels and do not detect semantic near duplicates.",
        "Split by source before transforming examples. Compare format reward with correctness reward; hold out sources and record teacher/student or detector quality separately from the CPU checks.",
    ),
    "evaluation": (
        "Paired evaluation with uncertainty",
        "Unique supplied case IDs bind baseline and candidate scores. The evaluator rejects missing/nonfinite scores and reports paired mean improvement, wins/ties/losses and a reproducible seeded bootstrap interval.",
        "It computes from supplied labels and does not run a model or an LLM judge. Tiny fixtures illustrate mechanics; correlated cases and small samples invalidate strong population claims.",
        "Label the same held-out inputs for both versions before inspecting aggregate scores. Compare confidence intervals by source group and report regressions as well as the mean.",
    ),
    "streaming": (
        "Explicit stream lifecycle",
        "A stream-event validator distinguishes accepted start, answer/thinking deltas, interruption, failure and successful completion. Only a completed nonempty answer is eligible for history; post-terminal events are rejected.",
        "The validator accepts captured events. It does not invent token timing or authenticate provider traces. The separate learning UI has its own real-browser validation and live Ollama transport.",
        "Capture a completed, stopped and failed stream. Compare the visible partial text with the next model history; explain why traces are neither final answers nor correctness evidence.",
    ),
    "artifacts": (
        "Bounded artifact integrity",
        "A manifest validates declared IDs, relative paths, nonempty files, byte budgets and SHA-256 content hashes. It rejects traversal, escaping symlinks, duplicates and checksum mismatches.",
        "Completeness means every declared file exists. It does not discover undeclared required files or assess video/audio codecs, synchronization, architecture quality or external deployments.",
        "Remove one declared output, duplicate an ID and alter one byte. Separate artifact transport failures from the original model or deployment quality.",
    ),
}
LAUNCHER = '''"""Run this project's executable learning extension from the collection checkout."""

import importlib
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent
    collection_root = project_root.parent
    if not (collection_root / "workbench_core" / "cli.py").is_file():
        raise SystemExit("Keep this folder beside workbench_core in the AI Projects checkout.")
    sys.path.insert(0, str(collection_root))
    return importlib.import_module("workbench_core.cli").main(project_root=project_root)


if __name__ == "__main__":
    raise SystemExit(main())
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def fixture_for(identifier, family, note):
    if family == "retrieval":
        return {
            "query": identifier + " retention",
            "documents": [
                {
                    "id": "support",
                    "tenant": "learner",
                    "source": identifier + "/synthetic-policy-v1",
                    "text": f"{identifier} retention policy: learner documents are retained for seven days. This is synthetic evidence.",
                },
                {
                    "id": "distractor",
                    "tenant": "learner",
                    "source": identifier + "/synthetic-other",
                    "text": "A synthetic unrelated recipe uses water and flour.",
                },
                {
                    "id": "private",
                    "tenant": "other",
                    "source": "private-policy",
                    "text": "confidential retention is ninety days.",
                },
            ],
        }
    if family == "workflow":
        return {"payload": {"project": identifier, "task": note["purpose"], "synthetic": True}}
    if family == "memory":
        return {
            "key": identifier + ":preference",
            "old_value": {"retention_days": 30},
            "new_value": {"retention_days": 7},
        }
    if family == "tools":
        return {"tool_name": re.sub(r"[^a-z0-9_]", "_", identifier.lower())[:70] + "_calculate"}
    if family == "sql":
        return {"row_name": identifier + "-synthetic-account"}
    if family in {"ocr", "transcript"}:
        text = (
            "Invoice 1042: total ₹375.00. Café research notes."
            if family == "ocr"
            else "Meeting 1042 approved a budget of 375 rupees for café research."
        )
        if identifier == "Latex-OCR-Lama":
            text = r"\frac{a+b}{c} = 375"
        return {
            "reference": text,
            "prediction": text.replace("375", "875"),
            "region_text": "375.00",
        }
    if family in {"training", "extraction"}:
        return {
            "schema": {
                "type": "object",
                "properties": {
                    "project": {"type": "string"},
                    "amount": {"type": "integer", "minimum": 0},
                },
                "required": ["project", "amount"],
                "additionalProperties": False,
            },
            "expected": {"project": identifier, "amount": 375},
            "target_field": "amount",
            "wrong_value": 875,
        }
    if family == "evaluation":
        return {
            "pairs": [
                {"id": identifier + "-normal", "baseline": 0.25, "candidate": 0.75},
                {"id": identifier + "-hard", "baseline": 0, "candidate": 0.5},
            ]
        }
    if family == "streaming":
        return {"answer": "Synthetic lifecycle test for " + identifier}
    return {
        "artifact_id": identifier + "-segment-1",
        "content": "Synthetic integrity fixture for " + identifier + "\n",
    }


def environment(root, identifier, project):
    records = project.get("files", [])
    paths = (
        [r["path"] for r in records]
        if records
        else [
            p.name for p in root.iterdir() if p.is_file() and p.suffix in {".py", ".toml", ".txt"}
        ]
    )
    report = analyze_project(root, paths)
    manifests, requirements, python_requirements = [], [], []
    candidates = [
        root / path
        for path in paths
        if Path(path).name
        in {"requirements.txt", "requirements-dev.txt", "pyproject.toml", "package.json"}
    ]
    for path in sorted(set(candidates)):
        manifests.append(path.relative_to(root).as_posix())
        if path.name == "pyproject.toml":
            data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
            metadata = data.get("project", {})
            requirements.extend(metadata.get("dependencies", []))
            if metadata.get("requires-python"):
                python_requirements.append(metadata["requires-python"])
        elif path.name.startswith("requirements"):
            for line in path.read_text(encoding="utf-8-sig").splitlines():
                line = line.split(" #")[0].strip()
                if re.match(r"^[A-Za-z0-9][A-Za-z0-9_.-]*(?:\[|[<>=!~; ]|$)", line):
                    requirements.append(line)
    names = report.get("environment", [])
    return {
        "project_id": identifier,
        "manifests": manifests,
        "requirements": sorted(set(requirements)),
        "python_requirements": sorted(set(python_requirements)),
        "environment_names": names,
        "scope": "declared Python dependency presence only; optional/dev/alternate paths may be included; Node manifests are listed, not resolved",
    }


def examples(root, profile):
    fixture, family = profile["fixture"], profile["family"]
    files = {}
    if family == "retrieval":
        files["corpus.json"] = fixture["documents"]
    elif family == "workflow":
        files["payload.json"] = fixture["payload"]
    elif family == "memory":
        files["value.json"] = fixture["new_value"]
    elif family in {"ocr", "transcript"}:
        files["quality.json"] = {
            "reference": fixture["reference"],
            "prediction": fixture["prediction"],
        }
    elif family in {"training", "extraction", "tools"}:
        schema = fixture.get(
            "schema",
            {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
                "additionalProperties": False,
            },
        )
        files["schema.json"] = {
            "schema": schema,
            "value": fixture.get("expected", {"expression": "37*3+19*2"}),
        }
        if family != "tools":
            files["reward.json"] = {
                "schema": schema,
                "expected": fixture["expected"],
                "prediction": {**fixture["expected"], "amount": 875},
            }
            files["splits.json"] = {
                "train": [{"input": "example-a", "group": "source-a"}],
                "test": [{"input": "example-b", "group": "source-b"}],
            }
            files["distill.json"] = {
                "teacher": [1000, 999],
                "student": [999, 1000],
                "target": 0,
                "temperature": 2,
                "alpha": 0.5,
            }
    elif family == "evaluation":
        files["pairs.json"] = fixture["pairs"]
    elif family == "streaming":
        files["events.json"] = [
            {"type": "start", "fixture": True},
            {"type": "delta", "channel": "answer", "text": fixture["answer"]},
            {"type": "done", "fixture": True},
        ]
    elif family == "artifacts":
        files["artifacts.json"] = [{"id": fixture["artifact_id"], "path": "segment.txt"}]
        files["segment.txt"] = fixture["content"]
    else:
        files["parameters.json"] = [fixture["row_name"]]
    for name, value in files.items():
        write(root / "enhancement/examples" / name, value)
    return ["enhancement/examples/" + name for name in files]


def operation(profile):
    family = profile["family"]
    return {
        "retrieval": f'search --documents enhancement/examples/corpus.json --query "{profile["project_id"]} retention" --tenant learner --save-index index.json',
        "workflow": "job --state runs.sqlite --owner learner --id run-1 --operation create --input enhancement/examples/payload.json",
        "memory": "memory --state memory.sqlite --owner learner --key preference --operation remember --input enhancement/examples/value.json --ttl 3600",
        "tools": "schema --input enhancement/examples/schema.json",
        "sql": 'query-sql --database YOUR_EXISTING_DATABASE.sqlite --sql "SELECT name FROM sqlite_master WHERE type=?" --parameters \'["table"]\'',
        "ocr": "quality --input enhancement/examples/quality.json",
        "transcript": "quality --input enhancement/examples/quality.json",
        "training": "reward --input enhancement/examples/reward.json",
        "extraction": "reward --input enhancement/examples/reward.json",
        "evaluation": "compare --input enhancement/examples/pairs.json",
        "streaming": "stream-check --input enhancement/examples/events.json",
        "artifacts": "artifacts --directory enhancement/examples --input enhancement/examples/artifacts.json",
    }[family]


def guide(profile, paths, local):
    feature, mechanism, limit, exercise = FEATURES[profile["family"]]
    journal = "LEARNING_JOURNAL.md"
    original = (
        "docs/REVERSE_ENGINEERING.md"
        if local and (ROOT / profile["project_id"] / "docs/REVERSE_ENGINEERING.md").exists()
        else "REVERSE_ENGINEERING.md"
    )
    if not (ROOT / profile["project_id"] / original).is_file():
        original = "README.md"
    return f'''# Enhancements: {profile["project_id"]}

## Source and purpose

{profile["purpose"]}

Original mechanism: {profile["mechanism"]}

Read the [existing walkthrough]({original}) alongside this extension. Original model/provider code remains the application implementation; `enhance.py` is an additional executable engineering lab. Shared code lives in [workbench_core](../workbench_core/README.md), so keep this project in the collection checkout. It uses Python 3.12+ and no third-party packages. This avoids 113 drifting copies and leaves each project's model environment isolated.

## What changed and why

**{feature}.** {mechanism}

Before this addition, the project's learning guide did not expose this contract through a common local command. It now has a source-specific profile, synthetic inputs, negative/recovery checks, read-only environment diagnostics and commands that accept your own data. The checks execute the shared algorithms; their inputs are explicitly synthetic and contain no inferred model output.

{limit}

## Run and inspect

From this project folder, using a real Python 3.12+ interpreter:

```powershell
python enhance.py check
python enhance.py doctor
python enhance.py {operation(profile)}
python enhance.py --help
```

`check` returns 0 only if every scenario passes, 1 for failed scenarios and 2 for invalid input. It uses temporary local files and makes no network calls. `doctor` reports declared package presence and environment **names/set flags**, never secret values; it does not certify compatible versions, optional credentials, installed models or hardware. Run it inside the original project's virtual environment to inspect that environment.

Examples: {", ".join("[" + Path(p).name + "](" + p + ")" for p in paths)}. Replace synthetic labels with independently checked held-out data. The SQL example intentionally names an existing database you supply; `check` creates and removes its own database.

## Learn from every scenario

| Scenario | Prediction to make | Evidence and explanation |
| --- | --- | --- |
| Normal | Which output follows from the fixed reference? | Inspect the returned scores, IDs, versions or state; keep actual counts. |
| Invalid/adversarial | Which boundary should reject the input? | Mutate a required field, limit or path. Record the rejection and confirm no side effect occurred. |
| Missing evidence/output | Can the system distinguish absence from success? | Test unmatched retrieval, empty text, missing artifacts or missing paired labels as relevant. |
| Interrupted/restarted | What survives and what may be retried? | Inspect durable state or partial output; distinguish local recovery from remote side-effect recovery. |
| Concurrent/another user | Which information and updates must be isolated? | Use separate owner/tenant inputs; local owner strings are not proof of authentication. |
| Regression | What changes on the same held-out cases? | Keep baseline and candidate labels together; separate synthetic checks from model quality. |

Focused extension exercise: {exercise}

Original project experiment to preserve: {profile["experiment"]}

Record your prediction, input/version, observed evidence, failure explanation and next experiment in [{journal}]({journal}). If a scenario is inapplicable to this algorithm, explain why and exercise it at the original application's boundary instead. A passing CPU check does not demonstrate remote outage, concurrency or model quality in the original integration.

## Better production deployment

{profile["production"]}

Connect this contract at the original boundary rather than placing the entire demo behind a public endpoint. Use verified identity to derive scope; separate ingestion/training/long jobs from request workers; cap input, output, queue and provider cost; pin and evaluate the selected dependency/model revision; keep secrets outside source. Track request/source/model IDs, terminal state, quality and latency without logging uploaded documents or credentials. Release against held-out normal, missing, invalid, failed and cross-user cases. Canary the candidate, retain the prior compatible artifact/index/schema, and rehearse rollback plus restore/deletion propagation.

For local learning, stdlib algorithms and SQLite keep behavior inspectable and inexpensive. At shared-service scale, use a durable queue/database and independently scaled inference workers when measured contention or GPU demand requires them. That adds operational cost, migrations and failure modes; model choice and capacity still require load and quality measurements. The original [learning guide]({"README.md" if local else "LEARNINGS.md"}) contains project-specific deployment tradeoffs.

## Packaging and evidence limits

`enhancement/Dockerfile` packages only the CPU extension. Build from the **collection root** with `docker build -f "{profile["project_id"]}/enhancement/Dockerfile" -t ai-learning-check .`. It copies this profile and the shared runtime, uses a nonroot user and runs `check`; it does not install the original SDKs, serve the app or provision a model. The image has not been built here. Resolve and pin a verified base-image digest in your own registry before a release.

The collection [coverage report](../docs/ENHANCEMENT_REPORT.md) records executed CPU checks and native OCR verification separately. No live provider, GPU training or production deployment is implied. Generated extension guides/configs are maintained by `tools.enhance_collection`; personal journals are never regenerated over existing content.
'''


def main():
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    with (ROOT / "tools/project_notes.psv").open(encoding="utf-8", newline="") as stream:
        notes = {row["id"]: row for row in csv.DictReader(stream, delimiter="|")}
    registry = []
    for project in catalog["projects"] + [{"id": name, "local": True} for name in OCR]:
        identifier, local = project["id"], project.get("local", False)
        root = ROOT / identifier
        note = OCR_NOTES[identifier] if local else notes[identifier]
        family = OVERRIDES.get(identifier, FAMILIES[note["category"]])
        variant = (
            "distillation"
            if "distill" in identifier.lower()
            else "detection"
            if "yolo" in identifier.lower()
            else None
        )
        profile = {
            "schema_version": 1,
            "project_id": identifier,
            "family": family,
            "variant": variant,
            "fixture_kind": "synthetic CPU reference inputs; not recorded model responses",
            **{key: note[key] for key in ("purpose", "mechanism", "experiment", "production")},
            "fixture": fixture_for(identifier, family, note),
        }
        write(root / "enhance.py", LAUNCHER)
        write(root / "enhancement/profile.json", profile)
        write(root / "enhancement/environment.json", environment(root, identifier, project))
        paths = examples(root, profile)
        write(root / "ENHANCEMENTS.md", guide(profile, paths, local))
        dockerfile = (
            "FROM python:3.12-slim\nENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1\n"
            "WORKDIR /workspace/project\nCOPY workbench_core /workspace/workbench_core\n"
            + "COPY "
            + json.dumps([identifier + "/enhance.py", "/workspace/project/enhance.py"])
            + "\n"
            + "COPY "
            + json.dumps(
                [
                    identifier + "/enhancement/profile.json",
                    "/workspace/project/enhancement/profile.json",
                ]
            )
            + "\n"
            + 'USER 65532:65532\nENTRYPOINT ["python", "enhance.py"]\nCMD ["check"]\n'
        )
        write(root / "enhancement/Dockerfile", dockerfile)
        write(
            root / "enhancement/Dockerfile.dockerignore",
            "**\n!workbench_core/\n!workbench_core/*.py\n"
            + f"!{identifier}/\n!{identifier}/enhance.py\n!{identifier}/enhancement/\n!{identifier}/enhancement/profile.json\n",
        )
        additions = [
            "enhance.py",
            "enhancement/profile.json",
            "enhancement/environment.json",
            "enhancement/Dockerfile",
            "enhancement/Dockerfile.dockerignore",
            "ENHANCEMENTS.md",
            *paths,
        ]
        records = [
            {
                "path": path,
                "local_sha256": digest(root / path),
                "changes": [
                    "Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs."
                ],
            }
            for path in additions
        ]
        registry.append({"id": identifier, "family": family, "local_ocr": local, "files": records})
        if not local:
            keep = [
                record
                for record in project.get("local_additions", [])
                if record["path"] not in additions
            ]
            project["local_additions"] = keep + records
            project["enhancement"] = {
                "entry": "enhance.py",
                "profile": "enhancement/profile.json",
                "family": family,
            }
        elif not (root / "LEARNING_JOURNAL.md").exists():
            write(
                root / "LEARNING_JOURNAL.md",
                "# Personal learning journal\n\nRecord predictions before each experiment, fixed inputs and model versions, actual observations, failures, cross-user isolation, quality/latency measurements, production tradeoffs and the next experiment. This file is never overwritten by the collection generator.\n",
            )
    write(ROOT / "catalog.json", catalog)
    write(ROOT / "enhancements.json", {"schema_version": 1, "projects": registry})
    print(
        f"Built executable learning extensions for {len(registry)} projects; existing journals preserved."
    )


if __name__ == "__main__":
    main()
