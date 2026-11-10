# Reverse engineering: documentation-writer-flow

## Problem and reconstructed mechanism

Produce repository documentation through planning and writing agents.

A workflow clones code, produces a documentation plan and dispatches writing tasks; MCP exposes the process as a tool.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-3](Building_Code_Documentation_Agents_Local.ipynb#cell-3) | load_llm | crewai |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-10](Building_Code_Documentation_Agents_Local.ipynb#cell-10) | DocItem, DocPlan |  |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-16](Building_Code_Documentation_Agents_Local.ipynb#cell-16) | check_mermaid_syntax | crewai, re |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-17](Building_Code_Documentation_Agents_Local.ipynb#cell-17) | top-level workflow | crewai_tools |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | DocumentationState, CreateDocumentationFlow, clone_repo, plan_docs, save_plan, create_docs | typing |
| [crew.py](crew.py) | initialize_planning_crew, initialize_documentation_crew | crewai, crewai_tools, schemas, utils |
| [documentation_flow.py](documentation_flow.py) | DocumentationState, CreateDocumentationFlow, clone_repo, plan_docs, save_plan, create_docs | crew, crewai, pathlib, pydantic, shutil, subprocess, typing, utils |
| [main.py](main.py) | run_doc_flow | documentation_flow, nest_asyncio |
| [schemas/models.py](schemas/models.py) | DocItem, DocPlan | pydantic, typing |
| [server.py](server.py) | write_documentation, list_docs, view_content | main, mcp, pathlib, typing |
| [utils.py](utils.py) | load_yaml_config, load_llm, check_mermaid_syntax, remove_readonly | crewai, os, re, stat, yaml |
| [config/documentation_agents.yaml](config/documentation_agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [config/documentation_tasks.yaml](config/documentation_tasks.yaml) | backend/configuration source; inspect directly | .yaml |
| [config/planner_agents.yaml](config/planner_agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [config/planner_tasks.yaml](config/planner_tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-3](Building_Code_Documentation_Agents_Local.ipynb#cell-3) | 3 | load_llm | FunctionDef |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-10](Building_Code_Documentation_Agents_Local.ipynb#cell-10) | 2 | DocItem | Represents a documentation item |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-10](Building_Code_Documentation_Agents_Local.ipynb#cell-10) | 10 | DocPlan | Documentation plan |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-16](Building_Code_Documentation_Agents_Local.ipynb#cell-16) | 4 | check_mermaid_syntax | FunctionDef |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | 5 | DocumentationState | State for the documentation flow |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | 13 | CreateDocumentationFlow | ClassDef |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | 17 | clone_repo | FunctionDef |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | 34 | plan_docs | FunctionDef |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | 43 | save_plan | FunctionDef |
| [Building_Code_Documentation_Agents_Local.ipynb#cell-19](Building_Code_Documentation_Agents_Local.ipynb#cell-19) | 48 | create_docs | FunctionDef |
| [crew.py](crew.py) | 17 | initialize_planning_crew | FunctionDef |
| [crew.py](crew.py) | 57 | initialize_documentation_crew | FunctionDef |
| [documentation_flow.py](documentation_flow.py) | 10 | DocumentationState | State for the documentation flow |
| [documentation_flow.py](documentation_flow.py) | 18 | CreateDocumentationFlow | ClassDef |
| [documentation_flow.py](documentation_flow.py) | 21 | clone_repo | FunctionDef |
| [documentation_flow.py](documentation_flow.py) | 39 | plan_docs | FunctionDef |
| [documentation_flow.py](documentation_flow.py) | 49 | save_plan | FunctionDef |
| [documentation_flow.py](documentation_flow.py) | 58 | create_docs | FunctionDef |
| [main.py](main.py) | 6 | run_doc_flow | FunctionDef |
| [schemas/models.py](schemas/models.py) | 5 | DocItem | Represents a documentation item |
| [schemas/models.py](schemas/models.py) | 13 | DocPlan | Documentation plan |
| [server.py](server.py) | 10 | write_documentation | Generates the documentation for the given GitHub repository URL. |
| [server.py](server.py) | 32 | list_docs | Lists the documentation files that are generated successfully. |
| [server.py](server.py) | 51 | view_content | Displays the content of a generated documentation file. |
| [utils.py](utils.py) | 9 | load_yaml_config | FunctionDef |
| [utils.py](utils.py) | 14 | load_llm | FunctionDef |
| [utils.py](utils.py) | 22 | check_mermaid_syntax | FunctionDef |
| [utils.py](utils.py) | 38 | remove_readonly | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `nomic-embed-text`
- `ollama/deepseek-r1:7b`
- `ollama/llama3.2`

Detected import roots: `IPython`, `crew`, `crewai`, `crewai_tools`, `documentation_flow`, `main`, `mcp`, `nest_asyncio`, `os`, `pathlib`, `pydantic`, `re`, `schemas`, `shutil`, `stat`, `subprocess`, `typing`, `utils`, `yaml`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [Building_Code_Documentation_Agents_Local.ipynb](Building_Code_Documentation_Agents_Local.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/documentation-writer-flow); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
