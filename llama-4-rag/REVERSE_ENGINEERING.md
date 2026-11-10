# Reverse engineering: llama-4-rag

## Problem and reconstructed mechanism

Use a hosted Llama 4 model in a local document-retrieval workflow.

RAGWorkflow embeds documents, retrieves evidence and synthesizes with provider-specific model configuration.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, reset_chat, display_pdf | UI surface |
| [workflow.py](workflow.py) | RetrieverEvent, RAGWorkflow, main, ingest, retrieve, synthesize, query, ingest_documents | asyncio, llama_index, nest_asyncio, os |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 34 | load_llm | FunctionDef |
| [app.py](app.py) | 40 | reset_chat | FunctionDef |
| [app.py](app.py) | 45 | display_pdf | FunctionDef |
| [workflow.py](workflow.py) | 11 | RetrieverEvent | Result of running retrieval |
| [workflow.py](workflow.py) | 15 | RAGWorkflow | ClassDef |
| [workflow.py](workflow.py) | 83 | main | AsyncFunctionDef |
| [workflow.py](workflow.py) | 32 | ingest | Entry point to ingest documents from a directory. |
| [workflow.py](workflow.py) | 43 | retrieve | Entry point for RAG retrieval. |
| [workflow.py](workflow.py) | 61 | synthesize | Generate a response using retrieved nodes. |
| [workflow.py](workflow.py) | 68 | query | Helper method to perform a complete RAG query. |
| [workflow.py](workflow.py) | 76 | ingest_documents | Helper method to ingest documents. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8`
- `meta-llama/llama-4-scout-17b-16e-instruct`

Detected import roots: `IPython`, `asyncio`, `base64`, `dotenv`, `gc`, `llama_index`, `nest_asyncio`, `os`, `random`, `streamlit`, `tempfile`, `time`, `uuid`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `CEREBRAS_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/cerebras.png](assets/cerebras.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/download.png](assets/download.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/llamaindex.png](assets/llamaindex.png) | Restored frontend source/asset after UI scope was authorized. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/llama-4-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
