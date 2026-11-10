"""Validate artifact completeness and provenance before consuming a pipeline output."""

import hashlib
from pathlib import Path, PureWindowsPath


def manifest(root, records):
    root = Path(root).resolve(strict=True)
    if not isinstance(records, list) or not 1 <= len(records) <= 1000:
        raise ValueError("Expected 1–1000 artifact records")
    result, identifiers, total = [], set(), 0
    for record in records:
        if (
            not isinstance(record, dict)
            or not isinstance(record.get("id"), str)
            or not record["id"]
        ):
            raise ValueError("Every artifact needs an ID")
        if record["id"] in identifiers:
            raise ValueError("Duplicate artifact ID")
        identifiers.add(record["id"])
        relative = record.get("path")
        if (
            not isinstance(relative, str)
            or not relative
            or Path(relative).is_absolute()
            or PureWindowsPath(relative).drive
            or ".." in relative.replace("\\", "/").split("/")
        ):
            raise ValueError("Artifact path must stay within its declared root")
        path = (root / relative).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("Artifact escapes the declared root or is not a file")
        size = path.stat().st_size
        total += size
        if not 0 < size <= 64 * 1024 * 1024 or total > 128 * 1024 * 1024:
            raise ValueError("Artifact byte budget exceeded or artifact is empty")
        with path.open("rb") as stream:
            checksum = hashlib.file_digest(stream, "sha256").hexdigest()
        if record.get("sha256") and checksum != record["sha256"]:
            raise ValueError("Artifact checksum mismatch")
        result.append({"id": record["id"], "path": relative, "bytes": size, "sha256": checksum})
    return {
        "artifacts": result,
        "total_bytes": total,
        "complete": True,
        "scope": "declared artifacts only; no media decoding or model quality was validated",
    }
