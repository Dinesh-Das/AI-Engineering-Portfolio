# AI Projects: reverse-engineering and learning collection

**102 AI project folders**, based on [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) revision `042aeb5067384981eeba6a07fa882f436bb1660d`, captured on 10 November 2026.

Start with the **[project index](PROJECT_INDEX.md)**. Every project has its own README, reverse-engineering walkthrough, learning/production guide, evaluation protocol, environment template, analysis report and source manifest.

This collection preserves the upstream implementations and adds source-backed explanations, safety fixes and local tooling. It does not claim that 102 projects were independently rewritten, that their dependencies all work together, or that paid inference/GPU training has been verified. Their original framework/model choices remain available for study.

## Scope

- Included: RAG, retrieval, agents, MCP integrations, memory, training, model evaluation, voice, media, extraction and AI deployment examples, including relevant projects not listed in the upstream README.
- Excluded: four completed OCR projects, seven projects in the upstream Chat Interfaces & UI category, and four general-resource folders.
- Mixed AI/UI projects retain their AI source and original Python presentation wrappers as reference. Frontend components and UI routes are omitted; no UI was built or launched.
- Two README links have no source folder at the pinned revision: `attention-is-all-you-need-impl` and `nvidia-demo`. They are recorded as missing rather than represented by invented implementations.
- Four included folders are integration/deployment guides; `omnigraph-multi-agent` supplies graph schemas and fixtures. Their docs explicitly distinguish these from runnable applications.

See [complete upstream reconciliation](docs/INVENTORY.md).

## What to read in each project

| File | What you learn |
| --- | --- |
| `README.md` | Purpose, setup, entry candidates, external requirements and verification status |
| `REVERSE_ENGINEERING.md` | Actual source map, functions/classes, models, configuration, findings and recorded improvements |
| `LEARNINGS.md` | Rebuild sequence, targeted experiments, failure modes, production architecture and tradeoffs |
| `EVALUATION.md` | Ground truth, task-specific metrics and evidence required before trusting a change |
| `analysis.json` | Complete static symbol/import/model/environment inventory |
| `project.json` | Pinned provenance, file hashes, transformations, omissions and runtime status |
| `UPSTREAM_README.md` | Original author instructions where provided |
| `UPSTREAM_LICENSE` | Original MIT attribution; additional source notices remain applicable |

## Local commands

The offline tooling uses Python 3.12 and the standard library. On this machine, `run.ps1` finds the existing uv-managed Python runtime even though the Windows `python` alias is broken. It prefers an activated virtual environment. Set `AI_PROJECTS_PYTHON` to a specific interpreter to override discovery.

Run from this folder:

```powershell
.\run.ps1 list
.\run.ps1 check
.\run.ps1 show --project simple-rag-workflow
.\run.ps1 run --project simple-rag-workflow --entry workflow.py
```

`run` previews the command by default. Append `--execute` only after preparing the chosen project's environment. This may invoke external APIs, download models, launch servers or incur GPU/API costs. The direct child has a configurable deadline; descendant processes require a container/job boundary for complete isolation.

For an entry with arguments:

```powershell
.\run.ps1 run --project colbert-rag --entry maxsim.py --execute
.\run.ps1 run --project ai-podcast-generator --entry cli.py --entry-args --help
```

Each project's dependencies must be installed separately. Some require Python 3.13 or other versions, native tools, Linux/Colab, databases or a GPU. A discovered entry point is a source-inspection result, not a successful integration test. Dependency-less recipes have no fabricated launch command.

The same wrapper also runs the tests, verifier and offline evaluator:

```powershell
.\run.ps1 test
.\run.ps1 verify
.\run.ps1 evaluate --input docs/examples/observations.jsonl
```

The supplied observations file is synthetic metric-test data, not model benchmark evidence.

## Improvements included

- Cleared notebook execution output and saved widget state; quarantined two empty notebooks and one malformed UI script.
- Fixed an unmatched parenthesis in a RAG notebook.
- Added explicit connect/read timeouts to eligible direct HTTP calls while preserving existing timeout settings.
- Redacted recognizable credential-like literals and generated empty environment templates.
- Added strict relevance gating to two corrective-RAG workflows: empty/unknown evidence now triggers recovery, and one irrelevant chunk no longer forces web search when usable evidence exists.
- Added a tested CPU MaxSim implementation with padding masks, shape/number validation, stable ranking and actual top-k behavior.
- Added headless podcast and meeting-note CLIs that bypass presentation shells.
- Added deterministic evaluation metrics with label-coverage reporting, source integrity checks, and path-contained command construction without a shell.

[Source change log](docs/CHANGES.md) records the affected files. [Validation report](docs/VALIDATION.md) distinguishes tested changes from remaining integration work. The limited pattern scanner is not a comprehensive dependency or security audit.

## Learning route

Follow [the learning path](docs/LEARNING_PATH.md) from basic RAG through retrieval, agents/MCP, memory, evaluation, multimodal work and training. Rebuild the smallest headless unit first, then perform the experiment in that project's learning guide. Keep a baseline and change one variable at a time.

Production proposals live in each `LEARNINGS.md` and the shared [deployment playbook](docs/DEPLOYMENT_PLAYBOOK.md). These are design proposals; no infrastructure was provisioned.

## Reproducibility and attribution

The original clone is cached under ignored `.source/ai-engineering-hub`. `tools.import_collection` performs a first import and refuses to overwrite existing project folders. `tools.write_docs` renders the maintained notes in `tools/project_notes.psv` against current source facts. It does not silently accept changed source hashes; record deliberate changes in the relevant manifest before updating the guides.

Work is committed locally on `main`. No branch-specific workflow or remote publication is required. See [third-party notices](docs/THIRD_PARTY_NOTICES.md) and [official documentation references](docs/SOURCES.md).
