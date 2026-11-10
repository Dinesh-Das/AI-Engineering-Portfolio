# Reverse engineering: pixeltable-mcp

## Problem and reconstructed mechanism

Coordinate multimodal storage and computed transformations through MCP.

Separate audio, image, video and document servers wrap Pixeltable tables, embeddings and transformation functions.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
authenticated client -> tool discovery -> argument validation -> authorized operation -> bounded backend call -> structured result
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [audio-index/server.py](audio-index/server.py) | create_starlette_app, parse_arguments, handle_sse | argparse, logging, mcp, starlette, tools, uvicorn |
| [audio-index/test.py](audio-index/test.py) | top-level workflow | pixeltable |
| [audio-index/tools.py](audio-index/tools.py) | setup_audio_index, insert_audio, query_audio, list_audio_tables | logging, mcp, os, pixeltable, typing |
| [base-sdk/server.py](base-sdk/server.py) | create_starlette_app, handle_sse | argparse, mcp, starlette, tools, uvicorn |
| [base-sdk/tools.py](base-sdk/tools.py) | create_table, insert_data, add_computed_column, create_view, execute_query, create_query | mcp, pixeltable |
| [crewai_mcp.ipynb#cell-7](crewai_mcp.ipynb#cell-7) | top-level workflow |  |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | PixeltableFlowState, Specialist, PixeltableManagerFlow, start_flow, route_query, handle_image_task, handle_video_task, handle_audio_task, handle_document_task, handle_default_task, synthesize_result |  |
| [doc-index/server.py](doc-index/server.py) | create_starlette_app, handle_sse | argparse, mcp, starlette, tools, uvicorn |
| [doc-index/test.py](doc-index/test.py) | search_documents, find_relevant_text | pixeltable |
| [doc-index/tools.py](doc-index/tools.py) | setup_document_index, insert_document, query_document, list_document_tables | mcp, pixeltable |
| [image-index/server.py](image-index/server.py) | create_starlette_app, handle_sse | argparse, mcp, starlette, tools, uvicorn |
| [image-index/test.py](image-index/test.py) | top-level workflow | os, pixeltable |
| [image-index/tools.py](image-index/tools.py) | setup_image_index, insert_image, query_image, list_image_tables | mcp, os, pixeltable |
| [video-index/server.py](video-index/server.py) | create_starlette_app, handle_sse | argparse, mcp, starlette, tools, uvicorn |
| [video-index/test.py](video-index/test.py) | top-level workflow | datetime, pixeltable |
| [video-index/tools.py](video-index/tools.py) | setup_video_index, insert_video, query_video, list_video_tables | datetime, mcp, os, pixeltable |
| [docker-compose.yaml](docker-compose.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [audio-index/server.py](audio-index/server.py) | 21 | create_starlette_app | Create a Starlette application that can serve the provided mcp server with SSE. |
| [audio-index/server.py](audio-index/server.py) | 75 | parse_arguments | Parse command line arguments. |
| [audio-index/server.py](audio-index/server.py) | 33 | handle_sse | Handle SSE connections from clients. |
| [audio-index/tools.py](audio-index/tools.py) | 90 | setup_audio_index | Set up an audio index with the provided name and OpenAI API key. |
| [audio-index/tools.py](audio-index/tools.py) | 166 | insert_audio | Insert an audio file into the specified audio index. |
| [audio-index/tools.py](audio-index/tools.py) | 193 | query_audio | Query the specified audio index with a text question. |
| [audio-index/tools.py](audio-index/tools.py) | 237 | list_audio_tables | List all audio indexes currently available. |
| [base-sdk/server.py](base-sdk/server.py) | 10 | create_starlette_app | Create a Starlette application that can server the provied mcp server with SSE. |
| [base-sdk/server.py](base-sdk/server.py) | 14 | handle_sse | AsyncFunctionDef |
| [base-sdk/tools.py](base-sdk/tools.py) | 8 | create_table | Create a table in Pixeltable. |
| [base-sdk/tools.py](base-sdk/tools.py) | 73 | insert_data | Insert data into a table in Pixeltable. |
| [base-sdk/tools.py](base-sdk/tools.py) | 92 | add_computed_column | Add a computed column to a table in Pixeltable. |
| [base-sdk/tools.py](base-sdk/tools.py) | 127 | create_view | Create a view based on a table in Pixeltable. |
| [base-sdk/tools.py](base-sdk/tools.py) | 164 | execute_query | Execute a query on a table or view in Pixeltable. |
| [base-sdk/tools.py](base-sdk/tools.py) | 240 | create_query | Create a named query in Pixeltable. |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 1 | PixeltableFlowState | ClassDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 6 | Specialist | ClassDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 10 | PixeltableManagerFlow | A CrewAI Flow to intelligently delegate multimodal indexing/search queries |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 17 | start_flow | FunctionDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 22 | route_query | Uses an agent to determine the correct specialist for the user's query. |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 57 | handle_image_task | FunctionDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 115 | handle_video_task | FunctionDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 173 | handle_audio_task | FunctionDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 231 | handle_document_task | FunctionDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 289 | handle_default_task | FunctionDef |
| [crewai_mcp.ipynb#cell-12](crewai_mcp.ipynb#cell-12) | 308 | synthesize_result | Uses a synthesis agent to create a user-friendly final response. |
| [doc-index/server.py](doc-index/server.py) | 10 | create_starlette_app | Create a Starlette application that can server the provied mcp server with SSE. |
| [doc-index/server.py](doc-index/server.py) | 14 | handle_sse | AsyncFunctionDef |
| [doc-index/test.py](doc-index/test.py) | 39 | search_documents | FunctionDef |
| [doc-index/test.py](doc-index/test.py) | 68 | find_relevant_text | FunctionDef |
| [doc-index/tools.py](doc-index/tools.py) | 15 | setup_document_index | Set up a document index with the provided name. |
| [doc-index/tools.py](doc-index/tools.py) | 73 | insert_document | Insert a document file into the specified document index. |
| [doc-index/tools.py](doc-index/tools.py) | 94 | query_document | Query the specified document index with a text question. |
| [doc-index/tools.py](doc-index/tools.py) | 131 | list_document_tables | List all document indexes currently available. |
| [image-index/server.py](image-index/server.py) | 10 | create_starlette_app | Create a Starlette application that can server the provied mcp server with SSE. |
| [image-index/server.py](image-index/server.py) | 14 | handle_sse | AsyncFunctionDef |
| [image-index/tools.py](image-index/tools.py) | 32 | setup_image_index | Set up an image index with the provided name and OpenAI API key. |
| [image-index/tools.py](image-index/tools.py) | 90 | insert_image | Insert an image file into the specified image index. |
| [image-index/tools.py](image-index/tools.py) | 111 | query_image | Query the specified image index with a text description. |
| [image-index/tools.py](image-index/tools.py) | 149 | list_image_tables | List all image indexes currently available. |
| [video-index/server.py](video-index/server.py) | 10 | create_starlette_app | Create a Starlette application that can server the provied mcp server with SSE. |
| [video-index/server.py](video-index/server.py) | 14 | handle_sse | AsyncFunctionDef |
| [video-index/tools.py](video-index/tools.py) | 36 | setup_video_index | Set up a video index with the provided name and OpenAI API key. |
| [video-index/tools.py](video-index/tools.py) | 116 | insert_video | Insert a video file into the specified video index. |
| [video-index/tools.py](video-index/tools.py) | 137 | query_video | Query the specified video index with a text question. |
| [video-index/tools.py](video-index/tools.py) | 176 | list_video_tables | List all video indexes currently available. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `base.en`
- `gpt-4o-mini`
- `intfloat/e5-large-v2`
- `ollama/gemma3`
- `openai/gpt-4`
- `openai/o3-mini`
- `whisper-1`

Detected import roots: `IPython`, `argparse`, `crewai`, `crewai_tools`, `datetime`, `dotenv`, `logging`, `mcp`, `os`, `pixeltable`, `pydantic`, `starlette`, `tools`, `typing`, `uvicorn`

Retained dependency manifests: [audio-index/requirements.txt](audio-index/requirements.txt), [base-sdk/requirements.txt](base-sdk/requirements.txt), [doc-index/requirements.txt](doc-index/requirements.txt), [image-index/requirements.txt](image-index/requirements.txt), [pyproject.toml](pyproject.toml), [video-index/requirements.txt](video-index/requirements.txt)

Environment names detected from code/configuration:

- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [crewai_mcp.ipynb](crewai_mcp.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [base-sdk/tools.py](base-sdk/tools.py) | 115 | code-execution | Review inputs to eval; untrusted data can execute code. |
| [base-sdk/tools.py](base-sdk/tools.py) | 269 | code-execution | Review inputs to exec; untrusted data can execute code. |
| [base-sdk/tools.py](base-sdk/tools.py) | 150 | code-execution | Review inputs to eval; untrusted data can execute code. |
| [base-sdk/tools.py](base-sdk/tools.py) | 200 | code-execution | Review inputs to eval; untrusted data can execute code. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/pixeltable-mcp); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
