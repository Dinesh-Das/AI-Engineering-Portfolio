# Reverse engineering: Colivara-deepseek-website-RAG

## Problem and reconstructed mechanism

Retrieve visually represented web pages and answer with a multimodal model.

Website screenshots become page-like documents; ColiVara search selects visual context for Janus-Pro synthesis.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat, display_pdf, create_pdf_from_screenshot | UI surface |
| [rag_code.py](rag_code.py) | batch_iterate, Retriever, RAG, search, generate_context, query | Janus, PIL, base64, colivara_py, io, torch, tqdm, transformers |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 45 | reset_chat | FunctionDef |
| [app.py](app.py) | 52 | display_pdf | FunctionDef |
| [app.py](app.py) | 74 | create_pdf_from_screenshot | FunctionDef |
| [rag_code.py](rag_code.py) | 12 | batch_iterate | Yield successive n-sized chunks from lst. |
| [rag_code.py](rag_code.py) | 18 | Retriever | ClassDef |
| [rag_code.py](rag_code.py) | 39 | RAG | ClassDef |
| [rag_code.py](rag_code.py) | 24 | search | FunctionDef |
| [rag_code.py](rag_code.py) | 59 | generate_context | FunctionDef |
| [rag_code.py](rag_code.py) | 62 | query | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `IPython`, `Janus`, `PIL`, `base64`, `colivara_py`, `dotenv`, `firecrawl`, `fpdf`, `gc`, `io`, `math`, `numpy`, `os`, `pdf2image`, `rag_code`, `random`, `requests`, `streamlit`, `streamlit_pdf_viewer`, `tempfile`, `time`, `torch`, `tqdm`, `transformers`, `uuid`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `COLIVARA_API_KEY`
- `FIRECRAWL_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Redacted 2 possible credential literals (values not retained). |
| [assets/deep-seek.png](assets/deep-seek.png) | Restored frontend source/asset after UI scope was authorized. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [app.py](app.py) | 75 | network-timeout | HTTP call has no explicit timeout; a stalled peer can occupy a worker. |
| [rag_code.py](rag_code.py) | 55 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/Colivara-deepseek-website-RAG); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
