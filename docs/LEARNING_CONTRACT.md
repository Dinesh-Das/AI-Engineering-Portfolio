# Learning is part of every project

The user explicitly requires the learning aspect to be preserved in every scenario. A working interface, copied notebook or passing syntax check is not a substitute for understanding. Every catalog project must retain the following substantive sections in LEARNINGS.md:

1. The core lesson: the AI/systems mechanism and its key distinction.
2. Rebuild it yourself: a sequence from a small fixed fixture to the integrated workflow.
3. Project-specific experiment: a controlled change and a testable hypothesis.
4. What to measure: task correctness, relevant quality metrics, latency and cost.
5. Failure modes to understand: where the mechanism breaks and which boundary owns the fix.
6. Better production deployment: a proposed architecture suited to the workload.
7. Deployment tradeoffs: alternatives and the evidence needed to choose between them.
8. Release and rollback evidence: what must be verified before claiming readiness.
9. Learn from every scenario: distinguish normal, invalid, failed, interrupted, repeated/concurrent and changed-system behavior with evidence.

`tools.learning_contract` validates these sections during `run.ps1 check` and `run.ps1 verify`. Documentation generation preserves project-specific notes and adds exercises for normal inputs, unsupported input, slow/failed dependencies, cancellation/restart, concurrent/repeated requests and changed models/data/UI.

For each experiment preserve four things: **prediction, observation, explanation, next experiment**. Keep the upstream source, local changes and evidence distinguishable so you can explain what changed and why. A model-provided trace is an artifact to inspect, not proof the answer is correct.

Every catalog project also has a personal LEARNING_JOURNAL.md. The generator creates it only when absent; it never overwrites an existing journal. Keep personal learning records there and link exported UI notes or other evidence, while the generated technical guides remain reproducible. This preservation behavior has a regression test.

UI projects also expose an experiment desk and exportable notes. Fixture mode is labeled; UI correctness, provider integration, model quality and production reliability are separate evidence categories.

The completed OCR projects belong to the user's existing work. Their files and learning material are preserved and linked in LOCAL_OCR_PROJECTS.md; the collection does not overwrite them with generated notes or claim they were retested.
