#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="$(cd "$SCRIPT_DIR/../assets" && pwd)"
OH_MY_ZSH_DIR="$HOME/.oh-my-zsh"
THEME_SOURCE="$ASSETS_DIR/nick-mac.zsh-theme"
THEME_TARGET="$OH_MY_ZSH_DIR/custom/themes/nick-mac.zsh-theme"
ZSHRC="$HOME/.zshrc"
BACKUP_SUFFIX="nick-mac.$(date +%Y%m%d%H%M%S)"

log() {
  printf '[nick-mac][terminal-zsh] %s\n' "$*"
}

warn() {
  printf '[nick-mac][terminal-zsh] WARN: %s\n' "$*" >&2
}

backup_zshrc_once() {
  if [ -f "$ZSHRC" ] && [ -z "${NICK_MAC_ZSHRC_BACKUP_DONE:-}" ]; then
    cp "$ZSHRC" "$ZSHRC.$BACKUP_SUFFIX"
    export NICK_MAC_ZSHRC_BACKUP_DONE=1
    log "Backed up ~/.zshrc to ~/.zshrc.$BACKUP_SUFFIX"
  fi
}

prepend_line() {
  local line="$1"
  local tmp

  tmp="$(mktemp)"
  {
    printf '%s\n' "$line"
    cat "$ZSHRC"
  } > "$tmp"
  mv "$tmp" "$ZSHRC"
}

ensure_oh_my_zsh() {
  if [ -d "$OH_MY_ZSH_DIR" ]; then
    return
  fi

  if ! command -v git >/dev/null 2>&1; then
    echo "git is required to install oh-my-zsh." >&2
    exit 1
  fi

  git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git "$OH_MY_ZSH_DIR"
  log "Installed oh-my-zsh."
}

install_theme() {
  if [ ! -f "$THEME_SOURCE" ]; then
    echo "Bundled theme asset is missing: $THEME_SOURCE" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$THEME_TARGET")"

  if [ -f "$THEME_TARGET" ] && cmp -s "$THEME_SOURCE" "$THEME_TARGET"; then
    log "nick-mac theme already matches the bundled asset."
    return
  fi

  cp "$THEME_SOURCE" "$THEME_TARGET"
  log "Installed nick-mac oh-my-zsh theme."
}

has_conflicting_framework() {
  [ -f "$ZSHRC" ] || return 1

  if grep -Eq 'oh-my-zsh\.sh' "$ZSHRC"; then
    return 1
  fi

  grep -Eiq 'antigen|zinit|zplug|starship|prezto|zimfw|oh-my-posh' "$ZSHRC"
}

create_minimal_zshrc() {
  cat > "$ZSHRC" <<'EOF'
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="nick-mac"
plugins=(git)

source $ZSH/oh-my-zsh.sh
EOF
  log "Created a minimal ~/.zshrc for oh-my-zsh."
}

update_zshrc() {
  if [ ! -f "$ZSHRC" ]; then
    create_minimal_zshrc
    return
  fi

  if has_conflicting_framework && [ "${NICK_MAC_FORCE:-0}" != "1" ]; then
    warn "~/.zshrc appears to use another shell framework. Review it first, then rerun with NICK_MAC_FORCE=1 if you want to replace it."
    exit 1
  fi

  backup_zshrc_once

  if grep -Eq 'oh-my-zsh\.sh' "$ZSHRC"; then
    if grep -Eq '^ZSH_THEME=' "$ZSHRC"; then
      perl -0pi -e 's{^ZSH_THEME=.*$}{ZSH_THEME="nick-mac"}m' "$ZSHRC"
    else
      prepend_line 'ZSH_THEME="nick-mac"'
    fi

    if grep -Eq '^export ZSH=' "$ZSHRC"; then
      perl -0pi -e 's{^export ZSH=.*$}{export ZSH="\$HOME/.oh-my-zsh"}m' "$ZSHRC"
    else
      prepend_line 'export ZSH="$HOME/.oh-my-zsh"'
    fi

    log "Updated existing oh-my-zsh settings in ~/.zshrc."
    return
  fi

  prepend_line 'source $ZSH/oh-my-zsh.sh'
  prepend_line 'ZSH_THEME="nick-mac"'
  prepend_line 'export ZSH="$HOME/.oh-my-zsh"'
  log "Prepended oh-my-zsh bootstrap lines to ~/.zshrc."
}

configure_terminal_profile() {
  defaults write com.apple.Terminal "Startup Window Settings" -string Pro
  defaults write com.apple.Terminal "Default Window Settings" -string Pro
  log "Set Terminal startup/default profile to Pro."
}

main() {
  ensure_oh_my_zsh
  install_theme
  update_zshrc
  configure_terminal_profile

  if ! printf '%s' "${SHELL:-}" | grep -Eq 'zsh$'; then
    warn "The configured prompt expects zsh, but the current login shell is ${SHELL:-unknown}."
  fi

  log "Terminal/Zsh configuration applied."
  log "Open a new Terminal window to pick up the updated shell theme."
}

main "$@"
