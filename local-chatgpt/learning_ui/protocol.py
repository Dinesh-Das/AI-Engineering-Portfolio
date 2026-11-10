"""Bounded Ollama requests and incremental reasoning-tag parsing.

Official contracts: https://docs.ollama.com/api/chat and
https://docs.ollama.com/capabilities/thinking . REST images use base64 data.
"""

import base64
import binascii
import json
import math
import re
import time
import urllib.error
import urllib.parse
import urllib.request

MAX_REQUEST_BYTES = 12 * 1024 * 1024
MAX_OUTPUT_CHARS = 200000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def local_opener():
    # A loopback inference request must not be redirected or sent through an ambient proxy.
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())


class ReasoningSplitter:
    """Keep partial delimiters between chunks so final-answer text is never dropped."""

    def __init__(self):
        self.buffer = ''
        self.channel = 'answer'

    def feed(self, text):
        self.buffer += text
        events = []
        while self.buffer:
            marker = '<think>' if self.channel == 'answer' else '</think>'
            position = self.buffer.find(marker)
            if position >= 0:
                if position:
                    events.append((self.channel, self.buffer[:position]))
                self.buffer = self.buffer[position + len(marker):]
                self.channel = 'thinking' if self.channel == 'answer' else 'answer'
                continue
            keep = next((size for size in range(min(len(marker) - 1, len(self.buffer)), 0, -1)
                         if self.buffer.endswith(marker[:size])), 0)
            ready = self.buffer[:-keep] if keep else self.buffer
            if ready:
                events.append((self.channel, ready))
            self.buffer = self.buffer[-keep:] if keep else ''
            break
        return events

    def finish(self):
        events = [(self.channel, self.buffer)] if self.buffer else []
        self.buffer = ''
        return events


def _image(value):
    if not isinstance(value, str) or len(value) > 4 * 1024 * 1024:
        raise ValueError('Each image must be base64 data below 3 MiB decoded.')
    try:
        raw = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError('Image data is not valid base64.') from None
    valid = raw.startswith(b'\x89PNG\r\n\x1a\n') or raw.startswith(b'\xff\xd8\xff') or (
        raw.startswith(b'RIFF') and raw[8:12] == b'WEBP')
    if not valid:
        raise ValueError('Image must have a PNG, JPEG or WebP signature.')
    return value


def validate_request(request, profile):
    if not isinstance(request, dict):
        raise ValueError('Expected a JSON object.')
    model = request.get('model', profile['model'])
    if not isinstance(model, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./:@+-]{0,159}', model):
        raise ValueError('Enter a valid Ollama model name.')
    messages = request.get('messages')
    if not isinstance(messages, list) or not 1 <= len(messages) <= 25:
        raise ValueError('Send 1–25 messages; clear the conversation when its budget is reached.')
    clean, total_text, total_images = [], 0, 0
    for index, message in enumerate(messages):
        if not isinstance(message, dict) or message.get('role') not in {'system', 'user', 'assistant'}:
            raise ValueError('Message role must be system, user or assistant.')
        if message['role'] == 'system' and index != 0:
            raise ValueError('The system message must be first.')
        content = message.get('content')
        if not isinstance(content, str) or not content.strip() or len(content) > 12000:
            raise ValueError('Each message must contain 1–12000 characters.')
        total_text += len(content)
        record = {'role': message['role'], 'content': content}
        images = message.get('images', [])
        if not isinstance(images, list) or len(images) > 2:
            raise ValueError('Attach at most two images per message.')
        if images:
            if not profile.get('vision') or message['role'] != 'user':
                raise ValueError('This project accepts images only on user turns in a vision profile.')
            record['images'] = [_image(value) for value in images]
            total_images += sum(len(value) for value in record['images'])
        clean.append(record)
    if total_text > 48000 or total_images > 8 * 1024 * 1024:
        raise ValueError('Conversation exceeds the text/image context budget; clear it and start a new experiment.')
    if clean[-1]['role'] != 'user':
        raise ValueError('The final message must be a user turn.')
    temperature = request.get('temperature', 0.3)
    limit = request.get('max_tokens', 512)
    if type(temperature) not in {float, int} or not math.isfinite(temperature) or not 0 <= temperature <= 2:
        raise ValueError('Temperature must be between 0 and 2.')
    if type(limit) is not int or not 1 <= limit <= 2048:
        raise ValueError('Output budget must be an integer between 1 and 2048.')
    payload = {'model': model, 'messages': clean, 'stream': True,
               'options': {'temperature': temperature, 'num_predict': limit}}
    think = request.get('think', profile.get('think', 'default'))
    modes = {'default': None, 'true': True, 'false': False, 'low': 'low', 'medium': 'medium', 'high': 'high'}
    if not isinstance(think, str) or think not in modes:
        raise ValueError('Unsupported thinking mode.')
    if profile.get('thinking') and modes[think] is not None:
        payload['think'] = modes[think]
    seed = request.get('seed')
    if seed is not None:
        if type(seed) is not int or not 0 <= seed <= 2**32 - 1:
            raise ValueError('Seed must be an unsigned 32-bit integer.')
        payload['options']['seed'] = seed
    return payload


def loopback_base(value):
    parsed = urllib.parse.urlsplit(value)
    if (parsed.scheme != 'http' or parsed.hostname not in {'localhost', '127.0.0.1', '::1'}
            or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {'', '/'}):
        raise ValueError('The local learning server accepts only a loopback HTTP Ollama endpoint.')
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError('Invalid model server port.')
    return value.rstrip('/')


def stream_ollama(payload, base_url, timeout=30, deadline=120):
    base = loopback_base(base_url)
    request = urllib.request.Request(base + '/api/chat', data=json.dumps(payload, allow_nan=False).encode(),
                                     headers={'Content-Type': 'application/json'}, method='POST')
    started = time.monotonic()
    try:
        with local_opener().open(request, timeout=timeout) as response:
            received = 0
            while True:
                if time.monotonic() - started > deadline:
                    raise RuntimeError('The generation deadline was reached.')
                line = response.readline(65537)
                if not line:
                    raise RuntimeError('The model stream ended before a completion event.')
                received += len(line)
                if len(line) > 65536 or received > 4 * 1024 * 1024:
                    raise RuntimeError('The model stream exceeded its response budget.')
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    raise RuntimeError('The model server returned malformed stream data.') from None
                if not isinstance(event, dict) or event.get('error'):
                    raise RuntimeError('The model server reported a generation failure.')
                yield event
                if event.get('done') is True:
                    return
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'Ollama rejected the request (HTTP {error.code}); check the installed model and options.') from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise RuntimeError('Ollama is unreachable or timed out. Start Ollama and check the model name.') from None
