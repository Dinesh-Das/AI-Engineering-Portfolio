# Reverse engineering: github-rag

## Problem and reconstructed mechanism

Answer repository questions after GitIngest converts source to retrieval context.

GitHub URL validation and ingestion feed a local LlamaIndex query engine; the original entry points are UI-bound.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | GitHubRAGError, validate_github_url, get_repo_name, reset_chat, process_with_gitingets, create_query_engine | UI surface |
| [app_local.py](app_local.py) | load_llm, reset_chat, process_with_gitingets | UI surface |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 25 | GitHubRAGError | Custom exception for GitHub RAG application errors |
| [app.py](app.py) | 29 | validate_github_url | Validate GitHub repository URL |
| [app.py](app.py) | 33 | get_repo_name | Extract repository name from URL |
| [app.py](app.py) | 40 | reset_chat | Reset chat session and clean up resources |
| [app.py](app.py) | 51 | process_with_gitingets | Process GitHub repository using gitingest |
| [app.py](app.py) | 62 | create_query_engine | Create and configure query engine |
| [app_local.py](app_local.py) | 27 | load_llm | FunctionDef |
| [app_local.py](app_local.py) | 31 | reset_chat | FunctionDef |
| [app_local.py](app_local.py) | 36 | process_with_gitingets | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `llama3.2`

Detected import roots: `dotenv`, `gc`, `gitingest`, `llama_index`, `logging`, `os`, `pandas`, `streamlit`, `tempfile`, `typing`, `uuid`

Retained dependency manifests: [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [app_local.py](app_local.py) | 79 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/github-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
