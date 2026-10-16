import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const cli = join(root, 'cli/specframe.mjs');
const version = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version;
const run = (args, folder, extraEnv = {}) => spawnSync(process.execPath, [cli, ...args], {
  cwd: folder, encoding: 'utf8', env: { ...process.env, CODEX_HOME: join(folder, 'codex home'), ...extraEnv },
});

test('help/version and invalid arguments never require Python or install', () => {
  const folder = mkdtempSync(join(tmpdir(), 'specframe-npm-'));
  try {
    const env = { SPECFRAME_PYTHON: join(folder, 'missing python') };
    for (const args of [[], ['--help'], ['-h']]) assert.equal(run(args, folder, env).status, 0);
    for (const args of [['--version'], ['-v']]) {
      const result = run(args, folder, env);
      assert.equal(result.status, 0); assert.equal(result.stdout.trim(), version);
    }
    for (const args of [
      ['unknown'], ['install', '--destination'], ['install', '--hooks'],
      ['install', '--unknown', 'x'], ['install', '--destination', ''],
      ['install', '--hooks', '--destination'], ['install', '--destination', '--hooks', 'x'],
      ['install', '--destination', 'x', '--destination', 'y'],
      ['install', '--hooks', 'x', '--hooks', 'y'], ['--help', 'install'],
    ]) assert.equal(run(args, folder, env).status, 2, JSON.stringify(args));
    assert.equal(run(['install'], folder, env).status, 1);
    assert.deepEqual(readdirSync(folder), []);
  } finally { rmSync(folder, { recursive: true, force: true }); }
});

test('actual installation preserves existing hooks and state; repeated install adds no duplicate hook', () => {
  const folder = mkdtempSync(join(tmpdir(), 'specframe npm '));
  try {
    const destination = join(folder, 'custom skills', 'specframe');
    const hooks = join(folder, 'custom hooks.json');
    const existing = { otherSetting: true, hooks: { SessionStart: [{ matcher: 'startup', hooks: [{ type: 'command', command: 'existing hook' }] }] } };
    const originalHooks = JSON.stringify(existing);
    writeFileSync(hooks, originalHooks);
    mkdirSync(join(folder, '.specframe'));
    const statePath = join(folder, '.specframe', 'session.json');
    writeFileSync(statePath, '{"current":"unchanged"}\n');
    const stateBefore = readFileSync(statePath);
    const first = run(['install', '--hooks', hooks, '--destination', destination], folder);
    assert.equal(first.status, 0, first.stderr);
    const output = JSON.parse(first.stdout);
    assert.equal(output.skill, destination); assert.equal(output.hooks, hooks);
    assert.match(output.hook_trust, /not changed/);
    for (const name of ['SKILL.md', 'agents/openai.yaml', 'references/operating-contract.md', 'references/web.md', 'references/visual.md', 'scripts/state.py']) {
      assert.deepEqual(readFileSync(join(destination, name)), readFileSync(join(root, 'skills/specframe', name)), name);
    }
    const config = JSON.parse(readFileSync(hooks));
    assert.equal(config.otherSetting, true);
    assert.deepEqual(config.hooks.SessionStart[0], existing.hooks.SessionStart[0]);
    assert.equal(config.hooks.SessionStart.length, 2);
    const recovery = config.hooks.SessionStart[1];
    assert.equal(recovery.matcher, '^(compact|resume)$');
    assert.equal(recovery.hooks[0].timeout, 5);
    assert.ok(recovery.hooks[0].command.includes(join(destination, 'scripts', 'state.py')));
    assert.equal(readFileSync(`${hooks}.before-specframe`, 'utf8'), originalHooks);
    const installedHooks = readFileSync(hooks);
    writeFileSync(join(destination, 'custom.txt'), 'preserve me');
    const python = spawnSync('python3', ['-c', 'import sys; print(sys.executable)'], { encoding: 'utf8' });
    assert.equal(python.status, 0, python.stderr);
    const second = run(['install', '--destination', destination, '--hooks', hooks], folder,
      { SPECFRAME_PYTHON: python.stdout.trim() });
    assert.equal(second.status, 0, second.stderr);
    assert.deepEqual(readFileSync(hooks), installedHooks);
    assert.equal(readFileSync(`${hooks}.before-specframe`, 'utf8'), originalHooks);
    assert.equal(readFileSync(join(destination, 'custom.txt'), 'utf8'), 'preserve me');
    assert.deepEqual(readFileSync(statePath), stateBefore);
    assert.ok(!existsSync(join(folder, 'codex home')));
  } finally { rmSync(folder, { recursive: true, force: true }); }
});

test('CODEX_HOME defaults and each independent path override install only inside the isolated workspace', () => {
  const folder = mkdtempSync(join(tmpdir(), 'specframe-npm-'));
  try {
    const codexHome = join(folder, 'codex home');
    const destination = join(codexHome, 'skills', 'specframe');
    const hooks = join(codexHome, 'hooks.json');
    const first = run(['install'], folder);
    assert.equal(first.status, 0, first.stderr);
    assert.equal(JSON.parse(first.stdout).skill, destination);
    assert.equal(JSON.parse(first.stdout).hooks, hooks);
    const customDestination = join(folder, 'other skill location');
    const destinationOnly = run(['install', '--destination', customDestination], folder);
    assert.equal(destinationOnly.status, 0, destinationOnly.stderr);
    assert.ok(existsSync(join(customDestination, 'SKILL.md')));
    assert.equal(JSON.parse(destinationOnly.stdout).hooks, hooks);
    const customHooks = join(folder, 'other hooks.json');
    const hooksOnly = run(['install', '--hooks', customHooks], folder);
    assert.equal(hooksOnly.status, 0, hooksOnly.stderr);
    assert.equal(JSON.parse(hooksOnly.stdout).skill, destination);
    assert.ok(existsSync(customHooks));
  } finally { rmSync(folder, { recursive: true, force: true }); }
});
