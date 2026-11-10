# Reverse engineering: trustworthy-rag

## Problem and reconstructed mechanism

Attach trustworthiness signals to document-grounded model output.

LlamaParse and retrieval build context while Cleanlab trustworthiness callbacks expose scores and reasoning.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, reset_chat, display_pdf | UI surface |
| [main.ipynb#cell-7](main.ipynb#cell-7) | top-level workflow |  |
| [main.ipynb#cell-8](main.ipynb#cell-8) | GetTrustworthinessScoreAndReasoning, display_response, class_name, handle | llama_index, typing |
| [utils.py](utils.py) | GetTrustworthinessScoreAndReasoning, setup_trustworthiness_handler, display_response, outputs_with_trustworthiness, class_name, handle | llama_index, typing |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 33 | load_llm | FunctionDef |
| [app.py](app.py) | 43 | reset_chat | FunctionDef |
| [app.py](app.py) | 49 | display_pdf | FunctionDef |
| [main.ipynb#cell-8](main.ipynb#cell-8) | 8 | GetTrustworthinessScoreAndReasoning | ClassDef |
| [main.ipynb#cell-8](main.ipynb#cell-8) | 36 | display_response | FunctionDef |
| [main.ipynb#cell-8](main.ipynb#cell-8) | 14 | class_name | Class name. |
| [main.ipynb#cell-8](main.ipynb#cell-8) | 18 | handle | FunctionDef |
| [utils.py](utils.py) | 8 | GetTrustworthinessScoreAndReasoning | ClassDef |
| [utils.py](utils.py) | 29 | setup_trustworthiness_handler | Initialize and register the trustworthiness event handler. |
| [utils.py](utils.py) | 37 | display_response | Display the response along with trustworthiness information. |
| [utils.py](utils.py) | 46 | outputs_with_trustworthiness | Display the response along with trustworthiness information. |
| [utils.py](utils.py) | 14 | class_name | Class name. |
| [utils.py](utils.py) | 18 | handle | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `BAAI/bge-small-en-v1.5`

Detected import roots: `IPython`, `base64`, `dotenv`, `gc`, `llama_index`, `llama_parse`, `os`, `random`, `streamlit`, `tempfile`, `time`, `typing`, `utils`, `uuid`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `CLEANLAB_API_KEY`
- `LLAMA_CLOUD_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [main.ipynb](main.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [app.py](app.py) | 93 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/trustworthy-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
