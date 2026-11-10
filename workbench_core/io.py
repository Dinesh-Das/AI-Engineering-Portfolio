import json
import math
import os
import tempfile
from pathlib import Path


def read_json(path, max_bytes=8 * 1024 * 1024):
    with Path(path).open("rb") as stream:
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError("JSON input exceeds its byte budget")

    def invalid(value):
        raise ValueError("Nonfinite JSON numbers are not accepted")

    def finite(value):
        result = float(value)
        if not math.isfinite(result):
            return invalid(value)
        return result

    return json.loads(raw, parse_constant=invalid, parse_float=finite)


def write_json(path, value, max_bytes=8 * 1024 * 1024):
    """Replace one explicitly selected output atomically; never leave partial JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if len(data.encode("utf-8")) > max_bytes:
        raise ValueError("JSON output exceeds its byte budget; segment the data before persisting")
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()
