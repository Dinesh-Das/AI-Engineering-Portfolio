# Implementation plan

The user authorized implementation of the complete non-UI, non-OCR AI collection. Work stays on main. The repository is empty initially; there is no completed local OCR code to alter.

1. Pin upstream main, inventory all tree directories and README links, classify exclusions and missing sources.
2. Import AI source and necessary samples with license/provenance; omit frontend-only assets and sanitize notebook outputs.
3. Analyze actual implementations, dependency manifests, model identifiers, environment requirements, entry points and hazards.
4. Add tested offline tooling, project-specific documentation, environment templates and verifiable source improvements.
5. Validate every project, reconcile coverage, review the diff, and commit completed increments.

Each project is an independent slice; catalog status distinguishes source analysis from live model evaluation. Verification runs without importing untrusted upstream code. API/GPU runs and real deployment are separate evidence categories.

Risks: upstream source may be incomplete, dependency constraints old or conflicting, examples may contain credentials or personal outputs, UI code may be mixed with AI logic, and tutorials may depend on paid services. Mitigate through explicit source evidence, output clearing, isolated manifests, headless entry-point classification and honest validation status.
