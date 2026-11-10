# Reverse engineering: video-rag-gemini

## Problem and reconstructed mechanism

Upload video to Gemini and ask grounded questions about its contents.

VideoProcessor and the headless demo upload a file, wait for processing and send multimodal requests.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated source -> extraction/script or prompt -> model generation -> validated segments -> assembly -> artifact manifest
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | VideoProcessor, is_video_file, get_file_size_mb, reset_chat, display_video, upload_video, wait_for_file_processing, chat_with_video | UI surface |
| [demo.py](demo.py) | demo_video_chat | dotenv, google, os, time |
| [test_setup.py](test_setup.py) | test_imports, test_api_key, test_gemini_connection, main | UI surface |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 25 | VideoProcessor | ClassDef |
| [app.py](app.py) | 72 | is_video_file | Check if uploaded file is a video |
| [app.py](app.py) | 80 | get_file_size_mb | Get file size in MB |
| [app.py](app.py) | 84 | reset_chat | Reset chat history and video state |
| [app.py](app.py) | 99 | display_video | Display uploaded video |
| [app.py](app.py) | 30 | upload_video | Upload video to Gemini File API |
| [app.py](app.py) | 42 | wait_for_file_processing | Wait for video file to be processed by Gemini |
| [app.py](app.py) | 57 | chat_with_video | Generate response based on video content and user prompt |
| [demo.py](demo.py) | 13 | demo_video_chat | Simple demo of video chat functionality |
| [test_setup.py](test_setup.py) | 10 | test_imports | Test if all required packages are installed |
| [test_setup.py](test_setup.py) | 37 | test_api_key | Test if API key is configured |
| [test_setup.py](test_setup.py) | 59 | test_gemini_connection | Test connection to Gemini API |
| [test_setup.py](test_setup.py) | 92 | main | Run all tests |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `base64`, `dotenv`, `google`, `importlib`, `mimetypes`, `os`, `pathlib`, `streamlit`, `sys`, `tempfile`, `time`

Retained dependency manifests: [requirements.txt](requirements.txt)

Environment names detected from code/configuration:

- `GEMINI_API_KEY`

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

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/video-rag-gemini); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
