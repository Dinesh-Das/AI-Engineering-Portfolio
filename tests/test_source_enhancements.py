import ast
import unittest
from pathlib import Path
from types import SimpleNamespace

from workbench_core.safety import arithmetic, parse_tool_selection

ROOT = Path(__file__).resolve().parents[1]


def source_function(path, name, namespace):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
    module = ast.fix_missing_locations(ast.Module(body=[future, function], type_ignores=[]))
    exec(compile(module, str(path), "exec"), namespace)
    return namespace[name]


class SourceSafetyTests(unittest.TestCase):
    def test_download_calls_pass_connect_and_read_deadlines(self):
        calls = []

        def request(url, **kwargs):
            calls.append((url, kwargs))
            raise TimeoutError("simulated remote stall")

        doc = SimpleNamespace(xray_url="https://fixture.invalid/xray", document_id="doc-1")
        gx = SimpleNamespace(
            documents=SimpleNamespace(lookup=lambda **kw: SimpleNamespace(documents=[doc]))
        )
        targets = [
            (
                "Colivara-deepseek-website-RAG/app.py",
                "create_pdf_from_screenshot",
                ["https://fixture.invalid/image"],
            ),
            ("groundX-doc-pipeline/groundx_utils.py", "fetch_xray_json", [gx, "bucket"]),
            (
                "groundX-doc-pipeline/groundx_utils.py",
                "get_xray_for_existing_document",
                [gx, "doc-1", "bucket"],
            ),
        ]
        for path, name, arguments in targets:
            function = source_function(
                ROOT / path, name, {"requests": SimpleNamespace(get=request)}
            )
            with self.subTest(function=name), self.assertRaises(TimeoutError):
                function(*arguments)
        self.assertEqual([call[1] for call in calls], [{"timeout": (10, 60)}] * 3)

    def test_calculator_keeps_arithmetic_and_rejects_function_execution(self):
        function = source_function(
            ROOT / "database-memory-agent/tools.py", "calculator_tool", {"arithmetic": arithmetic}
        )
        self.assertEqual(function("37*3+19*2"), "149")
        self.assertTrue(function("sum([1,2])").startswith("Error:"))

    def test_model_tool_selection_never_executes_model_text(self):
        calls = []
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **kw: SimpleNamespace(
                        choices=[SimpleNamespace(message=SimpleNamespace(content="trap()"))]
                    )
                )
            )
        )
        namespace = {
            "openai_client": client,
            "OPENAI_MODEL": "test",
            "parse_tool_selection": parse_tool_selection,
            "trap": lambda: calls.append("executed") or {"tool": "calculator_tool", "input": "2+2"},
        }
        function = source_function(
            ROOT / "database-memory-agent/planning.py", "tool_selector", namespace
        )
        self.assertEqual(function("test"), ("none", "test"))
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
