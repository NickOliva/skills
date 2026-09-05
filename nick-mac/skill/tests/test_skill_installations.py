import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check-skill-installations.py'
SPEC = importlib.util.spec_from_file_location('installations', SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'relocated-repo'
        self.home = self.root / 'different-user'
        self.source = self.repo / 'example/skill'
        self.source.mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('---\nname: example\n---\n')
        (self.source.parent / 'example-requirements.md').write_text(
            '---\nskill_name: example\ninstallation_scope: repo\n'
            'installation_target: .agents/skills/example\ninstallation_method: symlink\n---\n')
        self.target = self.repo / '.agents/skills/example'
        self.target.parent.mkdir(parents=True)

    def result(self):
        return module.audit(self.repo, self.home, self.home / '.codex', external_roots=False)[0]

    def test_relative_repo_installation_survives_different_home(self):
        self.target.symlink_to('../../example/skill')
        self.assertEqual(self.result()['status'], 'matches-recorded-value')

    def test_global_copy_found_by_skill_name_even_with_backup_directory_name(self):
        self.target.symlink_to('../../example/skill')
        backup = self.home / '.codex/skills/old-backup'
        backup.mkdir(parents=True)
        (backup / 'SKILL.md').write_text('---\nname: example\n---\n')
        self.assertIn('duplicate-installation', self.result()['issues'])
        self.assertIn('wrong-scope', self.result()['issues'])

    def test_wrong_wrapper_and_broken_links_reported(self):
        self.target.symlink_to('../../example')
        self.assertIn('wrong-link-target', self.result()['issues'])
        self.target.unlink()
        self.target.symlink_to('../../missing/skill')
        self.assertIn('broken-link', self.result()['issues'])

    def test_not_built_is_distinct_from_missing_installation(self):
        self.assertIn('missing-installation', self.result()['issues'])
        (self.source / 'SKILL.md').unlink()
        self.assertEqual(self.result()['status'], 'source-not-built')

    def test_machine_declaration_uses_target_home(self):
        p = self.source.parent / 'example-requirements.md'
        p.write_text(p.read_text().replace('installation_scope: repo', 'installation_scope: machine')
                     .replace('.agents/skills/example', '~/.codex/skills/example'))
        target = self.home / '.codex/skills/example'
        target.parent.mkdir(parents=True)
        target.symlink_to(self.source)
        self.assertEqual(self.result()['status'], 'matches-recorded-value')


if __name__ == '__main__':
    unittest.main()
