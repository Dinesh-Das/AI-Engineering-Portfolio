"""Check handbook freshness and browser evidence without changing either artifact."""

import hashlib
import json

from .build_interview import render


def verify(root):
    errors = []
    expected, data = render(root)
    path = root / "index.html"
    if not path.is_file() or path.read_text(encoding="utf-8") != expected:
        errors.append("Interview handbook is stale; run .\\run.ps1 handbook")
    evidence = root / "docs/interview-browser-validation.json"
    checks = 0
    if not evidence.is_file():
        errors.append("Missing handbook browser evidence")
    else:
        report = json.loads(evidence.read_text(encoding="utf-8"))
        checks = len(report.get("checks", []))
        if (
            not path.is_file()
            or report.get("source_sha256") != hashlib.sha256(path.read_bytes()).hexdigest()
        ):
            errors.append("Handbook browser evidence is stale for index.html")
        if (
            report.get("passed") is not True
            or report.get("failures")
            or checks < 12
            or any(c.get("passed") is not True for c in report.get("checks", []))
        ):
            errors.append("Handbook browser scenarios did not all pass")
        if report.get("coverage") != data["coverage"]:
            errors.append("Handbook browser coverage does not match generated content")
        if report.get("console_errors") != [] or report.get("external_requests") != []:
            errors.append(
                "Handbook browser evidence must record zero console errors and external requests"
            )
    return {**data["coverage"], "browser_scenarios": checks, "failures": errors}
