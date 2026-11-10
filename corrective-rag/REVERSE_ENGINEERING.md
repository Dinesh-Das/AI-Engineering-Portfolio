# Reverse engineering: corrective-rag

## Problem and reconstructed mechanism

Detect weak document evidence and recover through web search.

A LlamaIndex workflow retrieves, grades relevance, optionally searches the web and synthesizes a response.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, reset_chat, display_pdf, initialize_workflow, run_workflow | UI surface |
| [workflow.py](workflow.py) | RetrieveEvent, WebSearchEvent, QueryEvent, CorrectiveRAGWorkflow, retrieve, eval_relevance, web_search, query_result | dotenv, llama_index, os, relevance_policy, typing |
| [relevance_policy.py](relevance_policy.py) | is_relevant_grade, needs_web_search |  |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 49 | load_llm | FunctionDef |
| [app.py](app.py) | 53 | reset_chat | FunctionDef |
| [app.py](app.py) | 57 | display_pdf | FunctionDef |
| [app.py](app.py) | 71 | initialize_workflow | FunctionDef |
| [app.py](app.py) | 101 | run_workflow | AsyncFunctionDef |
| [workflow.py](workflow.py) | 30 | RetrieveEvent | Retrieve event (gets retrieved nodes). |
| [workflow.py](workflow.py) | 37 | WebSearchEvent | Web search event. |
| [workflow.py](workflow.py) | 43 | QueryEvent | Query event. Queries given relevant text and search text. |
| [workflow.py](workflow.py) | 83 | CorrectiveRAGWorkflow | Corrective RAG Workflow. |
| [workflow.py](workflow.py) | 103 | retrieve | Retrieve the relevant nodes for the query. |
| [workflow.py](workflow.py) | 118 | eval_relevance | Evaluate relevancy of retrieved documents with the query. |
| [workflow.py](workflow.py) | 143 | web_search | Search the transformed query with Tavily API. |
| [workflow.py](workflow.py) | 160 | query_result | Get result with relevant text. |
| [relevance_policy.py](relevance_policy.py) | 4 | is_relevant_grade | FunctionDef |
| [relevance_policy.py](relevance_policy.py) | 8 | needs_web_search | No evidence or an invalid grader response must trigger evidence recovery. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-large-en-v1.5`
- `deepseek-r1:7b`

Detected import roots: `IPython`, `asyncio`, `base64`, `contextlib`, `dotenv`, `gc`, `io`, `llama_index`, `logging`, `nest_asyncio`, `os`, `qdrant_client`, `relevance_policy`, `streamlit`, `sys`, `tempfile`, `time`, `typing`, `uuid`, `workflow`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `LINKUP_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [workflow.py](workflow.py) | Fixed evidence fallback routing and aligned context filtering with strict affirmative grading; unit-tested routing on extracted workflow methods without SDK imports. |
| [relevance_policy.py](relevance_policy.py) | Added a strict relevance gate; recover when retrieval is empty or no grade is affirmative. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/corrective-rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
