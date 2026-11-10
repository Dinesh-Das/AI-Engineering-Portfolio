# knowledge distillation

Transfer classifier behavior from a teacher network to a smaller student.

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

The upstream project has no dependency manifest. Installation commands, where available, remain in UPSTREAM_README.md or notebook setup cells. Resolve and lock the specific packages in an isolated environment before running; imports alone do not establish compatible package versions.

Copy the empty environment template and fill only variables required by your selected path. Optional variables and server URLs may also appear in the detected list.
```powershell
Copy-Item .env.example .env
```

A `.env` file is loaded only if the selected implementation calls a dotenv loader. Otherwise set process environment variables or inject them through the job runtime. No credentials are bundled.


## Headless execution

From the collection root, preview the command without executing source:

```powershell
.\run.ps1 run --project "knowledge distillation" --entry "Knowledge-Distillation-Notebook.ipynb"
```

After configuring an isolated environment and reviewing the entry, append `--execute --timeout 120`. The runner uses the active virtual environment when called through run.ps1. Notebook execution also needs Jupyter/nbconvert and an appropriate kernel. Training commonly needs a longer job deadline and a GPU or remote training account. These are discovered candidates, not proof the selected dependency/provider combination has been tested.

| Candidate | Kind | UI dependency |
| --- | --- | --- |
| [Knowledge-Distillation-Notebook.ipynb](Knowledge-Distillation-Notebook.ipynb) | notebook | headless candidate |
| [enhance.py](enhance.py) | python | headless candidate |

## Verification status

Source inspection and integrity checks are offline. No live model inference, GPU training, provider compatibility test or cloud deployment is claimed. Static analysis found 0 syntax/format issues in the inspected Python units. IPython shell/magic lines are normalized only for inspection; they are not run. Findings and limitations appear in the reverse-engineering guide.

Run the collection check from its root: `.\run.ps1 check --project "knowledge distillation"`.

## Provenance

Source: [knowledge distillation](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/knowledge%20distillation) at `042aeb5067384981eeba6a07fa882f436bb1660d`. Imported 2026-11-10. The original MIT notice is retained in [UPSTREAM_LICENSE](UPSTREAM_LICENSE); preserve any additional notices embedded in source files. Omitted artifacts and every source transformation are listed in project.json.
