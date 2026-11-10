# Executable engineering learning extensions

This shared, standard-library Python 3.12 package powers the `enhance.py` launcher in all 113 project folders. It adds usable CPU reference operations and objective quality tools beside the original AI applications. Keep the collection layout; the launcher resolves its parent without depending on the current working directory.

From the collection root, run `./run.ps1 enhance` for all registered scenarios, or `./run.ps1 enhance --project gemma3-ocr`. From a project, run `python enhance.py check`, `doctor` or `--help`. No network calls or model downloads occur in these commands. Each project's `ENHANCEMENTS.md` explains its chosen contract, examples, original mechanism and deployment tradeoffs.

| Module | Contract and design choice |
| --- | --- |
| `evidence.py` | BM25 lexical reference, tenant filtering before scoring, explicit bounded context, source IDs/content hashes and versioned persistence. No semantic similarity or model answer claim. |
| `state.py` | SQLite transactions, owner-scoped reads, idempotency conflicts and legal state transitions; versioned correctable memory with expiry/deletion. Caller identity must be authenticated by the integrating app. |
| `safety.py` | Bounded arithmetic AST and exact JSON tool selection. No Python expression evaluation of model output. A standalone copy is used directly by database-memory-agent. |
| `validation.py` | Explicit JSON Schema subset, unsupported contracts fail closed; bounded read-only SQLite with authorizer, parameter binding and progress deadline. |
| `quality.py` | CER/WER, one-to-one region matching, paired bootstrap comparison, field rewards, split leakage and stable distillation loss. Scores consume supplied data rather than invented model responses. |
| `contracts.py` | Allowlisted typed local tools, explicit write authorization and stream terminal-state validation. Neither a remote MCP implementation nor an execution sandbox. |
| `artifacts.py` | Bounded declared-file manifest with containment, duplicate, empty file and checksum checks. Does not evaluate codec or model quality. |
| `doctor.py` | Inspect distribution metadata and variable presence without importing provider SDKs, printing secrets or pretending all optional requirements are mandatory. |
| `scenarios.py` | Negative, missing, isolation and recovery experiments selected by each project profile. Fixtures are labeled synthetic. |

Inputs use UTF-8 JSON with finite numbers. JSON inputs and persisted outputs are capped at 8 MiB; an oversized index must be segmented before saving. Result writes use a temporary file and atomic replacement. Subcommands return JSON; malformed inputs return 2, failed checks/schema or leakage checks return 1. Scores such as low OCR accuracy are measurements, not execution failures. Use `--output` on check/doctor/quality/compare/schema/reward/dataset/distill/stream-check to save a report.

For OCR/transcripts, `quality` accepts `{"reference":"...","prediction":"..."}` and optional `reference_regions`/`prediction_regions`, each containing objects with `box:[x1,y1,x2,y2]` and `text`. CER uses normalized Unicode characters; WER splits whitespace, which is not a universal language tokenizer. Empty-reference hallucinations have undefined (`null`) rates and nonzero edit counts. Region scores use maximum-cardinality matching at IoU 0.5 and exact NFC text, not average precision or formula equivalence. Large alignments are rejected; score pages/segments separately.

For training, `dataset` accepts a mapping of split names to lists of `{input,group?}`. `reward` accepts `{prediction,expected,schema}`. `distill` accepts `{teacher:[logits],student:[logits],target:class_index,temperature:2,alpha:0.5}` and computes `alpha*T²*KL(teacher||student)+(1-alpha)*CE(student,target)` without gradients. For evaluation, `compare` accepts `[{id,baseline,candidate}]`, with both scores in [0,1]. An interval from two synthetic cases is illustrative, not scientific evidence.

Job commands persist real local state, but do not execute the payload as an agent task. Use `job --operation create/show/running/failed/completed/cancelled`; memory commands use `remember/recall/forget`. Remote side effects, queues, worker leases, authentication, encryption, backup purges and distributed concurrency remain application responsibilities.

The architecture decision is recorded in [ADR-001](../docs/decisions/001-executable-learning-extensions.md). [Executed coverage](../docs/ENHANCEMENT_REPORT.md) is fingerprinted and checked by the collection verifier. Original application, GPU and provider compatibility remain distinct validation layers.

Implementation references: [Lucene BM25 parameters and positive IDF](https://lucene.apache.org/core/9_12_1/core/org/apache/lucene/search/similarities/BM25Similarity.html) inform the lexical reference; [Python SQLite authorizers and resource limits](https://docs.python.org/3.12/library/sqlite3.html#sqlite3.Connection.set_authorizer) define the local read-only adapter; [Unicode normalization](https://docs.python.org/3.12/library/unicodedata.html#unicodedata.normalize) defines canonical text equivalence. The CPU packaging uses [Dockerfile-specific context ignore rules](https://docs.docker.com/build/concepts/context/#filename-and-location) to include only shared Python source, this launcher's file and its profile; no original environments, credentials or uploaded documents are in the declared build context. These references establish API/algorithm intent, not runtime certification of the original projects.
