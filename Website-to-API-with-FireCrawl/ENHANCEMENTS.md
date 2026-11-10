# Enhancements: Website-to-API-with-FireCrawl

## Source and purpose

Convert web content into schema-constrained extraction results.

Original mechanism: The notebook builds dynamic Pydantic extraction schemas and calls Firecrawl to produce structured data.

Read the [existing walkthrough](REVERSE_ENGINEERING.md) alongside this extension. Original model/provider code remains the application implementation; `enhance.py` is an additional executable engineering lab. Shared code lives in [workbench_core](../workbench_core/README.md), so keep this project in the collection checkout. It uses Python 3.12+ and no third-party packages. This avoids 113 drifting copies and leaves each project's model environment isolated.

## What changed and why

**Schema and semantic accuracy.** A strict schema subset validates output shape, while independently supplied expected fields determine exact field accuracy. Valid JSON with incorrect facts cannot earn full reward. Split audits flag identical inputs and shared source groups.

Before this addition, the project's learning guide did not expose this contract through a common local command. It now has a source-specific profile, synthetic inputs, negative/recovery checks, read-only environment diagnostics and commands that accept your own data. The checks execute the shared algorithms; their inputs are explicitly synthetic and contain no inferred model output.

Exact field equality is intentionally strict. It is not a semantic judge, a general JSON Schema engine or proof that the expected labels are correct.

## Run and inspect

From this project folder, using a real Python 3.12+ interpreter:

```powershell
python enhance.py check
python enhance.py doctor
python enhance.py reward --input enhancement/examples/reward.json
python enhance.py --help
```

`check` returns 0 only if every scenario passes, 1 for failed scenarios and 2 for invalid input. It uses temporary local files and makes no network calls. `doctor` reports declared package presence and environment **names/set flags**, never secret values; it does not certify compatible versions, optional credentials, installed models or hardware. Run it inside the original project's virtual environment to inspect that environment.

Examples: [schema.json](enhancement/examples/schema.json), [reward.json](enhancement/examples/reward.json), [splits.json](enhancement/examples/splits.json), [distill.json](enhancement/examples/distill.json). Replace synthetic labels with independently checked held-out data. The SQL example intentionally names an existing database you supply; `check` creates and removes its own database.

## Learn from every scenario

| Scenario | Prediction to make | Evidence and explanation |
| --- | --- | --- |
| Normal | Which output follows from the fixed reference? | Inspect the returned scores, IDs, versions or state; keep actual counts. |
| Invalid/adversarial | Which boundary should reject the input? | Mutate a required field, limit or path. Record the rejection and confirm no side effect occurred. |
| Missing evidence/output | Can the system distinguish absence from success? | Test unmatched retrieval, empty text, missing artifacts or missing paired labels as relevant. |
| Interrupted/restarted | What survives and what may be retried? | Inspect durable state or partial output; distinguish local recovery from remote side-effect recovery. |
| Concurrent/another user | Which information and updates must be isolated? | Use separate owner/tenant inputs; local owner strings are not proof of authentication. |
| Regression | What changes on the same held-out cases? | Keep baseline and candidate labels together; separate synthetic checks from model quality. |

Focused extension exercise: Create a schema-valid wrong amount and a correct value with an extra key. Explain why format rewards alone can train the wrong behavior.

Original project experiment to preserve: Remove required fields and alter page layout and test schema validity independently from semantic extraction accuracy.

Record your prediction, input/version, observed evidence, failure explanation and next experiment in [LEARNING_JOURNAL.md](LEARNING_JOURNAL.md). If a scenario is inapplicable to this algorithm, explain why and exercise it at the original application's boundary instead. A passing CPU check does not demonstrate remote outage, concurrency or model quality in the original integration.

## Better production deployment

Expose only approved extraction schemas and destinations, cap crawl size and validate results before returning them to downstream consumers.

Connect this contract at the original boundary rather than placing the entire demo behind a public endpoint. Use verified identity to derive scope; separate ingestion/training/long jobs from request workers; cap input, output, queue and provider cost; pin and evaluate the selected dependency/model revision; keep secrets outside source. Track request/source/model IDs, terminal state, quality and latency without logging uploaded documents or credentials. Release against held-out normal, missing, invalid, failed and cross-user cases. Canary the candidate, retain the prior compatible artifact/index/schema, and rehearse rollback plus restore/deletion propagation.

For local learning, stdlib algorithms and SQLite keep behavior inspectable and inexpensive. At shared-service scale, use a durable queue/database and independently scaled inference workers when measured contention or GPU demand requires them. That adds operational cost, migrations and failure modes; model choice and capacity still require load and quality measurements. The original [learning guide](LEARNINGS.md) contains project-specific deployment tradeoffs.

## Packaging and evidence limits

`enhancement/Dockerfile` packages only the CPU extension. Build from the **collection root** with `docker build -f "Website-to-API-with-FireCrawl/enhancement/Dockerfile" -t ai-learning-check .`. It copies this profile and the shared runtime, uses a nonroot user and runs `check`; it does not install the original SDKs, serve the app or provision a model. The image has not been built here. Resolve and pin a verified base-image digest in your own registry before a release.

The collection [coverage report](../docs/ENHANCEMENT_REPORT.md) records executed CPU checks and native OCR verification separately. No live provider, GPU training or production deployment is implied. Generated extension guides/configs are maintained by `tools.enhance_collection`; personal journals are never regenerated over existing content.
