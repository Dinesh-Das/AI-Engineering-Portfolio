# Reverse engineering: qwen3_vs_deepseek-r1

## Problem and reconstructed mechanism

Compare Qwen3 and DeepSeek on a common RAG evaluation pipeline.

Shared LlamaIndex workflow and Opik experiments compare answer behavior on the same document tasks.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned task set -> identical context/settings -> candidate generation -> blinded grading -> independent executable checks -> paired comparison
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, reset_chat, display_pdf | UI surface |
| [evaluation.ipynb#cell-4](evaluation.ipynb#cell-4) | load_llm | llama_index, os |
| [evaluation.ipynb#cell-5](evaluation.ipynb#cell-5) | top-level workflow |  |
| [evaluation.ipynb#cell-14](evaluation.ipynb#cell-14) | top-level workflow | llama_index |
| [evaluation.ipynb#cell-15](evaluation.ipynb#cell-15) | my_llm_application, evaluation_task | opik |
| [workflow.py](workflow.py) | RetrieverEvent, RAGWorkflow, main, ingest, retrieve, synthesize, query, ingest_documents | asyncio, llama_index, nest_asyncio, os |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 33 | load_llm | FunctionDef |
| [app.py](app.py) | 39 | reset_chat | FunctionDef |
| [app.py](app.py) | 44 | display_pdf | FunctionDef |
| [evaluation.ipynb#cell-4](evaluation.ipynb#cell-4) | 4 | load_llm | FunctionDef |
| [evaluation.ipynb#cell-15](evaluation.ipynb#cell-15) | 4 | my_llm_application | FunctionDef |
| [evaluation.ipynb#cell-15](evaluation.ipynb#cell-15) | 8 | evaluation_task | FunctionDef |
| [workflow.py](workflow.py) | 17 | RetrieverEvent | Result of running retrieval |
| [workflow.py](workflow.py) | 21 | RAGWorkflow | ClassDef |
| [workflow.py](workflow.py) | 91 | main | AsyncFunctionDef |
| [workflow.py](workflow.py) | 40 | ingest | Entry point to ingest documents from a directory. |
| [workflow.py](workflow.py) | 51 | retrieve | Entry point for RAG retrieval. |
| [workflow.py](workflow.py) | 69 | synthesize | Generate a response using retrieved nodes. |
| [workflow.py](workflow.py) | 76 | query | Helper method to perform a complete RAG query. |
| [workflow.py](workflow.py) | 84 | ingest_documents | Helper method to ingest documents. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `Qwen3`
- `deepseek-r1`
- `nomic-ai/nomic-embed-text-v1`
- `qwen3`

Detected import roots: `IPython`, `asyncio`, `base64`, `dotenv`, `gc`, `importlib`, `llama_index`, `nest_asyncio`, `opik`, `os`, `pandas`, `pathlib`, `random`, `streamlit`, `sys`, `tempfile`, `time`, `uuid`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [evaluation.ipynb](evaluation.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/groq-logo.png](assets/groq-logo.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/linkup.png](assets/linkup.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/llamaindex.png](assets/llamaindex.png) | Restored frontend source/asset after UI scope was authorized. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/pairs.json](enhancement/examples/pairs.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/qwen3_vs_deepseek-r1); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
