# Reverse engineering: agentic_rag_deepseek

## Problem and reconstructed mechanism

Combine a local reasoning model with managed document parsing and search.

A custom CrewAI DocumentSearchTool delegates parsing and retrieval to GroundX before DeepSeek synthesizes the response.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app_deep_seek.py](app_deep_seek.py) | load_llm, create_agents_and_tasks, reset_chat, display_pdf | UI reference |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | AgenticRag, retriever_agent, response_synthesizer_agent, retrieval_task, response_task, crew | agentic_rag, crewai, crewai_tools |
| [src/agentic_rag/main.py](src/agentic_rag/main.py) | run, train, replay, test | agentic_rag, sys, warnings |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | DocumentSearchToolInput, DocumentSearchTool, test_document_searcher | crewai, dotenv, groundx, os, pydantic, typing |
| [src/agentic_rag/config/agents.yaml](src/agentic_rag/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [src/agentic_rag/config/tasks.yaml](src/agentic_rag/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | 13 | AgenticRag | AgenticRag crew |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | 29 | retriever_agent | FunctionDef |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | 40 | response_synthesizer_agent | FunctionDef |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | 53 | retrieval_task | FunctionDef |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | 59 | response_task | FunctionDef |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | 65 | crew | Creates the AgenticRag crew |
| [src/agentic_rag/main.py](src/agentic_rag/main.py) | 14 | run | Run the crew. |
| [src/agentic_rag/main.py](src/agentic_rag/main.py) | 24 | train | Train the crew for a given number of iterations. |
| [src/agentic_rag/main.py](src/agentic_rag/main.py) | 37 | replay | Replay the crew execution from a specific task. |
| [src/agentic_rag/main.py](src/agentic_rag/main.py) | 47 | test | Test the crew execution and returns the results. |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | 11 | DocumentSearchToolInput | Input schema for DocumentSearchTool. |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | 15 | DocumentSearchTool | ClassDef |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | 80 | test_document_searcher | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/deepseek-r1:7b`

Detected import roots: `agentic_rag`, `base64`, `crewai`, `crewai_tools`, `dotenv`, `gc`, `groundx`, `os`, `pydantic`, `src`, `streamlit`, `sys`, `tempfile`, `time`, `tools`, `typing`, `warnings`, `yaml`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `GROUNDX_API_KEY`
- `SERPER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [src/agentic_rag/agentic_rag.ipynb](src/agentic_rag/agentic_rag.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [src/agentic_rag/tools/test.ipynb.invalid.txt](src/agentic_rag/tools/test.ipynb.invalid.txt) | Empty/invalid upstream notebook quarantined; no executable lesson was present. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/agentic_rag_deepseek); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
