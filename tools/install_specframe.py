#!/usr/bin/env python3
"""Install the skill and merge its opt-in, thread-scoped recovery hook."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import sys


def install(destination, hooks_path):
    source = Path(__file__).resolve().parents[1] / "skills" / "specframe"
    if destination.resolve() != source.resolve():
        shutil.copytree(source, destination, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    config = json.loads(hooks_path.read_text()) if hooks_path.exists() else {}
    command = shlex.quote(sys.executable) + " " + shlex.quote(str(destination.resolve() / "scripts" / "state.py")) + " hook"
    group = {"matcher": "^(compact|resume)$", "hooks": [{"type": "command", "command": command, "timeout": 5}]}
    groups = config.setdefault("hooks", {}).setdefault("SessionStart", [])
    if group not in groups:
        # Preserve every pre-existing hook and never alter host hook trust.
        backup = hooks_path.with_name(hooks_path.name + ".before-specframe")
        if hooks_path.exists() and not backup.exists():
            shutil.copy2(hooks_path, backup)
        groups.append(group)
        hooks_path.parent.mkdir(parents=True, exist_ok=True)
        hooks_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n")
    return {"skill": str(destination), "hooks": str(hooks_path), "hook_trust": "host review required; not changed by installer"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path.home() / ".codex" / "skills" / "specframe")
    parser.add_argument("--hooks", type=Path, default=Path.home() / ".codex" / "hooks.json")
    args = parser.parse_args()
    print(json.dumps(install(args.destination, args.hooks), ensure_ascii=False))
