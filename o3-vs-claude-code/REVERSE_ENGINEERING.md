# Reverse engineering: o3-vs-claude-code

## Problem and reconstructed mechanism

Compare repository-aware code responses and judge scoring across models.

Notebooks prepare repository context and evaluate generated code; the pinned data-preparation notebook is empty.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned task set -> identical context/settings -> candidate generation -> blinded grading -> independent executable checks -> paired comparison
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, parse_github_url, clone_repo, validate_owner_repo, parse_docs_by_file_types, create_index, reset_chat | UI reference |
| [Opik for LLM evaluation.ipynb#cell-6](Opik%20for%20LLM%20evaluation.ipynb#cell-6) | parse_github_url, clone_repo, parse_docs_by_file_types, setup_chat_engine |  |
| [Opik for LLM evaluation.ipynb#cell-8](Opik%20for%20LLM%20evaluation.ipynb#cell-8) | top-level workflow |  |
| [Opik for LLM evaluation.ipynb#cell-12](Opik%20for%20LLM%20evaluation.ipynb#cell-12) | my_llm_application, evaluation_task | opik |
| [Opik for LLM evaluation.ipynb#cell-13](Opik%20for%20LLM%20evaluation.ipynb#cell-13) | LLMJudgeMetric, score | json, openai, opik, typing |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [Opik for LLM evaluation.ipynb#cell-6](Opik%20for%20LLM%20evaluation.ipynb#cell-6) | 3 | parse_github_url | Extract owner and repo name from GitHub URL |
| [Opik for LLM evaluation.ipynb#cell-6](Opik%20for%20LLM%20evaluation.ipynb#cell-6) | 9 | clone_repo | Clone a GitHub repository |
| [Opik for LLM evaluation.ipynb#cell-6](Opik%20for%20LLM%20evaluation.ipynb#cell-6) | 13 | parse_docs_by_file_types | Parse documents based on file extension |
| [Opik for LLM evaluation.ipynb#cell-6](Opik%20for%20LLM%20evaluation.ipynb#cell-6) | 33 | setup_chat_engine | Set up the chat engine for a GitHub repository |
| [Opik for LLM evaluation.ipynb#cell-12](Opik%20for%20LLM%20evaluation.ipynb#cell-12) | 4 | my_llm_application | FunctionDef |
| [Opik for LLM evaluation.ipynb#cell-12](Opik%20for%20LLM%20evaluation.ipynb#cell-12) | 8 | evaluation_task | FunctionDef |
| [Opik for LLM evaluation.ipynb#cell-13](Opik%20for%20LLM%20evaluation.ipynb#cell-13) | 6 | LLMJudgeMetric | ClassDef |
| [Opik for LLM evaluation.ipynb#cell-13](Opik%20for%20LLM%20evaluation.ipynb#cell-13) | 34 | score | Score the output of an LLM. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-base-en-v1.5`
- `Claude 3.7 Sonnet`
- `claude-3-5-sonnet-20240620`
- `claude-3-7-sonnet-20250219`
- `o3-mini`

Detected import roots: `IPython`, `dotenv`, `gc`, `glob`, `json`, `llama_index`, `nest_asyncio`, `openai`, `opik`, `os`, `qdrant_client`, `re`, `streamlit`, `subprocess`, `textwrap`, `typing`, `uuid`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [data_prep.ipynb.invalid.txt](data_prep.ipynb.invalid.txt) | Empty/invalid upstream notebook quarantined; no executable lesson was present. |
| [Opik for LLM evaluation.ipynb](Opik%20for%20LLM%20evaluation.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/o3-vs-claude-code); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
