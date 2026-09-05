# Components

## finder-context-menu

Goal: reproduce the Finder context menu entries visible on Nick's current Mac when right-clicking a folder.

Source of truth from Nick's current Mac:
- Terminal app NSServices expose `New Terminal at Folder` and `New Terminal Tab at Folder`.
- `~/Library/Services/open in vs code.workflow` provides `open in vs code`.
- `Beyond Compare.app` NSServices provide `Compare Folders` and `Select Left Folder for Compare`.
- `Parallels Desktop.app` NSServices provide `Reveal in Windows`.

Apply behavior:
- copy the bundled workflow to `~/Library/Services/open in vs code.workflow`
- ensure the workflow is enabled in `~/Library/Preferences/pbs.plist` for `ContextMenu`, `FinderPreview`, `ServicesMenu`, and `TouchBar`
- refresh Launch Services metadata and restart the `pbs` service daemon
- enable the Beyond Compare Finder extension if Beyond Compare is installed
- register Terminal, Beyond Compare, and Parallels with Launch Services when present

Limitations:
- `Folder Actions Setup...` is a macOS default Finder item, not managed by this skill.
- Exact menu parity requires `Beyond Compare.app`, `Parallels Desktop.app`, and `Visual Studio Code.app` to exist on the target Mac.
- This skill currently does not install licensed/commercial apps automatically.

## terminal-zsh

Goal: reproduce the Terminal/Zsh appearance visible on Nick's current Mac without copying secrets.

Source of truth from Nick's current Mac:
- Terminal profile in use: `Pro`
- oh-my-zsh theme in `.zshrc`: `avit`
- prompt styling comes from the `avit` theme, not powerlevel10k
- theme colors exported by the theme:
  - `LSCOLORS=exfxcxdxbxegedabagacad`
  - `LS_COLORS=di=34;40:ln=35;40:so=32;40:pi=33;40:ex=31;40:bd=34;46:cd=34;43:su=0;41:sg=0;46:tw=0;42:ow=0;43:`
  - `GREP_COLORS=mt=1;33`

Apply behavior:
- ensure `~/.oh-my-zsh` exists
- install bundled `assets/nick-mac.zsh-theme` to `~/.oh-my-zsh/custom/themes/nick-mac.zsh-theme`
- update `~/.zshrc` minimally so `ZSH_THEME="nick-mac"` and oh-my-zsh is sourced
- set Terminal `Startup Window Settings` and `Default Window Settings` to `Pro`

Guardrails:
- do not copy env vars, aliases, repo-specific PATH entries, or credentials from Nick's current `.zshrc`
- if a competing framework is detected in `.zshrc` and oh-my-zsh is not already in use, warn and stop unless the user explicitly wants replacement
