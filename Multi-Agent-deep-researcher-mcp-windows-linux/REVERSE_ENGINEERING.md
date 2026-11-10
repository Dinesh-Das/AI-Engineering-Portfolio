# Reverse engineering: Multi-Agent-deep-researcher-mcp-windows-linux

## Problem and reconstructed mechanism

Expose a local multi-agent research crew through MCP.

Linkup-backed search tools feed a CrewAI research crew and a server entry point.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agents.py](agents.py) | get_llm_client, LinkUpSearchInput, LinkUpSearchTool, create_research_crew, run_research | crewai, dotenv, linkup, os, pydantic, typing |
| [app.py](app.py) | reset_chat | UI reference |
| [server.py](server.py) | crew_research | agents, asyncio, mcp |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [agents.py](agents.py) | 13 | get_llm_client | Initialize and return the LLM client |
| [agents.py](agents.py) | 23 | LinkUpSearchInput | Input schema for LinkUp Search Tool. |
| [agents.py](agents.py) | 32 | LinkUpSearchTool | ClassDef |
| [agents.py](agents.py) | 58 | create_research_crew | Create and configure the research crew with all agents and tasks |
| [agents.py](agents.py) | 129 | run_research | Run the research process and return results |
| [server.py](server.py) | 9 | crew_research | Run CrewAI-based research system for given user query. Can do both standard and deep web search. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/deepseek-r1:7b`

Detected import roots: `agents`, `asyncio`, `crewai`, `dotenv`, `linkup`, `mcp`, `os`, `pydantic`, `streamlit`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `LINKUP_API_KEY`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/Multi-Agent-deep-researcher-mcp-windows-linux); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
