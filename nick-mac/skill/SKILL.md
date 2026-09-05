---
name: nick-mac
description: Use when the user explicitly invokes `$nick-mac` or wants to standardize Nick's personal macOS setup across computers, especially Finder context menu services and Terminal/Zsh appearance. This skill asks a yes/no question for each available component before applying anything and uses bundled scripts and assets to make the selected changes.
---

# Nick Mac

Apply or extend Nick's reusable Mac setup.

## When To Use

- The user says `$nick-mac`.
- The user wants a Mac to match Nick's preferred local setup.
- The user wants to add another personal Mac standard to this skill.

## Workflow

1. Inspect only the selected Mac and only the components that matter.
   - Read `references/components.md`.
   - Check existing apps/files before changing anything.
2. Ask one plain yes/no question per component before applying it.
   - Current components:
     - `finder-context-menu`
     - `terminal-zsh`
   - If the user already named the components they want, do not re-ask the same question.
   - If a component depends on software that is missing, say so explicitly and ask whether to continue with the parts that can still be applied.
3. Apply only the chosen components with the bundled scripts.
   - `scripts/apply-selected.sh finder-context-menu`
   - `scripts/apply-selected.sh terminal-zsh`
4. Report exactly what changed, what was skipped, and any follow-up steps.
   - Mention if Finder or Terminal may need to be reopened.
   - Mention missing prerequisites such as `Beyond Compare.app` or `Parallels Desktop.app`.

## Current Components

Load `references/components.md` when you need the details.

### `finder-context-menu`

Make Finder match the service entries discovered on Nick's current Mac:
- `New Terminal at Folder`
- `Open in VS Code`
- `Select Left Folder for Compare`

Use `scripts/apply-finder-context-menu.sh`.

Important:
- This script installs the bundled VS Code Quick Action and refreshes Finder services metadata.
- `Compare Folders` and `Select Left Folder for Compare` come from Beyond Compare.
- `Reveal in Windows` comes from Parallels Desktop.
- Do not claim the menu will match exactly if those apps are absent.

### `terminal-zsh`

Make Terminal and Zsh match Nick's current look without copying machine-specific secrets:
- Terminal default/startup profile: `Pro`
- oh-my-zsh theme: bundled `nick-mac` theme based on Nick's current `avit` setup
- no `.zshrc` secrets, database credentials, or repo-local aliases

Use `scripts/apply-terminal-zsh.sh`.

Important:
- If the target Mac already uses a different Zsh framework, inspect first and warn before replacing it.
- Preserve unrelated shell configuration when possible.

## Extending This Skill

When adding another standard:
1. Add a new section to `references/components.md`.
2. Add a dedicated `scripts/apply-<component>.sh`.
3. Register the component in `scripts/apply-selected.sh`.
4. Keep scripts idempotent and avoid bundling secrets or machine-specific credentials.
