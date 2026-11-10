# Reverse engineering: paralegal-agent-crew

## Problem and reconstructed mechanism

Retrieve legal-document evidence, rerank it and use research fallback.

PDF embedding, Milvus storage, reranking and agent workflow modules separate retrieval from synthesis.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_chat, display_pdf, render_logs, load_and_split_pdf, initialize_workflow, run_workflow, cleanup_resources | UI surface |
| [config/settings.py](config/settings.py) | Settings, Config | os, pathlib, pydantic_settings |
| [examples/test.py](examples/test.py) | get_citations, print_citations, main, print_detailed_results, test_retrieval | asyncio, config, loguru, os, pathlib, pypdf, src, sys |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | batch_iterate, EmbedData, generate_embedding, embed, get_query_embedding, binary_quantize_query, clear | config, loguru, numpy, sentence_transformers, typing |
| [src/generation/rag.py](src/generation/rag.py) | ChatMessage, RAG, generate_context, query, get_detailed_response, set_prompt_template, set_system_message | config, crewai, loguru, pydantic, src, typing |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | MilvusVDB, initialize_client, create_collection, ingest_data, search, collection_exists, get_collection_info, close | config, loguru, pymilvus, src, typing |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | TextNode, NodeWithScore, Retriever, search, get_contexts, get_combined_context, search_with_scores, get_citations | config, loguru, pydantic, src, typing |
| [src/tools/firecrawl_search_tool.py](src/tools/firecrawl_search_tool.py) | FirecrawlSearchInput, FirecrawlSearchTool | config, crewai, firecrawl, os, pydantic, typing |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | ParalegalAgentState, ParalegalAgentWorkflow, retrieve, generate_rag_response, evaluate_response, perform_web_search, synthesize_response, run_workflow | config, crewai, events, loguru, pydantic, src, typing |
| [src/workflows/events.py](src/workflows/events.py) | RetrieveEvent, EvaluateEvent, WebSearchEvent, SynthesizeEvent | pydantic, src, typing |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 51 | reset_chat | Reset chat history and clear memory. |
| [app.py](app.py) | 57 | display_pdf | Display PDF preview in sidebar. |
| [app.py](app.py) | 69 | render_logs | Render logs with ANSI colors and emojis nicely in Streamlit |
| [app.py](app.py) | 84 | load_and_split_pdf | FunctionDef |
| [app.py](app.py) | 107 | initialize_workflow | FunctionDef |
| [app.py](app.py) | 183 | run_workflow | AsyncFunctionDef |
| [app.py](app.py) | 195 | cleanup_resources | Cleanup vector database and other resources. |
| [config/settings.py](config/settings.py) | 5 | Settings | ClassDef |
| [config/settings.py](config/settings.py) | 34 | Config | ClassDef |
| [examples/test.py](examples/test.py) | 19 | get_citations | Return retrieval results as simple citation dicts. |
| [examples/test.py](examples/test.py) | 35 | print_citations | FunctionDef |
| [examples/test.py](examples/test.py) | 50 | main | AsyncFunctionDef |
| [examples/test.py](examples/test.py) | 205 | print_detailed_results | FunctionDef |
| [examples/test.py](examples/test.py) | 225 | test_retrieval | AsyncFunctionDef |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 7 | batch_iterate | FunctionDef |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 11 | EmbedData | Handles document embedding with binary quantization support. |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 47 | generate_embedding | FunctionDef |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 57 | embed | FunctionDef |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 72 | get_query_embedding | FunctionDef |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 82 | binary_quantize_query | FunctionDef |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 89 | clear | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 8 | ChatMessage | ClassDef |
| [src/generation/rag.py](src/generation/rag.py) | 12 | RAG | ClassDef |
| [src/generation/rag.py](src/generation/rag.py) | 60 | generate_context | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 64 | query | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 72 | get_detailed_response | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 90 | set_prompt_template | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 95 | set_system_message | FunctionDef |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 7 | MilvusVDB | Milvus vector database with binary quantization support. |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 22 | initialize_client | FunctionDef |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 30 | create_collection | Create collection with binary vector support. |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 82 | ingest_data | Ingest embedded data into the vector database. |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 113 | search | FunctionDef |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 146 | collection_exists | FunctionDef |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 151 | get_collection_info | FunctionDef |
| [src/indexing/milvus_vdb.py](src/indexing/milvus_vdb.py) | 167 | close | FunctionDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 8 | TextNode | ClassDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 13 | NodeWithScore | ClassDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 17 | Retriever | ClassDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 28 | search | Search for relevant documents using vector similarity. |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 60 | get_contexts | FunctionDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 64 | get_combined_context | FunctionDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 68 | search_with_scores | FunctionDef |
| [src/retrieval/retriever_rerank.py](src/retrieval/retriever_rerank.py) | 82 | get_citations | FunctionDef |
| [src/tools/firecrawl_search_tool.py](src/tools/firecrawl_search_tool.py) | 8 | FirecrawlSearchInput | Input schema for Firecrawl web search tool |
| [src/tools/firecrawl_search_tool.py](src/tools/firecrawl_search_tool.py) | 13 | FirecrawlSearchTool | ClassDef |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 75 | ParalegalAgentState | ClassDef |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 79 | ParalegalAgentWorkflow | Paralegal Agent Workflow with router and web search fallback using CrewAI Flows. |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 98 | retrieve | Retrieve relevant documents from vector database |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 113 | generate_rag_response | Generate initial RAG response |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 130 | evaluate_response | Evaluate RAG response quality and route accordingly |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 145 | perform_web_search | Perform web search if insufficient information from RAG response |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 172 | synthesize_response | Synthesize final response from RAG and web search results |
| [src/workflows/agent_workflow.py](src/workflows/agent_workflow.py) | 210 | run_workflow | Run the complete flow for a given query. |
| [src/workflows/events.py](src/workflows/events.py) | 5 | RetrieveEvent | Event containing retrieved nodes from vector database. |
| [src/workflows/events.py](src/workflows/events.py) | 10 | EvaluateEvent | Event for evaluating RAG response quality. |
| [src/workflows/events.py](src/workflows/events.py) | 16 | WebSearchEvent | Event for web search when RAG response is insufficient. |
| [src/workflows/events.py](src/workflows/events.py) | 22 | SynthesizeEvent | Event for final response synthesis. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `ansi2html`, `asyncio`, `base64`, `config`, `contextlib`, `crewai`, `dotenv`, `events`, `firecrawl`, `gc`, `importlib`, `io`, `loguru`, `nest_asyncio`, `numpy`, `os`, `pathlib`, `pydantic`, `pydantic_settings`, `pymilvus`, `pypdf`, `re`, `sentence_transformers`, `src`, `streamlit`, `sys`, `tempfile`, `time`, `typing`, `uuid`, `warnings`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/corpus.json](enhancement/examples/corpus.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [src/embeddings/embed_data.py](src/embeddings/embed_data.py) | 31 | trust_remote_code | trust_remote_code=True crosses a code-execution trust boundary. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/paralegal-agent-crew); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
