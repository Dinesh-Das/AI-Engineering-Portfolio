# Learnings and production deployment: deploy-agentic-rag

## The core lesson

An AI system's operational boundaries determine whether experiments can become a dependable service. Model artifacts, APIs, tool permissions and data stores have different lifecycle and scaling requirements; keeping those boundaries explicit makes failures recoverable.

For this project specifically: AgenticRAGAPI separates setup, request decoding, prediction and response encoding; a client exercises the service.

## Rebuild it yourself

1. State the observable success condition: Serve an agentic RAG workflow through an API using LitServe.
2. Read the source map in REVERSE_ENGINEERING.md and sketch the actual input, intermediate state, external dependency and output. Identify the smallest headless unit that implements the AI concept.
3. Reproduce that unit on a tiny, fixed, non-sensitive fixture. Save expected results before changing models, chunking, prompts, reward functions or tool policies.
4. Connect one external dependency at a time in an isolated environment. Record package versions and model revisions. A successful import or HTTP 200 does not demonstrate task correctness.
5. Add the project-specific failure experiment below. Check that errors are distinguishable from empty/low-confidence results and that retries do not duplicate side effects.
6. Run the same evaluation before and after each change. Save source revision, dataset ID, generation settings, quality, latency and cost together. Explain any tradeoff using observed evidence.

## Project-specific experiment

Send malformed requests and concurrent queries while indexing is unavailable; distinguish readiness from process liveness.

Use a fixed fixture set, a baseline run and one controlled change. Include a normal case, a malformed/unsupported input and a dependency failure. Record the intermediate artifact that proves where a failure occurred, rather than inferring it from the final prose.

## What to measure

Startup/readiness behavior; recovery after restart; artifact integrity; unauthorized mutation rejection; queue depth, error rate and cost per completed operation.

Quality targets depend on your domain and must be chosen before a release. This collection supplies a protocol and offline metric helpers, not fabricated passing model scores. See EVALUATION.md for a practical evidence log.

## Failure modes to understand

Mutable artifact tags, process-local state behind multiple replicas, publishing credentials in tool environments, missing backups, and relying on a process health check that does not test its dependencies.

Inspect the project's actual review leads in REVERSE_ENGINEERING.md. Fix a failure at its owning boundary: bad retrieval at the index/retriever, invalid data at the schema, unauthorized access at the tool/data service, and duplicate operations at the persisted job boundary.

## Better production deployment

Recommended project-specific direction (a proposal, not deployed infrastructure):

Deploy stateless API replicas behind authentication and rate limits; keep model and vector services independently scalable.

Begin with an isolated container or VM appropriate to the workload and persist important state outside it. Run as an unprivileged user, inject secrets at runtime, restrict egress and distinguish liveness/readiness. Use immutable artifacts and a tested rollback path.

Use an authenticated entry boundary and a request/job ID. Persist required state outside application processes. Inject secrets at runtime, cap input size and external-call deadlines, and emit structured stage timings without copying private source content into logs. Run containers as an unprivileged user and use immutable, reviewed dependency/model artifacts.

For a small personal deployment, prefer the fewest processes that preserve these boundaries. For a shared deployment, add tenant authorization, job quotas, backups and tested restore. For GPU work, measure model load time, peak memory, batching and utilization before choosing instance capacity. Do not put long GPU training or document ingestion inside an unbounded web request.

## Deployment tradeoffs

A managed container service reduces routine operations for stateless APIs. A private VM can fit local model or tool requirements but adds patching, backup and capacity responsibilities. Introduce orchestration only after the workload warrants it.

Estimate cost per successful task as model/API usage + embedding/parsing/media usage + compute/storage + failed/retried work. Include idle GPU time when comparing hosted and local inference. Report p50/p95 under representative concurrency and include cold-start behavior; a tutorial's isolated timing is not a service-level objective.

## Release and rollback evidence

- Establish a versioned evaluation set, baseline and explicit task-specific quality threshold.
- Verify malformed inputs, authorization failures, timeouts, restart recovery and repeated delivery.
- Resolve and audit a locked dependency set in the project's own environment; test its model/provider contract.
- Package application, prompt/tool/schema versions and model/index versions together in a release manifest.
- Canary a small workload; compare error rate, task success, latency and cost against the baseline.
- Keep the previous model/index/configuration available. Test restoring required state, not only restarting a process.

See [collection deployment playbook](../docs/DEPLOYMENT_PLAYBOOK.md) and [official reference links](../docs/SOURCES.md). Live inference, training and deployment remain unverified until you produce that evidence.
