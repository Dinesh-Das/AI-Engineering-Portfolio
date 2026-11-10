# Reverse engineering: Youtube-trend-analysis

## Problem and reconstructed mechanism

Analyze channel or niche trends from collected video transcripts.

Bright Data collection feeds CrewAI agents configured by YAML to summarize and analyze video evidence.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_llm, create_agents_and_tasks, reset_chat, start_analysis, add_channel_field | UI reference |
| [brightdata_scrapper.py](brightdata_scrapper.py) | trigger_scraping_niche, trigger_scraping_channels, get_progress, get_output | dotenv, json, os, subprocess, time |
| [config.yaml](config.yaml) | backend/configuration source; inspect directly | .yaml |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [brightdata_scrapper.py](brightdata_scrapper.py) | 10 | trigger_scraping_niche | FunctionDef |
| [brightdata_scrapper.py](brightdata_scrapper.py) | 42 | trigger_scraping_channels | FunctionDef |
| [brightdata_scrapper.py](brightdata_scrapper.py) | 84 | get_progress | FunctionDef |
| [brightdata_scrapper.py](brightdata_scrapper.py) | 99 | get_output | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o`

Detected import roots: `base64`, `brightdata_scrapper`, `crewai`, `crewai_tools`, `dotenv`, `gc`, `json`, `os`, `streamlit`, `subprocess`, `tempfile`, `time`, `tqdm`, `yaml`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `BRIGHT_DATA_API_KEY`
- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/Youtube-trend-analysis); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
