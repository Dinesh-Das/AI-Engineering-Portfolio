# Reverse engineering: web-browsing-agent

## Problem and reconstructed mechanism

Plan and execute browser research with CrewAI and Stagehand.

BrowserAutomationFlow creates an AutomationPlan, calls a browser tool and synthesizes results.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [flow.py](flow.py) | stagehand_browser_tool, BrowserAutomationFlowState, AutomationPlan, BrowserAutomationFlow, main, start_flow, plan_task, handle_browser_automation, synthesize_result | asyncio, crewai, dotenv, pydantic, stagehand_tool, typing |
| [stagehand_tool.py](stagehand_tool.py) | browser_automation | asyncio, nest_asyncio, os, stagehand |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [flow.py](flow.py) | 20 | stagehand_browser_tool | A tool that allows to interact with a web browser. |
| [flow.py](flow.py) | 35 | BrowserAutomationFlowState | ClassDef |
| [flow.py](flow.py) | 40 | AutomationPlan | ClassDef |
| [flow.py](flow.py) | 45 | BrowserAutomationFlow | A CrewAI Flow to intelligently handle browser automation tasks |
| [flow.py](flow.py) | 147 | main | AsyncFunctionDef |
| [flow.py](flow.py) | 52 | start_flow | FunctionDef |
| [flow.py](flow.py) | 57 | plan_task | FunctionDef |
| [flow.py](flow.py) | 94 | handle_browser_automation | FunctionDef |
| [flow.py](flow.py) | 122 | synthesize_result | FunctionDef |
| [stagehand_tool.py](stagehand_tool.py) | 11 | browser_automation | Performs automated browser tasks using AI agent capabilities. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `computer-use-preview`
- `gpt-4o`
- `ollama/gpt-oss`
- `openai/gpt-4`

Detected import roots: `asyncio`, `crewai`, `dotenv`, `nest_asyncio`, `os`, `pydantic`, `stagehand`, `stagehand_tool`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `MODEL_API_KEY`
- `OPENAI_API_KEY`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/web-browsing-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
