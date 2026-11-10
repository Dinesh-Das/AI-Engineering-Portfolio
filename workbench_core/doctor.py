"""Read-only preflight: inspect declared requirements without importing provider SDKs."""

import importlib.metadata
import os
import platform
import re
import sys
from pathlib import Path

from .io import read_json


def inspect(project_root):
    root = Path(project_root).resolve()
    config = read_json(root / "enhancement/environment.json")
    installed = {
        re.sub(r"[-_.]+", "-", d.metadata["Name"]).lower(): d.version
        for d in importlib.metadata.distributions()
        if d.metadata.get("Name")
    }
    packages = []
    for requirement in config.get("requirements", []):
        match = re.match(r"([A-Za-z0-9][A-Za-z0-9_.-]*)", requirement)
        if not match:
            continue
        name = re.sub(r"[-_.]+", "-", match.group(1)).lower()
        packages.append(
            {
                "requirement": requirement,
                "installed_version": installed.get(name),
                "present": name in installed,
                "version_compatibility_verified": False,
            }
        )
    return {
        "project": config["project_id"],
        "python": platform.python_version(),
        "interpreter": sys.executable,
        "enhancement_runtime_ready": sys.version_info >= (3, 12),
        "original_python_requirements": config.get("python_requirements", []),
        "original_dependency_presence": packages,
        "environment_names": [
            {
                "name": name,
                "set": bool(os.environ.get(name)),
                "requiredness": "inspect selected original path",
            }
            for name in config.get("environment_names", [])
        ],
        "manifests": config.get("manifests", []),
        "original_integration_ready": "not established",
        "notes": [
            "No package was imported or installed and no environment value is printed.",
            "Package presence is not version/provider/hardware compatibility.",
            "Optional environment names must not all be treated as mandatory secrets.",
        ],
    }
