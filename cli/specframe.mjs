#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = new URL('../', import.meta.url);
const metadata = JSON.parse(readFileSync(new URL('package.json', root), 'utf8'));
const args = process.argv.slice(2);
const help = `SpecFrame ${metadata.version}

Usage:
  specframe install [--destination /path/to/skills/specframe] [--hooks /path/to/hooks.json]
  specframe --version
  specframe --help

Installs the bundled Codex skill and merges its recovery hook with existing hooks.
Existing skill files are updated. Hook trust requires host review and is not changed.
Requires Python 3.11+. Set SPECFRAME_PYTHON to its executable path if needed.
Defaults: CODEX_HOME/skills/specframe and CODEX_HOME/hooks.json
          (CODEX_HOME defaults to ~/.codex)
`;

function main() {
  if (args.length === 0 || (args.length === 1 && ['--help', '-h'].includes(args[0]))) {
    console.log(help); return 0;
  }
  if (args.length === 1 && ['--version', '-v'].includes(args[0])) {
    console.log(metadata.version); return 0;
  }
  const options = new Map();
  if (args[0] !== 'install' || args.length % 2 !== 1) {
    console.error(`Invalid arguments.\n${help}`); return 2;
  }
  for (let i = 1; i < args.length; i += 2) {
    const [option, value] = args.slice(i, i + 2);
    if (!['--destination', '--hooks'].includes(option) || options.has(option) || !value || value.startsWith('-')) {
      console.error(`Invalid arguments.\n${help}`); return 2;
    }
    options.set(option, value);
  }
  const codexHome = process.env.CODEX_HOME || join(homedir(), '.codex');
  const installerArgs = [
    '--destination', options.get('--destination') ?? join(codexHome, 'skills', 'specframe'),
    '--hooks', options.get('--hooks') ?? join(codexHome, 'hooks.json'),
  ];
  const candidates = process.env.SPECFRAME_PYTHON
    ? [[process.env.SPECFRAME_PYTHON]]
    : [['python3'], ['python'], ...(process.platform === 'win32' ? [['py', '-3']] : [])];
  for (const [command, ...prefix] of candidates) {
    const probe = spawnSync(command, [...prefix, '-c',
      'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'], { windowsHide: true, stdio: 'ignore' });
    if (probe.error || probe.status !== 0) continue;
    const result = spawnSync(command, [...prefix, fileURLToPath(new URL('tools/install_specframe.py', root)),
      ...installerArgs], { windowsHide: true, stdio: 'inherit' });
    if (result.error) { console.error(result.error.message); return 1; }
    return result.status ?? 1;
  }
  console.error('Python 3.11+ was not found. Install it or set SPECFRAME_PYTHON to its executable path.');
  return 1;
}

process.exitCode = main();
