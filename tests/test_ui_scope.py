import unittest
import tempfile
from pathlib import Path

from tools.import_collection import disposition, skip_reason
from tools.learning_contract import validate_learning
from tools.hub import build_ui_command
from tools.write_docs import ensure_journal


class UIScopeTests(unittest.TestCase):
    def test_ui_projects_and_frontend_sources_are_now_in_scope(self):
        self.assertEqual(disposition('qwen3-thinking-ui')[0], 'included')
        for name in ('frontend/app/page.tsx', 'components/Chat.tsx', 'src/ui/ui_components.py',
                     'assets/logo.png', '.streamlit/config.toml', 'app/layout.tsx'):
            with self.subTest(name=name):
                self.assertIsNone(skip_reason(Path(name)))

    def test_generated_outputs_and_actual_environments_still_are_not_imported(self):
        for name in ('.env', 'frontend/node_modules/package/index.js', 'dist/app.js', '.github/workflows/deploy.yml'):
            with self.subTest(name=name):
                self.assertIsNotNone(skip_reason(Path(name)))

    def test_ui_launch_uses_only_registered_entries_and_contained_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'learning_app.py').write_text('print(1)')
            project = {'ui_entries': [{'path': 'learning_app.py', 'kind': 'learning-ui'}]}
            command, cwd = build_ui_command(root, project, 'learning_app.py')
            self.assertEqual(cwd, root)
            self.assertEqual(command[-1], str(root / 'learning_app.py'))
            with self.assertRaises(ValueError):
                build_ui_command(root, project, '../app.py')


class LearningContractTests(unittest.TestCase):
    def test_personal_learning_entries_survive_document_regeneration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            journal = root / 'LEARNING_JOURNAL.md'
            journal.write_text('My experiment: the first prediction was wrong. Keep this observation.', encoding='utf-8')
            ensure_journal(root, {'purpose': 'Understand streaming'})
            self.assertEqual(journal.read_text(encoding='utf-8'), 'My experiment: the first prediction was wrong. Keep this observation.')

    def test_a_document_missing_the_experiment_or_deployment_is_rejected(self):
        self.assertTrue(validate_learning('# Learning\n\n## The core lesson\nSome useful facts.'))

    def test_real_existing_learning_guide_meets_the_contract(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / 'simple-rag-workflow/LEARNINGS.md').read_text(encoding='utf-8')
        self.assertEqual(validate_learning(text), [])


if __name__ == '__main__':
    unittest.main()
