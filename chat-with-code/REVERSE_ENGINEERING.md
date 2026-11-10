# Reverse engineering: chat-with-code

## Problem and reconstructed mechanism

Retrieve repository context for code questions and validate responses.

The notebook ingests repository files, builds a LlamaIndex index and uses Qwen3-Coder with validation helpers.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, initialize_codex_project, parse_github_url, clone_repo, validate_owner_repo, parse_docs_by_file_types, create_index, reset_chat | UI surface |
| [notebook.ipynb#cell-9](notebook.ipynb#cell-9) | top-level workflow |  |
| [notebook.ipynb#cell-11](notebook.ipynb#cell-11) | parse_github_url, clone_github_repo, validate_owner_repo, parse_docs_by_file_types, create_index |  |
| [notebook.ipynb#cell-13](notebook.ipynb#cell-13) | setup_query_engine |  |
| [notebook.ipynb#cell-19](notebook.ipynb#cell-19) | codex_validated_query |  |
| [validation.py](validation.py) | codex_validated_query |  |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 31 | load_llm | FunctionDef |
| [app.py](app.py) | 38 | initialize_codex_project | FunctionDef |
| [app.py](app.py) | 53 | parse_github_url | Parse the GitHub URL to extract owner and repository name. |
| [app.py](app.py) | 60 | clone_repo | Clone the GitHub repository. |
| [app.py](app.py) | 67 | validate_owner_repo | Validate the owner and repository name. |
| [app.py](app.py) | 72 | parse_docs_by_file_types | Parse documents by file types in the specified directory. |
| [app.py](app.py) | 91 | create_index | Create a Milvus collection and return a vectorstore index. |
| [app.py](app.py) | 117 | reset_chat | Reset the chat state. |
| [notebook.ipynb#cell-11](notebook.ipynb#cell-11) | 1 | parse_github_url | FunctionDef |
| [notebook.ipynb#cell-11](notebook.ipynb#cell-11) | 6 | clone_github_repo | FunctionDef |
| [notebook.ipynb#cell-11](notebook.ipynb#cell-11) | 14 | validate_owner_repo | FunctionDef |
| [notebook.ipynb#cell-11](notebook.ipynb#cell-11) | 17 | parse_docs_by_file_types | FunctionDef |
| [notebook.ipynb#cell-11](notebook.ipynb#cell-11) | 39 | create_index | FunctionDef |
| [notebook.ipynb#cell-13](notebook.ipynb#cell-13) | 1 | setup_query_engine | FunctionDef |
| [notebook.ipynb#cell-19](notebook.ipynb#cell-19) | 4 | codex_validated_query | FunctionDef |
| [validation.py](validation.py) | 6 | codex_validated_query | Validates a user query against a RAG pipeline response using Cleanlab Codex. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-base-en-v1.5`
- `qwen/qwen3-coder:free`

Detected import roots: `IPython`, `cleanlab_codex`, `dotenv`, `gc`, `glob`, `importlib`, `llama_index`, `nest_asyncio`, `os`, `pathlib`, `re`, `streamlit`, `subprocess`, `sys`, `time`, `uuid`, `validation`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `CODEX_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/chat-with-code); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
