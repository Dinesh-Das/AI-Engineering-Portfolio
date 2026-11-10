"""Bundle the reviewed runtime into seven independent learning-project folders."""

import json
from pathlib import Path

from .analysis import digest
from .hub import ROOT


def main():
    catalog_path = ROOT / 'catalog.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    profiles = json.loads((ROOT / 'tools/ui_profiles.json').read_text(encoding='utf-8'))
    template = ROOT / 'tools/chat_lab'
    runtime_files = [p for p in template.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    for project in catalog['projects']:
        if project['id'] not in profiles:
            continue
        profile = {'id': project['id'], **profiles[project['id']]}
        content = {'learning_ui/' + path.relative_to(template).as_posix(): path.read_bytes() for path in runtime_files}
        content['lab.json'] = (json.dumps(profile, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
        content['learning_app.py'] = ("from pathlib import Path\nfrom learning_ui.server import main\n\n"
                                      "if __name__ == '__main__':\n    main(Path(__file__).with_name('lab.json'))\n").encode()
        additions = {record['path']: record for record in project.get('local_additions', [])}
        for relative, raw in content.items():
            path = ROOT / project['id'] / relative
            if path.exists():
                previous = additions.get(relative)
                if previous is None or digest(path.read_bytes()) != previous['local_sha256']:
                    raise ValueError('Refusing to replace unrecorded/user-edited UI source: ' + str(path))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            additions[relative] = {'path': relative, 'local_sha256': digest(raw),
                                   'changes': ['Added an independently runnable learning UI: bounded local transport, incremental streams and project-specific experiments.']}
        project['local_additions'] = list(additions.values())
        project['learning_ui'] = {'entry': 'learning_app.py', 'profile': 'lab.json', 'runtime': 'python-stdlib',
                                  'fixture_supported': True, 'live_inference_verified': False}
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(f'Bundled {len(profiles)} independent learning interfaces.')


if __name__ == '__main__':
    main()
