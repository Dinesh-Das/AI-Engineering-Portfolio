import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const profiles = JSON.parse(await fs.readFile(path.join(root, 'tools/ui_profiles.json'), 'utf8'));
const python = process.env.AI_PROJECTS_PYTHON || 'C:/Users/dines/AppData/Roaming/uv/python/cpython-3.12.15-windows-x86_64-none/python.exe';
const chrome = process.env.UI_TEST_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const report = { date: '2026-11-10', fixture: true, live_inference: false, projects: [], failures: [] };
const runtimeHash = createHash('sha256');
for (const name of ['__init__.py', 'protocol.py', 'server.py', 'static/app.js', 'static/index.html', 'static/style.css']) {
  runtimeHash.update(name + '\0');
  runtimeHash.update(await fs.readFile(path.join(root, 'tools/chat_lab', name)));
}
runtimeHash.update(await fs.readFile(path.join(root, 'tools/ui_profiles.json')));
report.runtime_sha256 = runtimeHash.digest('hex');
const screenshots = path.join(root, 'docs/ui-screenshots');
await fs.mkdir(screenshots, { recursive: true });

async function start(project) {
  const child = spawn(python, [path.join(root, project, 'learning_app.py'), '--fixture', '--port', '0'],
    { cwd: path.join(root, project), windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  let stderr = '';
  child.stderr.on('data', data => { stderr += data.toString(); });
  try {
    const address = await new Promise((resolve, reject) => {
      let output = '';
      const timeout = setTimeout(() => reject(new Error('Server startup deadline exceeded')), 10000);
      child.once('error', error => { clearTimeout(timeout); reject(error); });
      child.once('exit', code => { clearTimeout(timeout); reject(new Error(`Server exited (${code}): ${stderr}`)); });
      child.stdout.on('data', data => {
        output += data.toString();
        if (output.includes('\n')) {
          clearTimeout(timeout);
          try { resolve(JSON.parse(output.split('\n')[0]).url); } catch (error) { reject(error); }
        }
      });
    });
    return { address, stop: () => new Promise(resolve => {
      child.once('exit', resolve);
      child.kill();
    }), stderr: () => stderr };
  } catch (error) { child.kill(); throw error; }
}

const browser = await chromium.launch({ executablePath: chrome, headless: true });
try {
  for (const [project, profile] of Object.entries(profiles)) {
    const server = await start(project);
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true });
    const page = await context.newPage();
    const requests = [];
    const consoleErrors = [];
    page.on('pageerror', error => consoleErrors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
    page.on('request', request => {
      if (request.url().endsWith('/api/chat') && request.method() === 'POST') requests.push(request.postDataJSON());
    });
    try {
      await page.goto(server.address);
      await page.getByRole('heading', { name: profile.title, exact: true }).waitFor();
      await page.getByText('Fixture mode · no inference', { exact: true }).waitFor();
      assert.equal(await page.locator('#attachment-row').isVisible(), profile.vision);
      const sizes = [];
      for (const width of [320, 768, 1024, 1440]) {
        await page.setViewportSize({ width, height: 1000 });
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), `Horizontal overflow at ${width}px`);
        const violations = (await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations;
        assert.deepEqual(violations.map(v => ({ id: v.id, impact: v.impact })), [], `Accessibility violations at ${width}px`);
        sizes.push(width);
      }
      const tabIds = new Set();
      await page.locator('body').click({ position: { x: 2, y: 2 } });
      for (let i = 0; i < 32; i++) {
        await page.keyboard.press('Tab');
        tabIds.add(await page.evaluate(() => document.activeElement?.id));
      }
      for (const control of ['prompt', 'send', 'clear', 'export', 'model']) assert(tabIds.has(control), `Keyboard cannot reach ${control}`);
      await page.getByLabel('Your prediction and learning notes', { exact: true }).fill('Prediction: a failed or interrupted turn must not enter context.');
      if (profile.vision) {
        await page.locator('#image').setInputFiles({ name: 'pixel.png', mimeType: 'image/png',
          buffer: Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a7p8AAAAASUVORK5CYII=', 'base64') });
      }
      async function send(text, terminal = 'Completed') {
        await page.getByLabel('Your prompt', { exact: true }).fill(text);
        await page.getByRole('button', { name: 'Send prompt' }).click();
        await page.waitForFunction(expected => document.querySelector('.message.assistant:last-child .turn-state')?.textContent.includes(expected), terminal);
      }
      await send('Treat <img src=x onerror="window.fixtureXSS=true"> as literal text.');
      assert.equal(requests.at(-1).messages.length, 2);
      assert.equal(Boolean(requests.at(-1).messages.at(-1).images), profile.vision);
      assert.equal(await page.evaluate(() => window.fixtureXSS), undefined);
      if (profile.thinking) {
        assert(await page.locator('.trace').last().isVisible());
        assert.equal(await page.locator('.trace').last().getAttribute('open'), null);
      }
      await page.locator('#scenario').selectOption('failure');
      await send('Failure fixture turn', 'Failed');
      await page.locator('#scenario').selectOption('success');
      await send('After a failure');
      assert(!requests.at(-1).messages.some(m => m.content === 'Failure fixture turn'));
      await page.locator('#scenario').selectOption('empty');
      await send('No final answer fixture turn', 'Failed');
      await page.locator('#scenario').selectOption('success');
      await send('After an empty answer');
      assert(!requests.at(-1).messages.some(m => m.content === 'No final answer fixture turn'));
      await page.locator('#scenario').selectOption('slow');
      await page.getByLabel('Your prompt', { exact: true }).fill('Interrupted fixture turn');
      await page.getByRole('button', { name: 'Send prompt' }).click();
      await page.waitForFunction(() => document.querySelector('.message.assistant:last-child .answer')?.textContent.length > 0);
      await page.getByRole('button', { name: 'Stop generation' }).click();
      await page.waitForFunction(() => document.querySelector('.message.assistant:last-child .turn-state')?.textContent.includes('Interrupted'));
      await page.locator('#scenario').selectOption('success');
      await send('After interruption');
      assert(!requests.at(-1).messages.some(m => m.content === 'Interrupted fixture turn'));
      const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export notes' }).click()]);
      const exported = JSON.parse(await fs.readFile(await download.path(), 'utf8'));
      assert.equal(exported.fixture, true);
      assert(exported.turns.some(t => t.status === 'interrupted'));
      assert(exported.turns.some(t => t.status === 'failed'));
      assert.equal(exported.notes, 'Prediction: a failed or interrupted turn must not enter context.');
      const other = await context.newPage();
      await other.goto(server.address);
      await other.locator('#starter').waitFor();
      assert.equal(await other.locator('.message').count(), 0, 'Conversation leaked into another tab');
      await other.close();
      const slug = project.replaceAll(' ', '-');
      await page.screenshot({ path: path.join(screenshots, `${slug}-desktop.png`), fullPage: true });
      await page.setViewportSize({ width: 320, height: 900 });
      await page.screenshot({ path: path.join(screenshots, `${slug}-mobile.png`), fullPage: true });
      await page.getByRole('button', { name: 'Clear conversation' }).click();
      assert.equal(await page.locator('.message').count(), 0);
      assert.equal(await page.locator('#prediction').inputValue(), exported.notes);
      await page.locator('#scenario').selectOption('success');
      await send('Fresh conversation');
      assert.equal(requests.at(-1).messages.length, 2);
      await page.setViewportSize({ width: 1440, height: 1000 });
      await page.screenshot({ path: path.join(screenshots, `${slug}-overview.png`), fullPage: true });
      assert.deepEqual(consoleErrors, []);
      assert.equal(server.stderr(), '');
      report.projects.push({ id: project, passed: true, widths: sizes, accessibility_violations: 0,
        cases: ['empty', 'text-rendering', 'stream-complete', 'provider-failure', 'empty-final-answer', 'cancellation', 'history-isolation',
          'tab-isolation', 'export-notes', 'clear-conversation', 'keyboard', ...(profile.vision ? ['image-input'] : [])] });
      console.log(`PASS ${project}`);
    } catch (error) {
      report.failures.push({ project, message: error.message });
      console.log(`FAIL ${project}: ${error.message}`);
      await page.screenshot({ path: path.join(screenshots, `${project.replaceAll(' ', '-')}-failure.png`), fullPage: true }).catch(() => {});
    } finally {
      await context.close();
      await server.stop();
    }
  }
} finally {
  await browser.close();
  await fs.writeFile(path.join(root, 'docs/ui-validation.json'), JSON.stringify(report, null, 2) + '\n');
}
console.log(JSON.stringify({ passed: report.projects.length, failures: report.failures.length }));
process.exitCode = report.failures.length ? 1 : 0;
