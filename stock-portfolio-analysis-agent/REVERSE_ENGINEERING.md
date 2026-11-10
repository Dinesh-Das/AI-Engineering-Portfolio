# Reverse engineering: stock-portfolio-analysis-agent

## Problem and reconstructed mechanism

Stream a portfolio-analysis workflow from a CrewAI backend.

StockAnalysisFlow coordinates data gathering, simulation, allocation and insights and emits AG-UI-compatible events.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agent/main.py](agent/main.py) | AgentState, crewai_agent, main, event_generator, emit_event | ag_ui, asyncio, copilotkit, fastapi, os, stock_analysis, typing, uuid |
| [agent/stock_analysis.py](agent/stock_analysis.py) | StockAnalysisFlow, convert_tool_call, start, chat, simulation, allocation, insights, end | ag_ui, asyncio, crewai, datetime, dotenv, json, litellm, numpy |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [agent/main.py](agent/main.py) | 51 | AgentState | Agent state class that manages the data throughout the stock analysis workflow. |
| [agent/main.py](agent/main.py) | 78 | crewai_agent | Main API endpoint for processing stock analysis requests. |
| [agent/main.py](agent/main.py) | 346 | main | Main function to start the uvicorn server. |
| [agent/main.py](agent/main.py) | 96 | event_generator | Asynchronous generator that streams events to the client in real-time. |
| [agent/main.py](agent/main.py) | 115 | emit_event | Callback function for the workflow to emit events |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 163 | StockAnalysisFlow | Main workflow class that orchestrates the stock analysis process. |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 1036 | convert_tool_call | Utility function to convert OpenAI tool call format to our internal format |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 176 | start | Step 1: Initialize the workflow |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 189 | chat | Step 2: Parse user input and extract investment parameters |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 296 | simulation | Step 3: Gather historical stock data for analysis |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 456 | allocation | Step 4: Calculate portfolio allocation and performance simulation |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 919 | insights | Step 5: Generate bull/bear insights about the selected stocks |
| [agent/stock_analysis.py](agent/stock_analysis.py) | 1022 | end | Step 6: Final step - return the complete state |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o-mini`

Detected import roots: `ag_ui`, `asyncio`, `copilotkit`, `crewai`, `datetime`, `dotenv`, `fastapi`, `json`, `litellm`, `numpy`, `openai`, `os`, `pandas`, `prompts`, `pydantic`, `stock_analysis`, `typing`, `uuid`, `uvicorn`, `yfinance`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `OPENAI_API_KEY`
- `PORT`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/stock-portfolio-analysis-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
