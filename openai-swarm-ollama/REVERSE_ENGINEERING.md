# Reverse engineering: openai-swarm-ollama

## Problem and reconstructed mechanism

Explore local-model handoffs between lightweight agents.

Swarm agents can delegate to each other and use web search while Ollama provides an OpenAI-shaped model endpoint.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | search_web, run_workflow, main | UI surface |
| [demo.ipynb#cell-2](demo.ipynb#cell-2) | search_web, run_workflow | UI surface |
| [openai_swarm_demo.py](openai_swarm_demo.py) | transfer_to_agent_b | dotenv, swarm |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 16 | search_web | FunctionDef |
| [app.py](app.py) | 73 | run_workflow | FunctionDef |
| [app.py](app.py) | 100 | main | FunctionDef |
| [demo.ipynb#cell-2](demo.ipynb#cell-2) | 16 | search_web | FunctionDef |
| [demo.ipynb#cell-2](demo.ipynb#cell-2) | 73 | run_workflow | FunctionDef |
| [openai_swarm_demo.py](openai_swarm_demo.py) | 9 | transfer_to_agent_b | FunctionDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `llama3.2`
- `llama3.2:1b`

Detected import roots: `datetime`, `dotenv`, `duckduckgo_search`, `importlib`, `pathlib`, `streamlit`, `swarm`, `sys`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [demo.ipynb](demo.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/openai-swarm-ollama); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
