# Reverse engineering: agentic_rag

## Problem and reconstructed mechanism

Route questions to document retrieval and use web fallback when needed.

CrewAI retrieval and response-synthesis agents wrap document tools; local DeepSeek and Llama variants show model substitution.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [agentic_rag.ipynb#cell-1](agentic_rag.ipynb#cell-1) | top-level workflow | crewai, langchain_openai, os |
| [agentic_rag.ipynb#cell-2](agentic_rag.ipynb#cell-2) | top-level workflow | crewai_tools |
| [agentic_rag.ipynb#cell-7](agentic_rag.ipynb#cell-7) | router_tool | crewai_tools |
| [app.py](app.py) | create_agents_and_tasks, reset_chat, display_pdf | UI surface |
| [app_deep_seek.py](app_deep_seek.py) | load_llm, create_agents_and_tasks, reset_chat, display_pdf | UI surface |
| [app_llama3.2.py](app_llama3.2.py) | load_llm, create_agents_and_tasks, reset_chat, display_pdf | UI surface |
| [demo_llama3.2.ipynb#cell-4](demo_llama3.2.ipynb#cell-4) | top-level workflow |  |
| [src/agentic_rag/crew.py](src/agentic_rag/crew.py) | AgenticRag, retriever_agent, response_synthesizer_agent, retrieval_task, response_task, crew | agentic_rag, crewai, crewai_tools |
| [src/agentic_rag/main.py](src/agentic_rag/main.py) | run, train, replay, test | agentic_rag, sys, warnings |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | DocumentSearchToolInput, DocumentSearchTool, test_document_searcher | chonkie, crewai, markitdown, os, pydantic, qdrant_client, typing |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |
| [src/agentic_rag/config/agents.yaml](src/agentic_rag/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [src/agentic_rag/config/tasks.yaml](src/agentic_rag/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [agentic_rag.ipynb#cell-7](agentic_rag.ipynb#cell-7) | 3 | router_tool | Router Function |
| [app.py](app.py) | 15 | create_agents_and_tasks | Creates a Crew with the given PDF tool (if any) and a web search tool. |
| [app.py](app.py) | 94 | reset_chat | FunctionDef |
| [app.py](app.py) | 98 | display_pdf | Displays the uploaded PDF in an iframe. |
| [app_deep_seek.py](app_deep_seek.py) | 13 | load_llm | FunctionDef |
| [app_deep_seek.py](app_deep_seek.py) | 23 | create_agents_and_tasks | Creates a Crew with the given PDF tool (if any) and a web search tool. |
| [app_deep_seek.py](app_deep_seek.py) | 104 | reset_chat | FunctionDef |
| [app_deep_seek.py](app_deep_seek.py) | 108 | display_pdf | Displays the uploaded PDF in an iframe. |
| [app_llama3.2.py](app_llama3.2.py) | 13 | load_llm | FunctionDef |
| [app_llama3.2.py](app_llama3.2.py) | 23 | create_agents_and_tasks | Creates a Crew with the given PDF tool (if any) and a web search tool. |
| [app_llama3.2.py](app_llama3.2.py) | 104 | reset_chat | FunctionDef |
| [app_llama3.2.py](app_llama3.2.py) | 108 | display_pdf | Displays the uploaded PDF in an iframe. |
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
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | 9 | DocumentSearchToolInput | Input schema for DocumentSearchTool. |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | 13 | DocumentSearchTool | ClassDef |
| [src/agentic_rag/tools/custom_tool.py](src/agentic_rag/tools/custom_tool.py) | 69 | test_document_searcher | FunctionDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-small-en-v1.5`
- `llama3-8b-8192`
- `ollama/deepseek-r1:7b`
- `ollama/llama3.2`

Detected import roots: `agentic_rag`, `base64`, `chonkie`, `crewai`, `crewai_tools`, `gc`, `importlib`, `langchain_community`, `langchain_openai`, `markitdown`, `os`, `pathlib`, `pydantic`, `qdrant_client`, `src`, `streamlit`, `sys`, `tempfile`, `time`, `tools`, `typing`, `warnings`, `yaml`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `GROQ_API_KEY`
- `MODEL`
- `OPENAI_API_KEY`
- `SERPER_API_KEY`
- `TAVILY_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [agentic_rag.ipynb](agentic_rag.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [demo_llama3.2.ipynb](demo_llama3.2.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [src/agentic_rag/agentic_rag.ipynb](src/agentic_rag/agentic_rag.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [assets/deep-seek.png](assets/deep-seek.png) | Restored frontend source/asset after UI scope was authorized. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/agentic_rag); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
