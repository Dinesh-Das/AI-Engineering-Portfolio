# Reverse engineering: stagehand x mcp-use

## Problem and reconstructed mechanism

Connect a local agent to browser-automation tools through MCP.

Stagehand tools are exposed through a server and consumed by an mcp-use agent wrapper; presentation tracking displays those tool lifecycle events.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agent_wrapper.py](agent_wrapper.py) | ToolCallTracker, StreamingMCPAgent, create_streaming_agent, start_tool_call, complete_tool_call, get_current_tools, get_completed_tools, next_step, run_with_streaming, patched_run | UI surface |
| [app.py](app.py) | handle_activate, handle_clear, run_agent, run_streaming_agent | UI surface |
| [server.py](server.py) | main | asyncio, langchain_openai, mcp_use |
| [stagehand_mcp.py](stagehand_mcp.py) | browser_automation_tool, add_numbers | mcp, stagehand_tool |
| [stagehand_tool.py](stagehand_tool.py) | browser_automation | asyncio, nest_asyncio, os, stagehand |
| [styles.py](styles.py) | inject_css | UI surface |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [agent_wrapper.py](agent_wrapper.py) | 13 | ToolCallTracker | Tracks tool calls and provides updates for the UI. |
| [agent_wrapper.py](agent_wrapper.py) | 62 | StreamingMCPAgent | Wrapper around MCPAgent to provide streaming tool updates. |
| [agent_wrapper.py](agent_wrapper.py) | 153 | create_streaming_agent | Create a streaming wrapper for the given MCPAgent. |
| [agent_wrapper.py](agent_wrapper.py) | 21 | start_tool_call | Start tracking a new tool call. |
| [agent_wrapper.py](agent_wrapper.py) | 33 | complete_tool_call | Complete a tool call with result or error. |
| [agent_wrapper.py](agent_wrapper.py) | 48 | get_current_tools | Get currently executing tools. |
| [agent_wrapper.py](agent_wrapper.py) | 52 | get_completed_tools | Get completed tools for current step. |
| [agent_wrapper.py](agent_wrapper.py) | 56 | next_step | Move to next step, clear current tools. |
| [agent_wrapper.py](agent_wrapper.py) | 81 | run_with_streaming | Run agent with streaming updates to UI containers. |
| [agent_wrapper.py](agent_wrapper.py) | 75 | patched_run | AsyncFunctionDef |
| [app.py](app.py) | 57 | handle_activate | FunctionDef |
| [app.py](app.py) | 79 | handle_clear | FunctionDef |
| [app.py](app.py) | 109 | run_agent | FunctionDef |
| [app.py](app.py) | 115 | run_streaming_agent | Run agent with streaming tool updates. |
| [server.py](server.py) | 5 | main | AsyncFunctionDef |
| [stagehand_mcp.py](stagehand_mcp.py) | 10 | browser_automation_tool | Perform browser automation. |
| [stagehand_mcp.py](stagehand_mcp.py) | 31 | add_numbers | Add two numbers together. |
| [stagehand_tool.py](stagehand_tool.py) | 11 | browser_automation | Performs automated browser tasks using AI agent capabilities. |
| [styles.py](styles.py) | 5 | inject_css | FunctionDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `computer-use-preview`
- `gpt-4o`
- `gpt-4o-mini`

Detected import roots: `agent_wrapper`, `asyncio`, `base64`, `dotenv`, `importlib`, `inspect`, `json`, `langchain_openai`, `mcp`, `mcp_use`, `nest_asyncio`, `os`, `pathlib`, `stagehand`, `stagehand_tool`, `streamlit`, `styles`, `sys`, `time`, `typing`, `warnings`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `BROWSERBASE_API_KEY`
- `BROWSERBASE_PROJECT_ID`
- `DEBUG_MCP`
- `MODEL_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/mcp-use.png](assets/mcp-use.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/stagehand.png](assets/stagehand.png) | Restored frontend source/asset after UI scope was authorized. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/payload.json](enhancement/examples/payload.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/stagehand%20x%20mcp-use); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
