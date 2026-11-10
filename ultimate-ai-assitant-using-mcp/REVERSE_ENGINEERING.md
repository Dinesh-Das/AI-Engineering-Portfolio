# Reverse engineering: ultimate-ai-assitant-using-mcp

## Problem and reconstructed mechanism

Explore one agent connecting to several MCP servers.

mcp-use client configuration and agent creation connect local/hosted models to a union of tools.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated client -> tool discovery -> argument validation -> authorized operation -> bounded backend call -> structured result
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [mcp_streamlit_app.py](mcp_streamlit_app.py) | reset_chat, create_mcp_client, create_agent, run_agent_query | UI surface |
| [server.py](server.py) | main | asyncio, dotenv, langchain_ollama, langchain_openai, mcp_use, os, warnings |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [mcp_streamlit_app.py](mcp_streamlit_app.py) | 38 | reset_chat | FunctionDef |
| [mcp_streamlit_app.py](mcp_streamlit_app.py) | 43 | create_mcp_client | Create MCPClient from configuration dictionary. |
| [mcp_streamlit_app.py](mcp_streamlit_app.py) | 52 | create_agent | Create MCPAgent with the client. |
| [mcp_streamlit_app.py](mcp_streamlit_app.py) | 65 | run_agent_query | Run a query through the MCP agent. |
| [server.py](server.py) | 13 | main | AsyncFunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o`

Detected import roots: `asyncio`, `base64`, `dotenv`, `json`, `langchain_ollama`, `langchain_openai`, `mcp_use`, `os`, `streamlit`, `warnings`

Retained dependency manifests: [pyproject.toml](pyproject.toml), [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `OPENAI_API_KEY`
- `RAGIE_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/ultimate-ai-assitant-using-mcp); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
