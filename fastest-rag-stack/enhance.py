"""Run this project's executable learning extension from the collection checkout."""

import importlib
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent
    collection_root = project_root.parent
    if not (collection_root / "workbench_core" / "cli.py").is_file():
        raise SystemExit("Keep this folder beside workbench_core in the AI Projects checkout.")
    sys.path.insert(0, str(collection_root))
    return importlib.import_module("workbench_core.cli").main(project_root=project_root)


if __name__ == "__main__":
    raise SystemExit(main())
