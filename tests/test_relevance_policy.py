import importlib.util
import ast
import asyncio
import re
import unittest
from pathlib import Path
from types import SimpleNamespace


class FallbackTests(unittest.TestCase):
    def test_fallback_depends_on_usable_evidence_in_both_workflows(self):
        root = Path(__file__).resolve().parents[1]
        for project in ('corrective-rag', 'firecrawl-agent'):
            path = root / project / 'relevance_policy.py'
            spec = importlib.util.spec_from_file_location(project.replace('-', '_') + '_policy', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cases = [([], True), (['no'], True), (['not sure'], True),
                     (['yes'], False), (['yes', 'no'], False), ([' YES '], False), (['not yes'], True)]
            for grades, expected in cases:
                with self.subTest(project=project, grades=grades):
                    self.assertEqual(module.needs_web_search(grades), expected)

    def test_actual_workflow_method_routes_empty_and_mixed_retrieval(self):
        root = Path(__file__).resolve().parents[1]
        for project in ('corrective-rag', 'firecrawl-agent'):
            path = root / project
            spec = importlib.util.spec_from_file_location('tested_policy', path / 'relevance_policy.py')
            policy = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(policy)
            tree = ast.parse((path / 'workflow.py').read_text(encoding='utf-8-sig'))
            owner = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'CorrectiveRAGWorkflow')
            method = next(n for n in owner.body if isinstance(n, ast.AsyncFunctionDef) and n.name == 'eval_relevance')
            method.decorator_list = []
            source = 'from __future__ import annotations\n' + ast.unparse(method)

            class Context:
                async def get(self, key):
                    return 'fixture query'

            class Model:
                def complete(self, prompt):
                    return SimpleNamespace(text=prompt)

                async def acomplete(self, prompt):
                    return self.complete(prompt)

            namespace = {'is_relevant_grade': policy.is_relevant_grade, 'needs_web_search': policy.needs_web_search,
                         're': re, 'DEFAULT_RELEVANCY_PROMPT_TEMPLATE': '{context_str}',
                         'WebSearchEvent': lambda **kw: ('web', kw), 'QueryEvent': lambda **kw: ('query', kw)}
            exec(compile(source, str(path / 'workflow.py'), 'exec'), namespace)
            for grades, route in [([], 'web'), (['yes', 'no'], 'query'), (['not yes'], 'web')]:
                nodes = [SimpleNamespace(text=grade) for grade in grades]
                result = asyncio.run(namespace['eval_relevance'](SimpleNamespace(llm=Model()), Context(), SimpleNamespace(retrieved_nodes=nodes)))
                with self.subTest(project=project, grades=grades):
                    self.assertEqual(result[0], route)
                    self.assertEqual(result[1]['relevant_text'], 'yes' if 'yes' in grades else '')


if __name__ == '__main__':
    unittest.main()
