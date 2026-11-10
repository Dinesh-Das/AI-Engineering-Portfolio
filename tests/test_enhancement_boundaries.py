"""Regressions for untrusted data, real commands and complete project coverage."""

import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from workbench_core.artifacts import manifest
from workbench_core.cli import main
from workbench_core.io import read_json, write_json
from workbench_core.quality import paired_comparison, region_quality
from workbench_core.safety import parse_tool_selection
from workbench_core.validation import validate_schema

ROOT = Path(__file__).resolve().parents[1]


class BoundaryTests(unittest.TestCase):
    def invoke(self, arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(argv=arguments), 0)
        return json.loads(output.getvalue())

    def test_job_commands_preserve_idempotency_and_actual_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "payload.json"
            source.write_text('{"task":"verify evidence"}')
            common = [
                "job",
                "--state",
                str(root / "state.sqlite"),
                "--owner",
                "learner",
                "--id",
                "case-1",
            ]
            create = common + ["--operation", "create", "--input", str(source)]
            self.assertTrue(self.invoke(create)["created"])
            self.assertFalse(self.invoke(create)["created"])
            self.invoke(common + ["--operation", "running"])
            self.assertEqual(
                self.invoke(common + ["--operation", "completed"])["status"], "completed"
            )
            self.assertEqual(self.invoke(common + ["--operation", "show"])["version"], 3)

    def test_sql_command_binds_parameters_and_returns_limited_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.sqlite"
            connection = sqlite3.connect(path)
            try:
                connection.execute("CREATE TABLE records (value TEXT)")
                connection.executemany("INSERT INTO records VALUES (?)", [("first",), ("second",)])
                connection.commit()
            finally:
                connection.close()
            result = self.invoke(
                [
                    "query-sql",
                    "--database",
                    str(path),
                    "--sql",
                    "SELECT value FROM records WHERE value=?",
                    "--parameters",
                    '["second"]',
                ]
            )
            self.assertEqual(result["rows"], [["second"]])
            result = self.invoke(
                [
                    "query-sql",
                    "--database",
                    str(path),
                    "--sql",
                    "SELECT value FROM records",
                    "--max-rows",
                    "1",
                ]
            )
            self.assertTrue(result["truncated"])

    def test_oversized_json_write_preserves_existing_result(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            write_json(path, {"status": "original"})
            with self.assertRaises(ValueError):
                write_json(path, {"large": "x" * 100}, max_bytes=20)
            self.assertEqual(read_json(path), {"status": "original"})

    def test_json_exponent_overflow_is_rejected_at_the_file_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text('{"score":1e1000}')
            with self.assertRaises(ValueError):
                read_json(path)

    def test_non_string_tool_name_is_a_validation_error(self):
        with self.assertRaises(ValueError):
            parse_tool_selection('{"tool":[],"input":"2+2"}')

    def test_malformed_schema_fails_closed_even_in_absent_property(self):
        for schema in (
            {"enum": 1},
            {"maxLength": "many"},
            {"additionalProperties": {}},
            {"properties": {"absent": {"pattern": ".*"}}},
        ):
            with self.subTest(schema=schema), self.assertRaises(ValueError):
                validate_schema({}, schema)

    def test_extreme_numeric_inputs_are_rejected_without_overflow(self):
        with self.assertRaises(ValueError):
            paired_comparison([{"id": "a", "baseline": 10**1000, "candidate": 1}])
        with self.assertRaises(ValueError):
            region_quality([], [{"box": [0, 0, 10**1000, 10], "text": "x"}])
        self.assertEqual(validate_schema(10**1000, {"type": "integer"}), [])

    def test_artifact_boundaries_and_actual_file_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "segment.txt").write_text("first", encoding="utf-8")
            record = manifest(root, [{"id": "a", "path": "segment.txt"}])["artifacts"][0]
            (root / "segment.txt").write_text("changed", encoding="utf-8")
            with self.assertRaises(ValueError):
                manifest(root, [record])
            for path in ("../outside", "/absolute", "C:\\outside", "missing.txt"):
                with self.subTest(path=path), self.assertRaises((ValueError, OSError)):
                    manifest(root, [{"id": "a", "path": path}])

    def test_quality_cli_consumes_actual_file_and_returns_invalid_input_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "quality.json"
            path.write_text(json.dumps({"reference": "amount 375", "prediction": "amount 875"}))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(argv=["quality", "--input", str(path)]), 0)
            self.assertEqual(json.loads(output.getvalue())["character_edits"], 1)
            path.write_text('{"reference":NaN}')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(argv=["quality", "--input", str(path)]), 2)

    def test_registry_covers_109_catalog_projects_and_four_ocr(self):
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "enhancements.json").read_text(encoding="utf-8"))["projects"]
        expected = {p["id"] for p in catalog["projects"]} | {
            "Latex-OCR-Lama",
            "gemma3-ocr",
            "llama-ocr",
            "qwen-2.5VL-ocr",
        }
        self.assertEqual(len(registry), 113)
        self.assertEqual({p["id"] for p in registry}, expected)
        for project in registry:
            profile = json.loads(
                (ROOT / project["id"] / "enhancement/profile.json").read_text(encoding="utf-8")
            )
            self.assertEqual(profile["project_id"], project["id"])
            self.assertTrue(profile["experiment"])
            self.assertTrue(profile["production"])


if __name__ == "__main__":
    unittest.main()
