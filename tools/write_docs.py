"""Render source-backed project guides from reviewed notes and measured source facts."""

import csv
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from .analysis import analyze_project

ROOT = Path(__file__).resolve().parents[1]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')


def link(path):
    return '[' + path + '](' + quote(path, safe='/#') + ')'


def table(headers, rows):
    def safe(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(safe(c) for c in row) + ' |' for row in rows])


def setup_instructions(root, report):
    lines = ['Create a separate environment for this project. The collection tools use Python 3.12; the original project may require another version (see its manifest). Never combine all projects into one environment.',
             '```powershell', 'python -m venv .venv', '.\\.venv\\Scripts\\Activate.ps1', 'python -m pip install --upgrade pip', '```']
    manifests = report['manifests']
    if manifests:
        lines += ['Dependency manifests retained from source:', '\n'.join('- ' + link(m) for m in manifests)]
        primary = next((m for m in manifests if m == 'pyproject.toml'), None)
        if primary:
            lines += ['Review the dependency constraints and required Python version before installation. For a project declaring `[project]`, an isolated editable install is:',
                      '```powershell', 'python -m pip install -e .', '```',
                      'If the project uses `uv.lock` and uv, use its documented `uv sync --frozen` path instead. A retained lockfile is upstream evidence, not a lock verified against this machine.']
        elif 'requirements.txt' in manifests:
            lines += ['```powershell', 'python -m pip install -r requirements.txt', '```']
        else:
            lines += ['Some manifests belong to nested subprojects or a TypeScript backend. Use the manifest-owning directory and the original installation instructions; no workspace-wide install is appropriate. For Node projects, review lifecycle scripts and use `npm ci --ignore-scripts` for the initial dependency inspection.']
    else:
        lines += ['The upstream project has no dependency manifest. Installation commands, where available, remain in UPSTREAM_README.md or notebook setup cells. Resolve and lock the specific packages in an isolated environment before running; imports alone do not establish compatible package versions.']
    if (root / 'UPSTREAM_README.md').exists():
        lines += ['Read ' + link('UPSTREAM_README.md') + ' for original setup details. Linux/Colab commands inside notebooks are not Windows PowerShell commands; review them before running.']
    lines += ['Copy the empty environment template and fill only variables required by your selected path. Optional variables and server URLs may also appear in the detected list.',
              '```powershell', 'Copy-Item .env.example .env', '```',
              'A `.env` file is loaded only if the selected implementation calls a dotenv loader. Otherwise set process environment variables or inject them through the job runtime. No credentials are bundled.']
    return '\n\n'.join(lines).replace('```powershell\n\n', '```powershell\n').replace('\n\n```', '\n```')


def project_docs(project, note, category):
    root = ROOT / project['id']
    all_records = project['files'] + project.get('local_additions', [])
    report = analyze_project(root, [r['path'] for r in all_records])
    report['environment'] = sorted(set(report['environment']) | set(project['analysis']['environment']))
    project.update(category=note['category'], purpose=note['purpose'], entries=report['entries'], analysis=report)
    project['validation']['syntax_errors'] = len(report['syntax_errors'])
    project['validation']['plain_python_units_checked'] = len(report['units'])
    headless = [e for e in report['entries'] if not e['ui']]
    recipe = note['category'] == 'recipe'
    source_kind = ('Integration/deployment guide; no vendored application runtime.' if recipe else
                   'Graph schema and event fixtures; no standalone application runtime.' if project['id'] == 'omnigraph-multi-agent' else
                   'TypeScript AI backend; UI components omitted.' if not report['units'] else
                   'AI implementation with Python source and/or notebooks; original UI wrappers are reference only.')
    env = '# Empty values only. Fill the subset used by your selected implementation.\n# See README.md and original manifests; this is not a list of mandatory secrets.\n'
    env += '\n'.join(name + '=' for name in report['environment']) + '\n'
    if not report['environment']:
        env += '# No literal environment names detected. Review SDK configuration and upstream instructions.\n'
    write(root / '.env.example', env)
    write(root / 'analysis.json', json.dumps(report, indent=2, ensure_ascii=False))
    entries_table = table(['Candidate', 'Kind', 'UI dependency'], [(link(e['path']), e['kind'], 'reference only' if e['ui'] else 'headless candidate') for e in report['entries']]) if report['entries'] else 'No standalone Python/notebook entry point was identified. The source may be a reusable library, an external-service recipe or a TypeScript backend.'
    if headless:
        entry = sorted(headless, key=lambda e: (e['path'].endswith('server.py'), len(Path(e['path']).parts), e['path']))[0]
        run = ('From the collection root, preview the command without executing source:\n\n```powershell\n' +
               f'.\\run.ps1 run --project "{project["id"]}" --entry "{entry["path"]}"\n```\n\n' +
               'After configuring an isolated environment and reviewing the entry, append `--execute --timeout 120`. The runner uses the active virtual environment when called through run.ps1. Notebook execution also needs Jupyter/nbconvert and an appropriate kernel. Training commonly needs a longer job deadline and a GPU or remote training account. These are discovered candidates, not proof the selected dependency/provider combination has been tested.')
    else:
        run = 'Use the source walkthrough below to identify the backend integration boundary. There is no automatic launch command for this project. UI wrappers are not launched. For a guide-only project, deploy and test the external service described by the guide; this folder does not pretend to contain that service.'
    readme = f'''# {project['id']}

{note['purpose']}

## What is in this folder

{source_kind} Original source is reused under its upstream license; this is a source-backed learning port with recorded improvements, not a claim of an independently rewritten or production-certified implementation.

- [Reverse engineering](REVERSE_ENGINEERING.md): source map, architecture, model/dependency choices, code-level findings and changes.
- [Learnings and production deployment](LEARNINGS.md): rebuild sequence, experiments, metrics, tradeoffs and deployment proposal.
- [Evaluation protocol](EVALUATION.md): how to establish quality beyond syntax checks.
- [Machine-readable project manifest](project.json) and [complete static analysis](analysis.json).

## Setup

{setup_instructions(root, report)}

## Headless execution

{run}

{entries_table}

## Verification status

Source inspection and integrity checks are offline. No live model inference, GPU training, provider compatibility test or cloud deployment is claimed. Static analysis found {len(report['syntax_errors'])} syntax/format issues in the inspected Python units. IPython shell/magic lines are normalized only for inspection; they are not run. Findings and limitations appear in the reverse-engineering guide.

Run the collection check from its root: `.\\run.ps1 check --project "{project['id']}"`.

## Provenance

Source: [{project['id']}]({project['source_url']}) at `{project['upstream_revision']}`. Imported 2026-11-10. The original MIT notice is retained in [UPSTREAM_LICENSE](UPSTREAM_LICENSE); preserve any additional notices embedded in source files. Omitted presentation assets and every source transformation are listed in project.json.
'''
    write(root / 'README.md', readme)
    source_rows = []
    for unit in report['units']:
        symbols = [s['name'] for s in unit['symbols'] if not s['name'].startswith('_')]
        if symbols or unit['models'] or unit['ui']:
            source_rows.append((link(unit['path']), ', '.join(symbols[:12]) or 'top-level workflow', 'UI reference' if unit['ui'] else ', '.join(unit['imports'][:8])))
    for relative in report['other_code']:
        source_rows.append((link(relative), 'backend/configuration source; inspect directly', Path(relative).suffix))
    if not source_rows:
        source_rows = [(link(f['path']), 'guide, schema or fixture', '') for f in project['files'][:20]]
    source_map = table(['Source', 'Important definitions', 'Dependencies / role'], source_rows)
    symbol_rows = []
    for unit in report['units']:
        if unit['ui']:
            continue
        for symbol in unit['symbols']:
            if not symbol['name'].startswith('_'):
                symbol_rows.append((link(unit['path']), symbol['line'], symbol['name'], symbol['doc'] or symbol['kind']))
    symbol_map = table(['Source', 'Line in file/cell', 'Symbol', 'Contract clue'], symbol_rows[:100]) if symbol_rows else 'There are no non-UI Python function/class definitions to map. Inspect the configuration, TypeScript sources or integration guide above.'
    changes = [(link(f['path']), change) for f in all_records for change in f['changes']]
    change_table = table(['File', 'Recorded change'], changes) if changes else 'No behavior-changing transformation was necessary during the initial source port.'
    findings = table(['Source', 'Line', 'Rule', 'Review implication'], [(link(f['path']), f['line'], f['rule'], f['message']) for f in report['findings']]) if report['findings'] else 'The limited static rules found no matching patterns. This does not establish application security, dependency safety or provider compatibility.'
    syntax = table(['Source', 'Line', 'Issue'], [(link(e['path']), e['line'], e['message']) for e in report['syntax_errors']]) if report['syntax_errors'] else 'No syntax errors were detected in the inspected Python units/cells.'
    model_text = '\n'.join('- `' + m + '`' for m in report['models']) or 'No literal model identifiers were detected. Inspect configuration, provider defaults and the original setup guide; absence from this list is not absence of a model dependency.'
    environment = '\n'.join('- `' + e + '`' for e in report['environment']) or 'No literal names detected; configuration may be passed through arguments or external SDK defaults.'
    reverse = f'''# Reverse engineering: {project['id']}

## Problem and reconstructed mechanism

{note['purpose']}

{note['mechanism']}

Conceptual data flow (an architectural interpretation of the source, not a recorded execution trace):

```text
{category['pipeline']}
```

## Source map

The following table is extracted from this project's actual retained files. Notebook cell numbers are one-based and include Markdown cells. UI definitions remain reference material and are not execution targets. Definitions may describe variants rather than one sequential call chain.

{source_map}

## Function and class walkthrough

Read the entry/orchestrator first, then the tool/retrieval/model adapter, then the output validator. Trace one input through the definitions below: identify accepted inputs, persistent state, external calls and returned artifacts. The complete symbol inventory is in analysis.json; line numbers refer to the imported version.

{symbol_map}

## Models, dependencies and configuration

Detected model literals (not a guarantee that a provider still serves them):

{model_text}

Detected import roots: {', '.join('`' + i + '`' for i in report['imports']) or 'No Python import roots; inspect the backend/service configuration.'}

Retained dependency manifests: {', '.join(link(m) for m in report['manifests']) or 'None. Reproducible dependency resolution remains a prerequisite for a live run.'}

Environment names detected from code/configuration:

{environment}

Some names are optional endpoints, tracing settings or path selectors. Read each lookup before deciding which values are required. Model weights, external services and training hardware are not supplied by this folder.

## Improvements actually applied

Every project now has a source/version manifest, empty environment template, a documented headless execution boundary, evaluation protocol and production learning guide. Source-level transformations are recorded below; SHA-256 hashes distinguish the original bytes from the local port. No untested dependency upgrade or provider migration is represented as completed.

{change_table}

## Code-level review leads

These AST rules detect a small set of risky patterns and are not a complete security audit. Enforce authorization and resource limits in deterministic code; prompts and tool descriptions are not access controls.

{findings}

## Known source limitations

{syntax}

Quarantined `.invalid.txt` files contain incomplete upstream examples, not runnable notebooks/scripts. Original UI shells may still couple initialization, caching and session state to the AI code; extracting those into tested backend services is described in LEARNINGS.md. A discovered entry may also require installation as a package, a database, service credentials or GPU support.

No source code was imported or executed by the inspection tool. No reported tutorial benchmark, accuracy or latency claim was reproduced. Review dependency locks and model licenses separately before a real release.

## Attribution and reproducibility

[Pinned upstream source]({project['source_url']}); revision `{project['upstream_revision']}`. `project.json` records file hashes, transformations, omissions and validation state. Original source notices, including any third-party exceptions, remain authoritative. Use the original file map to compare this port with the pinned upstream tree.
'''
    write(root / 'REVERSE_ENGINEERING.md', reverse)
    learning = f'''# Learnings and production deployment: {project['id']}

## The core lesson

{category['lesson']}

For this project specifically: {note['mechanism']}

## Rebuild it yourself

1. State the observable success condition: {note['purpose']}
2. Read the source map in REVERSE_ENGINEERING.md and sketch the actual input, intermediate state, external dependency and output. Identify the smallest headless unit that implements the AI concept.
3. Reproduce that unit on a tiny, fixed, non-sensitive fixture. Save expected results before changing models, chunking, prompts, reward functions or tool policies.
4. Connect one external dependency at a time in an isolated environment. Record package versions and model revisions. A successful import or HTTP 200 does not demonstrate task correctness.
5. Add the project-specific failure experiment below. Check that errors are distinguishable from empty/low-confidence results and that retries do not duplicate side effects.
6. Run the same evaluation before and after each change. Save source revision, dataset ID, generation settings, quality, latency and cost together. Explain any tradeoff using observed evidence.

## Project-specific experiment

{note['experiment']}

Use a fixed fixture set, a baseline run and one controlled change. Include a normal case, a malformed/unsupported input and a dependency failure. Record the intermediate artifact that proves where a failure occurred, rather than inferring it from the final prose.

## What to measure

{category['metrics']}

Quality targets depend on your domain and must be chosen before a release. This collection supplies a protocol and offline metric helpers, not fabricated passing model scores. See EVALUATION.md for a practical evidence log.

## Failure modes to understand

{category['failure']}

Inspect the project's actual review leads in REVERSE_ENGINEERING.md. Fix a failure at its owning boundary: bad retrieval at the index/retriever, invalid data at the schema, unauthorized access at the tool/data service, and duplicate operations at the persisted job boundary.

## Better production deployment

Recommended project-specific direction (a proposal, not deployed infrastructure):

{note['production']}

{category['deployment']}

Use an authenticated entry boundary and a request/job ID. Persist required state outside application processes. Inject secrets at runtime, cap input size and external-call deadlines, and emit structured stage timings without copying private source content into logs. Run containers as an unprivileged user and use immutable, reviewed dependency/model artifacts.

For a small personal deployment, prefer the fewest processes that preserve these boundaries. For a shared deployment, add tenant authorization, job quotas, backups and tested restore. For GPU work, measure model load time, peak memory, batching and utilization before choosing instance capacity. Do not put long GPU training or document ingestion inside an unbounded web request.

## Deployment tradeoffs

{category['tradeoff']}

Estimate cost per successful task as model/API usage + embedding/parsing/media usage + compute/storage + failed/retried work. Include idle GPU time when comparing hosted and local inference. Report p50/p95 under representative concurrency and include cold-start behavior; a tutorial's isolated timing is not a service-level objective.

## Release and rollback evidence

- Establish a versioned evaluation set, baseline and explicit task-specific quality threshold.
- Verify malformed inputs, authorization failures, timeouts, restart recovery and repeated delivery.
- Resolve and audit a locked dependency set in the project's own environment; test its model/provider contract.
- Package application, prompt/tool/schema versions and model/index versions together in a release manifest.
- Canary a small workload; compare error rate, task success, latency and cost against the baseline.
- Keep the previous model/index/configuration available. Test restoring required state, not only restarting a process.

See [collection deployment playbook](../docs/DEPLOYMENT_PLAYBOOK.md) and [official reference links](../docs/SOURCES.md). Live inference, training and deployment remain unverified until you produce that evidence.
'''
    write(root / 'LEARNINGS.md', learning)
    evaluation = f'''# Evaluation protocol: {project['id']}

## Hypothesis

{note['experiment']}

## Dataset and cases

Create a small versioned development set and a separate holdout. Include successful inputs, unanswerable/unsupported requests, malformed inputs, conflicting evidence, cross-user boundaries where relevant, and a simulated dependency timeout. Keep original documents, media timestamps, graph facts or executable expected results as ground truth.

## Metrics

{category['metrics']}

The collection's `tools.evaluate` helper computes exact answer match, retrieval recall/MRR, abstention accuracy and latency/cost summaries from observations you supply. It does not call a model, grade prose semantically or manufacture results. Use task-specific metrics in addition: executable tests for code, field-level matching for extraction, WER/diarization for audio, and held-out accuracy/AP for training.

## Run record

For every case record: case ID, dataset version, source revision, model/provider revision, prompt/tool settings, expected evidence/outcome, actual evidence/outcome, elapsed milliseconds and cost if known. Keep missing metrics missing; never treat absent labels as a perfect score.

Use `python -m tools.evaluate --input observations.jsonl` from the collection root. See [metric format](../docs/EVALUATION_FORMAT.md).

## Passing decision

Choose quality and cost/latency limits before observing the candidate results. Compare with a frozen baseline, inspect the worst failures and test repeated runs for nondeterministic output. Judge-based grading should be blinded and calibrated on an independently reviewed anchor set. Syntax/integrity checks establish source health only; they do not pass this quality evaluation.

Status at import: no live model observations, no GPU training result and no production benchmark reproduced.
'''
    write(root / 'EVALUATION.md', evaluation)
    write(root / 'project.json', json.dumps(project, indent=2, ensure_ascii=False))


def main():
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    with (ROOT / 'tools/project_notes.psv').open(encoding='utf-8') as stream:
        notes = {r['id']: r for r in csv.DictReader(stream, delimiter='|')}
    categories = json.loads((ROOT / 'tools/category_notes.json').read_text(encoding='utf-8'))
    expected = {p['id'] for p in catalog['projects']}
    if expected != set(notes):
        raise SystemExit('Project notes and catalog IDs disagree')
    for project in catalog['projects']:
        note = notes[project['id']]
        project_docs(project, note, categories[note['category']])
    write(ROOT / 'catalog.json', json.dumps(catalog, indent=2, ensure_ascii=False))
    rows = [(link(p['id'] + '/README.md'), p['category'], p['purpose'], len(p['files'])) for p in catalog['projects']]
    write(ROOT / 'PROJECT_INDEX.md', '# AI project index\n\n' +
          f'102 included projects from upstream `{catalog["revision"]}`. Start with a README, then the reverse-engineering guide, learning guide and evaluation protocol. Runtime/provider compatibility is unverified.\n\n' +
          table(['Project', 'Area', 'Learning objective', 'Source files'], rows))
    inventory = table(['Upstream path', 'Disposition', 'Reason', 'README-listed'],
                      [(r['path'], r['status'], r['reason'], r['listed_in_readme']) for r in catalog['inventory']])
    write(ROOT / 'docs/INVENTORY.md', '# Upstream reconciliation\n\n' +
          'Every top-level directory and every README project link is accounted for. Tree-only projects are included when relevant. The two missing links are not replaced with invented upstream implementations.\n\n' + inventory)
    change_rows = [(p['id'], f['path'], change) for p in catalog['projects'] for f in p['files'] + p.get('local_additions', []) for change in f['changes']]
    write(ROOT / 'docs/CHANGES.md', '# Recorded source transformations\n\n' +
          'Original and local SHA-256 hashes are in each project.json. Shared documentation/tooling additions apply to every included project.\n\n' +
          table(['Project', 'File', 'Change'], change_rows))
    print(f'Wrote guides and manifests for {len(catalog["projects"])} projects.')


if __name__ == '__main__':
    main()
