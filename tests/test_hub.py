import json
import tempfile
import unittest
from pathlib import Path

from tools.analysis import analyze_python, python_cell, sanitize_notebook, source_path
from tools.hub import build_command, get_project


class SourceBoundaryTests(unittest.TestCase):
    def test_parent_and_absolute_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for value in ('../outside.py', '/outside.py', 'C:/outside.py'):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    source_path(root, value)

    def test_project_must_be_in_catalog(self):
        with self.assertRaises(ValueError):
            get_project({'projects': []}, '../other')

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'project'
            root.mkdir()
            outside = Path(directory) / 'outside'
            outside.mkdir()
            try:
                (root / 'linked').symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('Host does not permit unprivileged symlink creation')
            with self.assertRaises(ValueError):
                source_path(root, 'linked/code.py')


class NotebookTests(unittest.TestCase):
    def test_multiline_shell_magic_inside_python_block(self):
        code = 'if True:\n    !pip install \\\n+        package-a package-b\nelse:\n    pass\n'
        cleaned, special = python_cell(code)
        self.assertTrue(special)
        self.assertIsNone(analyze_python(cleaned, 'cell')['syntax_error'])

    def test_outputs_execution_counts_and_widget_state_are_removed(self):
        notebook = {
            'nbformat': 4, 'nbformat_minor': 5,
            'metadata': {'widgets': {'saved': 'private'}, 'kernelspec': {'name': 'python3'}},
            'cells': [
                {'cell_type': 'code', 'source': ['print(1)'], 'outputs': [{'text': 'private'}],
                 'execution_count': 5, 'metadata': {'execution': {'private': True}}},
                {'cell_type': 'markdown', 'source': ['lesson'], 'metadata': {}},
            ],
        }
        clean = sanitize_notebook(notebook)
        self.assertEqual(clean['cells'][0]['outputs'], [])
        self.assertIsNone(clean['cells'][0]['execution_count'])
        self.assertNotIn('widgets', clean['metadata'])
        self.assertEqual(clean['cells'][0]['source'], ['print(1)'])
        self.assertEqual(clean['metadata']['kernelspec']['name'], 'python3')
        self.assertEqual(notebook['cells'][0]['execution_count'], 5)


class AnalysisTests(unittest.TestCase):
    def test_records_functions_models_environment_and_network_hazards(self):
        code = '''import os
import requests
from crewai import Agent
KEY = os.getenv("MODEL_API_KEY")
model = "llama3.2"
def retrieve(query):
    return requests.get("https://example.com", params={"q": query})
'''
        report = analyze_python(code, 'main.py')
        self.assertIn('MODEL_API_KEY', report['environment'])
        self.assertIn('crewai', report['imports'])
        self.assertTrue(any(f['name'] == 'retrieve' for f in report['symbols']))
        self.assertTrue(any(f['rule'] == 'network-timeout' for f in report['findings']))

    def test_syntax_failure_is_reported_without_execution(self):
        report = analyze_python('def broken(:\n', 'bad.py')
        self.assertTrue(report['syntax_error'])

    def test_existing_timeout_is_not_flagged(self):
        report = analyze_python('import requests\nrequests.get(url, timeout=10)', 'safe.py')
        self.assertFalse(any(f['rule'] == 'network-timeout' for f in report['findings']))

    def test_ui_import_marks_entry_as_ui(self):
        self.assertTrue(analyze_python('import streamlit as st\nst.title("demo")', 'app.py')['ui'])


class ExecutionTests(unittest.TestCase):
    def test_only_registered_headless_entries_can_execute(self):
        project = {'entries': [{'path': 'main.py', 'kind': 'python', 'ui': False},
                               {'path': 'app.py', 'kind': 'python', 'ui': True}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'main.py').write_text('print(1)')
            command = build_command(root, project, 'main.py')
            self.assertEqual(command[-1], str(root / 'main.py'))
            for entry in ('app.py', 'unknown.py', '../outside.py'):
                with self.subTest(entry=entry), self.assertRaises(ValueError):
                    build_command(root, project, entry)

    def test_notebook_command_disables_error_continuation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'demo.ipynb').write_text(json.dumps({'cells': []}))
            command = build_command(root, {'entries': [{'path': 'demo.ipynb', 'kind': 'notebook', 'ui': False}]}, 'demo.ipynb')
            self.assertIn('--ExecutePreprocessor.allow_errors=False', command)


if __name__ == '__main__':
    unittest.main()
