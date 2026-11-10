"""Add the newly authorized UI source, preserving existing source and local OCR work."""

import json
import re
import subprocess
from pathlib import Path

from .analysis import analyze_project, digest, source_path
from .import_collection import ROOT, UI, REPOSITORY, skip_reason, transform_file

LOCAL_OCR = {'LaTeX-OCR-with-Llama': 'Latex-OCR-Lama', 'gemma3-ocr': 'gemma3-ocr',
             'llama-ocr': 'llama-ocr', 'qwen-2.5VL-ocr': 'qwen-2.5VL-ocr'}


def import_file(source, destination, relative):
    raw = source_path(source, relative).read_bytes()
    local, target, changes = transform_file(raw, Path(relative))
    if relative == '.env.example':
        target = 'UPSTREAM_ENV.example'
        changes.append('Reference template renamed; local .env.example contains empty values.')
    output = source_path(destination, target)
    if output.exists():
        raise ValueError('Refusing to overwrite existing file: ' + str(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(local)
    return {'upstream_path': relative, 'path': target, 'upstream_sha256': digest(raw),
            'local_sha256': digest(local), 'changes': changes}


def main():
    source = ROOT / '.source/ai-engineering-hub'
    catalog_path = ROOT / 'catalog.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != catalog['revision']:
        raise ValueError('Source revision differs from the pinned catalog')
    for project in catalog['projects']:
        for record in project['files'] + project.get('local_additions', []):
            path = ROOT / project['id'] / record['path']
            if digest(path.read_bytes()) != record['local_sha256']:
                raise ValueError('Existing source changed; review before extending: ' + str(path))
    existing = {p['id'] for p in catalog['projects']}
    added = []
    restored = 0
    for name in sorted(UI - existing):
        origin = source / name
        destination = ROOT / name
        if destination.exists():
            raise ValueError('New project destination already exists: ' + str(destination))
        destination.mkdir()
        records, omitted = [], []
        for path in sorted(origin.rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(origin)
            reason = skip_reason(relative)
            if reason:
                omitted.append({'path': relative.as_posix(), 'reason': reason})
            else:
                records.append(import_file(origin, destination, relative.as_posix()))
        (destination / 'UPSTREAM_LICENSE').write_bytes((source / 'LICENSE').read_bytes())
        report = analyze_project(destination, [r['path'] for r in records])
        reference = destination / 'UPSTREAM_ENV.example'
        if reference.exists():
            report['environment'] = sorted(set(report['environment']) | set(re.findall(
                r'^([A-Z][A-Z0-9_]+)\s*=', reference.read_text(encoding='utf-8'), re.M)))
        project = {'id': name, 'upstream_revision': revision,
                   'source_url': f'{REPOSITORY}/tree/{revision}/' + name.replace(' ', '%20'),
                   'entries': report['entries'], 'files': records, 'omitted': omitted, 'analysis': report,
                   'validation': {'source_inspection': True, 'live_models': False,
                                  'dependencies_installed': False, 'deployed': False}}
        catalog['projects'].append(project)
        added.append(name)
    for project in catalog['projects']:
        destination = ROOT / project['id']
        remaining = []
        for omission in project['omitted']:
            relative = Path(omission['path'])
            reason = skip_reason(relative)
            if reason is None:
                record = import_file(source / project['id'], destination, relative.as_posix())
                record['changes'].append('Restored frontend source/asset after UI scope was authorized.')
                project['files'].append(record)
                restored += 1
            else:
                remaining.append({'path': omission['path'], 'reason': reason})
        project['omitted'] = remaining
    for row in catalog['inventory']:
        if row['path'] in UI:
            row.update(status='included', reason='UI category authorized in the user follow-up; learning remains required.')
        if row['path'] in LOCAL_OCR and (ROOT / LOCAL_OCR[row['path']]).is_dir():
            row.update(status='completed-local', local_path=LOCAL_OCR[row['path']],
                       reason='Completed OCR work moved here by the user; existing source and learning material preserved.')
    catalog['projects'].sort(key=lambda p: p['id'].lower())
    catalog['learning_required'] = True
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'added_projects': added, 'restored_files': restored, 'catalog_projects': len(catalog['projects'])}, indent=2))


if __name__ == '__main__':
    main()
