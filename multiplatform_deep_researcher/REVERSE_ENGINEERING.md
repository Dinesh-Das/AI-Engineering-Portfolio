# Reverse engineering: multiplatform_deep_researcher

## Problem and reconstructed mechanism

Research a question through platform-specific source specialists.

DeepResearchFlow collects URLs, dispatches specialists by source type and synthesizes their structured output.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat | UI surface |
| [flow.py](flow.py) | URLBuckets, SpecialistOutput, DeepResearchFlowState, server_params, DeepResearchFlow, main, start_flow, collect_urls, dispatch_to_specialists, synthesize_response | asyncio, crewai, crewai_tools, dotenv, json, logging, mcp, os |
| [research.py](research.py) | run_deep_research | flow, typing |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 18 | reset_chat | FunctionDef |
| [flow.py](flow.py) | 20 | URLBuckets | ClassDef |
| [flow.py](flow.py) | 28 | SpecialistOutput | ClassDef |
| [flow.py](flow.py) | 36 | DeepResearchFlowState | ClassDef |
| [flow.py](flow.py) | 42 | server_params | FunctionDef |
| [flow.py](flow.py) | 54 | DeepResearchFlow | ClassDef |
| [flow.py](flow.py) | 280 | main | AsyncFunctionDef |
| [flow.py](flow.py) | 60 | start_flow | Start the flow by setting the query in the state. |
| [flow.py](flow.py) | 66 | collect_urls | Search web for user query and return URLBuckets object. |
| [flow.py](flow.py) | 126 | dispatch_to_specialists | Fan-out to platform specialists. Each platform is processed independently. |
| [flow.py](flow.py) | 225 | synthesize_response | Final deep research response synthesis. |
| [research.py](research.py) | 5 | run_deep_research | Run the deep research flow and return the result. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/gpt-oss`
- `openai/gpt-4o`
- `openai/o3-mini`

Detected import roots: `asyncio`, `crewai`, `crewai_tools`, `dotenv`, `flow`, `importlib`, `json`, `logging`, `mcp`, `os`, `pathlib`, `pydantic`, `research`, `streamlit`, `sys`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `BRIGHT_DATA_API_TOKEN`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/multiplatform_deep_researcher); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
