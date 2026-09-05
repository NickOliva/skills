# Standard Decisions

The build is evolving. Record accepted changes by date and stable item ID, with the old value, chosen value, and Nick's reason when supplied. Keep computer names and unrelated device details out of this record. Values and assets live in their standard files; avoid duplicating large configuration data here.

## 2026-09-05 — Initial organization

- Nick chose iterative reviews across computers, with keep-recorded/adopt-observed/define-new choices for every differing item and one accepted alignment plan.
- The current Finder and Terminal settings are provisional review material. Inherited fixed menu, theme, and profile choices are reopened.
- Nick selected the captured FluidVoice setup as the initial voice transcription standard. Later differences remain subject to item-level decisions.
- No complete formula has been finalized. Additional tools, apps, and configuration items remain open to inclusion through review.

## 2026-09-05 — Application scope and inclusion

- Nick excluded software versions from the skill: identify tools and compare configuration, with updates managed independently. Removed captured software release/build fields and release comparisons; existing updater preferences remain configuration choices.
- Nick accepted inclusion of 1Password, Amazon Kindle, ChatGPT, Day One, Developer, Docker, Dropbox, FluidVoice, Google Chrome, Microsoft Excel, Microsoft PowerPoint, Microsoft Teams, Microsoft Word, Obsidian, Pages, Safari, TestFlight, Visual Studio Code, Xcode, and zoom.us. Each `applications:app:<bundle-id>` moved from candidate to required. Additional configuration choices remain awaiting review; FluidVoice retains its existing baseline.
- Keynote, Numbers, and Slack moved from candidate to not-required. This permits them to remain installed and does not authorize removal.
- OneDrive was initially deferred while Nick considered Office dependencies.

## 2026-09-05 — OneDrive excluded

- `applications:app:com.microsoft.OneDrive` changed from pending to not-required. Nick does not use OneDrive storage or syncing and excluded the desktop application from the standard.
- Nick separately authorized uninstalling OneDrive from the current target Mac. This does not authorize removal from other Macs; future runs review any proposed removal in the combined plan.

## 2026-09-05 — Background-task review

- Nick approved removing the stale Atlas updater and two Zoom updater tasks targeting an absent user installation. They were unloaded and their plists moved to Trash; the active Zoom installation's helpers were retained.
- Nick requested carrying these decisions into future Mac reviews. The background-items component records conditional cleanup of stale Atlas/Zoom tasks, retention of applicable Docker and installed-app helpers, and verification of the ONNX Runtime telemetry opt-out task. New targets still receive one combined plan before changes.
- Preserve `com.nick.tool-cleanup.telemetry-optouts`, which sets `ORT_DISABLE_TELEMETRY=1` at login. Use “Telemetry opt-out (ONNX Runtime)” in reports. No simple Settings display-name override was found; the functional task remains unchanged, as Nick permitted.
- The OneDrive uninstall required stopping its updater services and removing SyncReporter as well as the app. Keep this verification in future accepted uninstalls; do not confuse disabled background records with active services.
