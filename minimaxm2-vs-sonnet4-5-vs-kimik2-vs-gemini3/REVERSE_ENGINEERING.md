# Reverse engineering: minimaxm2-vs-sonnet4-5-vs-kimik2-vs-gemini3

## Problem and reconstructed mechanism

Benchmark several code-generation providers against common repository context.

Model-service mappings and Opik evaluation allow pairwise candidate generation and scoring.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
versioned task set -> identical context/settings -> candidate generation -> blinded grading -> independent executable checks -> paired comparison
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | handle_chat_input, process_model1_stream, process_model2_stream, validate_evaluation_result | UI surface |
| [code_evaluation_opik.py](code_evaluation_opik.py) | evaluate_code | opik |
| [code_ingestion.py](code_ingestion.py) | ingest_github_repo | gitingest |
| [model_service.py](model_service.py) | get_model_response_async, get_parallel_responses, get_model_responses, get_all_model_names, validate_model_name, get_model_mapping | asyncio, litellm, os, typing |
| [enhance.py](enhance.py) | main | importlib, pathlib, sys |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 186 | handle_chat_input | AsyncFunctionDef |
| [app.py](app.py) | 221 | process_model1_stream | AsyncFunctionDef |
| [app.py](app.py) | 240 | process_model2_stream | AsyncFunctionDef |
| [app.py](app.py) | 329 | validate_evaluation_result | FunctionDef |
| [code_evaluation_opik.py](code_evaluation_opik.py) | 4 | evaluate_code | Evaluate generated Python code using Comet Opik's GEval metrics. |
| [code_ingestion.py](code_ingestion.py) | 4 | ingest_github_repo | FunctionDef |
| [model_service.py](model_service.py) | 16 | get_model_response_async | AsyncFunctionDef |
| [model_service.py](model_service.py) | 76 | get_parallel_responses | Get parallel responses from two selected models. |
| [model_service.py](model_service.py) | 97 | get_model_responses | FunctionDef |
| [model_service.py](model_service.py) | 104 | get_all_model_names | Get all available model names for dropdown selection. |
| [model_service.py](model_service.py) | 113 | validate_model_name | Validate if a model name exists in available models. |
| [model_service.py](model_service.py) | 118 | get_model_mapping | Get the model mapping for a given model name. |
| [enhance.py](enhance.py) | 8 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.

Detected import roots: `asyncio`, `code_evaluation_opik`, `code_ingestion`, `dotenv`, `gitingest`, `importlib`, `litellm`, `model_service`, `opik`, `os`, `pandas`, `pathlib`, `plotly`, `streamlit`, `sys`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/best_practices.png](assets/best_practices.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/code_correctness.png](assets/code_correctness.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/code_readability.png](assets/code_readability.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/evaluate_generated_code.png](assets/evaluate_generated_code.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/generate_model_response.png](assets/generate_model_response.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/ingest_repository.png](assets/ingest_repository.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/streamlit_ui.png](assets/streamlit_ui.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/test_results_1.png](assets/test_results_1.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/test_results_2.png](assets/test_results_2.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/test_results_3.png](assets/test_results_3.png) | Restored frontend source/asset after UI scope was authorized. |
| [assets/test_results_4.png](assets/test_results_4.png) | Restored frontend source/asset after UI scope was authorized. |
| [enhance.py](enhance.py) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/profile.json](enhancement/profile.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/environment.json](enhancement/environment.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile](enhancement/Dockerfile) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/Dockerfile.dockerignore](enhancement/Dockerfile.dockerignore) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [ENHANCEMENTS.md](ENHANCEMENTS.md) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |
| [enhancement/examples/pairs.json](enhancement/examples/pairs.json) | Add executable CPU learning contract, synthetic scenarios and deployment tradeoffs. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/minimaxm2-vs-sonnet4-5-vs-kimik2-vs-gemini3); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
