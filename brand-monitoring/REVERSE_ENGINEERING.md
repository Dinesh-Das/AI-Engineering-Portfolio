# Reverse engineering: brand-monitoring

## Problem and reconstructed mechanism

Collect brand signals across multiple platforms and synthesize reports.

CrewAI flow dispatches platform-specific crews and combines their structured analyses.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [brand_monitoring_flow/src/brand_monitoring_app.py](brand_monitoring_flow/src/brand_monitoring_app.py) | reset_analysis, start_analysis | UI surface |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | InstagramWriterReport, InstagramReport, InstagramCrew, analysis_agent, analysis_task, writer_agent, write_report_task, crew | crewai, pydantic |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | LinkedInWriterReport, LinkedInReport, LinkedInCrew, analysis_agent, analysis_task, writer_agent, write_report_task, crew | crewai, pydantic |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | WebWriterReport, WebReport, WebCrew, analysis_agent, analysis_task, writer_agent, write_report_task, crew | crewai, pydantic |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | XWriterReport, XReport, XCrew, analysis_agent, analysis_task, writer_agent, write_report_task, crew | crewai, pydantic |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | YoutubeWriterReport, YoutubeReport, YoutubeCrew, analysis_agent, analysis_task, writer_agent, write_report_task, crew | crewai, pydantic |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | BrandMonitoringState, BrandMonitoringFlow, kickoff, plot, scrape_data, scrape_data_and_analyse, linkedin_analysis, instagram_analysis, youtube_analysis, x_analysis, web_analysis | asyncio, brand_monitoring_flow, crewai, pydantic, requests, time |
| [brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py](brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py) | BrightDataWebSearchToolInput, BrightDataWebSearchTool, scrape_urls | crewai, dotenv, os, pydantic, requests, ssl, time, typing |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/config/agents.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/config/tasks.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/config/agents.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/config/tasks.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/config/agents.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/config/tasks.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/config/agents.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/config/tasks.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/config/agents.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/config/tasks.yaml](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [brand_monitoring_flow/src/brand_monitoring_app.py](brand_monitoring_flow/src/brand_monitoring_app.py) | 21 | reset_analysis | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_app.py](brand_monitoring_flow/src/brand_monitoring_app.py) | 27 | start_analysis | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 7 | InstagramWriterReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 12 | InstagramReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 21 | InstagramCrew | Instagram Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 28 | analysis_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 35 | analysis_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 41 | writer_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 48 | write_report_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/instagram_crew/instagram_crew.py) | 55 | crew | Creates the Instagram Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 5 | LinkedInWriterReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 10 | LinkedInReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 20 | LinkedInCrew | LinkedIn Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 27 | analysis_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 34 | analysis_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 40 | writer_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 47 | write_report_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/linkedin_crew/linkedin_crew.py) | 54 | crew | Creates the LinkedIn Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 5 | WebWriterReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 10 | WebReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 20 | WebCrew | Web Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 27 | analysis_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 34 | analysis_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 40 | writer_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 47 | write_report_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/web_crew/web_crew.py) | 54 | crew | Creates the Web Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 5 | XWriterReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 10 | XReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 20 | XCrew | X Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 27 | analysis_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 34 | analysis_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 40 | writer_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 47 | write_report_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/X_crew/X_crew.py) | 54 | crew | Creates the X Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 5 | YoutubeWriterReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 10 | YoutubeReport | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 21 | YoutubeCrew | YouTube Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 28 | analysis_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 35 | analysis_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 41 | writer_agent | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 48 | write_report_task | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py](brand_monitoring_flow/src/brand_monitoring_flow/crews/youtube_crew/youtube_crew.py) | 55 | crew | Creates the YouTube Analysis Crew |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 17 | BrandMonitoringState | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 46 | BrandMonitoringFlow | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 263 | kickoff | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 268 | plot | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 49 | scrape_data | FunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 68 | scrape_data_and_analyse | AsyncFunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 70 | linkedin_analysis | AsyncFunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 97 | instagram_analysis | AsyncFunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 124 | youtube_analysis | AsyncFunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 152 | x_analysis | AsyncFunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/main.py](brand_monitoring_flow/src/brand_monitoring_flow/main.py) | 182 | web_analysis | AsyncFunctionDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py](brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py) | 14 | BrightDataWebSearchToolInput | Input schema for BrightDataWebSearchTool. |
| [brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py](brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py) | 18 | BrightDataWebSearchTool | ClassDef |
| [brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py](brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py) | 46 | scrape_urls | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `ollama/deepseek-r1`

Detected import roots: `asyncio`, `base64`, `brand_monitoring_flow`, `crewai`, `dotenv`, `gc`, `os`, `pydantic`, `requests`, `ssl`, `streamlit`, `time`, `typing`

Retained dependency manifests: [brand_monitoring_flow/pyproject.toml](brand_monitoring_flow/pyproject.toml)

Environment names detected from code/configuration:

- `BRIGHT_DATA_API_KEY`
- `BRIGHT_DATA_PASSWORD`
- `BRIGHT_DATA_USERNAME`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py](brand_monitoring_flow/src/brand_monitoring_flow/tools/custom_tool.py) | Added explicit connection/read timeouts to 5 direct requests calls. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/brand-monitoring); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
