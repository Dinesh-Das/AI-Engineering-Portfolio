"""Execute every registered project's CPU scenarios in bounded child processes."""

import argparse
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

from workbench_core.io import read_json, write_json

ROOT = Path(__file__).resolve().parents[1]


def fingerprint(root=ROOT):
    registry = read_json(root / "enhancements.json")
    paths = ["enhancements.json", "tools/run_enhancements.py"]
    paths.extend(
        p.relative_to(root).as_posix() for p in sorted((root / "workbench_core").glob("*.py"))
    )
    for project in registry["projects"]:
        paths.extend(project["id"] + "/" + record["path"] for record in project["files"])
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.encode() + b"\0" + (root / path).read_bytes() + b"\0")
    return digest.hexdigest()


def run_project(project):
    root = ROOT / project["id"]
    try:
        process = subprocess.run(
            [sys.executable, str(root / "enhance.py"), "check"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        if not process.stdout.strip():
            raise ValueError("Project produced no report: " + process.stderr[:2000])
        result = json.loads(process.stdout)
        if process.returncode or result.get("project") != project["id"] or not result.get("passed"):
            return {
                "id": project["id"],
                "passed": False,
                "result": result,
                "stderr": process.stderr[:2000],
            }
        doctor = subprocess.run(
            [sys.executable, str(root / "enhance.py"), "doctor"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        if doctor.returncode:
            raise ValueError("Environment diagnostics failed: " + doctor.stderr[:2000])
        return {
            "id": project["id"],
            "family": project["family"],
            "local_ocr": project["local_ocr"],
            "passed": True,
            "result": result,
            "doctor": json.loads(doctor.stdout),
        }
    except (subprocess.TimeoutExpired, OSError, ValueError) as error:
        return {"id": project["id"], "passed": False, "error": str(error)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", help="Run one registered project; no argument runs all 113")
    args = parser.parse_args(argv)
    registry = read_json(ROOT / "enhancements.json")
    projects = [p for p in registry["projects"] if not args.project or p["id"] == args.project]
    if not projects:
        parser.error("Unknown project")
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_project, projects))
    failures = [p["id"] for p in results if not p["passed"]]
    total = sum(len(p.get("result", {}).get("checks", [])) for p in results)
    report = {
        "schema_version": 1,
        "runtime_sha256": fingerprint(),
        "projects_checked": len(results),
        "scenario_checks": total,
        "failures": failures,
        "live_model_executed": False,
        "original_application_verified": False,
        "gpu_training": False,
        "container_built": False,
        "production_deployed": False,
        "projects": results,
    }
    if not args.project:
        write_json(ROOT / "docs/enhancement-validation.json", report)
        rows = ["| Project | Extension | Passed checks |", "| --- | --- | --- |"]
        for p in results:
            checks = p.get("result", {}).get("checks", [])
            rows.append(
                f"| [{p['id']}](../{quote(p['id'])}/ENHANCEMENTS.md) | {p.get('family', 'failed')} | {sum(c['passed'] for c in checks)}/{len(checks)} |"
            )
        text = (
            "# Executed enhancement coverage\n\n"
            f"{len(results)} project launchers executed; {total} deterministic CPU scenarios. Failures: {len(failures)}. "
            "Each launcher also ran read-only environment diagnostics in the collection interpreter. "
            "Missing original SDKs are reported as missing; presence does not establish compatible versions.\n\n"
            "The [machine-readable evidence](enhancement-validation.json) includes every case and a source fingerprint. "
            "These scenarios exercise actual shared algorithms on labeled synthetic inputs. "
            "They do not call original model integrations, train a model, build containers or deploy services. "
            "See [native OCR verification](OCR_ENHANCEMENT_VALIDATION.md) for the separate application suites, "
            "and [UI validation](UI_VALIDATION.md) for the existing browser checks.\n\n"
            + "\n".join(rows)
            + "\n"
        )
        (ROOT / "docs/ENHANCEMENT_REPORT.md").write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in report.items() if k != "projects"}, indent=2))
    for result in results:
        if not result["passed"]:
            print(json.dumps(result, indent=2))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
