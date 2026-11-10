# Reverse engineering: autogen-stock-analyst

## Problem and reconstructed mechanism

Use AutoGen with a custom model client for financial analysis and code generation.

CustomModelClient adapts a Qualcomm-hosted model to AutoGen's response, usage and cost interface.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [coding_and_financial_analyst.ipynb#cell-2](coding_and_financial_analyst.ipynb#cell-2) | config_list |  |
| [custom_autogen_model.py](custom_autogen_model.py) | CustomModelClient, create, message_retrieval, cost, get_usage | imagine, types |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [coding_and_financial_analyst.ipynb#cell-2](coding_and_financial_analyst.ipynb#cell-2) | 1 | config_list | FunctionDef |
| [custom_autogen_model.py](custom_autogen_model.py) | 12 | CustomModelClient | ClassDef |
| [custom_autogen_model.py](custom_autogen_model.py) | 48 | create | FunctionDef |
| [custom_autogen_model.py](custom_autogen_model.py) | 80 | message_retrieval | Retrieve the messages from the response. |
| [custom_autogen_model.py](custom_autogen_model.py) | 92 | cost | Calculate the cost of the response. |
| [custom_autogen_model.py](custom_autogen_model.py) | 98 | get_usage | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `Llama-3.1-70B`

Detected import roots: `autogen`, `custom_autogen_model`, `datetime`, `dotenv`, `imagine`, `json`, `os`, `types`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `IMAGINE_API_KEY`
- `IMAGINE_AUTOGEN_CONFIG`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [coding_and_financial_analyst.ipynb](coding_and_financial_analyst.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/autogen-stock-analyst); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
