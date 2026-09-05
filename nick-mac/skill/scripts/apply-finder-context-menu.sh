#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="$(cd "$SCRIPT_DIR/../assets" && pwd)"
WORKFLOW_SOURCE="$ASSETS_DIR/open in vs code.workflow"
WORKFLOW_TARGET="$HOME/Library/Services/open in vs code.workflow"
PBS_PLIST="$HOME/Library/Preferences/pbs.plist"
PLISTBUDDY="/usr/libexec/PlistBuddy"
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
VSCODE_SERVICE_KEY="(null) - open in vs code - runWorkflowAsService"

log() {
  printf '[nick-mac][finder] %s\n' "$*"
}

warn() {
  printf '[nick-mac][finder] WARN: %s\n' "$*" >&2
}

find_app_path() {
  local candidate
  for candidate in "$@"; do
    if [ -d "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

copy_vscode_workflow() {
  local backup

  if [ ! -d "$WORKFLOW_SOURCE" ]; then
    echo "Bundled workflow asset is missing: $WORKFLOW_SOURCE" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$WORKFLOW_TARGET")"

  if [ -d "$WORKFLOW_TARGET" ] && cmp -s \
    "$WORKFLOW_SOURCE/Contents/document.wflow" \
    "$WORKFLOW_TARGET/Contents/document.wflow"; then
    log "VS Code Quick Action already matches the bundled workflow."
    return
  fi

  if [ -e "$WORKFLOW_TARGET" ]; then
    backup="${WORKFLOW_TARGET}.bak.$(date +%Y%m%d%H%M%S)"
    mv "$WORKFLOW_TARGET" "$backup"
    log "Backed up existing workflow to $backup"
  fi

  ditto "$WORKFLOW_SOURCE" "$WORKFLOW_TARGET"
  log "Installed Finder Quick Action: open in vs code"
}

pb() {
  "$PLISTBUDDY" -c "$1" "$2" >/dev/null 2>&1
}

ensure_vscode_service_status() {
  local mode

  if [ ! -f "$PBS_PLIST" ]; then
    plutil -create xml1 "$PBS_PLIST"
  fi

  pb "Add :NSServicesStatus dict" "$PBS_PLIST" || true
  pb "Add :NSServicesStatus:'$VSCODE_SERVICE_KEY' dict" "$PBS_PLIST" || true
  pb "Add :NSServicesStatus:'$VSCODE_SERVICE_KEY':presentation_modes dict" "$PBS_PLIST" || true

  for mode in ContextMenu FinderPreview ServicesMenu TouchBar; do
    pb "Set :NSServicesStatus:'$VSCODE_SERVICE_KEY':presentation_modes:$mode true" "$PBS_PLIST" || \
      pb "Add :NSServicesStatus:'$VSCODE_SERVICE_KEY':presentation_modes:$mode bool true" "$PBS_PLIST" || true
  done

  log "Enabled the VS Code Quick Action in Finder context menus."
}

register_app_if_present() {
  local label="$1"
  local app_path="$2"

  if [ -n "$app_path" ] && [ -x "$LSREGISTER" ]; then
    "$LSREGISTER" -f "$app_path" >/dev/null 2>&1 || warn "Could not refresh Launch Services for $label."
  fi
}

main() {
  local terminal_app
  local beyond_compare_app
  local parallels_app

  copy_vscode_workflow
  ensure_vscode_service_status

  terminal_app="$(find_app_path \
    '/System/Applications/Utilities/Terminal.app' \
    '/Applications/Utilities/Terminal.app' || true)"
  register_app_if_present "Terminal" "$terminal_app"

  beyond_compare_app="$(find_app_path \
    '/Applications/Beyond Compare.app' \
    "$HOME/Applications/Beyond Compare.app" || true)"
  if [ -n "$beyond_compare_app" ]; then
    register_app_if_present "Beyond Compare" "$beyond_compare_app"
    if command -v pluginkit >/dev/null 2>&1; then
      pluginkit -e use -i com.ScooterSoftware.BeyondCompare.BCFinder >/dev/null 2>&1 || \
        warn "Beyond Compare is installed, but its Finder extension could not be enabled automatically."
    fi
  else
    warn "Beyond Compare.app is not installed. Finder will not show Compare Folders or Select Left Folder for Compare."
  fi

  parallels_app="$(find_app_path \
    '/Applications/Parallels Desktop.app' \
    "$HOME/Applications/Parallels Desktop.app" || true)"
  if [ -n "$parallels_app" ]; then
    register_app_if_present "Parallels Desktop" "$parallels_app"
  else
    warn "Parallels Desktop.app is not installed. Finder will not show Reveal in Windows."
  fi

  killall pbs >/dev/null 2>&1 || true

  log "Finder context menu configuration applied."
  log "If Finder does not refresh immediately, relaunch Finder once."
}

main "$@"
