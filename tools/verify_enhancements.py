"""Verify enhancement coverage, file provenance and executed source fingerprints."""

import hashlib

from workbench_core.io import read_json

from .run_enhancements import fingerprint


def verify(root, catalog):
    errors = []
    if (root / "database-memory-agent/safe_tools.py").read_bytes() != (
        root / "workbench_core/safety.py"
    ).read_bytes():
        errors.append(
            "Standalone database agent safety code differs from the tested shared implementation"
        )
    registry = read_json(root / "enhancements.json")["projects"]
    expected = {p["id"] for p in catalog["projects"]} | {
        "Latex-OCR-Lama",
        "gemma3-ocr",
        "llama-ocr",
        "qwen-2.5VL-ocr",
    }
    if len(registry) != 113 or {p["id"] for p in registry} != expected:
        errors.append("Enhancement registry must cover all 113 projects exactly once")
    for project in registry:
        directory = root / project["id"]
        profile = read_json(directory / "enhancement/profile.json")
        if profile["project_id"] != project["id"] or profile["family"] != project["family"]:
            errors.append(project["id"] + ": enhancement identity mismatch")
        for record in project["files"]:
            path = directory / record["path"]
            if (
                not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != record["local_sha256"]
            ):
                errors.append(project["id"] + ": stale/missing enhancement file " + record["path"])
        if not (directory / "LEARNING_JOURNAL.md").is_file():
            errors.append(project["id"] + ": missing personal learning journal")
    report = read_json(root / "docs/enhancement-validation.json")
    if report["runtime_sha256"] != fingerprint(root):
        errors.append("Enhancement execution evidence is stale; run .\\run.ps1 enhance")
    verified = {p["id"] for p in report["projects"] if p.get("passed")}
    if report["failures"] or verified != expected or report["projects_checked"] != 113:
        errors.append("Enhancement execution report does not pass all 113 projects")
    cases = sum(len(p.get("result", {}).get("checks", [])) for p in report["projects"])
    if not cases or cases != report["scenario_checks"]:
        errors.append("Enhancement execution report case count is inconsistent")
    for project in report["projects"]:
        result = project.get("result", {})
        checks = result.get("checks", [])
        if not checks or any(c.get("passed") is not True for c in checks):
            errors.append(project["id"] + ": missing/failed executed scenarios")
        if (
            result.get("live_model_executed") is not False
            or result.get("original_application_verified") is not False
        ):
            errors.append(project["id"] + ": CPU evidence scope is mislabeled")
    return {"projects": len(registry), "scenario_checks": cases, "failures": errors}
