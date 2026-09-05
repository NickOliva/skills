---
skill_name: nick-mac
installation_scope: machine
installation_target: ~/.codex/skills/nick-mac
installation_method: symlink
---

# Nick Mac Requirements

Standardize Nick's selected Finder services and Terminal/Zsh appearance using the existing bundled scripts and assets.

- Preserve the imported skill's behavior, component selection, and explicit invocation policy.
- Keep the deployable source in `nick-mac/skill/` in this repository.
- Install `~/.codex/skills/nick-mac` as a symlink to that `skill/` directory so repository edits update the installed files directly, without copying or reinstalling.
- Preserve a backup of the original installation outside the skills discovery directory when migrating it.
- Verify copied contents and executable permissions, validate the skill and script syntax, and confirm the installed link resolves to the repository source.

The symlink updates the installed skill files. Applying Finder or Terminal settings remains a separate invocation of the skill's selected components.
