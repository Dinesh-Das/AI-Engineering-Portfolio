"""Local-only NDJSON chat gateway with explicit fixture mode and no shared chat history."""

import argparse
import json
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .protocol import MAX_REQUEST_BYTES, MAX_OUTPUT_CHARS, ReasoningSplitter, local_opener, loopback_base, stream_ollama, validate_request

STATIC = Path(__file__).with_name('static')


def fixture_chunks(profile, scenario):
    if profile.get('thinking'):
        yield {'message': {'thinking': 'Fixture trace: this tests stream presentation; no model ran.'}}
    if scenario == 'empty':
        yield {'done': True}
        return
    text = 'Fixture response. No model inference ran. Compare one setting at a time, then record correctness and latency in your experiment notes.'
    for index in range(0, len(text), 7):
        time.sleep(0.07 if scenario == 'slow' else 0.025)
        yield {'message': {'content': text[index:index + 7]}}
        if scenario == 'failure' and index >= 14:
            raise RuntimeError('Simulated provider failure. The partial response was not added to model history.')
    yield {'done': True}


def make_server(profile, port=8765, fixture=False, ollama_host='http://127.0.0.1:11434'):
    base = loopback_base(ollama_host)
    slots = threading.BoundedSemaphore(2)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass  # Do not write user prompts or model output to request logs.

        def headers_for(self, status, content_type, length=None):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            if length is not None:
                self.send_header('Content-Length', str(length))
            self.end_headers()

        def json_response(self, status, body):
            data = json.dumps(body, allow_nan=False).encode()
            self.headers_for(status, 'application/json; charset=utf-8', len(data))
            self.wfile.write(data)

        def local_origin(self):
            port = self.server.server_port
            host = self.headers.get('Host', '')
            if host not in {f'127.0.0.1:{port}', f'localhost:{port}'}:
                return False
            origin = self.headers.get('Origin')
            return (not origin or origin == 'http://' + host) and self.headers.get('Sec-Fetch-Site') != 'cross-site'

        def do_GET(self):
            if not self.local_origin():
                return self.json_response(403, {'error': 'This learning app accepts same-origin local requests only.'})
            if self.path == '/api/config':
                return self.json_response(200, {**profile, 'fixture': fixture})
            if self.path == '/api/status':
                if fixture:
                    return self.json_response(200, {'reachable': True, 'fixture': True, 'models': [profile['model']]})
                try:
                    with local_opener().open(base + '/api/tags', timeout=3) as response:
                        data = json.loads(response.read(1024 * 1024))
                    return self.json_response(200, {'reachable': True, 'fixture': False,
                                                   'models': [m['name'] for m in data.get('models', [])]})
                except (OSError, ValueError, KeyError):
                    return self.json_response(200, {'reachable': False, 'fixture': False, 'models': []})
            routes = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'),
                      '/style.css': ('style.css', 'text/css'), '/favicon.ico': (None, 'image/x-icon')}
            if self.path not in routes:
                return self.json_response(404, {'error': 'Not found.'})
            name, mime = routes[self.path]
            data = (STATIC / name).read_bytes() if name else b''
            self.headers_for(200, mime + '; charset=utf-8', len(data))
            self.wfile.write(data)

        def event(self, body):
            self.wfile.write((json.dumps(body, allow_nan=False) + '\n').encode())
            self.wfile.flush()

        def do_POST(self):
            self.connection.settimeout(30)
            if not self.local_origin():
                return self.json_response(403, {'error': 'This learning app accepts same-origin local requests only.'})
            if self.path != '/api/chat':
                return self.json_response(404, {'error': 'Not found.'})
            if self.headers.get_content_type() != 'application/json':
                return self.json_response(415, {'error': 'Send application/json.'})
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= MAX_REQUEST_BYTES:
                    return self.json_response(413, {'error': 'Request exceeds the local app input budget.'})
                request = json.loads(self.rfile.read(size))
                payload = validate_request(request, profile)
                scenario = request.get('scenario', 'success')
                if scenario not in {'success', 'failure', 'slow', 'empty'} or (scenario != 'success' and not fixture):
                    raise ValueError('Fixture scenarios are available only in explicit fixture mode.')
            except (ValueError, TypeError, UnicodeDecodeError, TimeoutError):
                return self.json_response(400, {'error': 'Invalid request. Check message, image and parameter budgets.'})
            if not slots.acquire(blocking=False):
                return self.json_response(429, {'error': 'Two generations are already active; try again after one completes.'})
            try:
                self.headers_for(200, 'application/x-ndjson; charset=utf-8')
                self.event({'type': 'start', 'fixture': fixture, 'status': 'accepted'})
                started, first, output = time.monotonic(), None, 0
                parser = ReasoningSplitter()
                chunks = fixture_chunks(profile, scenario) if fixture else stream_ollama(payload, base)
                try:
                    for chunk in chunks:
                        message = chunk.get('message', {})
                        if not isinstance(message, dict):
                            raise RuntimeError('The model server returned an invalid message.')
                        updates = []
                        thinking = message.get('thinking') or ''
                        content = message.get('content') or ''
                        if not isinstance(thinking, str) or not isinstance(content, str):
                            raise RuntimeError('The model server returned invalid token data.')
                        if thinking:
                            updates.append(('thinking', thinking))
                        updates += parser.feed(content) if profile.get('thinking') else [('answer', content)]
                        if chunk.get('done') is True:
                            updates += parser.finish()
                        for channel, text in updates:
                            if not text:
                                continue
                            output += len(text)
                            if output > MAX_OUTPUT_CHARS:
                                raise RuntimeError('The generated output exceeded the response budget.')
                            if first is None:
                                first = round((time.monotonic() - started) * 1000)
                            self.event({'type': 'delta', 'channel': channel, 'text': text})
                        if chunk.get('done') is True:
                            self.event({'type': 'done', 'fixture': fixture, 'status': 'completed',
                                        'elapsed_ms': round((time.monotonic() - started) * 1000), 'first_token_ms': first,
                                        'input_tokens': chunk.get('prompt_eval_count'), 'output_tokens': chunk.get('eval_count')})
                            return
                    raise RuntimeError('The stream ended without a completion event.')
                finally:
                    chunks.close()
            except (ConnectionError, TimeoutError):
                pass  # Closing the provider generator releases its HTTP response on cancellation.
            except RuntimeError as error:
                try:
                    self.event({'type': 'error', 'message': str(error), 'fixture': fixture, 'status': 'failed'})
                except (ConnectionError, TimeoutError):
                    pass
            finally:
                slots.release()

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    return server


def main(profile_path=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, default=profile_path)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--fixture', action='store_true', help='Labeled offline responses; no model inference')
    parser.add_argument('--ollama-host', default='http://127.0.0.1:11434')
    args = parser.parse_args()
    if args.profile is None:
        parser.error('--profile is required')
    profile = json.loads(args.profile.read_text(encoding='utf-8'))
    server = make_server(profile, args.port, args.fixture, args.ollama_host)
    print(json.dumps({'url': f'http://127.0.0.1:{server.server_port}', 'fixture': args.fixture,
                      'project': profile.get('id', profile['title'])}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
