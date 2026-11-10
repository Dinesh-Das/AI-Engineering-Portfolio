"""Inspect source without importing it. Findings are review leads, not a security audit."""

import ast
import copy
import hashlib
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath

UI_MODULES = {'streamlit', 'chainlit', 'gradio', 'mesop', 'reflex'}


def source_path(root: Path, relative: str) -> Path:
    """Resolve only project-relative paths, including across Windows/POSIX callers."""
    if not relative or PurePosixPath(relative).is_absolute() or PureWindowsPath(relative).drive:
        raise ValueError('Expected a project-relative path')
    parts = relative.replace('\\', '/').split('/')
    if any(part in {'..', ''} for part in parts):
        raise ValueError('Path contains an invalid segment')
    resolved = root.joinpath(*parts).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError('Path escapes the project directory')
    return resolved


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sanitize_notebook(notebook: dict) -> dict:
    """Preserve lessons and code, clear execution data and saved widget state."""
    clean = copy.deepcopy(notebook)
    clean.setdefault('metadata', {}).pop('widgets', None)
    for cell in clean.get('cells', []):
        metadata = cell.setdefault('metadata', {})
        for key in ('execution', 'ExecuteTime', 'collapsed', 'scrolled'):
            metadata.pop(key, None)
        if cell.get('cell_type') == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
    return clean


def code_cells(notebook: dict):
    for index, cell in enumerate(notebook.get('cells', []), 1):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', '')
            yield index, ''.join(source) if isinstance(source, list) else source


def python_cell(source: str) -> tuple[str, bool]:
    """Magics are recorded rather than misreported as Python syntax errors."""
    if source.lstrip().startswith('%%'):
        return '', True
    special = False
    lines = []
    continuation = False
    for line in source.splitlines():
        if continuation:
            continuation = line.rstrip().endswith('\\')
            lines.append('')
            continue
        if line.lstrip().startswith(('%', '!')):
            indent = line[:len(line) - len(line.lstrip())]
            lines.append(indent + 'pass # notebook magic omitted for syntax inspection')
            special = True
            continuation = line.rstrip().endswith('\\')
        else:
            lines.append(line)
    return '\n'.join(lines), special


def name_of(node) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return name_of(node.value) + '.' + node.attr
    return ''


def analyze_python(source: str, filename: str) -> dict:
    report = {'path': filename, 'imports': [], 'environment': [], 'models': [],
              'symbols': [], 'calls': [], 'findings': [], 'ui': False, 'syntax_error': None}
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as error:
        report['syntax_error'] = {'line': error.lineno, 'message': error.msg}
        return report
    imports, environment, models, calls = set(), set(), set(), set()
    aliases = {}

    def finding(rule, node, message):
        report['findings'].append({'rule': rule, 'path': filename,
                                   'line': node.lineno, 'message': message})

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
                aliases[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split('.')[0])
            for alias in node.names:
                aliases[alias.asname or alias.name] = node.module + '.' + alias.name
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node) or ''
            report['symbols'].append({'name': node.name, 'line': node.lineno,
                                       'kind': type(node).__name__, 'doc': doc.split('\n')[0][:180]})
        elif isinstance(node, ast.Subscript) and name_of(node.value) in {'os.environ', 'environ'}:
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                environment.add(node.slice.value)
        elif isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                if any(re.search(r'(?:^|_)(?:model|model_name|model_id|checkpoint)$', name_of(t), re.I) for t in node.targets):
                    models.add(node.value.value)
        elif isinstance(node, ast.Call):
            call = name_of(node.func)
            first, _, tail = call.partition('.')
            canonical = aliases.get(first, first) + ('.' + tail if tail else '')
            calls.add(call)
            if canonical in {'os.getenv', 'getenv', 'os.environ.get', 'environ.get'} and node.args:
                if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    environment.add(node.args[0].value)
            for keyword in node.keywords:
                if keyword.arg in {'model', 'model_name', 'model_id', 'base_model'}:
                    if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                        models.add(keyword.value.value)
                if keyword.arg in {'shell', 'trust_remote_code', 'allow_dangerous_deserialization', 'allow_code_execution'}:
                    if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        finding(keyword.arg, node, f'{keyword.arg}=True crosses a code-execution trust boundary.')
            if canonical in {'eval', 'exec', 'os.system', 'pickle.load', 'pickle.loads'}:
                finding('code-execution', node, f'Review inputs to {canonical}; untrusted data can execute code.')
            if canonical.startswith('requests.') and canonical.rsplit('.', 1)[-1] in {'get', 'post', 'put', 'patch', 'delete', 'request', 'head'}:
                if not any(k.arg == 'timeout' for k in node.keywords):
                    finding('network-timeout', node, 'HTTP call has no explicit timeout; a stalled peer can occupy a worker.')
    report.update(imports=sorted(imports), environment=sorted(environment),
                  models=sorted(m for m in models if len(m) < 160), calls=sorted(calls),
                  ui=bool(imports & UI_MODULES))
    return report


def analyze_project(root: Path, tracked: list[str]) -> dict:
    units, manifests, notebooks, other_code = [], [], [], []
    for relative in tracked:
        path = source_path(root, relative)
        if path.suffix == '.py':
            units.append(analyze_python(path.read_text(encoding='utf-8-sig'), relative))
        elif path.suffix == '.ipynb':
            try:
                notebook = json.loads(path.read_text(encoding='utf-8-sig'))
            except json.JSONDecodeError as error:
                unit = analyze_python('', relative)
                unit['syntax_error'] = {'line': error.lineno, 'message': 'Invalid notebook JSON: ' + error.msg}
                units.append(unit)
                continue
            notebooks.append(relative)
            for index, source in code_cells(notebook):
                cleaned, special = python_cell(source)
                unit = analyze_python(cleaned, f'{relative}#cell-{index}')
                unit['notebook_magics'] = special
                units.append(unit)
        elif path.name == 'pyproject.toml' or re.match(r'requirements.*\.txt$', path.name) or path.name == 'package.json':
            manifests.append(relative)
        elif path.suffix in {'.ts', '.js', '.tsx', '.sh', '.yaml', '.yml'}:
            other_code.append(relative)
    environment = set(e for u in units for e in u['environment'])
    # Non-Python integrations and environment templates are also part of the contract.
    for relative in tracked:
        path = source_path(root, relative)
        if path.suffix in {'.ts', '.js', '.json', '.yaml', '.yml', '.toml'} or 'env' in path.name:
            if path.stat().st_size > 2_000_000:
                continue
            content = path.read_text(encoding='utf-8-sig', errors='replace')
            environment.update(re.findall(r'process\.env\.([A-Z][A-Z0-9_]+)', content))
            environment.update(re.findall(r'\$\{([A-Z][A-Z0-9_]+)\}', content))
            if 'env' in path.name:
                environment.update(re.findall(r'^([A-Z][A-Z0-9_]+)\s*=', content, re.M))
    entries = []
    for relative in tracked:
        path = Path(relative)
        if path.suffix == '.ipynb':
            matches = [u for u in units if u['path'].startswith(relative + '#')]
            entries.append({'path': relative, 'kind': 'notebook', 'ui': any(u['ui'] for u in matches)})
        elif path.suffix == '.py' and not path.name.startswith(('test_', '__', 'setup')):
            unit = next(u for u in units if u['path'] == relative)
            source = (root / relative).read_text(encoding='utf-8-sig')
            if re.search(r'if\s+__name__\s*==', source) or path.name in {'main.py', 'server.py', 'api.py', 'app.py', 'demo.py'}:
                entries.append({'path': relative, 'kind': 'python', 'ui': unit['ui']})
    return {
        'units': units, 'manifests': manifests, 'notebooks': notebooks, 'other_code': other_code,
        'environment': sorted(e for e in environment if re.fullmatch(r'[A-Z][A-Z0-9_]+', e)),
        'imports': sorted(set(i for u in units for i in u['imports'])),
        'models': sorted(set(m for u in units for m in u['models'])), 'entries': entries,
        'findings': [f for u in units for f in u['findings']],
        'syntax_errors': [{'path': u['path'], **u['syntax_error']} for u in units if u['syntax_error']],
    }
