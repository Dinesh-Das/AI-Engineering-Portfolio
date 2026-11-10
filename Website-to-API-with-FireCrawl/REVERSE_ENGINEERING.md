# Reverse engineering: Website-to-API-with-FireCrawl

## Problem and reconstructed mechanism

Convert web content into schema-constrained extraction results.

The notebook builds dynamic Pydantic extraction schemas and calls Firecrawl to produce structured data.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated document/URL -> parse/render -> extraction schema -> model/parser output -> schema and domain validation -> provenance-linked record
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | load_app, reset_chat, create_dynamic_model, create_schema_from_fields, convert_to_table, stream_text | UI surface |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | WebsiteScraper, create_dynamic_model, create_schema_from_fields, convert_to_table, scrape_website | dotenv, firecrawl, os, pandas, pydantic, time, typing |
| [notebook.ipynb#cell-5](notebook.ipynb#cell-5) | ExtractSchema |  |
| [notebook.ipynb#cell-8](notebook.ipynb#cell-8) | ExtractSchema | firecrawl, pydantic |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 18 | load_app | FunctionDef |
| [app.py](app.py) | 29 | reset_chat | FunctionDef |
| [app.py](app.py) | 33 | create_dynamic_model | Create a dynamic Pydantic model from schema fields. |
| [app.py](app.py) | 56 | create_schema_from_fields | Create schema using Pydantic model. |
| [app.py](app.py) | 64 | convert_to_table | Convert a list of dictionaries to a markdown table. |
| [app.py](app.py) | 75 | stream_text | Stream text with a typing effect. |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 9 | WebsiteScraper | ClassDef |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 16 | create_dynamic_model | Create a dynamic Pydantic model from schema fields. |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 37 | create_schema_from_fields | Create schema using Pydantic model. |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 45 | convert_to_table | Convert data to a pandas DataFrame and return as string. |
| [notebook.ipynb#cell-2](notebook.ipynb#cell-2) | 53 | scrape_website | Main function to scrape website data. |
| [notebook.ipynb#cell-5](notebook.ipynb#cell-5) | 1 | ExtractSchema | ClassDef |
| [notebook.ipynb#cell-8](notebook.ipynb#cell-8) | 7 | ExtractSchema | ClassDef |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `base64`, `dotenv`, `firecrawl`, `gc`, `importlib`, `inspect`, `os`, `pandas`, `pathlib`, `pydantic`, `streamlit`, `sys`, `time`, `typing`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

- `FIRECRAWL_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [notebook.ipynb](notebook.ipynb) | Cleared notebook outputs, execution counters, execution metadata and saved widgets. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/firecrawl.png](assets/firecrawl.png) | Restored frontend source/asset after UI scope was authorized. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/schema.json](enhancement/examples/schema.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/reward.json](enhancement/examples/reward.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/splits.json](enhancement/examples/splits.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/distill.json](enhancement/examples/distill.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/Website-to-API-with-FireCrawl); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
