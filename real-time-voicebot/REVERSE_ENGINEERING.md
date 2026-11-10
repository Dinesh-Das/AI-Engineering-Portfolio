# Reverse engineering: real-time-voicebot

## Problem and reconstructed mechanism

Implement a streaming travel conversation with ASR, an LLM and TTS.

AI_Assistant manages transcription callbacks, response generation and synthesized playback.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
audio stream/upload -> ASR with timestamps -> turn/segment state -> retrieval or analysis -> model output -> TTS or structured notes
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | AI_Assistant, stop_transcription, on_open, on_error, on_close, on_data, start_transcription, generate_ai_response, generate_audio | assemblyai, elevenlabs, openai |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 6 | AI_Assistant | ClassDef |
| [app.py](app.py) | 20 | stop_transcription | FunctionDef |
| [app.py](app.py) | 25 | on_open | FunctionDef |
| [app.py](app.py) | 29 | on_error | FunctionDef |
| [app.py](app.py) | 33 | on_close | FunctionDef |
| [app.py](app.py) | 37 | on_data | FunctionDef |
| [app.py](app.py) | 45 | start_transcription | FunctionDef |
| [app.py](app.py) | 59 | generate_ai_response | FunctionDef |
| [app.py](app.py) | 79 | generate_audio | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-3.5-turbo`

Detected import roots: `assemblyai`, `elevenlabs`, `openai`

Retained dependency manifests: None. Reproducible dependency resolution remains a prerequisite for a live run.

Environment names detected from code/configuration:

No literal names detected; configuration may be passed through arguments or external SDK defaults.

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/real-time-voicebot); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
