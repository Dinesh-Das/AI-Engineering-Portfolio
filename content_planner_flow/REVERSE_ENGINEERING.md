# Reverse engineering: content_planner_flow

## Problem and reconstructed mechanism

Plan social content from web material and schedule a draft.

CrewAI Flow moves through scraping, platform-specific draft creation, plan saving and Typefully scheduling.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [notebook.ipynb#cell-6](notebook.ipynb#cell-6) | top-level workflow |  |
| [notebook.ipynb#cell-12](notebook.ipynb#cell-12) | Tweet, Thread |  |
| [notebook.ipynb#cell-16](notebook.ipynb#cell-16) | LinkedInPost |  |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | ContentPlanningState, CreateContentPlanningFlow, scrape_blog_post, select_platform, twitter_draft, linkedin_draft, save_plan, publish | crewai |
| [scheduler.py](scheduler.py) | json_to_typefully_content, json_to_linkedin_content, schedule_thread, schedule | datetime, json, os, pydantic, requests, typing |
| [config/planner_agents.yaml](config/planner_agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [config/planner_tasks.yaml](config/planner_tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [notebook.ipynb#cell-12](notebook.ipynb#cell-12) | 1 | Tweet | Represents an individual tweet in a thread |
| [notebook.ipynb#cell-12](notebook.ipynb#cell-12) | 7 | Thread | Represents a Twitter thread |
| [notebook.ipynb#cell-16](notebook.ipynb#cell-16) | 1 | LinkedInPost | Represents a LinkedIn post |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 3 | ContentPlanningState | State for the content planning flow |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 12 | CreateContentPlanningFlow | ClassDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 16 | scrape_blog_post | FunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 30 | select_platform | FunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 37 | twitter_draft | FunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 46 | linkedin_draft | FunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 54 | save_plan | FunctionDef |
| [notebook.ipynb#cell-20](notebook.ipynb#cell-20) | 59 | publish | FunctionDef |
| [scheduler.py](scheduler.py) | 15 | json_to_typefully_content | Convert JSON thread format to Typefully's format with 4 newlines between tweets. |
| [scheduler.py](scheduler.py) | 27 | json_to_linkedin_content | Convert JSON thread format to Typefully's format. |
| [scheduler.py](scheduler.py) | 34 | schedule_thread | Schedule a thread on Typefully. |
| [scheduler.py](scheduler.py) | 62 | schedule | Schedule a thread from a Pydantic model. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/llama3.2`

Detected import roots: `IPython`, `crewai`, `crewai_tools`, `datetime`, `dotenv`, `firecrawl`, `getpass`, `json`, `nest_asyncio`, `os`, `pathlib`, `pydantic`, `requests`, `scheduler`, `subprocess`, `typing`, `uuid`, `yaml`

Retained dependency manifests: [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `OPENAI_API_KEY`
- `TYPEFULLY_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [scheduler.py](scheduler.py) | Added explicit connection/read timeouts to 1 direct requests calls. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/content_planner_flow); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
