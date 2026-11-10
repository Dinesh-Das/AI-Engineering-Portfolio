# Reverse engineering: book-writer-flow

## Problem and reconstructed mechanism

Generate a researched outline and chapters with a persistent workflow state.

BookFlow produces an Outline, dispatches chapter-writing work and saves the assembled manuscript.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | Outline, OutlineCrew, research_agent, research_task, outline_writer, write_outline, crew | book_writing_flow, crewai, crewai_tools, pydantic |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | Chapter, ChapterWriterCrew, topic_researcher, research_topic, writer, write_chapter, crew | book_writing_flow, crewai, crewai_tools, pydantic |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | Chapter, BookState, BookFlow, kickoff, plot, generate_outline, generate_chapters, save_book, write_single_chapter | asyncio, book_writing_flow, crewai, dotenv, os, pydantic |
| [book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py](book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py) | BrightDataWebSearchToolInput, BrightDataWebSearchTool | crewai, dotenv, os, pydantic, requests, ssl, typing |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/config/agents.yaml](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/config/tasks.yaml](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/config/agents.yaml](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/config/tasks.yaml](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 9 | Outline | Outline of the book |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 15 | OutlineCrew | Outline Crew |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 22 | research_agent | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 28 | research_task | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 32 | outline_writer | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 37 | write_outline | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Outline_crew/outline_crew.py) | 42 | crew | Creates the Outline Crew |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 10 | Chapter | Chapter of the book |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 16 | ChapterWriterCrew | Chapter Writer Crew |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 23 | topic_researcher | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 29 | research_topic | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 33 | writer | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 38 | write_chapter | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py](book_flow/book_writing_flow/src/book_writing_flow/crews/Writer_crew/writer_crew.py) | 43 | crew | Creates the Research Crew |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 15 | Chapter | ClassDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 19 | BookState | ClassDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 26 | BookFlow | ClassDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 75 | kickoff | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 80 | plot | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 29 | generate_outline | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 36 | generate_chapters | AsyncFunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 67 | save_book | FunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/main.py](book_flow/book_writing_flow/src/book_writing_flow/main.py) | 40 | write_single_chapter | AsyncFunctionDef |
| [book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py](book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py) | 13 | BrightDataWebSearchToolInput | Input schema for BrightDataWebSearchTool. |
| [book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py](book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py) | 17 | BrightDataWebSearchTool | ClassDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/gemma3:4b`

Detected import roots: `asyncio`, `book_writing_flow`, `crewai`, `crewai_tools`, `dotenv`, `importlib`, `os`, `pathlib`, `pydantic`, `requests`, `ssl`, `sys`, `typing`

Retained dependency manifests: [book_flow/book_writing_flow/pyproject.toml](book_flow/book_writing_flow/pyproject.toml)

Environment names detected from code/configuration:

- `BRIGHDATA_PASSWORD`
- `BRIGHDATA_USERNAME`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py](book_flow/book_writing_flow/src/book_writing_flow/tools/custom_tool.py) | Added explicit connection/read timeouts to 1 direct requests calls. |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/payload.json](enhancement/examples/payload.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/book-writer-flow); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
