# Reverse engineering: mcp-agentic-rag

## Problem and reconstructed mechanism

Expose web-ingested retrieval through MCP using Bright Data and Qdrant.

Scraped content is embedded into a local collection and made searchable through server tools.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated client -> tool discovery -> argument validation -> authorized operation -> bounded backend call -> structured result
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [notebook.ipynb#cell-4](notebook.ipynb#cell-4) | batch_iterate, EmbedData, generate_embedding, embed | llama_index, tqdm |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | QdrantVDB, define_client, create_collection, ingest_data | qdrant_client |
| [notebook.ipynb#cell-8](notebook.ipynb#cell-8) | Retriever, search |  |
| [rag_code.py](rag_code.py) | batch_iterate, EmbedData, QdrantVDB, Retriever, generate_embedding, embed, define_client, create_collection, ingest_data, search | llama_index, qdrant_client, tqdm |
| [server.py](server.py) | machine_learning_faq_retrieval_tool, bright_data_web_search_tool | dotenv, mcp, os, rag_code, requests, ssl |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [notebook.ipynb#cell-4](notebook.ipynb#cell-4) | 4 | batch_iterate | FunctionDef |
| [notebook.ipynb#cell-4](notebook.ipynb#cell-4) | 8 | EmbedData | ClassDef |
| [notebook.ipynb#cell-4](notebook.ipynb#cell-4) | 25 | generate_embedding | FunctionDef |
| [notebook.ipynb#cell-4](notebook.ipynb#cell-4) | 28 | embed | FunctionDef |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | 4 | QdrantVDB | ClassDef |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | 11 | define_client | FunctionDef |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | 15 | create_collection | FunctionDef |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | 31 | ingest_data | FunctionDef |
| [notebook.ipynb#cell-8](notebook.ipynb#cell-8) | 1 | Retriever | ClassDef |
| [notebook.ipynb#cell-8](notebook.ipynb#cell-8) | 8 | search | FunctionDef |
| [rag_code.py](rag_code.py) | 68 | batch_iterate | FunctionDef |
| [rag_code.py](rag_code.py) | 72 | EmbedData | ClassDef |
| [rag_code.py](rag_code.py) | 106 | QdrantVDB | ClassDef |
| [rag_code.py](rag_code.py) | 149 | Retriever | ClassDef |
| [rag_code.py](rag_code.py) | 90 | generate_embedding | FunctionDef |
| [rag_code.py](rag_code.py) | 93 | embed | FunctionDef |
| [rag_code.py](rag_code.py) | 114 | define_client | FunctionDef |
| [rag_code.py](rag_code.py) | 118 | create_collection | FunctionDef |
| [rag_code.py](rag_code.py) | 134 | ingest_data | FunctionDef |
| [rag_code.py](rag_code.py) | 156 | search | FunctionDef |
| [server.py](server.py) | 12 | machine_learning_faq_retrieval_tool | Retrieve the most relevant documents from the machine learning |
| [server.py](server.py) | 34 | bright_data_web_search_tool | Search for information on a given topic using Bright Data. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `dotenv`, `llama_index`, `mcp`, `os`, `qdrant_client`, `rag_code`, `requests`, `ssl`, `tqdm`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `BRIGHT_DATA_PASSWORD`
- `BRIGHT_DATA_USERNAME`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [server.py](server.py) | Added explicit connection/read timeouts to 1 direct requests calls. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [notebook.ipynb#cell-4](notebook.ipynb#cell-4) | 20 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |
| [rag_code.py](rag_code.py) | 84 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/mcp-agentic-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
