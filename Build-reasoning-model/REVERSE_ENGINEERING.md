# Reverse engineering: Build-reasoning-model

## Problem and reconstructed mechanism

Train a reasoning-oriented model with GRPO and explicit answer-format rewards.

Unsloth and TRL generate grouped completions and combine correctness, integer-answer and XML-format reward functions.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated versioned dataset -> baseline evaluation -> isolated training job -> checkpoint/adapter -> independent evaluation -> export parity -> registered artifact
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [Own_reasoning_model_with_GRPO.ipynb#cell-4](Own_reasoning_model_with_GRPO.ipynb#cell-4) | top-level workflow | torch, unsloth |
| [Own_reasoning_model_with_GRPO.ipynb#cell-5](Own_reasoning_model_with_GRPO.ipynb#cell-5) | extract_hash_answer, create_dataset | datasets, re |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | extract_xml_answer, correctness_reward_func, int_reward_func, strict_format_reward_func, soft_format_reward_func, count_xml, xmlcount_reward_func |  |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [Own_reasoning_model_with_GRPO.ipynb#cell-5](Own_reasoning_model_with_GRPO.ipynb#cell-5) | 14 | extract_hash_answer | FunctionDef |
| [Own_reasoning_model_with_GRPO.ipynb#cell-5](Own_reasoning_model_with_GRPO.ipynb#cell-5) | 20 | create_dataset | FunctionDef |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 1 | extract_xml_answer | FunctionDef |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 6 | correctness_reward_func | FunctionDef |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 13 | int_reward_func | FunctionDef |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 18 | strict_format_reward_func | Reward function that checks if the completion has a specific format. |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 25 | soft_format_reward_func | Reward function that checks if the completion has a specific format. |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 32 | count_xml | FunctionDef |
| [Own_reasoning_model_with_GRPO.ipynb#cell-6](Own_reasoning_model_with_GRPO.ipynb#cell-6) | 46 | xmlcount_reward_func | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `meta-llama/meta-Llama-3.1-8B-Instruct`

Detected import roots: `datasets`, `re`, `torch`, `trl`, `unsloth`, `vllm`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [Own_reasoning_model_with_GRPO.ipynb](Own_reasoning_model_with_GRPO.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/Build-reasoning-model); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
