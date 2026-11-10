# Learnings and production deployment: qwen3_vs_deepseek-r1

## The core lesson

A model comparison needs controlled inputs and a trustworthy success criterion. LLM judges can detect qualitative issues but also have position, style and model-family biases. For code and arithmetic, executable checks provide stronger evidence than prose preference.

For this project specifically: Shared LlamaIndex workflow and Opik experiments compare answer behavior on the same document tasks.

## Rebuild it yourself

1. State the observable success condition: Compare Qwen3 and DeepSeek on a common RAG evaluation pipeline.
2. Read the source map in REVERSE_ENGINEERING.md and sketch the actual input, intermediate state, external dependency and output. Identify the smallest headless unit that implements the AI concept.
3. Reproduce that unit on a tiny, fixed, non-sensitive fixture. Save expected results before changing models, chunking, prompts, reward functions or tool policies.
4. Connect one external dependency at a time in an isolated environment. Record package versions and model revisions. A successful import or HTTP 200 does not demonstrate task correctness.
5. Add the project-specific failure experiment below. Check that errors are distinguishable from empty/low-confidence results and that retries do not duplicate side effects.
6. Run the same evaluation before and after each change. Save source revision, dataset ID, generation settings, quality, latency and cost together. Explain any tradeoff using observed evidence.

## Project-specific experiment

Hold retrieved evidence fixed and score supported answers, abstention, latency and run-to-run variance.

Use a fixed fixture set, a baseline run and one controlled change. Include a normal case, a malformed/unsupported input and a dependency failure. Record the intermediate artifact that proves where a failure occurred, rather than inferring it from the final prose.

## What to measure

Task pass rate; supported-answer accuracy; judge/human agreement; run-to-run variance; cost per passing task; latency distributions and paired confidence intervals.

Quality targets depend on your domain and must be chosen before a release. This collection supplies a protocol and offline metric helpers, not fabricated passing model scores. See EVALUATION.md for a practical evidence log.

## Failure modes to understand

Different context budgets across candidates, grading the judge's own training examples, treating one response as a stable result, stale model aliases, and measuring only aggregate scores that hide failed task categories.

Inspect the project's actual review leads in REVERSE_ENGINEERING.md. Fix a failure at its owning boundary: bad retrieval at the index/retriever, invalid data at the schema, unauthorized access at the tool/data service, and duplicate operations at the persisted job boundary.

## Better production deployment

Recommended project-specific direction (a proposal, not deployed infrastructure):

Use a reproducible benchmark corpus and record generation settings, provider versions and judge prompts alongside results.

Use a queue-based evaluation runner and isolated execution workers for generated code. Store raw responses, task IDs, model revisions and grading configuration. Gate releases on agreed task-specific criteria; sample production traces separately to detect distribution drift.

Use an authenticated entry boundary and a request/job ID. Persist required state outside application processes. Inject secrets at runtime, cap input size and external-call deadlines, and emit structured stage timings without copying private source content into logs. Run containers as an unprivileged user and use immutable, reviewed dependency/model artifacts.

For a small personal deployment, prefer the fewest processes that preserve these boundaries. For a shared deployment, add tenant authorization, job quotas, backups and tested restore. For GPU work, measure model load time, peak memory, batching and utilization before choosing instance capacity. Do not put long GPU training or document ingestion inside an unbounded web request.

## Deployment tradeoffs

Hosted judges are easy to use but add cost and systematic bias. Human review is slower but useful for calibrating a small anchor set. Prefer exact checks for objectively verifiable tasks and judges for qualities that cannot be reduced to a deterministic test.

Estimate cost per successful task as model/API usage + embedding/parsing/media usage + compute/storage + failed/retried work. Include idle GPU time when comparing hosted and local inference. Report p50/p95 under representative concurrency and include cold-start behavior; a tutorial's isolated timing is not a service-level objective.

## Release and rollback evidence

- Establish a versioned evaluation set, baseline and explicit task-specific quality threshold.
- Verify malformed inputs, authorization failures, timeouts, restart recovery and repeated delivery.
- Resolve and audit a locked dependency set in the project's own environment; test its model/provider contract.
- Package application, prompt/tool/schema versions and model/index versions together in a release manifest.
- Canary a small workload; compare error rate, task success, latency and cost against the baseline.
- Keep the previous model/index/configuration available. Test restoring required state, not only restarting a process.

See [collection deployment playbook](../docs/DEPLOYMENT_PLAYBOOK.md) and [official reference links](../docs/SOURCES.md). Live inference, training and deployment remain unverified until you produce that evidence.
