# Reverse engineering: sonnet4-vs-qwen3-coder

## Problem and reconstructed mechanism

Evaluate Claude and Qwen3-Coder against repository-grounded tasks.

Parallel response generation and DeepEval scoring are supplemented by a batch-comparison notebook.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned task set -> identical context/settings -> candidate generation -> blinded grading -> independent executable checks -> paired comparison
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | handle_chat_input, process_claude_stream, process_qwen3_coder_stream | UI surface |
| [code_evaluation.py](code_evaluation.py) | evaluate_code | deepeval, typing |
| [code_ingestion.py](code_ingestion.py) | ingest_github_repo | gitingest, typing |
| [model_service.py](model_service.py) | get_model_response_async, get_parallel_responses, get_model_responses | asyncio, litellm, os, typing |
| [notebook.ipynb#cell-1](notebook.ipynb#cell-1) | get_full_response, process_single_query, process_queries, process_queries_sync | asyncio, code_evaluation, code_ingestion, dotenv, model_service, nest_asyncio, os, typing |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | create_results_table, display_results_table, display_formatted_table | numpy, pandas, typing |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 96 | handle_chat_input | AsyncFunctionDef |
| [app.py](app.py) | 115 | process_claude_stream | AsyncFunctionDef |
| [app.py](app.py) | 123 | process_qwen3_coder_stream | AsyncFunctionDef |
| [code_evaluation.py](code_evaluation.py) | 7 | evaluate_code | FunctionDef |
| [code_ingestion.py](code_ingestion.py) | 4 | ingest_github_repo | FunctionDef |
| [model_service.py](model_service.py) | 6 | get_model_response_async | AsyncFunctionDef |
| [model_service.py](model_service.py) | 51 | get_parallel_responses | AsyncFunctionDef |
| [model_service.py](model_service.py) | 57 | get_model_responses | FunctionDef |
| [notebook.ipynb#cell-1](notebook.ipynb#cell-1) | 11 | get_full_response | Get a complete response from a model (non-streaming) |
| [notebook.ipynb#cell-1](notebook.ipynb#cell-1) | 23 | process_single_query | Process a single query and return results for both models |
| [notebook.ipynb#cell-1](notebook.ipynb#cell-1) | 67 | process_queries | Process a list of queries against a GitHub repository |
| [notebook.ipynb#cell-1](notebook.ipynb#cell-1) | 94 | process_queries_sync | Synchronous wrapper for process_queries - works in Jupyter notebooks |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 5 | create_results_table | Create a formatted table from evaluation results |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 48 | display_results_table | Display the results table with formatting |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 72 | display_formatted_table | Display formatted table with styling (for Jupyter notebooks) |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `asyncio`, `code_evaluation`, `code_ingestion`, `deepeval`, `dotenv`, `gitingest`, `litellm`, `model_service`, `nest_asyncio`, `numpy`, `os`, `pandas`, `plotly`, `streamlit`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/sonnet4-vs-qwen3-coder); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
