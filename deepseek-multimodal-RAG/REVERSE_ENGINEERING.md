# Reverse engineering: deepseek-multimodal-RAG

## Problem and reconstructed mechanism

Retrieve PDF pages visually and answer with DeepSeek Janus-Pro.

ColPali page embeddings are stored in Qdrant; selected page images become multimodal generation context.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat, display_pdf | UI reference |
| [rag_code.py](rag_code.py) | batch_iterate, image_to_base64, EmbedData, QdrantVDB_QB, Retriever, RAG, get_query_embedding, generate_embedding, embed, define_client, create_collection, ingest_data | Janus, base64, colpali_engine, io, qdrant_client, torch, tqdm, transformers |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [rag_code.py](rag_code.py) | 12 | batch_iterate | Yield successive n-sized chunks from lst. |
| [rag_code.py](rag_code.py) | 17 | image_to_base64 | FunctionDef |
| [rag_code.py](rag_code.py) | 24 | EmbedData | ClassDef |
| [rag_code.py](rag_code.py) | 69 | QdrantVDB_QB | ClassDef |
| [rag_code.py](rag_code.py) | 114 | Retriever | ClassDef |
| [rag_code.py](rag_code.py) | 138 | RAG | ClassDef |
| [rag_code.py](rag_code.py) | 44 | get_query_embedding | FunctionDef |
| [rag_code.py](rag_code.py) | 53 | generate_embedding | FunctionDef |
| [rag_code.py](rag_code.py) | 60 | embed | FunctionDef |
| [rag_code.py](rag_code.py) | 76 | define_client | FunctionDef |
| [rag_code.py](rag_code.py) | 80 | create_collection | FunctionDef |
| [rag_code.py](rag_code.py) | 97 | ingest_data | FunctionDef |
| [rag_code.py](rag_code.py) | 121 | search | FunctionDef |
| [rag_code.py](rag_code.py) | 158 | generate_context | FunctionDef |
| [rag_code.py](rag_code.py) | 163 | query | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `IPython`, `Janus`, `base64`, `colpali_engine`, `gc`, `io`, `numpy`, `os`, `pdf2image`, `qdrant_client`, `rag_code`, `random`, `streamlit`, `tempfile`, `time`, `torch`, `tqdm`, `transformers`, `uuid`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [rag_code.py](rag_code.py) | 33 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |
| [rag_code.py](rag_code.py) | 154 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/deepseek-multimodal-RAG); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
