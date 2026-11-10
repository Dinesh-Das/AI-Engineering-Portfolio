"""Small, testable source transformations; do not execute imported code."""

import ast
import re

from .analysis import name_of


def harden_http(source: str) -> tuple[str, int]:
    """Bound direct requests calls; preserve source and existing timeout policy."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source, 0
    aliases = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module == 'requests':
            for alias in node.names:
                aliases[alias.asname or alias.name] = 'requests.' + alias.name
    raw = source.encode('utf-8')
    lines = raw.splitlines(keepends=True)
    starts, offset = [], 0
    for line in lines:
        starts.append(offset)
        offset += len(line)
    edits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call = name_of(node.func)
        first, _, tail = call.partition('.')
        canonical = aliases.get(first, first) + ('.' + tail if tail else '')
        if canonical not in {'requests.' + method for method in ('get', 'post', 'put', 'patch', 'delete', 'request', 'head', 'options')}:
            continue
        if any(k.arg in {'timeout', None} for k in node.keywords):
            continue
        position = starts[node.end_lineno - 1] + node.end_col_offset - 1
        prefix = raw[:position].rstrip()
        separator = b'' if prefix.endswith((b'(', b',')) else b', '
        edits.append((position, separator + b'timeout=(10, 60)'))
    for position, insertion in sorted(edits, reverse=True):
        raw = raw[:position] + insertion + raw[position:]
    result = raw.decode('utf-8')
    ast.parse(result)  # A transformation must never introduce a syntax error.
    return result, len(edits)


def redact_literals(text: str) -> tuple[str, int]:
    """Remove recognizable credential shapes; this is not an exhaustive secret scanner."""
    count = 0

    def redact(match):
        nonlocal count
        count += 1
        return 'REDACTED_SET_ENVIRONMENT'

    patterns = (
        r'\bsk-(?:proj-|or-v1-)?[A-Za-z0-9_-]{24,}',
        r'\bhf_[A-Za-z0-9]{25,}',
        r'\bgh[pousr]_[A-Za-z0-9]{30,}',
        r'\bAIza[A-Za-z0-9_-]{30,}',
        r'\bxai-[A-Za-z0-9]{30,}',
    )
    for pattern in patterns:
        text = re.sub(pattern, redact, text)
    # Literal environment assignments, as opposed to env lookups and placeholders.
    assignment = re.compile(r'\b([A-Z][A-Z0-9_]*(?:API_KEY|SECRET|PASSWORD|ACCESS_TOKEN))\s*=\s*([\'"])([^\'"\n]{12,})\2')

    def redact_assignment(match):
        nonlocal count
        value = match.group(3)
        if any(term in value.lower() for term in ('your', 'placeholder', 'example', 'getenv', 'environ', 'redacted')):
            return match.group(0)
        count += 1
        return match.group(1) + '=' + match.group(2) + 'REDACTED_SET_ENVIRONMENT' + match.group(2)

    text = assignment.sub(redact_assignment, text)
    dictionary = re.compile(r'''(["'](?:api_?key|access_?token|api_?token|password|secret)["']\s*:\s*)(["'])([^"'\n]{12,})\2''', re.I)

    def redact_dictionary(match):
        nonlocal count
        value = match.group(3)
        if value.upper() == value or any(term in value.lower() for term in ('your', 'placeholder', 'example', 'redacted', 'getenv', 'environ', '${', '...')):
            return match.group(0)
        count += 1
        return match.group(1) + match.group(2) + 'REDACTED_SET_ENVIRONMENT' + match.group(2)

    text = dictionary.sub(redact_dictionary, text)
    return text, count
