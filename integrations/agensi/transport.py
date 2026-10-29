"""Optional one-operation transport for the exact Agensi-delivered state helper.

No network, instruction cache, product judgment or interview history. The source
pin is for the independently reviewed SpecFrame 0.1.4 helper, not arbitrary MCP code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import bridge

PIN = '112dafbbe92cbd05119286f5e9eab5a17869353e9bc6206309129413adbc87fd'
HEADER = '## File: scripts/state.py (from SpecFrame)\n\n'


def select(cwd, session):
    session = bridge.identifier(session)
    cwd = Path(cwd).resolve()
    for root in (cwd, *cwd.parents):
        binding = root / '.specframe/agensi' / (session + '.json')
        if binding.is_file():
            break
    else:
        return None
    if not binding.resolve().is_relative_to(root):
        raise ValueError('Binding outside project')
    record = json.loads(binding.read_text())
    if not isinstance(record, dict) or record.get('format') != 1 or record.get('session') != session:
        raise ValueError('Binding/session mismatch')
    for key in ('owner', 'slug', 'server'):
        bridge.identifier(record[key])
    state = (root / record['state']).resolve()
    if not state.is_relative_to(root):
        raise ValueError('State outside project')
    pending = binding.parent / ('.prepared-' + session + '.json')
    return root, record, state, pending


def prepared(selection, session):
    root, record, state, pending = selection
    if pending.is_symlink():
        raise ValueError('Unsafe preparation record')
    data = json.loads(pending.read_text())
    path = Path(data['path'])
    if (path.parent != root or not path.name.startswith('.specframe-exec-' + session + '-')
            or path.suffix != '.py' or path.is_symlink() or data.get('session') != session
            or data.get('owner') != record['owner']):
        raise ValueError('Preparation outside selected activation')
    return path


def cleanup(cwd, session):
    selection = select(cwd, session)
    if selection is None or not selection[3].exists():
        return
    path = prepared(selection, session)
    path.unlink(missing_ok=True)
    selection[3].unlink()


def prepare(event):
    selection = select(event['cwd'], event['session_id'])
    if selection is None:
        return None
    root, record, state, pending = selection
    args = event.get('tool_input', {})
    if (event.get('hook_event_name') != 'PostToolUse'
            or event.get('tool_name') != 'mcp__' + record['server'] + '__get_skill'
            or args.get('slug') != record['slug'] or args.get('file') != 'scripts/state.py'
            or args.get('confirm') or args.get('topup_usd')):
        return None
    response = event.get('tool_response', {})
    if not isinstance(response, dict) or response.get('isError'):
        cleanup(event['cwd'], event['session_id'])
        return None
    text = '\n'.join(c['text'] for c in response.get('content', []) if c.get('type') == 'text')
    if not text.startswith(HEADER):
        cleanup(event['cwd'], event['session_id'])
        return None
    source = text[len(HEADER):].encode('utf-8')
    if hashlib.sha256(source).hexdigest() != PIN:
        cleanup(event['cwd'], event['session_id'])
        return None  # No fast-path execution of an unreviewed or partial source.
    session = event['session_id']
    if pending.exists():
        path = prepared(selection, session)
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != PIN:
            raise ValueError('Prepared source changed')
    else:
        fd, name = tempfile.mkstemp(prefix='.specframe-exec-' + session + '-', suffix='.py', dir=root)
        path = Path(name)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(source)
            with pending.open('x') as stream:
                json.dump({'session': session, 'owner': record['owner'], 'path': str(path)}, stream)
        except BaseException:
            path.unlink(missing_ok=True)
            raise
    command = shlex.join([sys.executable, str(Path(__file__).resolve()), 'run', '--root', str(root), '--session', session, '--'])
    return {'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext':
        'The independently configured transport verified the exact delivered SpecFrame 0.1.4 helper and prepared one temporary operation. '
        'Do not rewrite its source. Execute ' + command + ' <helper-command> with the same stdin patch if saving. '
        'Use resume-read for resume plus read --all in one invocation. The bound owner/state are supplied automatically. '
        'The runner deletes source after the operation; lifecycle cleanup deletes unused preparations. No source survives compact/resume or a user wait. '
        'This preparation proves no product review or approval. If unavailable, the original fresh-temporary-helper path remains valid.'}}


def run(root, session, command):
    selection = select(root, session)
    if selection is None:
        raise ValueError('No selected activation')
    path = prepared(selection, session)
    try:
        if hashlib.sha256(path.read_bytes()).hexdigest() != PIN:
            raise ValueError('Prepared source changed')
        if not command or command[0] == 'hook' or any(v in ('--state', '--owner') or v.startswith(('--state=', '--owner=')) for v in command):
            raise ValueError('Use bound state/owner and a state operation')
        operations = [['resume'], ['read', '--all']] if command == ['resume-read'] else [command]
        for operation in operations:
            result = subprocess.run([sys.executable, str(path), '--state', str(selection[2]), '--owner', selection[1]['owner'], *operation])
            if result.returncode:
                return result.returncode
        return 0
    finally:
        cleanup(root, session)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    p = sub.add_parser('run')
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--session', required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    sub.add_parser('hook')
    args = parser.parse_args()
    try:
        if args.mode == 'run':
            command = args.command[1:] if args.command[:1] == ['--'] else args.command
            sys.exit(run(args.root, args.session, command))
        event = json.load(sys.stdin)
        if event.get('hook_event_name') == 'PostToolUse':
            output = prepare(event)
            if output:
                print(json.dumps(output))
        elif event.get('hook_event_name') in ('Stop', 'PreCompact', 'SessionStart', 'Interrupt', 'SessionEnd'):
            cleanup(event['cwd'], event['session_id'])
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('SpecFrame temporary transport unavailable: ' + str(error), file=sys.stderr)
        sys.exit(1)
