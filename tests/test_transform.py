import ast
import unittest

from tools.transform import harden_http, redact_literals


class HttpHardeningTests(unittest.TestCase):
    def test_multiline_unicode_and_multiple_calls_preserve_python(self):
        source = 'import requests\nlabel = "café"\na=requests.get(\n "https://example.com",\n params={"q": label},\n)\nb=requests.post("https://example.com", json={})\n'
        result, count = harden_http(source)
        ast.parse(result)
        self.assertEqual(count, 2)
        self.assertEqual(result.count('timeout=(10, 60)'), 2)

    def test_alias_is_hardened_and_existing_timeout_preserved(self):
        source = 'from requests import get as fetch\na=fetch(url)\nb=fetch(url, timeout=2)\n'
        result, count = harden_http(source)
        self.assertEqual(count, 1)
        self.assertIn('timeout=2', result)

    def test_expanded_kwargs_are_left_for_review_to_avoid_duplicate_timeout(self):
        source = 'import requests\nrequests.get(url, **options)\n'
        self.assertEqual(harden_http(source), (source, 0))

    def test_method_with_same_name_in_other_library_is_unchanged(self):
        source = 'import storage\nstorage.get(key)\n'
        self.assertEqual(harden_http(source), (source, 0))

    def test_idempotent(self):
        first, count = harden_http('import requests\nrequests.get(url)')
        self.assertEqual(count, 1)
        self.assertEqual(harden_http(first), (first, 0))


class CredentialTests(unittest.TestCase):
    def test_dictionary_credential_literals_are_redacted(self):
        token = 'aB9_' * 12
        result, count = redact_literals('{"api_key": "' + token + '"}')
        self.assertEqual(count, 1)
        self.assertNotIn(token, result)

    def test_known_token_shape_is_redacted_without_revealing_it(self):
        token = 'sk-' + 'a' * 36
        result, count = redact_literals('key = "' + token + '"')
        self.assertEqual(count, 1)
        self.assertNotIn(token, result)
        ast.parse(result)

    def test_placeholder_is_not_treated_as_actual_key(self):
        self.assertEqual(redact_literals('OPENAI_API_KEY="your-api-key"')[1], 0)


if __name__ == '__main__':
    unittest.main()
