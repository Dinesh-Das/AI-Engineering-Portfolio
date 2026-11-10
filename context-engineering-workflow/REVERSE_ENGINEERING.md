# Reverse engineering: context-engineering-workflow

## Problem and reconstructed mechanism

Coordinate multi-source research with parsing, retrieval and long-term context.

TensorLake document parsing, Voyage embeddings, Milvus retrieval and Zep memory feed CrewAI research tasks.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated turn -> retrieve scoped history/facts -> select context under budget -> model/tool response -> validated memory write
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | initialize_session_state, check_api_keys, StreamlitResearchAssistant, create_research_assistant, process_uploaded_document, display_citations_dropdown, display_sidebar_document_processing, display_main_chat_interface, display_initialization_message, main, initialize, query | UI surface |
| [src/config/config_loader.py](src/config/config_loader.py) | ConfigLoader, load_agents_config, load_tasks_config, get_agent_config, get_task_config | os, pathlib, typing, yaml |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | TensorLakeClient, list_uploaded_files, verify_file_uploaded, upload, parse_structured, get_result | dotenv, json, os, tensorlake, typing |
| [src/generation/generation.py](src/generation/generation.py) | StructuredResponseGen, generate | json, openai, os, typing |
| [src/memory/memory.py](src/memory/memory.py) | ZepMemoryLayer, as_external_memory, save_user_message, save_assistant_message, save_preferences, wait_for_indexing, get_context_block | crewai, os, time, typing, zep_cloud, zep_crewai |
| [src/rag/embeddings.py](src/rag/embeddings.py) | ContextualizedEmbeddings, embed_document_chunks, embed_query | dotenv, os, typing, voyageai |
| [src/rag/rag_pipeline.py](src/rag/rag_pipeline.py) | RAGPipeline, process_documents, retrieve_context, generate_response, query | os, src, typing |
| [src/rag/retriever.py](src/rag/retriever.py) | MilvusVectorDB, insert, get_collection_count, search | pymilvus, typing |
| [src/tools/arxiv_tool.py](src/tools/arxiv_tool.py) | ArxivAPIInput, ArxivTool | crewai, json, pydantic, requests, typing, xml |
| [src/tools/memory_tool.py](src/tools/memory_tool.py) | MemoryInput, MemoryTool | crewai, json, pydantic, src, typing |
| [src/tools/rag_tool.py](src/tools/rag_tool.py) | RAGInput, RAGTool | crewai, json, os, pydantic, typing |
| [src/tools/web_search_tool.py](src/tools/web_search_tool.py) | WebSearchInput, FirecrawlSearchTool | crewai, firecrawl, json, os, pydantic, typing |
| [src/workflows/agents.py](src/workflows/agents.py) | Agents, create_rag_agent, create_memory_agent, create_web_search_agent, create_arxiv_agent, create_evaluator_agent, create_synthesizer_agent | crewai, os, src, typing |
| [src/workflows/flow.py](src/workflows/flow.py) | ResearchAssistantState, ContextEvaluationResult, ResearchAssistantFlow, create_research_assistant_flow, Config, process_query, gather_context_from_all_sources, evaluate_context_relevance, synthesize_final_response, process_documents | agents, crewai, json, os, pydantic, src, tasks, typing |
| [src/workflows/tasks.py](src/workflows/tasks.py) | Tasks, create_rag_search_task, create_memory_retrieval_task, create_web_search_task, create_arxiv_search_task, create_context_evaluation_task, create_synthesis_task | crewai, json, src, typing |
| [config/agents/research_agents.yaml](config/agents/research_agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [config/tasks/research_tasks.yaml](config/tasks/research_tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 72 | initialize_session_state | FunctionDef |
| [app.py](app.py) | 91 | check_api_keys | FunctionDef |
| [app.py](app.py) | 102 | StreamlitResearchAssistant | ClassDef |
| [app.py](app.py) | 144 | create_research_assistant | FunctionDef |
| [app.py](app.py) | 154 | process_uploaded_document | FunctionDef |
| [app.py](app.py) | 236 | display_citations_dropdown | FunctionDef |
| [app.py](app.py) | 554 | display_sidebar_document_processing | FunctionDef |
| [app.py](app.py) | 609 | display_main_chat_interface | FunctionDef |
| [app.py](app.py) | 669 | display_initialization_message | FunctionDef |
| [app.py](app.py) | 672 | main | FunctionDef |
| [app.py](app.py) | 109 | initialize | FunctionDef |
| [app.py](app.py) | 127 | query | FunctionDef |
| [src/config/config_loader.py](src/config/config_loader.py) | 6 | ConfigLoader | Utility class for loading YAML configuration files |
| [src/config/config_loader.py](src/config/config_loader.py) | 16 | load_agents_config | Load agents configuration from YAML file |
| [src/config/config_loader.py](src/config/config_loader.py) | 21 | load_tasks_config | Load tasks configuration from YAML file |
| [src/config/config_loader.py](src/config/config_loader.py) | 45 | get_agent_config | Get configuration for a specific agent |
| [src/config/config_loader.py](src/config/config_loader.py) | 54 | get_task_config | Get configuration for a specific task |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | 57 | TensorLakeClient | ClassDef |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | 61 | list_uploaded_files | FunctionDef |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | 72 | verify_file_uploaded | FunctionDef |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | 83 | upload | FunctionDef |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | 119 | parse_structured | FunctionDef |
| [src/document_processing/doc_parser.py](src/document_processing/doc_parser.py) | 165 | get_result | FunctionDef |
| [src/generation/generation.py](src/generation/generation.py) | 52 | StructuredResponseGen | ClassDef |
| [src/generation/generation.py](src/generation/generation.py) | 67 | generate | FunctionDef |
| [src/memory/memory.py](src/memory/memory.py) | 9 | ZepMemoryLayer | ClassDef |
| [src/memory/memory.py](src/memory/memory.py) | 40 | as_external_memory | FunctionDef |
| [src/memory/memory.py](src/memory/memory.py) | 43 | save_user_message | FunctionDef |
| [src/memory/memory.py](src/memory/memory.py) | 49 | save_assistant_message | FunctionDef |
| [src/memory/memory.py](src/memory/memory.py) | 55 | save_preferences | FunctionDef |
| [src/memory/memory.py](src/memory/memory.py) | 61 | wait_for_indexing | FunctionDef |
| [src/memory/memory.py](src/memory/memory.py) | 64 | get_context_block | Fetch the full user context block from Zep memory. |
| [src/rag/embeddings.py](src/rag/embeddings.py) | 11 | ContextualizedEmbeddings | ClassDef |
| [src/rag/embeddings.py](src/rag/embeddings.py) | 16 | embed_document_chunks | FunctionDef |
| [src/rag/embeddings.py](src/rag/embeddings.py) | 33 | embed_query | FunctionDef |
| [src/rag/rag_pipeline.py](src/rag/rag_pipeline.py) | 8 | RAGPipeline | Unified RAG pipeline combining document parsing, embeddings, and retrieval |
| [src/rag/rag_pipeline.py](src/rag/rag_pipeline.py) | 23 | process_documents | FunctionDef |
| [src/rag/rag_pipeline.py](src/rag/rag_pipeline.py) | 100 | retrieve_context | FunctionDef |
| [src/rag/rag_pipeline.py](src/rag/rag_pipeline.py) | 111 | generate_response | FunctionDef |
| [src/rag/rag_pipeline.py](src/rag/rag_pipeline.py) | 127 | query | FunctionDef |
| [src/rag/retriever.py](src/rag/retriever.py) | 4 | MilvusVectorDB | ClassDef |
| [src/rag/retriever.py](src/rag/retriever.py) | 35 | insert | FunctionDef |
| [src/rag/retriever.py](src/rag/retriever.py) | 65 | get_collection_count | FunctionDef |
| [src/rag/retriever.py](src/rag/retriever.py) | 72 | search | FunctionDef |
| [src/tools/arxiv_tool.py](src/tools/arxiv_tool.py) | 9 | ArxivAPIInput | Input schema for ArXiv API tool |
| [src/tools/arxiv_tool.py](src/tools/arxiv_tool.py) | 18 | ArxivTool | ClassDef |
| [src/tools/memory_tool.py](src/tools/memory_tool.py) | 9 | MemoryInput | Input schema for memory search tool |
| [src/tools/memory_tool.py](src/tools/memory_tool.py) | 13 | MemoryTool | ClassDef |
| [src/tools/rag_tool.py](src/tools/rag_tool.py) | 8 | RAGInput | Input schema for RAG search tool |
| [src/tools/rag_tool.py](src/tools/rag_tool.py) | 15 | RAGTool | ClassDef |
| [src/tools/web_search_tool.py](src/tools/web_search_tool.py) | 8 | WebSearchInput | Input schema for web search tool |
| [src/tools/web_search_tool.py](src/tools/web_search_tool.py) | 13 | FirecrawlSearchTool | ClassDef |
| [src/workflows/agents.py](src/workflows/agents.py) | 16 | Agents | Class for creating agents from configuration files |
| [src/workflows/agents.py](src/workflows/agents.py) | 21 | create_rag_agent | FunctionDef |
| [src/workflows/agents.py](src/workflows/agents.py) | 32 | create_memory_agent | FunctionDef |
| [src/workflows/agents.py](src/workflows/agents.py) | 43 | create_web_search_agent | FunctionDef |
| [src/workflows/agents.py](src/workflows/agents.py) | 54 | create_arxiv_agent | FunctionDef |
| [src/workflows/agents.py](src/workflows/agents.py) | 65 | create_evaluator_agent | FunctionDef |
| [src/workflows/agents.py](src/workflows/agents.py) | 74 | create_synthesizer_agent | FunctionDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 13 | ResearchAssistantState | ClassDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 19 | ContextEvaluationResult | Pydantic schema for context evaluation agent output validation |
| [src/workflows/flow.py](src/workflows/flow.py) | 65 | ResearchAssistantFlow | ClassDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 245 | create_research_assistant_flow | FunctionDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 38 | Config | ClassDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 103 | process_query | FunctionDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 116 | gather_context_from_all_sources | FunctionDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 149 | evaluate_context_relevance | FunctionDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 182 | synthesize_final_response | FunctionDef |
| [src/workflows/flow.py](src/workflows/flow.py) | 241 | process_documents | FunctionDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 8 | Tasks | ClassDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 12 | create_rag_search_task | FunctionDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 20 | create_memory_retrieval_task | FunctionDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 28 | create_web_search_task | FunctionDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 36 | create_arxiv_search_task | FunctionDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 44 | create_context_evaluation_task | FunctionDef |
| [src/workflows/tasks.py](src/workflows/tasks.py) | 65 | create_synthesis_task | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `agents`, `crewai`, `dotenv`, `firecrawl`, `json`, `openai`, `os`, `pathlib`, `pydantic`, `pymilvus`, `requests`, `src`, `streamlit`, `tasks`, `tempfile`, `tensorlake`, `time`, `typing`, `voyageai`, `xml`, `yaml`, `zep_cloud`, `zep_crewai`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `OPENAI_API_KEY`
- `TENSORLAKE_API_KEY`
- `VOYAGE_API_KEY`
- `ZEP_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/context-engineering-workflow); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
