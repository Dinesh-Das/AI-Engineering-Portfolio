# Implementation plan

## Enhancement pass: all 113 projects

The user explicitly selected all 113, including the completed OCR projects. Build useful, executable enhancements by problem family: evidence retrieval and provenance, durable agent jobs and tool validation, scoped/expiring memory, objective evaluation, training-data/reward checks, transcript/OCR quality, structured extraction validation and artifact integrity. Project-specific profiles and scenarios bind the reusable implementation to each project's learning objective.

1. Establish native OCR test baselines and preserve journals plus unrelated dirty files. Audit original source for directly verifiable defects.
2. Implement standard-library enhancement primitives in small tested modules. Add per-project commands, fixed scenario suites, preflight checks and CPU-lab packaging. Do not claim these replace the original AI integrations.
3. Apply targeted source fixes with regression tests (unsafe model-output parsing/calculation, bounded HTTP calls and observed runtime defects). Record changed source hashes and before/after explanations.
4. Exercise every project's scenario suite in a separate process. Add OCR character/word/region evaluation to the completed projects and run their native tests and applicable lint checks.
5. Validate all source, learning contracts, package/profile coverage and preserved journals. Write a coverage/result matrix and commit scoped changes on main in the parent and affected OCR repositories.

Success means a verified executable enhancement for every project, not 113 independently audited production systems. Live API/GPU benchmarks and actual infrastructure deployment remain separate evidence.

The initial AI collection is complete as a source-learning port. The user's follow-up authorizes UI category projects and requires the learning aspect throughout. Work stays on main. Four completed OCR folders now exist locally and must be preserved.

## Follow-up: include UI and preserve learning

1. Extend the pinned source inventory with the seven UI-category projects, restoring previously omitted frontend source/assets without overwriting existing project files or the moved OCR work.
2. Preserve all upstream references and create a small runnable local learning interface for each new UI project, with project-specific model/capability settings and separated transport/state/presentation code.
3. Test stream parsing, model request validation, failure and cancellation, per-tab history, responsive behavior, keyboard access and accessibility. Use clearly labeled fixtures for browser tests; report live model checks separately.
4. Extend per-project guides with AI/UI architecture, controlled experiments, scenario-based learning and production tradeoffs. Enforce the learning contract through collection validation and link existing OCR guides.
5. Verify the expanded catalog and source hashes, review changes, and commit only this task's changes on main.

1. Pin upstream main, inventory all tree directories and README links, classify exclusions and missing sources.
2. Import AI source and necessary samples with license/provenance; omit frontend-only assets and sanitize notebook outputs.
3. Analyze actual implementations, dependency manifests, model identifiers, environment requirements, entry points and hazards.
4. Add tested offline tooling, project-specific documentation, environment templates and verifiable source improvements.
5. Validate every project, reconcile coverage, review the diff, and commit completed increments.

Each project is an independent slice; catalog status distinguishes source analysis from live model evaluation. Verification runs without importing untrusted upstream code. API/GPU runs and real deployment are separate evidence categories.

Risks: upstream source may be incomplete, dependency constraints old or conflicting, examples may contain credentials or personal outputs, UI code may be mixed with AI logic, and tutorials may depend on paid services. Mitigate through explicit source evidence, output clearing, isolated manifests, headless entry-point classification and honest validation status.

## All-113 enhancement results

Implemented per-project launchers, source-specific profiles and examples, shared CPU operations, preflight diagnostics, learning/production guides and CPU-only container packaging. All 113 launchers passed 630 scenarios; collection suites passed 75 tests with one Windows symlink-permission skip; four native OCR suites passed 130 tests. Source/document/learning verification passed. All 109 existing journals and two unrelated user files are byte-identical. Native OCR additions were committed independently on main; parent changes are staged only from known task paths. Docker daemon, live provider, GPU training and production deployment remain unverified. See docs/ENHANCEMENT_REVIEW.md and docs/ENHANCEMENT_REPORT.md.

## Offline interview handbook

Reconcile all current projects and curate source-backed chapters; generate a self-contained root index.html; add searchable project/topic readers, revision paths, mock interview questions, calculators and local study state; verify commands, safe rendering, offline browser use, responsive layouts and accessibility; preserve existing changes and commit scoped work on main. Full specification: docs/INTERVIEW_HANDBOOK_SPEC.md.

Handbook completed: root index.html embeds all 113 project readers (six guide views), 574 annotated commands, 46 technical chapters and 477 answered questions, plus four revision paths, four calculators and local study tools. Seven content/security tests and the full collection suites pass (82 passed, one host symlink-permission skip). Twelve real-browser scenario groups pass, including all project readers/command panels, offline file use, responsive/accessibility checks, backup safety and storage recovery. Collection verification enforces content/evidence freshness. All 116 pre-existing journal/report/user-edit hashes are preserved; existing OCR repositories are untouched.
