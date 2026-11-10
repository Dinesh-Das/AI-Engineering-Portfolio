# Native OCR enhancement verification

Executed on 2026-11-10 in the four existing project virtual environments. Baselines were run before this pass. No inference backend or model weights were initialized by the new tests.

| Project | Before | After adding quality regressions | Lint / format |
| --- | --- | --- | --- |
| Latex-OCR-Lama | 12 passed | 14 passed | No project Ruff gate declared; Python tests passed |
| gemma3-ocr | 33 passed | 35 passed | `ruff check .` and `ruff format --check .` passed |
| llama-ocr | 44 passed | 46 passed | `ruff check .` and `ruff format --check .` passed |
| qwen-2.5VL-ocr | 33 passed | 35 passed | `ruff check .` and `ruff format --check .` passed |

Commands from each project: `.\.venv\Scripts\python.exe -m pytest -q`, and the two Ruff commands through that interpreter where applicable. Total: **130 native tests passed**, including eight new regressions. Existing tests validate each application's documented boundaries; the added tests exercise actual edit distance, Unicode normalization, empty-reference handling and one-to-one region precision.

Every OCR folder additionally executes six CPU scenarios through `enhance.py check`. See the [113-project report](ENHANCEMENT_REPORT.md). These synthetic checks do not measure real OCR model accuracy. Use independently labeled pages and boxes with `enhance.py quality --input YOUR_LABELS.json` for actual output scoring; CER is not a formula-equivalence or layout metric.

The OCR inference/UI code and existing learning documents were retained. The two pre-existing user edits in `Latex-OCR-Lama/docs/verification.md` and `Latex-OCR-Lama/scripts/verify_browser.py` were preserved and excluded from this task's commits. All 109 existing personal journals were checked against pre-pass hashes. Four OCR journals were added without replacing existing files.

This pass did not repeat the original OCR browser/model benchmarks, download models, call DashScope/Ollama inference, or certify GPU capacity. Native suites, CPU scenario reports, previous browser evidence and live-model quality are separate evidence layers.

The four enhancement commits and preserved local changes are recorded in [repository revisions](ocr-enhancement-revisions.json). The OCR repositories have no configured remotes here; retain their folders alongside the parent checkout when copying this workspace. The parent does not embed them as Git submodules.
