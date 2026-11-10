import base64
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import contextlib
import io
from unittest.mock import patch

from tools.chat_lab.protocol import ReasoningSplitter, validate_request, stream_ollama
from tools.chat_lab.server import make_server

PROFILE = {'title': 'Test inference notebook', 'model': 'qwen3:4b', 'vision': True,
           'thinking': True, 'think': 'true', 'lesson': 'Trace streams.', 'experiment': 'Compare settings.'}


class StreamParsingTests(unittest.TestCase):
    def test_tags_split_at_every_possible_boundary_do_not_lose_answer(self):
        source = '<think>Check the evidence.</think>Final answer.'
        for split in range(len(source) + 1):
            parser = ReasoningSplitter()
            events = parser.feed(source[:split]) + parser.feed(source[split:]) + parser.finish()
            with self.subTest(split=split):
                self.assertEqual(''.join(t for c, t in events if c == 'thinking'), 'Check the evidence.')
                self.assertEqual(''.join(t for c, t in events if c == 'answer'), 'Final answer.')

    def test_plain_text_and_incomplete_tag_prefix_are_preserved(self):
        parser = ReasoningSplitter()
        events = parser.feed('plain <thi') + parser.finish()
        self.assertEqual(''.join(text for _, text in events), 'plain <thi')


class RequestTests(unittest.TestCase):
    def test_valid_request_separates_model_input_from_ui_metadata(self):
        result = validate_request({'model': 'qwen3:4b', 'messages': [{'role': 'user', 'content': 'Hi'}],
                                   'temperature': 0.2, 'max_tokens': 100, 'think': 'true'}, PROFILE)
        self.assertTrue(result['stream'])
        self.assertTrue(result['think'])
        self.assertEqual(result['options']['num_predict'], 100)

    def test_invalid_roles_empty_history_and_unbounded_options_fail(self):
        cases = [[], [{'role': 'tool', 'content': 'x'}], [{'role': 'user', 'content': ''}]]
        for messages in cases:
            with self.subTest(messages=messages), self.assertRaises(ValueError):
                validate_request({'messages': messages}, PROFILE)
        for option in ({'temperature': float('nan')}, {'max_tokens': True}, {'max_tokens': 999999}):
            with self.subTest(option=option), self.assertRaises(ValueError):
                validate_request({'messages': [{'role': 'user', 'content': 'x'}], **option}, PROFILE)

    def test_images_are_validated_and_text_only_profiles_reject_them(self):
        image = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'fixture').decode()
        request = {'messages': [{'role': 'user', 'content': 'Describe', 'images': [image]}]}
        self.assertEqual(validate_request(request, PROFILE)['messages'][0]['images'], [image])
        with self.assertRaises(ValueError):
            validate_request(request, {**PROFILE, 'vision': False})
        with self.assertRaises(ValueError):
            validate_request({'messages': [{'role': 'user', 'content': 'x', 'images': ['not-base64']}]}, PROFILE)

    def test_non_loopback_model_servers_are_rejected_before_network_access(self):
        with self.assertRaises(ValueError):
            list(stream_ollama({}, 'https://example.com'))


class ModelTransportTests(unittest.TestCase):
    def test_real_http_ndjson_contract_and_premature_eof(self):
        class Provider(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"message":{"thinking":"trace","content":"answer"}}\n')
                if body.get('model') != 'eof':
                    self.wfile.write(b'{"done":true,"eval_count":3}\n')

        server = ThreadingHTTPServer(('127.0.0.1', 0), Provider)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        try:
            events = list(stream_ollama({'model': 'normal'}, base))
            self.assertEqual(events[0]['message']['content'], 'answer')
            self.assertTrue(events[-1]['done'])
            with self.assertRaisesRegex(RuntimeError, 'before a completion'):
                list(stream_ollama({'model': 'eof'}, base))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_model_redirects_are_not_followed(self):
        class Provider(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers.get('Content-Length', '0')))
                self.send_response(302)
                self.send_header('Location', 'http://127.0.0.1:1/should-not-be-contacted')
                self.end_headers()

        server = ThreadingHTTPServer(('127.0.0.1', 0), Provider)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with self.assertRaisesRegex(RuntimeError, 'HTTP 302'):
                list(stream_ollama({}, f'http://127.0.0.1:{server.server_port}'))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(PROFILE, port=0, fixture=True)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, path, body=None, origin=None):
        headers = {'Content-Type': 'application/json'}
        if origin:
            headers['Origin'] = origin
        return urllib.request.urlopen(urllib.request.Request(self.base + path,
            data=json.dumps(body).encode() if body is not None else None, headers=headers), timeout=5)

    def test_fixture_stream_labels_its_origin_and_completes(self):
        with self.request('/api/chat', {'messages': [{'role': 'user', 'content': 'Hello'}]}) as response:
            events = [json.loads(line) for line in response if line.strip()]
        self.assertEqual(events[0]['type'], 'start')
        self.assertEqual(events[-1]['type'], 'done')
        self.assertTrue(events[-1]['fixture'])
        self.assertTrue(any(e.get('channel') == 'answer' for e in events))

    def test_fixture_failure_never_reports_completion(self):
        with self.request('/api/chat', {'messages': [{'role': 'user', 'content': 'Hello'}], 'scenario': 'failure'}) as response:
            events = [json.loads(line) for line in response if line.strip()]
        self.assertEqual(events[-1]['type'], 'error')
        self.assertFalse(any(e['type'] == 'done' for e in events))

    def test_cross_origin_requests_and_arbitrary_static_paths_are_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as failure:
            self.request('/api/chat', {'messages': [{'role': 'user', 'content': 'Hi'}]}, origin='https://untrusted.example')
        self.assertEqual(failure.exception.code, 403)
        for path in ('/.env', '/../../catalog.json', '/unknown'):
            with self.subTest(path=path), self.assertRaises(urllib.error.HTTPError):
                self.request(path)

    def test_config_and_static_shell_have_security_headers(self):
        with self.request('/api/config') as response:
            config = json.load(response)
            self.assertTrue(config['fixture'])
        with self.request('/') as response:
            self.assertIn("default-src 'self'", response.headers['Content-Security-Policy'])
            self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')

    def test_windows_connection_abort_is_cleanly_handled(self):
        captured = io.StringIO()
        with contextlib.redirect_stderr(captured), patch.object(self.server.RequestHandlerClass, 'event', side_effect=ConnectionAbortedError('simulated Windows disconnect')):
            with self.request('/api/chat', {'messages': [{'role': 'user', 'content': 'Disconnect'}]}) as response:
                response.read()
        self.assertEqual(captured.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
