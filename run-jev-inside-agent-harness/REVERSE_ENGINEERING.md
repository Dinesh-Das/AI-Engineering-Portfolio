# Reverse engineering: run-jev-inside-agent-harness

## Problem and reconstructed mechanism

Study task orchestration and credential boundaries in an agent-harness integration guide.

The folder contains explanatory material and diagrams rather than a runnable harness implementation.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source guide -> dependency/contract inventory -> minimal isolated integration -> failure tests -> reviewed deployment plan
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `importlib`, `pathlib`, `sys`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/agent-with-jev.jpg](assets/agent-with-jev.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/agent-without-jev.jpg](assets/agent-without-jev.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/closed-vs-open-harness.jpg](assets/closed-vs-open-harness.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/code-mode.jpg](assets/code-mode.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/confidence-threshold.jpg](assets/confidence-threshold.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/connector-jev-mcp.jpg](assets/connector-jev-mcp.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/context-volume-levers.jpg](assets/context-volume-levers.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/credential-isolation.jpg](assets/credential-isolation.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/decision-cost-comparison.jpg](assets/decision-cost-comparison.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/deferred-tool-loading.jpg](assets/deferred-tool-loading.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/enterprise-bench-results.jpg](assets/enterprise-bench-results.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/jev-choice-question.jpg](assets/jev-choice-question.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/jev-workflow.jpg](assets/jev-workflow.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/llm-vs-jev.jpg](assets/llm-vs-jev.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/offloading.jpg](assets/offloading.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/requests-vs-issues.jpg](assets/requests-vs-issues.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/results-with-vs-without-jev.jpg](assets/results-with-vs-without-jev.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/settings-models.jpg](assets/settings-models.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/subagents.jpg](assets/subagents.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/trueforge-architecture.jpg](assets/trueforge-architecture.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/trueforge-banner.jpg](assets/trueforge-banner.jpg) | Restored frontend source/asset after UI scope was authorized. |
| [assets/weekly-schedule.jpg](assets/weekly-schedule.jpg) | Restored frontend source/asset after UI scope was authorized. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/run-jev-inside-agent-harness); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
