# Reverse engineering: streaming-ai-chatbot

## Problem and reconstructed mechanism

Understand event-driven chat state and recovery through an observable local implementation.

The pinned Motia metadata references three absent step files; a documented local Ollama reconstruction demonstrates accepted, streaming, completed, failed and interrupted states.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
labeled input -> validated request -> bounded model transport -> incremental thinking/answer events -> terminal status -> completed-turn history and experiment notes
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [learning_ui/protocol.py](learning_ui/protocol.py) | NoRedirect, local_opener, ReasoningSplitter, validate_request, loopback_base, stream_ollama, redirect_request, feed, finish | base64, binascii, json, math, re, time, urllib |
| [learning_ui/server.py](learning_ui/server.py) | fixture_chunks, make_server, main, Handler, log_message, headers_for, json_response, local_origin, do_GET, event, do_POST | argparse, http, json, pathlib, protocol, threading, time, urllib |
| [types.d.ts](types.d.ts) | backend/configuration source; inspect directly | .ts |
| [learning_ui/static/app.js](learning_ui/static/app.js) | backend/configuration source; inspect directly | .js |
| [learning_ui/static/index.html](learning_ui/static/index.html) | backend/configuration source; inspect directly | .html |
| [learning_ui/static/style.css](learning_ui/static/style.css) | backend/configuration source; inspect directly | .css |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 21 | NoRedirect | ClassDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 26 | local_opener | FunctionDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 31 | ReasoningSplitter | Keep partial delimiters between chunks so final-answer text is never dropped. |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 79 | validate_request | FunctionDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 134 | loopback_base | FunctionDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 144 | stream_ollama | FunctionDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 22 | redirect_request | FunctionDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 38 | feed | FunctionDef |
| [learning_ui/protocol.py](learning_ui/protocol.py) | 59 | finish | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 16 | fixture_chunks | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 31 | make_server | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 165 | main | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 35 | Handler | ClassDef |
| [learning_ui/server.py](learning_ui/server.py) | 36 | log_message | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 39 | headers_for | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 50 | json_response | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 55 | local_origin | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 63 | do_GET | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 87 | event | FunctionDef |
| [learning_ui/server.py](learning_ui/server.py) | 91 | do_POST | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `argparse`, `base64`, `binascii`, `http`, `json`, `learning_ui`, `math`, `pathlib`, `protocol`, `re`, `threading`, `time`, `urllib`

Retained dependency manifests: [package.json](package.json)

Environment names detected from code/configuration:

- `OPENAI_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [learning_ui/protocol.py](learning_ui/protocol.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/server.py](learning_ui/server.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/__init__.py](learning_ui/__init__.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/static/app.js](learning_ui/static/app.js) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/static/index.html](learning_ui/static/index.html) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/static/style.css](learning_ui/static/style.css) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [lab.json](lab.json) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_app.py](learning_app.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/streaming-ai-chatbot); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
