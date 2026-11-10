# Reverse engineering: simple-rag-workflow

## Problem and reconstructed mechanism

Learn the ingestion, retrieval and synthesis stages of a minimal RAG system.

A LlamaIndex workflow emits retrieval events and synthesizes from selected nodes; separate notebooks cover evaluation.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [evaluation.ipynb#cell-4](evaluation.ipynb#cell-4) | load_workflow | asyncio, workflow |
| [evaluation.ipynb#cell-5](evaluation.ipynb#cell-5) | top-level workflow |  |
| [evaluation.ipynb#cell-15](evaluation.ipynb#cell-15) | my_llm_application, evaluation_task | opik |
| [workflow.ipynb#cell-2](workflow.ipynb#cell-2) | top-level workflow | llama_index |
| [workflow.ipynb#cell-3](workflow.ipynb#cell-3) | RetrieverEvent | llama_index |
| [workflow.ipynb#cell-4](workflow.ipynb#cell-4) | RAGWorkflow, ingest, retrieve, synthesize | llama_index |
| [workflow.py](workflow.py) | RetrieverEvent, RAGWorkflow, main, ingest, retrieve, synthesize, query, ingest_documents | asyncio, llama_index, nest_asyncio |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [evaluation.ipynb#cell-4](evaluation.ipynb#cell-4) | 4 | load_workflow | FunctionDef |
| [evaluation.ipynb#cell-15](evaluation.ipynb#cell-15) | 4 | my_llm_application | AsyncFunctionDef |
| [evaluation.ipynb#cell-15](evaluation.ipynb#cell-15) | 8 | evaluation_task | FunctionDef |
| [workflow.ipynb#cell-3](workflow.ipynb#cell-3) | 5 | RetrieverEvent | Result of running retrieval |
| [workflow.ipynb#cell-4](workflow.ipynb#cell-4) | 11 | RAGWorkflow | ClassDef |
| [workflow.ipynb#cell-4](workflow.ipynb#cell-4) | 13 | ingest | Entry point to ingest a document, triggered by a StartEvent with `dirname`. |
| [workflow.ipynb#cell-4](workflow.ipynb#cell-4) | 26 | retrieve | Entry point for RAG, triggered by a StartEvent with `query`. |
| [workflow.ipynb#cell-4](workflow.ipynb#cell-4) | 52 | synthesize | Return a streaming response using reranked nodes. |
| [workflow.py](workflow.py) | 13 | RetrieverEvent | Result of running retrieval |
| [workflow.py](workflow.py) | 17 | RAGWorkflow | ClassDef |
| [workflow.py](workflow.py) | 82 | main | AsyncFunctionDef |
| [workflow.py](workflow.py) | 31 | ingest | Entry point to ingest documents from a directory. |
| [workflow.py](workflow.py) | 42 | retrieve | Entry point for RAG retrieval. |
| [workflow.py](workflow.py) | 60 | synthesize | Generate a response using retrieved nodes. |
| [workflow.py](workflow.py) | 67 | query | Helper method to perform a complete RAG query. |
| [workflow.py](workflow.py) | 75 | ingest_documents | Helper method to ingest documents. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-small-en-v1.5`
- `Gemma3`
- `gemma3`
- `llama3.2`

Detected import roots: `asyncio`, `dotenv`, `importlib`, `llama_index`, `nest_asyncio`, `opik`, `pandas`, `pathlib`, `sys`, `workflow`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [evaluation.ipynb](evaluation.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [workflow.ipynb](workflow.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/corpus.json](enhancement/examples/corpus.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/simple-rag-workflow); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
