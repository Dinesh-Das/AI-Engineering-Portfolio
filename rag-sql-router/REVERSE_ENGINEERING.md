# Reverse engineering: rag-sql-router

## Problem and reconstructed mechanism

Route questions between document retrieval and structured SQL tools.

A custom tool-gathering workflow chooses a document query engine or database query path.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat, get_database_connection, get_table_data, get_table_schema, create_population_chart, create_state_distribution_chart, create_population_scatter, render_database_tab, initialize_model, handle_file_upload, initialize_workflow, process_query | UI surface |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | top-level workflow | llama_index |
| [notebook.ipynb#cell-10](notebook.ipynb#cell-10) | create_docs_query_engine | llama_index |
| [notebook.ipynb#cell-12](notebook.ipynb#cell-12) | create_codex_project | cleanlab_codex |
| [notebook.ipynb#cell-16](notebook.ipynb#cell-16) | document_query_tool |  |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | InputEvent, GatherToolsEvent, ToolCallEvent, ToolCallEventResult, RouterOutputAgentWorkflow, reset, prepare_chat, chat, dispatch_calls, call_tool, gather | llama_index, typing |
| [tools.py](tools.py) | create_codex_project, get_or_create_codex_project, get_codex_project_info, setup_sql_tool, setup_document_tool, document_query_tool | cleanlab_codex, llama_index, os, sqlalchemy, uuid |
| [workflow.py](workflow.py) | InputEvent, GatherToolsEvent, ToolCallEvent, ToolCallEventResult, RouterOutputAgentWorkflow, reset, prepare_chat, chat, dispatch_calls, call_tool, gather | asyncio, llama_index, typing |
| [workflow_all_flows.html](workflow_all_flows.html) | backend/configuration source; inspect directly | .html |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 72 | reset_chat | Reset the chat history and clear context |
| [app.py](app.py) | 86 | get_database_connection | Create a database connection |
| [app.py](app.py) | 101 | get_table_data | Get data from the specified table |
| [app.py](app.py) | 116 | get_table_schema | Get the schema of the specified table |
| [app.py](app.py) | 132 | create_population_chart | Create a population chart using Plotly |
| [app.py](app.py) | 159 | create_state_distribution_chart | Create a state distribution chart |
| [app.py](app.py) | 179 | create_population_scatter | Create a scatter plot of cities by population |
| [app.py](app.py) | 203 | render_database_tab | Render the database visualization tab |
| [app.py](app.py) | 373 | initialize_model | Initialize models for LLM and embedding |
| [app.py](app.py) | 386 | handle_file_upload | Function to handle multiple file uploads with temporary directory |
| [app.py](app.py) | 427 | initialize_workflow | Initialize workflow with the given tools |
| [app.py](app.py) | 438 | process_query | Function to process a query using the workflow |
| [app.py](app.py) | 526 | main | FunctionDef |
| [notebook.ipynb#cell-10](notebook.ipynb#cell-10) | 6 | create_docs_query_engine | FunctionDef |
| [notebook.ipynb#cell-12](notebook.ipynb#cell-12) | 4 | create_codex_project | FunctionDef |
| [notebook.ipynb#cell-16](notebook.ipynb#cell-16) | 1 | document_query_tool | FunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 15 | InputEvent | Input event. |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 19 | GatherToolsEvent | Gather Tools Event |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 25 | ToolCallEvent | Tool Call event |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 31 | ToolCallEventResult | Tool call event result. |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 37 | RouterOutputAgentWorkflow | Custom router output agent workflow. |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 60 | reset | Resets Chat History |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 65 | prepare_chat | AsyncFunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 76 | chat | Appends msg to chat history, then gets tool calls. |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 108 | dispatch_calls | Dispatches calls. |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 120 | call_tool | Calls tool. |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 144 | gather | Gathers tool calls. |
| [tools.py](tools.py) | 24 | create_codex_project | Create a Codex project for document validation. |
| [tools.py](tools.py) | 54 | get_or_create_codex_project | Get existing Codex project or create a new one for the session. |
| [tools.py](tools.py) | 72 | get_codex_project_info | Get information about the current Codex project for debugging. |
| [tools.py](tools.py) | 104 | setup_sql_tool | Setup SQL query tool for querying city database. |
| [tools.py](tools.py) | 138 | setup_document_tool | Setup document query tool from uploaded documents with Codex validation. |
| [tools.py](tools.py) | 191 | document_query_tool | Query documents with Codex validation for enhanced accuracy. |
| [workflow.py](workflow.py) | 21 | InputEvent | Input event. |
| [workflow.py](workflow.py) | 25 | GatherToolsEvent | Gather Tools Event |
| [workflow.py](workflow.py) | 31 | ToolCallEvent | Tool Call event |
| [workflow.py](workflow.py) | 37 | ToolCallEventResult | Tool call event result. |
| [workflow.py](workflow.py) | 43 | RouterOutputAgentWorkflow | Custom router output agent workflow. |
| [workflow.py](workflow.py) | 69 | reset | Resets Chat History |
| [workflow.py](workflow.py) | 74 | prepare_chat | AsyncFunctionDef |
| [workflow.py](workflow.py) | 85 | chat | Appends msg to chat history, then gets tool calls. |
| [workflow.py](workflow.py) | 120 | dispatch_calls | Dispatches calls. |
| [workflow.py](workflow.py) | 132 | call_tool | Calls tool. |
| [workflow.py](workflow.py) | 204 | gather | Gathers tool calls. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-small-en-v1.5`
- `qwen/qwen-turbo`

Detected import roots: `IPython`, `ast`, `asyncio`, `cleanlab_codex`, `llama_index`, `nest_asyncio`, `os`, `pandas`, `plotly`, `random`, `shutil`, `sqlalchemy`, `streamlit`, `tempfile`, `time`, `tools`, `torch`, `typing`, `uuid`, `workflow`

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
| [.streamlit/config.toml](.streamlit/config.toml) | Restored frontend source/asset after UI scope was authorized. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/rag-sql-router); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
