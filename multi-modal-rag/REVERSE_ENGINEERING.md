# Reverse engineering: multi-modal-rag

## Problem and reconstructed mechanism

Study CLIP image retrieval and multimodal prompting through notebooks.

One notebook embeds image/text pairs for semantic search; another explores vision-model conversation and tool use.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [clip.ipynb#cell-5](clip.ipynb#cell-5) | top-level workflow | torch, transformers |
| [clip.ipynb#cell-13](clip.ipynb#cell-13) | search_images |  |
| [clip.ipynb#cell-15](clip.ipynb#cell-15) | search_similar_images |  |
| [clip.ipynb#cell-20](clip.ipynb#cell-20) | semantic_search |  |
| [mm_prompting.ipynb#cell-4](mm_prompting.ipynb#cell-4) | top-level workflow |  |
| [mm_prompting.ipynb#cell-7](mm_prompting.ipynb#cell-7) | top-level workflow |  |
| [mm_prompting.ipynb#cell-9](mm_prompting.ipynb#cell-9) | Conversation, generate |  |
| [mm_prompting.ipynb#cell-14](mm_prompting.ipynb#cell-14) | top-level workflow |  |
| [mm_prompting.ipynb#cell-16](mm_prompting.ipynb#cell-16) | top-level workflow |  |
| [mm_prompting.ipynb#cell-20](mm_prompting.ipynb#cell-20) | top-level workflow |  |
| [mm_prompting.ipynb#cell-23](mm_prompting.ipynb#cell-23) | get_stock_price | ollama, yfinance |
| [mm_prompting.ipynb#cell-24](mm_prompting.ipynb#cell-24) | get_stock_price | ollama, yfinance |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [clip.ipynb#cell-13](clip.ipynb#cell-13) | 1 | search_images | FunctionDef |
| [clip.ipynb#cell-15](clip.ipynb#cell-15) | 1 | search_similar_images | FunctionDef |
| [clip.ipynb#cell-20](clip.ipynb#cell-20) | 15 | semantic_search | FunctionDef |
| [mm_prompting.ipynb#cell-9](mm_prompting.ipynb#cell-9) | 1 | Conversation | ClassDef |
| [mm_prompting.ipynb#cell-9](mm_prompting.ipynb#cell-9) | 6 | generate | FunctionDef |
| [mm_prompting.ipynb#cell-23](mm_prompting.ipynb#cell-23) | 7 | get_stock_price | FunctionDef |
| [mm_prompting.ipynb#cell-24](mm_prompting.ipynb#cell-24) | 7 | get_stock_price | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `llama3.2-vision`
- `openai/clip-vit-base-patch32`

Detected import roots: `IPython`, `PIL`, `datasets`, `matplotlib`, `ollama`, `requests`, `torch`, `transformers`, `yfinance`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [clip.ipynb](clip.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [clip.ipynb](clip.ipynb) | Added explicit connection/read timeouts to 1 requests calls in notebook cells. |
| [mm_prompting.ipynb](mm_prompting.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/multi-modal-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
