# hugging-face-skills

Inspect reusable dataset, evaluation, training and publishing scripts for AI agents.

## What is in this folder

AI implementation with Python source and/or notebooks; retained UI source is available for study and explicit launch. Original source is reused under its upstream license; this is a source-backed learning port with recorded improvements, not a claim of an independently rewritten or production-certified implementation.

- [Reverse engineering](REVERSE_ENGINEERING.md): source map, architecture, model/dependency choices, code-level findings and changes.
- [Learnings and production deployment](LEARNINGS.md): rebuild sequence, experiments, metrics, tradeoffs and deployment proposal.
- [Evaluation protocol](EVALUATION.md): how to establish quality beyond syntax checks.
- [Personal learning journal](LEARNING_JOURNAL.md): your predictions, observations, explanations and next experiments; preserved during guide regeneration.
- [Executable enhancements](ENHANCEMENTS.md): project-specific CPU contracts, negative/recovery checks, real-data commands and deployment tradeoffs; run `python enhance.py check`.
- [Machine-readable project manifest](project.json) and [complete static analysis](analysis.json).

## Setup

Create a separate environment for this project. The collection tools use Python 3.12; the original project may require another version (see its manifest). Never combine all projects into one environment.
```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
```

Dependency manifests retained from source:

- [apps/evals-leaderboard/requirements.txt](apps/evals-leaderboard/requirements.txt)
- [apps/hackers-leaderboard/requirements.txt](apps/hackers-leaderboard/requirements.txt)
- [skills/hugging-face-evaluation/requirements.txt](skills/hugging-face-evaluation/requirements.txt)

Some manifests belong to nested subprojects or a TypeScript backend. Use the manifest-owning directory and the original installation instructions; no workspace-wide install is appropriate. For Node projects, review lifecycle scripts and use `npm ci --ignore-scripts` for the initial dependency inspection.

Read [UPSTREAM_README.md](UPSTREAM_README.md) for original setup details. Linux/Colab commands inside notebooks are not Windows PowerShell commands; review them before running.

Copy the empty environment template and fill only variables required by your selected path. Optional variables and server URLs may also appear in the detected list.
```powershell
Copy-Item .env.example .env
```

A `.env` file is loaded only if the selected implementation calls a dotenv loader. Otherwise set process environment variables or inject them through the job runtime. No credentials are bundled.


## Headless execution

From the collection root, preview the command without executing source:

```powershell
.\run.ps1 run --project "hugging-face-skills" --entry "enhance.py"
```

After configuring an isolated environment and reviewing the entry, append `--execute --timeout 120`. The runner uses the active virtual environment when called through run.ps1. Notebook execution also needs Jupyter/nbconvert and an appropriate kernel. Training commonly needs a longer job deadline and a GPU or remote training account. These are discovered candidates, not proof the selected dependency/provider combination has been tested.

| Candidate | Kind | UI dependency |
| --- | --- | --- |
| [apps/evals-leaderboard/app.py](apps/evals-leaderboard/app.py) | python | launch with ui action |
| [apps/evals-leaderboard/collect_evals.py](apps/evals-leaderboard/collect_evals.py) | python | headless candidate |
| [apps/hackers-leaderboard/app.py](apps/hackers-leaderboard/app.py) | python | launch with ui action |
| [apps/hackers-leaderboard/collect_points.py](apps/hackers-leaderboard/collect_points.py) | python | headless candidate |
| [scripts/generate_agents.py](scripts/generate_agents.py) | python | headless candidate |
| [skills/hugging-face-datasets/scripts/dataset_manager.py](skills/hugging-face-datasets/scripts/dataset_manager.py) | python | headless candidate |
| [skills/hugging-face-datasets/scripts/sql_manager.py](skills/hugging-face-datasets/scripts/sql_manager.py) | python | headless candidate |
| [skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py](skills/hugging-face-evaluation/examples/artificial_analysis_to_hub.py) | python | headless candidate |
| [skills/hugging-face-evaluation/scripts/evaluation_manager.py](skills/hugging-face-evaluation/scripts/evaluation_manager.py) | python | headless candidate |
| [skills/hugging-face-evaluation/scripts/inspect_eval_uv.py](skills/hugging-face-evaluation/scripts/inspect_eval_uv.py) | python | headless candidate |
| [skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py](skills/hugging-face-evaluation/scripts/inspect_vllm_uv.py) | python | headless candidate |
| [skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py](skills/hugging-face-evaluation/scripts/lighteval_vllm_uv.py) | python | headless candidate |
| [skills/hugging-face-evaluation/scripts/run_eval_job.py](skills/hugging-face-evaluation/scripts/run_eval_job.py) | python | headless candidate |
| [skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py](skills/hugging-face-evaluation/scripts/run_vllm_eval_job.py) | python | headless candidate |
| [skills/hugging-face-jobs/scripts/cot-self-instruct.py](skills/hugging-face-jobs/scripts/cot-self-instruct.py) | python | headless candidate |
| [skills/hugging-face-jobs/scripts/finepdfs-stats.py](skills/hugging-face-jobs/scripts/finepdfs-stats.py) | python | headless candidate |
| [skills/hugging-face-jobs/scripts/generate-responses.py](skills/hugging-face-jobs/scripts/generate-responses.py) | python | headless candidate |
| [skills/hugging-face-model-trainer/scripts/dataset_inspector.py](skills/hugging-face-model-trainer/scripts/dataset_inspector.py) | python | headless candidate |
| [skills/hugging-face-model-trainer/scripts/estimate_cost.py](skills/hugging-face-model-trainer/scripts/estimate_cost.py) | python | headless candidate |
| [skills/hugging-face-paper-publisher/scripts/paper_manager.py](skills/hugging-face-paper-publisher/scripts/paper_manager.py) | python | headless candidate |
| [skills/hugging-face-tool-builder/references/baseline_hf_api.py](skills/hugging-face-tool-builder/references/baseline_hf_api.py) | python | headless candidate |
| [enhance.py](enhance.py) | python | headless candidate |

## Verification status

Source inspection and integrity checks are offline. No live model inference, GPU training, provider compatibility test or cloud deployment is claimed. Static analysis found 0 syntax/format issues in the inspected Python units. IPython shell/magic lines are normalized only for inspection; they are not run. Findings and limitations appear in the reverse-engineering guide.

Run the collection check from its root: `.\run.ps1 check --project "hugging-face-skills"`.

## Provenance

Source: [hugging-face-skills](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/hugging-face-skills) at `042aeb5067384981eeba6a07fa882f436bb1660d`. Imported 2026-11-10. The original MIT notice is retained in [UPSTREAM_LICENSE](UPSTREAM_LICENSE); preserve any additional notices embedded in source files. Omitted artifacts and every source transformation are listed in project.json.
