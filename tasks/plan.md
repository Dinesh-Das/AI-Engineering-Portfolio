# Implementation plan

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
