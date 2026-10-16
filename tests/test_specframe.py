"""State/recovery contract checks; these do not grade semantic elicitation."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/specframe/scripts/state.py"
spec = importlib.util.spec_from_file_location("specframe_state", SCRIPT)
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class CurrentStateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.path = self.root / ".specframe/session-a.json"
        self.patch = {"sections": {"GOAL": "Member use", "SCOPE": "Exclude push", "CONSTRAINTS": "Existing data stays",
                                   "R1": "While suspended, member cannot reserve; viewing allowed. user-confirmed",
                                   "R2": "Unresolved staff override; affects access; decide before approval",
                                   "R3": "Other independently reviewed requirement"},
                      "focus": ["R1"], "pending": ["R2"], "next": "Clarify override"}
        state.save(self.path, "session-a", self.patch)

    def test_noop_does_not_write_or_accumulate_history(self):
        before = self.path.stat().st_mtime_ns
        self.assertFalse(state.save(self.path, "session-a", self.patch)["written"])
        self.assertEqual(before, self.path.stat().st_mtime_ns)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])
        with self.assertRaises(ValueError):
            state.save(self.path, "session-a", {"question_log": []})
        with self.assertRaises(ValueError):
            state.save(self.path, "session-a", {"change_reason": "x"})

    def test_fresh_process_resume_preserves_conditions_exclusions_pending(self):
        before = self.path.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "--state", str(self.path), "--owner", "session-a", "resume"], capture_output=True, text=True, check=True)
        restored = json.loads(result.stdout)
        for key in ("GOAL", "SCOPE", "CONSTRAINTS", "R1"):
            self.assertEqual(restored["sections"][key], self.patch["sections"][key])
        self.assertEqual(restored["pending"], ["R2"])
        self.assertEqual(restored["approval"], "draft")
        self.assertNotIn("R2", restored["sections"])
        self.assertNotIn("R3", restored["sections"])
        detail = subprocess.run([sys.executable, str(SCRIPT), "--state", str(self.path), "--owner", "session-a", "read", "R2"], capture_output=True, text=True, check=True)
        self.assertEqual(detail.stdout.strip(), "## R2\n\n" + self.patch["sections"]["R2"])
        self.assertEqual(before, self.path.read_bytes())

    def test_only_real_owner_compact_event_restores_and_does_not_write(self):
        event = {"hook_event_name": "SessionStart", "source": "compact", "session_id": "session-a", "cwd": str(self.root), "transcript_path": "/must/not/be/read"}
        before = self.path.read_bytes()
        output = state.hook(event)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        self.assertIn("While suspended", output["additionalContext"])
        self.assertIn('"pending":["R2"]', output["additionalContext"])
        self.assertNotIn("Unresolved staff override", output["additionalContext"])
        self.assertIn("read relevant pending and linked sections before dependent work", output["additionalContext"])
        self.assertNotIn("Other independently reviewed", output["additionalContext"])
        self.assertEqual(before, self.path.read_bytes())
        self.assertIsNone(state.hook(dict(event, source="startup")))
        self.assertIsNone(state.hook(dict(event, session_id="session-b")))

    def test_invalid_patch_does_not_corrupt_current_state(self):
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            state.save(self.path, "session-a", {"sections": {"R1": None}})
        self.assertEqual(before, self.path.read_bytes())
        with self.assertRaises(ValueError):
            state.save(self.path, "session-b", {"next": "Wrong task"})
        self.assertEqual(before, self.path.read_bytes())

    def test_meaning_change_clears_approval_editorial_preserves(self):
        state.save(self.path, "session-a", {}, reviewed=True)
        data = state.load(self.path)
        data["approval"] = "approved"  # Actual user confirmation belongs to the host, not this test.
        state.write_current(self.path, data)
        state.save(self.path, "session-a", {"sections": {"R1": self.patch["sections"]["R1"] + "."}}, editorial=True)
        self.assertEqual(state.load(self.path)["approval"], "approved")
        state.save(self.path, "session-a", {"sections": {"R1": "Suspended members may reserve"}})
        self.assertEqual(state.load(self.path)["approval"], "draft")
        failed = subprocess.run([sys.executable, str(SCRIPT), "--state", str(self.path), "--owner", "session-a", "approve", "--user-confirmed"], capture_output=True)
        self.assertNotEqual(failed.returncode, 0)

    def test_explicit_state_without_environment_owner_remains_usable(self):
        env = dict(os.environ)
        env.pop("CODEX_THREAD_ID", None)
        result = subprocess.run([sys.executable, str(SCRIPT), "--state", str(self.path), "read", "R1"], capture_output=True, text=True, env=env, check=True)
        self.assertIn(self.patch["sections"]["R1"], result.stdout)

    def test_stdin_patch_has_no_persistent_transport_file(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--state", str(self.path), "--owner", "session-a", "save"], input=json.dumps({"next": "Check next decision"}), capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(result.stdout)["written"])
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])


if __name__ == "__main__":
    unittest.main()
