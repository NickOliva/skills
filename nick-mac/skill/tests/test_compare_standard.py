import importlib.util
import json
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts/compare-standard.py"
SPEC = importlib.util.spec_from_file_location("compare_standard", SCRIPT)
compare = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compare)


class ComparisonTests(unittest.TestCase):
    def test_plist_json_data_compares_by_value(self):
        spec = {"domain": "app", "set_preferences": {"Dictionary": {"plist_data_json": [{"word": "hello"}]}}}
        result = compare.preference_items("voice", spec, {"Dictionary": b'[ { "word": "hello" } ]'})
        self.assertEqual(result[0]["status"], "matches-recorded-value")

    def test_nested_settings_have_separate_decisions(self):
        spec = {"domain": "pbs", "set_preferences": {"Actions": {"rotate": True}}}
        result = compare.preference_items("finder", spec, {"Actions": {"rotate": False, "extra": True}})
        self.assertEqual({r["id"] for r in result}, {"finder:pbs:Actions/rotate", "finder:pbs:Actions/extra"})
        self.assertTrue(all(r["status"] == "review-difference" for r in result))

    def test_unset_settings_do_not_claim_effective_equivalence(self):
        spec = {"domain": "app", "use_version_defaults": ["Hotkey"]}
        absent = compare.preference_items("voice", spec, {})
        explicit = compare.preference_items("voice", spec, {"Hotkey": "different"})
        self.assertEqual(absent[0]["status"], "verify-effective-default")
        self.assertEqual(explicit[0]["status"], "review-override-vs-default")

    def test_unmanaged_state_is_not_exposed(self):
        spec = {"domain": "app", "set_preferences": {"Theme": "dark"}}
        actual = {"Theme": "dark", "ProviderAPIKeys": "fixture-secret", "TranscriptionHistoryEntries": b"private"}
        result = compare.preference_items("voice", spec, actual)
        self.assertNotIn("fixture-secret", json.dumps(result))
        self.assertNotIn("private", json.dumps(result))

    def test_cli_compares_a_different_computer_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prefs, apps, support = root / "prefs", root / "apps", root / "support"
            for path in [prefs, apps, support]:
                path.mkdir()
            # A synthetic skill makes this independent of Nick's evolving baseline.
            fixture_skill = root / "fixture-skill"
            (fixture_skill / "scripts").mkdir(parents=True)
            fixture_script = fixture_skill / "scripts/compare-standard.py"
            shutil.copyfile(SCRIPT, fixture_script)
            (fixture_skill / "manifest.json").write_text(json.dumps({
                "revision": 1,
                "components": [{
                    "id": "voice-transcription", "standard": "standard.json",
                    "initial_review_state": "provisional",
                }],
            }))
            (fixture_skill / "standard.json").write_text(json.dumps({
                "app": {"bundle_id": "com.FluidApp.app", "version": "test-version", "build": "test-build"},
                "set_preferences": {"CopyTranscriptionToClipboard": True},
                "use_version_defaults": [], "app_controls": {},
                "required_model_directories": [], "vocabulary_file": "vocabulary.json",
            }))
            (fixture_skill / "vocabulary.json").write_text('{"terms": []}')
            fixture = prefs / "com.FluidApp.app.plist"
            fixture.write_bytes(plistlib.dumps({"CopyTranscriptionToClipboard": False, "Unmanaged": "keep"}))
            before = fixture.read_bytes()
            result = subprocess.run([sys.executable, str(fixture_script), "--component", "voice-transcription",
                                     "--preferences-dir", str(prefs), "--applications-dir", str(apps),
                                     "--support-dir", str(support)], capture_output=True, text=True, check=True)
            report = json.loads(result.stdout)
            item = next(i for i in report["items"] if i["id"].endswith(":CopyTranscriptionToClipboard"))
            self.assertEqual(item["status"], "review-difference")
            self.assertIs(item["recorded"], True)
            self.assertIs(item["observed"], False)
            self.assertTrue(any(i["id"] == "voice-transcription:app:version" for i in report["items"]))
            self.assertEqual(fixture.read_bytes(), before)
            self.assertEqual(list(apps.iterdir()), [])
            self.assertEqual(list(support.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
