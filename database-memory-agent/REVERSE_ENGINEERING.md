# Reverse engineering: database-memory-agent

## Problem and reconstructed mechanism

Combine conversation history, semantic document search and tool selection in MongoDB.

Voyage embeddings support Atlas vector search; OpenAI chooses tools and generates responses using stored session history.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated turn -> retrieve scoped history/facts -> select context under budget -> model/tool response -> validated memory write
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat, display_pdf, check_vector_index, process_pdf_upload, ingest_sample_data | UI reference |
| [config.py](config.py) | top-level workflow | dotenv, openai, os, pymongo, voyageai |
| [ingest_data.py](ingest_data.py) | get_embedding, ingest_data | config, langchain_community, langchain_text_splitters, pymongo, time |
| [memory.py](memory.py) | store_chat_message, retrieve_session_history | config, datetime, typing |
| [planning.py](planning.py) | tool_selector, generate_response, get_llm_response | config, memory, tools |
| [tools.py](tools.py) | vector_search_tool, calculator_tool | config, ingest_data |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [ingest_data.py](ingest_data.py) | 7 | get_embedding | FunctionDef |
| [ingest_data.py](ingest_data.py) | 13 | ingest_data | FunctionDef |
| [memory.py](memory.py) | 5 | store_chat_message | FunctionDef |
| [memory.py](memory.py) | 14 | retrieve_session_history | FunctionDef |
| [planning.py](planning.py) | 5 | tool_selector | FunctionDef |
| [planning.py](planning.py) | 46 | generate_response | FunctionDef |
| [planning.py](planning.py) | 85 | get_llm_response | FunctionDef |
| [tools.py](tools.py) | 4 | vector_search_tool | FunctionDef |
| [tools.py](tools.py) | 32 | calculator_tool | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o`
- `voyage-3-large`

Detected import roots: `base64`, `config`, `datetime`, `dotenv`, `ingest_data`, `io`, `langchain_community`, `langchain_text_splitters`, `memory`, `openai`, `os`, `planning`, `pymongo`, `streamlit`, `sys`, `time`, `tools`, `typing`, `uuid`, `voyageai`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `MONGODB_URI`
- `OPENAI_API_KEY`
- `VOYAGE_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Redacted 2 possible credential literals (values not retained). |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [planning.py](planning.py) | 41 | code-execution | Review inputs to eval; untrusted data can execute code. |
| [tools.py](tools.py) | 34 | code-execution | Review inputs to eval; untrusted data can execute code. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/database-memory-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
