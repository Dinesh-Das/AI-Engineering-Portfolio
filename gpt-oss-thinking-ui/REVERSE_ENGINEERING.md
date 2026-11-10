# Reverse engineering: gpt-oss-thinking-ui

## Problem and reconstructed mechanism

Render native thinking and answer channels incrementally for local GPT-OSS.

The original app collects both channels before displaying the result; the learning UI updates each stream channel and preserves an explicit terminal state.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
labeled input -> validated request -> bounded model transport -> incremental thinking/answer events -> terminal status -> completed-turn history and experiment notes
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | process_thinking_stream, display_message, display_assistant_message, display_chat_history, get_chat_model, handle_user_input, main | UI surface |
| [learning_ui/protocol.py](learning_ui/protocol.py) | NoRedirect, local_opener, ReasoningSplitter, validate_request, loopback_base, stream_ollama, redirect_request, feed, finish | base64, binascii, json, math, re, time, urllib |
| [learning_ui/server.py](learning_ui/server.py) | fixture_chunks, make_server, main, Handler, log_message, headers_for, json_response, local_origin, do_GET, event, do_POST | argparse, http, json, pathlib, protocol, threading, time, urllib |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |
| [learning_ui/static/app.js](learning_ui/static/app.js) | backend/configuration source; inspect directly | .js |
| [learning_ui/static/index.html](learning_ui/static/index.html) | backend/configuration source; inspect directly | .html |
| [learning_ui/static/style.css](learning_ui/static/style.css) | backend/configuration source; inspect directly | .css |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 9 | process_thinking_stream | Process streaming response with native thinking support. |
| [app.py](app.py) | 30 | display_message | Display a single message in the chat interface. |
| [app.py](app.py) | 40 | display_assistant_message | Display assistant message with thinking content if present. |
| [app.py](app.py) | 51 | display_chat_history | Display all previous messages in the chat history. |
| [app.py](app.py) | 62 | get_chat_model | Get a cached instance of the chat model. |
| [app.py](app.py) | 71 | handle_user_input | Handle new user input and generate assistant response. |
| [app.py](app.py) | 93 | main | Main function to handle the chat interface and streaming responses. |
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
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-oss:20b`

Detected import roots: `argparse`, `base64`, `binascii`, `http`, `importlib`, `json`, `learning_ui`, `math`, `ollama`, `pathlib`, `protocol`, `re`, `streamlit`, `sys`, `threading`, `time`, `urllib`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [learning_ui/protocol.py](learning_ui/protocol.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/server.py](learning_ui/server.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/__init__.py](learning_ui/__init__.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/static/app.js](learning_ui/static/app.js) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/static/index.html](learning_ui/static/index.html) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_ui/static/style.css](learning_ui/static/style.css) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [lab.json](lab.json) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [learning_app.py](learning_app.py) | Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/events.json](enhancement/examples/events.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/gpt-oss-thinking-ui); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
