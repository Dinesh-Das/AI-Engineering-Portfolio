# Learnings and production deployment: agent2agent-demo

## The core lesson

An agent is a model-driven controller over tools and state. Its output is only as reliable as the tool contracts, termination rules and persisted state. Keep deterministic business calculations outside free-form generation and validate each state transition.

For this project specifically: Three python_a2a agents expose mathematical tools; the useful lesson is discovery, message routing and task responses.

## Rebuild it yourself

1. State the observable success condition: Understand agent-to-agent communication through sine, cosine and tangent services.
2. Read the source map in REVERSE_ENGINEERING.md and sketch the actual input, intermediate state, external dependency and output. Identify the smallest headless unit that implements the AI concept.
3. Reproduce that unit on a tiny, fixed, non-sensitive fixture. Save expected results before changing models, chunking, prompts, reward functions or tool policies.
4. Connect one external dependency at a time in an isolated environment. Record package versions and model revisions. A successful import or HTTP 200 does not demonstrate task correctness.
5. Add the project-specific failure experiment below. Check that errors are distinguishable from empty/low-confidence results and that retries do not duplicate side effects.
6. Run the same evaluation before and after each change. Save source revision, dataset ID, generation settings, quality, latency and cost together. Explain any tradeoff using observed evidence.

## Project-specific experiment

Exercise missing fields, nonnumeric arguments and tangent near a cosine zero; compare protocol errors with arithmetic errors.

Use a fixed fixture set, a baseline run and one controlled change. Include a normal case, a malformed/unsupported input and a dependency failure. Record the intermediate artifact that proves where a failure occurred, rather than inferring it from the final prose.

## What to measure

Task success on labeled scenarios; unauthorized-action rate; tool-call validity; recovery after a failed step; duplicate-side-effect rate; tokens and cost per successful task.

Quality targets depend on your domain and must be chosen before a release. This collection supplies a protocol and offline metric helpers, not fabricated passing model scores. See EVALUATION.md for a practical evidence log.

## Failure modes to understand

Unbounded delegation, repeated tool calls after retries, lost state on restart, prompt-injected tool instructions, and judging success by fluent prose instead of observable task completion.

Inspect the project's actual review leads in REVERSE_ENGINEERING.md. Fix a failure at its owning boundary: bad retrieval at the index/retriever, invalid data at the schema, unauthorized access at the tool/data service, and duplicate operations at the persisted job boundary.

## Better production deployment

Recommended project-specific direction (a proposal, not deployed infrastructure):

Use typed capability contracts and bounded calls; production discovery must authenticate the advertised agent endpoint.

Use a small stateless API to submit jobs and durable workers to execute long workflows. Persist step IDs, tool inputs and outcomes in a transactional store; use idempotency keys for external effects. Bound steps, concurrency, tokens and wall time. Separate read-only research tools from tools that publish or mutate data.

Use an authenticated entry boundary and a request/job ID. Persist required state outside application processes. Inject secrets at runtime, cap input size and external-call deadlines, and emit structured stage timings without copying private source content into logs. Run containers as an unprivileged user and use immutable, reviewed dependency/model artifacts.

For a small personal deployment, prefer the fewest processes that preserve these boundaries. For a shared deployment, add tenant authorization, job quotas, backups and tested restore. For GPU work, measure model load time, peak memory, batching and utilization before choosing instance capacity. Do not put long GPU training or document ingestion inside an unbounded web request.

## Deployment tradeoffs

A direct workflow is easier to debug than a large unconstrained agent crew. Add agents only when specialization improves measured task success. Durable orchestration adds operational cost but is justified when restart recovery and external side effects matter.

Estimate cost per successful task as model/API usage + embedding/parsing/media usage + compute/storage + failed/retried work. Include idle GPU time when comparing hosted and local inference. Report p50/p95 under representative concurrency and include cold-start behavior; a tutorial's isolated timing is not a service-level objective.

## Release and rollback evidence

- Establish a versioned evaluation set, baseline and explicit task-specific quality threshold.
- Verify malformed inputs, authorization failures, timeouts, restart recovery and repeated delivery.
- Resolve and audit a locked dependency set in the project's own environment; test its model/provider contract.
- Package application, prompt/tool/schema versions and model/index versions together in a release manifest.
- Canary a small workload; compare error rate, task success, latency and cost against the baseline.
- Keep the previous model/index/configuration available. Test restoring required state, not only restarting a process.

See [collection deployment playbook](../docs/DEPLOYMENT_PLAYBOOK.md) and [official reference links](../docs/SOURCES.md). Live inference, training and deployment remain unverified until you produce that evidence.
