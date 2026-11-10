# Reverse engineering: ai-avatar-demo

## Problem and reconstructed mechanism

Supply a conversational avatar with a memory-aware AI backend.

FastAPI backend services combine streamed LLM completion, Zep context and Anam session tokens; visual avatar rendering is excluded.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated turn -> retrieve scoped history/facts -> select context under budget -> model/tool response -> validated memory write
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | top-level workflow | UI reference |
| [backend.py](backend.py) | Message, ChatRequest, SessionCreateRequest, health_check, test_graph, create_zep_session, llm_stream, event_generator | config, fastapi, json, pydantic, services, time, typing |
| [config/settings.py](config/settings.py) | Settings, Config | pydantic_settings, typing |
| [scripts/ingest_to_graph.py](scripts/ingest_to_graph.py) | main | dotenv, json, os, pathlib, sys, time, zep_cloud |
| [services/anam_service.py](services/anam_service.py) | AnamService, create_session_token | config, httpx, typing |
| [services/llm_service.py](services/llm_service.py) | LLMService, stream_chat_completion | config, json, openai, typing |
| [services/zep_service.py](services/zep_service.py) | ZepService, create_user, create_thread, add_message, get_user_context, search_graph, add_to_graph | config, typing, zep_cloud |
| [zep_demo.ipynb#cell-15](zep_demo.ipynb#cell-15) | ask_with_knowledge |  |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [backend.py](backend.py) | 19 | Message | ClassDef |
| [backend.py](backend.py) | 24 | ChatRequest | ClassDef |
| [backend.py](backend.py) | 28 | SessionCreateRequest | ClassDef |
| [backend.py](backend.py) | 60 | health_check | AsyncFunctionDef |
| [backend.py](backend.py) | 65 | test_graph | Simple debug endpoint to verify Zep graph connectivity. |
| [backend.py](backend.py) | 86 | create_zep_session | Helper endpoint to create a Zep user + thread (session) for a given user_id. |
| [backend.py](backend.py) | 120 | llm_stream | Streaming LLM endpoint with Zep KG integration. |
| [backend.py](backend.py) | 148 | event_generator | Async generator that: |
| [config/settings.py](config/settings.py) | 6 | Settings | Application settings loaded from environment variables. |
| [config/settings.py](config/settings.py) | 22 | Config | ClassDef |
| [scripts/ingest_to_graph.py](scripts/ingest_to_graph.py) | 19 | main | Main function to ingest data to user graph. |
| [services/anam_service.py](services/anam_service.py) | 7 | AnamService | Service for interacting with Anam AI API. |
| [services/anam_service.py](services/anam_service.py) | 20 | create_session_token | Create a session token for initializing an Anam persona. |
| [services/llm_service.py](services/llm_service.py) | 7 | LLMService | Service for LLM interactions with Minimax M2 via OpenRouter. |
| [services/llm_service.py](services/llm_service.py) | 20 | stream_chat_completion | Stream chat completion from Minimax M2. |
| [services/zep_service.py](services/zep_service.py) | 9 | ZepService | Service for interacting with Zep Cloud (async-safe). |
| [services/zep_service.py](services/zep_service.py) | 20 | create_user | Create a new user in Zep. |
| [services/zep_service.py](services/zep_service.py) | 46 | create_thread | Create a new thread for a user. |
| [services/zep_service.py](services/zep_service.py) | 62 | add_message | Add a message to a thread. |
| [services/zep_service.py](services/zep_service.py) | 81 | get_user_context | Get user context from a thread using thread.get_user_context. |
| [services/zep_service.py](services/zep_service.py) | 112 | search_graph | Search the knowledge graph for a docs user (or provided user_id). |
| [services/zep_service.py](services/zep_service.py) | 145 | add_to_graph | Add data to a user's graph (docs user by default). |
| [zep_demo.ipynb#cell-15](zep_demo.ipynb#cell-15) | 1 | ask_with_knowledge | Simple function to query the knowledge graph and use Minimax M2 to generate a coherent response. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `minimax/minimax-m2`

Detected import roots: `anam_service`, `asyncio`, `config`, `dotenv`, `fastapi`, `httpx`, `json`, `llm_service`, `openai`, `os`, `pathlib`, `pydantic`, `pydantic_settings`, `services`, `settings`, `streamlit`, `sys`, `time`, `typing`, `zep_cloud`, `zep_service`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `ANAM_API_KEY`
- `ANAM_AVATAR_ID`
- `ANAM_VOICE_ID`
- `OPENROUTER_API_KEY`
- `ZEP_API_KEY`
- `ZEP_DOCS_USER_ID`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Redacted 1 possible credential literals (values not retained). |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [zep_demo.ipynb](zep_demo.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/ai-avatar-demo); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
