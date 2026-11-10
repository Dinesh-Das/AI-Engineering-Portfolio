# Reverse engineering: groundX-doc-pipeline

## Problem and reconstructed mechanism

Process complex documents and evaluate structured extraction quality.

GroundX utilities ingest and poll documents; CLI evaluation compares parsed invoice output against a reference.

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
validated document/URL -> parse/render -> extraction schema -> model/parser output -> schema and domain validation -> provenance-linked record
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI and headless entry points are classified separately in README.md. Definitions may describe variants rather than one sequential call chain.

| Source | Important definitions | Dependencies / role |
| --- | --- | --- |
| [app.py](app.py) | reset_analysis, prepare_chat_context, generate_chat_response, MockUploadedFile, getbuffer | UI surface |
| [evaluation_geval.py](evaluation_geval.py) | evaluate_invoice_parsing, EvaluatorGEval, create_evaluator_geval, process_invoice, run, gx_task, gpt_task | base64, dotenv, fitz, groundx, openai, opik, os, requests |
| [groundx_utils.py](groundx_utils.py) | create_client, ensure_bucket, ingest_document, poll_until_complete, fetch_xray_json, check_file_exists, get_xray_for_existing_document, process_document | UI surface |
| [run_evaluation_cli.py](run_evaluation_cli.py) | discover_invoice_files, infer_mime_type, main | argparse, dotenv, evaluation_geval, mimetypes, pathlib, typing |

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

| Source | Line in file/cell | Symbol | Contract clue |
| --- | --- | --- | --- |
| [app.py](app.py) | 54 | reset_analysis | Reset all analysis-related session state variables |
| [app.py](app.py) | 63 | prepare_chat_context | Prepare context from X-Ray data for the LLM |
| [app.py](app.py) | 94 | generate_chat_response | Generate AI response using Ollama with structured prompt engineering |
| [app.py](app.py) | 242 | MockUploadedFile | ClassDef |
| [app.py](app.py) | 247 | getbuffer | FunctionDef |
| [evaluation_geval.py](evaluation_geval.py) | 17 | evaluate_invoice_parsing | Evaluate invoice parsing results using Comet Opik's GEval metrics. |
| [evaluation_geval.py](evaluation_geval.py) | 100 | EvaluatorGEval | Evaluator that scores answers using GEval (LLM judge with rubric). |
| [evaluation_geval.py](evaluation_geval.py) | 288 | create_evaluator_geval | FunctionDef |
| [evaluation_geval.py](evaluation_geval.py) | 117 | process_invoice | FunctionDef |
| [evaluation_geval.py](evaluation_geval.py) | 229 | run | FunctionDef |
| [evaluation_geval.py](evaluation_geval.py) | 247 | gx_task | FunctionDef |
| [evaluation_geval.py](evaluation_geval.py) | 252 | gpt_task | FunctionDef |
| [groundx_utils.py](groundx_utils.py) | 18 | create_client | Initialize and return a Ground X API client instance |
| [groundx_utils.py](groundx_utils.py) | 25 | ensure_bucket | Ensure storage bucket exists and return its identifier |
| [groundx_utils.py](groundx_utils.py) | 36 | ingest_document | Upload and process document in Ground X, return processing identifier |
| [groundx_utils.py](groundx_utils.py) | 52 | poll_until_complete | Monitor document processing status until completion |
| [groundx_utils.py](groundx_utils.py) | 101 | fetch_xray_json | Retrieve X-Ray analysis data for documents in storage bucket |
| [groundx_utils.py](groundx_utils.py) | 115 | check_file_exists | Verify document existence in bucket and return document identifier |
| [groundx_utils.py](groundx_utils.py) | 123 | get_xray_for_existing_document | Retrieve X-Ray analysis data for existing document |
| [groundx_utils.py](groundx_utils.py) | 138 | process_document | Process document through Ground X pipeline and return analysis data |
| [run_evaluation_cli.py](run_evaluation_cli.py) | 12 | discover_invoice_files | Discover invoice files in the specified folder. |
| [run_evaluation_cli.py](run_evaluation_cli.py) | 22 | infer_mime_type | Infer MIME type for the given file path. |
| [run_evaluation_cli.py](run_evaluation_cli.py) | 28 | main | FunctionDef |

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

- `gpt-4o`

Detected import roots: `argparse`, `base64`, `beam`, `dotenv`, `evaluation_geval`, `fitz`, `groundx`, `groundx_utils`, `mimetypes`, `openai`, `opik`, `os`, `pathlib`, `requests`, `streamlit`, `tempfile`, `time`, `typing`

Retained dependency manifests: [pyproject.toml](pyproject.toml)

Environment names detected from code/configuration:

- `COMET_API_KEY`
- `GROUNDX_API_KEY`
- `OPENAI_API_KEY`
- `SAMPLE_FILE_NAME`

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

| File | Recorded change |
| --- | --- |
| [UPSTREAM_ENV.example](UPSTREAM_ENV.example) | Reference template renamed; local .env.example contains empty values. |
| [evaluation_geval.py](evaluation_geval.py) | Added explicit connection/read timeouts to 1 direct requests calls. |
| [UPSTREAM_README.md](UPSTREAM_README.md) | Preserved upstream README separately from the local learning guide. |
| [assets/groundx.png](assets/groundx.png) | Restored frontend source/asset after UI scope was authorized. |

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

| Source | Line | Rule | Review implication |
| --- | --- | --- | --- |
| [groundx_utils.py](groundx_utils.py) | 109 | network-timeout | HTTP call has no explicit timeout; a stalled peer can occupy a worker. |
| [groundx_utils.py](groundx_utils.py) | 130 | network-timeout | HTTP call has no explicit timeout; a stalled peer can occupy a worker. |

## Known source limitations

No syntax errors were detected in the inspected Python units/cells.

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/groundX-doc-pipeline); revision `042aeb5067384981eeba6a07fa882f436bb1660d`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
