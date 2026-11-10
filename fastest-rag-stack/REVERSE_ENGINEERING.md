# Reverse engineering: fastest-rag-stack

## Problem and reconstructed mechanism

Combine quantized Qdrant retrieval with SambaNova-hosted generation.

Embedding, binary-quantized storage, retrieval and synthesis are distinct classes in rag_code.py.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned embedding model -> candidate index -> top-N candidates -> optional precise reranking -> top-k evidence -> generator
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat, display_pdf | UI surface |
| [notebook.ipynb#cell-5](notebook.ipynb#cell-5) | create_index |  |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | top-level workflow |  |
| [notebook.ipynb#cell-13](notebook.ipynb#cell-13) | top-level workflow |  |
| [rag_code.py](rag_code.py) | batch_iterate, EmbedData, QdrantVDB_QB, Retriever, RAG, generate_embedding, embed, define_client, create_collection, ingest_data, search, generate_context | llama_index, qdrant_client |
| [sambanova.ipynb#cell-1](sambanova.ipynb#cell-1) | top-level workflow | dotenv, llama_index |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 28 | reset_chat | FunctionDef |
| [app.py](app.py) | 34 | display_pdf | FunctionDef |
| [notebook.ipynb#cell-5](notebook.ipynb#cell-5) | 8 | create_index | FunctionDef |
| [rag_code.py](rag_code.py) | 11 | batch_iterate | Yield successive n-sized chunks from lst. |
| [rag_code.py](rag_code.py) | 16 | EmbedData | ClassDef |
| [rag_code.py](rag_code.py) | 39 | QdrantVDB_QB | ClassDef |
| [rag_code.py](rag_code.py) | 80 | Retriever | ClassDef |
| [rag_code.py](rag_code.py) | 109 | RAG | ClassDef |
| [rag_code.py](rag_code.py) | 28 | generate_embedding | FunctionDef |
| [rag_code.py](rag_code.py) | 31 | embed | FunctionDef |
| [rag_code.py](rag_code.py) | 46 | define_client | FunctionDef |
| [rag_code.py](rag_code.py) | 50 | create_collection | FunctionDef |
| [rag_code.py](rag_code.py) | 67 | ingest_data | FunctionDef |
| [rag_code.py](rag_code.py) | 87 | search | FunctionDef |
| [rag_code.py](rag_code.py) | 140 | generate_context | FunctionDef |
| [rag_code.py](rag_code.py) | 153 | query | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `Meta-Llama-3.1-405B-Instruct`
- `Meta-Llama-3.3-70B-Instruct`

Detected import roots: `IPython`, `base64`, `dotenv`, `gc`, `llama_index`, `nest_asyncio`, `openai`, `os`, `qdrant_client`, `rag_code`, `random`, `streamlit`, `tempfile`, `time`, `uuid`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `SAMBANOVA_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [notebook.ipynb](notebook.ipynb) | Fixed unmatched closing parenthesis in notebook cell 23. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [sambanova.ipynb](sambanova.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | 5 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |
| [rag_code.py](rag_code.py) | 25 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/fastest-rag-stack); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
