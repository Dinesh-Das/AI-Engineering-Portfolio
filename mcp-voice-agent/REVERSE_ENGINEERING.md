# Reverse engineering: mcp-voice-agent

## Problem and reconstructed mechanism

Give a LiveKit voice agent MCP-backed web and database tools.

Tool schemas are adapted into LiveKit-compatible callables and the voice session invokes them during dialogue.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
audio stream/upload -> ASR with timestamps -> turn/segment state -> retrieval or analysis -> model output -> TTS or structured notes
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agent.py](agent.py) | schema_to_google_docstring, firecrawl_search, build_livekit_tools, entrypoint, make_proxy, proxy | __future__, asyncio, copy, dotenv, firecrawl, inspect, json, livekit |
| [setup.sh](setup.sh) | backend/configuration source; inspect directly | .sh |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [agent.py](agent.py) | 75 | schema_to_google_docstring | Generate a Google-style docstring section from a JSON schema. |
| [agent.py](agent.py) | 107 | firecrawl_search | Search the web via Firecrawl. |
| [agent.py](agent.py) | 143 | build_livekit_tools | Build LiveKit tools from a Supabase MCP server. |
| [agent.py](agent.py) | 223 | entrypoint | Main entrypoint for the LiveKit agent. |
| [agent.py](agent.py) | 169 | make_proxy | FunctionDef |
| [agent.py](agent.py) | 175 | proxy | AsyncFunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o`

Detected import roots: `__future__`, `asyncio`, `copy`, `dotenv`, `firecrawl`, `inspect`, `json`, `livekit`, `logging`, `os`, `pydantic_ai`, `typing`

Retained dependency manifests: [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_URL`
- `OPENAI_API_KEY`
- `SUPABASE_ACCESS_TOKEN`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/mcp-voice-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
