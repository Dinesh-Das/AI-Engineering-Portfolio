"""Import a pinned, locally cloned MIT source tree. Does not run project code.

Initial import only. Refuses to overwrite an existing project directory.
"""

import argparse
import ast
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

from .analysis import analyze_project, code_cells, digest, python_cell, sanitize_notebook
from .transform import harden_http, redact_literals

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/patchy631/ai-engineering-hub'
OCR = {'LaTeX-OCR-with-Llama', 'llama-ocr', 'gemma3-ocr', 'qwen-2.5VL-ocr'}
UI = {'local-chatgpt', 'local-chatgpt with DeepSeek', 'local-chatgpt with Gemma 3',
      'deepseek-thinking-ui', 'qwen3-thinking-ui', 'gpt-oss-thinking-ui', 'streaming-ai-chatbot'}
RESOURCE = {'assets', 'resources', 'courses', 'ai-engineering-roadmap'}
SKIP_PARTS = {'frontend', 'node_modules', 'public', 'components', 'hooks', 'styles',
              '__pycache__', '.github', '.streamlit', '.chainlit', '.vscode', 'dist', '.next'}
TEXT_SUFFIXES = {'.py', '.ts', '.js', '.json', '.jsonl', '.yaml', '.yml', '.toml', '.txt',
                 '.md', '.sh', '.sql', '.gq', '.pg', '.html', '.css', '.lock', '.csv'}


def disposition(name):
    if name in OCR:
        return 'excluded-ocr', 'User already completed OCR projects.'
    if name in UI:
        return 'excluded-ui', 'Upstream Chat Interfaces & UI category; excluded by user request.'
    if name in RESOURCE:
        return 'excluded-resource', 'General learning material or shared promotional assets, not an AI project.'
    return 'included', 'AI algorithm, workflow, backend, model evaluation or infrastructure learning project.'


def skip_reason(relative: Path):
    if any(part in SKIP_PARTS for part in relative.parts[:-1]):
        return 'Frontend, generated output or development automation omitted.'
    if relative.suffix.lower() in {'.mp4', '.gif', '.webm', '.tsx', '.css'}:
        return 'Demo media or presentation-only source omitted.'
    if relative.name in {'.env', '.env.local', '.env.production'}:
        return 'Actual environment file omitted.'
    if relative.suffix in {'.tsbuildinfo', '.pyc'}:
        return 'Generated build cache omitted.'
    if relative.as_posix().startswith('src/ui/'):
        return 'UI subtree omitted; AI services remain.'
    if relative.parts[0] == 'assets':
        return 'Screenshots and promotional assets omitted.'
    if relative.as_posix().startswith('app/') and not relative.as_posix().startswith('app/api/'):
        return 'Next.js presentation routes omitted; backend API routes remain.'
    return None


def transform_file(raw: bytes, relative: Path):
    changes = []
    target = relative.as_posix()
    if relative.name in {'AGENTS.md', 'CLAUDE.md'}:
        target = relative.with_name(relative.stem + '.upstream.md').as_posix()
        changes.append('Quarantined imported agent instructions as reference documentation.')
    if relative.as_posix() == 'README.md':
        target = 'UPSTREAM_README.md'
        changes.append('Preserved upstream README separately from the local learning guide.')
    if relative.suffix == '.ipynb':
        try:
            notebook = json.loads(raw.decode('utf-8-sig'))
        except json.JSONDecodeError:
            return raw, target + '.invalid.txt', ['Empty/invalid upstream notebook quarantined; no executable lesson was present.']
        notebook = sanitize_notebook(notebook)
        changes.append('Cleared notebook outputs, execution counters, execution metadata and saved widgets.')
        fixes = 0
        redactions = 0
        for index, cell in enumerate(notebook.get('cells', []), 1):
            source = cell.get('source', '')
            source = ''.join(source) if isinstance(source, list) else source
            source, count = redact_literals(source)
            redactions += count
            if cell.get('cell_type') == 'code':
                if relative.as_posix() == 'notebook.ipynb' and source.strip() == 'ai_stream_msgs[7])':
                    source = source.replace('ai_stream_msgs[7])', 'ai_stream_msgs[7]')
                    changes.append(f'Fixed unmatched closing parenthesis in notebook cell {index}.')
                # Whole-cell syntax must be ordinary Python for a safe source rewrite.
                source, count = harden_http(source)
                fixes += count
            cell['source'] = source.splitlines(keepends=True)
        if fixes:
            changes.append(f'Added explicit connection/read timeouts to {fixes} requests calls in notebook cells.')
        if redactions:
            changes.append(f'Redacted {redactions} possible credential literals (values not retained).')
        return (json.dumps(notebook, indent=1, ensure_ascii=False) + '\n').encode('utf-8'), target, changes
    if relative.suffix.lower() in TEXT_SUFFIXES or relative.name.startswith('.env'):
        text = raw.decode('utf-8-sig', errors='strict')
        text, count = redact_literals(text)
        if count:
            changes.append(f'Redacted {count} possible credential literals (values not retained).')
        if relative.suffix == '.py' and not re.search(r'\b(?:import|from)\s+(streamlit|chainlit|gradio)\b', text):
            text, count = harden_http(text)
            if count:
                changes.append(f'Added explicit connection/read timeouts to {count} direct requests calls.')
        elif relative.suffix == '.py':
            try:
                ast.parse(text)
            except SyntaxError:
                target = 'reference/ui/' + relative.name + '.invalid.txt'
                changes.append('Quarantined malformed upstream UI script; AI modules remain available without that wrapper.')
        return text.encode('utf-8'), target, changes
    return raw, target, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / '.source' / 'ai-engineering-hub')
    args = parser.parse_args()
    source = args.source.resolve()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    source_readme = (source / 'README.md').read_text(encoding='utf-8')
    links = set(unquote(p) for p in re.findall(r'\]\(\./([^\)#]+)\)', source_readme))
    folders = sorted(p.name for p in source.iterdir() if p.is_dir() and not p.name.startswith('.'))
    inventory = []
    included = [name for name in folders if disposition(name)[0] == 'included']
    conflicts = [name for name in included if (ROOT / name).exists()]
    if conflicts:
        raise SystemExit('Refusing to overwrite existing projects: ' + ', '.join(conflicts))
    projects = []
    for name in folders:
        status, reason = disposition(name)
        inventory.append({'path': name, 'status': status, 'reason': reason, 'listed_in_readme': name in links})
        if status != 'included':
            continue
        origin = source / name
        destination = ROOT / name
        destination.mkdir()
        records, omitted = [], []
        for path in sorted(origin.rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(origin)
            reason = skip_reason(relative)
            if reason:
                omitted.append({'path': relative.as_posix(), 'reason': reason})
                continue
            raw = path.read_bytes()
            try:
                local, target, changes = transform_file(raw, relative)
            except UnicodeDecodeError:
                local, target, changes = raw, relative.as_posix(), []
            # The local environment template is generated later, with no imported values.
            if relative.as_posix() == '.env.example':
                target = 'UPSTREAM_ENV.example'
                changes.append('Reference template renamed; local .env.example contains empty values.')
            output = destination / target
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(local)
            records.append({'upstream_path': relative.as_posix(), 'path': target,
                            'upstream_sha256': digest(raw), 'local_sha256': digest(local), 'changes': changes})
        (destination / 'UPSTREAM_LICENSE').write_bytes((source / 'LICENSE').read_bytes())
        report = analyze_project(destination, [record['path'] for record in records])
        # Capture names from the renamed reference env template as well.
        env_reference = destination / 'UPSTREAM_ENV.example'
        if env_reference.exists():
            report['environment'] = sorted(set(report['environment']) | set(re.findall(
                r'^([A-Z][A-Z0-9_]+)\s*=', env_reference.read_text(encoding='utf-8'), re.M)))
        project = {'id': name, 'upstream_revision': revision,
                   'source_url': f'{REPOSITORY}/tree/{revision}/' + name.replace(' ', '%20'),
                   'entries': report['entries'], 'files': records, 'omitted': omitted,
                   'analysis': report, 'validation': {'source_inspection': True, 'live_models': False,
                    'dependencies_installed': False, 'deployed': False}}
        (destination / 'analysis.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        projects.append(project)
    for link in sorted(links - set(folders)):
        inventory.append({'path': link, 'status': 'missing-upstream',
                          'reason': 'README link has no source directory at the pinned revision.', 'listed_in_readme': True})
    catalog = {'repository': REPOSITORY, 'revision': revision, 'date': '2026-11-10',
               'projects': projects, 'inventory': inventory}
    (ROOT / 'catalog.json').write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'revision': revision, 'projects': len(projects), 'inventory_entries': len(inventory),
                      'source_files': sum(len(p['files']) for p in projects)}, indent=2))


if __name__ == '__main__':
    main()
