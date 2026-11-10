# Reverse engineering: motia-content-creation

## Problem and reconstructed mechanism

Implement event-driven article-to-social-content generation.

Motia steps accept a request, scrape content, generate platform-specific text and schedule delivery.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
request -> validated state -> plan/route -> scoped tool calls -> checked tool results -> synthesis -> persisted outcome
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [steps/api.step.py](steps/api.step.py) | RequestBody, SuccessResponse, ErrorResponse, handler | datetime, pydantic, time |
| [steps/generate-linkedin.step.py](steps/generate-linkedin.step.py) | GenerateInput, handler | datetime, dotenv, json, openai, os, pydantic |
| [steps/generate-twitter.step.py](steps/generate-twitter.step.py) | GenerateInput, handler | datetime, dotenv, json, openai, os, pydantic |
| [steps/scrape.step.py](steps/scrape.step.py) | ScrapeInput, handler | datetime, dotenv, firecrawl, os, pydantic |
| [config/index.js](config/index.js) | backend/configuration source; inspect directly | .js |
| [steps/schedule-linkedin.step.ts](steps/schedule-linkedin.step.ts) | backend/configuration source; inspect directly | .ts |
| [steps/schedule-twitter.step.ts](steps/schedule-twitter.step.ts) | backend/configuration source; inspect directly | .ts |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [steps/api.step.py](steps/api.step.py) | 5 | RequestBody | ClassDef |
| [steps/api.step.py](steps/api.step.py) | 8 | SuccessResponse | ClassDef |
| [steps/api.step.py](steps/api.step.py) | 14 | ErrorResponse | ClassDef |
| [steps/api.step.py](steps/api.step.py) | 32 | handler | AsyncFunctionDef |
| [steps/generate-linkedin.step.py](steps/generate-linkedin.step.py) | 14 | GenerateInput | ClassDef |
| [steps/generate-linkedin.step.py](steps/generate-linkedin.step.py) | 31 | handler | AsyncFunctionDef |
| [steps/generate-twitter.step.py](steps/generate-twitter.step.py) | 14 | GenerateInput | ClassDef |
| [steps/generate-twitter.step.py](steps/generate-twitter.step.py) | 31 | handler | AsyncFunctionDef |
| [steps/scrape.step.py](steps/scrape.step.py) | 11 | ScrapeInput | ClassDef |
| [steps/scrape.step.py](steps/scrape.step.py) | 26 | handler | AsyncFunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o`

Detected import roots: `datetime`, `dotenv`, `firecrawl`, `json`, `openai`, `os`, `pydantic`, `time`

Retained dependency manifests: [package.json](package.json), [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `MOTIA_PORT`
- `OLLAMA_MODEL`
- `OPENAI_API_KEY`
- `TYPEFULLY_API_KEY`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/motia-content-creation); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
