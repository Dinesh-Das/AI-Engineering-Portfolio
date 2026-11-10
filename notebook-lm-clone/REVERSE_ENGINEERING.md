# Reverse engineering: notebook-lm-clone

## Problem and reconstructed mechanism

Build a document-grounded notebook backend with citations, memory and audio output.

Separate processing, embedding, retrieval, memory and podcast modules support a pipeline independent of the presentation shell.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
source -> parse/chunk -> embed -> persistent index -> retrieve -> optional rerank -> grounded synthesis -> cited answer
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | create_interactive_citations, init_session_state, reset_chat, initialize_pipeline, process_uploaded_files, process_urls, process_youtube_video, process_text, render_sources_sidebar, render_source_upload_dialog, render_chat_interface, generate_podcast | UI surface |
| [notebooks/notebook-lm-walkthrough.ipynb#cell-18](notebooks/notebook-lm-walkthrough.ipynb#cell-18) | top-level workflow | src |
| [notebooks/notebook-lm-walkthrough.ipynb#cell-27](notebooks/notebook-lm-walkthrough.ipynb#cell-27) | top-level workflow | src |
| [notebooks/notebook-lm-walkthrough.ipynb#cell-34](notebooks/notebook-lm-walkthrough.ipynb#cell-34) | top-level workflow | src |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | SpeakerSegment, AudioTranscriber, get_timestamp_str, transcribe_audio, get_transcript_summary, batch_transcribe, format_time | assemblyai, dataclasses, json, logging, os, pathlib, src, time |
| [src/audio_processing/youtube_transcriber.py](src/audio_processing/youtube_transcriber.py) | YouTubeTranscriber, extract_video_id, download_audio, transcribe_youtube_video, cleanup_temp_files | assemblyai, logging, os, pathlib, src, tempfile, typing, yt_dlp |
| [src/document_processing/doc_processor.py](src/document_processing/doc_processor.py) | DocumentChunk, DocumentProcessor, get_citation_info, process_document, batch_process | dataclasses, datetime, hashlib, logging, os, pathlib, pymupdf, typing |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | EmbeddedChunk, EmbeddingGenerator, to_vector_db_format, generate_embeddings, generate_query_embedding, get_embedding_dimension, batch_generate_embeddings | dataclasses, fastembed, logging, numpy, src, typing |
| [src/generation/rag.py](src/generation/rag.py) | RAGResult, RAGGenerator, get_citation_summary, generate_response, generate_summary | crewai, dataclasses, logging, os, src, typing |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | ConversationTurn, NotebookMemoryLayer, save_conversation_turn, save_user_preferences, save_document_metadata, get_conversation_context, get_relevant_memory, wait_for_indexing, get_session_summary, clear_session | crewai, dataclasses, datetime, logging, os, src, time, typing |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | PodcastScript, PodcastScriptGenerator, get_speaker_lines, to_json, generate_script_from_document, generate_script_from_text, generate_script_from_website | crewai, dataclasses, json, logging, os, src, typing |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | AudioSegment, PodcastTTSGenerator, generate_podcast_audio | dataclasses, json, kokoro, logging, numpy, os, pathlib, soundfile |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | MilvusVectorDB, create_index, insert_embeddings, search, delete_collection, get_chunk_by_id, close | json, logging, pathlib, pymilvus, src, typing |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | WebPageData, WebScraper, scrape_url, batch_scrape_urls, get_url_preview | dataclasses, datetime, firecrawl, logging, os, pathlib, src, time |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | NotebookLMPipeline, test_pipeline, process_documents, process_audio, process_url, ask_question, cleanup | logging, os, pathlib, src |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 16 | create_interactive_citations | FunctionDef |
| [app.py](app.py) | 278 | init_session_state | FunctionDef |
| [app.py](app.py) | 292 | reset_chat | FunctionDef |
| [app.py](app.py) | 322 | initialize_pipeline | FunctionDef |
| [app.py](app.py) | 391 | process_uploaded_files | FunctionDef |
| [app.py](app.py) | 447 | process_urls | FunctionDef |
| [app.py](app.py) | 488 | process_youtube_video | FunctionDef |
| [app.py](app.py) | 531 | process_text | FunctionDef |
| [app.py](app.py) | 572 | render_sources_sidebar | FunctionDef |
| [app.py](app.py) | 600 | render_source_upload_dialog | FunctionDef |
| [app.py](app.py) | 658 | render_chat_interface | FunctionDef |
| [app.py](app.py) | 749 | generate_podcast | FunctionDef |
| [app.py](app.py) | 899 | render_studio_tab | FunctionDef |
| [app.py](app.py) | 939 | main | FunctionDef |
| [app.py](app.py) | 30 | replace_citation | Replace citation number with interactive element |
| [app.py](app.py) | 795 | ChunkLike | ClassDef |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 17 | SpeakerSegment | Represents a speaker segment with timing and content |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 34 | AudioTranscriber | ClassDef |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 25 | get_timestamp_str | FunctionDef |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 46 | transcribe_audio | FunctionDef |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 264 | get_transcript_summary | FunctionDef |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 294 | batch_transcribe | FunctionDef |
| [src/audio_processing/audio_transcriber.py](src/audio_processing/audio_transcriber.py) | 26 | format_time | FunctionDef |
| [src/audio_processing/youtube_transcriber.py](src/audio_processing/youtube_transcriber.py) | 15 | YouTubeTranscriber | ClassDef |
| [src/audio_processing/youtube_transcriber.py](src/audio_processing/youtube_transcriber.py) | 25 | extract_video_id | FunctionDef |
| [src/audio_processing/youtube_transcriber.py](src/audio_processing/youtube_transcriber.py) | 34 | download_audio | FunctionDef |
| [src/audio_processing/youtube_transcriber.py](src/audio_processing/youtube_transcriber.py) | 69 | transcribe_youtube_video | FunctionDef |
| [src/audio_processing/youtube_transcriber.py](src/audio_processing/youtube_transcriber.py) | 124 | cleanup_temp_files | FunctionDef |
| [src/document_processing/doc_processor.py](src/document_processing/doc_processor.py) | 16 | DocumentChunk | Represents a processed document chunk with metadata for citations |
| [src/document_processing/doc_processor.py](src/document_processing/doc_processor.py) | 55 | DocumentProcessor | ClassDef |
| [src/document_processing/doc_processor.py](src/document_processing/doc_processor.py) | 38 | get_citation_info | FunctionDef |
| [src/document_processing/doc_processor.py](src/document_processing/doc_processor.py) | 61 | process_document | FunctionDef |
| [src/document_processing/doc_processor.py](src/document_processing/doc_processor.py) | 195 | batch_process | FunctionDef |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 14 | EmbeddedChunk | Document chunk with its embedding vector |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 36 | EmbeddingGenerator | ClassDef |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 20 | to_vector_db_format | FunctionDef |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 57 | generate_embeddings | FunctionDef |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 83 | generate_query_embedding | FunctionDef |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 92 | get_embedding_dimension | FunctionDef |
| [src/embeddings/embedding_generator.py](src/embeddings/embedding_generator.py) | 95 | batch_generate_embeddings | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 14 | RAGResult | Represents the result of RAG generation with citations |
| [src/generation/rag.py](src/generation/rag.py) | 36 | RAGGenerator | ClassDef |
| [src/generation/rag.py](src/generation/rag.py) | 22 | get_citation_summary | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 59 | generate_response | FunctionDef |
| [src/generation/rag.py](src/generation/rag.py) | 183 | generate_summary | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 18 | ConversationTurn | Represents a single conversation turn with context |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 27 | NotebookMemoryLayer | ClassDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 86 | save_conversation_turn | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 176 | save_user_preferences | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 192 | save_document_metadata | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 208 | get_conversation_context | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 217 | get_relevant_memory | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 245 | wait_for_indexing | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 249 | get_session_summary | FunctionDef |
| [src/memory/memory_layer.py](src/memory/memory_layer.py) | 275 | clear_session | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 14 | PodcastScript | Represents a podcast script with metadata |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 35 | PodcastScriptGenerator | ClassDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 21 | get_speaker_lines | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 24 | to_json | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 45 | generate_script_from_document | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 76 | generate_script_from_text | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 102 | generate_script_from_website | FunctionDef |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | 21 | AudioSegment | Represents a single audio segment with metadata |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | 30 | PodcastTTSGenerator | ClassDef |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | 45 | generate_podcast_audio | FunctionDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 13 | MilvusVectorDB | ClassDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 128 | create_index | FunctionDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 177 | insert_embeddings | FunctionDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 207 | search | FunctionDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 274 | delete_collection | FunctionDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 287 | get_chunk_by_id | FunctionDef |
| [src/vector_database/milvus_vector_db.py](src/vector_database/milvus_vector_db.py) | 332 | close | FunctionDef |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 18 | WebPageData | Represents scraped web page data with additional metadata |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 28 | WebScraper | ClassDef |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 35 | scrape_url | FunctionDef |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 160 | batch_scrape_urls | FunctionDef |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 187 | get_url_preview | FunctionDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 17 | NotebookLMPipeline | ClassDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 143 | test_pipeline | FunctionDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 53 | process_documents | FunctionDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 81 | process_audio | FunctionDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 101 | process_url | FunctionDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 121 | ask_question | FunctionDef |
| [tests/notebook_pipeline.py](tests/notebook_pipeline.py) | 135 | cleanup | FunctionDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-small-en-v1.5`
- `gpt-4o-mini`

Detected import roots: `assemblyai`, `crewai`, `dataclasses`, `datetime`, `dotenv`, `fastembed`, `firecrawl`, `hashlib`, `importlib`, `json`, `kokoro`, `logging`, `numpy`, `os`, `pathlib`, `pymilvus`, `pymupdf`, `re`, `soundfile`, `src`, `streamlit`, `sys`, `tempfile`, `time`, `typing`, `urllib`, `uuid`, `yt_dlp`, `zep_cloud`, `zep_crewai`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `ASSEMBLYAI_API_KEY`
- `FIRECRAWL_API_KEY`
- `OPENAI_API_KEY`
- `ZEP_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [notebooks/notebook-lm-walkthrough.ipynb](notebooks/notebook-lm-walkthrough.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/app-UI.png](assets/app-UI.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/flow-diagram.jpg](assets/flow-diagram.jpg) | Restored frontend source/asset after UI scope was authorized. |
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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/notebook-lm-clone); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
