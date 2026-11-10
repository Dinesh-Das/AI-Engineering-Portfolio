'use strict';

const $ = (id) => document.getElementById(id);
const state = { config: null, history: [], turns: [], controller: null, running: false };
const empty = $('empty');

function textNode(tag, value, className) {
  const element = document.createElement(tag);
  element.textContent = value;
  if (className) element.className = className;
  return element;
}

function status(message) { $('status').textContent = message; }

function setBusy(value) {
  state.running = value;
  $('send').disabled = value;
  $('clear').disabled = value;
  $('settings').disabled = value;
  $('image').disabled = value;
  $('prompt').disabled = value;
  $('stop').hidden = !value;
  $('composer').setAttribute('aria-busy', String(value));
}

function message(role, content = '', image = null) {
  empty.remove();
  const article = textNode('article', '', `message ${role}`);
  const heading = textNode('h2', role === 'user' ? 'You' : 'Assistant');
  const badge = textNode('span', role === 'assistant' ? 'Generating' : '', 'turn-state');
  heading.append(badge);
  article.append(heading);
  const trace = document.createElement('details');
  trace.className = 'trace';
  trace.hidden = true;
  trace.append(textNode('summary', 'Model-provided trace'));
  const traceText = textNode('div', '', 'trace-text');
  trace.append(traceText, textNode('p', 'Generated model output; not evidence of correctness.', 'hint'));
  const answer = textNode('div', content, 'answer');
  article.append(trace, answer);
  if (image) {
    const preview = document.createElement('img');
    preview.src = image;
    preview.alt = 'Image attached to this question';
    preview.className = 'attached-image';
    article.append(preview);
  }
  $('transcript').append(article);
  return { answer, trace, traceText, badge };
}

async function readImage() {
  const file = $('image').files[0];
  if (!file) return null;
  if (file.size > 3 * 1024 * 1024 || !['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) {
    throw new Error('Choose a PNG, JPEG or WebP image up to 3 MiB.');
  }
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error('The image could not be read.'));
    reader.readAsDataURL(file);
  });
}

async function* events(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let pending = '';
  try {
    while (true) {
      const part = await reader.read();
      pending += decoder.decode(part.value || new Uint8Array(), { stream: !part.done });
      if (pending.length > 300000) throw new Error('The stream exceeded its event budget.');
      let end;
      while ((end = pending.indexOf('\n')) >= 0) {
        const line = pending.slice(0, end);
        pending = pending.slice(end + 1);
        if (line.trim()) yield JSON.parse(line);
      }
      if (part.done) break;
    }
    if (pending.trim()) yield JSON.parse(pending);
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}

function recordMetrics(event) {
  $('first-token').textContent = event.first_token_ms == null ? '—' : `${event.first_token_ms} ms`;
  $('elapsed').textContent = `${event.elapsed_ms} ms`;
  $('tokens').textContent = event.output_tokens == null ? 'Not reported' : String(event.output_tokens);
  $('measurement-note').textContent = event.fixture
    ? 'Fixture timings describe the UI test, not model performance.'
    : 'Observed local inference timing. Check correctness separately.';
}

$('composer').addEventListener('submit', async (event) => {
  event.preventDefault();
  if (state.running || !state.config) return;
  const prompt = $('prompt').value.trim();
  if (!prompt) return;
  if (state.history.length >= 24) return status('Context budget reached. Export your notes and clear the conversation.');
  setBusy(true);
  $('stop').hidden = true;
  let image;
  try { image = await readImage(); } catch (error) { setBusy(false); return status(error.message); }
  const user = { role: 'user', content: prompt };
  if (image) user.images = [image.split(',', 2)[1]];
  const system = $('system').value.trim();
  const history = system ? [{ role: 'system', content: system }, ...state.history, user] : [...state.history, user];
  const request = { model: $('model').value.trim(), messages: history,
    temperature: Number($('temperature').value), max_tokens: Number($('budget').value),
    think: $('think').value, scenario: $('scenario').value };
  message('user', prompt, image);
  const responseView = message('assistant');
  const turn = { prompt, model: request.model, temperature: request.temperature, max_tokens: request.max_tokens,
    image_count: image ? 1 : 0, answer: '', trace: '', status: 'generating', fixture: state.config.fixture };
  state.turns.push(turn);
  state.controller = new AbortController();
  setBusy(true);
  status('Generating a response…');
  let completed = null;
  try {
    const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request), signal: state.controller.signal });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'The local server rejected this request.');
    }
    for await (const event of events(response)) {
      if (event.type === 'error') throw new Error(event.message);
      if (event.type === 'delta') {
        if (event.channel === 'thinking') {
          turn.trace += event.text;
          responseView.traceText.textContent = turn.trace;
          responseView.trace.hidden = false;
        } else {
          turn.answer += event.text;
          responseView.answer.textContent = turn.answer;
        }
      }
      if (event.type === 'done') completed = event;
    }
    if (!completed) throw new Error('The stream ended before it completed. The partial response was not added to history.');
    if (!turn.answer.trim()) throw new Error('The model finished without a final answer. Try a larger output budget; this turn is excluded from history.');
    turn.status = 'completed';
    turn.metrics = completed;
    state.history.push(user, { role: 'assistant', content: turn.answer });
    responseView.badge.textContent = state.config.fixture ? 'Completed · fixture' : 'Completed';
    recordMetrics(completed);
    status('Response complete. Record what changed and check the evidence.');
    $('prompt').value = '';
    $('image').value = '';
    $('attachment-status').textContent = '';
  } catch (error) {
    const stopped = error.name === 'AbortError';
    turn.status = stopped ? 'interrupted' : 'failed';
    responseView.badge.textContent = stopped ? 'Interrupted · excluded from history' : 'Failed · excluded from history';
    responseView.badge.classList.add('failed');
    status(stopped ? 'Generation stopped. Partial output stays visible and is excluded from model history.' : error.message);
  } finally {
    state.controller = null;
    setBusy(false);
    $('prompt').focus();
  }
});

$('stop').addEventListener('click', () => state.controller?.abort());
$('prompt').addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    if (!state.running) $('composer').requestSubmit();
  }
});
$('temperature').addEventListener('input', () => { $('temperature-value').value = $('temperature').value; });
$('image').addEventListener('change', () => {
  const file = $('image').files[0];
  $('attachment-status').textContent = file ? `${file.name} · ${Math.ceil(file.size / 1024)} KiB` : '';
});
$('starter').addEventListener('click', () => {
  $('prompt').value = state.config.starter || 'Explain your answer and identify what evidence would change it.';
  $('prompt').focus();
});
$('clear').addEventListener('click', () => {
  state.history = [];
  state.turns = [];
  $('transcript').replaceChildren(empty);
  $('prompt').value = '';
  $('image').value = '';
  $('attachment-status').textContent = '';
  for (const name of ['first-token', 'elapsed', 'tokens']) $(name).textContent = '—';
  status('Conversation cleared. Your experiment notes are preserved.');
  $('prompt').focus();
});
$('export').addEventListener('click', () => {
  const notes = { project: state.config.id, fixture: state.config.fixture, exported_at: new Date().toISOString(),
    learning_goal: state.config.lesson, notes: $('prediction').value, turns: state.turns };
  const blob = new Blob([JSON.stringify(notes, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `${state.config.id.replace(/[^a-z0-9-]/gi, '_')}-notes.json`;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

async function initialize() {
  $('send').disabled = true;
  try {
    const response = await fetch('/api/config');
    if (!response.ok) throw new Error('Could not load this project.');
    state.config = await response.json();
    const config = state.config;
    document.title = `${config.title} / Inference notebook`;
    $('title').textContent = config.title;
    $('description').textContent = config.description;
    $('lesson-title').textContent = config.focus;
    $('lesson').textContent = config.lesson;
    $('experiment').textContent = config.experiment;
    $('model').value = config.model;
    $('think').value = config.think || 'default';
    $('attachment-row').hidden = !config.vision;
    $('thinking-setting').hidden = !config.thinking;
    $('fixture-setting').hidden = !config.fixture;
    $('mode').textContent = config.fixture ? 'Fixture mode · no inference' : 'Local Ollama';
    const statusResponse = await fetch('/api/status');
    const connection = await statusResponse.json();
    $('connection').textContent = config.fixture ? 'Offline UI fixture · model not used'
      : connection.reachable ? `Ollama connected · ${connection.models.length} installed models` : 'Ollama unavailable · start the local model server';
    $('send').disabled = false;
  } catch (error) {
    $('mode').textContent = 'Connection error';
    status(error.message);
  }
}

initialize();
