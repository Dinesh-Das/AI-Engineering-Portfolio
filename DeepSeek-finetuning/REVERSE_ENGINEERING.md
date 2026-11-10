# Reverse engineering: DeepSeek-finetuning

## Problem and reconstructed mechanism

Adapt a distilled DeepSeek model and export it for local inference.

An Unsloth notebook loads a quantized base model, prepares training examples, fine-tunes and exports for Ollama.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated versioned dataset -> baseline evaluation -> isolated training job -> checkpoint/adapter -> independent evaluation -> export parity -> registered artifact
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [Fine_tune_DeepSeek.ipynb#cell-3](Fine_tune_DeepSeek.ipynb#cell-3) | top-level workflow | torch, unsloth |
| [Fine_tune_DeepSeek.ipynb#cell-24](Fine_tune_DeepSeek.ipynb#cell-24) | top-level workflow | ollama |
| [Fine_tune_DeepSeek.ipynb#cell-25](Fine_tune_DeepSeek.ipynb#cell-25) | top-level workflow | IPython, ollama |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `deepseek_finetuned_model`
- `unsloth/DeepSeek-R1-Distill-Llama-8B-unsloth-bnb-4bit`

Detected import roots: `IPython`, `datasets`, `importlib`, `ollama`, `pathlib`, `subprocess`, `sys`, `time`, `torch`, `transformers`, `trl`, `unsloth`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [Fine_tune_DeepSeek.ipynb](Fine_tune_DeepSeek.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/schema.json](enhancement/examples/schema.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/reward.json](enhancement/examples/reward.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/splits.json](enhancement/examples/splits.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/distill.json](enhancement/examples/distill.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/DeepSeek-finetuning); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
