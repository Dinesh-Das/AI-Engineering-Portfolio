# Reverse engineering: eval-and-observability

## Problem and reconstructed mechanism

Build an end-to-end RAG evaluation and trace collection pipeline.

Dataset-generation and application notebooks connect RAG calls to Opik and judge metrics.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned task set -> identical context/settings -> candidate generation -> blinded grading -> independent executable checks -> paired comparison
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [data_gen.ipynb#cell-10](data_gen.ipynb#cell-10) | top-level workflow |  |
| [demo.ipynb#cell-11](demo.ipynb#cell-11) | my_function | opik |
| [demo.ipynb#cell-13](demo.ipynb#cell-13) | top-level workflow | openai, opik |
| [demo.ipynb#cell-36](demo.ipynb#cell-36) | my_llm_application | opik |
| [demo.ipynb#cell-38](demo.ipynb#cell-38) | top-level workflow | openai, opik |
| [demo.ipynb#cell-40](demo.ipynb#cell-40) | evaluation_task |  |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [demo.ipynb#cell-11](demo.ipynb#cell-11) | 4 | my_function | FunctionDef |
| [demo.ipynb#cell-36](demo.ipynb#cell-36) | 4 | my_llm_application | FunctionDef |
| [demo.ipynb#cell-40](demo.ipynb#cell-40) | 1 | evaluation_task | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-3.5-turbo`
- `llama3`
- `nomic-embed-text`
- `phi3`

Detected import roots: `dotenv`, `langchain`, `langchain_community`, `langchain_openai`, `llama_index`, `openai`, `opik`, `os`, `pandas`, `ragas`, `requests`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [data_gen.ipynb](data_gen.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [demo.ipynb](demo.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [demo.ipynb](demo.ipynb) | Added explicit connection/read timeouts to 1 requests calls in notebook cells. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/eval-and-observability); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
