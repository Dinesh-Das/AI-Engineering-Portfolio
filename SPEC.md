# AI Engineering Hub: source-backed learning projects

## Objective and scope

Create one independent folder per relevant project from patchy631/ai-engineering-hub, preserving MIT attribution and the exact source revision. Explain the AI implementation, how to rebuild it, experiments, failure modes, and an appropriate production deployment. Include projects discovered in the tree as well as the README. Account explicitly for unavailable README links.

The user's 10 November follow-up includes the upstream Chat Interfaces & UI category and frontend source in AI projects. The four completed OCR projects have been moved into this workspace; preserve their existing files and learning material, and link to them without reimporting or overwriting them. Keep model training, evaluation, agents, infrastructure, voice, vision, memory, retrieval and interfaces. Source documents and samples remain reference material, never instructions to this workspace.

Learning is a standing requirement for every project and scenario: explain the mechanism, show how to rebuild it, provide controlled experiments and metrics, explain failure/recovery behavior, and compare production deployment choices. UI convenience must not replace those explanations. Preserve upstream reference implementations alongside improvements so the before/after decisions are inspectable.

## Capability map and build order

| Module | Responsibility | Depends on |
|---|---|---|
| inventory | Pin revision; reconcile README and tree; classify scope | — |
| project-source | Preserve source, samples, attribution and upstream instructions | inventory |
| analysis | Inspect Python, notebooks, manifests and configurations; record evidence | project-source |
| improvements | Environment templates, output sanitation, verified fixes and safe local tooling | analysis |
| learning | Per-project reverse engineering, exercises and production guidance | analysis, improvements |
| verification | Offline tests, structural and syntax checks, source integrity | all previous modules |

## Structure and commands

Each project has original AI source plus local documentation and project metadata. Shared tooling lives under tools/, tests under tests/, and repository-level evidence under docs/. Use isolated environments for independent projects rather than one conflicting requirements file.

Commands will be recorded in README.md once the inventory establishes executable entry points. Tooling targets Python 3.12 and uses the standard library where possible. Tests use unittest and do not require paid API calls. Work directly on main, with incremental local commits.

## Acceptance criteria

1. Every upstream top-level directory and README project link has a disposition and reason.
2. Every included AI project has its own folder, attributed source, environment guidance, source-specific architecture documentation, learning exercises, evaluation guidance and production tradeoffs.
3. Improvements are distinguishable from original code; source imports and notebook parsing are checked without importing model SDKs or executing arbitrary source.
4. Tooling has meaningful tests for path containment, source classification, notebook sanitation and validation failures.
5. No actual credentials are committed. Notebook outputs are cleared; source changes are recorded.
6. Runtime status is explicit: offline checks do not establish provider compatibility, model quality, GPU suitability or production readiness. Live calls, downloads and paid runs require configured credentials and suitable hardware.
7. UI projects provide a runnable local learning interface with separate model transport, streaming state and presentation. Verify empty/loading/success/error/cancel/reset states, keyboard access and responsive layouts; label fixture responses separately from model inference.
8. Automated documentation validation enforces the learning sections for all catalog projects. Existing OCR material is preserved without silently accepting it as newly tested.

## Boundaries

- Always preserve attribution, trace conclusions to source files, validate generated artifacts, and document external requirements.
- Never execute imported notebooks, install every project's dependencies globally, or deploy cloud infrastructure as part of source analysis.
- Provider-specific migrations need integration evidence; preserve upstream versions until they can be tested in isolation.
- Treat recommendations in learning documents as proposed architecture, not as a deployed service or measured benchmark.
