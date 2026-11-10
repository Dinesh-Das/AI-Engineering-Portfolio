# Reverse engineering: llamaindex-mcp

## Problem and reconstructed mechanism

Connect a local LlamaIndex agent to SQLite-backed MCP tools.

The server initializes a database and exposes data operations; the notebook builds the client and handles user messages.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated client -> tool discovery -> argument validation -> authorized operation -> bounded backend call -> structured result
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [ollama_client.ipynb#cell-4](ollama_client.ipynb#cell-4) | top-level workflow | llama_index |
| [ollama_client.ipynb#cell-11](ollama_client.ipynb#cell-11) | get_agent | llama_index |
| [ollama_client.ipynb#cell-13](ollama_client.ipynb#cell-13) | handle_user_message | llama_index |
| [server.py](server.py) | init_db, add_data, read_data | argparse, mcp, sqlite3 |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [ollama_client.ipynb#cell-11](ollama_client.ipynb#cell-11) | 4 | get_agent | AsyncFunctionDef |
| [ollama_client.ipynb#cell-13](ollama_client.ipynb#cell-13) | 8 | handle_user_message | AsyncFunctionDef |
| [server.py](server.py) | 7 | init_db | FunctionDef |
| [server.py](server.py) | 22 | add_data | Add new data to the people table using a SQL INSERT query. |
| [server.py](server.py) | 59 | read_data | Read data from the people table using a SQL SELECT query. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4`
- `llama3.2`

Detected import roots: `argparse`, `importlib`, `llama_index`, `mcp`, `nest_asyncio`, `pathlib`, `sqlite3`, `sys`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [ollama_client.ipynb](ollama_client.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/parameters.json](enhancement/examples/parameters.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/llamaindex-mcp); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
