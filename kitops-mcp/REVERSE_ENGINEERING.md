# Reverse engineering: kitops-mcp

## Problem and reconstructed mechanism

Manage machine-learning ModelKit artifacts through an MCP tool boundary.

Typed server tools create Kitfiles and inspect, pack, push, pull or remove model artifacts.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated request/job -> isolated runtime -> versioned model/data artifact -> bounded operation -> persisted result and observable status
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [server.py](server.py) | create_kitfile, inspect_modelkit, push_and_pack_modelkit, pull_and_unpack_modelkit, remove_modelkit | mcp, tools, typing |
| [tools.py](tools.py) | create, inspect, push_and_pack, pull_and_unpack, remove | json, kitops, os, typing, util |
| [util.py](util.py) | validate_modelkit_tag |  |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [server.py](server.py) | 11 | create_kitfile | Create a new Kitfile at the specified directory with the given ModelKit name. |
| [server.py](server.py) | 35 | inspect_modelkit | Inspect a ModelKit and return its detailed information from the remote registry. |
| [server.py](server.py) | 56 | push_and_pack_modelkit | Pack the project situated at the working directory and push it as a ModelKit to the remote registry. |
| [server.py](server.py) | 78 | pull_and_unpack_modelkit | Pull a ModelKit from the remote registry and unpack it to the specified directory. |
| [server.py](server.py) | 104 | remove_modelkit | Remove a ModelKit from the remote registry. |
| [tools.py](tools.py) | 11 | create | Create a new Kitfile at the specified path with referred modelkit name. |
| [tools.py](tools.py) | 53 | inspect | Inspect a ModelKit and return its detailed information. |
| [tools.py](tools.py) | 73 | push_and_pack | Pack and push a ModelKit to the repository. |
| [tools.py](tools.py) | 105 | pull_and_unpack | Pull and unpack a ModelKit to the working directory. |
| [tools.py](tools.py) | 138 | remove | Remove a ModelKit from the remote registry only. |
| [util.py](util.py) | 1 | validate_modelkit_tag | Validate that ModelKit tag has correct format |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `importlib`, `joblib`, `json`, `kitops`, `mcp`, `os`, `pandas`, `pathlib`, `sklearn`, `sys`, `tools`, `typing`, `util`

Retained dependency manifests: [ml-project/requirements.txt](ml-project/requirements.txt), [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/artifacts.json](enhancement/examples/artifacts.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/segment.txt](enhancement/examples/segment.txt) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/kitops-mcp); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
