"""Validate source coverage, manifests, local docs and offline syntax without SDK imports."""

import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from .analysis import analyze_project, code_cells, python_cell
from .hub import ROOT, check_project


def verify(root=ROOT):
    catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    snapshot = json.loads((root / 'docs/upstream-tree.json').read_text(encoding='utf-8'))
    errors = []
    ids = [p['id'] for p in catalog['projects']]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate project IDs')
    included = {r['path'] for r in catalog['inventory'] if r['status'] == 'included'}
    if set(ids) != included:
        errors.append('Included inventory does not match project folders')
    directories = {path.split('/')[0] for path in snapshot['paths'] if '/' in path}
    inventoried = {r['path'] for r in catalog['inventory']}
    if not directories <= inventoried:
        errors.append('Upstream tree directories missing from inventory')
    if snapshot['revision'] != catalog['revision']:
        errors.append('Source snapshot revision mismatch')
    documents = [root / p for p in ('README.md', 'PROJECT_INDEX.md', 'docs/INVENTORY.md',
                                   'docs/CHANGES.md', 'docs/LEARNING_PATH.md', 'docs/DEPLOYMENT_PLAYBOOK.md',
                                   'docs/EVALUATION_FORMAT.md', 'docs/SOURCES.md', 'docs/THIRD_PARTY_NOTICES.md')]
    python_files = notebook_cells = magic_cells = 0
    for project in catalog['projects']:
        project_root = root / project['id']
        errors.extend(project['id'] + ': ' + error for error in check_project(project_root, project))
        metadata = json.loads((project_root / 'project.json').read_text(encoding='utf-8'))
        if metadata != project:
            errors.append(project['id'] + ': project.json differs from catalog')
        original = {p[len(project['id']) + 1:] for p in snapshot['paths'] if p.startswith(project['id'] + '/')}
        accounted = {r['upstream_path'] for r in project['files']} | {r['path'] for r in project['omitted']}
        if original != accounted:
            errors.append(project['id'] + ': source import/omission map is incomplete')
        records = project['files'] + project.get('local_additions', [])
        report = analyze_project(project_root, [r['path'] for r in records])
        errors.extend(project['id'] + ': ' + str(error) for error in report['syntax_errors'])
        for record in records:
            path = project_root / record['path']
            if path.suffix == '.py':
                try:
                    compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
                    python_files += 1
                except SyntaxError as error:
                    errors.append(f'{path}: {error.msg}')
            elif path.suffix == '.ipynb':
                notebook = json.loads(path.read_text(encoding='utf-8'))
                for index, source in code_cells(notebook):
                    cleaned, magic = python_cell(source)
                    magic_cells += int(magic)
                    try:
                        compile(cleaned, f'{path}#cell-{index}', 'exec', flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
                        notebook_cells += 1
                    except SyntaxError as error:
                        errors.append(f'{path}#cell-{index}: {error.msg}')
        for line in (project_root / '.env.example').read_text(encoding='utf-8').splitlines():
            if line and not line.startswith('#') and (not re.fullmatch(r'[A-Z][A-Z0-9_]*=', line)):
                errors.append(project['id'] + ': environment template contains a nonempty/invalid value')
        documents.extend(project_root / name for name in ('README.md', 'REVERSE_ENGINEERING.md', 'LEARNINGS.md', 'EVALUATION.md'))
    for document in documents:
        if not document.is_file():
            errors.append('Missing document: ' + str(document.relative_to(root)))
            continue
        text = document.read_text(encoding='utf-8')
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text):
            if re.match(r'[a-zA-Z]+://|mailto:|#', target):
                continue
            relative = unquote(target.split('#')[0])
            if not relative:
                continue
            if not (document.parent / relative).is_file():
                errors.append(f'{document.relative_to(root)}: broken local link {target}')
    return {'projects': len(ids), 'inventory_entries': len(catalog['inventory']),
            'dispositions': dict(Counter(r['status'] for r in catalog['inventory'])),
            'python_files_compiled': python_files, 'notebook_cells_compiled': notebook_cells,
            'cells_with_ipython_syntax': magic_cells, 'documents_checked': len(documents),
            'failures': errors, 'live_model_tests': False, 'gpu_training': False, 'deployed': False}


def main():
    result = verify()
    (ROOT / 'docs/validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))
    return int(bool(result['failures']))


if __name__ == '__main__':
    raise SystemExit(main())
