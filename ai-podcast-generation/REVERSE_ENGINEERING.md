# Reverse engineering: ai-podcast-generation

## Problem and reconstructed mechanism

Turn source material into a two-speaker podcast with cloud or local generation.

Separate scraping, script generation and Kokoro speech modules make the pipeline reusable without the Streamlit shell.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated source -> extraction/script or prompt -> model generation -> validated segments -> assembly -> artifact manifest
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | init_session_state, initialize_generators, initialize_web_scraper, add_url_source, add_text_source, remove_source, render_sources_sidebar, generate_podcast, render_add_sources_tab, render_studio_tab, main | UI surface |
| [app_oss.py](app_oss.py) | init_session_state, initialize_generators, initialize_web_scraper, add_url_source, add_text_source, remove_source, render_sources_sidebar, generate_podcast, render_add_sources_tab, render_studio_tab, main | UI surface |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | PodcastScript, PodcastScriptGenerator, get_speaker_lines, to_json, generate_script_from_text | crewai, dataclasses, json, logging, typing |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | PodcastScript, PodcastScriptGeneratorOSS, get_speaker_lines, to_json, generate_script_from_text, check_ollama_connection | dataclasses, json, logging, requests, typing |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | AudioSegment, PodcastTTSGenerator, generate_podcast_audio | dataclasses, huggingface_hub, kokoro, logging, numpy, os, pathlib, soundfile |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | WebScraper, scrape_url | datetime, firecrawl, logging, typing, urllib |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 88 | init_session_state | FunctionDef |
| [app.py](app.py) | 103 | initialize_generators | FunctionDef |
| [app.py](app.py) | 136 | initialize_web_scraper | Initialize or reinitialize web scraper with provided API key |
| [app.py](app.py) | 150 | add_url_source | FunctionDef |
| [app.py](app.py) | 177 | add_text_source | FunctionDef |
| [app.py](app.py) | 193 | remove_source | FunctionDef |
| [app.py](app.py) | 199 | render_sources_sidebar | FunctionDef |
| [app.py](app.py) | 267 | generate_podcast | FunctionDef |
| [app.py](app.py) | 358 | render_add_sources_tab | FunctionDef |
| [app.py](app.py) | 382 | render_studio_tab | FunctionDef |
| [app.py](app.py) | 422 | main | FunctionDef |
| [app_oss.py](app_oss.py) | 99 | init_session_state | FunctionDef |
| [app_oss.py](app_oss.py) | 117 | initialize_generators | FunctionDef |
| [app_oss.py](app_oss.py) | 151 | initialize_web_scraper | Initialize or reinitialize web scraper with provided API key |
| [app_oss.py](app_oss.py) | 165 | add_url_source | FunctionDef |
| [app_oss.py](app_oss.py) | 192 | add_text_source | FunctionDef |
| [app_oss.py](app_oss.py) | 208 | remove_source | FunctionDef |
| [app_oss.py](app_oss.py) | 214 | render_sources_sidebar | FunctionDef |
| [app_oss.py](app_oss.py) | 282 | generate_podcast | FunctionDef |
| [app_oss.py](app_oss.py) | 373 | render_add_sources_tab | FunctionDef |
| [app_oss.py](app_oss.py) | 397 | render_studio_tab | FunctionDef |
| [app_oss.py](app_oss.py) | 437 | main | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 13 | PodcastScript | Represents a podcast script with metadata |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 34 | PodcastScriptGenerator | ClassDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 20 | get_speaker_lines | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 23 | to_json | FunctionDef |
| [src/podcast/script_generator.py](src/podcast/script_generator.py) | 44 | generate_script_from_text | FunctionDef |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | 12 | PodcastScript | Represents a podcast script with metadata |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | 33 | PodcastScriptGeneratorOSS | ClassDef |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | 19 | get_speaker_lines | FunctionDef |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | 22 | to_json | FunctionDef |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | 65 | generate_script_from_text | FunctionDef |
| [src/podcast/script_generator_oss.py](src/podcast/script_generator_oss.py) | 212 | check_ollama_connection | Check if Ollama is running and the model is available |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | 33 | AudioSegment | Represents a single audio segment with metadata |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | 42 | PodcastTTSGenerator | ClassDef |
| [src/podcast/text_to_speech.py](src/podcast/text_to_speech.py) | 61 | generate_podcast_audio | FunctionDef |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 12 | WebScraper | ClassDef |
| [src/web_scraping/web_scraper.py](src/web_scraping/web_scraper.py) | 18 | scrape_url | Scrape a URL and return the content as text. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `en_core_web_sm`
- `gpt-oss:20b`

Detected import roots: `crewai`, `dataclasses`, `datetime`, `dotenv`, `firecrawl`, `huggingface_hub`, `importlib`, `json`, `kokoro`, `logging`, `numpy`, `os`, `pathlib`, `requests`, `soundfile`, `spacy`, `src`, `streamlit`, `sys`, `tempfile`, `time`, `typing`, `urllib`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`
- `HF_HOME`
- `KOKORO_REPO_ID`
- `OPENAI_API_KEY`
- `PODCAST_CACHE_DIR`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/ai-podcast-generation); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
