"""Release archives must be reproducible and contain only their intended payload."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class AgensiBuild(unittest.TestCase):
    def test_reproducible_separate_archives_preserve_policy_and_helper(self):
        with tempfile.TemporaryDirectory() as directory:
            output = []
            for name in ('a', 'b'):
                folder = Path(directory) / name
                subprocess.run([sys.executable, str(ROOT/'tools/build_agensi.py'), '--output', str(folder)], check=True, capture_output=True)
                output.append(folder)
            first = sorted(output[0].glob('*.zip'))
            for path in first:
                self.assertEqual(path.read_bytes(), (output[1]/path.name).read_bytes())
            skill = next(p for p in first if p.name.endswith('-agensi.zip'))
            with zipfile.ZipFile(skill) as bundle:
                self.assertEqual(len(bundle.namelist()), 8)
                for name in ('references/operating-contract.md', 'references/web.md', 'references/visual.md', 'scripts/state.py', 'agents/openai.yaml'):
                    self.assertEqual(bundle.read('specframe/'+name), (ROOT/'skills/specframe'/name).read_bytes())
                self.assertFalse(any('transport.py' in name or '.specframe/' in name for name in bundle.namelist()))
            bridge = next(p for p in first if p.name.endswith('-bridge.zip'))
            with zipfile.ZipFile(bridge) as bundle:
                self.assertEqual(set(bundle.namelist()), {'bridge.py', 'bind.py', 'transport.py', 'README.md'})

if __name__ == '__main__':
    unittest.main()
