"""Content coverage, safe rendering and command provenance for the offline handbook."""

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from tools.build_interview import build_data, inline_json, markdown, render

ROOT = Path(__file__).resolve().parents[1]


class HandbookTests(unittest.TestCase):
    def test_deliverable_contains_only_embedded_scripts_and_styles(self):
        class Assets(HTMLParser):
            def __init__(self):
                super().__init__()
                self.scripts = []
                self.stylesheets = []

            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == "script":
                    self.scripts.append(attributes)
                if tag == "link" and attributes.get("rel") == "stylesheet":
                    self.stylesheets.append(attributes)

        document, _ = render(ROOT)
        parser = Assets()
        parser.feed(document)
        self.assertEqual(len(parser.scripts), 2)
        self.assertFalse(any("src" in s for s in parser.scripts))
        self.assertEqual(parser.stylesheets, [])
        self.assertIn("connect-src 'none'", document)

    def test_build_never_reads_private_journals_or_environment_values(self):
        original = Path.read_text

        def guarded(path, *args, **kwargs):
            if path.name in {"LEARNING_JOURNAL.md", ".env", ".env.local", ".env.production"}:
                raise AssertionError("Private file read: " + str(path))
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", guarded):
            self.assertEqual(len(build_data(ROOT)["projects"]), 113)

    @classmethod
    def setUpClass(cls):
        cls.data = build_data(ROOT)

    def test_inventory_covers_every_project_folder(self):
        expected = {
            p.name
            for p in ROOT.iterdir()
            if p.is_dir()
            and (
                (p / "project.json").is_file()
                or p.name in {"Latex-OCR-Lama", "gemma3-ocr", "llama-ocr", "qwen-2.5VL-ocr"}
            )
        }
        actual = [p["id"] for p in self.data["projects"]]
        self.assertEqual(len(actual), 113)
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(set(actual)))

    def test_each_project_has_explanations_questions_and_bounded_command_claims(self):
        for project in self.data["projects"]:
            with self.subTest(project=project["id"]):
                self.assertTrue(project["purpose"])
                self.assertTrue(project["mechanism"])
                self.assertGreaterEqual(len(project["questions"]), 3)
                self.assertGreater(len(project["docs"]["learning"]), 500)
                self.assertTrue(any(c["kind"] == "offline" for c in project["commands"]))
                self.assertTrue(all(c["note"] and c["cwd"] for c in project["commands"]))
                self.assertNotIn("LEARNING_JOURNAL.md", project["embedded_files"])

    def test_topics_have_depth_and_answered_questions_at_all_levels(self):
        self.assertGreaterEqual(len(self.data["topics"]), 40)
        for topic in self.data["topics"]:
            with self.subTest(topic=topic["id"]):
                self.assertGreater(len(topic["body"]), 1500)
                self.assertEqual(
                    {q["level"] for q in topic["questions"]}, {"Foundation", "Applied", "Advanced"}
                )
                self.assertTrue(all(len(q["answer"]) > 100 for q in topic["questions"]))
                self.assertTrue(topic["sources"])

    def test_renderer_escapes_html_and_rejects_active_links(self):
        rendered = markdown(
            "<script>alert(1)</script>\n\n[x](javascript:alert(1))\n\n`<img onerror=x>`"
        )
        self.assertNotIn("<script>", rendered)
        self.assertNotIn('href="javascript:', rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("<code>", rendered)

    def test_json_cannot_terminate_the_data_script(self):
        value = {"note": "</script><script>alert(1)</script>", "unicode": "\u2028"}
        encoded = inline_json(value)
        self.assertNotIn("</script", encoded)
        self.assertEqual(json.loads(encoded), value)


if __name__ == "__main__":
    unittest.main()
