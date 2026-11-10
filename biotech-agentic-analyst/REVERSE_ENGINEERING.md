# Reverse engineering: biotech-agentic-analyst

## Problem and reconstructed mechanism

Extract scientific figures and produce structured research intelligence.

Mistral document extraction feeds a quality-routed CrewAI ScienceFlow and typed FigureIntelligence records.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated document/URL -> parse/render -> extraction schema -> model/parser output -> schema and domain validation -> provenance-linked record
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | init_mistral_client | UI reference |
| [flow/crews/figure_analyst/crew.py](flow/crews/figure_analyst/crew.py) | FigureAnalystCrew, figure_analyst, figure_analysis, crew | __future__, crewai, models, os, typing |
| [flow/science_flow.py](flow/science_flow.py) | ScienceFlow, validate_extraction, route_on_quality, analyze_figures, handle_poor_quality | __future__, crewai, flow, hashlib, time, typing |
| [flow/state.py](flow/state.py) | ScienceFlowState | __future__, models, pydantic, typing |
| [mistral_ocr_pipeline/pipeline.py](mistral_ocr_pipeline/pipeline.py) | run_science_pipeline, parse_pipeline_results | __future__, json, models, pathlib, re, sys |
| [models.py](models.py) | ExtractedFigure, FigureIntelligence, FigureIntelligenceList | __future__, pydantic, typing |
| [utils.py](utils.py) | decode_thumbnail | PIL, __future__, base64, io, typing |
| [flow/crews/figure_analyst/config/agents.yaml](flow/crews/figure_analyst/config/agents.yaml) | backend/configuration source; inspect directly | .yaml |
| [flow/crews/figure_analyst/config/tasks.yaml](flow/crews/figure_analyst/config/tasks.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [flow/crews/figure_analyst/crew.py](flow/crews/figure_analyst/crew.py) | 19 | FigureAnalystCrew | Crew for extracting structured intelligence from scientific figures. |
| [flow/crews/figure_analyst/crew.py](flow/crews/figure_analyst/crew.py) | 29 | figure_analyst | FunctionDef |
| [flow/crews/figure_analyst/crew.py](flow/crews/figure_analyst/crew.py) | 39 | figure_analysis | FunctionDef |
| [flow/crews/figure_analyst/crew.py](flow/crews/figure_analyst/crew.py) | 46 | crew | FunctionDef |
| [flow/science_flow.py](flow/science_flow.py) | 25 | ScienceFlow | Orchestrates figure analysis. |
| [flow/science_flow.py](flow/science_flow.py) | 29 | validate_extraction | FunctionDef |
| [flow/science_flow.py](flow/science_flow.py) | 38 | route_on_quality | FunctionDef |
| [flow/science_flow.py](flow/science_flow.py) | 44 | analyze_figures | FunctionDef |
| [flow/science_flow.py](flow/science_flow.py) | 120 | handle_poor_quality | FunctionDef |
| [flow/state.py](flow/state.py) | 8 | ScienceFlowState | State for the science flow. |
| [mistral_ocr_pipeline/pipeline.py](mistral_ocr_pipeline/pipeline.py) | 83 | run_science_pipeline | Upload a PDF and run Mistral OCR 4 with Document AI figure extraction. |
| [mistral_ocr_pipeline/pipeline.py](mistral_ocr_pipeline/pipeline.py) | 144 | parse_pipeline_results | Parse OCR response into figures, page count, and average page confidence. |
| [models.py](models.py) | 7 | ExtractedFigure | Extracted figure from the document. |
| [models.py](models.py) | 22 | FigureIntelligence | Figure intelligence. |
| [models.py](models.py) | 55 | FigureIntelligenceList | List of figure intelligences. |
| [utils.py](utils.py) | 10 | decode_thumbnail | Decode a base64 string (raw or a data: URI) to an image. |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `mistral-ocr-4-0`

Detected import roots: `PIL`, `__future__`, `base64`, `crewai`, `dotenv`, `fitz`, `flow`, `hashlib`, `html`, `io`, `json`, `mistral_ocr_pipeline`, `mistralai`, `models`, `os`, `pathlib`, `pydantic`, `re`, `streamlit`, `sys`, `tempfile`, `time`, `typing`, `utils`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `FIGURE_ANALYST_MODEL`
- `MISTRAL_API_KEY`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/biotech-agentic-analyst); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
