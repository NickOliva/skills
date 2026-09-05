#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  echo "Usage: $0 finder-context-menu|terminal-zsh [additional components...]" >&2
}

if [ "$#" -lt 1 ]; then
  usage
  exit 64
fi

for component in "$@"; do
  case "$component" in
    finder-context-menu)
      "$SCRIPT_DIR/apply-finder-context-menu.sh"
      ;;
    terminal-zsh)
      "$SCRIPT_DIR/apply-terminal-zsh.sh"
      ;;
    *)
      echo "Unknown nick-mac component: $component" >&2
      usage
      exit 64
      ;;
  esac
done
