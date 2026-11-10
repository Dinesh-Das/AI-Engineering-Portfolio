# Work checklist

## Enhancement pass: all 113 projects

- [x] Record native OCR baselines and existing user changes.
  - Acceptance: tests run in each existing environment; personal learning files and unrelated changes are recorded.
  - Verify: native pytest outputs and preservation hashes.
- [x] Build tested enhancement primitives and per-project executable scenarios.
  - Acceptance: all 113 projects have meaningful CPU operations and project-specific checks.
  - Verify: primitive unit tests and isolated scenario runs.
- [x] Add preflight diagnostics, packaging and targeted original-source fixes.
  - Acceptance: setup gaps are actionable; fixes have regression tests and recorded provenance.
  - Verify: CLI checks, source-integrity verification and focused tests.
- [x] Add OCR quality evaluation and preserve learning across all projects.
  - Acceptance: CER/WER/region checks work; journals and original learning material are retained.
  - Verify: quality regression tests, native OCR tests and required lint checks.
- [x] Verify complete enhancement coverage and commit scoped changes on main.
  - Acceptance: per-project evidence is recorded, no fabricated model benchmarks and no unrelated files committed.
  - Verify: full checks, enhancement matrix and Git review.

- [x] Pin upstream revision and reconcile every project path.
  - Acceptance: tree and README entries have inclusion/exclusion/missing reasons.
  - Verify: inventory coverage test.
- [x] Import independent project folders with MIT attribution and cleared notebooks.
  - Acceptance: source hashes and intentional transformations are recorded.
  - Verify: source-integrity and notebook-output checks.
- [x] Add source-specific reverse engineering and learning documents.
  - Acceptance: every included project has architecture, experiments, evaluation and deployment guidance.
  - Verify: documentation and metadata validation.
- [x] Implement tested improvements and headless local tooling.
  - Acceptance: useful offline commands; credential-free checks; bounded execution and path validation.
  - Verify: unit tests and actual CLI checks.
- [x] Review, validate the entire collection, and commit on main.
  - Acceptance: no accidental credentials; recorded validation results; clean working tree.
  - Verify: tests, catalog coverage, syntax report and git status.

Live provider/GPU execution must be reported separately from the source-analysis deliverable. Do not mark such execution verified without running it.

## Follow-up: UI projects with learning preserved

- [x] Add the seven UI-category projects and restore omitted frontend source/assets.
  - Acceptance: every source path has a current disposition; moved OCR content is untouched.
  - Verify: additive-import tests, source integrity and preserved OCR hashes.
- [x] Build runnable local learning interfaces with project-specific capabilities.
  - Acceptance: text/vision/reasoning/streaming scenarios have explicit state and a bounded model transport.
  - Verify: unit tests and local HTTP integration tests.
- [x] Preserve learning across all projects and scenarios.
  - Acceptance: required learning sections are validated, controlled experiments are present, and OCR guides remain linked.
  - Verify: documentation contract and link checks.
- [x] Verify interfaces in an isolated real browser and commit on main.
  - Acceptance: responsive layouts, keyboard use, error/cancel/reset and accessible controls pass; fixture versus live evidence is recorded.
  - Verify: browser report, full collection checks, tests and scoped Git review.
