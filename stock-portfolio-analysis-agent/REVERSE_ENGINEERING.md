# Reverse engineering: stock-portfolio-analysis-agent

## Problem and reconstructed mechanism

Stream a portfolio-analysis workflow from a CrewAI backend.

StockAnalysisFlow coordinates data gathering, simulation, allocation and insights and emits AG-UI-compatible events.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agent/main.py](agent/main.py) | AgentState, crewai_agent, main, event_generator, emit_event | ag_ui, asyncio, copilotkit, fastapi, os, stock_analysis, typing, uuid |
| [agent/stock_analysis.py](agent/stock_analysis.py) | StockAnalysisFlow, convert_tool_call, start, chat, simulation, allocation, insights, end | ag_ui, asyncio, crewai, datetime, dotenv, json, litellm, numpy |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |
| [frontend/next-env.d.ts](frontend/next-env.d.ts) | backend/configuration source; inspect directly | .ts |
| [frontend/next.config.ts](frontend/next.config.ts) | backend/configuration source; inspect directly | .ts |
| [frontend/pnpm-lock.yaml](frontend/pnpm-lock.yaml) | backend/configuration source; inspect directly | .yaml |
| [frontend/postcss.config.mjs](frontend/postcss.config.mjs) | backend/configuration source; inspect directly | .mjs |
| [frontend/src/app/api/copilotkit/route.ts](frontend/src/app/api/copilotkit/route.ts) | backend/configuration source; inspect directly | .ts |
| [frontend/src/app/components/cash-panel.tsx](frontend/src/app/components/cash-panel.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/chart-components/allocation-table.tsx](frontend/src/app/components/chart-components/allocation-table.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/chart-components/bar-chart.tsx](frontend/src/app/components/chart-components/bar-chart.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/chart-components/insight-card.tsx](frontend/src/app/components/chart-components/insight-card.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/chart-components/line-chart.tsx](frontend/src/app/components/chart-components/line-chart.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/chart-components/section-title.tsx](frontend/src/app/components/chart-components/section-title.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/component-tree.tsx](frontend/src/app/components/component-tree.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/generative-canvas.tsx](frontend/src/app/components/generative-canvas.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/prompt-panel.tsx](frontend/src/app/components/prompt-panel.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/theme-provider.tsx](frontend/src/app/components/theme-provider.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/components/tool-logs.tsx](frontend/src/app/components/tool-logs.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/globals.css](frontend/src/app/globals.css) | backend/configuration source; inspect directly | .css |
| [frontend/src/app/layout.tsx](frontend/src/app/layout.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/app/page.tsx](frontend/src/app/page.tsx) | backend/configuration source; inspect directly | .tsx |
| [frontend/src/utils/prompts.ts](frontend/src/utils/prompts.ts) | backend/configuration source; inspect directly | .ts |

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
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o-mini`

Detected import roots: `ag_ui`, `asyncio`, `copilotkit`, `crewai`, `datetime`, `dotenv`, `fastapi`, `importlib`, `json`, `litellm`, `numpy`, `openai`, `os`, `pandas`, `pathlib`, `prompts`, `pydantic`, `stock_analysis`, `sys`, `typing`, `uuid`, `uvicorn`, `yfinance`

Retained dependency manifests: [pyproject.toml](pyproject.toml), [frontend/package.json](frontend/package.json)

Environment names detected from code/configuration:

- `NEXT_PUBLIC_CREWAI_URL`
- `OPENAI_API_KEY`
- `PORT`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [frontend/.env.example](frontend/.env.example) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/next-env.d.ts](frontend/next-env.d.ts) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/next.config.ts](frontend/next.config.ts) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/package.json](frontend/package.json) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/pnpm-lock.yaml](frontend/pnpm-lock.yaml) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/postcss.config.mjs](frontend/postcss.config.mjs) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/api/copilotkit/route.ts](frontend/src/app/api/copilotkit/route.ts) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/cash-panel.tsx](frontend/src/app/components/cash-panel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/chart-components/allocation-table.tsx](frontend/src/app/components/chart-components/allocation-table.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/chart-components/bar-chart.tsx](frontend/src/app/components/chart-components/bar-chart.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/chart-components/insight-card.tsx](frontend/src/app/components/chart-components/insight-card.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/chart-components/line-chart.tsx](frontend/src/app/components/chart-components/line-chart.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/chart-components/section-title.tsx](frontend/src/app/components/chart-components/section-title.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/component-tree.tsx](frontend/src/app/components/component-tree.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/generative-canvas.tsx](frontend/src/app/components/generative-canvas.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/prompt-panel.tsx](frontend/src/app/components/prompt-panel.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/theme-provider.tsx](frontend/src/app/components/theme-provider.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/components/tool-logs.tsx](frontend/src/app/components/tool-logs.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/favicon.ico](frontend/src/app/favicon.ico) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/globals.css](frontend/src/app/globals.css) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/layout.tsx](frontend/src/app/layout.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/app/page.tsx](frontend/src/app/page.tsx) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/src/utils/prompts.ts](frontend/src/utils/prompts.ts) | Restored frontend source/asset after UI scope was authorized. |
| [frontend/tsconfig.json](frontend/tsconfig.json) | Restored frontend source/asset after UI scope was authorized. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/stock-portfolio-analysis-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
