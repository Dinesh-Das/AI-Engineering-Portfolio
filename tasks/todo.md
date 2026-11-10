# Work checklist

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
