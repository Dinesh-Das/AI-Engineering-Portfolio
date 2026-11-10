# Reverse engineering: multimodal-rag-assemblyai

## Problem and reconstructed mechanism

Unify audio and document ingestion with vector retrieval and CrewAI flows.

A data-ingestion flow transcribes and embeds content into Milvus; a query flow searches and synthesizes.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [main.py](main.py) | DataIngestionState, QueryState, get_milvus_connection, get_collection, transcribe_audio_file, search_vector_database, format_search_results, SearchKnowledgeBaseTool, DataIngestionFlow, MultimodalRAGFlow, record_audio, process_query | PyPDF2, assemblyai, config, crewai, dataclasses, glob, logging, openai |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |
| [docker-compose.yml](docker-compose.yml) | backend/configuration source; inspect directly | .yml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [main.py](main.py) | 40 | DataIngestionState | State for data ingestion flow |
| [main.py](main.py) | 49 | QueryState | State for query processing flow |
| [main.py](main.py) | 58 | get_milvus_connection | Get or create Milvus connection |
| [main.py](main.py) | 71 | get_collection | Get or create collection |
| [main.py](main.py) | 81 | transcribe_audio_file | Transcribe audio file using AssemblyAI |
| [main.py](main.py) | 88 | search_vector_database | Search vector database for relevant information |
| [main.py](main.py) | 125 | format_search_results | Format search results into readable string |
| [main.py](main.py) | 143 | SearchKnowledgeBaseTool | Tool for searching the knowledge base |
| [main.py](main.py) | 156 | DataIngestionFlow | CrewAI Flow for data ingestion and vector database setup |
| [main.py](main.py) | 320 | MultimodalRAGFlow | CrewAI Flow for query processing and response generation |
| [main.py](main.py) | 423 | record_audio | Record audio from microphone and save to temporary file |
| [main.py](main.py) | 448 | process_query | Process a query through the RAG flow |
| [main.py](main.py) | 466 | check_system_status | Check if the system is ready |
| [main.py](main.py) | 492 | main | Main application entry point |
| [main.py](main.py) | 163 | discover_files | Discover all files in the data directory |
| [main.py](main.py) | 181 | setup_vector_database | Initialize Milvus connection and collection |
| [main.py](main.py) | 208 | process_multimodal_data | Process discovered files from the data directory |
| [main.py](main.py) | 273 | generate_embeddings_flow | Generate embeddings for processed chunks |
| [main.py](main.py) | 303 | store_in_vector_database | Insert processed chunks into Milvus |
| [main.py](main.py) | 327 | transcribe_audio_if_needed | Transcribe audio if query is audio-based |
| [main.py](main.py) | 340 | search_knowledge_base | Search the vector database for relevant information |
| [main.py](main.py) | 356 | generate_response | Generate final response using CrewAI agents |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `PyPDF2`, `assemblyai`, `config`, `crewai`, `dataclasses`, `dotenv`, `glob`, `importlib`, `logging`, `openai`, `os`, `pathlib`, `pymilvus`, `sounddevice`, `soundfile`, `sys`, `tempfile`, `traceback`, `typing`

Retained dependency manifests: [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `ASSEMBLYAI_API_KEY`
- `EMBEDDING_DIMENSION`
- `EMBEDDING_MODEL`
- `LLM_MODEL`
- `MILVUS_COLLECTION_NAME`
- `MILVUS_HOST`
- `MILVUS_PORT`
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

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/multimodal-rag-assemblyai); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
