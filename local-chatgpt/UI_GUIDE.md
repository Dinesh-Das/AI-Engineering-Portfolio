# UI learning guide: Local Llama vision

## Original mechanism and the improvement

The original Chainlit app passes image paths to the SDK, waits for a complete answer, then replays characters. This version sends bounded base64 images through the REST API and displays tokens as they arrive.

The original app and upstream guide remain in this folder. The added `learning_app.py`, `lab.json` and `learning_ui/` package form an independently runnable local implementation with no third-party Python dependencies. It preserves this project's model/capability focus while making transport and state explicit. It is a reconstruction for learning, not a claim that the original framework integration has been fully exercised.

## Run it

From the collection root:

```powershell
.\run.ps1 ui --project "local-chatgpt" --execute --timeout 3600 --entry-args --fixture --port 8765
```

Open http://127.0.0.1:8765. Fixture mode is visibly labeled and supports completed, provider-failure and slow-stream scenarios. It does not call a model. Omit `--fixture` to use a running local Ollama server and an already installed `llama3.2-vision` model. No model is downloaded automatically.

For an independent copy of this folder, run `python learning_app.py --fixture` from its own directory. The full learning runtime is bundled locally. Original Chainlit/Streamlit/Motia instructions remain in UPSTREAM_README.md and require their own dependencies.

## Trace the implementation

| Boundary | Source | What to inspect |
| --- | --- | --- |
| Project identity | [lab.json](lab.json) | Model, vision/thinking support, lesson and controlled experiment |
| Local entry | [learning_app.py](learning_app.py) | Starts this folder's bundled server and profile |
| Validation and model transport | [protocol.py](learning_ui/protocol.py) | Message/image budgets, native Ollama fields and NDJSON stream deadlines |
| Legacy trace parsing | [ReasoningSplitter](learning_ui/protocol.py) | Retains partial delimiters across chunks and preserves final-answer suffixes |
| HTTP and terminal events | [server.py](learning_ui/server.py) | Local-origin checks, bounded concurrency, fixture labeling, completion and failure events |
| Browser state | [app.js](learning_ui/static/app.js) | Separate transcript and completed history, abort handling, model-safe text rendering and notes export |
| Accessible layout | [index.html](learning_ui/static/index.html), [style.css](learning_ui/static/style.css) | Labeled controls, visible focus, live status and responsive columns |

## Controlled experiment

Ask about one image, then repeat the question without the image in a fresh conversation. Compare supported visual details and first-token latency.

Write your prediction before sending the first prompt. Keep the input and model revision fixed, change one parameter, and export the observations. A fixture timing measures the UI path; a live inference timing still does not prove answer correctness.

## Scenario exercises

1. Complete one turn. Trace the accepted event, deltas and completion event to the final history update.
2. In fixture mode, select provider failure. Inspect the visible partial output and prove that the failed turn is absent from the next model request's messages.
3. Select slow stream and stop generation. Confirm the interrupted status, restored controls and exclusion of partial history. Cancellation closes the local upstream response; it does not prove a remote worker has instantly stopped all computation.
4. Open a second browser tab. Confirm the first tab's conversation and notes are not automatically shared.
5. Clear the conversation and confirm the independent experiment notes remain. Export explicitly; no chat is stored automatically in local storage.
6. Navigate with the keyboard and resize the page to 320, 768, 1024 and 1440 pixels. Check composer reachability, overflow, focus and labeled status.
7. Switch to a live installed model only after local Ollama is available. Compare independently checked task correctness, first-token time, total time and reported token counts. Missing token counts remain missing.

## Key pitfall

Character-by-character display after a blocking model call is not provider streaming. Local deployment also needs image/context memory budgets.

Model-provided trace is generated output and may be incomplete or misleading. It is not a faithful audit of hidden model computation or proof of a correct answer. The UI keeps it collapsed and excludes it from subsequent answer history.

## Deliberate local limits and production direction

The app binds to loopback, validates local Host/Origin headers and exposes only fixed static/API paths. It keeps conversations in browser memory and allows at most two active generations. It validates image signatures and size, not complete image-codec semantics; a shared upload service needs full decoding/normalization. Input text, history, image bytes, output tokens, network reads and generated output are bounded.

This standard-library server is a learning runtime, not a public hosting stack. Before sharing it, add authenticated identities, owned durable sessions, queue-backed inference, per-user budgets, deployment monitoring and a reverse proxy with a production application server. Use immutable model/prompt/tool versions and test disconnect/cancellation and retry behavior under concurrency. The complete project-specific deployment discussion remains in [LEARNINGS.md](LEARNINGS.md).

## Evidence status

See the collection's [UI validation report](../docs/UI_VALIDATION.md) for browser/fixture checks. Fixtures establish interface behavior; no live model quality or GPU benchmark is implied. Restored original framework frontends are source material and need their own dependency/service integration checks.
