# Reverse engineering: financial-analyst-deepseek

## Problem and reconstructed mechanism

Expose stock analysis and generated plots through a local-model MCP workflow.

CrewAI analysis calls market-data tools, writes code artifacts and can execute generated code for plotting.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [building-financial-analyst.ipynb#cell-3](building-financial-analyst.ipynb#cell-3) | QueryAnalysisOutput | pydantic |
| [building-financial-analyst.ipynb#cell-4](building-financial-analyst.ipynb#cell-4) | top-level workflow |  |
| [finance_crew.py](finance_crew.py) | QueryAnalysisOutput, run_financial_analysis | crewai, crewai_tools, dotenv, json, os, pydantic, re, yfinance |
| [server.py](server.py) | analyze_stock, save_code, run_code_and_show_plot | finance_crew, mcp |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [building-financial-analyst.ipynb#cell-3](building-financial-analyst.ipynb#cell-3) | 3 | QueryAnalysisOutput | Structured output for the query analysis task. |
| [finance_crew.py](finance_crew.py) | 13 | QueryAnalysisOutput | Structured output for the query analysis task. |
| [finance_crew.py](finance_crew.py) | 95 | run_financial_analysis | FunctionDef |
| [server.py](server.py) | 8 | analyze_stock | Analyzes stock market data based on the query and generates executable Python code for analysis and visualization. |
| [server.py](server.py) | 35 | save_code | Expects a nicely formatted, working and executable python code as input in form of a string.  |
| [server.py](server.py) | 54 | run_code_and_show_plot | Run the code in stock_analysis.py and generate the plot |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/deepseek-r1:7b`

Detected import roots: `crewai`, `crewai_tools`, `dotenv`, `finance_crew`, `json`, `mcp`, `os`, `pydantic`, `re`, `yfinance`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [building-financial-analyst.ipynb](building-financial-analyst.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [building-financial-analyst.ipynb#cell-4](building-financial-analyst.ipynb#cell-4) | 47 | allow_code_execution | allow_code_execution=True crosses a code-execution trust boundary. |
| [finance_crew.py](finance_crew.py) | 70 | allow_code_execution | allow_code_execution=True crosses a code-execution trust boundary. |
| [server.py](server.py) | 59 | code-execution | Review inputs to exec; untrusted data can execute code. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/financial-analyst-deepseek); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
