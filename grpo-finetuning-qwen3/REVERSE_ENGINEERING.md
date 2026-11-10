# Reverse engineering: grpo-finetuning-qwen3

## Problem and reconstructed mechanism

Improve Qwen3 structured invoice extraction through remote GRPO training.

A JSON-schema reward, Fireworks training loop and baseline/post-training evaluation form the learning path.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated versioned dataset -> baseline evaluation -> isolated training job -> checkpoint/adapter -> independent evaluation -> export parity -> registered artifact
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | vlen, box_line, print_banner, extract, validate, run_agent | argparse, dotenv, json, openai, os, re, sys, time |
| [agent-skill/grpo-finetune/generate_reward.py](agent-skill/grpo-finetune/generate_reward.py) | load_reward, validate_reward | argparse, importlib, pathlib, sys |
| [agent-skill/grpo-finetune/run_pipeline.py](agent-skill/grpo-finetune/run_pipeline.py) | banner, checkpoint, make_client, run_eval, main | argparse, asyncio, dotenv, fireworks, generate_reward, json, nest_asyncio, openai |
| [grpo_json_extraction.ipynb#cell-6](grpo_json_extraction.ipynb#cell-6) | score | jsonschema |
| [grpo_json_extraction.ipynb#cell-10](grpo_json_extraction.ipynb#cell-10) | run_eval | openai |
| [grpo_json_extraction.ipynb#cell-12](grpo_json_extraction.ipynb#cell-12) | invoice_reward | asyncio, nest_asyncio, sys, training |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | 38 | vlen | FunctionDef |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | 42 | box_line | FunctionDef |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | 47 | print_banner | FunctionDef |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | 65 | extract | FunctionDef |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | 83 | validate | FunctionDef |
| [agent-skill/grpo-finetune/agent_demo.py](agent-skill/grpo-finetune/agent_demo.py) | 87 | run_agent | FunctionDef |
| [agent-skill/grpo-finetune/generate_reward.py](agent-skill/grpo-finetune/generate_reward.py) | 13 | load_reward | FunctionDef |
| [agent-skill/grpo-finetune/generate_reward.py](agent-skill/grpo-finetune/generate_reward.py) | 20 | validate_reward | FunctionDef |
| [agent-skill/grpo-finetune/run_pipeline.py](agent-skill/grpo-finetune/run_pipeline.py) | 33 | banner | FunctionDef |
| [agent-skill/grpo-finetune/run_pipeline.py](agent-skill/grpo-finetune/run_pipeline.py) | 37 | checkpoint | FunctionDef |
| [agent-skill/grpo-finetune/run_pipeline.py](agent-skill/grpo-finetune/run_pipeline.py) | 41 | make_client | FunctionDef |
| [agent-skill/grpo-finetune/run_pipeline.py](agent-skill/grpo-finetune/run_pipeline.py) | 47 | run_eval | FunctionDef |
| [agent-skill/grpo-finetune/run_pipeline.py](agent-skill/grpo-finetune/run_pipeline.py) | 73 | main | FunctionDef |
| [grpo_json_extraction.ipynb#cell-6](grpo_json_extraction.ipynb#cell-6) | 15 | score | FunctionDef |
| [grpo_json_extraction.ipynb#cell-10](grpo_json_extraction.ipynb#cell-10) | 11 | run_eval | FunctionDef |
| [grpo_json_extraction.ipynb#cell-12](grpo_json_extraction.ipynb#cell-12) | 22 | invoice_reward | FunctionDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `Qwen/Qwen3-8B`
- `accounts/fireworks/models/qwen3-8b`
- `invoice-extractor-v1`

Detected import roots: `argparse`, `asyncio`, `dotenv`, `fireworks`, `generate_reward`, `importlib`, `json`, `jsonschema`, `matplotlib`, `nest_asyncio`, `openai`, `os`, `pathlib`, `re`, `subprocess`, `sys`, `time`, `training`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `FIREWORKS_ACCOUNT_ID`
- `FIREWORKS_API_KEY`
- `OPENROUTER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [grpo_json_extraction.ipynb](grpo_json_extraction.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/grpo-finetuning-qwen3); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
