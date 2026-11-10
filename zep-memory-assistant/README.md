# zep-memory-assistant

Add persistent Zep memory to an AutoGen conversational agent.

## What is in this folder

AI implementation with Python source and/or notebooks; original UI wrappers are reference only. Original source is reused under its upstream license; this is a source-backed learning port with recorded improvements, not a claim of an independently rewritten or production-certified implementation.

- [Reverse engineering](REVERSE_ENGINEERING.md): source map, architecture, model/dependency choices, code-level findings and changes.
- [Learnings and production deployment](LEARNINGS.md): rebuild sequence, experiments, metrics, tradeoffs and deployment proposal.
- [Evaluation protocol](EVALUATION.md): how to establish quality beyond syntax checks.
- [Machine-readable project manifest](project.json) and [complete static analysis](analysis.json).

## Setup

Create a separate environment for this project. The collection tools use Python 3.12; the original project may require another version (see its manifest). Never combine all projects into one environment.
```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
```

Dependency manifests retained from source:

- [pyproject.toml](pyproject.toml)

Review the dependency constraints and required Python version before installation. For a project declaring `[project]`, an isolated editable install is:
```powershell
python -m pip install -e .
```

If the project uses `uv.lock` and uv, use its documented `uv sync --frozen` path instead. A retained lockfile is upstream evidence, not a lock verified against this machine.

Read [UPSTREAM_README.md](UPSTREAM_README.md) for original setup details. Linux/Colab commands inside notebooks are not Windows PowerShell commands; review them before running.

Copy the empty environment template and fill only variables required by your selected path. Optional variables and server URLs may also appear in the detected list.
```powershell
Copy-Item .env.example .env
```

A `.env` file is loaded only if the selected implementation calls a dotenv loader. Otherwise set process environment variables or inject them through the job runtime. No credentials are bundled.

## Headless execution

Use the source walkthrough below to identify the backend integration boundary. There is no automatic launch command for this project. UI wrappers are not launched. For a guide-only project, deploy and test the external service described by the guide; this folder does not pretend to contain that service.

| Candidate | Kind | UI dependency |
| --- | --- | --- |
| [app.py](app.py) | python | reference only |

## Verification status

Source inspection and integrity checks are offline. No live model inference, GPU training, provider compatibility test or cloud deployment is claimed. Static analysis found 0 syntax/format issues in the inspected Python units. IPython shell/magic lines are normalized only for inspection; they are not run. Findings and limitations appear in the reverse-engineering guide.

Run the collection check from its root: `.\run.ps1 check --project "zep-memory-assistant"`.

## Provenance

Source: [zep-memory-assistant](https://github.com/patchy631/ai-engineering-hub/tree/042aeb5067384981eeba6a07fa882f436bb1660d/zep-memory-assistant) at `042aeb5067384981eeba6a07fa882f436bb1660d`. Imported 2026-11-10. The original MIT notice is retained in [UPSTREAM_LICENSE](UPSTREAM_LICENSE); preserve any additional notices embedded in source files. Omitted presentation assets and every source transformation are listed in project.json.
