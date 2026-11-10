# Reverse engineering: rag-voice-agent

## Problem and reconstructed mechanism

Connect spoken interaction to document retrieval and speech synthesis.

LiveKit prewarming loads the RAG stack while session entrypoints connect ASR, model/tool use and Cartesia or OpenAI speech.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
audio stream/upload -> ASR with timestamps -> turn/segment state -> retrieval or analysis -> model output -> TTS or structured notes
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [voice_agent.py](voice_agent.py) | prewarm, entrypoint | dotenv, livekit, llama_index, logging, os |
| [voice_agent_openai.py](voice_agent_openai.py) | prewarm, entrypoint | dotenv, livekit, llama_index, logging, os |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [voice_agent.py](voice_agent.py) | 47 | prewarm | FunctionDef |
| [voice_agent.py](voice_agent.py) | 51 | entrypoint | AsyncFunctionDef |
| [voice_agent_openai.py](voice_agent_openai.py) | 42 | prewarm | FunctionDef |
| [voice_agent_openai.py](voice_agent_openai.py) | 46 | entrypoint | AsyncFunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `BAAI/bge-small-en-v1.5`
- `gemma3`
- `sonic-2`

Detected import roots: `dotenv`, `livekit`, `llama_index`, `logging`, `os`

Retained dependency manifests: [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `ASSEMBLYAI_API_KEY`
- `CARTESIA_API_KEY`
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_URL`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/rag-voice-agent); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
