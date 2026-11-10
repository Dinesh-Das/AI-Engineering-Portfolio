# Reverse engineering: firecrawl-agent

## Problem and reconstructed mechanism

Combine corrective document retrieval with Firecrawl web fallback.

The workflow grades retrieved context and reaches web search when local evidence is insufficient.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, reset_chat, display_pdf, initialize_workflow, run_workflow | UI surface |
| [start_server.py](start_server.py) | load_model | beam, subprocess, time |
| [workflow.py](workflow.py) | RetrieveEvent, WebSearchEvent, QueryEvent, CorrectiveRAGWorkflow, retrieve, eval_relevance, web_search, query_result | dotenv, llama_index, os, re, relevance_policy, requests, typing |
| [relevance_policy.py](relevance_policy.py) | is_relevant_grade, needs_web_search |  |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 49 | load_llm | FunctionDef |
| [app.py](app.py) | 55 | reset_chat | FunctionDef |
| [app.py](app.py) | 60 | display_pdf | FunctionDef |
| [app.py](app.py) | 76 | initialize_workflow | FunctionDef |
| [app.py](app.py) | 129 | run_workflow | AsyncFunctionDef |
| [start_server.py](start_server.py) | 3 | load_model | FunctionDef |
| [workflow.py](workflow.py) | 32 | RetrieveEvent | Retrieve event (gets retrieved nodes). |
| [workflow.py](workflow.py) | 38 | WebSearchEvent | Web search event. |
| [workflow.py](workflow.py) | 44 | QueryEvent | Query event. Queries given relevant text and search text. |
| [workflow.py](workflow.py) | 85 | CorrectiveRAGWorkflow | Corrective RAG Workflow. |
| [workflow.py](workflow.py) | 118 | retrieve | Retrieve the relevant nodes for the query. |
| [workflow.py](workflow.py) | 144 | eval_relevance | Evaluate relevancy of retrieved documents with the query. |
| [workflow.py](workflow.py) | 237 | web_search | Search the transformed query |
| [workflow.py](workflow.py) | 266 | query_result | Get result with relevant text. |
| [relevance_policy.py](relevance_policy.py) | 4 | is_relevant_grade | FunctionDef |
| [relevance_policy.py](relevance_policy.py) | 8 | needs_web_search | No evidence or an invalid grader response must trigger evidence recovery. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `gpt-4o`

Detected import roots: `asyncio`, `base64`, `beam`, `contextlib`, `dotenv`, `gc`, `importlib`, `io`, `llama_index`, `logging`, `nest_asyncio`, `os`, `pathlib`, `qdrant_client`, `re`, `relevance_policy`, `requests`, `streamlit`, `subprocess`, `sys`, `tempfile`, `time`, `typing`, `uuid`, `workflow`

Retained dependency manifests: [pyproject.toml](pyproject.toml), [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [workflow.py](workflow.py) | Fixed evidence fallback routing and aligned context filtering with strict affirmative grading; unit-tested routing on extracted workflow methods without SDK imports. |
| [assets/firecrawl-logo-with-fire.png](assets/firecrawl-logo-with-fire.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/firecrawl_logo.png](assets/firecrawl_logo.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/images.jpeg](assets/images.jpeg) | Restored frontend source/asset after UI scope was authorized. |
| [relevance_policy.py](relevance_policy.py) | Added a strict relevance gate; reject misleading yes substrings and recover from empty retrieval. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/corpus.json](enhancement/examples/corpus.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/firecrawl-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
