# Learnings and production deployment: local-chatgpt with DeepSeek

## The core lesson

A chat UI is a distributed state machine over a model transport. Distinguish request acceptance, incremental output and successful completion. Keep model context separate from visible partial turns and preserve an inspectable path from browser input through provider payload to displayed output.

For this project specifically: An original Chainlit session stores messages; the reconstructed interface separates completed history from visible partial or failed turns.

## Rebuild it yourself

1. State the observable success condition: Understand local dialogue state and incremental DeepSeek responses.
2. Read the source map in REVERSE_ENGINEERING.md and sketch the actual input, intermediate state, external dependency and output. Identify the smallest headless unit that implements the AI concept.
3. Reproduce that unit on a tiny, fixed, non-sensitive fixture. Save expected results before changing models, chunking, prompts, reward functions or tool policies.
4. Connect one external dependency at a time in an isolated environment. Record package versions and model revisions. A successful import or HTTP 200 does not demonstrate task correctness.
5. Add the project-specific failure experiment below. Check that errors are distinguishable from empty/low-confidence results and that retries do not duplicate side effects.
6. Run the same evaluation before and after each change. Save source revision, dataset ID, generation settings, quality, latency and cost together. Explain any tradeoff using observed evidence.

## Project-specific experiment

Introduce a fact in one tab and ask a follow-up in another; verify isolation and compare failed-turn history behavior.

Use a fixed fixture set, a baseline run and one controlled change. Include a normal case, a malformed/unsupported input and a dependency failure. Record the intermediate artifact that proves where a failure occurred, rather than inferring it from the final prose.

## What to measure

Exact task correctness separately from perceived fluency; first-token and completion latency; output-token usage; cancellation/failure recovery; session isolation; keyboard access and responsive layout.

Quality targets depend on your domain and must be chosen before a release. This collection supplies a protocol and offline metric helpers, not fabricated passing model scores. See EVALUATION.md for a practical evidence log.

## Failure modes to understand

Replaying a completed answer as fake streaming, dropping content across split delimiters, blocking async handlers with synchronous inference, including incomplete turns in history, cross-tab state leakage and treating generated traces as proof of correctness.

Inspect the project's actual review leads in REVERSE_ENGINEERING.md. Fix a failure at its owning boundary: bad retrieval at the index/retriever, invalid data at the schema, unauthorized access at the tool/data service, and duplicate operations at the persisted job boundary.

## Learn from every scenario

| Scenario | Learning question | Evidence to retain |
| --- | --- | --- |
| Normal result | Did the mechanism achieve the project's stated goal? | Input, supporting source/tool evidence and independently checked output |
| Empty or unsupported input | Does the boundary reject or abstain clearly? | Validation outcome and proof no unnecessary expensive operation ran |
| Slow or failed dependency | Can the user distinguish pending, failed and complete work? | Stage/status, bounded deadline and recovery result |
| Cancellation or restart | What state is committed, and what remains incomplete? | Partial versus completed artifacts and replay/resume behavior |
| Repeated or concurrent requests | Can sessions leak data or side effects repeat? | Request/turn identity, isolation checks and duplicate-operation count |
| Changed model, data or UI | Which observed behavior actually changed? | Fixed baseline, one controlled variable and before/after task metrics |

Apply these questions to the project-specific experiment above. UI fixture evidence, live model quality, and production reliability are different observations; label each explicitly. Preserve your predicted outcome, observed result, explanation and next experiment rather than only saving a successful screenshot.

Keep personal records in [LEARNING_JOURNAL.md](LEARNING_JOURNAL.md). The generator never replaces an existing journal. UI note exports can be referenced from that file, while source-backed technical guides remain reproducible.

## Better production deployment

Recommended project-specific direction (a proposal, not deployed infrastructure):

Use authenticated session ownership and bounded asynchronous inference; keep durable conversation storage separate from model workers.

For learning, a loopback-only server and in-memory browser state make the system inspectable. For shared deployment, use an authenticated application service, per-user durable state, a bounded inference queue and independently provisioned model workers. Propagate cancellation and disconnects, apply input/image/token budgets and record request/turn IDs plus terminal status.

Use an authenticated entry boundary and a request/job ID. Persist required state outside application processes. Inject secrets at runtime, cap input size and external-call deadlines, and emit structured stage timings without copying private source content into logs. Run containers as an unprivileged user and use immutable, reviewed dependency/model artifacts.

For a small personal deployment, prefer the fewest processes that preserve these boundaries. For a shared deployment, add tenant authorization, job quotas, backups and tested restore. For GPU work, measure model load time, peak memory, batching and utilization before choosing instance capacity. Do not put long GPU training or document ingestion inside an unbounded web request.

## Deployment tradeoffs

Chainlit and Streamlit accelerate UI prototyping but couple lifecycle behavior to their session/runtime models. A small explicit transport teaches state and streaming clearly while requiring more UI code. Managed inference avoids local GPU operations; local models require measured memory, cold-start and concurrency planning.

Estimate cost per successful task as model/API usage + embedding/parsing/media usage + compute/storage + failed/retried work. Include idle GPU time when comparing hosted and local inference. Report p50/p95 under representative concurrency and include cold-start behavior; a tutorial's isolated timing is not a service-level objective.

## Release and rollback evidence

- Establish a versioned evaluation set, baseline and explicit task-specific quality threshold.
- Verify malformed inputs, authorization failures, timeouts, restart recovery and repeated delivery.
- Resolve and audit a locked dependency set in the project's own environment; test its model/provider contract.
- Package application, prompt/tool/schema versions and model/index versions together in a release manifest.
- Canary a small workload; compare error rate, task success, latency and cost against the baseline.
- Keep the previous model/index/configuration available. Test restoring required state, not only restarting a process.

See [collection deployment playbook](../docs/DEPLOYMENT_PLAYBOOK.md) and [official reference links](../docs/SOURCES.md). Live inference, training and deployment remain unverified until you produce that evidence.
