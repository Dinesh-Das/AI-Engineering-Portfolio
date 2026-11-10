"""Credential-free catalog checks and explicit, bounded headless execution.

Run from the collection root: python -m tools.hub --help
"""

import argparse
import json
import subprocess
import sys
import shutil
from pathlib import Path

from .analysis import digest, source_path
from .learning_contract import validate_learning

ROOT = Path(__file__).resolve().parents[1]


def get_project(catalog: dict, project_id: str) -> dict:
    for project in catalog['projects']:
        if project['id'] == project_id:
            return project
    raise ValueError(f'Unknown project: {project_id}')


def build_command(root: Path, project: dict, entry: str) -> list[str]:
    registered = next((e for e in project['entries'] if e['path'] == entry), None)
    if not registered or registered['ui']:
        raise ValueError('Select a registered headless entry from the project metadata')
    path = source_path(root, entry)
    if not path.is_file():
        raise ValueError('Entry does not exist')
    if registered['kind'] == 'python' and path.suffix == '.py':
        return [sys.executable, str(path)]
    if registered['kind'] == 'notebook' and path.suffix == '.ipynb':
        return [sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                '--ExecutePreprocessor.allow_errors=False', '--ExecutePreprocessor.force_raise_errors=True',
                '--ExecutePreprocessor.store_widget_state=False', '--ExecutePreprocessor.timeout=120',
                '--output-dir', str(root / 'outputs'), str(path)]
    raise ValueError('Unsupported entry type')


def check_project(root: Path, project: dict) -> list[str]:
    errors = []
    for name in ('README.md', 'REVERSE_ENGINEERING.md', 'LEARNINGS.md', 'LEARNING_JOURNAL.md', 'project.json', 'UPSTREAM_LICENSE'):
        if not (root / name).is_file():
            errors.append(f'Missing {name}')
    for record in project['files'] + project.get('local_additions', []):
        path = source_path(root, record['path'])
        if not path.is_file():
            errors.append(f'Missing source: {record["path"]}')
        elif digest(path.read_bytes()) != record['local_sha256']:
            errors.append(f'Source changed since import: {record["path"]}')
        if path.suffix == '.ipynb' and path.is_file():
            notebook = json.loads(path.read_text(encoding='utf-8-sig'))
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code' and (cell.get('outputs') or cell.get('execution_count') is not None):
                    errors.append(f'Saved notebook execution data: {record["path"]}')
    learning = root / 'LEARNINGS.md'
    if learning.is_file():
        errors.extend(validate_learning(learning.read_text(encoding='utf-8')))
    return errors


def build_ui_command(root, project, entry):
    registered = next((e for e in project.get('ui_entries', []) if e['path'] == entry), None)
    if registered is None:
        raise ValueError('Select a registered UI entry from project.json')
    path = source_path(root, entry)
    if not path.is_file():
        raise ValueError('UI entry does not exist')
    kind = registered['kind']
    if kind == 'learning-ui':
        return [sys.executable, str(path)], root
    if kind == 'streamlit':
        return [sys.executable, '-m', 'streamlit', 'run', str(path), '--server.address', '127.0.0.1'], root
    if kind == 'chainlit':
        return [sys.executable, '-m', 'chainlit', 'run', str(path), '--host', '127.0.0.1'], root
    if kind == 'npm' and registered.get('script') in {'dev', 'start'}:
        executable = shutil.which('npm.cmd') or shutil.which('npm')
        if not executable:
            raise ValueError('npm is unavailable')
        return [executable, 'run', registered['script']], path.parent
    raise ValueError('Unsupported UI entry kind')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('list', 'show', 'check', 'run', 'ui'))
    parser.add_argument('--project')
    parser.add_argument('--entry', help='Exact inventoried relative entry path')
    parser.add_argument('--execute', action='store_true', help='Actually execute source; may make paid API calls')
    parser.add_argument('--timeout', type=int, default=120, help='Whole-process deadline in seconds (1–3600)')
    parser.add_argument('--entry-args', nargs=argparse.REMAINDER, default=[], help='Arguments passed to a Python entry; place last')
    args = parser.parse_args(argv)
    try:
        catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
        projects = [get_project(catalog, args.project)] if args.project else catalog['projects']
        if args.action in {'show', 'run', 'ui'} and not args.project:
            raise ValueError('--project is required')
        if args.action == 'list':
            for project in projects:
                print(f'{project["id"]:52} {project["category"]}')
        elif args.action == 'show':
            print(json.dumps(projects[0], indent=2, ensure_ascii=True))
        elif args.action == 'check':
            failures = 0
            for project in projects:
                errors = check_project(source_path(ROOT, project['id']), project)
                failures += len(errors)
                for error in errors:
                    print(f'{project["id"]}: {error}')
            print(f'Checked {len(projects)} projects; {failures} integrity/documentation failures.')
            return int(bool(failures))
        else:
            if args.action == 'ui' and not args.entry:
                args.entry = projects[0].get('learning_ui', {}).get('entry')
            if not args.entry:
                raise ValueError('--entry is required; inspect project.json for available candidates')
            if not 1 <= args.timeout <= 3600:
                raise ValueError('--timeout must be between 1 and 3600 seconds')
            root = source_path(ROOT, projects[0]['id'])
            command, cwd = (build_ui_command(root, projects[0], args.entry) if args.action == 'ui'
                            else (build_command(root, projects[0], args.entry), root))
            if args.entry_args:
                if not args.entry.endswith('.py'):
                    raise ValueError('--entry-args is supported only for Python script entries')
                command += args.entry_args
            print(json.dumps({'cwd': str(cwd), 'command': command, 'execute': args.execute}, indent=2), flush=True)
            if args.execute:
                # No shell expansion; subprocess.run kills and waits for the direct child on timeout.
                # Descendant jobs/GPU processes require a worker/container boundary in production.
                return subprocess.run(command, cwd=cwd, timeout=args.timeout, check=False).returncode
        return 0
    except (ValueError, OSError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
