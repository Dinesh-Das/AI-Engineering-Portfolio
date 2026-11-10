# UI validation

All seven added learning interfaces pass the isolated Chrome checks. Machine-readable evidence is in [ui-validation.json](ui-validation.json), fingerprinted against the exact runtime and project profiles. Changing that source invalidates the recorded evidence until the browser checks are rerun.

| Learning interface | Responsive widths | Accessibility result | Lifecycle result |
| --- | --- | --- | --- |
| Local Llama vision | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed, including image input |
| Local DeepSeek dialogue | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed |
| Gemma visual dialogue | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed, including image input |
| DeepSeek stream inspector | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed |
| Qwen thinking lab | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed |
| GPT-OSS response notebook | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed |
| Streaming state notebook | 320, 768, 1024, 1440 | Zero reported WCAG A/AA violations in the automated checks | Passed |

Each interface was tested for its empty state, safe literal-text rendering, completed stream, provider failure, empty final answer, cancellation, exclusion of failed/interrupted turns from history, separate-tab isolation, notes export, clear/reset and keyboard reachability. Trace panels remain collapsed by default. Screens were inspected visually; automated accessibility checks are evidence for the tested rules, not a complete accessibility certification.

Browser console/page errors and server tracebacks were absent in the final run. The first run exposed a Windows connection-abort exception during cancellation; a failing regression test reproduced it and the connection handler was corrected before the final checks.

Representative overview: [Qwen thinking lab](ui-screenshots/qwen3-thinking-ui-overview.png). Full desktop/mobile scenario screenshots are retained in ui-screenshots/ and use explicitly labeled fixture output.

The transport also has local HTTP integration tests for native thinking/content NDJSON, successful completion, premature EOF and rejected redirects. Fixtures deliberately simulate success, failure, slow output and no final answer. Their timings and text are not model benchmarks.

The browser test dependencies are pinned in tools/browser-tests/package-lock.json; their initial install used `--ignore-scripts`, and npm reported no known vulnerabilities in that small test dependency graph. This does not audit every imported application's original dependencies.

Live Ollama inference remains unverified because the local model server was unavailable. No model downloads, GPU training or cloud deployments were performed. Restored original Chainlit, Streamlit, Next.js and Motia applications need their own dependency/model/service integration checks; they are not represented as browser-tested by proxy. The Motia source's absent step files are documented and its local learning implementation is explicitly reconstructed.
