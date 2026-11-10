# Reverse engineering: document-chat-rag

## Problem and reconstructed mechanism

Build document-grounded question answering with local models and optional vector storage.

Notebook variants demonstrate index construction, local generation and retrieval/reranking choices.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, reset_chat, display_pdf | UI reference |
| [main_self_hosted_vectorDB.ipynb#cell-5](main_self_hosted_vectorDB.ipynb#cell-5) | create_index |  |
| [main_self_hosted_vectorDB.ipynb#cell-7](main_self_hosted_vectorDB.ipynb#cell-7) | top-level workflow |  |
| [rag_demo.ipynb#cell-5](rag_demo.ipynb#cell-5) | create_index |  |
| [rag_demo.ipynb#cell-6](rag_demo.ipynb#cell-6) | top-level workflow |  |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [main_self_hosted_vectorDB.ipynb#cell-5](main_self_hosted_vectorDB.ipynb#cell-5) | 8 | create_index | FunctionDef |
| [rag_demo.ipynb#cell-5](rag_demo.ipynb#cell-5) | 8 | create_index | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `cross-encoder/ms-marco-MiniLM-L-2-v2`
- `llama3.2:1b`
- `llama3.3`

Detected import roots: `IPython`, `base64`, `dotenv`, `gc`, `llama_index`, `nest_asyncio`, `os`, `qdrant_client`, `random`, `streamlit`, `tempfile`, `time`, `uuid`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [main_self_hosted_vectorDB.ipynb](main_self_hosted_vectorDB.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [rag_demo.ipynb](rag_demo.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [app.py](app.py) | 89 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |
| [main_self_hosted_vectorDB.ipynb#cell-7](main_self_hosted_vectorDB.ipynb#cell-7) | 5 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |
| [rag_demo.ipynb#cell-6](rag_demo.ipynb#cell-6) | 4 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/document-chat-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
