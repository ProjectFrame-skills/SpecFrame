"""Build reproducible Agensi and independent-bridge ZIPs from current source."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ('SKILL.md', 'agents/openai.yaml', 'references/operating-contract.md',
         'references/web.md', 'references/visual.md', 'scripts/state.py')


def archive(path, files):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for name, source in sorted(files.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes())


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    version = json.loads((ROOT / 'package.json').read_text())['version']
    integration = ROOT / 'integrations/agensi'
    with tempfile.TemporaryDirectory(prefix='specframe-agensi-') as temporary:
        package = Path(temporary) / 'specframe'
        for name in FILES:
            dest = package / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / 'skills/specframe' / name, dest)
        subprocess.run(['patch', '--batch', '--fuzz=0', '-s', '-d', str(package), '-p1', '-i', str(integration / 'skill.patch')], check=True)
        shutil.copyfile(integration / 'README.md', package / 'references/setup.md')
        shutil.copyfile(integration / 'package-readme.md', package / 'README.md')
        for name in FILES[1:]:
            assert (package / name).read_bytes() == (ROOT / 'skills/specframe' / name).read_bytes(), name
        archive(output / f'specframe-{version}-agensi.zip', {
            'specframe/' + str(p.relative_to(package)): p for p in package.rglob('*') if p.is_file()})
    archive(output / f'specframe-{version}-agensi-bridge.zip', {
        name: integration / name for name in ('bridge.py', 'bind.py', 'transport.py', 'README.md')})
    files = [output / f'specframe-{version}-agensi.zip', output / f'specframe-{version}-agensi-bridge.zip']
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (output / f'specframe-{version}-agensi-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    for path in build(args.output.resolve()):
        print(path)
