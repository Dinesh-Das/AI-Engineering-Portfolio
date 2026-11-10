# Validation — 10 November 2026

The source-learning port passes the offline checks below. Machine-readable results are in [validation.json](validation.json).

| Check | Observed result |
| --- | --- |
| Upstream coverage | 119 inventory entries: 109 included, 4 completed local OCR folders preserved, 4 resource folders excluded, 2 missing README sources |
| Source integrity | All recorded source and local-addition hashes match; every included upstream path is imported or explicitly omitted |
| Python syntax | 364 source files compiled without execution |
| Notebook syntax | 555 code cells compiled without execution; 25 cells require IPython magic/shell normalization |
| Documentation | 564 generated/root documents checked for local-link validity |
| Learning preservation | Required learning sections checked for all 109 projects; personal journals are never overwritten during guide regeneration |
| Tooling/workflow tests | 43 passed, 1 skipped because this Windows host restricts unprivileged symlink creation |
| ColBERT reference tests | 4 passed: MaxSim, masked negative scores, stable top-k, invalid data |
| UI browser checks | All 7 learning interfaces passed lifecycle, session isolation, keyboard, responsive and automated accessibility checks; evidence matches current runtime source |
| Existing OCR preservation | 256 existing non-environment/code/document files matched their pre-task hashes; no OCR files were modified or staged |
| Runtime checks | PowerShell runner preview and explicit CPU MaxSim execution passed; podcast/meeting CLIs expose help without model dependencies |
| Metric example | Synthetic observations were parsed and summarized with explicit label coverage; these are not model benchmark results |
| Credential review | Recognizable token shapes and named credential literals were redacted; generated environment templates have empty values |

Commands:

```powershell
.\run.ps1 check
.\run.ps1 verify
.\run.ps1 test
.\run.ps1 run --project colbert-rag --entry maxsim.py --execute
.\run.ps1 evaluate --input docs/examples/observations.jsonl
```

No live LLM/ASR/TTS calls, GPU training, provider compatibility runs, full original-application dependency installs, Node backend builds, load tests or cloud deployments were performed. The new learning UIs were executed in an isolated browser using fixtures, and the provider transport was tested against a local contract-test server. Preserved upstream benchmarks and example outputs are historical source artifacts, not results produced by this port. Original framework wrappers were not launched by those fixture tests.

The limited static review detects selected patterns only. It does not establish that every imported demo is secure or production-ready. See each project's evaluation protocol and deployment learning guide for the remaining integration evidence.
