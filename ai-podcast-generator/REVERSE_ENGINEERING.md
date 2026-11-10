# Reverse engineering: ai-podcast-generator

## Problem and reconstructed mechanism

Create article-to-podcast audio using MiniMax generation and speech.

WebScraper, ScriptGenerator and TTSConverter isolate the source, dialogue and audio stages; the upstream presentation script is malformed.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated source -> extraction/script or prompt -> model generation -> validated segments -> assembly -> artifact manifest
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [scraper.py](scraper.py) | WebScraper, scrape | dotenv, firecrawl, os |
| [script_generator.py](script_generator.py) | ScriptGenerator, generate | dotenv, os, requests |
| [tts_converter.py](tts_converter.py) | TTSConverter, convert | dotenv, os, requests, time |
| [cli.py](cli.py) | main | argparse, dotenv, json, os, pathlib, scraper, script_generator, tts_converter |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [scraper.py](scraper.py) | 8 | WebScraper | ClassDef |
| [scraper.py](scraper.py) | 12 | scrape | Scrape content from a given URL. |
| [script_generator.py](script_generator.py) | 8 | ScriptGenerator | ClassDef |
| [script_generator.py](script_generator.py) | 13 | generate | Generate podcast script from content using Minimax-M2. |
| [tts_converter.py](tts_converter.py) | 9 | TTSConverter | ClassDef |
| [tts_converter.py](tts_converter.py) | 22 | convert | Convert script to speech using Minimax TTS. |
| [cli.py](cli.py) | 9 | main | FunctionDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `argparse`, `dotenv`, `firecrawl`, `importlib`, `json`, `os`, `pathlib`, `requests`, `scraper`, `script_generator`, `sys`, `time`, `tts_converter`, `urllib`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `MINIMAX_API_KEY`
- `OPENROUTER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [reference/ui/app.py.invalid.txt](reference/ui/app.py.invalid.txt) | Quarantined malformed upstream UI script; AI modules remain available without that wrapper. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [script_generator.py](script_generator.py) | Added explicit connection/read timeouts to 1 direct requests calls. |
| [tts_converter.py](tts_converter.py) | Added explicit connection/read timeouts to 1 direct requests calls. |
| [cli.py](cli.py) | Added an input-bounded headless script/speech CLI with persisted stage status. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/artifacts.json](enhancement/examples/artifacts.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/segment.txt](enhancement/examples/segment.txt) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/ai-podcast-generator); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
