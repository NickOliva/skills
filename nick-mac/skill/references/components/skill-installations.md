# Nick skill installation scopes

Every full Nick Mac run checks the skills in this Nick Skills repository. The [policy](../../assets/skill-installations/standard.json) uses each skill's requirements frontmatter as the authority, so new skills are included without maintaining a second installation list. Skills need not have a `nick-` prefix to belong to this repository.

## Inspect

Run `scripts/check-skill-installations.py` or the main comparison helper's `skill-installations` component. The helper resolves the repository from its real source location, reads installation declarations, and checks machine, repository, and ancestor discovery roots. It compares skill names as well as directory names to find renamed backups and duplicates. It checks the declared symlink resolves to `<skill-folder>/skill`, not a wrapper directory or old checkout.

Use `skill-installations:<skill-name>` IDs. Read the declaration when its intended scope is unclear or disagrees with current installation. Report missing declarations for review rather than inferring scope from where an app happened to discover the skill. A requirements-only folder has no installable implementation yet. The helper verifies paths and identity, not the quality of each skill's contents or a newly refreshed Codex discovery list.

`--repo`, `--home`, and `--codex-home` permit inspection of explicit target locations. Run on the target Mac or against its actual filesystem; do not interpret the initiating Mac's home directory as the other Mac. `~` in a declaration means the target user's home. Respect explicit installation targets; a custom Codex home or disabled-skill configuration can require an additional availability check. Review relevant Codex disabled-skill settings and other configured discovery roots without exposing unrelated configuration. Search other repository checkouts only when their locations are known and relevant; the helper does not claim to scan every repository on the computer.

## Plan, apply, verify

Show declared and observed scope, target, and source for each difference. Existing scope declarations are baseline choices; ask Nick to keep them, adopt another scope, define a new target, or defer. Put proposed installation, relinking, duplicate removal, and declaration changes into the combined plan. Merely running the audit does not authorize fixing every finding.

Nick Mac must remain repository-only: `.agents/skills/nick-mac -> ../../nick-mac/skill`. For other repository-scoped skills use portable relative links to their source. Machine-scoped links must resolve to the chosen repository checkout on that Mac; never copy another Mac's absolute home path. Preserve unique edits in a standalone copy before replacing it with a link. Move backup skill copies outside all discovery roots. Verify the correct local link before removing an old global link; unlink a symlink without deleting its target.

After accepted changes, rerun the audit and verify discovered scope in a fresh task if the current task retains an earlier skill list. Preserve explicit invocation policies. Repository symlinks reflect edits locally; another Mac must receive the repository changes separately. Do not commit, push, or alter other skill installations merely to make the audit green.
