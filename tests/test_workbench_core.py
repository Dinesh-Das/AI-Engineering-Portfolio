import json
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from workbench_core.contracts import ToolRegistry, stream_state
from workbench_core.evidence import EvidenceIndex
from workbench_core.quality import (
    distillation_loss,
    paired_comparison,
    region_quality,
    text_quality,
)
from workbench_core.safety import arithmetic, parse_tool_selection
from workbench_core.state import StateStore
from workbench_core.validation import readonly_query, validate_schema


class EvidenceTests(unittest.TestCase):
    def test_tenant_filter_and_abstention_are_applied_before_ranking(self):
        index = EvidenceIndex(
            [
                {"id": "a", "tenant": "one", "text": "invoice total 375 rupees"},
                {"id": "b", "tenant": "two", "text": "secret invoice total 900 rupees"},
            ]
        )
        self.assertEqual(index.search("invoice total", "one")[0]["id"], "a")
        self.assertEqual(index.search("secret", "one"), [])
        self.assertEqual(index.search("unanswerable", "one"), [])

    def test_duplicate_ids_conflicting_versions_and_invalid_k_fail(self):
        with self.assertRaises(ValueError):
            EvidenceIndex(
                [
                    {"id": "a", "text": "first", "tenant": "x"},
                    {"id": "a", "text": "other", "tenant": "x"},
                ]
            )
        with self.assertRaises(ValueError):
            EvidenceIndex([]).search("x", "one", k=0)

    def test_persistence_keeps_version_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.json"
            index = EvidenceIndex(
                [{"id": "a", "text": "model lifecycle", "tenant": "one", "source": "page-3"}]
            )
            index.save(path)
            loaded = EvidenceIndex.load(path)
            self.assertEqual(loaded.search("lifecycle", "one")[0]["source"], "page-3")
            data = json.loads(path.read_text())
            data["schema_version"] = 999
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                EvidenceIndex.load(path)


class DurableStateTests(unittest.TestCase):
    def test_jobs_are_idempotent_owned_and_transition_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.sqlite"
            with StateStore(path) as store:
                self.assertTrue(store.create_job("run", "alice", {"topic": "RAG"}))
                self.assertFalse(store.create_job("run", "alice", {"topic": "RAG"}))
                with self.assertRaises(ValueError):
                    store.create_job("run", "alice", {"topic": "changed"})
                with self.assertRaises(PermissionError):
                    store.job("run", "bob")
                store.transition("run", "alice", "running")
            with StateStore(path) as resumed:
                self.assertEqual(resumed.job("run", "alice")["status"], "running")
                resumed.transition("run", "alice", "failed")
                resumed.transition("run", "alice", "running")
                resumed.transition("run", "alice", "completed")
                with self.assertRaises(ValueError):
                    resumed.transition("run", "alice", "running")

    def test_memory_corrects_expires_and_deletes_without_cross_tenant_leakage(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            StateStore(Path(directory) / "state.sqlite") as store,
        ):
            store.remember("alice", "preference", "old", now=10, ttl=10)
            store.remember("alice", "preference", "new", now=11, ttl=10)
            self.assertEqual(store.recall("alice", "preference", now=12)["value"], "new")
            self.assertIsNone(store.recall("bob", "preference", now=12))
            self.assertIsNone(store.recall("alice", "preference", now=22))
            store.forget("alice", "preference")
            self.assertIsNone(store.recall("alice", "preference", now=12))


class ValidationTests(unittest.TestCase):
    def test_write_tool_authorization_precedes_the_actual_operation(self):
        writes = []
        registry = ToolRegistry()
        registry.register(
            "publish",
            {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
                "additionalProperties": False,
            },
            lambda text: writes.append(text),
            write=True,
        )
        with self.assertRaises(PermissionError):
            registry.call("publish", {"text": "draft"})
        self.assertEqual(writes, [])
        registry.call("publish", {"text": "draft"}, allow_write=True)
        self.assertEqual(writes, ["draft"])

    def test_failed_incomplete_and_empty_streams_cannot_become_history(self):
        start = {"type": "start", "fixture": True}
        delta = {"type": "delta", "channel": "answer", "text": "partial"}
        self.assertFalse(stream_state([start, delta])["can_commit_history"])
        self.assertFalse(stream_state([start, delta, {"type": "error"}])["can_commit_history"])
        self.assertFalse(stream_state([start, {"type": "done"}])["can_commit_history"])
        self.assertTrue(stream_state([start, delta, {"type": "done"}])["can_commit_history"])
        with self.assertRaises(ValueError):
            stream_state([start, {"type": "done"}, delta])

    def test_arithmetic_has_no_python_execution_surface_and_has_budgets(self):
        self.assertEqual(arithmetic("(37 * 3) + 19 * 2"), 149)
        for expression in (
            "__import__('os').getcwd()",
            "2 ** 100000",
            "[1] * 9999",
            "True + 1",
            "9" * 600,
        ):
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                arithmetic(expression)

    def test_schema_distinguishes_boolean_from_integer_and_rejects_unknown_keywords(self):
        schema = {
            "type": "object",
            "required": ["total"],
            "properties": {"total": {"type": "integer"}},
            "additionalProperties": False,
        }
        self.assertEqual(validate_schema({"total": 375}, schema), [])
        self.assertTrue(validate_schema({"total": True}, schema))
        self.assertTrue(validate_schema({"total": 375, "extra": 1}, schema))
        with self.assertRaises(ValueError):
            validate_schema({}, {"$ref": "https://example.com/schema"})

    def test_model_tool_choice_uses_json_and_allowlisted_contract(self):
        self.assertEqual(
            parse_tool_selection('{"tool":"calculator_tool","input":"2+2"}'),
            ("calculator_tool", "2+2"),
        )
        for value in (
            "__import__('os').getcwd()",
            '{"tool":"delete","input":"x"}',
            '{"tool":"none","input":42}',
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_tool_selection(value)

    def test_sqlite_queries_are_readonly_and_bounded(self):
        import sqlite3

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.sqlite"
            with closing(sqlite3.connect(path)) as connection:
                connection.execute("CREATE TABLE evidence (value TEXT)")
                connection.executemany("INSERT INTO evidence VALUES (?)", [("a",), ("b",)])
                connection.commit()
            self.assertEqual(
                readonly_query(path, "SELECT value FROM evidence WHERE value = ?", ["a"])["rows"],
                [["a"]],
            )
            for statement in (
                "DELETE FROM evidence",
                "ATTACH DATABASE ':memory:' AS other",
                "SELECT load_extension('bad')",
            ):
                with self.subTest(statement=statement), self.assertRaises(ValueError):
                    readonly_query(path, statement)
            self.assertTrue(readonly_query(path, "SELECT * FROM evidence", max_rows=1)["truncated"])


class QualityTests(unittest.TestCase):
    def test_ocr_unicode_empty_and_insertions_have_explicit_metrics(self):
        self.assertEqual(text_quality("café", "cafe\u0301")["cer"], 0)
        self.assertEqual(text_quality("one two", "one too")["wer"], 0.5)
        self.assertIsNone(text_quality("", "extra")["cer"])
        self.assertEqual(text_quality("", "")["exact_match"], True)

    def test_spotting_uses_one_to_one_matching(self):
        gold = [{"box": [0, 0, 10, 10], "text": "total"}]
        prediction = gold + gold
        result = region_quality(gold, prediction)
        self.assertEqual(result["precision"], 0.5)
        self.assertEqual(result["recall"], 1)

    def test_paired_comparison_rejects_missing_pairs(self):
        result = paired_comparison(
            [{"id": "a", "baseline": 0, "candidate": 1}, {"id": "b", "baseline": 1, "candidate": 1}]
        )
        self.assertEqual(result["mean_difference"], 0.5)
        with self.assertRaises(ValueError):
            paired_comparison([{"id": "a", "candidate": 1}])

    def test_distillation_uses_stable_temperature_scaled_probabilities(self):
        self.assertAlmostEqual(
            distillation_loss([1000, 999], [1000, 999], 0, temperature=2, alpha=1)["kl_scaled"], 0
        )
        with self.assertRaises(ValueError):
            distillation_loss([1, 2], [1], 0)


if __name__ == "__main__":
    unittest.main()
