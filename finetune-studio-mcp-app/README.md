# finetune-studio-mcp-app

Study an MCP backend that submits and monitors Hugging Face fine-tuning jobs.

## What is in this folder

TypeScript AI application and its retained interface/configuration source; the added Python extension is a separate CPU learning lab. Original source is reused under its upstream license; this is a source-backed learning port with recorded improvements, not a claim of an independently rewritten or production-certified implementation.

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

- [package.json](package.json)

Some manifests belong to nested subprojects or a TypeScript backend. Use the manifest-owning directory and the original installation instructions; no workspace-wide install is appropriate. For Node projects, review lifecycle scripts and use `npm ci --ignore-scripts` for the initial dependency inspection.

Read [UPSTREAM_README.md](UPSTREAM_README.md) for original setup details. Linux/Colab commands inside notebooks are not Windows PowerShell commands; review them before running.

Copy the empty environment template and fill only variables required by your selected path. Optional variables and server URLs may also appear in the detected list.
```powershell
Copy-Item .env.example .env
```

A `.env` file is loaded only if the selected implementation calls a dotenv loader. Otherwise set process environment variables or inject them through the job runtime. No credentials are bundled.

## UI execution and learning

Original UI source is now in scope. Prepare the relevant manifest-owning environment before explicit launch; these framework integrations are not automatically verified.

Preview from the collection root:

```powershell
.\run.ps1 ui --project "finetune-studio-mcp-app" --entry "package.json"
```

Append `--execute` only after reviewing the entry and configuring its isolated dependencies. Original apps may require databases, model services or credentials.

| UI entry | Runtime |
| --- | --- |
| [package.json](package.json) | npm |


## Headless execution

From the collection root, preview the command without executing source:

```powershell
.\run.ps1 run --project "finetune-studio-mcp-app" --entry "enhance.py"
```

After configuring an isolated environment and reviewing the entry, append `--execute --timeout 120`. The runner uses the active virtual environment when called through run.ps1. Notebook execution also needs Jupyter/nbconvert and an appropriate kernel. Training commonly needs a longer job deadline and a GPU or remote training account. These are discovered candidates, not proof the selected dependency/provider combination has been tested.

| Candidate | Kind | UI dependency |
| --- | --- | --- |
| [enhance.py](enhance.py) | python | headless candidate |

## Verification status

Source inspection and integrity checks are offline. No live model inference, GPU training, provider compatibility test or cloud deployment is claimed. Static analysis found 0 syntax/format issues in the inspected Python units. IPython shell/magic lines are normalized only for inspection; they are not run. Findings and limitations appear in the reverse-engineering guide.

Run the collection check from its root: `.\run.ps1 check --project "finetune-studio-mcp-app"`.

## Provenance

Source: [finetune-studio-mcp-app](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/finetune-studio-mcp-app) at `042aeb5067384981eeba6a07fa882f436bb1660d`. Imported 2026-11-10. The original MIT notice is retained in [UPSTREAM_LICENSE](UPSTREAM_LICENSE); preserve any additional notices embedded in source files. Omitted artifacts and every source transformation are listed in project.json.
