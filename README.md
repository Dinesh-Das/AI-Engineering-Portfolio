# AI Projects: reverse-engineering and learning collection

Open **[the interactive interview field manual](index.html)** for the complete offline study desk: all 113 projects, embedded deep guides, run commands, 46 technical chapters, 477 answered questions, learning paths, metric/capacity examples and local revision notes. Double-click `index.html`; no server or install is needed to read it. Rebuild after documentation changes with `.\run.ps1 handbook`; verify freshness with `.\run.ps1 handbook --check`.

**109 source-backed AI project folders, including the UI category**, based on [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) revision `042aeb5067384981eeba6a07fa882f436bb1660d`, captured on 10 November 2026. The user's four completed OCR folders are also preserved locally and linked separately.

Start with the **[project index](PROJECT_INDEX.md)**. Every project has its own README, reverse-engineering walkthrough, learning/production guide, evaluation protocol, environment template, analysis report and source manifest.

**All 113 projects now have executable engineering extensions**, including the four OCR repositories. Each folder's `ENHANCEMENTS.md` connects its source mechanism to usable CPU operations, synthetic negative/recovery checks, preserved learning exercises and production tradeoffs. Run `.\run.ps1 enhance` from this root, or `python enhance.py check` / `doctor` inside a project. Read the [executed coverage](docs/ENHANCEMENT_REPORT.md), [extension architecture](workbench_core/README.md) and [native OCR verification](docs/OCR_ENHANCEMENT_VALIDATION.md). These checks are separate from original model/provider/GPU qualification.

This collection preserves the upstream implementations and adds source-backed explanations, targeted fixes and local tooling. The seven UI-category projects also include independently runnable learning interfaces with bundled standard-library code. Their original Chainlit/Streamlit/Motia source remains available for comparison. Original framework dependencies, live inference and GPU training are separate integration checks.

**Learning is required throughout.** Every catalog project retains a mechanism walkthrough, rebuild sequence, controlled experiment, metrics, scenario exercises and production deployment tradeoffs. The checks enforce this [learning contract](docs/LEARNING_CONTRACT.md); UI convenience does not replace it.

## Scope

- Included: RAG, retrieval, agents, MCP integrations, memory, training, model evaluation, voice, media, extraction and AI deployment examples, including relevant projects not listed in the upstream README.
- Included now: all seven projects in the upstream Chat Interfaces & UI category, plus 424 restored frontend source files and assets across the existing collection.
- The four completed OCR folders were moved here by the user. Their code, tests and learning material are preserved; see [local OCR guides](docs/LOCAL_OCR_PROJECTS.md). Four general-resource folders remain outside the project catalog.
- Mixed AI/UI projects now retain frontend components, UI routes, styles and required static assets. Large demo media, generated build caches and credential-setup screenshots remain explicitly omitted.
- Two README links have no source folder at the pinned revision: `attention-is-all-you-need-impl` and `nvidia-demo`. They are recorded as missing rather than represented by invented implementations.
- Four included folders are integration/deployment guides; `omnigraph-multi-agent` supplies graph schemas and fixtures. Their docs explicitly distinguish these from runnable applications.

See [complete upstream reconciliation](docs/INVENTORY.md).

## What to read in each project

| File | What you learn |
| --- | --- |
| `README.md` | Purpose, setup, entry candidates, external requirements and verification status |
| `REVERSE_ENGINEERING.md` | Actual source map, functions/classes, models, configuration, findings and recorded improvements |
| `LEARNINGS.md` | Rebuild sequence, targeted experiments, failure modes, production architecture and tradeoffs |
| `LEARNING_JOURNAL.md` | Your personal experiment records, preserved during documentation regeneration |
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
.\run.ps1 ui --project qwen3-thinking-ui
```

`run` previews the command by default. Append `--execute` only after preparing the chosen project's environment. This may invoke external APIs, download models, launch servers or incur GPU/API costs. The direct child has a configurable deadline; descendant processes require a container/job boundary for complete isolation.

For an entry with arguments:

```powershell
.\run.ps1 run --project colbert-rag --entry maxsim.py --execute
.\run.ps1 run --project ai-podcast-generator --entry cli.py --entry-args --help
```

Each project's dependencies must be installed separately. Some require Python 3.13 or other versions, native tools, Linux/Colab, databases or a GPU. A discovered entry point is a source-inspection result, not a successful integration test. Dependency-less recipes have no fabricated launch command.

The seven new learning interfaces require no third-party Python packages. Start one with labeled offline fixtures:

```powershell
.\run.ps1 ui --project qwen3-thinking-ui --execute --timeout 3600 --entry-args --fixture --port 8765
```

Open http://127.0.0.1:8765. Use the experiment desk, test failure/cancellation/empty-answer scenarios and export your prediction/observation notes. Omit `--fixture` to connect to an already running local Ollama instance and installed model. Nothing downloads a model automatically. See a project's UI_GUIDE.md for the code walkthrough and differences from its upstream framework app.

The same wrapper also runs the tests, verifier and offline evaluator:

```powershell
.\run.ps1 test
.\run.ps1 verify
.\run.ps1 evaluate --input docs/examples/observations.jsonl
```

The supplied observations file is synthetic metric-test data, not model benchmark evidence.

Browser checks use isolated Chrome and project-local test dependencies:

```powershell
npm ci --ignore-scripts --prefix tools/browser-tests
npm test --prefix tools/browser-tests
```

Set `AI_PROJECTS_PYTHON` and `UI_TEST_CHROME` if the test runner needs different interpreter/browser paths. See [UI validation](docs/UI_VALIDATION.md) for responsive, accessibility and lifecycle evidence. Restored original framework UIs are not represented as tested by those learning-interface checks.

## Improvements included

- Cleared notebook execution output and saved widget state; quarantined two empty notebooks and one malformed UI script.
- Fixed an unmatched parenthesis in a RAG notebook.
- Added explicit connect/read timeouts to eligible direct HTTP calls while preserving existing timeout settings.
- Redacted recognizable credential-like literals and generated empty environment templates.
- Added strict relevance gating to two corrective-RAG workflows: empty/unknown evidence now triggers recovery, and one irrelevant chunk no longer forces web search when usable evidence exists.
- Added a tested CPU MaxSim implementation with padding masks, shape/number validation, stable ranking and actual top-k behavior.
- Added headless podcast and meeting-note CLIs that bypass presentation shells.
- Added deterministic evaluation metrics with label-coverage reporting, source integrity checks, and path-contained command construction without a shell.
- Added seven local learning UIs with real incremental transport, image budgets, separate trace/answer channels, cancellation, completed-turn history and exportable experiment notes.
- Restored UI source across the collection and made learning sections a validated requirement in every project and scenario.

[Source change log](docs/CHANGES.md) records the affected files. [Validation report](docs/VALIDATION.md) distinguishes tested changes from remaining integration work. The limited pattern scanner is not a comprehensive dependency or security audit.

## Learning route

Follow [the learning path](docs/LEARNING_PATH.md) from basic RAG through retrieval, agents/MCP, memory, evaluation, multimodal work and training. Rebuild the smallest headless unit first, then perform the experiment in that project's learning guide. Keep a baseline and change one variable at a time.

Production proposals live in each `LEARNINGS.md` and the shared [deployment playbook](docs/DEPLOYMENT_PLAYBOOK.md). These are design proposals; no infrastructure was provisioned.

## Reproducibility and attribution

The original clone is cached under ignored `.source/ai-engineering-hub`. `tools.import_collection` performs a first import and refuses to overwrite existing project folders. `tools.write_docs` renders the maintained notes in `tools/project_notes.psv` against current source facts. It does not silently accept changed source hashes; record deliberate changes in the relevant manifest before updating the guides.

Work is committed locally on `main`. No branch-specific workflow or remote publication is required. See [third-party notices](docs/THIRD_PARTY_NOTICES.md) and [official documentation references](docs/SOURCES.md).
